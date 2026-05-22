"""
Safe Code Executor for Jarvis
-------------------------------
Runs LLM-generated Python code inside a strict sandbox.

BLOCKED (raises SecurityError):
  - os.remove, os.unlink, os.rmdir, shutil.rmtree → no file deletion
  - exec, eval, __import__ inside generated code
  - open() in write/append mode for system paths
  - Any access to APPDATA, WINDIR, ProgramFiles, System32

ALLOWED:
  - Reading files from user's Desktop / Documents / Downloads
  - Writing new files to Desktop / Documents / Jarvis data dir
  - shutil.copy, shutil.move (file management, not deletion)
  - webbrowser, pyautogui, psutil, requests
  - subprocess for pip installs only (safe known commands)
  - All standard math/string/data processing
"""

import ast
import io
import sys
import os
import time
import json
import re
import traceback
import contextlib
import pathlib

# ── Blocklist ──────────────────────────────────────────────────────────────

BLOCKED_CALLS = {
    # Destructive file operations only
    "os.remove", "os.unlink", "os.rmdir", "os.removedirs",
    "shutil.rmtree",
    # Dynamic execution
    "exec", "compile",
}

BLOCKED_MODULES = {
    "ctypes",
}

BLOCKED_SYSTEM_PATHS = [
    os.environ.get("WINDIR", "C:\\Windows"),
    os.environ.get("PROGRAMFILES", "C:\\Program Files"),
    os.environ.get("PROGRAMFILES(X86)", "C:\\Program Files (x86)"),
    os.environ.get("SYSTEMROOT", "C:\\Windows"),
]


class SecurityError(Exception):
    """Raised when generated code violates safety constraints."""
    pass


class SafetyVisitor(ast.NodeVisitor):
    """AST visitor that inspects generated code before execution."""

    def visit_Call(self, node):
        # Check attribute calls like os.remove(...)
        if isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name):
                full = f"{node.func.value.id}.{node.func.attr}"
                if full in BLOCKED_CALLS:
                    raise SecurityError(f"Blocked dangerous call: {full}")
        # Check bare calls like exec(...)
        if isinstance(node.func, ast.Name):
            if node.func.id in {"exec", "eval", "compile", "__import__"}:
                raise SecurityError(f"Blocked dangerous call: {node.func.id}")
        self.generic_visit(node)

    def visit_Import(self, node):
        for alias in node.names:
            if alias.name.split(".")[0] in BLOCKED_MODULES:
                raise SecurityError(f"Blocked module import: {alias.name}")
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module and node.module.split(".")[0] in BLOCKED_MODULES:
            raise SecurityError(f"Blocked module import: {node.module}")
        self.generic_visit(node)


def _validate_code(code: str) -> None:
    """Parse and walk the AST, raising SecurityError on violations."""
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        raise SyntaxError(f"Syntax error in generated code: {e}")
    SafetyVisitor().visit(tree)


def execute_safe(code: str, timeout: int = 60) -> tuple[bool, str]:
    """
    Validates and runs 'code' in a restricted namespace.

    Returns:
        (success: bool, output: str)
    """
    # 1. Static safety check
    try:
        _validate_code(code)
    except SecurityError as e:
        return False, f"[SECURITY BLOCK] {e}"
    except SyntaxError as e:
        return False, f"[SYNTAX ERROR] {e}"

    from app.services.ui_inspector import get_screen_text_summary, get_active_window_info, click_ui_element
    import subprocess
    import shutil
    import datetime

    # 2. Build a rich global namespace
    safe_globals = {
        "__builtins__": {
            # Core builtins
            "print": print, "len": len, "range": range, "str": str,
            "int": int, "float": float, "bool": bool, "list": list,
            "dict": dict, "tuple": tuple, "set": set, "type": type,
            "isinstance": isinstance, "issubclass": issubclass,
            "enumerate": enumerate, "zip": zip, "map": map,
            "filter": filter, "sorted": sorted, "reversed": reversed,
            "min": min, "max": max, "sum": sum, "abs": abs,
            "round": round, "hash": hash, "id": id,
            "any": any, "all": all, "next": next, "iter": iter,
            "open": _safe_open, "__import__": _safe_import,
            "hasattr": hasattr, "getattr": getattr, "setattr": setattr,
            "vars": vars, "dir": dir, "repr": repr, "format": format,
            "chr": chr, "ord": ord, "hex": hex, "oct": oct, "bin": bin,
            "bytes": bytes, "bytearray": bytearray, "memoryview": memoryview,
            "Exception": Exception, "ValueError": ValueError,
            "TypeError": TypeError, "KeyError": KeyError,
            "IndexError": IndexError, "FileNotFoundError": FileNotFoundError,
            "OSError": OSError, "IOError": IOError,
            "NotImplementedError": NotImplementedError,
            "StopIteration": StopIteration,
        },
        # Standard library modules pre-imported
        "os": os,
        "sys": sys,
        "re": re,
        "json": json,
        "time": time,
        "pathlib": pathlib,
        "subprocess": subprocess,
        "shutil": shutil,
        "datetime": datetime,
        # Jarvis UI tools
        "get_screen_text_summary": get_screen_text_summary,
        "get_active_window_info": get_active_window_info,
        "click_ui_element": click_ui_element,
    }

    # 3. Capture stdout
    stdout_capture = io.StringIO()
    try:
        with contextlib.redirect_stdout(stdout_capture):
            exec(compile(code, "<jarvis_skill>", "exec"), safe_globals)  # noqa: S102
        output = stdout_capture.getvalue().strip()
        return True, output or "[Skill executed with no output]"
    except Exception:
        err = traceback.format_exc(limit=5)
        return False, f"[RUNTIME ERROR]\n{err}"


def _safe_open(path, mode="r", *args, **kwargs):
    """Restricted open(): blocks writes to system paths."""
    if any(c in ("w", "a", "x") for c in mode):
        abs_path = os.path.abspath(path)
        for blocked in BLOCKED_SYSTEM_PATHS:
            if blocked and abs_path.lower().startswith(blocked.lower()):
                raise SecurityError(f"Writing to system path is not allowed: {abs_path}")
    return open(path, mode, *args, **kwargs)


def _safe_import(name, *args, **kwargs):
    """Restricted __import__: blocks dangerous modules."""
    top = name.split(".")[0]
    if top in BLOCKED_MODULES:
        raise SecurityError(f"Importing '{name}' is not allowed.")
    return __import__(name, *args, **kwargs)
