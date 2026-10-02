"""
spotify_service.py — Isolated Spotify Automation
------------------------------------------------
Drives the Spotify Desktop app (Store or classic install).

How playback works:
  1. `spotify:search:<query>` URI opens/navigates the desktop app to the search page.
  2. The app's UI Automation tree (Chromium/CEF) exposes real, named buttons:
       - an unnamed "Play" button on the Top Result card,
       - "Play <title>" buttons on each song/album/playlist row,
       - the player bar: "Previous" / "Play"|"Pause" / "Next", shuffle, repeat, like.
     We invoke those buttons directly (no pixel guessing), then verify playback via
     the window title, which Spotify changes to "Artist - Song" while playing.
  3. If UIA is unavailable, fall back to the old green-play-button pixel search.
"""

import os
import re
import time
import difflib
import subprocess
import urllib.parse

import pyautogui

_IDLE_TITLES = {"spotify", "spotify free", "spotify premium", ""}


# ── helpers ────────────────────────────────────────────────────────────────

def _com_init():
    """UIA calls need COM initialised in the calling thread (tools may run in a worker)."""
    try:
        import comtypes
        comtypes.CoInitialize()
    except Exception:
        pass


def _find_spotify_window():
    """UIA element of the Spotify main window (visible, titled), or None.
    Uses uia_local (a UIAutomation object per thread): pywinauto's shared one belongs to
    whichever thread created it, and calls from the backend's worker threads came back
    empty right after a song started."""
    try:
        import ctypes
        import ctypes.wintypes as wt
        from app.services.uia_local import element_from_handle
        pids = _spotify_pids()
        if not pids:
            return None
        user32 = ctypes.windll.user32
        WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
        found = []

        def _cb(hwnd, _):
            pid = ctypes.c_ulong()
            user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            if pid.value in pids and user32.IsWindowVisible(hwnd) and user32.GetWindowTextLengthW(hwnd) > 0:
                found.append(hwnd)
            return True
        user32.EnumWindows(WNDENUMPROC(_cb), 0)
        # biggest visible window = the main player (skips small popups / tooltips)
        best, area = None, 0
        for h in found:
            r = wt.RECT()
            user32.GetWindowRect(h, ctypes.byref(r))
            a = (r.right - r.left) * (r.bottom - r.top)
            if user32.IsIconic(h):
                a = max(a, 1)
            if a > area:
                best, area = h, a
        return element_from_handle(best) if best else None
    except Exception as e:
        print(f"[spotify] window lookup failed: {type(e).__name__}: {e}")
        return None


def _restore(win):
    """Un-minimise Spotify (CEF does not render search results while minimised)."""
    try:
        import ctypes
        user32 = ctypes.windll.user32
        if user32.IsIconic(win.handle):
            user32.ShowWindow(win.handle, 9)  # SW_RESTORE
            time.sleep(0.4)
    except Exception:
        pass


def _buttons(win):
    """All buttons in the window. The first UIA query after launch can be sparse, so retry."""
    for _ in range(3):
        try:
            btns = win.descendants(control_type="Button")
            if len(btns) > 10:
                return btns
        except Exception:
            pass
        time.sleep(0.5)
    return []


def _content_play_buttons(win, btns):
    """'Play…' buttons that are on screen inside the main content area (not the player bar)."""
    try:
        r = win.rectangle()
    except Exception:
        return []
    out = []
    for b in btns:
        try:
            name = b.window_text() or ""
            if not name.startswith("Play"):
                continue
            br = b.rectangle()
            if br.top < r.top + 90 or br.bottom > r.bottom - 110 or br.width() == 0:
                continue
            out.append((name, b))
        except Exception:
            continue
    return out


def _player_bar(win, btns=None):
    """Return dict of player-bar buttons: previous, toggle (Play/Pause), next, shuffle, repeat, like."""
    btns = btns if btns is not None else _buttons(win)
    try:
        r = win.rectangle()
    except Exception:
        return {}
    bar = {}
    for b in btns:
        try:
            br = b.rectangle()
            if br.top < r.bottom - 110:
                continue
            name = b.window_text() or ""
            if name == "Previous":
                bar["previous"] = b
            elif name == "Next":
                bar["next"] = b
            elif name in ("Play", "Pause"):
                bar["toggle"] = b
            elif "shuffle" in name.lower():
                bar["shuffle"] = b
            elif "repeat" in name.lower():
                bar["repeat"] = b
            elif name in ("Add to Liked Songs", "Remove from Liked Songs") or "Liked Songs" in name:
                bar.setdefault("like", b)
        except Exception:
            continue
    return bar


