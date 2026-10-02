"""
youtube_control.py — YouTube search, result picking, player control and "YouTube mode"
======================================================================================
Flow the user sees:
    "open youtube"                → opens youtube.com, enters YouTube mode, asks what to search
    "lofi hip hop" / "type lofi"  → searches, reads back the top 5 numbered results
    "play the second one"         → opens that exact video (by URL, no pixel clicking)
    "the one by Lofi Girl" / "the 1 hour one" / "the video about rain" → fuzzy pick
    "speed 2x" / "go to 5:30" / "forward 10 minutes" / "skip this part" / "captions off" /
    "volume 40" / "what's the time left" / "next chapter" / "skip ad" / "like this video"
                                  → precise player control via youtube_player.player_action
    "close youtube" / "exit youtube mode" → ends the mode

Results come from YouTube's own results page (ytInitialData JSON), so every result has
a real videoId. Session state (last query, results, current video, mode flag) is persisted
to app/memory/youtube_session.json, not module globals. chat.py consults
`youtube_session_active()` + `parse_youtube_followup()` before normal routing.

Every public function returns a human-readable string and never raises.
"""

import os
import re
import json
import time
import difflib
import webbrowser
import urllib.parse
import urllib.request


_SESSION_FILE = os.path.join(os.path.dirname(__file__), "..", "memory", "youtube_session.json")
_SESSION_TTL = 20 * 60          # YouTube mode expires after 20 min without a YouTube command
_SHOW_N = 5                     # results read back to the user
_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
       "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

_ORDINALS = {
    "first": 1, "1st": 1, "top": 1, "second": 2, "2nd": 2, "third": 3, "3rd": 3,
    "fourth": 4, "4th": 4, "fifth": 5, "5th": 5, "sixth": 6, "6th": 6, "seventh": 7,
    "7th": 7, "eighth": 8, "8th": 8, "ninth": 9, "9th": 9, "tenth": 10, "10th": 10,
}
_NUM_WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
              "seven": 7, "eight": 8, "nine": 9, "ten": 10}


# ── session persistence ────────────────────────────────────────────────────

