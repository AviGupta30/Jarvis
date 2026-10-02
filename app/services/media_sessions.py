"""
media_sessions.py — control whatever is ACTUALLY playing (helper, not a tool)
============================================================================
Uses Windows' own media sessions (System Media Transport Controls, the ones shown in the
volume flyout / media keys overlay) through the `winrt` packages. Every app that plays
media registers one: Spotify, each browser tab with audio (YouTube, YouTube Music, …),
VLC, etc. Each session reports its playback status and title and can be paused/played/
skipped directly, with no keyboard, no focus change and no leaving fullscreen.

Why: Jarvis used to guess the player from "what Jarvis started last", so songs that were
already playing (started by hand, in a background tab, or before a restart) didn't stop.

Requires: pip install winrt-Windows.Media.Control winrt-Windows.Foundation
          winrt-Windows.Foundation.Collections winrt-runtime   (Windows 10+)
All functions are synchronous and never raise; they return None/[] when unavailable.
"""

import re
import asyncio

# Load order matters: if winrt initialises first, onnxruntime (embeddings / TTS) later fails
# with "DLL initialization routine failed". Make sure onnxruntime is loaded before winrt.
try:
    import onnxruntime  # noqa: F401
except Exception:
    pass

_BROWSERS = ("msedge", "edge", "chrome", "firefox", "brave", "opera", "vivaldi")
_STATUS = {0: "closed", 1: "opened", 2: "changing", 3: "stopped", 4: "playing", 5: "paused"}


def _run(coro):
    """Run a coroutine from sync code (we're on the media worker thread, no running loop)."""
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)
    # Called from inside an event loop (unexpected): run in a private thread
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor(1) as ex:
        return ex.submit(asyncio.run, coro).result()


def app_kind(app_id: str) -> str:
    a = (app_id or "").lower()
    if "spotify" in a:
        return "spotify"
    if any(b in a for b in _BROWSERS):
        return "browser"
    return "other"


async def _sessions_async():
    from winrt.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as M
    mgr = await M.request_async()
    cur = mgr.get_current_session()
    cur_id = cur.source_app_user_model_id if cur else None
    out = []
    for s in mgr.get_sessions():
        info = s.get_playback_info()
        title = artist = ""
        try:
            props = await s.try_get_media_properties_async()
            title, artist = props.title or "", props.artist or ""
        except Exception:
            pass
        out.append({"session": s, "app_id": s.source_app_user_model_id, "kind": app_kind(s.source_app_user_model_id),
                    "status": _STATUS.get(int(info.playback_status), str(info.playback_status)),
                    "title": title, "artist": artist,
                    "current": s.source_app_user_model_id == cur_id})
    return out


def sessions() -> list[dict]:
    """[{app_id, kind: spotify|browser|other, status: playing|paused|…, title, artist, current}]"""
    try:
        return _run(_sessions_async())
    except Exception as e:
        print(f"[media_sessions] unavailable: {type(e).__name__}: {e}")
        return []


def _label(s: dict) -> str:
    t, a = s.get("title") or "", s.get("artist") or ""
    if s["kind"] == "browser":
        return t or "the browser video"
    return f"{t} by {a}" if t and a else (t or ("Spotify" if s["kind"] == "spotify" else "the music"))


async def _do(s, action: str) -> bool:
    sess = s["session"]
    try:
        if action == "pause":
            return bool(await sess.try_pause_async())
        if action == "play":
            return bool(await sess.try_play_async())
        if action == "next":
            return bool(await sess.try_skip_next_async())
        if action == "previous":
            return bool(await sess.try_skip_previous_async())
        if action == "toggle":
            return bool(await sess.try_toggle_play_pause_async())
    except Exception:
        return False
    return False


def _filter(ss: list, app: str | None) -> list:
    if app in ("spotify",):
        return [s for s in ss if s["kind"] == "spotify"]
    if app in ("youtube", "browser", "video"):
        return [s for s in ss if s["kind"] == "browser"]
    return ss


