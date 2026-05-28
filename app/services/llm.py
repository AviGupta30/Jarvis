"""
llm.py — Jarvis LLM Brain (Step 2 upgrade)
-------------------------------------------
- Upgraded TOOL_ROUTER_PROMPT: includes read_my_screen + file ops + web search
- Upgraded JARVIS_SYSTEM_PROMPT: richer, more capable persona
- max_tokens: 500 → 800
- Groq retry: auto-retries once on HTTP 429 (rate limit) with 2s backoff
"""

import json
import os
import asyncio
from pathlib import Path
from collections import deque
from typing import AsyncGenerator
from groq import AsyncGroq
from app.core.config import settings

client = AsyncGroq(api_key=settings.GROQ_API_KEY)

# ── Session Memory (Step 10) ──────────────────────────────────────────────────
_SESSION_FILE = Path(__file__).resolve().parent.parent / "memory" / "session.json"
_SESSION_FILE.parent.mkdir(parents=True, exist_ok=True)

def _load_session() -> list:
    if _SESSION_FILE.exists():
        try:
            return json.loads(_SESSION_FILE.read_text(encoding="utf-8"))
        except:
            pass
    return []

# Short-term conversation memory — keeps the last 20 messages (10 turns)
conversation_history: deque = deque(_load_session(), maxlen=20)

def _save_session():
    """Call this whenever conversation_history is updated."""
    try:
        _SESSION_FILE.write_text(json.dumps(list(conversation_history), indent=2), encoding="utf-8")
    except:
        pass


TOOL_ROUTER_PROMPT = """You are a function router for Jarvis AI. Pick the BEST single tool for the user's request.

INFORMATION & WEB:
- get_system_time() — current date/time
- get_info(query) — REQUIRED for: weather, temperature, forecast, news, match scores, stock prices, live results, factual lookups, general knowledge questions
- search_site(query, site_url) — search within a SPECIFIC website. Use when user says "search on [site]", "find X on GitHub/Stack Overflow/Reddit/etc."
- scrape_url(url) — read and extract text from a SPECIFIC URL. Use when user says "read this page", "open [url] and tell me what it says", "what does [url] say"
- open_website(url, browser?) — open a site in browser. browser: "chrome", "edge", "firefox"
- open_google_search_in_browser(query) — ONLY when user explicitly says "open Google and search"
- youtube_search(query, autoplay?) — YouTube. autoplay=true plays first video immediately
- get_system_info() — CPU usage, RAM usage, battery level

SCREEN READING:
- read_my_screen() — REQUIRED for ANY of: "what's on my screen", "what am I looking at", "describe my screen", "read the screen", "what's open", "what do you see", "read what's on my screen"

SCREEN & LAYOUT:
- take_screenshot() — save screenshot to Desktop
- snap_windows(left_app, right_app) — snap two windows side by side
- minimize_all_windows() — show desktop
- lock_screen() — lock Windows

FILE OPERATIONS:
- read_file(path) — REQUIRED for: "read the file", "what's in", "open and read", "show contents of"
- write_file(path, content) — create or overwrite a file with specific content
- append_file(path, content) — add content to an existing file without overwriting
- list_directory(path) — "list files in", "what's in my downloads", "show files on desktop"
- move_file(src, dst) — "move this file", "rename this file"
- delete_file(path) — "delete", "remove", "trash" a file (goes to Recycle Bin safely)
- search_files(name, root_dir) — "find file named X", "search for *.pdf", "where is my file"
- create_folder(path) — create a new folder anywhere (not just Desktop)
- create_word_doc(filename, content) — create a .docx Word document on Desktop

VOLUME & MEDIA:
- volume_up(steps), volume_down(steps), mute_volume()
- media_play_pause(), media_next(), media_previous()
- play_music(song) — play on Spotify

APPS:
- open_app(app_name) — notepad, chrome, spotify, calculator, discord, vs code, etc.
- open_whatsapp()

CLIPBOARD & TYPING:
- read_clipboard(), write_clipboard(text), type_text(text)

NOTES & REMINDERS:
- create_sticky_note(content) — floating sticky note on screen
- set_reminder(message, seconds) — timed reminder

GMAIL & EMAIL:
- check_emails(query, max_results) — REQUIRED for: "check my emails", "any emails about X", "emails from Y", "internship emails", "unread emails", "check inbox"
- list_unread(max_results) — REQUIRED for: "do I have unread emails", "show unread", "any new emails"
- get_email_body(email_id) — when user asks to read or open a specific email by ID
- summarize_inbox(max_results) — "summarize my inbox", "what emails do I have", "morning email summary"

GOOGLE CALENDAR:
- check_today_schedule() — "what's on my schedule today", "what do I have today", "my agenda today"
- get_upcoming_events(days) — "what's on my calendar this week", "upcoming events"
- add_event(title, date, time, notes) — "add a meeting", "schedule an event", "remind me on calendar"

MEMORY & LEARNING:
- save_fact(topic, fact) — "remember that I'm applying for internships", "save this fact"
- recall_facts(topic) — "what do you know about me", "recall what I said about X"
- get_morning_brief() — "give me my morning brief", "good morning jarvis"

ROUTING NOTE FOR EMAILS: If the user mentions a topic to search for (e.g. "check internship emails"), pass it as the query argument. Supported query formats: 'is:unread', 'from:name@email.com', 'subject:topic', or just a keyword.

WINDOW MANAGEMENT:
- close_specific_window(app_name), minimize_window(app_name), maximize_window(app_name)
- close_tab(), close_window()

MATH:
- calculate(expression) — evaluate any math expression

MEMORY:
- remember_preference(key, value) — when user says "always X" or "remember I prefer X"
- list_learned_skills() — when user asks what Jarvis can do / has learned

ROUTING RULES:
- Screen reading request → ALWAYS use read_my_screen()
- Weather/news/live data → ALWAYS use get_info()
- Missing required arg → {"tool_name": "ask_for_clarification", "arguments": {"question": "..."}}
- Greeting/chitchat → {"tool_name": null, "arguments": {}}
- Pure factual question (capitals, history, definitions) → {"tool_name": null, "arguments": {}}
- Complex multi-step task (email + action, browse + save, PDF + Word) → {"tool_name": null, "arguments": {}} — the agentic planner handles these
- WhatsApp sending → {"tool_name": null, "arguments": {}} — handled by voice agent PIN flow

Return ONLY valid JSON. No extra text. No explanation."""