def _press(btn):
    try:
        btn.invoke()
    except Exception:
        btn.click_input()


def _now_playing_title(win) -> str:
    try:
        t = win.window_text().strip()
        return "" if t.lower() in _IDLE_TITLES else t
    except Exception:
        return ""


def _is_playing(win) -> bool:
    bar = _player_bar(win)
    try:
        return bar.get("toggle") is not None and bar["toggle"].window_text() == "Pause"
    except Exception:
        return False


def _tokens(text: str) -> set[str]:
    stop = {"the", "a", "an", "of", "by", "and", "to", "in", "on", "feat", "ft", "from", "song", "remix"}
    return {w for w in re.findall(r"[a-z0-9]+", (text or "").lower()) if w not in stop and len(w) > 1}


def _title_match(title: str, query: str) -> float:
    """Share of the query's words found in a title/name (0..1)."""
    q = _tokens(query)
    return len(q & _tokens(title)) / len(q) if q else 1.0


def _page_matches(win, btns, query: str) -> bool:
    """Is Spotify showing results for this query? (≥60% of its words appear on screen)"""
    q = _tokens(query)
    if not q:
        return True
    seen = set()
    try:
        r = win.rectangle()
        elems = list(btns)
        try:
            elems += win.descendants(control_type="Hyperlink")
        except Exception:
            pass
        for e in elems:
            try:
                er = e.rectangle()
                if er.top < r.top + 90 or er.bottom > r.bottom - 110 or er.width() == 0:
                    continue
                seen |= _tokens(e.window_text())
            except Exception:
                continue
    except Exception:
        return True
    return len(q & seen) / len(q) >= 0.6


def _pick_target(candidates, query: str):
    """Top-result card button (named exactly 'Play') wins; else best fuzzy title match."""
    for name, b in candidates:
        if name == "Play":
            return name, b
    q = query.lower()
    best, best_score = None, 0.0
    for name, b in candidates:
        title = name[5:].lower()
        score = difflib.SequenceMatcher(None, q, title).ratio()
        if q in title or title in q:
            score += 0.5
        if score > best_score:
            best, best_score = (name, b), score
    return best


def _clean_query(song: str) -> str:
    q = song.strip().strip(" .,!?\"'")
    q = re.sub(r'\s+(?:on\s+spotify|for\s+me|please)$', '', q, flags=re.I)
    q = re.sub(r'^(?:the\s+)?(?:song|track|music)\s+', '', q, flags=re.I)
    q = re.sub(r'\s+(?:song|track)$', '', q, flags=re.I)   # "kesariya song" → "kesariya"
    # "shape of you by ed sheeran" → "shape of you ed sheeran" (Spotify search likes this better)
    q = re.sub(r'\s+by\s+', ' ', q, flags=re.I)
    return q.strip()


def _vision_fallback(song_name: str) -> str:
    """Legacy: click the top-most Spotify-green blob in the upper half of the screen."""
    try:
        import numpy as np
        img = np.array(pyautogui.screenshot())
        r, g, b = img[:, :, 0], img[:, :, 1], img[:, :, 2]
        y, x = np.where((r < 80) & (g > 160) & (b < 130))
        keep = y < img.shape[0] // 2
        y, x = y[keep], x[keep]
        if len(y):
            pyautogui.click(int(x[0]) + 24, int(y[0]) + 24)
            return f"I searched Spotify for '{song_name}' and pressed play on the top result."
    except Exception:
        pass
    return f"I opened Spotify's search for '{song_name}', Sir, but couldn't press play automatically."


# ── public API ─────────────────────────────────────────────────────────────

