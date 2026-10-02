from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import re
import json
import asyncio
from app.services.llm import (
    generate_chat_response,
    check_for_tool_intent,
    conversation_history,
    _save_session,
)
from app.services.embeddings import get_embedding
from app.services.vector_store import search_similar_chunks
from app.services.tools import TOOL_REGISTRY
from app.services.dynamic_skill import run_dynamic_skill
from app.services.planner import run_agentic_plan, is_complex_task
from app.services.ui_inspector import get_screen_text_summary
from app.services.screen_reader import describe_screen_for_llm, read_screen_as_tool
from app.memory import find_skill, format_preferences_for_prompt

router = APIRouter()

class ChatRequest(BaseModel):
    prompt: str
    lang: str | None = None   # "en" | "hi" — spoken language from the voice agent's STT
    voice: bool = False       # reply will be spoken aloud (short, Devanagari for Hindi)


# ── YouTube query cleaner ──────────────────────────────────────────────────
_YT_STOP_PHRASES = re.compile(
    r'\s+(?:and\s+)?(?:play|click|open|select|choose|pick)\s+(?:the\s+)?'
    r'(?:first|top|1st|best)?\s*(?:result|video|one|it).*$',
    re.IGNORECASE
)
def _clean_yt_query(q: str) -> str:
    """Remove trailing action phrases from a YouTube search query."""
    q = _YT_STOP_PHRASES.sub('', q).strip().strip('.,!?')
    return q

_NON_CONTACTS = {
    'me', 'a', 'the', 'my', 'him', 'her', 'them', 'someone', 'anybody',
    'anyone', 'you', 'it', 'that', 'this', 'message', 'msg', 'text'
}

def detect_whatsapp_call(text: str):
    """Returns contact name if user wants to make a WhatsApp call, else None."""
    normalized = text.strip().rstrip('.,!?।')
    # Only match if user used a call-related word
    call_kw = re.search(r'\b(call|audio call|voice call|ring|phone)\b', normalized, re.IGNORECASE)
    if not call_kw:
        return None
    call_patterns = [
        # "make a/an (whatsapp) call to X" or "make a/an (whatsapp) call X"
        r'(?:make|place|give|do)\s+(?:an?\s+)?(?:whatsapp\s+)?(?:call|audio\s+call|voice\s+call)\s+(?:to\s+)?([\w\s\.]+?)(?:\s+on\s+(?:whatsapp|wp))?\s*$',
        # "call/ring/phone X on/via whatsapp"
        r'(?:call|ring|phone)\s+([\w\s\.]+?)\s+(?:on|via|using|through|over)\s+(?:whatsapp|wa|wp)',
        # "whatsapp call X" or "call X on whatsapp"
        r'(?:whatsapp\s+call|call)\s+([\w\s\.]+?)\s+(?:on|via|over)\s+whatsapp',
        # Broad fallback: any 'call' keyword combined with 'whatsapp' in same sentence
        r'(?:whatsapp\s+)?call\s+(?:to\s+)?([\w\s\.]{2,40})$',
    ]
    for pattern in call_patterns:
        m = re.search(pattern, normalized, re.IGNORECASE)
        if m:
            contact = m.group(1).strip().strip('.,!?')
            words = contact.lower().split()
            # Reject if contact looks like a non-contact word
            if len(contact) > 1 and not all(w in _NON_CONTACTS for w in words):
                return contact
    return None


def detect_whatsapp_send(text: str):
    # If it's a call intent, don't treat as send
    if detect_whatsapp_call(text):
        return None
    normalized = text.strip().rstrip('.,!?।')
    patterns = [
        r'send\s+(?:a\s+)?(?:message|msg|text|whatsapp\s+message)\s+to\s+([\w\s\.]+?)(?:\s+on\s+(?:whatsapp|wp)|$)',
        r'message\s+([\w\s\.]+?)\s+on\s+(?:whatsapp|wp)',
        r'whatsapp\s+(?:message\s+(?:to\s+)?|text\s+(?:to\s+)?)?([\w\s\.]+?)(?:\s+saying.*)?$',
        r'send\s+([\w\s\.]+?)\s+a\s+(?:message|msg|text|whatsapp)',
        r'send\s+(?:a\s+)?(?:message|msg|text)(?:\s+to)?\s+([\w\s\.]+?)(?:\s+on\s+(?:whatsapp|wp)|$)',
    ]
    for pattern in patterns:
        m = re.search(pattern, normalized, re.IGNORECASE)
        if m:
            contact = m.group(1).strip().strip('.,!?')
            words = contact.lower().split()
            if len(contact) > 1 and not all(w in _NON_CONTACTS for w in words):
                return contact
    return None

def detect_note_intent(text: str) -> bool:
    normalized = text.strip().rstrip('.,!?\u0964').lower()
    patterns = [
        r'^(?:add|create|write|make|put|save)\s+(?:a\s+)?(?:short\s+)?(?:note|sticky|reminder)(?:\s+(?:on|to|for)\s+\S+)?',
        r'^take\s+(?:a\s+)?note(?:\s+(?:for|on)\s+\S+)?',
        r'^(?:note|sticky|reminder)\s+(?:it|this|down)?',
        r'^remind\s+me\s+to',
    ]
    for p in patterns:
        if re.search(p, normalized):
            return True
    return False


def _named_app(lower: str) -> str:
    """'spotify' / 'youtube' if the sentence names a player, else '' (= whatever is playing)."""
    if re.search(r'\bspotify\b', lower):
        return "spotify"
    if re.search(r'\b(?:video|youtube|yt)\b', lower):
        return "youtube"
    return ""


def _media_target(lower: str) -> str | None:
    """Which player an ambiguous media command ("pause it", "next song") is for:
    named app > last app the user used (if still open) > whichever is open."""
    if "spotify" in lower:
        return "spotify"
    if re.search(r'\b(?:video|youtube|yt)\b', lower):
        return "youtube"
    try:
        from app.services.media_state import get_last, spotify_running
        from app.services.youtube_control import youtube_tab_open
        last = get_last()
        sp, yt = spotify_running(), youtube_tab_open()
        if last == "spotify" and sp:
            return "spotify"
        if last == "youtube" and yt:
            return "youtube"
        if sp:
            return "spotify"
        if yt:
            return "youtube"
    except Exception:
        pass
    return None


