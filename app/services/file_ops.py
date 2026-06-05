"""
file_ops.py — Jarvis Full File System Operations (Step 4)
----------------------------------------------------------
Completely isolated module. Safe to develop and test independently.
Nothing in existing Jarvis code breaks until tools.py explicitly imports it.

SAFETY RULES built-in:
  - All paths are resolved through _resolve_path() which expands shortcuts like
    "Desktop", "Downloads", "Documents", "Pictures" automatically.
  - delete_file() uses send2trash (Recycle Bin) — NEVER permanent deletion.
  - System paths (C:\\Windows, Program Files, etc.) are blocked from deletion.
  - File reads are capped at 10,000 chars to prevent LLM token overflow.

Public API:
  read_file(path)                      → str  read a text or PDF file
  write_file(path, content)            → str  create or overwrite a file
  append_to_file(path, content)        → str  append content to a file
  list_directory(path)                 → str  list files/folders with sizes
  move_file(src, dst)                  → str  move or rename a file
  delete_file(path)                    → str  move to Recycle Bin
  search_files(name, root_dir)         → str  recursive search by name/pattern
  create_folder(path)                  → str  create folder (anywhere, not just Desktop)
"""

import os
import re
import glob
import shutil
from pathlib import Path
from datetime import datetime

# ── Path Resolution ────────────────────────────────────────────────────────────

_USER_HOME = Path.home()

# Friendly shortcuts → actual paths
_SHORTCUTS: dict[str, Path] = {
    "desktop":      _USER_HOME / "Desktop",
    "downloads":    _USER_HOME / "Downloads",
    "documents":    _USER_HOME / "Documents",
    "pictures":     _USER_HOME / "Pictures",
    "music":        _USER_HOME / "Music",
    "videos":       _USER_HOME / "Videos",
    "home":         _USER_HOME,
    "~":            _USER_HOME,
    "onedrive":     _USER_HOME / "OneDrive",
}

# System paths — never allowed to be deleted
_PROTECTED_ROOTS = [
    "c:\\windows",
    "c:\\program files",
    "c:\\program files (x86)",
    "c:\\programdata",
    "c:\\system32",
]


def _resolve_path(raw: str) -> Path:
    """
    Convert a user-friendly path to an absolute Path object.
    Handles:
      - "Desktop/todo.txt"  →  C:\\Users\\user\\Desktop\\todo.txt
      - "~/notes.txt"       →  C:\\Users\\user\\notes.txt
      - "C:\\absolute\\path"  →  unchanged
      - "todo.txt"          →  C:\\Users\\user\\Desktop\\todo.txt  (defaults to Desktop)
    """
    raw = raw.strip().strip('"').strip("'")

    # Check if starts with a known shortcut (case-insensitive)
    parts = raw.replace("\\", "/").split("/")
    first = parts[0].lower()
    if first in _SHORTCUTS:
        base = _SHORTCUTS[first]
        rest = parts[1:]
        return base / "/".join(rest) if rest else base
    elif raw.startswith("~"):
        return Path(os.path.expanduser(raw))
    elif os.path.isabs(raw):
        return Path(raw)
    else:
        # Relative path — default to Desktop for convenience
        return _USER_HOME / "Desktop" / raw


def _fmt_size(bytes_: int) -> str:
    """Human-readable file size."""
    if bytes_ < 1024:
        return f"{bytes_} B"
    elif bytes_ < 1024 ** 2:
        return f"{bytes_ / 1024:.1f} KB"
    elif bytes_ < 1024 ** 3:
        return f"{bytes_ / 1024**2:.1f} MB"
    else:
        return f"{bytes_ / 1024**3:.1f} GB"


# ── Read File ──────────────────────────────────────────────────────────────────

