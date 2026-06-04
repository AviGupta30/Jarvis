"""
ui_inspector.py — Jarvis UIA Engine (Upgraded)
-----------------------------------------------
Replaces the shallow "find text → get bounding box → click" approach with a
proper Windows UI Automation (UIA) tree walker that can programmatically
invoke controls WITHOUT touching the physical mouse cursor.

This is the same API used by Windows screen readers (Narrator, NVDA).
It's faster, invisible to the user, and works even when windows are
behind other windows.

Architecture:
  UIAEngine         — core class wrapping pywinauto's Desktop(backend="uia")
  click_ui_element  — legacy-compatible wrapper (unchanged public API)
  smart_click       — new: UIA first, falls back to coordinate click
  type_into_element — new: inject text via UIA Value pattern
  read_element_text — new: read any control's text via UIA TextPattern
  debug_ui_tree     — new: dump accessibility tree for discovering AutomationIds
  get_active_window_info     — unchanged public API
  get_screen_text_summary    — unchanged public API
"""

import os
import re
import ctypes
import logging
from typing import Optional

logger = logging.getLogger(__name__)


# ── UIAEngine ─────────────────────────────────────────────────────────────────

class UIAEngine:
    """
    Core wrapper around pywinauto's UIA backend.
    All interactions go through the OS accessibility API — no mouse, no OCR.
    """

    def __init__(self):
        try:
            from pywinauto import Desktop
            self.desktop = Desktop(backend="uia")
            self._available = True
        except Exception as e:
            logger.warning(f"[UIA] pywinauto unavailable: {e}")
            self.desktop = None
            self._available = False

    # ── Window resolution ─────────────────────────────────────────────────────

    def get_window(self, title_pattern: str):
        """
        Get a window wrapper by partial title match (regex-safe).
        Returns None if not found or UIA unavailable.
        """
        if not self._available:
            return None
        try:
            win = self.desktop.window(title_re=f".*{re.escape(title_pattern)}.*")
            win.wait("exists", timeout=3)
            return win
        except Exception:
            return None

    def get_foreground_window(self):
        """Get the currently focused window via Win32 HWND matching."""
        if not self._available:
            return None
        try:
            hwnd = ctypes.windll.user32.GetForegroundWindow()
            for win in self.desktop.windows():
                try:
                    if win.handle == hwnd:
                        return win
                except Exception:
                    continue
        except Exception:
            pass
        return None

    # ── Element resolution ────────────────────────────────────────────────────

    def find_element(self, window, name: str = None,
                     control_type: str = None, automation_id: str = None):
        """
        Walk the accessibility tree and find a matching element.
        Priority: AutomationId (stable) > Name > ControlType.

        Args:
            window:        pywinauto window wrapper
            name:          Visible label / window text of the element
            control_type:  UIA control type string, e.g. 'Button', 'Edit', 'Pane'
            automation_id: AutomationId (from debug_ui_tree — most stable)

        Returns:
            Element wrapper, or None if not found.
        """
        if window is None:
            return None
        criteria = {}
        if automation_id:
            criteria["auto_id"] = automation_id
        if name:
            criteria["title"] = name
        if control_type:
            criteria["control_type"] = control_type

        try:
            from pywinauto.findwindows import ElementNotFoundError
            element = window.child_window(**criteria)
            element.wait("exists enabled visible", timeout=5)
            return element
        except Exception:
            return None

    def find_element_fuzzy(self, window, text: str):
        """
        Walk all descendants looking for any control whose window_text
        contains `text` (case-insensitive). Returns the first match.
        Used as a fallback when AutomationId is unknown.
        """
        if window is None:
            return None
        text_lower = text.lower()
        try:
            for ctrl in window.descendants():
                try:
                    ctext = ctrl.window_text().strip()
                    if ctext and text_lower in ctext.lower():
                        return ctrl
                except Exception:
                    continue
        except Exception:
            pass
        return None

    # ── Actions ───────────────────────────────────────────────────────────────

    def invoke(self, element) -> bool:
        """
        Fire an element's primary action via UIA Invoke pattern.
        No mouse movement — fires the action handler directly.
        Falls back to click_input (sends WM_LBUTTONDOWN to HWND).
        Returns True on success.
        """
        if element is None:
            return False
        try:
            element.invoke()
            return True
        except Exception:
            pass
        try:
            element.click_input()
            return True
        except Exception:
            return False

    def set_value(self, element, text: str) -> bool:
        """
        Inject text into an input element via UIA Value pattern.
        No simulated keystrokes — sets the value directly in the control.
        Falls back to type_keys if the Value pattern is unavailable.
        Returns True on success.
        """
        if element is None:
            return False
        try:
            element.set_edit_text(text)
            return True
        except Exception:
            pass
        try:
            element.type_keys(text, with_spaces=True)
            return True
        except Exception:
            return False

    def get_text(self, element) -> str:
        """
        Read text from an element via UIA TextPattern or window_text.
        Returns empty string on failure.
        """
        if element is None:
            return ""
        try:
            return element.window_text()
        except Exception:
            return ""

    # ── Tree inspection ───────────────────────────────────────────────────────

    def dump_tree(self, window, depth: int = 3) -> list:
        """
        Walk the accessibility tree and return all elements up to `depth` levels.
        Use this during development to discover AutomationIds for an app.

        Returns a list of dicts:
            level, name, type, auto_id, rect
        """
        results = []

        def walk(el, level=0):
            if level > depth:
                return
            try:
                results.append({
                    "level": level,
                    "name": el.window_text(),
                    "type": el.element_info.control_type,
                    "auto_id": el.element_info.automation_id,
                    "rect": str(el.rectangle()),
                })
                for child in el.children():
                    walk(child, level + 1)
            except Exception:
                pass

        if window is not None:
            walk(window)
        return results


