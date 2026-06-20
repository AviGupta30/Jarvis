"""
reply_generator.py — Jarvis WhatsApp Intelligence: Reply Generator
===================================================================
COMPLETELY ISOLATED — imports nothing from the rest of Jarvis.
Safe to modify without affecting any other functionality.

PURPOSE:
    Takes a WhatsApp thread + your style profile and calls the LLM to
    generate 3 reply drafts ranked by naturalness.

    The LLM is told to sound exactly like YOU — using your avg reply length,
    hinglish ratio, emoji frequency, punctuation style, and your own examples.

LLM ROUTING (mirrors llm.py logic — uses Groq directly, no llm.py import):
    - Groq llama-3.1-8b-instant  (same API key from env)
    - Falls back gracefully if the key is missing

OUTPUT FORMAT:
    [
        {"rank": 1, "draft": "haan aa jaunga kal", "confidence": "high"},
        {"rank": 2, "draft": "kal tak dekh lete hai bhai", "confidence": "medium"},
        {"rank": 3, "draft": "thoda busy hun abhi, kal baat karte hai", "confidence": "low"},
    ]

DRAFT CACHE (in-memory per session):
    _DRAFT_CACHE stores the last generated drafts so that
    send_style_reply(contact, draft_index) can pick them up
    without re-generating.
"""

import os
import json
import re
from typing import List, Dict, Optional

from whatsapp_intelligence.style_profiler import get_profile
from whatsapp_intelligence.thread_extractor import extract_thread

# ─────────────────────────────────────────────────────────────────────────────
# IN-MEMORY DRAFT CACHE  (one session, one contact at a time)
# ─────────────────────────────────────────────────────────────────────────────

_DRAFT_CACHE: Dict = {
    "contact": "",
    "latest_incoming": "",
    "drafts": [],        # list of {"rank":int, "draft":str, "confidence":str}
}


# ─────────────────────────────────────────────────────────────────────────────
# LLM CALLER  (direct Groq — no llm.py dependency)
# ─────────────────────────────────────────────────────────────────────────────

def _get_groq_api_key() -> str:
    """
    Resolves the Groq API key.
    Priority: env var → app.core.config settings (if available)
    """
    key = os.environ.get("GROQ_API_KEY", "")
    if key:
        return key

    # Non-critical fallback — try loading from Jarvis settings
    # If Jarvis isn't importable (isolated test), this just silently fails
    try:
        import sys
        sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent.parent.parent.parent))
        from app.core.config import settings          # noqa: F401
        return settings.GROQ_API_KEY
    except Exception:
        pass

    return ""


def _call_groq(prompt: str, system: str, max_tokens: int = 600, temperature: float = 0.8) -> str:
    """
    Synchronous Groq call — kept sync intentionally so this module
    can be called from the tools registry without async overhead.
    """
    key = _get_groq_api_key()
    if not key:
        return ""

    try:
        from groq import Groq
        client = Groq(api_key=key)
        resp = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return resp.choices[0].message.content.strip()
    except Exception:
        return ""


# ─────────────────────────────────────────────────────────────────────────────
# PROMPT BUILDER
# ─────────────────────────────────────────────────────────────────────────────

