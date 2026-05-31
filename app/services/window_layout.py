"""
window_layout.py — Isolated Window Layout & Window Manager
==========================================================
COMPLETELY ISOLATED — no pygetwindow, pure Win32 ctypes only.
Safe to modify without affecting any other Jarvis functionality.

FIXES:
  - Correct WINFUNCTYPE callback return types (int, not bool)
  - Proper Z-order enumeration to find target windows reliably
  - Strips the Jarvis overlay + system tasks from targeting
  - Works whether called from voice agent or backend server

PUBLIC API:
  adjust_active_window(position, width_percent, height_percent) -> str
  win32_find_window(app_name) -> int | None       (hwnd)
  win32_close_window(app_name) -> str
  win32_minimize_window(app_name) -> str
  win32_maximize_window(app_name) -> str
  win32_focus_window(app_name) -> str
  win32_close_active_tab() -> str
  win32_close_active_window() -> str
  win32_snap_two_windows(left_app, right_app) -> str
"""

import ctypes
import ctypes.wintypes
import re
import time

# ─── Win32 constants ───────────────────────────────────────────────────────────
SW_RESTORE  = 9
SW_MINIMIZE = 6
SW_MAXIMIZE = 3
GW_HWNDNEXT = 2

# ─── Internal helpers ──────────────────────────────────────────────────────────

_user32 = ctypes.windll.user32
_kernel32 = ctypes.windll.kernel32

# Correct callback type: returns BOOL (int), takes HWND (int) + LPARAM (int)
_WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int)

# Window titles to always skip
_SKIP_TITLES = {
    'jarvis', 'program manager', 'windows input experience',
    'settings', 'microsoft text input application',
    'nvidia geforce overlay', 'task manager', ''
}

# Process names to always skip (exact match after .exe strip)
_SKIP_PROCS = {
    'searchhost', 'shellexperiencehost', 'startmenuexperiencehost',
    'runtimebroker', 'applicationframehost', 'conhost', 'svchost',
    'msedgewebview2',       # Windows Widgets WebView
    'textinputhost',        # On-screen keyboard
    'fontdrvhost',
    'sihost',               # Shell Infrastructure Host
    'ctfmon',               # IME
    'dllhost',
    'wininit',
    # Terminal / shell processes — NEVER auto-target these for window ops
    # (the voice agent runs inside one of these)
    'windowsterminal',      # Windows Terminal
    'powershell',           # PowerShell
    'cmd',                  # Command Prompt
    'pwsh',                 # PowerShell Core
    # ASUS/OEM utilities
    'asusscreenxpertreunion',
    'asus',
    # Antigravity / IDE coding assistant
    'antigravity',
}


def _get_title(hwnd: int) -> str:
    """Get the window title string from a HWND."""
    length = _user32.GetWindowTextLengthW(hwnd)
    if length == 0:
        return ''
    buf = ctypes.create_unicode_buffer(length + 1)
    _user32.GetWindowTextW(hwnd, buf, length + 1)
    return buf.value


def _get_process_name(hwnd: int) -> str:
    """Get the executable name of the process owning this HWND."""
    try:
        pid = ctypes.c_ulong(0)
        _user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        PROCESS_QUERY_LIMITED = 0x1000
        h_proc = _kernel32.OpenProcess(PROCESS_QUERY_LIMITED, False, pid.value)
        if not h_proc:
            return ''
        buf = ctypes.create_unicode_buffer(260)
        _kernel32.QueryFullProcessImageNameW(h_proc, 0, buf, ctypes.byref(ctypes.c_ulong(260)))
        _kernel32.CloseHandle(h_proc)
        return buf.value.split('\\')[-1].lower()
    except Exception:
        return ''