def play_song_dynamic(song_name: str) -> str:
    """
    Opens Spotify, searches for song_name, plays the top result and confirms what is playing.
    Blocking (~3-10 s). Returns a human-readable status string.
    """
    try:
        _com_init()
        query = _clean_query(song_name)
        if not query:
            return "Which song would you like me to play, Sir?"

        win = _find_spotify_window()
        if win:
            _restore(win)
        before_title = _now_playing_title(win) if win else ""

        search_uri = f'start "" "spotify:search:{urllib.parse.quote(query)}"'
        was_running = win is not None
        subprocess.Popen(search_uri, shell=True)

        # Wait for the window (cold start can take a while)
        deadline = time.time() + 25
        while not win and time.time() < deadline:
            time.sleep(0.8)
            win = _find_spotify_window()
        if not win:
            return "I couldn't open the Spotify app, Sir. Is it installed and signed in?"
        _restore(win)
        if not was_running:
            # Cold start: the Store app opens Home and drops the search link. Wait until its UI
            # is up, then send the search again.
            end = time.time() + 15
            while time.time() < end and len(_buttons(win)) < 15:
                time.sleep(0.7)
            time.sleep(1.0)
            subprocess.Popen(search_uri, shell=True)

        # Wait for search results that belong to THIS query. Spotify keeps showing the previous
        # page for a moment, and pressing its Play button played the wrong song ("Jai Ho" for
        # "shape of you"): require the visible buttons/links to mention the query's words.
        time.sleep(1.0)
        target, cands = None, []
        start = time.time()
        deadline = start + 14
        resent = False
        while time.time() < deadline:
            btns = _buttons(win)
            cands = _content_play_buttons(win, btns)
            if cands and _page_matches(win, btns, query):
                target = _pick_target(cands, query)
                if target:
                    break
            if not resent and time.time() - start > 5:
                subprocess.Popen(search_uri, shell=True)   # link got lost (app was busy): resend once
                resent = True
            time.sleep(0.6)

        if not target:
            try:
                win.set_focus()
            except Exception:
                pass
            time.sleep(1.0)
            return _vision_fallback(song_name)

        tried = set()
        for _attempt in range(2):
            tried.add(target[0])
            _press(target[1])
            # Verify playback, and that it is the song asked for
            title = ""
            end = time.time() + 6
            while time.time() < end:
                time.sleep(0.6)
                title = _now_playing_title(win)
                if title and (title != before_title or _is_playing(win)):
                    break
            got = _title_match(title, query) if title else 0.0
            if title and got >= 0.34:
                _mark_last()
                return f"Now playing {title} on Spotify, Sir."
            # Track doesn't mention the query. Artist / playlist requests ("play arijit singh")
            # legitimately play someone else's credit, so only switch when a song row matches
            # the query clearly better (that was the "Jai Ho" for "shape of you" case).
            better = [(n, b) for n, b in cands if n != "Play" and n not in tried]
            better.sort(key=lambda nb: -_title_match(nb[0][5:], query))
            if not better or _title_match(better[0][0][5:], query) < max(0.6, got + 0.2):
                break
            target = better[0]
        title = _now_playing_title(win)
        if title:
            _mark_last()
            if _title_match(title, query) >= 0.34:
                return f"Now playing {title} on Spotify, Sir."
            return f"Playing {song_name} on Spotify, Sir. Now playing {title}."
        if _is_playing(win):
            _mark_last()
            return f"Playing '{song_name}' on Spotify, Sir."
        return f"I found '{song_name}' on Spotify and pressed play, but I can't confirm it started, Sir."

    except Exception as e:
        return f"Spotify automation error: {e}"


def _mark_last():
    try:
        from app.services.media_state import set_last
        set_last("spotify")
    except Exception:
        pass


def _spotify_pids() -> set[int]:
    try:
        import psutil
        return {p.pid for p in psutil.process_iter(["name"]) if (p.info["name"] or "").lower() == "spotify.exe"}
    except Exception:
        return set()