def keyword_detect_tool(prompt: str) -> dict | None:
    """
    Fast, 100% reliable keyword-based tool detection.
    Runs BEFORE the LLM router to catch common patterns the small router model misses.
    Returns a tool_intent dict or None.
    """
    lower = prompt.lower().strip()
    
    # Strip out attached files for keyword matching to prevent filename collisions
    lower = re.sub(r'\[attached_file:.*?\]', '', lower, flags=re.IGNORECASE).strip()
    # Voice transcripts arrive as "Pause that song." / "Jarvis, play the first result."
    lower = re.sub(r'^(?:(?:hey|ok|okay)\s+)?jarvis[\s,.!:-]+', '', lower)
    lower = lower.strip(' .,!?;:')
    
    # If the command is complex (multiple actions), let planner handle it.
    if is_complex_task(lower):
        return None

    # ── Weather / Temperature ─────────────────────────────────────────────
    weather_kw = ['weather', 'temperature', 'temp', 'rain', 'forecast',
                  'humid', 'sunny', 'cloudy', 'mausam', 'barish', 'garmi']
    if any(kw in lower for kw in weather_kw):
        return {"tool_name": "get_info", "arguments": {"query": prompt}}

    # ── Music / Song playback ─────────────────────────────────────────────
    question_words = ['which', 'who', 'what', 'when', 'where', 'how', 'tell me',
                      'about', 'details', 'learn', 'tune in', 'today', 'ipl',
                      'match', 'teams', 'cricket', 'news', 'score']
    is_question = any(w in lower for w in question_words)

    # ── Spotify player queries/controls (before the question filter) ──────
    if re.search(r"\bwhat(?:'s| is)\s+(?:this\s+song|the\s+song|playing|this\s+track)\b|"
                 r"\b(?:which|what)\s+song\s+is\s+(?:this|playing)\b", lower):
        return {"tool_name": "media_control", "arguments": {"action": "now_playing", "app": _named_app(lower)}}
    if re.search(r'\b(?:like|save|heart)\s+(?:this|the|current)\s+(?:song|track)\b|\badd\s+(?:this|the)\s+song\s+to\s+(?:my\s+)?liked', lower):
        return {"tool_name": "spotify_control", "arguments": {"action": "like"}}
    if re.fullmatch(r'(?:jarvis\s+)?(?:turn\s+(?:on|off)\s+|toggle\s+|enable\s+|disable\s+)?(?:shuffle|repeat)(?:\s+(?:on|off|mode|on spotify|the song|this song))?', lower):
        return {"tool_name": "spotify_control", "arguments": {"action": "shuffle" if "shuffle" in lower else "repeat"}}

    # ── YouTube CHANNEL: "open mrbeast's channel", "search for channel mr beast",
    #    "play mrbeast's latest video" (before generic search so "channel" isn't searched literally)
    try:
        from app.services.youtube_control import _channel_name, _latest_of
        _yt_l = re.sub(r'^(?:jarvis\s+)?(?:(?:can you|please|could you)\s+)?', '', lower).strip(' .,!?')
        _latest = _latest_of(_yt_l)
        if _latest:
            return {"tool_name": "youtube_channel", "arguments": {"name": _latest, "play_latest": True}}
        _chan = _channel_name(_yt_l)
        if _chan and _chan != "__current__":
            return {"tool_name": "youtube_channel", "arguments": {"name": _chan}}
    except Exception:
        pass

    # ── YouTube: "play X on youtube" / "open youtube and play X" → autoplay first result
    yt_play_m = (
        re.match(r'^(?:jarvis\s+)?(?:can you\s+)?play(?:\s+(?:me\s+)?(?:the\s+)?(?:song|music|track|video))?\s+(.+?)\s+on\s+(?:youtube|yt)\s*$', lower)
        or re.match(r'^(?:jarvis\s+)?(?:open|go to|launch)\s+(?:youtube|yt)\s+and\s+play\s+(?:the\s+)?(?:song\s+|video\s+)?(.+)$', lower)
        or re.match(r'^(?:jarvis\s+)?(?:youtube|yt)\s+play\s+(.+)$', lower)
    )
    if yt_play_m and not is_question:
        song = _clean_yt_query(yt_play_m.group(1).strip(' ,.'))
        return {"tool_name": "youtube_search", "arguments": {"query": song, "autoplay": True}}

    # ── Play on Spotify explicitly ──────────────────────
    spotify_play_m = re.search(
        r'(?:open\s+spotify\s+and\s+)?play(?:\s+(?:me\s+)?(?:the\s+)?(?:song|music|track|album|artist|playlist))?\s+(.+?)(?:\s+on\s+spotify)\s*$',
        lower
    ) or re.search(r'open\s+spotify\s+and\s+play\s+(?:the\s+)?(?:song\s+)?(.+)$', lower)
    if spotify_play_m and not is_question:
        song = spotify_play_m.group(1).strip(' ,.')
        return {"tool_name": "play_music", "arguments": {"song": song}}

    # ── Media grammar: switching / closing / "another" (voice phrasings) ──
    # "switch to X", "change it to X", "put on X", "play X instead" → "play X"
    _sw = re.fullmatch(r'(?:switch(?:\s+it)?\s+to|change\s+(?:it|this|that|the\s+(?:video|song|music|track)|this\s+(?:video|song))\s+to|'
                       r'change\s+to|put\s+on|now\s+play|instead\s+play|replace\s+(?:it|this)\s+with)\s+(.+)', lower)
    if _sw:
        lower = "play " + _sw.group(1).strip()
    lower = re.sub(r'^play\s+(.+?)\s+instead$', r'play \1', lower)

    # "close/stop/end this song" = stop listening (pause), not "close a window called 'this song'"
    if re.fullmatch(r'(?:please\s+)?(?:close|end|exit|quit|kill|turn\s+off|shut\s+off|switch\s+off|stop)\s+'
                    r'(?:this|the|current|that|my)?\s*(?:song|track|music|audio)(?:\s+(?:on spotify|on youtube|please|now))?', lower):
        # pause whatever is actually playing (Windows media sessions), not a guess
        return {"tool_name": "media_control", "arguments": {"action": "pause", "app": _named_app(lower)}}
    # "close this video" / "close the youtube tab" → close the YouTube tab
    if re.fullmatch(r'(?:please\s+)?(?:close|exit|quit|end|kill|shut)\s+(?:this|the|current|that)?\s*(?:youtube\s+)?(?:video|tab)'
                    r'(?:\s+on\s+youtube)?(?:\s+please)?', lower):
        return {"tool_name": "youtube_control", "arguments": {"action": "close"}}
    # "play another song/video", "play something else", "next one"
    if re.fullmatch(r'(?:play|put\s+on|give\s+me|show\s+me)\s+(?:another|a\s+different|some\s+other|other|a\s+new|the\s+next|next)\s+'
                    r'(?:video|song|track|one|music|clip)|(?:play\s+)?something\s+else|next\s+one|the\s+next\s+one', lower):
        _tgt = _media_target(lower)
        if _tgt == "youtube":
            return {"tool_name": "youtube_control", "arguments": {"action": "next"}}
        return {"tool_name": "media_control", "arguments": {"action": "next", "app": _named_app(lower)}}
    # "go back" / "go back to the previous video" (YouTube page history)
    if re.fullmatch(r'go\s+back(?:\s+to\s+(?:the\s+)?(?:previous|last|old|earlier)\s+(?:video|page|one|results?))?|previous\s+page|back\s+to\s+(?:the\s+)?(?:previous|last)\s+video', lower):
        if _media_target(lower) == "youtube":
            return {"tool_name": "youtube_control", "arguments": {"action": "back"}}
    # "watch X" → YouTube
    _w = re.fullmatch(r'watch\s+(?!(?:it|this|that|the\s+(?:first|second|third|last|latest|next)\b))(.+?)(?:\s+videos?)?(?:\s+on\s+(?:youtube|yt))?', lower)
    if _w and not is_question:
        return {"tool_name": "youtube_search", "arguments": {"query": _clean_yt_query(_w.group(1)), "autoplay": True}}

    # ── Spotify app: open / close ─────────────────────────────────────────
    if re.fullmatch(r'(?:please\s+)?(?:close|quit|exit|shut\s*down|kill|end)\s+(?:the\s+)?spotify(?:\s+app)?(?:\s+please)?', lower):
        return {"tool_name": "spotify_control", "arguments": {"action": "close"}}
    if re.fullmatch(r'(?:please\s+)?(?:open|launch|start)\s+(?:the\s+)?spotify(?:\s+app)?(?:\s+please)?', lower):
        return {"tool_name": "spotify_control", "arguments": {"action": "open"}}

    # ── Pause / resume: send to the player the user is actually using ─────
    # "pause", "pause it", "pause that song", "stop the music", "resume", "play it again"
    _pause_m = re.fullmatch(r'(?:please\s+)?(?:pause|stop|hold)(?:\s+(?:it|this|that|the|my))?'
                            r'(?:\s+(?:song|music|track|playback|audio|spotify|video|youtube|media|player))?'
                            r'(?:\s+(?:on spotify|on youtube|please|now|for a (?:sec|second|moment|bit)))?', lower)
    _resume_m = re.fullmatch(r'(?:please\s+)?(?:resume|continue|unpause|play)(?:\s+(?:it|this|that|the|my))?'
                             r'(?:\s+(?:song|music|track|playback|spotify|video|youtube|media))?'
                             r'(?:\s+(?:again|on spotify|on youtube|please|now))?', lower)
    if _pause_m or _resume_m:
        # Windows media sessions: pauses what is REALLY playing (any app, any tab, songs
        # started by hand), resumes the last-used player.
        return {"tool_name": "media_control",
                "arguments": {"action": "pause" if _pause_m else "play", "app": _named_app(lower)}}

    # ── Next / previous song: same targeting ─────────────────────────────
    _nx = re.search(r'\b(?:next|skip(?:\s+(?:this|the))?)\s+(?:song|track)\b|^next$|^skip$', lower)
    _pv = re.search(r'\b(?:previous|prev|last)\s+(?:song|track)\b|^previous$', lower)
    if _nx or _pv:
        _tgt = _media_target(lower)
        _act = "next" if _nx else "previous"
        if _tgt == "youtube" and _named_app(lower) != "spotify":
            return {"tool_name": "youtube_control", "arguments": {"action": _act}}
        return {"tool_name": "media_control", "arguments": {"action": _act, "app": _named_app(lower)}}

    # ── Pick / resume a YouTube video ("play the first result", "open the second one") ──
    # Reference-based play = a video on screen / in the last YouTube results, NOT a
    # Spotify song. Must be caught BEFORE the bare Spotify matcher.
    browser_video_play_kw = [
        'play that video', 'play this video', 'play the video',
        'play that one', 'play this one', 'play the first', 'play the top',
        'click on it', 'open that video', 'open it', 'click the video', 'click that',
    ]
    _ord = r'(?:first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|last|top|\d{1,2}(?:st|nd|rd|th)?)'
    _is_browser_video_play = (
        any(kw in lower for kw in browser_video_play_kw)
        or bool(re.search(r'play\s+the\s+\d+\s*(?:minute|min|hour|hr|second)s?\s+(?:one|video)', lower))
        or bool(re.search(rf'^(?:play|open|click(?:\s+on)?|watch|start)\s+(?:the\s+)?{_ord}\s+(?:one|video|result|link|search result)\b', lower))
        or bool(re.search(r'^(?:play|open|watch)\s+(?:video|result)\s+(?:number\s+)?\w+$', lower))
        or bool(re.search(r'^(?:play|open|watch|start)\s+(?:the\s+)?(?:latest|newest|most recent|most viewed|most popular|oldest)\s+(?:one|video|upload)s?$', lower))
        or (re.match(r'^play\s+(?:that|this|the)\b', lower) and 'spotify' not in lower
            and not re.match(r'^play\s+the\s+(?:song|music|track|album|artist|playlist)\b', lower))
    )
    if _is_browser_video_play:
        _choice = re.sub(r'^(?:play|open|click(?:\s+on)?|watch|start)\s+', '', lower).strip()
        return {"tool_name": "youtube_play_result", "arguments": {"choice": _choice or "that"}}

    # ── Bare "play X" (no platform) → default Spotify ─────────────────────────
    # Exclusions: don't route reference-based play to Spotify
    _spotify_exclusions = [
        'that', 'it', 'this', 'the video', 'the one', 'minutes', 'minute',
        'hour', 'top video', 'first video', 'second video',
    ]
    play_match = re.search(
        r'(?:open\s+spotify\s+and\s+)?\bplay(?:\s+(?:me\s+)?(?:the\s+)?(?:song|music|track|album|artist|playlist))?\s+(.+)',
        lower
    )
    if play_match and not is_question:
        song = play_match.group(1).strip(' ,.')
        song = re.sub(r'\s+(for me|please)$', '', song).strip()
        # "play mr beast video(s)" → YouTube
        _vid = re.fullmatch(r'(?:a\s+|some\s+|the\s+)?(.+?)\s+(?:video|videos|clip|clips)(?:\s+on\s+(?:youtube|yt))?', song)
        if _vid and _vid.group(1) not in ('that', 'this', 'the', 'it', 'a', 'another'):
            return {"tool_name": "youtube_search", "arguments": {"query": _clean_yt_query(_vid.group(1)), "autoplay": True}}
        # Skip if it looks like a context reference, not a song name
        if song and len(song) > 1 and not any(excl == song or song.startswith(excl + ' ') for excl in _spotify_exclusions):
            # While the user is watching YouTube, "play X" means YouTube (unless they say song/Spotify)
            if not re.search(r'\bspotify\b|^play\s+(?:the\s+|a\s+|me\s+)?(?:song|track|album|playlist)\b|\b(?:song|track)$', lower) \
                    and _media_target(lower) == "youtube":
                try:
                    from app.services.media_state import get_last
                    if get_last() == "youtube":
                        return {"tool_name": "youtube_search", "arguments": {"query": _clean_yt_query(song), "autoplay": True}}
                except Exception:
                    pass
            return {"tool_name": "play_music", "arguments": {"song": song}}

    # ── YouTube SEARCH (show numbered results, enters YouTube mode) ───────────
    yt_search_m = re.search(
        r'(?:search|find|look\s+up|look\s+for|show)\s+(?:for\s+)?(?:the\s+)?(?:channel|video|videos|playlist)?\s*(.+?)\s+(?:on|in)\s+(?:youtube|yt)\b',
        lower
    )
    if yt_search_m:
        query = _clean_yt_query(yt_search_m.group(1).strip())
        return {"tool_name": "youtube_search", "arguments": {"query": query, "autoplay": False}}

    yt_open_search_m = re.search(
        r'(?:youtube|yt)\s+(?:and\s+)?(?:search|find|type|look\s+up)\s+(?:for\s+)?(.+)',
        lower
    )
    if yt_open_search_m:
        query = _clean_yt_query(yt_open_search_m.group(1).strip())
        return {"tool_name": "youtube_search", "arguments": {"query": query, "autoplay": False}}

    if re.match(r'^(?:jarvis\s+)?(?:(?:can you|please)\s+)?(?:open|launch|start|go to)\s+(?:the\s+)?(?:youtube|yt)(?:\s+(?:app|website|for me|please))?\s*$', lower) \
            or re.fullmatch(r'(?:jarvis\s+)?(?:youtube|yt)', lower):
        return {"tool_name": "youtube_open", "arguments": {}}

    # ── News ──────────────────────────────────────────────────────────────
    news_kw = ['news', 'headlines', 'today news', 'latest news', 'breaking']
    if any(kw in lower for kw in news_kw):
        return {"tool_name": "get_info", "arguments": {"query": f"{prompt} today"}}

    # ── Sports / Match scores ─────────────────────────────────────────────
    sports_kw = ['ipl', 'match', 'score', 'cricket', 'football', 'tournament',
                 'standings', 'winner', 'result today']
    if any(kw in lower for kw in sports_kw):
        return {"tool_name": "get_info", "arguments": {"query": f"{prompt} 2025"}}

    # ── Stock / Finance ───────────────────────────────────────────────────
    finance_kw = ['stock price', 'share price', 'sensex', 'nifty', 'bitcoin', 'crypto']
    if any(kw in lower for kw in finance_kw):
        return {"tool_name": "get_info", "arguments": {"query": prompt}}

    # ── Time ──────────────────────────────────────────────────────────────
    if re.search(r'\btime\b|\bdate\b|\bday\b', lower) and len(lower) < 25:
        return {"tool_name": "get_system_time", "arguments": {}}

    # ── Screenshot ────────────────────────────────────────────────────────
    if any(w in lower for w in ['screenshot', 'screen shot', 'take ss', 'capture screen']):
        return {"tool_name": "take_screenshot", "arguments": {}}

    # ── Volume ────────────────────────────────────────────────────────────
    if re.search(r'\bvolume up\b|\bloud(er)?\b|\bincrease volume\b', lower):
        return {"tool_name": "volume_up", "arguments": {}}
    if re.search(r'\bvolume down\b|\bquiet(er)?\b|\blower volume\b|\bdecrease volume\b', lower):
        return {"tool_name": "volume_down", "arguments": {}}
    if re.search(r'\bmute\b', lower):
        return {"tool_name": "mute_volume", "arguments": {}}

    # ── Media (Next/Prev) ──────────────────────────────────────────────────
    if re.search(r'\bprev\b', lower):
        return {"tool_name": "spotify_control", "arguments": {"action": "previous"}}

    # ── Media Enhancement (Dark Image/Video) ───────────────────────────────
    if re.search(r'\b(enhance|fix)\b.*\b(image|video|photo|media|picture|dark)\b', lower):
        media_path = ""
        attached_media = re.findall(r'\[ATTACHED_FILE:\s*(.+?)\]', prompt)
        if attached_media:
            media_path = attached_media[0].strip()
        return {"tool_name": "enhance_media", "arguments": {"file_path": media_path}}

    # ── Prompt Enhancer (Bypass LLM Router & Conversational LLM) ───────────
    if lower.startswith("enhance ") or lower.startswith("refine "):
        clean_prompt = re.sub(r'^(enhance|refine)\s+(this\s+)?(prompt)?\s*[:\"\'\-]*\s*', '', prompt, flags=re.IGNORECASE).strip(' "\'')
        from app.services.skill_prompt_enhancer import enhance_prompt
        res = enhance_prompt(clean_prompt)
        
        # If it has the SYSTEM DIRECTIVE wrapper, strip it for direct streaming
        if "SYSTEM DIRECTIVE TO JARVIS:" in res:
            res = res.split("**ENHANCED PROMPT", 1)[-1]
            res = "**ENHANCED PROMPT" + res
            
        async def flow_stream(): yield res
        from fastapi.responses import StreamingResponse
        return StreamingResponse(flow_stream(), media_type="text/event-stream")

    # ── WhatsApp (Smart — fuzzy, two-phase, confirmation) ────────────────────
    if 'whatsapp' in lower or ('send' in lower and ('message' in lower or 'msg' in lower or 'text' in lower) and re.search(r'\bto\b', lower)):
        # — WhatsApp CALL: always check FIRST before any send logic
        call_contact = detect_whatsapp_call(prompt)
        if call_contact:
            return {"tool_name": "initiate_whatsapp_call", "arguments": {"contact_name": call_contact}}

        # — Read messages
        read_wa = re.search(
            r'(?:read|show|check|open|what(?:\'s| are| did| has)|any)\s+(?:my\s+)?(?:whatsapp\s+)?(?:messages?|chats?|msgs?)\s+(?:from|with|of)\s+(.+?)(?:\s*\?|$)',
            lower
        )
        if read_wa:
            contact = read_wa.group(1).strip().strip('.,!?')
            return {"tool_name": "read_whatsapp_messages", "arguments": {"contact_name": contact}}

        # — Just open WhatsApp
        if re.search(r'\bopen\s+whatsapp\b|\blaunch\s+whatsapp\b|\bstart\s+whatsapp\b', lower):
            if not any(w in lower for w in ['send', 'message', 'msg', 'text']):
                return {"tool_name": "open_whatsapp", "arguments": {}}


        # — Confirmed send: user said 'yes send it' / 'yes go ahead' after confirmation
        confirm_wa = re.search(
            r'(?:yes|yeah|yep|confirm|go ahead|send it|do it|ok|okay|haan|kar do)',
            lower
        )
        # We detect confirmed send via pending state stored in conversation — look for last assistant msg
        history_list_wa = list(conversation_history)
        last_assistant = next(
            (m['content'] for m in reversed(history_list_wa) if m['role'] == 'assistant'), ''
        )
        if confirm_wa and 'Should I go ahead and send this?' in last_assistant:
            # Extract To/Message from the previous confirmation block
            to_match = re.search(r'To:\s*(.+)', last_assistant)
            msg_match = re.search(r'Message:\s*"(.+?)"', last_assistant)
            if to_match and msg_match:
                confirmed_contact = to_match.group(1).strip()
                confirmed_msg = msg_match.group(1).strip()
                return {"tool_name": "confirm_whatsapp_send", "arguments": {
                    "contact_name": confirmed_contact, "message": confirmed_msg
                }}

        # — User picks a contact by number after disambiguation
        pick_wa = re.search(r'^(?:jarvis\s+)?(?:send it to\s+)?(?:number\s+)?(\d+)(?:\s+.+)?$', lower)
        if pick_wa and 'Which one should I send' in last_assistant:
            choice_num = int(pick_wa.group(1)) - 1
            # Extract names from numbered list in last assistant message
            listed_names = re.findall(r'\d+\.\s+(.+)', last_assistant)
            if 0 <= choice_num < len(listed_names):
                # Get the message from conversation context
                last_user_with_msg = next(
                    (m['content'] for m in reversed(history_list_wa) if m['role'] == 'user' and ('send' in m['content'].lower() or 'message' in m['content'].lower())), ''
                )
                msg_from_ctx = re.search(r'(?:message|saying|say|tell(?:ing)?\s+(?:him|her|them)?)[:\s]+["\']?(.+?)["\']?\s*$', last_user_with_msg, re.I)
                picked_name = listed_names[choice_num].strip()
                picked_msg = msg_from_ctx.group(1).strip() if msg_from_ctx else ""
                if picked_msg:
                    return {"tool_name": "initiate_whatsapp_send", "arguments": {
                        "contact_name": picked_name, "message": picked_msg
                    }}

        # — Send message: extract contact and message from sentence
        send_wa = re.search(
            r'(?:send|text|message|msg)\s+(?:a\s+)?(?:message\s+)?(?:to\s+)?(.+?)\s+(?:saying|saying that|that|:)[\s"\'](.+?)["\']?$',
            lower
        )
        if not send_wa:
            send_wa = re.search(
                r'(?:send|text|message|msg)\s+(.+?)\s+(?:on|via|using)?\s*(?:whatsapp)?[:\s]+["\']?(.+?)["\']?$',
                lower
            )
        if send_wa:
            contact = send_wa.group(1).strip().strip('.,!?')
            msg = send_wa.group(2).strip().strip('.,!?"\'')
            # Phase 1: always ask to search first if name is short/ambiguous (could be multiple people)
            if len(contact.split()) <= 2:
                return {"tool_name": "initiate_whatsapp_send", "arguments": {
                    "contact_name": contact, "message": msg
                }}
            return {"tool_name": "initiate_whatsapp_send", "arguments": {
                "contact_name": contact, "message": msg
            }}

        # — Just search/find contact
        search_wa = re.search(
            r'(?:find|search|look\s+up|who\s+is)\s+(.+?)\s+(?:on|in)?\s*whatsapp',
            lower
        )
        if search_wa:
            return {"tool_name": "search_whatsapp_contact", "arguments": {
                "name": search_wa.group(1).strip()
            }}


    # ── Smart Web Action (Search → Fetch → Synthesize) ─────────────────────
    # Pattern 1: "go to <site> and find/search <task>"
    smart_nav_1 = re.search(r'(?:go to|open|browse)\s+(?:the\s+)?(?:site of\s+)?(.+?)\s+and\s+(search for.+|find.+|get.+|show.+|list.+)$', lower)
    if smart_nav_1:
        site = smart_nav_1.group(1).strip()
        task = smart_nav_1.group(2).strip()
        return {"tool_name": "agentic_web_action", "arguments": {"site_or_task": site, "specific_task": task}}

    # Pattern 2: "find/search <task> on/in <site>"
    smart_nav_2 = re.search(r'(?:search for|find|list|show me)\s+(.+?)\s+(?:on|in|at|from)\s+([a-zA-Z0-9]+)(?:\s+site|\s+website)?$', lower)
    if smart_nav_2 and not "whatsapp" in smart_nav_2.group(2).lower() and not "youtube" in smart_nav_2.group(2).lower():
        task = smart_nav_2.group(1).strip()
        site = smart_nav_2.group(2).strip()
        return {"tool_name": "agentic_web_action", "arguments": {"site_or_task": site, "specific_task": task}}

    # Pattern 3: General research / browse questions that need live web data
    web_research_kw = [
        "find me", "search for", "look up", "what are", "list of",
        "upcoming hackathons", "upcoming contests", "latest", "recent",
        "browse", "check online", "search online", "search the web",
        "find online", "look online", "find hackathons", "find internships",
        "find jobs", "find competitions", "search web",
    ]
    if any(kw in lower for kw in web_research_kw) and len(lower.split()) >= 3:
        return {"tool_name": "agentic_web_action", "arguments": {"site_or_task": lower}}
    # ── Adjust window layout ───────────────────────────────────────────────
    # Semantic approach: works for ANY phrasing the user might say, e.g.:
    #   "tune in screen of VS Code to upper left"
    #   "set the Microsoft Edge tab to upper right"
    #   "snap Chrome to left"
    #   "adjust my window to 60% horizontally"
    #   "move it to bottom right"
    #   "put VS Code in the upper left"

    def _semantic_window_adjust(text: str):
        """
        Semantic window layout parser.
        Returns {"position":..., "width_percent":..., "height_percent":..., "app_name":...} or None.
        Works by:
          1. Checking the text contains a layout trigger verb
          2. Finding position keyword OR percentage anywhere in the text
          3. Extracting app name by subtracting all known filler from the text
        """
        # ── Step 1: Must contain a layout trigger verb ────────────────────
        _LAYOUT_VERBS = r'\b(adjust|move|set|resize|snap|put|place|pin|tile|shift|tune|bring|send|dock|push|slide|position)\b'
        if not re.search(_LAYOUT_VERBS, text):
            return None

        # ── Step 2: Resolve spoken numbers → digits ───────────────────────
        spoken_map = {
            'ten': '10', 'twenty': '20', 'thirty': '30', 'forty': '40', 'fifty': '50',
            'sixty': '60', 'seventy': '70', 'eighty': '80', 'ninety': '90', 'hundred': '100',
            'twenty five': '25', 'seventy five': '75', 'thirty three': '33', 'sixty six': '66',
            'half': '50', 'quarter': '25', 'three quarters': '75', 'three quarter': '75',
        }
        t = text
        for word, digit in spoken_map.items():
            t = re.sub(r'\b' + word + r'\b(\s*percent)?', digit + '%', t)

        # ── Step 3: Find position ─────────────────────────────────────────
        pos = None
        pos_checks = [
            ('top_left',     r'\b(upper\s+left|top\s+left)\b'),
            ('top_right',    r'\b(upper\s+right|top\s+right)\b'),
            ('bottom_left',  r'\b(bottom\s+left|lower\s+left)\b'),
            ('bottom_right', r'\b(bottom\s+right|lower\s+right)\b'),
            ('left',         r'\bleft\b'),
            ('right',        r'\bright\b'),
            ('top',          r'\b(top|upper)\b'),
            ('bottom',       r'\b(bottom|lower)\b'),
            ('center',       r'\b(center|centre|middle)\b'),
        ]
        for pos_name, pat in pos_checks:
            if re.search(pat, t):
                pos = pos_name
                break

        # ── Step 4: Find percentage ───────────────────────────────────────
        w_pct = h_pct = None
        pct_m = re.findall(r'(\d+)\s*%', t)
        if pct_m:
            if re.search(r'\b(horizontally|horizontal|width)\b', t):
                w_pct = int(pct_m[0])
            elif re.search(r'\b(vertically|vertical|height)\b', t):
                h_pct = int(pct_m[0])
            elif len(pct_m) >= 2:
                w_pct = int(pct_m[0])
                h_pct = int(pct_m[1])
            else:
                # Single unlabelled percentage → treat as width
                w_pct = int(pct_m[0])

        # Must have found EITHER a position or a percentage
        if not pos and not (w_pct or h_pct):
            return None

        # ── Step 5: Extract app name ──────────────────────────────────────
        # Remove all words that are NOT the app name
        _STRIP_WORDS = {
            # Layout verbs
            'adjust', 'move', 'set', 'resize', 'snap', 'put', 'place', 'pin',
            'tile', 'shift', 'tune', 'bring', 'send', 'dock', 'push', 'slide',
            'position', 'in', 'into',
            # Articles / pronouns
            'the', 'my', 'a', 'an', 'this', 'that', 'it', 'its', 'i', 'will',
            'you', 'me', 'we', 'us', 'going', 'want', 'can', 'could', 'should',
            'would', 'let', 'make',
            # Layout nouns
            'screen', 'tab', 'window', 'current', 'active', 'section', 'part',
            'side', 'area', 'half', 'quarter', 'portion',
            # Connectors
            'of', 'to', 'at', 'for', 'from', 'on', 'with', 'and', 'or', 'is', 'be',
            # Direction words
            'upper', 'lower', 'top', 'bottom', 'left', 'right',
            'center', 'centre', 'middle',
            # Filler
            'please', 'jarvis', 'ok', 'okay', 'now', 'just', 'hey', 'hi',
            # Orientation helpers
            'horizontally', 'horizontal', 'vertically', 'vertical',
            'width', 'height', 'percent', 'percentage',
        }

        # Remove percentage tokens from text first
        clean = re.sub(r'\d+\s*%', '', t)
        # Tokenise and filter
        tokens = re.split(r'[\s,\.!?]+', clean)
        app_tokens = []
        for tok in tokens:
            tok_clean = tok.strip().lower()
            if not tok_clean:
                continue
            # Skip pure position phrases already captured
            if tok_clean in _STRIP_WORDS:
                continue
            # Skip numeric-only tokens
            if re.match(r'^\d+$', tok_clean):
                continue
            app_tokens.append(tok)

        app_name = ' '.join(app_tokens).strip()
        # Reject very short or clearly non-app leftovers
        if len(app_name) <= 1 or app_name.lower() in ('', 'it', 'i', 'up', 'out'):
            app_name = None

        result = {"position": pos, "width_percent": w_pct, "height_percent": h_pct}
        if app_name:
            result["app_name"] = app_name
        return result

    # Slide/presentation talk ("put the image on the left of slide 3") is a PPT edit, not a window move.
    _is_slide_talk = re.search(r'\bslides?\s*\d|\b(ppt|deck|presentation|powerpoint)\b|'
                               r'\b(first|second|third|fourth|fifth|last|title|closing|final|cover|\d+(st|nd|rd|th))\s+slide\b', lower)
    _adj = None if _is_slide_talk else _semantic_window_adjust(lower)
    if _adj is not None:
        return {"tool_name": "adjust_active_window", "arguments": _adj}

    # ── Close / Minimize / Maximize specific app ──────────────────────────
    close_m = re.match(r'^(?:jarvis\s+)?close\s+(.+?)(?:\s+(?:window|app))?\s*$', lower)
    if close_m:
        target = close_m.group(1).strip().strip('.,!?')
        if target in ('tab', 'this tab', 'the tab', 'current tab', 'the current tab'):
            return {"tool_name": "close_tab", "arguments": {}}
        if target in ('the current', 'current', 'this', 'active', 'the current window', 'current window', 'this window', 'active window'):
            return {"tool_name": "close_window", "arguments": {}}
        return {"tool_name": "close_specific_window", "arguments": {"app_name": target}}

    minimize_m = re.match(r'^(?:jarvis\s+)?(?:minimize|minimise|hide)\s+(.+?)(?:\s+(?:window|app|tab))?\s*$', lower)
    if minimize_m:
        app = minimize_m.group(1).strip().strip('.,!?')
        if app in ('the current', 'current', 'this', 'active', 'the current window', 'current window', 'this window', 'active window', 'all windows', 'everything', 'all', 'every window'):
            return {"tool_name": "minimize_all_windows", "arguments": {}}
        return {"tool_name": "minimize_window", "arguments": {"app_name": app}}

    maximize_m = re.match(r'^(?:jarvis\s+)?(?:maximize|maximise|fullscreen|full screen|enlarge|expand)\s+(.+?)(?:\s+(?:window|app|tab))?\s*$', lower)
    if maximize_m:
        return {"tool_name": "maximize_window", "arguments": {"app_name": maximize_m.group(1).strip().strip('.,!?')}}


    # ── Layer 3 Intent Router: Screen reading with describe / suggest / execute modes ──
    # DESCRIBE mode: "What am I looking at?", "What's on my screen?"
    describe_screen_kw = [
        "what's on my screen", "whats on my screen", "what is on my screen",
        "what am i looking at", "what am i looking", "describe my screen",
        "read my screen", "read the screen", "what's on screen",
        "what can you see", "what's open", "whats open on my screen",
        "read what's on", "tell me what's on", "tell me what is on my screen",
        "what is this", "what app is open", "describe what you see",
        "what's happening on my screen", "what page am i on",
    ]
    if any(kw in lower for kw in describe_screen_kw):
        return {"tool_name": "read_my_screen", "arguments": {"intent_mode": "describe", "user_query": prompt}}

    # SUGGEST mode: "Help me", "What should I do?", "What's next?"
    suggest_screen_kw = [
        "what should i do", "help me with my screen", "what's next",
        "whats next", "what do i do here", "any suggestions",
        "what would you recommend", "what are my options",
        "how should i proceed", "what should i do here",
        "what can i do next", "suggest something", "give me suggestions",
    ]
    if any(kw in lower for kw in suggest_screen_kw):
        return {"tool_name": "read_my_screen", "arguments": {"intent_mode": "suggest", "user_query": prompt}}

    # EXECUTE mode: "Fix this", "Do that", "Fix the error"
    execute_screen_kw = [
        "fix this", "fix the error", "fix it", "do that",
        "resolve this", "handle this", "take care of this",
        "apply the fix", "correct this", "debug this",
    ]
    if any(kw in lower for kw in execute_screen_kw):
        return {"tool_name": "read_my_screen", "arguments": {"intent_mode": "execute", "user_query": prompt}}

    # ── Search on a specific site ────────────────────────────────────────────
    # "search on Stack Overflow for Python error"
    # "find Python projects on GitHub"
    # "look up asyncio on Reddit"
    # Pattern 1: search <query> on <site>
    search_on_site_m1 = re.search(
        r'(?:search|find|look\s+up|look\s+for)\s+(.+?)\s+(?:on|in)\s+([\w\s\.\-]+(?:\.com|\.in|\.org|\.net|\.io)?)\s*$',
        lower
    )
    # Pattern 2: search on <site> for <query>
    search_on_site_m2 = re.search(
        r'(?:search|find|look\s+up|look\s+for)\s+(?:on|in)\s+([\w\s\.\-]+(?:\.com|\.in|\.org|\.net|\.io)?)\s+for\s+(.+)$',
        lower
    )
    
    match = search_on_site_m1 or search_on_site_m2
    if match:
        if match == search_on_site_m1:
            q, site = match.group(1).strip(), match.group(2).strip()
        else:
            site, q = match.group(1).strip(), match.group(2).strip()
            
        # Exclude YouTube (handled by youtube_search) and Google
        if site not in ('youtube', 'yt', 'google'):
            return {"tool_name": "search_site", "arguments": {"query": q, "site_url": site}}

    # ── Scrape / read a URL ──────────────────────────────────────────────────
    # "read the page https://example.com"  /  "open example.com and tell me what it says"
    url_in_prompt = re.search(
        r'https?://[^\s]+|(?:www\.)?[\w\-]+\.(?:com|in|org|net|io|co)\b[^\s]*',
        lower
    )
    scrape_trigger_kw = [
        'read the page', 'read this page', 'read this url', 'read this link',
        'what does this page say', 'what does this site say',
        'scrape this', 'extract from this url', 'tell me what this page says',
        'open this link and read', 'read the content of',
    ]
    if url_in_prompt and any(kw in lower for kw in scrape_trigger_kw):
        url = url_in_prompt.group(0)
        return {"tool_name": "scrape_url", "arguments": {"url": url}}

    # ── File System Operations (Step 4) ──────────────────────────────────────

    # READ FILE: "read my todo.txt", "what's in notes.txt", "open and read report.pdf"
    read_file_m = re.search(
        r'(?:read|open and read|show|what(?:\'s| is) in|contents? of|show me)\s+(?:the\s+|my\s+)?(?:file\s+)?["\']?([\w\s\-\.\/\\]+\.[\w]+)["\']?',
        lower
    )
    if read_file_m and 'page' not in lower and 'url' not in lower:
        fpath = read_file_m.group(1).strip()
        return {"tool_name": "read_file", "arguments": {"path": fpath}}

    # LIST DIRECTORY: "list files on my desktop", "what's in my downloads folder"
    list_dir_kw = [
        'list files', 'list the files', 'show files', 'what files', "what's in my",
        'whats in my', 'show me my', 'what is in my', 'list my', 'list folder',
        'show folder', 'list directory',
    ]
    if any(kw in lower for kw in list_dir_kw):
        # Extract which folder
        folder_m = re.search(
            r'\b(desktop|downloads|documents|pictures|music|videos|onedrive)\b', lower
        )
        folder = folder_m.group(1) if folder_m else "Desktop"
        return {"tool_name": "list_directory", "arguments": {"path": folder}}

    # DELETE FILE: "delete todo.txt", "remove the file notes.txt", "trash my report"
    delete_m = re.search(
        r'(?:delete|remove|trash|get rid of)\s+(?:the\s+|my\s+|file\s+)?["\']?([\w\s\-\.\/\\]+\.[\w]+)["\']?',
        lower
    )
    if delete_m:
        fpath = delete_m.group(1).strip()
        return {"tool_name": "delete_file", "arguments": {"path": fpath}}

    # SEARCH FILES: "find my resume.pdf", "where is notes.txt", "search for *.pdf"
    search_file_m = re.search(
        r'(?:find|search for|where is|locate|look for)\s+(?:the\s+|my\s+|file\s+)?["\']?([\w\s\-\.\*]+\.[\w\*]+)["\']?',
        lower
    )
    if search_file_m and 'email' not in lower and 'web' not in lower:
        return {"tool_name": "search_files", "arguments": {"name": search_file_m.group(1).strip()}}

    # ── Google Calendar (Step 8) ──────────────────────────────────────────────
    
    calendar_today_kw = [
        "what's on my schedule today", "what do i have today", "my agenda today",
        "what is on my calendar today", "today's schedule"
    ]
    if any(kw in lower for kw in calendar_today_kw):
        return {"tool_name": "check_today_schedule", "arguments": {}}
        
    calendar_week_kw = [
        "upcoming events", "what's on my calendar", "my schedule this week",
        "events this week"
    ]
    if any(kw in lower for kw in calendar_week_kw):
        return {"tool_name": "get_upcoming_events", "arguments": {"days": 7}}

    # ── Morning Brief (Step 10) ───────────────────────────────────────────────
    brief_kw = [
        "morning brief", "good morning", "morning summary"
    ]
    if any(kw in lower for kw in brief_kw):
        return {"tool_name": "get_morning_brief", "arguments": {}}

    # ── Long-Term Memory Recall (RAG) ─────────────────────────────────────────
    # Explicit recall queries: Jarvis uses FAISS to search past conversation turns.
    # This triggers a HIGH-RECALL search (top_k=10, min_score=0.2) for wide coverage.
    # Note: implicit semantic recall also happens automatically in llm.py for ALL queries.
    memory_recall_kw = [
        "what did i say", "what did i tell you", "do you remember",
        "you told me", "i told you", "i mentioned", "i said",
        "remind me", "recall", "remember when", "last time i",
        "you remember", "earlier i said", "previously i",
        "what was my", "what were my", "from last week", "from yesterday",
        "from last month", "last session", "past conversation",
        "memory", "forget about", "what have i told",
    ]
    if any(kw in lower for kw in memory_recall_kw):
        return {"tool_name": "recall_memory", "arguments": {"query": prompt}}

    # ── Gmail / Email (Step 5) ────────────────────────────────────────────────

    # UNREAD: "do I have any unread emails", "show unread", "any new emails"
    if re.search(r'\bunread\b.*\bemail', lower) or re.search(r'\bemail.*\bunread\b', lower) or \
       re.search(r'\bnew\s+emails?\b', lower) or lower.strip() in ('any new emails', 'show unread emails'):
        return {"tool_name": "list_unread", "arguments": {"max_results": 5}}

    # SUMMARIZE: "summarize my inbox", "what emails do I have", "check my inbox"
    summarize_kw = [
        'summarize my inbox', 'summarize inbox', 'email summary',
        'what emails do i have', 'check my inbox', 'morning emails',
        'what is in my inbox', "what's in my inbox",
    ]
    if any(kw in lower for kw in summarize_kw):
        return {"tool_name": "summarize_inbox", "arguments": {"max_results": 10}}

    # CHECK EMAILS by topic/sender: "check my emails", "any emails about X", "emails from Y"
    email_check_kw = [
        'check my email', 'check email', 'check emails',
        'any emails', 'do i have emails', 'any email',
        'emails about', 'emails from', 'email from',
        'internship email', 'college email', 'interview email',
        'competition email', 'job email', 'offer letter',
    ]
    if any(kw in lower for kw in email_check_kw):
        # Extract topic if mentioned: "check emails about internship" -> query="internship"
        topic_m = re.search(
            r'(?:about|regarding|for|on|related to)\s+([a-z][\w\s]{2,30}?)(?:\s+email|\s*$)',
            lower
        )
        sender_m = re.search(r'from\s+([\w@\.\-]+)', lower)
        if topic_m:
            query = topic_m.group(1).strip()
        elif sender_m:
            query = f"from:{sender_m.group(1).strip()}"
        else:
            query = "is:unread"
        return {"tool_name": "check_emails", "arguments": {"query": query, "max_results": 5}}

    # ── Universal "open X" / "launch X" handler (fallback for anything not caught above) ──
    # Handles: "open google", "open chrome", "open calculator", "open vs code", etc.
    open_m = re.match(
        r'^(?:jarvis\s+)?(?:open|launch|start|run|start up)\s+(.+?)(?:\s+(?:app|application|browser|window|site|website|page))?\s*$',
        lower
    )
    if open_m:
        target = open_m.group(1).strip().strip('.,!?')
        # List of known desktop apps
        _KNOWN_APPS = {
            'notepad', 'calculator', 'calc', 'paint', 'explorer', 'file explorer',
            'task manager', 'cmd', 'command prompt', 'terminal', 'vs code', 'vscode',
            'word', 'excel', 'powerpoint', 'chrome', 'edge', 'firefox',
            'spotify', 'discord', 'zoom', 'settings', 'control panel', 'snipping tool',
        }
        # List of known websites
        _KNOWN_SITES = {
            'google', 'youtube', 'github', 'gmail', 'twitter', 'x', 'instagram',
            'linkedin', 'netflix', 'amazon', 'whatsapp', 'chatgpt', 'gemini',
            'reddit', 'wikipedia', 'hotstar', 'facebook', 'telegram', 'notion',
            'figma', 'canva', 'flipkart', 'swiggy', 'zomato', 'maps', 'stackoverflow',
            'spotify web', 'prime', 'prime video',
        }
        if target in _KNOWN_APPS:
            return {"tool_name": "open_app", "arguments": {"app_name": target}}
        if target in _KNOWN_SITES:
            return {"tool_name": "open_website", "arguments": {"url": target}}
        # If ends with .com/.in/.org etc or contains a dot, treat as website
        if re.search(r'\.(com|in|org|net|io|co|dev|app)$', target) or ('.' in target and ' ' not in target):
            return {"tool_name": "open_website", "arguments": {"url": target}}
        # Otherwise try as app first, then website
        return {"tool_name": "open_app", "arguments": {"app_name": target}}

    # ── Assignment Automation (Phase 1) ───────────────────────────────────────
    # "extract questions from assignment.pdf" / "read my assignment" / "parse pdf"
    assignment_extract_kw = [
        "extract questions", "extract the questions", "get questions from",
        "read assignment", "parse assignment", "read my assignment",
        "questions from pdf", "questions from my pdf", "questions from the pdf",
        "assignment questions", "find questions in",
    ]
    if any(kw in lower for kw in assignment_extract_kw):
        # Try to extract filename from the prompt
        pdf_m = re.search(r'[\w\s\-]+\.pdf', lower)
        pdf_path = pdf_m.group(0).strip() if pdf_m else pdf_m
        # If no filename found, try to grab what comes after "from"
        if not pdf_path:
            from_m = re.search(r'from\s+(?:my\s+)?(?:the\s+)?(.+?)(?:\s*$)', lower)
            pdf_path = from_m.group(1).strip() if from_m else "assignment"
        return {"tool_name": "extract_questions", "arguments": {"pdf_path": pdf_path}}

    # "list my assignments" / "show my pdfs" / "what pdfs do I have"
    list_assign_kw = [
        "list assignments", "list my assignments", "show assignments",
        "list my pdfs", "show my pdfs", "what pdfs", "find my pdf",
        "my assignment files", "assignment pdf",
    ]
    if any(kw in lower for kw in list_assign_kw):
        return {"tool_name": "list_assignments", "arguments": {}}

    # -- Assignment Automation (Phase 2) --------------------------------------
    # -- Assignment Automation (Phase 5 Pipeline) ------------------------------
    do_assign_kw = [
        'do my assignment', 'complete my assignment', 'solve my assignment',
        'answer my assignment', 'finish my assignment'
    ]
    if any(kw in lower for kw in do_assign_kw):
        pdf_m = re.search(r'[\w\-\.]+\.(?:pdf|docx|doc|txt)', lower)
        pdf_path = pdf_m.group(0).strip() if pdf_m else ''
        out_fmt = 'ppt' if 'ppt' in lower or 'powerpoint' in lower else 'word'
        return {
            'tool_name': 'do_assignment',
            'arguments': {'pdf_path': pdf_path, 'output_format': out_fmt, 'humanize': False}
        }

    # -- Assignment Automation (Phase 2 Generate Answers) ----------------------
    gen_answers_kw = [
        'generate answers', 'generate the answers',
        'answer the assignment', 'answer these questions',
    ]
    if any(kw in lower for kw in gen_answers_kw):
        pdf_m = re.search(r'[\w\-\.]+\.(?:pdf|docx|doc|txt)', lower)
        pdf_path = pdf_m.group(0).strip() if pdf_m else ''
        return {
            'tool_name': 'generate_answers',
            'arguments': {'questions_json': prompt, 'pdf_path': pdf_path}
        }

    # 'answer this question: <text>' / 'answer question 3'
    gen_one_kw = [
        'answer this question', 'answer the question',
        'answer question', 'solve this question', 'solve question',
    ]
    if any(kw in lower for kw in gen_one_kw):
        for kw in gen_one_kw:
            if kw in lower:
                idx = lower.index(kw) + len(kw)
                q_text = prompt[idx:].strip().lstrip(':').strip()
                if not q_text:
                    q_text = prompt
                return {
                    'tool_name': 'generate_answer',
                    'arguments': {'question': q_text, 'question_type': 'long_answer'}
                }

    # -- Assignment Automation (Phase 3) --------------------------------------
    # 'humanize answers' / 'humanize my assignment'
    humanize_batch_kw = [
        'humanize answers', 'humanize the answers', 'humanize my assignment',
        'paraphrase answers', 'paraphrase the answers', 'make it human',
        'rewrite answers', 'humanize qa'
    ]
    if any(kw in lower for kw in humanize_batch_kw):
        return {
            'tool_name': 'humanize_all_answers',
            'arguments': {'qa_json': prompt}
        }

    # 'humanize this text: <text>'
    humanize_single_kw = [
        'humanize this text', 'humanize text', 'paraphrase this',
        'paraphrase text', 'humanize this', 'rewrite this to sound human'
    ]
    if any(kw in lower for kw in humanize_single_kw):
        for kw in humanize_single_kw:
            if kw in lower:
                idx = lower.index(kw) + len(kw)
                txt = prompt[idx:].strip().lstrip(':').strip()
                if not txt:
                    txt = prompt
                return {
                    'tool_name': 'humanize_ai_content',
                    'arguments': {'text': txt}
                }

    # -- Assignment Automation (Phase 4) --------------------------------------
    # 'assemble assignment' / 'create assignment doc'
    assemble_kw = [
        'assemble assignment', 'create assignment doc', 'create assignment word',
        'create assignment ppt', 'generate assignment doc', 'save assignment to'
    ]
    if any(kw in lower for kw in assemble_kw):
        return {
            'tool_name': 'assemble_assignment',
            'arguments': {
                'qa_json': prompt, 
                'filename': 'Assignment', 
                'format_type': 'ppt' if 'ppt' in lower or 'powerpoint' in lower else 'word'
            }
        }

    # ── PowerPoint / Presentation Creation ────────────────────────────────────
    ppt_create_kw = [
        'create a presentation', 'make a presentation', 'build a presentation',
        'generate a presentation', 'design a presentation', 'prepare a presentation',
        'create slides', 'make slides', 'build slides',
        'make a ppt', 'create a ppt', 'build a ppt', 'generate a ppt',
        'create a deck', 'make a deck', 'build a deck',
        'create a powerpoint', 'make a powerpoint', 'build a powerpoint',
        'create presentation', 'make presentation', 'ppt on ', 'ppt about ',
        'presentation on ', 'presentation about ', 'slide deck on ',
        'pitch deck', 'make ppt', 'create ppt', 'make slides for', 'ppt for ', 'presentation for ',
    ]
    is_ppt_create = any(kw in lower for kw in ppt_create_kw) or \
        len(re.findall(r'(?im)^\s*(?:#+\s*)?\**\s*slide\s*\d{1,2}\s*\**\s*[:\-–—]', prompt)) >= 3

    # ── PowerPoint follow-up edits (checked before create: "make the ppt dark" ≠ "make a ppt") ──
    _edit_verbs = (r"(change|replace|make|add|remove|delete|move|swap|rename|convert|turn|use|put|shorten|expand|"
                   r"rewrite|fix|update|edit|modify|redo|improve|insert|reduce|increase|switch|set|drop|reorder)")
    _slide_ref = (r"(slides?\s*\d{1,2}|\d{1,2}(st|nd|rd|th)\s+slide|(first|second|third|fourth|fifth|sixth|seventh|"
                  r"eighth|ninth|tenth|last|title|closing|final|cover)\s+slide)")
    _explicit_edit = re.search(rf"\b{_edit_verbs}\b.*\b{_slide_ref}\b|\b{_slide_ref}\b.*\b{_edit_verbs}\b", lower) or \
        re.search(r"\b(add|insert)\s+(a\s+|an\s+|another\s+|one\s+more\s+|new\s+)*(\w+\s+){0,2}slide\b", lower) or \
        any(kw in lower for kw in ['change slide', 'edit slide', 'update slide', 'modify slide',
                                   'redo slide', 'fix slide', 'replace slide'])
    _vague_edit = re.search(rf"\b{_edit_verbs}\b.*\b(the|this|that|my)\s+(ppt|deck|presentation|slides|powerpoint)\b|"
                            rf"\b(the|this|that|my)\s+(ppt|deck|presentation|slides|powerpoint)\b.*\b{_edit_verbs}\b", lower) \
        or re.match(r"^\s*(undo|revert)\b", lower)
    if not is_ppt_create and (_explicit_edit or _vague_edit):
        try:
            from app.services.ppt_studio import has_active_deck
            _deck_ok = has_active_deck(max_age_hours=None if _explicit_edit else 72)
        except Exception:
            _deck_ok = False
        if _deck_ok:
            return {"tool_name": "ppt_edit", "arguments": {"edit_prompt": prompt}}

    if is_ppt_create:
        style_m = re.search(
            r'\b(cyber_dark|midnight_exec|solar_flare|arctic_clean|forest_calm'
            r'|ocean_gradient|velvet_noir|charcoal_minimal)\b',
            lower
        )
        hackathon_kw = ["hackathon", "pitch", "startup", "demo", "prototype", "mvp", "investor", "product launch"]
        purpose = "hackathon" if any(kw in lower for kw in hackathon_kw) else "general"

        # Extract user-uploaded image paths + optional descriptions from [ATTACHED_FILE: ...] tags
        # Frontend format: [ATTACHED_FILE: /path/to/img.jpg | DESCRIPTION: a graph about sales]
        import os as _os
        _img_exts = ('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif')
        attached_img_paths = []
        attached_img_descriptions = []
        template_path = None
        for raw in re.findall(r'\[ATTACHED_FILE:\s*(.+?)\]', prompt, re.IGNORECASE):
            parts = raw.split('|')
            img_path = parts[0].strip()
            if img_path.lower().endswith(('.pptx', '.potx', '.pptm', '.potm')) and _os.path.exists(img_path):
                template_path = template_path or img_path      # user's own format → used as-is
                continue
            if img_path.lower().endswith(_img_exts) and _os.path.exists(img_path):
                attached_img_paths.append(img_path)
                # Extract DESCRIPTION if present
                desc = ""
                for part in parts[1:]:
                    if part.strip().upper().startswith("DESCRIPTION:"):
                        desc = part.split(":", 1)[1].strip()
                        break
                attached_img_descriptions.append(desc)

        return {
            "tool_name": "ppt_create",
            "arguments": {
                "user_prompt": prompt,
                "style": style_m.group(1) if style_m else None,
                "purpose": purpose,
                "image_paths": attached_img_paths if attached_img_paths else None,
                "image_descriptions": attached_img_descriptions if attached_img_descriptions else None,
                "template_path": template_path,
            }
        }

    # ── PowerPoint Styles ──────────────────────────────────────────────────────
    ppt_styles_kw = [
        'list ppt styles', 'what ppt styles', 'available ppt styles',
        'presentation styles', 'ppt personalities', 'show me the styles',
        'what styles can you make', 'ppt design styles',
    ]
    if any(kw in lower for kw in ppt_styles_kw):
        return {"tool_name": "ppt_styles", "arguments": {}}

    # ── Syllabus Auditor ──────────────────────────────────────────────────────
    # Triggers on: "audit my playlist", "check playlist coverage",
    #              "does this playlist cover my syllabus", "gap analysis", etc.
    audit_kw = [
        'audit my playlist', 'audit playlist', 'audit this playlist',
        'check playlist coverage', 'does this playlist cover',
        'does the playlist cover', 'analyze my playlist', 'analyse my playlist',
        'playlist vs syllabus', 'syllabus coverage', 'audit syllabus',
        'what topics are missing', 'missing topics in playlist',
        'playlist audit', 'coverage report', 'check if playlist covers',
        'gap analysis', 'audit the playlist', 'check my playlist',
    ]
    if any(kw in lower for kw in audit_kw):
        import os
        # Extract YouTube playlist URL
        url_m = re.search(r'https?://[^\s\]]+', prompt)
        playlist_url = url_m.group(0) if url_m else ''

        # Primary: image path from [ATTACHED_FILE: path] tag (drag-and-drop / frontend upload)
        attached_imgs = re.findall(
            r'\[ATTACHED_FILE:\s*(.+?\.(?:jpg|jpeg|png|webp|bmp))\s*\]',
            prompt, re.IGNORECASE
        )
        image_path = attached_imgs[0].strip() if attached_imgs else ''

        # Fallback: filename mentioned in text -> fuzzy search common folders
        if not image_path:
            img_name_m = re.search(
                r'([\w\s\-]+\.(?:jpg|jpeg|png|webp|bmp))',
                prompt, re.IGNORECASE
            )
            if img_name_m:
                img_filename = img_name_m.group(1).strip()
                search_dirs = [
                    os.path.join(os.path.expanduser('~'), 'Desktop'),
                    os.path.join(os.path.expanduser('~'), 'Pictures'),
                    os.path.join(os.path.expanduser('~'), 'Downloads'),
                    os.path.join(os.path.expanduser('~'), 'Documents'),
                ]
                for folder in search_dirs:
                    candidate = os.path.join(folder, img_filename)
                    if os.path.exists(candidate):
                        image_path = candidate
                        break

        if not playlist_url:
            return {
                'tool_name': 'audit_playlist_syllabus',
                'arguments': {
                    'playlist_url': '',
                    'image_path': image_path,
                }
            }

        return {
            'tool_name': 'audit_playlist_syllabus',
            'arguments': {
                'playlist_url': playlist_url,
                'image_path': image_path,
            }
        }
    # ── Social Media & Content (Interactive) ──────────────────────────────────
    social_kw = [
        'write a caption', 'give me caption', 'give me a caption', 'caption for', 'linkedin post',
        'tweet about', 'instagram post', 'social media idea', 'social media post', 'post for linkedin'
    ]
    
    # Check if user is replying to the clarification question
    is_replying_to_clarification = False
    original_idea = prompt
    if len(conversation_history) >= 2:
        last_bot_msg = conversation_history[-1].get("content", "")
        if "Would you like auto hashtags? Emojis? Should the tone be formal or informal?" in last_bot_msg:
            is_replying_to_clarification = True
            original_idea = conversation_history[-2].get("content", "")
            
    if any(kw in lower for kw in social_kw) or is_replying_to_clarification:
        has_params = any(word in lower for word in ['emoji', 'hashtag', 'formal', 'informal', 'creative'])
        if not has_params and not is_replying_to_clarification:
            return {"tool_name": "ask_for_clarification", "arguments": {"question": "Would you like auto hashtags? Emojis? Should the tone be formal or informal?"}}
        
        # Determine parameters
        combined_text = (original_idea + " " + prompt).lower()
        platform = "LinkedIn"
        if "instagram" in combined_text: platform = "Instagram"
        elif "tweet" in combined_text or " x " in combined_text: platform = "X"
        
        tone = "formal" if "formal" in combined_text and "informal" not in combined_text else ("informal" if "informal" in combined_text else "engaging")
        emojis = "no emoji" not in combined_text and "without emoji" not in combined_text
        hashtags = "no hashtag" not in combined_text and "without hashtag" not in combined_text
        
        return {"tool_name": "generate_social_content", "arguments": {
            "idea": original_idea if is_replying_to_clarification else prompt,
            "platform": platform,
            "tone": tone,
            "smart_emojis": emojis,
            "auto_hashtag": hashtags,
            "creativity": 50.0
        }}

    return None  # Fall through to LLM router