def _is_real_app_window(hwnd: int, require_visible: bool = True) -> bool:
    """Return True if this HWND looks like a real user-facing application window."""
    if require_visible and not _user32.IsWindowVisible(hwnd):
        return False
        
    import ctypes
    class RECT(ctypes.Structure):
        _fields_ = [('left', ctypes.c_long), ('top', ctypes.c_long), ('right', ctypes.c_long), ('bottom', ctypes.c_long)]
    rect = RECT()
    _user32.GetWindowRect(hwnd, ctypes.byref(rect))
    w = rect.right - rect.left
    h = rect.bottom - rect.top
    
    # Check if window is minimized (IsIconic)
    is_minimized = _user32.IsIconic(hwnd)
    
    # Filter out tiny floating windows, but allow them if they are minimized
    if not is_minimized and (w < 100 or h < 100):
        return False
        
    title = _get_title(hwnd)
    if not title:
        return False
    if title.lower() in _SKIP_TITLES:
        return False

    # Get process name (strip .exe suffix for comparison against _SKIP_PROCS)
    proc_raw = _get_process_name(hwnd)                      # e.g. 'chrome.exe'
    proc = proc_raw.replace('.exe', '').replace('.EXE', '') # e.g. 'chrome'

    # Skip known system/OEM processes
    if proc in _SKIP_PROCS:
        return False
    # Also skip processes that START with a known OEM prefix
    if any(proc.startswith(skip) for skip in ('asus', 'nvidia', 'intel', 'amd', 'realtek')):
        return False

    # Skip Jarvis Pygame overlay (python process with title "Jarvis")
    if 'jarvis' in title.lower() and proc in ('python', 'pythonw'):
        return False

    return True


def _norm(s: str) -> str:
    """Normalise string for fuzzy comparison."""
    import re
    return re.sub(r'[^a-z0-9]', '', s.lower())


def _enumerate_app_windows(require_visible: bool = True) -> list[tuple[int, str]]:
    """
    Return list of (hwnd, title) for all real user-facing windows,
    in Z-order (topmost first), excluding Jarvis overlay and system tasks.
    """
    results = []

    def _cb(hwnd, _lparam):
        if _is_real_app_window(hwnd, require_visible):
            results.append((hwnd, _get_title(hwnd)))
        return 1  # Must return non-zero int to continue enumeration

    cb = _WNDENUMPROC(_cb)
    _user32.EnumWindows(cb, 0)
    return results


def win32_find_window(app_name: str) -> int | None:
    """
    Find a window HWND by fuzzy matching against app_name.
    Returns the HWND integer or None if not found.
    Handles common aliases (e.g. 'vs code' → 'visual studio code', 'chrome' → 'chrome').
    """
    # ── Alias table: common spoken names → real title/process keywords ──
    _ALIASES = {
        'vs code': 'visual studio code',
        'vscode': 'visual studio code',
        'visual studio code': 'visual studio code',
        'code': 'visual studio code',
        'chrome': 'chrome',
        'google chrome': 'chrome',
        'edge': 'edge',
        'microsoft edge': 'edge',
        'firefox': 'firefox',
        'firefox browser': 'firefox',
        'notepad': 'notepad',
        'notepad++': 'notepad',
        'word': 'word',
        'microsoft word': 'word',
        'excel': 'excel',
        'microsoft excel': 'excel',
        'powerpoint': 'powerpoint',
        'outlook': 'outlook',
        'spotify': 'spotify',
        'discord': 'discord',
        'steam': 'steam',
        'task manager': 'task manager',
        'file explorer': 'file explorer',
        'explorer': 'file explorer',
        'paint': 'paint',
        'terminal': 'windows terminal',
        'cmd': 'command prompt',
        'powershell': 'powershell',
        'pycharm': 'pycharm',
        'intellij': 'intellij',
        'android studio': 'android studio',
    }

    raw_lower = app_name.lower().strip()
    expanded = _ALIASES.get(raw_lower, raw_lower)
    target = _norm(expanded)
    alt_target = _norm(raw_lower)  # also keep original form for fallback

    windows = _enumerate_app_windows(require_visible=False)

    # Pass 1: title contains the expanded alias string
    for hwnd, title in windows:
        if target in _norm(title):
            return hwnd

    # Pass 2: title contains the original (non-expanded) string
    if alt_target != target:
        for hwnd, title in windows:
            if alt_target in _norm(title):
                return hwnd

    # Pass 3: any significant keyword from target appears in title
    words = [w for w in target.split() if len(w) > 2]
    for hwnd, title in windows:
        norm_title = _norm(title)
        if any(w in norm_title for w in words):
            return hwnd

    # Pass 4: process name contains app_name keyword
    for hwnd, title in windows:
        proc = _get_process_name(hwnd)
        if alt_target in _norm(proc) or target in _norm(proc):
            return hwnd

    return None


def _pick_target_window(preferred_skip_names: list[str] = None) -> tuple[int, str]:
    """
    Pick the best user-visible foreground window to operate on.
    Tries GetForegroundWindow first. Falls back to Z-order enumeration.
    preferred_skip_names: extra window titles to skip (e.g. the browser Jarvis frontend).
    """
    extra_skip = set(_norm(s) for s in (preferred_skip_names or []))

    hwnd = _user32.GetForegroundWindow()
    title = _get_title(hwnd)

    if _is_real_app_window(hwnd) and _norm(title) not in extra_skip:
        return hwnd, title

    # Fallback: enumerate and pick first real app window
    for hwnd, title in _enumerate_app_windows():
        if _norm(title) not in extra_skip:
            return hwnd, title

    return 0, ''


