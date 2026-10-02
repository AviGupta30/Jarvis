"""
media_state.py — which media app the user used last (Spotify or YouTube)
=======================================================================
Tiny shared helper (not a tool). spotify_service and youtube_control record themselves
here when they start/control playback, and chat.py's router uses it to send ambiguous
commands ("pause it", "pause the song", "next song", "resume") to the right player.
Persisted to app/memory/media_state.json so it survives restarts and needs no globals.
"""

import os
import json
import time

_FILE = os.path.join(os.path.dirname(__file__), "..", "memory", "media_state.json")


def set_last(app: str):
    """app: 'spotify' | 'youtube'."""
    try:
        os.makedirs(os.path.dirname(_FILE), exist_ok=True)
        with open(_FILE, "w", encoding="utf-8") as f:
            json.dump({"last": app, "t": time.time()}, f)
    except Exception:
        pass


def get_last(max_age: float = 6 * 3600) -> str | None:
    """Last media app used within max_age seconds, else None."""
    try:
        with open(_FILE, "r", encoding="utf-8") as f:
            d = json.load(f)
        if time.time() - d.get("t", 0) <= max_age:
            return d.get("last")
    except Exception:
        pass
    return None


def spotify_running() -> bool:
    """True if the Spotify desktop app has a window (cheap: EnumWindows, no UIA)."""
    try:
        from app.services.window_layout import _enumerate_app_windows, _get_process_name
        return any(_get_process_name(h) == "spotify.exe"
                   for h, _ in _enumerate_app_windows(require_visible=False))
    except Exception:
        return False