# Global state for frontend API flows (mimics voice_agent local state)
api_whatsapp_flow = {"active": False, "step": None, "contact": None, "message": None}
api_whatsapp_call_flow = {"active": False, "step": None, "contact": None}
api_note_flow = {"active": False}

# Media tools: blocking UI automation (run in a worker thread so the event loop stays
# free) whose result string is already the final reply (no LLM paraphrase).
_DIRECT_MEDIA_TOOLS = {
    "play_music", "spotify_control", "media_control", "youtube_search", "youtube_open", "youtube_channel",
    "youtube_list_results",
    "youtube_play_result", "youtube_control", "play_video_in_browser",
}

# One dedicated thread for all media automation: UI Automation / COM objects stay on one
# thread, and two commands can never type into the browser or Spotify at the same time.
from concurrent.futures import ThreadPoolExecutor as _TPE
import functools as _ft
_MEDIA_EXECUTOR = _TPE(max_workers=1, thread_name_prefix="jarvis-media")


async def _run_media(name: str, args: dict):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(_MEDIA_EXECUTOR, _ft.partial(TOOL_REGISTRY[name], **args))


async def _run_direct_tool(tool_intent: dict, prompt: str):
    name, args = tool_intent["tool_name"], tool_intent.get("arguments", {}) or {}
    try:
        result = str(await _run_media(name, args))
    except Exception as e:
        result = f"Sorry Sir, that didn't work: {e}"
    conversation_history.append({"role": "user", "content": prompt})
    conversation_history.append({"role": "assistant", "content": result})
    _save_session()
    async def direct_stream(): yield result
    return StreamingResponse(direct_stream(), media_type="text/event-stream")