def read_file(path: str) -> str:
    """
    Read and return the contents of a text file or PDF.
    Long files are automatically summarized via LLM for easy consumption.
    Supports: .txt, .md, .py, .json, .csv, .html, .log, .pdf, .docx
    """
    resolved = _resolve_path(path)

    if not resolved.exists():
        return f"File not found: '{resolved}'. Check the filename and location."

    if not resolved.is_file():
        return f"'{resolved}' is a directory, not a file. Use list_directory to see its contents."

    suffix = resolved.suffix.lower()

    try:
        # PDF support
        if suffix == ".pdf":
            try:
                import pdfplumber
                with pdfplumber.open(str(resolved)) as pdf:
                    text = "\n".join(
                        page.extract_text() or "" for page in pdf.pages
                    )
                text = text.strip()
                if not text:
                    return f"PDF '{resolved.name}' appears to have no extractable text (may be a scanned image)."
                return _maybe_summarize(resolved.name, text, 10000)
            except ImportError:
                return "pdfplumber is not installed. Run: pip install pdfplumber"

        # Word document (.docx) support
        elif suffix == ".docx":
            try:
                from docx import Document
                doc = Document(str(resolved))
                text = "\n".join(para.text for para in doc.paragraphs)
                return _maybe_summarize(resolved.name, text, 10000)
            except ImportError:
                return "python-docx is not installed. Run: pip install python-docx"

        # Image support via Gemini Vision
        elif suffix in [".png", ".jpg", ".jpeg", ".webp"]:
            try:
                import base64
                from app.services.screen_vision import _call_gemini_vision
                with open(resolved, "rb") as img_file:
                    b64_data = base64.b64encode(img_file.read()).decode("utf-8")
                
                system_prompt = "You are an expert image analyzer. Describe this image in immense detail so a text-based AI can fully understand its contents, text, layout, and meaning."
                user_query = f"Please describe this uploaded image ({resolved.name})."
                
                description = _call_gemini_vision(b64_data, system_prompt, user_query)
                return f"[Image Analysis of '{resolved.name}']\n\n{description}"
            except ImportError:
                return f"Cannot analyze image '{resolved.name}': screen_vision module unavailable."
            except Exception as e:
                return f"Failed to analyze image '{resolved.name}': {e}"

        # All other text-based files
        else:
            with open(resolved, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            if not content.strip():
                return f"'{resolved.name}' is empty."
            return _maybe_summarize(resolved.name, content, 10000)

    except PermissionError:
        return f"Permission denied: cannot read '{resolved}'."
    except Exception as e:
        return f"Could not read '{resolved}': {e}"


def _maybe_summarize(filename: str, content: str, cap: int) -> str:
    """
    For files longer than 1000 chars, generate an LLM summary AND return the raw content.
    Appends a summary header so Jarvis can speak it, with the full content available below.
    """
    raw = content[:cap]
    if len(content) <= 1000:
        return f"[Content of '{filename}']\n\n{raw}"

    # Try LLM summary
    try:
        from groq import Groq
        from app.core.config import settings
        client = Groq(api_key=settings.GROQ_API_KEY)
        prompt = (
            f"Summarize the key points of this file called '{filename}' in 3 concise sentences. "
            f"Ready to speak aloud.\n\nCONTENT:\n{content[:3000]}"
        )
        resp = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.3
        )
        summary = resp.choices[0].message.content.strip()
        return f"[Summary of '{filename}']\n{summary}\n\n[Full Content]\n{raw}"
    except Exception:
        return f"[Content of '{filename}']\n\n{raw}"


# ── Write / Create File ────────────────────────────────────────────────────────

def write_file(path: str, content: str) -> str:
    """
    Create a new file or overwrite an existing one with the given content.
    Automatically creates parent directories if they don't exist.
    Path shortcuts ('Desktop', 'Downloads', etc.) are resolved automatically.
    """
    resolved = _resolve_path(path)
    try:
        resolved.parent.mkdir(parents=True, exist_ok=True)
        with open(resolved, "w", encoding="utf-8") as f:
            f.write(content)
        return f"File created: '{resolved.name}' at {resolved.parent}"
    except PermissionError:
        return f"Permission denied: cannot write to '{resolved}'."
    except Exception as e:
        return f"Could not create file: {e}"


# ── Append to File ─────────────────────────────────────────────────────────────

