import time
import pyautogui
import pyperclip

def focus_whatsapp():
    try:
        import pygetwindow as gw
        windows = gw.getWindowsWithTitle("WhatsApp")
        if windows:
            win = windows[0]
            win.restore()
            win.activate()
            time.sleep(1.0)
            return True
    except Exception:
        pass
    return False

if focus_whatsapp():
    # step 1: search
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.1)
    pyautogui.press('delete')
    time.sleep(0.1)
    
    pyperclip.copy("dad")
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(2.0)
    pyautogui.screenshot("wa_step1.png")
    
    # Try pressing down
    pyautogui.press('down')
    time.sleep(1.0)
    pyautogui.screenshot("wa_step2.png")
    
    # Try pressing enter
    pyautogui.press('enter')
    time.sleep(1.0)
    pyautogui.screenshot("wa_step3.png")
