"""
Validate the computed call button position and take a screenshot to verify.
Run WHILE WhatsApp is open on Archit Shukla's chat.
"""
import time
import pygetwindow as gw
import pyautogui

windows = gw.getWindowsWithTitle("Whatsapp") or gw.getWindowsWithTitle("WhatsApp")
if not windows:
    print("WhatsApp not found!"); exit(1)

win = windows[0]
win.activate()
time.sleep(0.5)

shadow = 9
right_x = win.left + win.width - shadow
top_y   = win.top  + shadow

# Audio call = 2nd from right
btn_x = right_x - 204
btn_y = top_y   + 75

print(f"Window: left={win.left}, top={win.top}, width={win.width}, height={win.height}")
print(f"Visible right edge: {right_x}, visible top: {top_y}")
print(f"Audio call button target: ({btn_x}, {btn_y})")
print("Moving mouse there (3 sec, then clicking)...")
pyautogui.moveTo(btn_x, btn_y, duration=0.5)
time.sleep(3)
pyautogui.screenshot().save("wa_hover.png")
print("Screenshot saved as wa_hover.png")
print("Clicking...")
pyautogui.click(btn_x, btn_y)
time.sleep(1)
pyautogui.screenshot().save("wa_clicked.png")
print("Post-click screenshot saved as wa_clicked.png")