_MEDIA_TOOLS_ALL = _DIRECT_MEDIA_TOOLS | {"media_play_pause", "media_next", "media_previous"}
_CLAUSE_SPLIT = re.compile(r"\s*,?\s*\b(?:and\s+then|and\s+after\s+that|after\s+that|and\s+also|and|then)\b\s*,?\s*", re.I)


def _media_intent_for(clause: str):
    """Media tool intent for one clause (YouTube-mode parser first, then keyword router)."""
    it = None
    try:
        from app.services.youtube_control import youtube_session_active, parse_youtube_followup, youtube_tab_open
        if youtube_session_active():
            it = parse_youtube_followup(clause)
        elif youtube_tab_open():
            it = parse_youtube_followup(clause, controls_only=True)
        if it and it.pop("bare", False):
            it = None
    except Exception:
        it = None
    if not it:
        it = keyword_detect_tool(clause)
    return it if isinstance(it, dict) and it.get("tool_name") in _MEDIA_TOOLS_ALL else None


def _explicit_platform(text: str):
    """'youtube' / 'spotify' if the text names one platform (song/music are neutral)."""
    t = (text or "").lower()
    yt = re.search(r"\b(?:youtube|yt|video|videos|watch|channel)\b", t)
    sp = re.search(r"\bspotify\b", t)
    if yt and not sp:
        return "youtube"
    if sp and not yt:
        return "spotify"
    return None


