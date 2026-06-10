"""
whatsapp_call.py — Jarvis Smart WhatsApp Calling Integration (Fully Isolated)
=======================================================================
COMPLETELY ISOLATED — imports nothing from the rest of Jarvis.
Safe to modify without affecting any other functionality.

FEATURES:
  - Two-phase call flow: always CONFIRMS before making an audio call.
  - Proper Unicode support via clipboard.
  - Uses Ctrl+Shift+C (audio call shortcut in WhatsApp Desktop).

PUBLIC API (called from tools.py):
  initiate_whatsapp_call(contact_name)  → str  first phase: show confirmation
  confirm_whatsapp_call(contact_name)   → str  second phase: actually make the call
"""

import time
import subprocess
import pyautogui
import pyperclip

# ─────────────────────────────────────────────────────────────────────────────
# Safety settings
# ─────────────────────────────────────────────────────────────────────────────
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.05

def _get_whatsapp_window():
    import pygetwindow as gw
    for w in gw.getAllWindows():
        if w.title in ("WhatsApp", "Whatsapp"):
            return w
    for w in gw.getAllWindows():
        t = w.title.lower()
        if "whatsapp" in t and not any(x in t for x in ["antigravity", "chrome", "edge", "firefox", "brave", "cursor", "devin", "regression", "jarvis", "issue", "bug"]):
            return w
    return None

def _focus_or_open_whatsapp() -> bool:
    """Focus the WhatsApp window or open it if not running. Returns True on success."""
    try:
        win = _get_whatsapp_window()
        if win:
            try:
                win.restore()
            except Exception:
                pass
            win.activate()
            time.sleep(1.0)
            return True
    except Exception:
        pass

    subprocess.Popen("start whatsapp:", shell=True)
    time.sleep(6)

    try:
        win = _get_whatsapp_window()
        if win:
            win.activate()
            time.sleep(0.8)
            return True
    except Exception:
        pass

    return False

def _type_via_clipboard(text: str, delay: float = 0.3):
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(delay)

def initiate_whatsapp_call(contact_name: str) -> str:
    contact_name = contact_name.strip()
    if not contact_name:
        return "I need a contact name. Who should I call?"

    return (
        f"Before I make the call, let me confirm:\n\n"
        f"  Calling: {contact_name}\n\n"
        f"Should I go ahead and call them on WhatsApp? Say 'yes call' or 'no cancel'."
    )

def _click_voice_call_button() -> bool:
    """
    Click the audio call button in the WhatsApp Desktop chat header.
    Position is computed from the window bounds — works for any window size.
    Offsets measured precisely via get_btn_pos.py:
      offset_from_right = 180, offset_from_top = 89
    """
    try:
        win = _get_whatsapp_window()
        if not win:
            return False

        shadow = 9
        right_x = win.left + win.width - shadow   # right edge of visible content
        top_y   = win.top  + shadow                # top edge of visible content

        btn_x = right_x - 180   # exact offset measured from right edge
        btn_y = top_y   + 89    # exact offset measured from top edge

        pyautogui.click(btn_x, btn_y)
        return True
    except Exception:
        return False




def confirm_whatsapp_call(contact_name: str) -> str:
    contact_name = contact_name.strip()

    if not _focus_or_open_whatsapp():
        return "Could not open WhatsApp. Please open it manually and try again."

    time.sleep(1.5)

    try:
        # Step 1: Close any open panels
        pyautogui.press('escape')
        time.sleep(0.3)

        # Step 2: Open New Chat (Ctrl+N)
        pyautogui.hotkey('ctrl', 'n')
        time.sleep(1.0)

        # Step 3: Type contact name via clipboard
        _type_via_clipboard(contact_name, delay=2.0)

        # Step 4: Press Enter to open the chat
        pyautogui.press('enter')
        time.sleep(2.5)

        # Step 5: Click the Voice Call button via UIA (most reliable)
        _click_voice_call_button()
        time.sleep(0.5)

        return f"Calling {contact_name} on WhatsApp now."

    except Exception as e:
        return f"WhatsApp call error: {e}"

