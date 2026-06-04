"""
Find the Voice Call button position in WhatsApp Desktop window.
Run this while WhatsApp is open on a chat screen.
"""
import time
import pygetwindow as gw
import pyautogui

# Focus WhatsApp
windows = gw.getWindowsWithTitle("Whatsapp") or gw.getWindowsWithTitle("WhatsApp")
if not windows:
    print("WhatsApp not found!")
    exit(1)

win = windows[0]
win.activate()
time.sleep(1)

print(f"Window: left={win.left}, top={win.top}, width={win.width}, height={win.height}")
print(f"Window right edge: {win.left + win.width}")

# The Voice Call button in WhatsApp Desktop is in the top-right header area of the chat.
# Let's take a screenshot and show where common button positions are.
ss = pyautogui.screenshot()
ss.save("wa_screenshot.png")
print("Screenshot saved as wa_screenshot.png")

# Common positions for call button (relative to window right edge, fixed y from top)
# These are the approximate positions based on WhatsApp Desktop layout
header_y = win.top + 35  # Header bar is roughly 70px tall, button centers at ~35px from top
# Call button is 3rd button from right: video call, audio call, search
# Each button ~40px wide
audio_call_x = win.left + win.width - 130  # Approx: 3rd button from right
print(f"\nEstimated audio call button position: x={audio_call_x}, y={header_y}")
print("Moving mouse there (not clicking)...")
pyautogui.moveTo(audio_call_x, header_y, duration=0.5)
time.sleep(2)

# Try clicking
print("Clicking...")
pyautogui.click(audio_call_x, header_y)
time.sleep(1)

# Take another screenshot
ss2 = pyautogui.screenshot()
ss2.save("wa_after_click.png")
print("Post-click screenshot saved as wa_after_click.png")