def _to_platform(it: dict, plat: str) -> dict:
    """Re-target an unspecific media intent (pause/next/play X) to the given platform."""
    name, args = it["tool_name"], dict(it.get("arguments") or {})
    act = args.get("action")
    if plat == "youtube":
        if name == "spotify_control" and act in ("pause", "play", "next", "previous"):
            return {"tool_name": "youtube_control", "arguments": {"action": act}}
        if name == "media_control" and act in ("pause", "play"):
            return {"tool_name": "media_control", "arguments": {"action": act, "app": "youtube"}}
        if name == "media_control" and act in ("next", "previous"):
            return {"tool_name": "youtube_control", "arguments": {"action": act}}
        if name == "play_music":
            return {"tool_name": "youtube_search", "arguments": {"query": args.get("song", ""), "autoplay": True}}
        if name == "media_play_pause":
            return {"tool_name": "youtube_control", "arguments": {"action": "pause"}}
    elif plat == "spotify":
        if name == "youtube_control" and act in ("pause", "play", "next", "previous"):
            return {"tool_name": "spotify_control", "arguments": {"action": act}}
        if name == "media_control" and act in ("pause", "play", "next", "previous"):
            return {"tool_name": "media_control", "arguments": {"action": act, "app": "spotify"}}
        if name == "youtube_search" and args.get("autoplay"):
            return {"tool_name": "play_music", "arguments": {"song": args.get("query", "")}}
        if name == "media_play_pause":
            return {"tool_name": "spotify_control", "arguments": {"action": "pause"}}
    return it


