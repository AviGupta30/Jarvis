import sys

with open('app/services/window_layout.py', 'r', encoding='utf-8') as f:
    text = f.read()

bad = '''def _is_real_app_window(hwnd: int, require_visible: bool = True) -> bool:
    """Return True if this HWND looks like a real user-facing application window."""
    if require_visible and not _user32.IsWindowVisible(hwnd):
        return False
        
    import ctypes
    class RECT(ctypes.Structure):
        _fields_ = [('left', ctypes.c_long), ('top', ctypes.c_long), ('right', ctypes.c_long), ('bottom', ctypes.c_long)]
    rect = RECT()
    _user32.GetWindowRect(hwnd, ctypes.byref(rect))
    if (rect.right - rect.left) < 100 or (rect.bottom - rect.top) < 100:
        return False'''

good = '''def _is_real_app_window(hwnd: int, require_visible: bool = True) -> bool:
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
        return False'''

if bad in text:
    with open('app/services/window_layout.py', 'w', encoding='utf-8') as f:
        f.write(text.replace(bad, good))
    print('window_layout.py patched successfully!')
else:
    print('Failed to find bad block!')
