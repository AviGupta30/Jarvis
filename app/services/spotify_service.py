"""
spotify_service.py — Isolated Spotify Automation
------------------------------------------------
This file is completely isolated. It handles the GUI interaction 
with the Spotify Desktop application.
"""

import time
import subprocess
import pyautogui
import urllib.parse
from app.services.window_layout import win32_focus_window

def play_song_dynamic(song_name: str) -> str:
    """
    Dynamically opens Spotify, searches for the provided song_name, 
    and triggers the play action on the top result.
    """
    try:
        # 1. URL encode the song name to handle spaces and special characters
        # Example: "Kesariya" -> "Kesariya", "Blinding Lights" -> "Blinding%20Lights"
        encoded_song = urllib.parse.quote(song_name)
        
        # 2. Use the Spotify URI protocol to trigger a search directly
        # This is the most dynamic way to open the app and search simultaneously
        subprocess.Popen(f'start spotify:search:{encoded_song}', shell=True)
        
        # 3. Wait for Spotify to launch and the search results to render
        # Spotify is a heavy app; we give it a few seconds to stabilize
        time.sleep(4.0)
        
        # 4. Use your existing Win32 logic to ensure Spotify is the focused window
        focus_res = win32_focus_window("spotify")
        if "❌" in focus_res or "Could not" in focus_res:
            return f"I opened Spotify for '{song_name}', but I couldn't focus the window to press play."

        # 5. THE EXECUTION SEQUENCE
        # Keyboard navigation in Spotify is highly variable due to dynamic filters.
        # We will use visual detection to find the signature Spotify green Play button.
        import numpy as np
        time.sleep(2.0) # Wait a bit longer for page to finish rendering
        
        img = pyautogui.screenshot()
        img_np = np.array(img)
        # Search for Spotify green (RGB ~ 30, 215, 96), allowing some tolerance
        r, g, b = img_np[:,:,0], img_np[:,:,1], img_np[:,:,2]
        mask = (r < 80) & (g > 160) & (b < 130)
        y, x = np.where(mask)
        
        # Filter to only the top half of the screen to avoid the bottom player bar
        screen_h = img_np.shape[0]
        top_half = y < (screen_h // 2)
        y = y[top_half]
        x = x[top_half]
        
        if len(y) > 0:
            # We take the topmost green pixel (y[0]), and click slightly inside the button
            target_x = int(x[0]) + 24
            target_y = int(y[0]) + 24
            # Move slowly and click to ensure it registers
            pyautogui.moveTo(target_x, target_y, duration=0.2)
            time.sleep(0.2)
            pyautogui.click()
            time.sleep(0.2)
            pyautogui.click() # Double-tap just in case the first one only gave focus
            return f"Playing '{song_name}' on Spotify (vision detection)."
        else:
            # Fallback: Click the relative coordinates of the Top Result card
            import pygetwindow as gw
            wins = [w for w in gw.getAllWindows() if 'spotify' in w.title.lower()]
            if wins:
                win = wins[0]
                click_x = win.left + int(win.width * 0.40)
                click_y = win.top + int(win.height * 0.30)
                pyautogui.moveTo(click_x, click_y, duration=0.2)
                time.sleep(0.2)
                pyautogui.click()
                time.sleep(0.2)
                pyautogui.click()
            return f"Playing '{song_name}' on Spotify (coordinate fallback)."

    except Exception as e:
        return f"Spotify automation error: {str(e)}"

if __name__ == "__main__":
    # Local Test: Run this file alone to verify the automation
    import sys
    test_song = sys.argv[1] if len(sys.argv) > 1 else "Kesariya"
    print(f"Testing dynamic playback for: {test_song}")
    print(play_song_dynamic(test_song))