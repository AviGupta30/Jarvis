"""
llm.py — Jarvis LLM Brain
---------------------------
Model routing (all Groq):
  FAST_MODEL (openai/gpt-oss-20b)  → tool routing, simple replies, history compression
  DEEP_MODEL (openai/gpt-oss-120b) → complex reasoning / long tool results (_is_complex_response)

Free-tier throughput: each model has its own 8,000 tokens/min bucket and one request
(router ~2.8k prompt tokens + reply) uses ~4k, so a second request within a minute
used to hit 429 and the SDK silently waited ~30 s. Every response's rate-limit headers
are recorded (_track_limits) and pick_model() sends a call to whichever gpt-oss bucket
has room; a 429 switches to the other model immediately instead of waiting.
"""

import json
import os
import re
import time
import asyncio
import httpx
from pathlib import Path
from collections import deque
from typing import AsyncGenerator
from groq import AsyncGroq
from app.core.config import settings
from app.services.personality import TOOL_ROUTER_PROMPT, get_context_aware_prompt
from app.services.context_classifier import classify_context

FAST_MODEL = "openai/gpt-oss-20b"
DEEP_MODEL = "openai/gpt-oss-120b"

# ── Token-bucket tracking across the two gpt-oss models ───────────────────────
_BUCKETS: dict[str, dict] = {}   # model -> {"remaining": int, "reset_at": epoch s}
_TPM_DEFAULT = 8000


def _parse_reset(value: str | None) -> float:
    """Groq reset strings: '30.56s', '577ms', '1m2.5s'."""
    if not value:
        return 0.0
    total = 0.0
    for num, unit in re.findall(r"([\d.]+)(ms|m|s|h)", value):
        total += float(num) * {"ms": 0.001, "s": 1, "m": 60, "h": 3600}[unit]
    return total


async def _track_limits(response: httpx.Response):
    try:
        rem = response.headers.get("x-ratelimit-remaining-tokens")
        if rem is None:
            return
        model = json.loads(response.request.content or b"{}").get("model")
        if model:
            _BUCKETS[model] = {
                "remaining": int(float(rem)),
                "reset_at": time.time() + _parse_reset(response.headers.get("x-ratelimit-reset-tokens")),
            }
    except Exception:
        pass


def _room(model: str) -> int:
    b = _BUCKETS.get(model)
    if not b or time.time() >= b["reset_at"]:
        return _TPM_DEFAULT
    return b["remaining"]


def _other(model: str) -> str:
    return DEEP_MODEL if model == FAST_MODEL else FAST_MODEL


def pick_model(preferred: str, need: int) -> str:
    """Preferred model unless its bucket can't fit `need` tokens and the other has more room."""
    if preferred not in (FAST_MODEL, DEEP_MODEL):
        return preferred
    if _room(preferred) >= need or _room(preferred) >= _room(_other(preferred)):
        return preferred
    return _other(preferred)


def _is_rate_limit(e: Exception) -> bool:
    err = str(e).lower()
    return "429" in err or "rate limit" in err or "rate_limit" in err


def _mark_exhausted(model: str, e: Exception):
    """A 429 (per-minute OR per-day) parks that model until Groq's 'try again in …'."""
    m = re.search(r"try again in ((?:[\d.]+(?:ms|h|m|s))+)", str(e))
    wait = _parse_reset(m.group(1)) if m else 30.0
    _BUCKETS[model] = {"remaining": 0, "reset_at": time.time() + max(wait, 1.0)}


client = AsyncGroq(
    api_key=settings.GROQ_API_KEY,
    max_retries=0,   # we fail over to the other bucket instead of the SDK sleeping ~30 s
    http_client=httpx.AsyncClient(timeout=httpx.Timeout(60.0, connect=10.0),
                                  event_hooks={"response": [_track_limits]}),
)