def _media_compound(prompt: str):
    """
    "close this song and play shape of you", "pause the video then open mrbeast's channel":
    split into clauses and return their media intents, only if EVERY clause is a media
    command (so "play rock and roll" or "email X and play Y" are left alone).
    """
    text = re.sub(r'\[attached_file:.*?\]', '', prompt, flags=re.I).strip().strip(' .!?')
    text = re.sub(r'^(?:(?:hey|ok|okay)\s+)?jarvis[\s,.!:-]+', '', text, flags=re.I)
    parts = [p.strip(' ,.') for p in _CLAUSE_SPLIT.split(text) if p and p.strip(' ,.')]
    if not 2 <= len(parts) <= 4:
        return None
    intents = []
    hint = _explicit_platform(text)  # a platform named anywhere applies to the unspecific parts
    ctx = None                       # platform set by an earlier clause ("open youtube and play X")
    for part in parts:
        it = _media_intent_for(part)
        if not it:
            return None
        pl = part.lower()
        own = _explicit_platform(pl)
        plat = own or ctx or hint
        if plat and not own:
            it = _to_platform(it, plat)
        name, args = it["tool_name"], it.get("arguments") or {}
        if args.get("action") == "close":
            # closing YouTube itself → what follows is for Spotify, and vice versa;
            # closing "this video" keeps us on YouTube
            if name == "youtube_control" and re.search(r"\b(?:youtube|yt)\b", pl):
                ctx = "spotify"
            elif name == "spotify_control":
                ctx = "youtube"
            else:
                ctx = "youtube"
        elif name.startswith("youtube") or name == "play_video_in_browser":
            ctx = "youtube"
        elif name in ("play_music", "spotify_control"):
            ctx = "spotify"
        elif name == "media_control" and args.get("app") in ("spotify", "youtube"):
            ctx = args["app"]
        intents.append(it)
    # "open youtube and play X" / "open spotify and play X": the later step opens it anyway
    def _is_open(it):
        return it["tool_name"] == "youtube_open" or (
            it["tool_name"] == "spotify_control" and (it.get("arguments") or {}).get("action") == "open")
    def _plat(it):
        n = it["tool_name"]
        return "youtube" if n.startswith("youtube") else ("spotify" if n in ("play_music", "spotify_control") else None)
    intents = [it for i, it in enumerate(intents)
               if not (_is_open(it) and any(_plat(n) == _plat(it) and not _is_open(n) for n in intents[i + 1:]))]
    if not intents:
        return None
    # "close this video and play X": keep the tab (pause) so X plays in it
    for i, it in enumerate(intents[:-1]):
        if it["tool_name"] == "youtube_control" and (it.get("arguments") or {}).get("action") == "close" \
                and any(n["tool_name"].startswith("youtube") for n in intents[i + 1:]):
            it["arguments"] = {"action": "pause"}
    return intents


async def _run_direct_tools(intents: list, prompt: str):
    """Run several media intents in order; one short combined reply."""
    replies = []
    for it in intents:
        try:
            replies.append(str(await _run_media(it["tool_name"], it.get("arguments") or {})))
        except Exception as e:
            replies.append(f"Sorry Sir, that didn't work: {e}")
    # Keep it short for voice: drop pure acknowledgements when a later step said more
    keep = [r for r in replies[:-1] if not re.match(r"^(?:Paused|Resumed|Done|It's already paused|Closed)\b", r)] + replies[-1:]
    result = " ".join(keep)
    conversation_history.append({"role": "user", "content": prompt})
    conversation_history.append({"role": "assistant", "content": result})
    _save_session()
    async def direct_stream(): yield result
    return StreamingResponse(direct_stream(), media_type="text/event-stream")