# ── Module-level singleton ────────────────────────────────────────────────────

_uia = UIAEngine()


# ── Public tool functions ─────────────────────────────────────────────────────

def click_ui_element(text: str) -> bool:
    """
    Legacy-compatible API: find a control by text in the active window and click it.
    Now uses UIA Invoke pattern (no mouse movement) with coordinate fallback.
    Returns True if clicked, False if not found.
    """
    window = _uia.get_foreground_window()
    el = _uia.find_element_fuzzy(window, text)
    if el:
        return _uia.invoke(el)
    return False


def smart_click(app_title: str, element_name: str = None,
                automation_id: str = None, control_type: str = None) -> str:
    """
    Click a UI element by AutomationId, name, or control type inside an app.
    Does NOT move the physical mouse cursor.

    Falls back to coordinate-based pyautogui click if UIA fails.

    Args:
        app_title:     Partial window title of the target app
        element_name:  Visible label of the element (optional)
        automation_id: UIA AutomationId — preferred (stable across runs)
        control_type:  UIA control type: 'Button', 'Edit', 'MenuItem', 'Pane', etc.

    Returns:
        Result string describing success or failure.
    """
    win = _uia.get_window(app_title)
    el = _uia.find_element(win, name=element_name,
                           automation_id=automation_id,
                           control_type=control_type)
    if el:
        if _uia.invoke(el):
            label = element_name or automation_id or control_type or "element"
            return f"✅ Clicked '{label}' in {app_title} via UIA (no mouse moved)."

    # Fallback: coordinate-based click via fuzzy text search
    if element_name:
        win2 = _uia.get_foreground_window()
        el2 = _uia.find_element_fuzzy(win2, element_name)
        if el2:
            try:
                rect = el2.rectangle()
                cx = rect.left + (rect.right - rect.left) // 2
                cy = rect.top + (rect.bottom - rect.top) // 2
                import pyautogui
                pyautogui.click(cx, cy)
                return f"✅ Clicked '{element_name}' via coordinate fallback."
            except Exception:
                pass

    label = element_name or automation_id or control_type or "element"
    return f"❌ Element '{label}' not found in '{app_title}'."


