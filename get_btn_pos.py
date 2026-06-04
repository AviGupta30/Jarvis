"""
Step 1: Open WhatsApp, go to any chat (e.g. Archit Shukla)
Step 2: Hover your mouse over the PHONE/AUDIO CALL button (the phone handset icon)
Step 3: This script will capture the position every 3 seconds for 15 seconds
        Just hover over the button and wait!
"""
import time
import pyautogui

print("You have 5 seconds to move your mouse to the AUDIO CALL (phone) button in WhatsApp...")
print("Hover over it and HOLD STILL")
time.sleep(5)

positions = []
for i in range(5):
    x, y = pyautogui.position()
    positions.append((x, y))
    print(f"  [{i+1}] Mouse position: x={x}, y={y}")
    time.sleep(1)

# Most common / median position
xs = [p[0] for p in positions]
ys = [p[1] for p in positions]
avg_x = int(sum(xs)/len(xs))
avg_y = int(sum(ys)/len(ys))
print(f"\nAverage position: x={avg_x}, y={avg_y}")
print(f"\nNow capturing window info for offset calculation...")

import pygetwindow as gw
windows = gw.getWindowsWithTitle("Whatsapp") or gw.getWindowsWithTitle("WhatsApp")
if windows:
    win = windows[0]
    print(f"Window: left={win.left}, top={win.top}, width={win.width}, height={win.height}")
    shadow = 9
    right_x = win.left + win.width - shadow
    top_y = win.top + shadow
    offset_from_right = right_x - avg_x
    offset_from_top = avg_y - top_y
    print(f"\nComputed offsets:")
    print(f"  offset_from_right = {offset_from_right}")
    print(f"  offset_from_top   = {offset_from_top}")
    print(f"\nPaste these two values to Jarvis!")
else:
    print("WhatsApp window not found!")
