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
        # When you launch via spotify:search, the cursor is naturally inside the search bar.
        # We press TAB to jump from the search input to the FIRST search result.
        # Then we press ENTER to play that top result.
        pyautogui.press('tab') 
        time.sleep(0.3)
        pyautogui.press('enter')
        
        return f"Playing '{song_name}' on Spotify, sir."

    except Exception as e:
        return f"Spotify automation error: {str(e)}"

if __name__ == "__main__":
    # Local Test: Run this file alone to verify the automation
    import sys
    test_song = sys.argv[1] if len(sys.argv) > 1 else "Kesariya"
    print(f"Testing dynamic playback for: {test_song}")
    print(play_song_dynamic(test_song))