def _build_system_prompt(profile: Dict, contact_name: str) -> str:
    """
    Builds the LLM system prompt that injects the user's style profile.
    The LLM is told to be the user, not Jarvis.
    """
    is_formal = contact_name in profile.get("formal_contacts", [])
    tone_instruction = (
        "Be professional and polite — this is a formal contact."
        if is_formal
        else "Be casual, natural, and informal."
    )

    hinglish_pct = int(profile.get("hinglish_ratio", 0.3) * 100)
    emoji_pct = int(profile.get("emoji_frequency", 0.1) * 100)
    avg_len = profile.get("avg_reply_length", 10)
    punct_style = profile.get("punctuation_style", "no_period")
    fillers = profile.get("common_fillers", [])
    deflections = profile.get("deflection_phrases", [])

    punct_desc = {
        "no_period": "Do NOT end sentences with periods.",
        "normal": "Use normal punctuation including periods.",
        "minimal": "Use minimal punctuation — commas are okay, periods only when needed.",
    }.get(punct_style, "Use minimal punctuation.")

    filler_line = (
        f"Naturally include these filler words/phrases when appropriate: {', '.join(fillers)}"
        if fillers else ""
    )

    deflection_line = (
        f"When the context calls for it, use phrases like: {', '.join(deflections)}"
        if deflections else ""
    )

    examples = profile.get("reply_examples", [])[-5:]   # last 5 for few-shot
    example_block = ""
    if examples:
        example_lines = []
        for ex in examples:
            example_lines.append(f"  THEM: {ex['their_msg']}")
            example_lines.append(f"  YOU:  {ex['your_reply']}")
        example_block = (
            "\n\nHere are real examples of how this person replies:\n"
            + "\n".join(example_lines)
        )

    return f"""You are generating WhatsApp replies on behalf of the user. Your job is to write replies that sound EXACTLY like them — not like an AI, not like Jarvis.

STYLE RULES (follow all of them precisely):
- Reply length: approximately {avg_len} words. Short and punchy, not long-winded.
- Language mix: ~{hinglish_pct}% Hinglish (mix of Hindi words in English script), rest English.
  {0 if hinglish_pct < 20 else "Use natural Hindi words like bhai, yaar, haan, theek, kal, abhi when appropriate."}
- Emoji usage: {emoji_pct}% of replies should have an emoji. {"Include one if natural." if emoji_pct > 10 else "Avoid emojis unless clearly appropriate."}
- Punctuation: {punct_desc}
- Tone: {tone_instruction}
{filler_line}
{deflection_line}
{example_block}

OUTPUT FORMAT — respond ONLY with valid JSON, no extra text:
{{
  "drafts": [
    {{"rank": 1, "draft": "...", "confidence": "high"}},
    {{"rank": 2, "draft": "...", "confidence": "medium"}},
    {{"rank": 3, "draft": "...", "confidence": "low"}}
  ]
}}

Generate exactly 3 reply options, ranked from most natural/likely to least. Each should be meaningfully different."""


def _build_user_prompt(thread: List[Dict], latest_incoming: str, contact_name: str) -> str:
    """Builds the per-request prompt with thread context."""
    # Show last 6 turns of context (enough without bloating the prompt)
    context_turns = thread[-6:] if len(thread) > 6 else thread

    thread_lines = []
    for msg in context_turns:
        who = "YOU" if msg["sender"] == "you" else contact_name.upper()
        ts = f" [{msg['timestamp']}]" if msg.get("timestamp") else ""
        thread_lines.append(f"{who}{ts}: {msg['text']}")

    thread_str = "\n".join(thread_lines) if thread_lines else "(no prior context)"

    return (
        f"CONVERSATION CONTEXT:\n{thread_str}\n\n"
        f"THEIR LATEST MESSAGE: \"{latest_incoming}\"\n\n"
        f"Generate 3 reply options for the message above."
    )


# ─────────────────────────────────────────────────────────────────────────────
# PARSING
# ─────────────────────────────────────────────────────────────────────────────

def _parse_drafts_from_response(raw: str) -> List[Dict]:
    """
    Parses the LLM JSON response into a clean list of draft dicts.
    Handles malformed JSON gracefully.
    """
    # Try direct JSON parse
    try:
        # Strip markdown code fences if present
        clean = re.sub(r"```(?:json)?", "", raw).strip().strip("`").strip()
        data = json.loads(clean)
        drafts = data.get("drafts", [])
        if drafts and isinstance(drafts, list):
            return [
                {
                    "rank": int(d.get("rank", i + 1)),
                    "draft": str(d.get("draft", "")).strip(),
                    "confidence": str(d.get("confidence", "medium")),
                }
                for i, d in enumerate(drafts)
                if d.get("draft")
            ]
    except Exception:
        pass

    # Fallback: extract quoted strings that look like replies
    quoted = re.findall(r'"draft"\s*:\s*"([^"]+)"', raw)
    if quoted:
        confidences = ["high", "medium", "low"]
        return [
            {"rank": i + 1, "draft": d.strip(), "confidence": confidences[i] if i < 3 else "low"}
            for i, d in enumerate(quoted[:3])
        ]

    return []


# ─────────────────────────────────────────────────────────────────────────────
# PUBLIC API
# ─────────────────────────────────────────────────────────────────────────────