def _load() -> dict:
    try:
        with open(_SESSION_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save(sess: dict):
    try:
        sess["updated"] = time.time()
        os.makedirs(os.path.dirname(_SESSION_FILE), exist_ok=True)
        with open(_SESSION_FILE, "w", encoding="utf-8") as f:
            json.dump(sess, f, ensure_ascii=False, indent=1)
    except Exception:
        pass


def youtube_session_active() -> bool:
    """True while the user is in YouTube mode (recent YouTube command, not closed)."""
    s = _load()
    return bool(s.get("active")) and time.time() - s.get("updated", 0) < _SESSION_TTL


def _end_session():
    s = _load()
    s["active"] = False
    _save(s)


# ── results fetching ───────────────────────────────────────────────────────

def _dur_to_sec(d) -> int | None:
    if not d:
        return None
    try:
        parts = [int(p) for p in d.split(":")]
        sec = 0
        for p in parts:
            sec = sec * 60 + p
        return sec
    except Exception:
        return None


def _views(text) -> int | None:
    """'1,234,567 views' / '82 million views' / '1.2M' → int."""
    if not text:
        return None
    t = str(text).lower().replace(",", "")
    m = re.search(r"(\d+(?:\.\d+)?)\s*(k|m|b|thousand|million|billion)?", t)
    if not m:
        return None
    mult = {"k": 1e3, "thousand": 1e3, "m": 1e6, "million": 1e6, "b": 1e9, "billion": 1e9}.get(m.group(2) or "", 1)
    return int(float(m.group(1)) * mult)


def _initial_data(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": _UA, "Accept-Language": "en-US,en;q=0.9"})
    html = urllib.request.urlopen(req, timeout=8).read().decode("utf-8", "ignore")
    m = re.search(r"var ytInitialData\s*=\s*(\{.*?\});</script>", html, re.S)
    return (json.loads(m.group(1)) if m else None), html


def _parse_videos(data, limit: int, default_channel: str = "") -> list[dict]:
    """Collect videos from ytInitialData: classic videoRenderer (search) and the newer
    lockupViewModel (channel pages) → [{id,title,channel,duration,seconds,views}]."""
    out, seen = [], set()

    def add(vid, title, chan, dur, views):
        if vid and vid not in seen and len(out) < limit:
            seen.add(vid)
            out.append({"id": vid, "title": title or "Untitled", "channel": chan or default_channel,
                        "duration": dur or "LIVE", "seconds": _dur_to_sec(dur), "views": _views(views)})

    def walk(o):
        if len(out) >= limit:
            return
        if isinstance(o, dict):
            v = o.get("videoRenderer")
            if isinstance(v, dict) and v.get("videoId"):
                add(v["videoId"],
                    "".join(r.get("text", "") for r in v.get("title", {}).get("runs", [])),
                    (v.get("ownerText", {}).get("runs") or [{}])[0].get("text", ""),
                    v.get("lengthText", {}).get("simpleText"),
                    v.get("viewCountText", {}).get("simpleText"))
            lk = o.get("lockupViewModel")
            if isinstance(lk, dict) and lk.get("contentType") == "LOCKUP_CONTENT_TYPE_VIDEO":
                meta = lk.get("metadata", {}).get("lockupMetadataViewModel", {})
                parts = [p for row in meta.get("metadata", {}).get("contentMetadataViewModel", {})
                         .get("metadataRows", []) for p in row.get("metadataParts", [])]
                views = next((p.get("accessibilityLabel") for p in parts
                              if "view" in (p.get("accessibilityLabel") or "")), None)
                dur = None
                for ov in lk.get("contentImage", {}).get("thumbnailViewModel", {}).get("overlays", []):
                    for b in ov.get("thumbnailBottomOverlayViewModel", {}).get("badges", []):
                        txt = b.get("thumbnailBadgeViewModel", {}).get("text", "")
                        if re.fullmatch(r"\d+(?::\d{2}){1,2}", txt):
                            dur = txt
                add(lk.get("contentId"), meta.get("title", {}).get("content"), "", dur, views)
            for x in o.values():
                walk(x)
        elif isinstance(o, list):
            for x in o:
                walk(x)

    walk(data)
    return out


def _fetch_results(query: str, limit: int = 10) -> list[dict]:
    """Scrape YouTube's results page → [{id,title,channel,duration,seconds,views}]; [] on failure."""
    try:
        data, html = _initial_data("https://www.youtube.com/results?search_query="
                                   + urllib.parse.quote_plus(query) + "&hl=en")
        if not data:
            ids = list(dict.fromkeys(re.findall(r"watch\?v=([a-zA-Z0-9_-]{11})", html)))
            return [{"id": i, "title": f"Video {n + 1}", "channel": "", "duration": None,
                     "seconds": None, "views": None} for n, i in enumerate(ids[:limit])]
        return _parse_videos(data, limit)
    except Exception:
        return []


def _find_channel(name: str):
    """Best channel for a name → (title, '/@handle'), or None. Tries the 'Channels' search
    filter (twice: YouTube occasionally returns a page without ytInitialData), then the
    plain results page, which also lists matching channels."""
    q = urllib.parse.quote_plus(name)
    for url in (f"https://www.youtube.com/results?search_query={q}&sp=EgIQAg%253D%253D&hl=en",
                f"https://www.youtube.com/results?search_query={q}&sp=EgIQAg%253D%253D&hl=en",
                f"https://www.youtube.com/results?search_query={q}&hl=en"):
        hit = _find_channel_at(url, name)
        if hit:
            return hit
    print(f"[youtube_control] no channel found for {name!r}")
    return None


def _find_channel_at(url: str, name: str):
    try:
        data, _ = _initial_data(url)
        found = []

        def walk(o):
            if isinstance(o, dict):
                c = o.get("channelRenderer")
                if isinstance(c, dict):
                    base = c.get("navigationEndpoint", {}).get("browseEndpoint", {}).get("canonicalBaseUrl")
                    title = c.get("title", {}).get("simpleText", "")
                    if base:
                        found.append((title, base))
                for x in o.values():
                    walk(x)
            elif isinstance(o, list):
                for x in o:
                    walk(x)

        walk(data or {})
        if not found:
            return None
        # Best name match among YouTube's top channels; reject unrelated ones
        key = re.sub(r"\W", "", name.lower())

        def sim(title, base):
            t, b = re.sub(r"\W", "", title.lower()), re.sub(r"\W", "", base.lower().lstrip("/@"))
            if key in (t, b):
                return 2.0
            return max(difflib.SequenceMatcher(None, key, t).ratio(), difflib.SequenceMatcher(None, key, b).ratio(),
                       0.9 if key and (key in t or t in key) else 0)

        scored = sorted(((sim(t, b), i, t, b) for i, (t, b) in enumerate(found[:6])), key=lambda x: (-x[0], x[1]))
        if scored and scored[0][0] >= 0.5:
            return scored[0][2], scored[0][3]
        return None
    except Exception as e:
        print(f"[youtube_control] channel lookup failed: {type(e).__name__}: {e}")
        return None


def _short(title: str, n: int = 55) -> str:
    """Speakable short title: drop [..]/(..)/|-tails, emoji and hashtags, cap the length."""
    t = re.sub(r"\[[^\]]*\]|\([^)]*\)|#\w+", " ", title or "")
    t = re.split(r"\s[|•]\s", t)[0]
    t = "".join(ch for ch in t if ord(ch) < 0x2190 or 0x0900 <= ord(ch) <= 0x097F)
    t = re.sub(r"\s+", " ", t).strip(" -–:|")
    if len(t) > n:
        t = t[:n].rsplit(" ", 1)[0] + "…"
    return t or (title or "")[:n]


def _format_results(results: list[dict], query: str) -> str:
    lines = [f"Results for '{query}', Sir:"]
    for i, r in enumerate(results[:_SHOW_N], 1):
        meta = ", ".join(x for x in (r.get("channel"), r.get("duration")) if x)
        lines.append(f"{i}. {_short(r['title'], 70)}" + (f" ({meta})" if meta else ""))
    return "\n".join(lines)


# ── browser helpers (youtube_player is the low-level bridge) ────────────────

from app.services.youtube_player import (  # noqa: E402
    youtube_windows as _youtube_windows,
    focus as _focus,
    navigate as _navigate,
    send_keys as _player_keys,
    player_action as _player_action,
    current_video_info as _current_video_info,
    page_videos as _page_videos,
    open_video as _open_video,
    ensure_audible as _ensure_audible,
    parse_player_command as _parse_player_command,
)


def _mark_last():
    try:
        from app.services.media_state import set_last
        set_last("youtube")
    except Exception:
        pass


def youtube_tab_open() -> bool:
    """True if some browser window's active tab is YouTube."""
    return bool(_youtube_windows())


# ── choice resolution ──────────────────────────────────────────────────────

_FILLER = re.compile(
    r"\b(?:please|jarvis|the|a|video|videos|result|results|one|on|number|no\.|link|thumbnail|"
    r"for me|now|youtube|yt|play|open|click|watch|start|select|choose|put)\b", re.I)


def _resolve_choice(choice: str, sess: dict):
    """
    Map a spoken choice to a result index (0-based), or 'toggle' (resume current video),
    or None when nothing matches.
    """
    results = sess.get("results") or []
    cur = sess.get("current")
    c = (choice or "").lower().strip(" .,!?")
    if not c:
        return 0 if results else None

    # pure references: "it", "that", "this video", "the video"
    if re.fullmatch(r"(?:(?:play|open|click(?: on)?|watch|start)\s+)?(?:it|that|this|the)"
                    r"(?:\s+(?:video|one))?(?:\s+(?:now|please))?", c):
        return "toggle" if cur is not None else (0 if results else None)

    if not results:
        return None
    n = len(results)

    if re.search(r"\b(?:latest|newest|most recent|new (?:one|video|upload)|recent (?:one|video|upload)|last upload(?:ed)?)\b", c) \
            and sess.get("step") in ("channel", "playing", "results"):
        return 0                                  # channel videos (and search) are newest-first
    if re.search(r"\b(?:oldest)\b", c):
        return n - 1
    if re.search(r"\b(?:most (?:viewed|popular|watched)|popular|viral|famous|top viewed)\b", c) \
            and any(r.get("views") for r in results):
        return max(range(n), key=lambda i: results[i].get("views") or 0)
    if re.search(r"\b(?:next)\b", c):
        return min((cur if cur is not None else -1) + 1, n - 1)
    if re.search(r"\b(?:previous|prev|last one before|before that)\b", c):
        return max((cur or 0) - 1, 0)
    if re.search(r"\blast\b", c):
        return min(n, _SHOW_N) - 1

    short = len(c.split()) <= 4
    for w, i in _ORDINALS.items():
        if re.search(rf"\b{w}\s+(?:one|video|result|link)\b", c) or c in (w, "the " + w) \
                or (short and w != "top" and re.search(rf"\b{w}\b", c)):
            return min(i, n) - 1

    # duration: "the 52 minute one", "the 1 hour video"
    dm = re.search(r"(\d+(?:\.\d+)?)\s*(hour|hr|minute|min|second|sec)s?\b", c)
    if dm:
        mult = {"h": 3600, "m": 60, "s": 1}[dm.group(2)[0]]
        target = float(dm.group(1)) * mult
        timed = [(abs((r.get("seconds") or 10**9) - target), i) for i, r in enumerate(results)]
        return min(timed)[1]

    # "number 3", "video 2", "3", "#2"
    nm = re.search(r"(?:\b(?:number|no|video|result|option)\s*|#|^)(\d{1,2})\b", c)
    if nm and 1 <= int(nm.group(1)) <= n:
        return int(nm.group(1)) - 1
    for w, i in _NUM_WORDS.items():
        if re.search(rf"\b(?:number|video|result|option)\s+{w}\b", c) or c == w:
            return min(i, n) - 1

    # "by <channel>" / "from <channel>"
    cm = re.search(r"\b(?:by|from)\s+(.+)$", c)
    if cm:
        chan = cm.group(1).strip()
        scored = [(difflib.SequenceMatcher(None, chan, (r.get("channel") or "").lower()).ratio()
                   + (0.5 if chan in (r.get("channel") or "").lower() else 0), i)
                  for i, r in enumerate(results)]
        best = max(scored)
        if best[0] >= 0.6:
            return best[1]

    # free text: fuzzy over title + channel
    q = re.sub(r"\b(?:about|called|named|titled|with|which says|that says)\b", " ", c)
    q = re.sub(r"\s+", " ", _FILLER.sub(" ", q)).strip()
    if len(q) < 2:
        return None
    q_tokens = set(re.findall(r"\w+", q))
    best_i, best_s = None, 0.0
    for i, r in enumerate(results):
        hay = f"{r.get('title', '')} {r.get('channel', '')}".lower()
        h_tokens = set(re.findall(r"\w+", hay))
        overlap = len(q_tokens & h_tokens) / max(len(q_tokens), 1)
        s = overlap + 0.5 * difflib.SequenceMatcher(None, q, r.get("title", "").lower()).ratio()
        if s > best_s:
            best_i, best_s = i, s
    return best_i if best_s >= 0.6 else None


# ── public tools ───────────────────────────────────────────────────────────

def youtube_open(query: str = "") -> str:
    """Open YouTube and enter YouTube mode (Jarvis then waits for what to search/play)."""
    try:
        if query and query.strip():
            return youtube_search(query.strip(), autoplay=False)
        webbrowser.open("https://www.youtube.com")
        _save({"active": True, "step": "await_query", "query": None, "results": [],
               "current": None})
        return "YouTube is open, Sir. What should I search for?"
    except Exception as e:
        return f"I couldn't open YouTube: {e}"


def youtube_search(query: str, autoplay: bool = False) -> str:
    """Search YouTube; show numbered results (autoplay=False) or play the top video."""
    try:
        query = re.sub(r"\s+(?:on|in)\s+(?:youtube|yt)$", "", (query or "").strip(" .,!?\"'"),
                       flags=re.I)
        if isinstance(autoplay, str):
            autoplay = autoplay.strip().lower() in ("true", "1", "yes")
        if not query:
            return youtube_open()

        results = _fetch_results(query)
        sess = {"active": True, "step": "results", "query": query, "results": results,
                "current": None, "list_kind": "search"}

        if autoplay and results:
            v = results[0]
            if _navigate(f"https://www.youtube.com/watch?v={v['id']}").endswith("muted"):
                _ensure_audible(delay=2.5)
            sess.update(step="playing", current=0)
            _save(sess)
            _mark_last()
            return f"Playing {_short(v['title'])}, Sir."

        _navigate("https://www.youtube.com/results?search_query=" + urllib.parse.quote_plus(query))
        _save(sess)
        # Short on purpose: reading titles aloud blocks the voice agent from hearing the user.
        # "read the results" (youtube_list_results) reads them on request.
        return f"Here are the results for {query}, Sir. Which one should I play?"
    except Exception as e:
        return f"YouTube search failed: {e}"


def _screen_results(sess: dict) -> dict:
    """
    Replace the session's result list with the videos actually on screen in the front
    YouTube tab (the user's personalised order), so "play the first result" means the first
    one they SEE. On a watch page, a fresh Jarvis list (< 30 min) wins; otherwise the
    up-next sidebar is used. Returns the (possibly updated) session.
    """
    fresh_playing = sess.get("step") == "playing" and sess.get("results")         and time.time() - sess.get("updated", 0) < 30 * 60
    if fresh_playing:
        return sess          # watching a video picked from a list: "the second one" means that list
    page = _page_videos()
    if not page or not page.get("list"):
        return sess
    path = page.get("path") or ""
    fresh = time.time() - sess.get("updated", 0) < 30 * 60 and bool(sess.get("results"))
    if path.startswith("/watch") and fresh:
        return sess
    results = [{"id": v["id"], "title": v.get("title") or "Untitled", "channel": v.get("channel", ""),
                "duration": v.get("duration") or "", "seconds": _dur_to_sec(v.get("duration")),
                "views": None} for v in page["list"]]
    step = "playing" if path.startswith("/watch") else ("channel" if path.startswith("/@") or "/channel/" in path else "results")
    query = sess.get("query")
    m = re.search(r"search_query=([^&]+)", page.get("search") or "")
    if m:
        query = urllib.parse.unquote_plus(m.group(1))
    return {**sess, "active": True, "step": step, "query": query, "results": results,
            "current": None, "source": "screen", "list_kind": "channel" if step == "channel" else "screen"}


def youtube_play_result(choice: str = "first") -> str:
    """
    Open one of the videos on screen / in the last results: 'first result', 'second one', '3',
    'last', 'next', 'latest', 'most viewed', 'the one by <channel>', 'the 10 minute one', or a
    title fragment. Reads the front YouTube tab first, so the order matches what the user sees.
    """
    try:
        sess = _load()
        idx = _resolve_choice(choice, sess)
        if idx == "toggle":                       # "play it" with a video already open
            sess["active"] = True
            _save(sess)
            _mark_last()
            return _player_action("play")

        if _youtube_windows():
            sess = _screen_results(sess)
        elif time.time() - sess.get("updated", 0) > 30 * 60:
            sess = {**sess, "results": []}           # stale list: don't play something random
        if not sess.get("results"):
            return "I don't see any YouTube videos to pick from, Sir. What should I search for?"

        idx = _resolve_choice(choice, sess)
        if idx == "toggle":
            idx = 0
        if idx is None:
            _save(sess)
            return "I couldn't tell which video you meant, Sir. Say its number or part of its title."

        v = sess["results"][idx]
        if not (sess.get("source") == "screen" and _open_video(v["id"])):
            if _navigate(f"https://www.youtube.com/watch?v={v['id']}").endswith("muted"):
                _ensure_audible(delay=2.5)
        sess.update(active=True, step="playing", current=idx)
        _save(sess)
        _mark_last()
        return f"Playing {_short(v['title'])}, Sir."
    except Exception as e:
        return f"Couldn't open that video: {e}"


def youtube_channel(name: str, play_latest: bool = False) -> str:
    """Open a YouTube channel's Videos tab ("open MrBeast's channel") and load its latest
    videos so "play the latest one" / "play the second one" / a title fragment works.
    name="__current__" (or "this"/"his") = the channel of the video that's playing.
    play_latest=True plays its newest video straight away."""
    try:
        if isinstance(play_latest, str):
            play_latest = play_latest.strip().lower() in ("true", "1", "yes")
        if (name or "").strip().lower() in ("__current__", "this", "his", "her", "their", "current"):
            sess = _load()
            cur = sess.get("current")
            name = ""
            if cur is not None and sess.get("results") and cur < len(sess["results"]):
                name = sess["results"][cur].get("channel", "")
            if not name:
                info = _current_video_info() or {}
                name = info.get("author", "")
            if not name:
                return "I can't tell which channel this video is from, Sir."
        name = re.sub(r"^(?:the\s+)?(?:youtube\s+)?channel\s+(?:of\s+|called\s+|named\s+)?|"
                      r"(?:'s|s')?\s+(?:youtube\s+)?channel$|\s+on\s+(?:youtube|yt)$", "",
                      (name or "").strip(" .,!?\"'"), flags=re.I).strip()
        if not name:
            return "Which channel, Sir?"
        ch = _find_channel(name)
        if not ch:
            youtube_search(name)
            return f"I couldn't find a channel called {name}, so I searched for it instead, Sir."
        title, base = ch
        url = "https://www.youtube.com" + base + "/videos"
        if not play_latest:
            _navigate(url)
        videos = []
        try:
            data, _ = _initial_data(url + "?hl=en")
            videos = _parse_videos(data or {}, 30, default_channel=title)
        except Exception:
            pass
        sess = {"active": True, "step": "channel", "query": title, "channel": base,
                "results": videos, "current": None, "list_kind": "channel"}
        if play_latest and videos:
            v = videos[0]
            if _navigate(f"https://www.youtube.com/watch?v={v['id']}").endswith("muted"):
                _ensure_audible(delay=2.5)
            sess.update(step="playing", current=0)
            _save(sess)
            _mark_last()
            return f"Playing {title}'s latest video, {_short(v['title'])}, Sir."
        _save(sess)
        return f"Opened {title}'s channel, Sir. Which video should I play?"
    except Exception as e:
        return f"I couldn't open that channel: {e}"


def youtube_list_results() -> str:
    """Read out the current YouTube results / channel videos (only when the user asks)."""
    sess = _load()
    if not sess.get("results"):
        return "There are no YouTube results open right now, Sir."
    return _format_results(sess["results"], sess.get("query") or "your search")


def youtube_control(action: str, amount: float = 0, value: str = "") -> str:
    """
    Control the YouTube player in the browser (precise, via the page's player API).
    action: status | pause | play | toggle | forward | rewind | seek_to | seek_pct | seek_end |
            restart | speed | faster | slower | volume | volume_up | volume_down | mute | unmute |
            captions | loop | quality | skip_part | chapter_next | chapter_prev | chapter_goto |
            chapters | current_chapter | skip_ad | like | dislike | unlike | subscribe | theater |
            miniplayer | pip | fullscreen | exit_fullscreen | next | previous |
            back_to_results | close | exit_mode
    amount: seconds for forward/rewind/seek_to (or step for faster/slower/volume_up/down).
    value:  speed ("2", "1.5", "normal"), volume ("40"), percent for seek_pct, "on"/"off"
            for captions/loop, chapter number/name, quality ("1080", "max").
    """
    try:
        a = (action or "").lower().strip().replace(" ", "_")
        sess = _load()

        if a in ("exit_mode", "done", "stop_mode"):
            _end_session()
            return "Leaving YouTube mode, Sir."
        if a in ("close", "close_tab"):
            err = _player_keys(("ctrl", "w"))
            _end_session()
            return err or "Closed YouTube, Sir."
        # Next in a channel's video list is meaningful; for a search, the next results are
        # mostly re-uploads of the same video, so use YouTube's own Up Next instead.
        if a in ("next", "previous") and sess.get("list_kind") == "channel"                 and sess.get("results") and sess.get("current") is not None:
            return youtube_play_result(a)
        if a in ("back_to_results", "back"):
            err = _player_keys(("alt", "left"))
            if not err:
                sess.update(active=True, step="results")
                _save(sess)
            return err or "Went back, Sir."
        # legacy aliases from the first version of this tool
        a = {"resume": "play", "full_screen": "fullscreen", "exit_full_screen": "exit_fullscreen",
             "subtitles": "captions"}.get(a, a)

        reply = _player_action(a, amount, value)
        if _youtube_windows():
            sess["active"] = True
            _save(sess)
            if a in ("play", "pause", "toggle", "forward", "rewind", "seek_to", "speed", "next", "previous"):
                _mark_last()
        return reply
    except Exception as e:
        return f"YouTube control error: {e}"


# ── follow-up parser used by chat.py while YouTube mode is active ──────────

_CHANNEL_PATTERNS = [
    # "search for channel mr beast", "open the channel called t series", "find the youtube channel of dhruv rathee"
    r"^(?:search(?:\s+for)?|find|open|show(?:\s+me)?|go\s+to|take\s+me\s+to|look\s+(?:up|for)|visit)\s+(?:the\s+)?"
    r"(?:youtube\s+)?channel\s+(?:of\s+|called\s+|named\s+|for\s+)?(.+?)(?:\s+on\s+(?:youtube|yt))?$",
    # "open mrbeast's channel", "go to the t-series youtube channel", "search mr beast channel on youtube"
    r"^(?:search(?:\s+for)?|find|open|show(?:\s+me)?|go\s+to|take\s+me\s+to|look\s+(?:up|for)|visit|play)\s+(?:the\s+)?"
    r"(.+?)(?:'s|s')?\s+(?:youtube\s+)?channel(?:\s+on\s+(?:youtube|yt))?$",
]


def _is_positional(c: str) -> bool:
    """A pick by position, not by title: 'the first result', 'number 3', 'the latest one'.
    These must go to youtube_play_result (which reads the screen) even when Jarvis has no
    saved list, instead of becoming a search for the words 'the first result'."""
    c = (c or "").lower().strip(" .,!?")
    return bool(re.fullmatch(
        r"(?:the\s+)?(?:(?:very\s+)?(?:first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|last|top|"
        r"\d{1,2}(?:st|nd|rd|th)?|latest|newest|most recent|most viewed|most popular|oldest)"
        r"(?:\s+(?:one|video|result|search result|link|upload))?|(?:video|result|number|option)\s+(?:number\s+)?\w+|\d{1,2}|"
        r"(?:it|that|this)(?:\s+(?:one|video))?)", c))


def _last_media():
    try:
        from app.services.media_state import get_last
        return get_last()
    except Exception:
        return None


def _latest_of(t: str) -> str | None:
    """'play mrbeast's latest video' / 'play the latest video of t series' → channel name."""
    t = (t or "").lower().strip(" .,!?")
    m = re.match(r"^(?:play|open|watch|show(?:\s+me)?|put\s+on)\s+(?:the\s+)?(?:latest|newest|new|most recent|last)\s+"
                 r"(?:video|upload|vid)\s+(?:of|from|by|on)\s+(.+?)(?:'s)?(?:\s+(?:youtube\s+)?channel)?(?:\s+on\s+(?:youtube|yt))?$", t) \
        or re.match(r"^(?:play|open|watch|show(?:\s+me)?|put\s+on)\s+(.+?)(?:'s|s')\s+(?:latest|newest|new|most recent|last)\s+"
                    r"(?:video|upload|vid)(?:\s+on\s+(?:youtube|yt))?$", t)
    return m.group(1).strip() if m else None


def _channel_name(t: str) -> str | None:
    """Channel name from a request like 'open MrBeast's channel', else None."""
    t = (t or "").lower().strip(" .,!?")
    for pat in _CHANNEL_PATTERNS:
        m = re.match(pat, t)
        if m:
            name = m.group(1).strip(" '\"")
            if name in ("this", "that", "his", "her", "their", "this video's", "the video's", "its"):
                return "__current__"
            if name and name not in ("the", "my"):
                return name
    return None


# Player commands that also make sense for Spotify / the OS; outside YouTube mode they only
# go to YouTube when the message names the video.
_AMBIGUOUS = {"pause", "play", "mute", "unmute", "status", "like", "dislike", "unlike",
              "subscribe", "loop", "volume_up", "volume_down"}


def parse_youtube_followup(text: str, controls_only: bool = False) -> dict | None:
    """
    Interpret a message said while in YouTube mode. Returns a tool_intent dict
    ({"tool_name", "arguments"}, plus "bare": True for plain-text searches that chat.py
    should only honour if no other tool claims the message) or None to fall through.

    controls_only=True is used when YouTube mode has expired but a YouTube tab is in front:
    only unambiguous player commands ("speed 2x", "go to 5:30") are taken.
    """
    try:
        sess = _load()
        t = re.sub(r"\[attached_file:.*?\]", "", (text or ""), flags=re.I)
        t = re.sub(r"^(?:ok(?:ay)?|hey|so|now|and|then)?[\s,]*(?:jarvis)?[\s,]*", "", t.strip(), flags=re.I)
        t = re.sub(r"^(?:can you|could you|please|would you)\s+", "", t.lower().strip(" .,!?"))
        t = re.sub(r"\s+(?:please|for me)$", "", t).strip()
        if not t or "spotify" in t or "whatsapp" in t:
            return None
        # "switch to X", "change it to X", "put on X", "play X instead" → "play X"
        sw = re.fullmatch(r"(?:switch(?:\s+it)?\s+to|change\s+(?:it|this|that|the\s+(?:video|song)|this\s+(?:video|song))\s+to|"
                          r"change\s+to|put\s+on|now\s+play|instead\s+play|replace\s+(?:it|this)\s+with)\s+(.+)", t)
        if sw:
            t = "play " + sw.group(1).strip()
        t = re.sub(r"^play\s+(.+?)\s+instead$", r"play \1", t)
        names_video = bool(re.search(r"\b(?:video|youtube|yt)\b", t))

        def intent(tool, **args):
            return {"tool_name": tool, "arguments": args}

        # leave / close
        if re.search(r"\b(?:exit|leave|stop|end|quit)\s+(?:the\s+)?youtube\s+mode\b|\bdone with youtube\b", t):
            return intent("youtube_control", action="exit_mode")
        if re.fullmatch(r"(?:close|quit|exit|end|kill|shut)\s+(?:the\s+|this\s+|current\s+|that\s+)?"
                        r"(?:youtube|yt|video|tab|youtube tab|youtube video)", t):
            return intent("youtube_control", action="close")
        # "play another video", "something else", "next one"
        if re.fullmatch(r"(?:play|put\s+on|give\s+me|show\s+me)\s+(?:another|a\s+different|some\s+other|other|a\s+new)\s+"
                        r"(?:video|song|track|one|clip)|(?:play\s+)?something\s+else|(?:the\s+)?next\s+one", t):
            if controls_only and not names_video:
                return None
            return intent("youtube_control", action="next")
        # "go back", "go back to the previous video" = browser back (previous page / video)
        if re.fullmatch(r"go\s+back(?:\s+to\s+(?:the\s+)?(?:previous|last|old|earlier)\s+(?:video|page|one))?|previous\s+page|"
                        r"back\s+to\s+(?:the\s+)?(?:previous|last)\s+video", t):
            if controls_only and not names_video:
                return None
            return intent("youtube_control", action="back")

        # next / previous video
        if re.fullmatch(r"(?:play\s+|open\s+)?(?:the\s+)?(?:next|skip)(?:\s+(?:video|one|result|this video|this))?", t) \
                or t in ("skip this video", "skip this", "skip video"):
            if controls_only and not names_video:
                return None
            return intent("youtube_control", action="next")
        if re.fullmatch(r"(?:play\s+|open\s+)?(?:the\s+)?previous(?:\s+(?:video|one|result))?", t):
            if controls_only and not names_video:
                return None
            return intent("youtube_control", action="previous")
        if re.search(r"\b(?:back to|go back to|show)\s+(?:the\s+)?(?:results|search results|list)\b", t):
            return intent("youtube_control", action="back_to_results")

        # read the list aloud (only on request — search replies stay short)
        if not controls_only and re.search(
                r"\b(?:read|list|tell|say|show)(?: me| out)?(?: all)? (?:the )?(?:results|options|videos|list)\b|"
                r"\bwhat (?:are the|are my) (?:results|options|videos)\b|\bwhat (?:videos|results) (?:are there|did you find|came up)\b", t):
            return intent("youtube_list_results")

        # channels: "search for channel mr beast", "open mrbeast's channel", "go to the t-series channel"
        ch = _channel_name(t)
        if ch and not controls_only:
            return intent("youtube_channel", name=ch)
        lm = _latest_of(t)
        if lm and not controls_only:
            return intent("youtube_channel", name=lm, play_latest=True)

        # precise player commands (speed, seek, chapters, captions, volume, quality…)
        cmd = _parse_player_command(t)
        if cmd:
            action, amount, value = cmd
            if controls_only and action in _AMBIGUOUS and not names_video:
                return None
            # "pause" / "resume" right after using Spotify is for Spotify, not this video
            if action in ("pause", "play", "mute", "unmute") and not names_video and _last_media() == "spotify":
                return None
            return intent("youtube_control", action=action, amount=amount, value=value)
        if controls_only:
            return None

        # new search: "search X", "type X", "look up X", "find X"
        sm = re.match(r"^(?:search(?:\s+for)?|type(?:\s+in)?|look\s+(?:up|for)|find|show\s+me|search\s+youtube\s+for)\s+(.+)$", t)
        if sm:
            q = re.sub(r"\s+(?:on|in)\s+(?:youtube|yt|the search(?: bar| box)?|search(?: bar| box)?)$", "", sm.group(1))
            q = re.sub(r"\s+(?:there|in it|and search|and press enter)$", "", q).strip()
            if q:
                return intent("youtube_search", query=q, autoplay=False)

        # pick a result / play something
        vm = re.match(r"^(play|open|click(?:\s+on)?|watch|start|select|choose|put\s+on|go\s+to)\s+(.+)$", t)
        if vm:
            rest = vm.group(2).strip()
            if rest in ("youtube", "yt"):
                return None
            idx = _resolve_choice(rest, sess)
            if idx is not None or _is_positional(rest):
                return intent("youtube_play_result", choice=rest)
            q = re.sub(r"\s+(?:on|in)\s+(?:youtube|yt)$", "", rest)
            q = re.sub(r"^(?:the\s+)?(?:video|song)\s+(?:of|about|called|for)?\s*", "", q).strip()
            if q:
                return intent("youtube_search", query=q, autoplay=True)

        # bare choice: "the second one", "number 3", "3", "the one by lofi girl", "last one"
        if re.fullmatch(r"(?:the\s+)?(?:(?:first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|last|top|"
                        r"\d{1,2}(?:st|nd|rd|th)?)\s*(?:one|video|result)?|(?:number|video|result|option)\s+\w+|"
                        r"\d{1,2}|(?:the\s+)?one\s+(?:by|from|about)\s+.+)", t):
            if _resolve_choice(t, sess) is not None or _is_positional(t):
                return intent("youtube_play_result", choice=t)

        # Plain text right after "open youtube" = the search query ("lofi hip hop")
        if sess.get("step") == "await_query" and len(t.split()) <= 10 \
                and not re.match(r"^(?:what|who|when|where|why|how|tell me|can you|could you|is|are|do|does)\b", t):
            q = re.sub(r"^(?:for\s+)?", "", t)
            return {"tool_name": "youtube_search", "arguments": {"query": q, "autoplay": False},
                    "bare": True}
        return None
    except Exception as e:
        print(f"[youtube_control] follow-up parse error: {type(e).__name__}: {e}")
        return None


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    print(youtube_search(" ".join(sys.argv[1:]) or "lofi hip hop"))