def _close_spotify() -> str:
    """Quit the Spotify app: WM_CLOSE its windows, then end the process if it only hid to the tray."""
    import ctypes
    pids = _spotify_pids()
    if not pids:
        return "Spotify isn't running, Sir."
    user32 = ctypes.windll.user32
    WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    hwnds = []

    def _cb(hwnd, _):
        pid = ctypes.c_ulong()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        if pid.value in pids and user32.GetWindowTextLengthW(hwnd) > 0:
            hwnds.append(hwnd)
        return True
    user32.EnumWindows(WNDENUMPROC(_cb), 0)
    for h in hwnds:
        user32.PostMessageW(h, 0x0010, 0, 0)   # WM_CLOSE
    deadline = time.time() + 4
    while time.time() < deadline and _spotify_pids():
        time.sleep(0.3)
    if _spotify_pids():                     # "close button minimises to tray" setting
        subprocess.run("taskkill /IM Spotify.exe /F", shell=True, capture_output=True)
        time.sleep(0.8)
    return "Closed Spotify, Sir." if not _spotify_pids() else "I couldn't close Spotify, Sir."


def spotify_control(action: str) -> str:
    """
    Control the Spotify desktop player through its own buttons (targets Spotify even when a
    browser tab owns the media keys). action: play | pause | toggle | next | previous |
    shuffle | repeat | like | now_playing | open | close. Falls back to media keys if
    Spotify isn't open.
    """
    try:
        _com_init()
        action = (action or "toggle").lower().strip().replace(" ", "_")
        aliases = {"resume": "play", "stop": "pause", "skip": "next", "prev": "previous",
                   "back": "previous", "what's_playing": "now_playing", "current": "now_playing",
                   "save": "like", "favourite": "like", "favorite": "like",
                   "quit": "close", "exit": "close", "kill": "close", "launch": "open", "start": "open"}
        action = aliases.get(action, action)

        if action == "close":
            return _close_spotify()
        if action == "open":
            if _find_spotify_window():
                win = _find_spotify_window()
                _restore(win)
                try:
                    win.set_focus()
                except Exception:
                    pass
                return "Spotify is open, Sir."
            subprocess.Popen('start "" "spotify:"', shell=True)
            deadline = time.time() + 15
            while time.time() < deadline and not _find_spotify_window():
                time.sleep(0.6)
            return "Spotify is open, Sir." if _find_spotify_window() else "I couldn't open Spotify, Sir."

        win = _find_spotify_window()
        if not win:
            keys = {"play": "playpause", "pause": "playpause", "toggle": "playpause",
                    "next": "nexttrack", "previous": "prevtrack"}
            if action in keys:
                pyautogui.press(keys[action])
                return "Spotify isn't open, so I sent the media key instead, Sir."
            return "Spotify isn't open right now, Sir."

        if action == "now_playing":
            title = _now_playing_title(win)
            if title:
                return f"You're listening to {title}, Sir."
            return "Nothing is playing on Spotify right now, Sir."

        bar = _player_bar(win)
        if not bar:
            return "I couldn't reach Spotify's player controls, Sir."
        toggle = bar.get("toggle")
        state = toggle.window_text() if toggle else ""

        if action in ("play", "pause", "toggle"):
            if not toggle:
                return "I couldn't find Spotify's play button, Sir."
            if action == "pause" and state != "Pause":
                return "Spotify is already paused, Sir."
            if action == "play" and state == "Pause":
                return "Spotify is already playing, Sir."
            _press(toggle)
            _mark_last()
            return "Paused Spotify, Sir." if state == "Pause" else "Resumed Spotify, Sir."

        if action in ("next", "previous"):
            btn = bar.get(action)
            if not btn:
                return f"I couldn't find Spotify's {action} button, Sir."
            _press(btn)
            _mark_last()
            time.sleep(1.2)
            title = _now_playing_title(win)
            return f"Skipped. Now playing {title}." if title else "Done, Sir."

        if action in ("shuffle", "repeat", "like"):
            btn = bar.get(action)
            if not btn:
                return f"I couldn't find Spotify's {action} button, Sir."
            label = btn.window_text()
            _press(btn)
            return f"Done — {label.lower()}."

        return f"I don't know the Spotify action '{action}', Sir."
    except Exception as e:
        return f"Spotify control error: {e}"


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) > 2 and sys.argv[1] == "--control":
        print(spotify_control(sys.argv[2]))
    else:
        test_song = sys.argv[1] if len(sys.argv) > 1 else "Kesariya"
        print(f"Testing dynamic playback for: {test_song}")
        print(play_song_dynamic(test_song))