def generate_reply_draft(contact_name: str, n_messages: int = 20) -> str:
    """
    Tool-registry entry point.
    Reads the thread, loads the style profile, calls the LLM,
    and returns 3 numbered reply drafts.

    The drafts are cached in _DRAFT_CACHE so send_style_reply() can
    pick them up immediately without re-reading or re-generating.

    Args:
        contact_name: Name exactly as saved in WhatsApp.
        n_messages:   How many recent messages to load for context.

    Returns:
        Human-readable string with 3 numbered draft options.
    """
    global _DRAFT_CACHE

    try:
        # Step 1: Extract the thread
        thread_data = extract_thread(contact_name, n_messages)

        if "error" in thread_data and thread_data["error"]:
            return thread_data["error"]

        if not thread_data.get("thread"):
            return f"No messages found in chat with {contact_name}."

        if not thread_data.get("needs_reply"):
            return (
                f"Your last message in the chat with {contact_name} was sent by you — "
                f"no incoming message to reply to yet."
            )

        latest_incoming = thread_data["latest_incoming"]
        thread = thread_data["thread"]

        # Step 2: Load style profile (contact-specific → falls back to default)
        profile = get_profile(contact_name)

        # Step 3: Build prompts and call LLM
        system_prompt = _build_system_prompt(profile, contact_name)
        user_prompt = _build_user_prompt(thread, latest_incoming, contact_name)

        raw_response = _call_groq(system_prompt + "\n\n" + user_prompt, system="",
                                   max_tokens=600, temperature=0.85)

        # If the model merges system+user, try with proper roles
        if not raw_response:
            raw_response = _call_groq(
                prompt=user_prompt,
                system=system_prompt,
                max_tokens=600,
                temperature=0.85,
            )

        if not raw_response:
            return (
                "Could not generate reply drafts — Groq API unavailable. "
                "Check that GROQ_API_KEY is set in your environment."
            )

        # Step 4: Parse drafts
        drafts = _parse_drafts_from_response(raw_response)

        if not drafts:
            return f"LLM returned an unexpected format. Raw response:\n{raw_response[:500]}"

        # Step 5: Cache drafts for send_style_reply()
        _DRAFT_CACHE["contact"] = contact_name
        _DRAFT_CACHE["latest_incoming"] = latest_incoming
        _DRAFT_CACHE["drafts"] = drafts

        # Step 6: Format for display
        lines = [
            f"Replying to {contact_name}: \"{latest_incoming}\"\n",
            "Here are your reply options:\n",
        ]
        for d in drafts:
            lines.append(f"  {d['rank']}. {d['draft']}")

        lines.append(
            "\nSay 'send reply 1' (or 2 / 3) to send, "
            "or 'send style reply' to auto-pick the top draft."
        )

        return "\n".join(lines)

    except Exception as e:
        return f"Reply generator error: {str(e)}"


def get_cached_drafts() -> List[Dict]:
    """
    Returns the in-memory draft cache.
    Used by send_style_reply() in tools.py.
    """
    return _DRAFT_CACHE.get("drafts", [])


def get_cached_contact() -> str:
    """Returns the contact name from the last draft generation."""
    return _DRAFT_CACHE.get("contact", "")


def get_cached_incoming() -> str:
    """Returns the incoming message from the last draft generation."""
    return _DRAFT_CACHE.get("latest_incoming", "")


def send_style_reply(contact_name: str = "", draft_index: int = 1) -> str:
    """
    Picks draft N from the cache and sends it via confirm_whatsapp_send.

    Args:
        contact_name: Optional override. If empty, uses the cached contact.
        draft_index:  1-based index (1 = top draft, 2 = second, 3 = third).

    Returns:
        Human-readable result string.
    """
    drafts = get_cached_drafts()
    if not drafts:
        return (
            "No reply drafts in memory. "
            "Call generate_reply_draft(contact_name) first."
        )

    contact = contact_name.strip() or get_cached_contact()
    if not contact:
        return "I need a contact name to send the reply."

    # Clamp index
    idx = max(1, min(draft_index, len(drafts)))
    chosen = drafts[idx - 1]["draft"]

    # Record the sent reply for ongoing style learning
    try:
        from whatsapp_intelligence.style_profiler import record_sent_reply
        record_sent_reply(
            their_message=get_cached_incoming(),
            your_reply=chosen,
            contact_name=contact,
        )
    except Exception:
        pass  # Learning failure must never block sending

    # Delegate actual sending to whatsapp_smart.confirm_whatsapp_send
    try:
        from app.services.whatsapp_smart import confirm_whatsapp_send
        result = confirm_whatsapp_send(contact, chosen)
        # Clear cache after successful send
        _DRAFT_CACHE["drafts"] = []
        return result
    except ImportError:
        # Isolated test mode — just return what we'd send
        return (
            f"[TEST MODE] Would send to {contact}:\n\"{chosen}\"\n"
            "(Import whatsapp_smart to actually send)"
        )
    except Exception as e:
        return f"Send failed: {str(e)}"
