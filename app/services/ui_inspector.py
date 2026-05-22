"""
UI Inspector for Jarvis
-------------------------
Reads the active Windows application's accessibility tree and returns a
plain-text description of what's visible on screen.

Uses:
  - pywinauto (primary): reads Win32/UIA accessibility tree
  - Fallback: gets window title only (always works)

This gives the LLM "eyes" without needing a paid vision API or GPU.
"""

import os


def get_active_window_info() -> str:
    """
    Returns a text summary of the currently focused window:
    window title + list of visible UI controls (buttons, text fields, etc.)
    """
    # 1. Try pywinauto (best result)
    try:
        from pywinauto import Desktop
        desktop = Desktop(backend="uia")
        windows = desktop.windows()
        # Find foreground window
        import ctypes
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        # Match by handle
        for win in windows:
            try:
                if win.handle == hwnd:
                    title = win.window_text()
                    controls = []
                    for ctrl in win.descendants():
                        ctype = ctrl.element_info.control_type or ""
                        ctext = ctrl.window_text().strip()
                        if ctext and len(ctext) < 80:
                            controls.append(f"  [{ctype}] {ctext}")
                    controls = controls[:40]  # cap at 40 items
                    result = f"ACTIVE WINDOW: {title}\n"
                    if controls:
                        result += "VISIBLE CONTROLS:\n" + "\n".join(controls)
                    else:
                        result += "(no readable controls)"
                    return result
            except Exception:
                continue
    except Exception:
        pass

    # 2. Fallback: just get the title bar text
    try:
        import ctypes
        buf = ctypes.create_unicode_buffer(256)
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        ctypes.windll.user32.GetWindowTextW(hwnd, buf, 256)
        return f"ACTIVE WINDOW: {buf.value or '(unknown)'}"
    except Exception:
        return "(unable to read screen)"


def click_ui_element(text: str) -> bool:
    """
    Searches the active window's accessibility tree for a control containing
    the given text, finds its bounding rectangle, and clicks its center.
    Returns True if clicked, False if not found.
    """
    try:
        import pyautogui
        from pywinauto import Desktop
        import ctypes
        
        desktop = Desktop(backend="uia")
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        
        for win in desktop.windows():
            if win.handle == hwnd:
                text_lower = text.lower()
                for ctrl in win.descendants():
                    ctext = ctrl.window_text().strip()
                    if ctext and text_lower in ctext.lower():
                        rect = ctrl.rectangle()
                        # Calculate center
                        cx = rect.left + (rect.right - rect.left) // 2
                        cy = rect.top + (rect.bottom - rect.top) // 2
                        pyautogui.click(cx, cy)
                        return True
    except Exception as e:
        print(f"[UI Click Error] {e}")
    return False


def get_screen_text_summary() -> str:
    """
    Returns a combined string with window info + clipboard content.
    Useful for providing the LLM maximum context before generating code.
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