async def _groq_generate(messages: list, max_tokens: int = 800, temperature: float = 0.7,
                         model: str = FAST_MODEL) -> AsyncGenerator[str, None]:
    """Stream a response from a Groq chat model (fails over between the gpt-oss buckets)."""
    need = sum(len(str(m.get("content", ""))) for m in messages) // 4 + max_tokens
    model = pick_model(model, need)
    for attempt in range(3):
        started = False
        try:
            completion = await client.chat.completions.create(
                model=model,
                messages=messages,
                stream=True,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            async for chunk in completion:
                if chunk.choices[0].delta.content is not None:
                    started = True
                    yield chunk.choices[0].delta.content
            return
        except Exception as e:
            if not started and _is_rate_limit(e) and attempt < 2:
                _mark_exhausted(model, e)
                if _room(_other(model)) > 0:
                    model = _other(model)          # other bucket, no waiting
                else:
                    # Both buckets empty: wait for whichever refills first (≤ 20 s) —
                    # a late answer beats "I couldn't connect".
                    resets = [b["reset_at"] for b in _BUCKETS.values() if b.get("reset_at")]
                    await asyncio.sleep(min(max(min(resets, default=0) - time.time(), 1.0), 20.0))
                    model = max((FAST_MODEL, DEEP_MODEL), key=_room)
                continue
            if not started:
                yield "I ran into an issue connecting to my brain. Please try again in a moment."
            return


def _is_complex_response(tool_result: str, user_message: str) -> bool:
    """
    Decide whether to use DEEP_MODEL (complex reasoning) vs FAST_MODEL.
    Complex = agentic plan narration, code explanation, deep analysis, long tool results.
    """
    if tool_result and len(tool_result) > 500:
        return True  # Long tool result → larger model reasons over it better
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

    need = sum(len(str(m.get("content", ""))) for m in messages) // 4 + 600
    model = pick_model(FAST_MODEL, need)
    for attempt in range(2):
        try:
            completion = await client.chat.completions.create(
                model=model,
                messages=messages,
                response_format={"type": "json_object"},
                # gpt-oss is a reasoning model: hidden reasoning counts against max_tokens.
                # 150 was often used up before any JSON was emitted (json_validate_failed).
                max_tokens=600,
                reasoning_effort="low",
                temperature=0.0,   # Deterministic routing
            )
            content = completion.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            if _is_rate_limit(e) and attempt == 0:
                _mark_exhausted(model, e)
                model = _other(model)   # other gpt-oss bucket, no waiting
                continue
            return None
    return None


def _reply_language_note(language: str, voice: bool) -> str:
    if language == "english":
        note = ("[REPLY LANGUAGE] The user spoke ENGLISH. Reply in English only — "
                "no Hindi or Hinglish words, even if earlier turns were in Hindi.")
    elif voice:
        note = ("[REPLY LANGUAGE] The user spoke HINDI. Reply in natural conversational Hindi as "
                "spoken in India, written in DEVANAGARI script (a Hindi voice will read it aloud). "
                "Keep names, app names, numbers and technical terms in English/Latin letters. "
                "Do not reply in English sentences, even if earlier turns were in English.")
    else:
        note = ("[REPLY LANGUAGE] The user spoke HINDI/HINGLISH. Reply in natural Hindi written in "
                "Roman letters (romanized Hindi), not in English sentences, even if earlier turns "
                "were in English.")
    if voice:
        note += ("\n[VOICE] This reply is spoken aloud. Keep it short and natural (1-3 sentences "
                 "unless the user asked for detail). No markdown, lists, tables, URLs or emoji.")
    return note


async def generate_chat_response(
    user_message: str,
    tool_name: str = None,
    tool_args: dict = None,
    tool_result: str = None,
    language: str | None = None,
    voice: bool = False,
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
    # The voice agent knows the spoken language from the audio (Whisper language ID),
    # which beats guessing from romanized words — honour it when given.
    if language in ("en", "english"):
        ctx["language"] = "english"
    elif language in ("hi", "hindi", "hinglish"):
        ctx["language"] = "hindi"
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

    # ── Long-term RAG Memory Recall (MySQL + FAISS) ────────────────────────────
    # Always-on semantic recall: if past turns are similar to this query, inject them.
    # No need for explicit "remember" keywords — if it's related, Jarvis recalls it.
    try:
        from app.services.rag_memory import recall, format_recall_for_prompt
        recalled = await recall(user_message, top_k=5, min_score=0.30)
        if recalled:
            memory_block = format_recall_for_prompt(recalled, query=user_message)
            if memory_block:
                messages.append({"role": "system", "content": memory_block})
    except Exception:
        pass  # Memory recall is best-effort — never break the chat flow

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
    # Language rule again, right before the user turn: otherwise the language of
    # earlier turns in history wins and an English question gets a Hinglish answer.
    messages.append({"role": "system", "content": _reply_language_note(ctx["language"], voice)})
    messages.append({"role": "user", "content": user_message})

    for attempt in range(2):
        try:
            # Route to correct model based on complexity
            if _is_complex_response(tool_result or "", user_message):
                # Larger model for deep reasoning / long tool result analysis
                async for token in _groq_generate(messages, max_tokens=1000, temperature=0.7, model=DEEP_MODEL):
                    yield token
            else:
                # Fast model for simple responses
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
            model=pick_model(FAST_MODEL, len(prompt) // 4 + 150),
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
