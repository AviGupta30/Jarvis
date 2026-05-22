from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import re
from app.services.llm import (
    generate_chat_response,
    check_for_tool_intent,
    conversation_history,
)
from app.services.embeddings import get_embedding
from app.services.vector_store import search_similar_chunks
from app.services.tools import TOOL_REGISTRY
from app.services.dynamic_skill import run_dynamic_skill
from app.services.planner import run_agentic_plan, is_complex_task
from app.services.ui_inspector import get_screen_text_summary
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

    # ── Play on Spotify explicitly: "play X on spotify" ──────────────────────
    spotify_play_m = re.match(
        r'^(?:jarvis\s+)?play(?:\s+(?:me\s+)?(?:the\s+)?(?:song|music|track|album|artist))?\s+(.+?)\s+on\s+spotify\s*$',
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

    # ── Bare "play X" (no platform) → default Spotify ─────────────────────────
    play_match = re.match(
        r'^(?:jarvis\s+)?play(?:\s+(?:me\s+)?(?:the\s+)?(?:song|music|track|album|artist))?\s+(.+)',
        lower
    )
    if play_match and not is_question:
        song = play_match.group(1).strip(' ,.')
        song = re.sub(r'\s+(for me|please)$', '', song).strip()
        if song and len(song) > 1:
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

    # ── Media ─────────────────────────────────────────────────────────────
    if re.search(r'\bpause\b|\bplay\b', lower) and any(w in lower for w in ['music', 'song', 'spotify', 'media']):
        return {"tool_name": "media_play_pause", "arguments": {}}
    if re.search(r'\bnext (song|track)\b', lower):
        return {"tool_name": "media_next", "arguments": {}}
    if re.search(r'\bprevious (song|track)\b|\bprev\b', lower):
        return {"tool_name": "media_previous", "arguments": {}}

    # ── WhatsApp desktop app ─────────────────────────────────────────────
    if re.search(r'\bopen\s+whatsapp\b|\blaunch\s+whatsapp\b|\bstart\s+whatsapp\b', lower):
        if not any(w in lower for w in ['send', 'message', 'msg', 'text']):
            return {"tool_name": "open_whatsapp", "arguments": {}}

    # ── Sticky note ────────────────────────────────────────────────────────
    note_m = re.search(r'(?:add|create|write|make|put|save)\s+(?:a\s+)?(?:short\s+)?(?:note|sticky|reminder)\b', lower)
    if note_m:
        content_m = re.search(r'(?:note|sticky|reminder)\s+(?:saying|that says|:)\s*["\']?(.+?)["\']?\s*$', lower)
        content = content_m.group(1).strip() if content_m else ""
        if not content:
            return {"tool_name": "ask_for_clarification", "arguments": {"question": "What should I write in the note?"}}
        return {"tool_name": "create_sticky_note", "arguments": {"content": content}}

    if re.search(r'(?:delete|remove|close|clear)\s+(?:the\s+)?(?:sticky\s+)?note', lower):
        return {"tool_name": "close_sticky_notes", "arguments": {}}

    # ── Open in specific browser ───────────────────────────────────────────────
    browser_m = re.search(
        r'(?:open|launch|go to)\s+(.+?)\s+(?:using|in|with|via|on)\s+(chrome|edge|firefox)',
        lower
    )
    if browser_m:
        site = browser_m.group(1).strip().strip('.,!?')
        browser = browser_m.group(2).strip()
        return {"tool_name": "open_website", "arguments": {"url": site, "browser": browser}}

    # ── Open a website / app ─────────────────────────────────────────────
    open_match = re.match(
        r'^(?:jarvis\s+)?(?:open|launch|go to|take me to|show me|start|tune in to|focus)\s+(.+?)(?:\s+(?:website|site|page|app|browser))?\s*$',
        lower
    )
    if open_match:
        site = open_match.group(1).strip().strip('.,!?;:\'"')
        non_web = ['notepad', 'calculator', 'settings', 'file explorer', 'task manager',
                   'camera', 'calendar', 'photos', 'paint', 'terminal', 'cmd', 'powershell']
        context_words = ['channel', 'video', 'playlist', 'on youtube', 'search', 'and', 'for me']
        if site not in non_web and not any(w in site for w in context_words):
            if len(site.split()) <= 3:
                return {"tool_name": "open_website", "arguments": {"url": site}}
            return {"tool_name": "open_google_search_in_browser", "arguments": {"query": site}}

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
        if app in ('the current', 'current', 'this', 'active', 'the current window', 'current window', 'this window', 'active window', 'all windows', 'everything'):
            return {"tool_name": "minimize_all_windows", "arguments": {}}
        return {"tool_name": "minimize_window", "arguments": {"app_name": app}}

    maximize_m = re.match(r'^(?:jarvis\s+)?(?:maximize|maximise|fullscreen|full screen|enlarge)\s+(.+?)(?:\s+(?:window|app|tab))?\s*$', lower)
    if maximize_m:
        return {"tool_name": "maximize_window", "arguments": {"app_name": maximize_m.group(1).strip().strip('.,!?')}}

    return None  # Fall through to LLM router


@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    history_list = list(conversation_history)

    # ── PATH A: Agentic Planner for complex multi-step tasks ──────────────
    if is_complex_task(request.prompt):
        conversation_history.append({"role": "user", "content": request.prompt})

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
        conversation_history.append({"role": "user", "content": request.prompt})
        conversation_history.append({"role": "assistant", "content": question})

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

    # 8. Stream LLM response
    async def response_stream_with_history():
        full_response = ""
        async for chunk in generate_chat_response(request.prompt, context=context, history=history_list):
            full_response += chunk
            yield chunk
        conversation_history.append({"role": "assistant", "content": full_response})

    return StreamingResponse(
        response_stream_with_history(),
        media_type="text/event-stream"
    )


@router.delete("/chat/history")
async def clear_history():
    """Clears the conversation history (start fresh)."""
    conversation_history.clear()
    return {"status": "Conversation history cleared."}