# ─── Public API ───────────────────────────────────────────────────────────────

def adjust_active_window(
    position: str = None,
    width_percent: int = None,
    height_percent: int = None,
    app_name: str = None,
) -> str:
    """
    Snap or resize a window. If app_name is given, finds that specific app window.
    If app_name is None, targets the foreground window (skipping terminals/overlays).

    position:      'top_left' | 'top_right' | 'bottom_left' | 'bottom_right'
                   | 'left' | 'right' | 'top' | 'bottom' | 'center'
    width_percent:  1-100, percentage of screen width
    height_percent: 1-100, percentage of screen height
    app_name:      Optional — e.g. 'VS Code', 'Chrome', 'Notepad'
    """
    try:
        screen_w = _user32.GetSystemMetrics(0)
        screen_h = _user32.GetSystemMetrics(1)

        # Resolve the target window
        if app_name and app_name.strip():
            hwnd = win32_find_window(app_name.strip())
            if not hwnd:
                return f"Could not find an open window matching '{app_name}'. Is the app open?"
            title = _get_title(hwnd)
        else:
            hwnd, title = _pick_target_window()
            if not hwnd:
                return "Could not detect a valid active window to adjust."

        # Restore if maximised / minimised before resizing
        _user32.ShowWindow(hwnd, SW_RESTORE)
        time.sleep(0.15)

        # Determine default target size from position
        if position in ('top_left', 'top_right', 'bottom_left', 'bottom_right'):
            target_w, target_h = screen_w // 2, screen_h // 2
        elif position in ('left', 'right'):
            target_w, target_h = screen_w // 2, screen_h
        elif position in ('top', 'bottom'):
            target_w, target_h = screen_w, screen_h // 2
        elif position == 'center':
            # Keep current size, just centre it
            rect = ctypes.wintypes.RECT()
            _user32.GetWindowRect(hwnd, ctypes.byref(rect))
            target_w = rect.right - rect.left
            target_h = rect.bottom - rect.top
        else:
            # No position — start from current size, only override with percentages
            rect = ctypes.wintypes.RECT()
            _user32.GetWindowRect(hwnd, ctypes.byref(rect))
            target_w = rect.right - rect.left
            target_h = rect.bottom - rect.top

        # Override dimensions with explicit percentages
        if width_percent is not None and 1 <= width_percent <= 100:
            target_w = int(screen_w * width_percent / 100)
        if height_percent is not None and 1 <= height_percent <= 100:
            target_h = int(screen_h * height_percent / 100)

        # Determine X coordinate
        if position:
            pos = position.lower().replace(' ', '_').replace('-', '_')
            if 'left' in pos:
                x = 0
            elif 'right' in pos:
                x = screen_w - target_w
            else:  # top / bottom / center
                x = (screen_w - target_w) // 2
        else:
            # Keep X, clamp to screen
            rect = ctypes.wintypes.RECT()
            _user32.GetWindowRect(hwnd, ctypes.byref(rect))
            x = max(0, min(rect.left, screen_w - target_w))

        # Determine Y coordinate
        if position:
            pos = position.lower().replace(' ', '_').replace('-', '_')
            if 'top' in pos or 'upper' in pos:
                y = 0
            elif 'bottom' in pos or 'lower' in pos:
                y = screen_h - target_h
            elif pos in ('left', 'right'):
                y = 0  # snap to full height from top
            else:  # center
                y = (screen_h - target_h) // 2
        else:
            rect = ctypes.wintypes.RECT()
            _user32.GetWindowRect(hwnd, ctypes.byref(rect))
            y = max(0, min(rect.top, screen_h - target_h))

        # Apply the move/resize — bRepaint=True
        _user32.MoveWindow(hwnd, x, y, target_w, target_h, True)
        _user32.SetForegroundWindow(hwnd)

        parts = []
        if position:
            parts.append(f"position '{position}'")
        if width_percent:
            parts.append(f"{width_percent}% width")
        if height_percent:
            parts.append(f"{height_percent}% height")
        detail = ", ".join(parts) if parts else "custom size"
        return f"✅ Adjusted '{title[:35]}' → {detail}"

    except Exception as e:
        return f"Error adjusting window: {e}"