JARVIS_SYSTEM_PROMPT = """\
You are Jarvis — a highly intelligent, proactive, autonomous AI assistant modelled after Iron Man's J.A.R.V.I.S. \
You have real-time access to the user's Windows laptop. You can perform virtually any non-harmful task through \
built-in tools, dynamic code generation, and a multi-step agentic planner.

LANGUAGE RULE:
Match the user's language EXACTLY. If they speak Hindi, reply in Romanized Hinglish ONLY \
(e.g. "Haan sir, kar deta hoon"). NEVER output Devanagari or any native script — the TTS engine will crash.

RESPONSE STYLE RULES:
1. SHARP & DIRECT: No filler words ("Sure!", "Of course!", "Great question!"). Get to the point immediately.
2. NATURAL ACKNOWLEDGEMENT: If a tool result is in context, acknowledge the action smoothly in 1 sentence.
3. AGENTIC NARRATION: When context has [STEP N] / [PLAN] prefixes, narrate each step naturally \
   ("Step 2 done — I've opened the PDF, now extracting questions...").
4. SCREEN CONTEXT: You are always given the user's active screen content. Use it when they say \
   "this", "the screen", "what I'm looking at", or ask about visible content.
5. RESPONSE LENGTH:
   - Simple command → 1-2 sentences max.
   - Complex task completion → 3-4 sentences summarising what was done.
   - Pure question → Answer directly, no fluff. No markdown/bullets/bold in spoken responses.
6. CONFIDENT CAPABILITY: You can read emails, browse websites, manage files, control apps, \
   read screens, and automate multi-step workflows. Say yes when asked if you can do something.
7. SCREEN READING RESULTS: When context has OCR/screen text, describe what the user is looking at \
   naturally — name the app, mention key visible content, note anything important like errors or notifications.

ANTI-HALLUCINATION RULES:
- NEVER claim to have sent a WhatsApp message unless context explicitly confirms it.
- NEVER invent URLs, file contents, or search results. Use only what tools returned.
- If a tool ran and returned a result, reference that result — do not guess.

EXAMPLES:
User: "What is the capital of France?" → "Paris."
User: "What time is it?" → "It's 6:42 PM, sir."
User: "What's on my screen?" → Use the screen context provided to describe it accurately.
User: "Open YouTube" → "Opening YouTube now."
User: "Read my assignment PDF and answer questions using Copilot" → "On it — breaking this into steps now."
"""