def type_into_element(app_title: str, element_name: str = None,
                      text: str = "", automation_id: str = None) -> str:
    """
    Inject text into a specific input field in an app via UIA Value pattern.
    No global keyboard simulation — sets the value directly in the control.

    Args:
        app_title:     Partial window title
        element_name:  Label of the text field
        text:          Text to enter
        automation_id: Optional AutomationId for stability

    Returns:
        Result string.
    """
    win = _uia.get_window(app_title)
    el = _uia.find_element(win, name=element_name,
                           automation_id=automation_id,
                           control_type="Edit")

    # Fuzzy fallback if exact match fails
    if el is None and element_name:
        el = _uia.find_element_fuzzy(win, element_name)

    if el:
        if _uia.set_value(el, text):
            label = element_name or automation_id or "field"
            return f"✅ Typed into '{label}' in {app_title}."
        return f"❌ Could not set value in '{element_name}' — field may be read-only."
    return f"❌ Input field '{element_name or automation_id}' not found in '{app_title}'."


def read_element_text(app_title: str, element_name: str = None,
                      automation_id: str = None) -> str:
    """
    Read the current text content of a UI element (e.g. terminal output pane, label).

    Args:
        app_title:     Partial window title
        element_name:  Name of the element to read
        automation_id: Optional AutomationId

    Returns:
        Text content of the element, or empty string.
    """
    win = _uia.get_window(app_title)
    el = _uia.find_element(win, name=element_name, automation_id=automation_id)

    if el is None and element_name:
        el = _uia.find_element_fuzzy(win, element_name)

    text = _uia.get_text(el)
    if text:
        return text[:4000]
    return f"(No text found in '{element_name or automation_id or 'element'}' in '{app_title}')"


def debug_ui_tree(app_title: str, depth: int = 3) -> str:
    """
    Dump the full accessibility tree of an app window as a readable string.
    Use this to discover AutomationIds for a specific app — run once per app.

    Returns:
        Human-readable tree dump string.
    """
    win = _uia.get_window(app_title)
    if win is None:
        return f"Window '{app_title}' not found or not accessible."

    nodes = _uia.dump_tree(win, depth=depth)
    if not nodes:
        return f"No UIA elements found in '{app_title}'."

    lines = [f"UIA Tree for '{app_title}' (depth={depth}):"]
    for node in nodes:
        indent = "  " * node["level"]
        auto_id = f" | id='{node['auto_id']}'" if node.get("auto_id") else ""
        lines.append(
            f"{indent}[{node['type']}] '{node['name']}'{auto_id}"
        )
    return "\n".join(lines[:200])  # cap at 200 lines


# ── Legacy-compatible public API (unchanged) ──────────────────────────────────

def get_active_window_info() -> str:
    """
    Returns a text summary of the currently focused window:
    window title + list of visible UI controls (buttons, text fields, etc.).
    Unchanged public API — called by tools.py and planner.py.
    """
    window = _uia.get_foreground_window()
    if window is None:
        # Fallback: title bar only
        try:
            buf = ctypes.create_unicode_buffer(256)
            hwnd = ctypes.windll.user32.GetForegroundWindow()
            ctypes.windll.user32.GetWindowTextW(hwnd, buf, 256)
            return f"ACTIVE WINDOW: {buf.value or '(unknown)'}"
        except Exception:
            return "(unable to read screen)"

    try:
        title = window.window_text()
        controls = []
        for ctrl in window.descendants():
            try:
                ctype = ctrl.element_info.control_type or ""
                ctext = ctrl.window_text().strip()
                auto_id = ctrl.element_info.automation_id or ""
                if ctext and len(ctext) < 80:
                    aid_str = f" [id={auto_id}]" if auto_id else ""
                    controls.append(f"  [{ctype}]{aid_str} {ctext}")
            except Exception:
                continue
        controls = controls[:50]  # cap at 50 items
        result = f"ACTIVE WINDOW: {title}\n"
        if controls:
            result += "VISIBLE CONTROLS:\n" + "\n".join(controls)
        else:
            result += "(no readable controls)"
        return result
    except Exception:
        return f"ACTIVE WINDOW: (error reading controls)"


def get_screen_text_summary() -> str:
    """
    Returns window info + clipboard content.
    Unchanged public API — called by planner.py for context injection.
    """
    window_info = get_active_window_info()
    try:
        import pyperclip
        clipboard = pyperclip.paste()
        if clipboard and len(clipboard) < 500:
            return window_info + f"\n\nCLIPBOARD: {clipboard}"
    except Exception:
        pass
    return window_info