def control(action: str, app: str | None = None, prefer: str | None = None, title_hint: str = "") -> dict:
    """
    action: pause | play | next | previous | toggle
    app:    None (anything) | 'spotify' | 'youtube'/'browser'
    prefer: app kind to pick first when several sessions qualify (e.g. the last player used)
    title_hint: pick the session whose title matches (the YouTube tab's video title)
    Returns {"ok": bool, "did": [labels], "reason": str}.
    """
    try:
        ss = _filter(sessions(), app)
        if not ss:
            return {"ok": False, "did": [], "reason": "none"}
        if title_hint:
            # a specific tab: only consider the session(s) with that title (not other tabs)
            th = title_hint.lower()
            match = [s for s in ss if s["title"] and (s["title"].lower() in th or th in s["title"].lower())]
            if match:
                ss = match
            elif len(ss) > 1:
                return {"ok": False, "did": [], "reason": "none"}
        playing = [s for s in ss if s["status"] == "playing"]
        paused = [s for s in ss if s["status"] in ("paused", "stopped", "opened")]

        def rank(s):
            score = 0
            if title_hint and s["title"] and (s["title"].lower() in title_hint.lower() or title_hint.lower() in s["title"].lower()):
                score -= 10
            if prefer and s["kind"] == ("browser" if prefer == "youtube" else prefer):
                score -= 4
            if s["current"]:
                score -= 2
            return score

        async def run(targets, act):
            did = []
            for s in targets:
                if await _do(s, act):
                    did.append(_label(s))
            return did

        # NOTE: the reported playback status lags (Edge: ~2 s after a pause it still says
        # "playing"), so it never decides WHETHER to act. Pause/play are idempotent:
        # pause asks every matching session, play resumes the best candidate.
        if action == "pause":
            targets = sorted(ss, key=rank)
            if title_hint:                       # a specific tab: only that one
                targets = targets[:1]
            did_any = _run(run(targets, "pause"))
            labels = [_label(s) for s in targets if s["status"] == "playing"] or did_any
            if not did_any:
                return {"ok": False, "did": [], "reason": "nothing_playing" if not playing else "failed"}
            return {"ok": True, "did": labels if playing else [], "reason": ""}
        if action == "play":
            pool = sorted(ss, key=lambda s: (rank(s), s["status"] == "playing"))
            target = pool[0]
            did = _run(run([target], "play"))
            return {"ok": bool(did), "did": did, "reason": "" if did else "failed"}
        if action in ("next", "previous", "toggle"):
            pool = sorted(playing or ss, key=rank)
            did = _run(run(pool[:1], action))
            return {"ok": bool(did), "did": did, "reason": "" if did else "failed"}
        return {"ok": False, "did": [], "reason": "unknown_action"}
    except Exception as e:
        print(f"[media_sessions] control failed: {type(e).__name__}: {e}")
        return {"ok": False, "did": [], "reason": "error"}


def kind_playing(kind: str) -> bool:
    return any(s["kind"] == kind and s["status"] == "playing" for s in sessions())


def media_command(action: str, app: str = "") -> str:
    """
    Tool entry (registered as `media_control` in TOOL_REGISTRY): pause / resume / next /
    previous / now_playing for whatever is playing. app: '' (anything), 'spotify', 'youtube'.
    """
    try:
        a = (action or "pause").lower().strip()
        a = {"stop": "pause", "resume": "play", "continue": "play", "unpause": "play", "skip": "next",
             "prev": "previous", "back": "previous", "status": "now_playing", "what": "now_playing"}.get(a, a)
        app = (app or "").lower().strip() or None
        where = {"spotify": " on Spotify", "youtube": " on YouTube", "browser": " in the browser"}.get(app or "", "")
        try:
            from app.services.media_state import get_last, set_last
        except Exception:
            get_last = lambda: None
            set_last = lambda x: None
        last = get_last()

        if a == "now_playing":
            ss = _filter(sessions(), app)
            pl = [s for s in ss if s["status"] == "playing"]
            if not pl:
                return f"Nothing is playing{where} right now, Sir."
            return "Playing now: " + "; ".join(_label(s) for s in pl) + "."

        r = control(a, app, prefer=last)
        if r["ok"]:
            kinds = {s["kind"] for s in _filter(sessions(), app) if _label(s) in r["did"]}
            if "spotify" in kinds:
                set_last("spotify")
            elif "browser" in kinds:
                set_last("youtube")
            what = (r["did"][0] if len(r["did"]) == 1 else
                    ("everything that was playing" if r["did"] else "the music"))
            return {"pause": f"Paused {what}, Sir.", "play": f"Resumed {what}, Sir.",
                    "next": "Skipped to the next one, Sir.", "previous": "Went back to the previous one, Sir.",
                    "toggle": "Done, Sir."}.get(a, "Done, Sir.")
        if r["reason"] == "nothing_playing":
            return f"Nothing is playing{where} right now, Sir."
        if r["reason"] == "none":
            return f"I don't see any music or video{where} to control, Sir."
        return "I couldn't control the player just then, Sir. Please try again."
    except Exception as e:
        return f"Media control error: {e}"


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    for s in sessions():
        print(s["kind"], s["status"], "|", _label(s), "|", s["app_id"], "| current" if s["current"] else "")
    if len(sys.argv) > 1:
        print(media_command(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else ""))
