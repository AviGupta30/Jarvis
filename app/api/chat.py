from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import re
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


def keyword_detect_tool(prompt: str) -> dict | None:
    """
    Fast, 100% reliable keyword-based tool detection.
    Runs BEFORE the LLM router to catch common patterns the small router model misses.
    Returns a tool_intent dict or None.
    """
    lower = prompt.lower().strip()
    
    # If the command is complex (multiple actions), let planner handle it.
    if is_complex_task(prompt):
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

    # ── Play on Spotify explicitly ──────────────────────
    spotify_play_m = re.search(
        r'(?:open\s+spotify\s+and\s+)?play(?:\s+(?:me\s+)?(?:the\s+)?(?:song|music|track|album|artist))?\s+(.+?)(?:\s+on\s+spotify)\s*$',
        lower
    )
    if spotify_play_m and not is_question:
        song = spotify_play_m.group(1).strip(' ,.')
        return {"tool_name": "play_music", "arguments": {"song": song}}

    # ── Play on YouTube explicitly: "play X on youtube" → autoplay first result
    yt_play_m = re.match(
        r'^(?:jarvis\s+)?play(?:\s+(?:me\s+)?(?:the\s+)?(?:song|music|track|video))?\s+(.+?)\s+on\s+(?:youtube|yt)\s*$',
        lower
    )
    if yt_play_m and not is_question:
        song = _clean_yt_query(yt_play_m.group(1).strip(' ,.'))
        return {"tool_name": "youtube_search", "arguments": {"query": song, "autoplay": True}}

    # ── Play video in browser (context-based: "play that", "play it", "play the video") ──
    # These are reference-based play commands — user means the video currently visible
    # on screen, NOT a Spotify song. Must be caught BEFORE the bare Spotify matcher.
    browser_video_play_kw = [
        'play that video', 'play it', 'play this video', 'play the video',
        'play that one', 'play this one', 'play the first', 'play the top',
        'play it now', 'play it please', 'click on it', 'open that video',
        'open it', 'click the video', 'click that',
    ]
    # Also catch "play the 52 minutes one", "play the 10 minute video", etc.
    _is_browser_video_play = (
        any(kw in lower for kw in browser_video_play_kw)
        or bool(re.search(r'play\s+the\s+\d+\s*(?:minute|min|hour|hr|second)s?\s+(?:one|video)', lower))
        or (re.match(r'^(?:jarvis\s+)?play\s+(?:that|it|this|the)\b', lower) and 'spotify' not in lower)
    )
    if _is_browser_video_play:
        return {"tool_name": "play_video_in_browser", "arguments": {}}

    # ── Media (Exact matches for play/pause/resume) ───────────────────────
    if re.fullmatch(r'^(?:jarvis\s+)?(?:play|resume)(?:\s+(?:music|spotify|media|the song|it))?', lower):
        return {"tool_name": "media_play_pause", "arguments": {}}
    if re.fullmatch(r'^(?:jarvis\s+)?(?:pause|stop)(?:\s+(?:music|spotify|media|the song|it))?', lower):
        return {"tool_name": "media_play_pause", "arguments": {}}

    # ── Bare "play X" (no platform) → default Spotify ─────────────────────────
    # Exclusions: don't route reference-based play to Spotify
    _spotify_exclusions = [
        'that', 'it', 'this', 'the video', 'the one', 'minutes', 'minute',
        'hour', 'top video', 'first video', 'second video',
    ]
    play_match = re.search(
        r'(?:open\s+spotify\s+and\s+)?play(?:\s+(?:me\s+)?(?:the\s+)?(?:song|music|track|album|artist))?\s+(.+)',
        lower
    )
    if play_match and not is_question:
        song = play_match.group(1).strip(' ,.')
        song = re.sub(r'\s+(for me|please)$', '', song).strip()
        # Skip if it looks like a context reference, not a song name
        if song and len(song) > 1 and not any(excl == song or song.startswith(excl + ' ') for excl in _spotify_exclusions):
            return {"tool_name": "play_music", "arguments": {"song": song}}

    # ── YouTube SEARCH (show results, no autoplay) ────────────────────────────
    yt_search_m = re.search(
        r'(?:search|find|look\s+up|look\s+for|show|open)\s+(?:for\s+)?(?:the\s+)?(?:channel|video|playlist)?\s*(.+?)\s+(?:on|in)\s+(?:youtube|yt)\b',
        lower
    )
    if yt_search_m:
        query = _clean_yt_query(yt_search_m.group(1).strip())
        return {"tool_name": "youtube_search", "arguments": {"query": query, "autoplay": False}}

    yt_open_search_m = re.search(
        r'(?:youtube|yt)\s+(?:and\s+)?(?:search|find)\s+(?:for\s+)?(.+)',
        lower
    )
    if yt_open_search_m:
        query = _clean_yt_query(yt_open_search_m.group(1).strip())
        return {"tool_name": "youtube_search", "arguments": {"query": query, "autoplay": False}}

    if re.match(r'^(?:jarvis\s+)?(?:open|launch)\s+(?:youtube|yt)\s*$', lower):
        return {"tool_name": "open_website", "arguments": {"url": "youtube"}}

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
    if re.search(r'\bnext (song|track)\b', lower):
        return {"tool_name": "media_next", "arguments": {}}
    if re.search(r'\bprevious (song|track)\b|\bprev\b', lower):
        return {"tool_name": "media_previous", "arguments": {}}

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


    # ── Smart Web Action (Isolated Navigator) ──────────────────────────────
    smart_nav_1 = re.search(r'(?:go to|open)\s+(?:the\s+)?(?:site of\s+)?(.+?)\s+and\s+(search for.+|find.+|do.+)$', lower)
    if smart_nav_1:
        site = smart_nav_1.group(1).strip()
        task = smart_nav_1.group(2).strip()
        return {"tool_name": "smart_web_action", "arguments": {"site_name": site, "task": task}}

    smart_nav_2 = re.search(r'(?:search for|find)\s+(.+?)\s+(?:in|on|at)\s+(.+?)(?:\s+site|\s+website)?$', lower)
    if smart_nav_2 and not "whatsapp" in smart_nav_2.group(2).lower() and not "youtube" in smart_nav_2.group(2).lower():
        task = "search for " + smart_nav_2.group(1).strip()
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

    _adj = _semantic_window_adjust(lower)
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

    return None  # Fall through to LLM router

