"""
llm.py — Jarvis LLM Brain
---------------------------
Model routing:
  Groq llama-3.3-70b-versatile  → tool routing + simple fast responses
  Gemma 4 (Google AI Studio)    → complex reasoning, planner narration, deep Q&A
  Groq llama-3.1-8b-instant     → history compression (cheap + fast)

All models are 100% free on their respective free tiers.
"""

import json
import os
import asyncio
from pathlib import Path
from collections import deque
from typing import AsyncGenerator
from groq import AsyncGroq
from app.core.config import settings
from app.services.personality import TOOL_ROUTER_PROMPT, get_context_aware_prompt
from app.services.context_classifier import classify_context

client = AsyncGroq(api_key=settings.GROQ_API_KEY)

# ── Gemma 4 client (Google AI Studio — same free key as screen_vision) ────────

async def _gemma_generate(messages: list, max_tokens: int = 800, temperature: float = 0.7) -> AsyncGenerator[str, None]:
    """
    Stream a response from Gemma 4 (gemma-3-27b-it) via Google AI Studio.
    Same GEMINI_API_KEY used by the screen vision module.
    Falls back to Groq Llama on any error.
    """
    try:
        async for token in _groq_generate(messages, max_tokens, temperature):
            yield token
    except Exception as e:
        import logging
        logging.getLogger(__name__).warning(f"[llm] Gemma fallback to Groq: {e}")


async def _groq_generate(messages: list, max_tokens: int = 800, temperature: float = 0.7) -> AsyncGenerator[str, None]:
    """Stream a response from Groq Llama 3.3 70B."""
    for attempt in range(2):
        try:
            completion = await client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                stream=True,
                max_tokens=max_tokens,
                temperature=temperature,
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


def _is_complex_response(tool_result: str, user_message: str) -> bool:
    """
    Decide whether to use Gemma 4 (complex reasoning) vs Groq Llama (fast).
    Complex = agentic plan narration, code explanation, deep analysis, long tool results.
    """
    if tool_result and len(tool_result) > 500:
        return True  # Long tool result → Gemma reasons over it better
    complex_kw = [
        "explain", "why", "how does", "analyse", "analyze", "debug",
        "write", "summarize", "plan", "suggest", "compare", "fix",
        "what went wrong", "what should i", "help me understand",
    ]
    lower = user_message.lower()
    return any(kw in lower for kw in complex_kw)


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


# JARVIS_SYSTEM_PROMPT and TOOL_ROUTER_PROMPT now live in personality.py —
# imported above. This ensures a single source of truth.


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

    # ── Build dynamic, context-aware system prompt ──────────────────────────────
    # Classify context so Jarvis adjusts tone for time-of-day and mood
    ctx = classify_context(user_message)
    personalized_system = get_context_aware_prompt(
        hour=ctx["hour"],
        user_mood=ctx["mood"],
        language=ctx["language"],
    )

    # Urgency injection (one-sentence max when user is in a rush)
    if ctx["urgency"] == "high":
        personalized_system += "\n[URGENCY] User is in a hurry. Be extremely brief. One sentence max. No humor."
    if ctx["topic"] == "casual_chat":
        personalized_system += "\n[TOPIC] This is small talk. Be warm and conversational."

    # Inject user memory facts for personalization
    if user_facts:
        personalized_system += f"\n\n{user_facts}"

    messages = [{"role": "system", "content": personalized_system}]

    # ── Compress history if it's getting long ──────────────────────────────────
    await _maybe_compress_history()

    history_list = list(conversation_history)

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
            # Route to correct model based on complexity
            if _is_complex_response(tool_result or "", user_message):
                # Gemma 4 for deep reasoning / long tool result analysis
                async for token in _gemma_generate(messages, max_tokens=1000, temperature=0.7):
                    yield token
            else:
                # Groq Llama for fast simple responses
                async for token in _groq_generate(messages, max_tokens=800, temperature=0.7):
                    yield token
            return
        except Exception as e:
            err = str(e).lower()
            if ("429" in err or "rate" in err or "quota" in err) and attempt == 0:
                await asyncio.sleep(2.0)
                continue
            if "429" not in err and "quota" not in err:
                import logging
                logging.getLogger(__name__).error(f"[llm] Chat generation failed: {e}")
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