def append_file(path: str, content: str) -> str:
    """
    Append content to an existing file. Creates the file if it doesn't exist.
    A newline is always added before the new content.
    """
    resolved = _resolve_path(path)
    try:
        resolved.parent.mkdir(parents=True, exist_ok=True)
        with open(resolved, "a", encoding="utf-8") as f:
            f.write("\n" + content)
        return f"Appended to '{resolved.name}'."
    except PermissionError:
        return f"Permission denied: cannot write to '{resolved}'."
    except Exception as e:
        return f"Could not append to file: {e}"


# ── List Directory ─────────────────────────────────────────────────────────────

def list_directory(path: str = "Desktop") -> str:
    """
    List all files and folders inside a directory.
    Returns name, type (file/folder), size, and modification date.
    Defaults to Desktop if no path given.
    """
    resolved = _resolve_path(path)

    if not resolved.exists():
        return f"Directory not found: '{resolved}'. Did you mean Desktop, Downloads, or Documents?"

    if not resolved.is_dir():
        return f"'{resolved}' is a file, not a folder. Use read_file to read it."

    try:
        items = sorted(resolved.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
        if not items:
            return f"The '{resolved.name}' folder is empty."

        lines = [f"Contents of {resolved} ({len(items)} items):\n"]
        for item in items:
            try:
                if item.is_dir():
                    count = len(list(item.iterdir()))
                    lines.append(f"  📁  {item.name}/  ({count} items inside)")
                else:
                    size = _fmt_size(item.stat().st_size)
                    mtime = datetime.fromtimestamp(item.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
                    lines.append(f"  📄  {item.name}  [{size}]  Modified: {mtime}")
            except Exception:
                lines.append(f"  ??  {item.name}  (could not read metadata)")

        return "\n".join(lines)

    except PermissionError:
        return f"Permission denied: cannot read '{resolved}'."
    except Exception as e:
        return f"Could not list directory: {e}"


# ── Move / Rename File ─────────────────────────────────────────────────────────

def move_file(src: str, dst: str) -> str:
    """
    Move a file to a new location, or rename it.
    Both src and dst support path shortcuts (Desktop, Downloads, etc.).
    Examples:
      move_file("Desktop/notes.txt", "Documents/notes.txt")  — move
      move_file("Desktop/notes.txt", "Desktop/my_notes.txt") — rename
    """
    src_path = _resolve_path(src)
    dst_path = _resolve_path(dst)

    if not src_path.exists():
        return f"Source not found: '{src_path}'."

    try:
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src_path), str(dst_path))
        action = "Renamed" if src_path.parent == dst_path.parent else "Moved"
        return f"{action} '{src_path.name}' → '{dst_path}'."
    except PermissionError:
        return f"Permission denied: cannot move '{src_path}'."
    except Exception as e:
        return f"Could not move file: {e}"


# ── Delete File (Recycle Bin) ──────────────────────────────────────────────────

def delete_file(path: str) -> str:
    """
    Move a file or folder to the Recycle Bin (NOT permanent delete).
    Blocks deletion of critical system paths.
    """
    resolved = _resolve_path(path)

    # Safety check — block system paths
    resolved_lower = str(resolved).lower()
    for protected in _PROTECTED_ROOTS:
        if resolved_lower.startswith(protected):
            return f"BLOCKED: Cannot delete system path '{resolved}'. This is a protected location."

    if not resolved.exists():
        return f"File not found: '{resolved}'."

    try:
        import send2trash
        send2trash.send2trash(str(resolved))
        return f"Moved '{resolved.name}' to Recycle Bin."
    except ImportError:
        return "send2trash is not installed. Run: pip install send2trash"
    except Exception as e:
        return f"Could not delete '{resolved}': {e}"


# ── Search Files ───────────────────────────────────────────────────────────────