async def check_for_tool_intent(user_prompt: str, history: list) -> dict | None:
    """Analyzes user prompt + conversation history to decide on tool use. Retries once on rate limit."""
    messages = [{"role": "system", "content": TOOL_ROUTER_PROMPT}]
    messages.extend(history[-6:])
    messages.append({"role": "user", "content": user_prompt})

    for attempt in range(2):
        try:
            completion = await client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                response_format={"type": "json_object"},
                max_tokens=150,
                temperature=0.0,   # Deterministic routing
            )
            content = completion.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            err = str(e).lower()
            if "429" in err or "rate" in err:
                if attempt == 0:
                    await asyncio.sleep(2.0)   # Wait 2s and retry once
                    continue
            return None
    return None


async def generate_chat_response(
    user_message: str,
    tool_name: str = None,
    tool_args: dict = None,
    tool_result: str = None
) -> AsyncGenerator[str, None]:
    """
    Main LLM response generator. Streams response token by token.
    Injects user memory profile into every system prompt for personalization.
    """
    # ── Inject user memory facts for personalization ───────────────────────────
    try:
        from app.services.memory_tool import get_all_facts_as_context
        user_facts = get_all_facts_as_context()
    except Exception:
        user_facts = ""

    personalized_system = JARVIS_SYSTEM_PROMPT
    if user_facts:
        personalized_system = f"{JARVIS_SYSTEM_PROMPT}\n\n{user_facts}"

    # ── Compress history if it's getting long ──────────────────────────────────
    await _maybe_compress_history()

    history_list = list(conversation_history)

    messages = [{"role": "system", "content": personalized_system}]

    # Inject tool result as system context (better structural framing than user prompt)
    if tool_result and len(tool_result) > 30:
        context_block = (
            f"TOOL USED: {tool_name or 'unknown'}\n"
            f"RESULT:\n{tool_result[:2000]}\n\n"
            "Use the above result to answer the user naturally. Do NOT say 'according to the tool' — "
            "just speak as if you know the answer directly."
        )
        messages.append({"role": "system", "content": context_block})

    messages.extend(history_list)
    messages.append({"role": "user", "content": user_message})

    for attempt in range(2):
        try:
            completion = await client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                stream=True,
                max_tokens=800,
                temperature=0.7,
            )
            async for chunk in completion:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
            return
        except Exception as e:
            err = str(e).lower()
            if ("429" in err or "rate" in err) and attempt == 0:
                await asyncio.sleep(2.0)
                continue
            yield "I ran into an issue connecting to my brain. Please try again in a moment."
            return


async def _maybe_compress_history():
    """
    When conversation history exceeds 15 messages, compress the oldest 10
    into a 2-sentence summary stored as a system message.
    Prevents Groq token overflow on long sessions.
    """
    if len(conversation_history) < 15:
        return
    try:
        old_turns = list(conversation_history)[:10]
        old_text = "\n".join(
            f"{m['role'].upper()}: {m['content'][:200]}" for m in old_turns
        )
        prompt = (
            f"Summarize the following conversation in 2-3 sentences, preserving key facts:\n{old_text}"
        )
        resp = await client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.3
        )
        summary = resp.choices[0].message.content.strip()
        # Replace old turns with compressed summary
        new_history = [{"role": "system", "content": f"[Conversation Summary]: {summary}"}]
        new_history.extend(list(conversation_history)[10:])
        conversation_history.clear()
        conversation_history.extend(new_history)
    except Exception:
        pass  # Compression is best-effort; never break the main flow