# Global state for frontend API flows (mimics voice_agent local state)
api_whatsapp_flow = {"active": False, "step": None, "contact": None, "message": None}
api_whatsapp_call_flow = {"active": False, "step": None, "contact": None}
api_note_flow = {"active": False}

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    global api_whatsapp_flow, api_whatsapp_call_flow, api_note_flow
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

    # ── PATH A: Agentic Planner for complex multi-step tasks ──────────────
    if is_complex_task(request.prompt):
        conversation_history.append({"role": "user", "content": request.prompt})
        _save_session()

        async def agentic_stream():
            full_narrative = []
            try:
                async for update in run_agentic_plan(request.prompt):
                    full_narrative.append(update)
                    # Stream each update line to the voice agent
                    yield update + "\n"
            except Exception as e:
                err_msg = f"Agentic task failed: {e}"
                full_narrative.append(err_msg)
                yield err_msg

            # Save the full execution narrative as assistant turn
            conversation_history.append({
                "role": "assistant",
                "content": "\n".join(full_narrative)
            })
            _save_session()

        return StreamingResponse(agentic_stream(), media_type="text/event-stream")

    # ── PATH B: Fast single-action path (keyword → tool → LLM response) ──

    # 1. Fast keyword detection (reliable, instant)
    tool_intent = keyword_detect_tool(request.prompt)

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

    # 4. Execute tool
    tool_output_str = ""
    if tool_name and tool_name in TOOL_REGISTRY:
        args = tool_intent.get("arguments", {})
        try:
            result = TOOL_REGISTRY[tool_name](**args)
            tool_output_str = f"[Tool result: {result}]\n\n"
            
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

    # Only call screen inspector if no tool result (avoids double-call)
    if not tool_output_str:
        try:
            current_screen = describe_screen_for_llm()
        except Exception:
            try:
                current_screen = get_screen_text_summary()
            except Exception:
                current_screen = ""

    context_parts = []
    if tool_output_str:
        context_parts.append(tool_output_str)
    if rag_context:
        context_parts.append(rag_context)
    if current_screen:
        context_parts.append(f"[Active Screen: {current_screen}]")
    context = "\n\n".join(context_parts)

    # 7. Save user turn to history
    conversation_history.append({"role": "user", "content": request.prompt})
    _save_session()

    # 8. Stream LLM response — pass context as tool_result
    async def response_stream_with_history():
        full_response = ""
        async for chunk in generate_chat_response(
            user_message=request.prompt,
            tool_name="context" if context else None,
            tool_result=context if context else None
        ):
            full_response += chunk
            yield chunk
        conversation_history.append({"role": "assistant", "content": full_response})
        _save_session()

    return StreamingResponse(
        response_stream_with_history(),
        media_type="text/event-stream"
    )


@router.delete("/chat/history")
async def clear_history():
    """Clears the conversation history (start fresh)."""
    conversation_history.clear()
    return {"status": "Conversation history cleared."}