def search_files(name: str, root_dir: str = "home") -> str:
    """
    Recursively search for files matching a name or pattern within a directory.
    Supports wildcards: e.g., name="*.pdf" or name="report*"
    root_dir defaults to the user's home directory.
    Results capped at 30 matches.
    """
    root = _resolve_path(root_dir)

    if not root.exists():
        return f"Search directory not found: '{root}'."

    try:
        # If name contains wildcards, use glob; otherwise do a partial-name search
        pattern = name if any(c in name for c in ["*", "?", "["]) else f"*{name}*"
        matches = list(root.rglob(pattern))

        # Filter out system/hidden dirs
        matches = [
            m for m in matches
            if not any(part.startswith(".") for part in m.parts)
            and "\\AppData\\" not in str(m)
        ]

        if not matches:
            return f"No files matching '{name}' found in '{root}'."

        lines = [f"Found {len(matches[:30])} result(s) for '{name}' in '{root}':"]
        for m in matches[:30]:
            size = _fmt_size(m.stat().st_size) if m.is_file() else "folder"
            lines.append(f"  {'📁' if m.is_dir() else '📄'}  {m}  [{size}]")

        if len(matches) > 30:
            lines.append(f"  ... and {len(matches) - 30} more.")

        return "\n".join(lines)

    except PermissionError:
        return f"Permission denied searching in '{root}'."
    except Exception as e:
        return f"Search failed: {e}"


# ── Create Folder ──────────────────────────────────────────────────────────────

def create_folder(path: str) -> str:
    """
    Create a new folder. Supports path shortcuts (Desktop, Downloads, etc.).
    Creates all intermediate directories automatically.
    """
    resolved = _resolve_path(path)
    try:
        resolved.mkdir(parents=True, exist_ok=True)
        return f"Created folder: '{resolved.name}' at '{resolved.parent}'."
    except PermissionError:
        return f"Permission denied: cannot create folder at '{resolved}'."
    except Exception as e:
        return f"Could not create folder: {e}"


# ── Bulk Rename ──────────────────────────────────────────────────────────────────

def bulk_rename(directory: str, find: str, replace: str) -> str:
    """
    Rename all files in a folder whose names contain 'find', replacing it with 'replace'.
    Example: bulk_rename('Downloads', '.txt', '_backup.txt')
    Returns a report of all renamed files.
    """
    dir_path = _resolve_path(directory)
    if not dir_path.exists() or not dir_path.is_dir():
        return f"Directory not found: '{dir_path}'."
    renamed = []
    skipped = []
    for f in dir_path.iterdir():
        if f.is_file() and find in f.name:
            new_name = f.name.replace(find, replace)
            new_path = f.parent / new_name
            try:
                f.rename(new_path)
                renamed.append(f"{f.name} → {new_name}")
            except Exception as e:
                skipped.append(f"{f.name}: {e}")
    if not renamed and not skipped:
        return f"No files containing '{find}' found in '{dir_path.name}'."
    lines = [f"Bulk rename complete in '{dir_path.name}':"]
    for r in renamed:
        lines.append(f"  ✓ {r}")
    for s in skipped:
        lines.append(f"  ✗ {s}")
    return "\n".join(lines)


# ── Diff Files ───────────────────────────────────────────────────────────────────

def diff_files(path1: str, path2: str) -> str:
    """
    Compare two text files and return a summary of what changed.
    Shows added and removed lines.
    """
    import difflib
    p1 = _resolve_path(path1)
    p2 = _resolve_path(path2)
    for p in (p1, p2):
        if not p.exists():
            return f"File not found: '{p}'."
    try:
        lines1 = open(p1, encoding="utf-8", errors="replace").readlines()
        lines2 = open(p2, encoding="utf-8", errors="replace").readlines()
        diff = list(difflib.unified_diff(lines1, lines2, fromfile=p1.name, tofile=p2.name, lineterm=""))
        if not diff:
            return f"The files '{p1.name}' and '{p2.name}' are identical."
        added = sum(1 for l in diff if l.startswith('+') and not l.startswith('++'))
        removed = sum(1 for l in diff if l.startswith('-') and not l.startswith('--'))
        diff_text = "\n".join(diff[:60])  # cap at 60 diff lines
        return (
            f"Comparing '{p1.name}' vs '{p2.name}':\n"
            f"+{added} lines added, -{removed} lines removed.\n\n{diff_text}"
        )
    except Exception as e:
        return f"Could not compare files: {e}"