@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    global api_whatsapp_flow, api_whatsapp_call_flow, api_note_flow
    from fastapi.responses import StreamingResponse

    # ── Handle Attached Files ─────────────────────────────────────────────
    attached_files = re.findall(r'\[ATTACHED_FILE:\s*(.+?)\]', request.prompt)
    if attached_files:
        from app.services.file_ops import read_file
        file_contents = []
        for fpath in attached_files:
            # Only read contents if it's a text-based file
            if re.search(r'\.(pdf|txt|docx|doc|csv|json|md|py|js|html|css|jsx)$', fpath, re.IGNORECASE):
                try:
                    file_contents.append(f"Content of {fpath}:\n" + read_file(fpath))
                except Exception:
                    pass
        
        # We no longer strip the ATTACHED_FILE tags from the prompt so media tools can use the paths
        if file_contents:
            request.prompt += "\n\nAttached Context:\n" + "\n".join(file_contents)

    history_list = list(conversation_history)
    prompt_lower = request.prompt.lower().strip()

    # ── Frontend Note Flow Intercept ──
    if api_note_flow["active"]:
        api_note_flow["active"] = False
        from app.services.tools import create_sticky_note
        res = create_sticky_note(request.prompt.strip())
        async def flow_stream(): yield res
        return StreamingResponse(flow_stream(), media_type="text/event-stream")

    # ── Frontend WhatsApp CALL Flow Intercept ──
    if api_whatsapp_call_flow["active"]:
        step = api_whatsapp_call_flow["step"]
        if step == "confirm":
            yes_kw = ['yes', 'yeah', 'yep', 'go ahead', 'do it', 'ok', 'okay', 'confirm', 'haan', 'kar do', 'correct', 'sure', 'call']
            no_kw  = ['no', 'nope', 'cancel', 'stop', 'abort', 'nahi', 'mat karo', 'nevermind', 'never mind', "don't", "dont", 'not', 'wait']
            is_no  = any(w in prompt_lower for w in no_kw)
            is_yes = (not is_no) and any(w in prompt_lower for w in yes_kw)

            if is_yes:
                from app.services.whatsapp_call import confirm_whatsapp_call
                contact = api_whatsapp_call_flow["contact"]
                api_whatsapp_call_flow = {"active": False, "step": None, "contact": None}
                async def flow_stream(): yield confirm_whatsapp_call(contact)
                return StreamingResponse(flow_stream(), media_type="text/event-stream")
            elif is_no:
                api_whatsapp_call_flow = {"active": False, "step": None, "contact": None}
                async def flow_stream(): yield "Okay, call cancelled."
                return StreamingResponse(flow_stream(), media_type="text/event-stream")
            else:
                async def flow_stream(): yield "Should I go ahead and call? Please say yes or no."
                return StreamingResponse(flow_stream(), media_type="text/event-stream")

    # ── Frontend WhatsApp MESSAGE Flow Intercept ──
    if api_whatsapp_flow["active"]:
        step = api_whatsapp_flow["step"]
        if step == "ask_message":
            api_whatsapp_flow["message"] = request.prompt.strip()
            api_whatsapp_flow["step"] = "confirm"
            reply = f"Got it. Before I send, confirming: To {api_whatsapp_flow['contact']} — {api_whatsapp_flow['message']}. Should I go ahead and send this?"
            async def flow_stream(): yield reply
            return StreamingResponse(flow_stream(), media_type="text/event-stream")
            
        elif step == "confirm":
            yes_kw = ['yes', 'yeah', 'yep', 'go ahead', 'do it', 'ok', 'okay', 'confirm', 'haan', 'kar do', 'correct', 'sure']
            no_kw  = ['no', 'nope', 'cancel', 'stop', 'abort', 'nahi', 'mat bhejo', 'nevermind', 'never mind', "don't", "dont", 'not', 'wait']
            is_no  = any(w in prompt_lower for w in no_kw)
            is_yes = (not is_no) and any(w in prompt_lower for w in yes_kw)

            if is_yes:
                from app.services.whatsapp_smart import confirm_whatsapp_send
                contact = api_whatsapp_flow["contact"]
                msg = api_whatsapp_flow["message"]
                api_whatsapp_flow = {"active": False, "step": None, "contact": None, "message": None}
                async def flow_stream(): yield confirm_whatsapp_send(contact, msg)
                return StreamingResponse(flow_stream(), media_type="text/event-stream")
            elif is_no:
                api_whatsapp_flow = {"active": False, "step": None, "contact": None, "message": None}
                async def flow_stream(): yield "Okay, message cancelled."
                return StreamingResponse(flow_stream(), media_type="text/event-stream")
            else:
                async def flow_stream(): yield "Should I send it? Please say yes or no."
                return StreamingResponse(flow_stream(), media_type="text/event-stream")
                
        elif step == "ask_contact":
            api_whatsapp_flow["contact"] = request.prompt.strip()
            stored_msg = api_whatsapp_flow.get("message")
            if stored_msg:
                api_whatsapp_flow["step"] = "confirm"
                reply = f"Okay. To {api_whatsapp_flow['contact']}: {stored_msg}. Should I send?"
            else:
                api_whatsapp_flow["step"] = "ask_message"
                reply = f"Got it. What message should I send to {api_whatsapp_flow['contact']}?"
            async def flow_stream(): yield reply
            return StreamingResponse(flow_stream(), media_type="text/event-stream")

    # ── Resume creator: "make my resume like this" (+ image), edits, or details after "send me your details" ──
    # Runs before media/DAG/complex-task checks: pasted resume details are long multi-clause text.
    try:
        from app.services.resume_builder import detect_resume_request, create_resume, list_resume_templates, open_resume_editor
        _resume_args = detect_resume_request(request.prompt)
        if _resume_args is not None:
            from starlette.concurrency import iterate_in_threadpool
            if _resume_args.pop("_list", False):
                _gen = iter([list_resume_templates()])
            elif _resume_args.pop("_editor", False):
                _gen = iter([open_resume_editor()])
            else:
                _gen = create_resume(**_resume_args)
            async def resume_stream():
                _last = ""
                async for _chunk in iterate_in_threadpool(_gen):
                    _last = _chunk
                    yield _chunk
                conversation_history.append({"role": "user", "content": _resume_args.get("details") or _resume_args.get("instruction") or request.prompt[:400]})
                conversation_history.append({"role": "assistant", "content": _last[:1500]})
                _save_session()
            return StreamingResponse(resume_stream(), media_type="text/event-stream")
    except Exception as e:
        print(f"[Jarvis] resume check failed: {e}")

    # ── Multi-step media commands: "close this song and play X", "pause it then next video" ──
    try:
        _compound = _media_compound(request.prompt)
        if _compound:
            return await _run_direct_tools(_compound, request.prompt)
    except Exception as e:
        print(f"[Jarvis] media compound check failed: {e}")

    # ── YouTube mode: follow-ups after "open youtube" / a YouTube search ──
    # ("lofi beats", "play the second one", "pause", "skip 30 seconds", "close youtube")
    try:
        from app.services.youtube_control import youtube_session_active, parse_youtube_followup, youtube_tab_open
        _yt_intent = None
        if youtube_session_active():
            _yt_intent = parse_youtube_followup(request.prompt)
        elif youtube_tab_open():
            # Mode expired, but a YouTube tab is in front: only unambiguous player commands
            _yt_intent = parse_youtube_followup(request.prompt, controls_only=True)
        if _yt_intent:
            # Plain-text search only if no other tool claims the message (weather, time…)
            if _yt_intent.pop("bare", False) and keyword_detect_tool(request.prompt):
                _yt_intent = None
            if _yt_intent:
                return await _run_direct_tool(_yt_intent, request.prompt)
    except Exception as e:
        print(f"[Jarvis] YouTube mode check failed: {e}")

    # ── Universal Note / WhatsApp Intent Check (moved from voice_agent) ──
    if detect_note_intent(request.prompt):
        api_note_flow["active"] = True
        async def flow_stream(): yield "What should I write in the note?"
        return StreamingResponse(flow_stream(), media_type="text/event-stream")

    # ── Check for WhatsApp CALL intent FIRST (before send check) ──
    wa_call_contact = detect_whatsapp_call(request.prompt)
    if wa_call_contact:
        api_whatsapp_call_flow.update({"active": True, "step": "confirm", "contact": wa_call_contact})
        reply = f"Shall I go ahead and make a WhatsApp call to {wa_call_contact}?"
        async def flow_stream(): yield reply
        return StreamingResponse(flow_stream(), media_type="text/event-stream")

    wa_contact = detect_whatsapp_send(request.prompt)
    if wa_contact:
        msg_inline = re.search(
            r'(?:saying|say(?:ing)?|that\s+says)[:\s]+["\']?(.+?)["\']?\s*$',
            request.prompt, re.I
        )
        if msg_inline:
            inline_msg = msg_inline.group(1).strip()
            api_whatsapp_flow.update({"active": True, "step": "confirm", "contact": wa_contact, "message": inline_msg})
            reply = f"Before I send, confirming: To {wa_contact} — {inline_msg}. Should I go ahead and send this?"
        else:
            api_whatsapp_flow.update({"active": True, "step": "ask_message", "contact": wa_contact, "message": None})
            reply = f"Sure. What message should I send to {wa_contact}?"
        async def flow_stream(): yield reply
        return StreamingResponse(flow_stream(), media_type="text/event-stream")

    # ── Media fast path: player commands skip task-resume / DAG / LLM ─────────
    # ("resume the music" was being caught by the task-resume detector below)
    _media_intent = keyword_detect_tool(request.prompt)
    if isinstance(_media_intent, dict) and _media_intent.get("tool_name") in (
            _DIRECT_MEDIA_TOOLS | {"media_play_pause", "media_next", "media_previous"}):
        return await _run_direct_tool(_media_intent, request.prompt)

    # ── Task Resumption: detect 'continue/extend/update prior task' intent ──────
    # Runs BEFORE keyword detection and DAG planner so that continuation requests
    # are correctly routed to the original task's tool with prior context injected.
    # Fully fail-safe: all errors are caught, normal flow continues unaffected.
    try:
        from app.services.task_ledger import get_recent_tasks_raw
        from app.services.resume_detector import detect_resume_intent, get_resume_context_string
        _recent_tasks = get_recent_tasks_raw(n=10)
        _resume_info = detect_resume_intent(request.prompt, _recent_tasks)
        if _resume_info and _resume_info.get("is_resume"):
            _resume_ctx = get_resume_context_string(_resume_info)
            if _resume_ctx:
                # Prepend the original task context to the user's prompt.
                # The LLM and planner now know WHICH file/resource to operate on.
                request.prompt = _resume_ctx + "\n\n[USER INSTRUCTION]: " + request.prompt
    except Exception:
        pass  # Best-effort — never block normal chat flow

    # ── PATH A-DAG: Multi-branch DAG planner ──────────────────────────────────
    # Runs BEFORE keyword_detect_tool so multi-intent requests (e.g. "email prof
    # AND remind me Friday AND check calendar") get decomposed into a parallel
    # execution graph instead of being routed to a single tool.
    # Safe: is_dag_task() explicitly excludes assignment, PPT, and single-tool commands.
    try:
        from app.services.dag_executor import is_dag_task, run_dag_plan
        if is_dag_task(request.prompt):
            async def _dag_stream_with_history():
                full_narration_parts = []
                async for event_str in run_dag_plan(request.prompt):
                    # Collect text content for conversation history
                    try:
                        import json as _json
                        evt = _json.loads(event_str.replace("data: ", "").strip())
                        text = evt.get("text") or evt.get("result") or ""
                        if text:
                            full_narration_parts.append(text)
                    except Exception:
                        pass
                    yield event_str

                # Save to conversation history so memory + RAG work correctly
                conversation_history.append({"role": "user", "content": request.prompt})
                full_narration = " ".join(full_narration_parts)
                conversation_history.append({"role": "assistant", "content": full_narration or "(dag plan executed)"})
                _save_session()
                # Store to long-term RAG memory (best-effort)
                try:
                    from app.services.rag_memory import store_turn
                    await store_turn(role="user", content=request.prompt, turn_index=len(conversation_history))
                    if full_narration:
                        await store_turn(role="assistant", content=full_narration, turn_index=len(conversation_history))
                except Exception:
                    pass

            return StreamingResponse(_dag_stream_with_history(), media_type="text/event-stream")
    except Exception as _dag_err:
        import logging as _log
        _log.getLogger(__name__).warning(f"[DAG] Guard failed, falling through: {_dag_err}")
        # Fall through to PATH B safely

    # ── PATH B: Fast single-action path (keyword → tool → LLM response) ──

    # 1. Fast keyword detection (reliable, instant)
    tool_intent = keyword_detect_tool(request.prompt)
    
    from fastapi.responses import StreamingResponse
    if isinstance(tool_intent, StreamingResponse):
        return tool_intent

    # 2. Fall back to LLM router if keyword detection found nothing
    if tool_intent is None:
        tool_intent = await check_for_tool_intent(request.prompt, history_list)

    tool_name = tool_intent.get("tool_name") if tool_intent else None

    # 3. Handle clarification requests
    if tool_name == "ask_for_clarification":
        question = tool_intent["arguments"].get("question", "Could you clarify that?")
        if "What should I write in the note" in question:
            api_note_flow["active"] = True
            
        conversation_history.append({"role": "user", "content": request.prompt})
        conversation_history.append({"role": "assistant", "content": question})
        _save_session()

        async def clarification_stream():
            for char in question:
                yield char

        return StreamingResponse(clarification_stream(), media_type="text/event-stream")

    # 3b. Complex multi-step task with no single tool → linear agentic planner.
    # keyword_detect_tool() bails out on is_complex_task() prompts and the router
    # prompt tells the LLM to return null for them, so this is where they land.
    if tool_name is None and is_complex_task(request.prompt):
        async def planner_stream():
            updates = []
            try:
                async for update in run_agentic_plan(request.prompt):
                    updates.append(update)
                    yield update + "\n\n"
            except Exception as e:
                msg = f"The planner hit an error: {e}"
                updates.append(msg)
                yield msg
            conversation_history.append({"role": "user", "content": request.prompt})
            conversation_history.append({"role": "assistant", "content": "\n".join(updates)})
            _save_session()
            try:
                from app.services.rag_memory import store_turn
                await store_turn(role="user", content=request.prompt, turn_index=len(conversation_history))
                await store_turn(role="assistant", content="\n".join(updates), turn_index=len(conversation_history))
            except Exception:
                pass

        return StreamingResponse(planner_stream(), media_type="text/event-stream")

    # 4. Execute tool
    tool_output_str = ""

    # ── Special async handling for recall_memory (FAISS search is async) ──────
    if tool_name == "recall_memory":
        try:
            from app.services.rag_memory import recall, format_recall_for_prompt
            query = tool_intent.get("arguments", {}).get("query", request.prompt)
            # High-recall mode: more results, lower threshold for explicit memory queries
            recalled = await recall(query, top_k=10, min_score=0.20)
            if recalled:
                formatted = format_recall_for_prompt(recalled, query=query)
                tool_output_str = f"[MEMORY RECALL RESULTS — {len(recalled)} matches found]\n{formatted}\n\n"
            else:
                tool_output_str = "[MEMORY RECALL] No relevant memories found for this query.\n\n"
        except Exception as e:
            tool_output_str = f"[MEMORY RECALL] Could not access memory: {e}\n\n"

    elif tool_name == "open_website" and re.sub(r'^(?:https?://)?(?:www\.)?', '', str(
            (tool_intent.get("arguments") or {}).get("url", "")).lower()).rstrip('/') in ("youtube", "youtube.com", "yt"):
        return await _run_direct_tool({"tool_name": "youtube_open", "arguments": {}}, request.prompt)

    elif tool_name in _DIRECT_MEDIA_TOOLS and tool_name in TOOL_REGISTRY:
        return await _run_direct_tool(tool_intent, request.prompt)

    elif tool_name and tool_name in TOOL_REGISTRY:
        args = tool_intent.get("arguments", {})
        try:
            result = TOOL_REGISTRY[tool_name](**args)
            import inspect
            if inspect.isgenerator(result):
                async def tool_stream():
                    full_log = []
                    for chunk in result:
                        full_log.append(chunk)
                        yield chunk + "\n\n"
                    
                    conversation_history.append({"role": "user", "content": request.prompt})
                    conversation_history.append({"role": "assistant", "content": "\n".join(full_log)})
                    _save_session()
                    
                return StreamingResponse(tool_stream(), media_type="text/event-stream")
                
            tool_output_str = f"[Tool result: {result}]\n\n"

            # ── Task Ledger: log this completed tool execution ────────────────
            # Records what Jarvis just did so it can be resumed/extended later.
            # Completely fail-safe — never interrupts the chat flow.
            try:
                from app.services.task_ledger import log_task
                _ledger_context = {
                    "args": {k: str(v)[:200] for k, v in args.items()},
                    "result_preview": str(result)[:300],
                }
                # Enrich context with common resource fields for easy lookup later
                for _field in ("path", "file_path", "filename", "contact_name", "url", "pdf_path"):
                    if _field in args:
                        _ledger_context[_field] = str(args[_field])[:300]
                log_task(
                    task_type=tool_name,
                    description=request.prompt[:400],
                    context=_ledger_context,
                    status="completed",
                    related_tool=tool_name,
                )
            except Exception:
                pass  # Best-effort — never break chat flow
            # ─────────────────────────────────────────────────────────────────

            if tool_name in ("enhance_media", "generate_social_content"):
                async def flow_stream(): yield result
                return StreamingResponse(flow_stream(), media_type="text/event-stream")

            # Check for state machine triggers to activate flow for frontend
            if tool_name == "initiate_whatsapp_send":
                if "What message should I send" in result:
                    api_whatsapp_flow.update({"active": True, "step": "ask_message", "contact": args.get("contact_name"), "message": None})
                elif "Before I send, let me confirm" in result:
                    api_whatsapp_flow.update({"active": True, "step": "confirm", "contact": args.get("contact_name"), "message": args.get("message")})
                # Return immediately without LLM paraphrasing
                async def flow_stream(): yield result
                return StreamingResponse(flow_stream(), media_type="text/event-stream")

            elif tool_name == "initiate_whatsapp_call":
                # Activate the call flow so the next 'yes' triggers confirm_whatsapp_call
                contact = args.get("contact_name", "")
                api_whatsapp_call_flow.update({"active": True, "step": "confirm", "contact": contact})
                reply = f"Shall I go ahead and make a WhatsApp call to {contact}?"
                async def flow_stream(): yield reply
                return StreamingResponse(flow_stream(), media_type="text/event-stream")

            
            elif tool_name == "search_whatsapp_contact" and "__ASK_CONTACT__" in str(result):
                api_whatsapp_flow.update({"active": True, "step": "ask_contact", "contact": None, "message": None})
                result_clean = str(result).replace("__ASK_CONTACT__", "").strip()
                async def flow_stream(): yield result_clean
                return StreamingResponse(flow_stream(), media_type="text/event-stream")
                
        except Exception as e:
            tool_output_str = f"[Tool failed: {tool_name} — {str(e)}]\n\n"

    # 4c. No tool matched at all → try dynamic skill generation
    # Only trigger if both fast keyword router AND LLM router both returned no tool,
    # AND the request looks like a genuine PC automation task (not a question).
    if not tool_output_str and tool_name is None:
        lower_p = request.prompt.lower()
        is_question = lower_p.strip().startswith(('what', 'who', 'when', 'where', 'why',
                                                   'how much', 'how many', 'tell me', 'explain',
                                                   'can you', 'could you', 'define', 'describe'))
        # Must have clear PC automation intent to avoid spurious dynamic skill calls
        automation_triggers = [
            'rename', 'compress', 'resize', 'batch', 'automate', 'drag',
            'zoom in', 'capture screen', 'record screen', 'empty the trash',
            'sort the files', 'clean the desktop', 'organize my files',
        ]
        is_automation = any(w in lower_p for w in automation_triggers)
        if is_automation and not is_question:
            try:
                prefs = format_preferences_for_prompt()
                full_ctx = prefs if prefs else ""
                skill_result = await run_dynamic_skill(request.prompt, ui_context=full_ctx)
                tool_output_str = f"[Dynamic skill result: {skill_result}]\n\n"
            except Exception as e:
                tool_output_str = f"[Dynamic skill error: {e}]\n\n"

    # 5. Smart RAG + Context (skip expensive steps when tool already handled it)
    rag_context = ""
    current_screen = ""

    # Only run RAG if this is a question/knowledge query (not a tool action)
    prompt_lower = request.prompt.lower()
    is_knowledge_query = any(prompt_lower.startswith(w) for w in [
        "what", "who", "when", "where", "why", "how", "tell me", "explain",
        "can you", "could you", "describe", "define",
    ])
    if is_knowledge_query and not tool_output_str:
        try:
            embedding = await get_embedding(request.prompt)
            matches = await search_similar_chunks(embedding, limit=2)
            rag_context = "\n\n".join(matches) if matches else ""
        except Exception:
            rag_context = ""

    # Only call screen inspector if no tool result (avoids double-call).
    # It is a screenshot + vision call + OCR: measured 44 s when the vision model is
    # rate-limited, and it used to run synchronously, freezing every other request.
    # Voice requests skip it (spoken questions rarely need the screen; "what's on my
    # screen" still goes through the read_my_screen tool). Otherwise: off the event
    # loop, capped at 3 s.
    if not tool_output_str and not request.voice:
        try:
            current_screen = await asyncio.wait_for(asyncio.to_thread(describe_screen_for_llm), timeout=3.0)
        except Exception:
            try:
                current_screen = await asyncio.wait_for(asyncio.to_thread(get_screen_text_summary), timeout=1.5)
            except Exception:
                current_screen = ""

    context_parts = []
    if tool_output_str:
        context_parts.append(tool_output_str)
    if rag_context:
        context_parts.append(rag_context)
    if current_screen:
        context_parts.append(f"[Active Screen: {current_screen}]")

    # ── Task Ledger: inject recent task history so LLM is context-aware ──────
    # Gives the LLM natural awareness of what Jarvis recently did.
    # Enables replies like "I've added that section to quantum_computing.docx"
    # instead of "I have created a new file...".
    try:
        from app.services.task_ledger import get_task_ledger_for_prompt
        _ledger_prompt_ctx = get_task_ledger_for_prompt()
        if _ledger_prompt_ctx:
            context_parts.append(_ledger_prompt_ctx)
    except Exception:
        pass  # Best-effort — never break chat flow

    context = "\n\n".join(context_parts)

    # 7. Save user turn to history + long-term RAG memory
    conversation_history.append({"role": "user", "content": request.prompt})
    _save_session()
    # Store user turn to long-term memory (background, non-blocking)
    try:
        from app.services.rag_memory import store_turn
        _bg_task = asyncio.ensure_future(store_turn(
            role="user",
            content=request.prompt,
            turn_index=len(conversation_history),
        ))
        # Hold a reference so the task isn't garbage-collected before it completes
        _bg_task.add_done_callback(lambda t: t.exception() if not t.cancelled() else None)
    except Exception:
        pass

    # 8. Stream LLM response — pass context as tool_result
    async def response_stream_with_history():
        full_response = ""
        async for chunk in generate_chat_response(
            user_message=request.prompt,
            tool_name="context" if context else None,
            tool_result=context if context else None,
            language=request.lang,
            voice=request.voice,
        ):
            full_response += chunk
            yield chunk
        conversation_history.append({"role": "assistant", "content": full_response})
        _save_session()
        # Store assistant turn to long-term memory (best-effort)
        try:
            from app.services.rag_memory import store_turn
            await store_turn(
                role="assistant",
                content=full_response,
                turn_index=len(conversation_history),
            )
        except Exception:
            pass

    return StreamingResponse(
        response_stream_with_history(),
        media_type="text/event-stream"
    )


@router.delete("/chat/history")
async def clear_history():
    """Clears the conversation history (start fresh)."""
    conversation_history.clear()
    return {"status": "Conversation history cleared."}
