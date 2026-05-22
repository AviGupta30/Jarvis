"""
WhatsApp Windows Desktop App Automation
Uses the native Windows app via keyboard automation — no browser needed.
"""
import os
import time
import subprocess
import pyautogui
import pyperclip

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.05


def _focus_or_open_whatsapp() -> bool:
    """Focus the WhatsApp window or open it if not running. Returns True on success."""
    import pygetwindow as gw

    # Try to find existing WhatsApp window
    try:
        windows = gw.getWindowsWithTitle("WhatsApp")
        if windows:
            win = windows[0]
            win.restore()
            win.activate()
            time.sleep(0.8)
            return True
    except Exception:
        pass

    # Launch WhatsApp via Windows URI scheme (works for Microsoft Store app)
    subprocess.Popen("start whatsapp:", shell=True)
    time.sleep(5)  # Give app time to open

    # Try focusing again
    try:
        import pygetwindow as gw
        windows = gw.getWindowsWithTitle("WhatsApp")
        if windows:
            windows[0].activate()
            time.sleep(0.5)
            return True
    except Exception:
        pass

    return False


def open_whatsapp() -> str:
    """Opens the WhatsApp desktop app."""
    success = _focus_or_open_whatsapp()
    return "WhatsApp is open." if success else "WhatsApp opened (may take a few seconds to load)."


def send_whatsapp_message(contact_name: str, message: str) -> str:
    """
    Sends a WhatsApp message using the Windows desktop app via keyboard automation.
    Uses Ctrl+F to search for the contact, then sends the message.
    """
    if not _focus_or_open_whatsapp():
        return "Could not open WhatsApp. Please open it manually and try again."

    time.sleep(1.5)

    try:
        # Step 1: Open new chat / search using Ctrl+F
        pyautogui.hotkey('ctrl', 'f')
        time.sleep(0.8)

        # Step 2: Clear search and type contact name
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.2)
        # Use clipboard to handle Unicode contact names reliably
        pyperclip.copy(contact_name)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(2.0)  # Wait for search results

        # Step 3: Press Enter or Down + Enter to select first result
        pyautogui.press('down')
        time.sleep(0.3)
        pyautogui.press('enter')
        time.sleep(1.0)

        # Step 4: Type and send the message
        pyperclip.copy(message)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.3)
        pyautogui.press('enter')
        time.sleep(0.5)

        return f"Message sent to {contact_name}."

    except Exception as e:
        return f"WhatsApp automation error: {str(e)}"