def win32_focus_window(app_name: str) -> str:
    """Bring the named window to the foreground."""
    hwnd = win32_find_window(app_name)
    if not hwnd:
        return f"Could not find an open window matching '{app_name}'."
    try:
        if _user32.IsIconic(hwnd):  # is minimised?
            _user32.ShowWindow(hwnd, SW_RESTORE)
            time.sleep(0.2)
        _user32.SetForegroundWindow(hwnd)
        time.sleep(0.1)
        return f"✅ Focused: '{_get_title(hwnd)[:50]}'"
    except Exception as e:
        return f"Failed to focus '{app_name}': {e}"


def win32_minimize_window(app_name: str) -> str:
    """Minimise the named window."""
    hwnd = win32_find_window(app_name)
    if not hwnd:
        return f"Could not find an open window matching '{app_name}'."
    try:
        _user32.ShowWindow(hwnd, SW_MINIMIZE)
        return f"✅ Minimised '{_get_title(hwnd)[:50]}'"
    except Exception as e:
        return f"Failed to minimise '{app_name}': {e}"


def win32_maximize_window(app_name: str) -> str:
    """Maximise the named window."""
    hwnd = win32_find_window(app_name)
    if not hwnd:
        return f"Could not find an open window matching '{app_name}'."
    try:
        _user32.ShowWindow(hwnd, SW_MAXIMIZE)
        _user32.SetForegroundWindow(hwnd)
        return f"✅ Maximised '{_get_title(hwnd)[:50]}'"
    except Exception as e:
        return f"Failed to maximise '{app_name}': {e}"


def win32_close_window(app_name: str) -> str:
    """Close the named window by sending WM_CLOSE."""
    WM_CLOSE = 0x0010
    hwnd = win32_find_window(app_name)
    if not hwnd:
        return f"Could not find an open window matching '{app_name}'."
    title = _get_title(hwnd)
    try:
        _user32.PostMessageW(hwnd, WM_CLOSE, 0, 0)
        time.sleep(0.3)
        return f"✅ Closed '{title[:50]}'"
    except Exception as e:
        return f"Failed to close '{app_name}': {e}"


def win32_close_active_window() -> str:
    """Close whichever real app window is currently active (not Jarvis)."""
    WM_CLOSE = 0x0010
    hwnd, title = _pick_target_window()
    if not hwnd:
        return "Could not detect the active window."
    try:
        _user32.PostMessageW(hwnd, WM_CLOSE, 0, 0)
        return f"✅ Closed active window: '{title[:50]}'"
    except Exception as e:
        return f"Failed to close active window: {e}"


def win32_close_active_tab() -> str:
    """
    Send Ctrl+W to the active window to close its current tab.
    Works for Chrome, Edge, Firefox, VS Code, etc.
    """
    import pyautogui
    hwnd, title = _pick_target_window()
    if hwnd:
        _user32.SetForegroundWindow(hwnd)
        time.sleep(0.15)
    pyautogui.hotkey('ctrl', 'w')
    return f"✅ Closed current tab in '{title[:40]}'" if title else "Closed current tab."


def win32_snap_two_windows(left_app: str, right_app: str) -> str:
    """
    Snap left_app to the left half and right_app to the right half of the screen
    using Win32 MoveWindow (no keyboard shortcuts, fully reliable).
    """
    screen_w = _user32.GetSystemMetrics(0)
    screen_h = _user32.GetSystemMetrics(1)
    half_w = screen_w // 2

    l_hwnd = win32_find_window(left_app)
    r_hwnd = win32_find_window(right_app)

    if not l_hwnd:
        return f"Could not find a window for '{left_app}'. Is the app open?"
    if not r_hwnd:
        return f"Could not find a window for '{right_app}'. Is the app open?"

    l_title = _get_title(l_hwnd)
    r_title = _get_title(r_hwnd)

    try:
        _user32.ShowWindow(l_hwnd, SW_RESTORE)
        _user32.MoveWindow(l_hwnd, 0, 0, half_w, screen_h, True)
        _user32.ShowWindow(r_hwnd, SW_RESTORE)
        _user32.MoveWindow(r_hwnd, half_w, 0, half_w, screen_h, True)
        _user32.SetForegroundWindow(r_hwnd)
        return (
            f"✅ Snapped:\n"
            f"  Left:  '{l_title[:40]}'\n"
            f"  Right: '{r_title[:40]}'"
        )
    except Exception as e:
        return f"Failed to snap windows: {e}"
