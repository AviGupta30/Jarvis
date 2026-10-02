"""
skill_prompt_enhancer.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Jarvis Prompt Enhancer (v2 — faithful rewrite).

Pipeline (enhance_prompt_text):
  1. protect_blocks()   ``` code/log blocks → [[BLOCK_n]] placeholders
  2. _call_groq()       one rewrite call (system prompt + few-shot in the library)
  3. clean_output()     strip labels / wrapping quotes
  4. guards             chatbot-reply or bloat → one stricter retry → fall back to original
  5. restore_blocks()   put the user's code back verbatim

Callers:
  - enhance_prompt(raw)        chat intercept + TOOL_REGISTRY; returns a labelled string, never raises
  - enhance_prompt_text(raw)   floating "Enhance" button; returns clean text, raises on API failure
"""

from groq import Groq
from app.core.config import settings
from app.services.prompt_enhancement_library import (
    ENHANCEMENT_SYSTEM_PROMPT,
    PROJECT_CONTEXT,
    RETRY_REMINDER,
    protect_blocks,
    restore_blocks,
    clean_output,
    check_for_hallucination,
    is_bloated,
    detect_domain,
)

_MODELS = ("openai/gpt-oss-120b", "openai/gpt-oss-20b")


# ─────────────────────────────────────────────────────────────────────────────
# Internal Groq caller (120b first, 20b if it fails / is rate-limited)
# ─────────────────────────────────────────────────────────────────────────────
def _call_groq(messages: list, temperature: float = 0.3, max_tokens: int = 2048) -> str:
    client = Groq(api_key=settings.GROQ_API_KEY)
    last_err = None
    for model in _MODELS:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                # gpt-oss reasoning tokens count against max_tokens, so keep headroom
                max_tokens=max_tokens,
                reasoning_effort="low",
            )
            content = (response.choices[0].message.content or "").strip()
            if content:
                return content
            last_err = RuntimeError(f"{model} returned an empty response")
        except Exception as e:
            last_err = e
            print(f"[Enhancer] {model} failed: {e}")
    raise last_err


def _is_how_to(raw: str) -> bool:
    lower = raw.lower()
    return any(s in lower for s in (
        "how should i", "how do i", "how to", "how can i", "what is the best way",
        "walk me through", "guide me", "explain how",
    ))


def _build_messages(masked: str) -> list:
    system = ENHANCEMENT_SYSTEM_PROMPT.strip()
    if "jarvis" in masked.lower():
        system += (
            "\n\nBACKGROUND (for understanding only, never mention its components "
            "unless the user did):\n" + PROJECT_CONTEXT.strip()
        )
    note = ""
    if _is_how_to(masked):
        note = "(This is a how-to question: it must stay a question, not become a build command.)\n"
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": f"{note}Input: {masked}\nOutput:"},
    ]


# ─────────────────────────────────────────────────────────────────────────────
# Core: clean enhanced text
# ─────────────────────────────────────────────────────────────────────────────
def enhance_prompt_text(raw_prompt: str) -> str:
    """Return the enhanced prompt as plain text (no header).
    Raises on Groq/API failure so UI callers can show an error; a bad
    rewrite that survives the retry falls back to the original prompt."""
    raw = (raw_prompt or "").strip()
    if not raw:
        return raw

    masked, blocks = protect_blocks(raw)
    messages = _build_messages(masked)

    enhanced = clean_output(_call_groq(messages))
    if check_for_hallucination(enhanced, masked) or is_bloated(masked, enhanced):
        print("[Enhancer] Rewrite rejected (chatbot/bloat) — retrying once.")
        retry = messages + [
            {"role": "assistant", "content": enhanced},
            {"role": "user", "content": RETRY_REMINDER},
        ]
        enhanced = clean_output(_call_groq(retry, temperature=0.1))
        if check_for_hallucination(enhanced, masked) or is_bloated(masked, enhanced):
            print("[Enhancer] Retry still rejected — returning the original prompt.")
            return raw

    return restore_blocks(enhanced, blocks).strip()


# ─────────────────────────────────────────────────────────────────────────────
# Public tool entry point — chat.py intercept + TOOL_REGISTRY
# ─────────────────────────────────────────────────────────────────────────────
def enhance_prompt(raw_prompt: str) -> str:
    """Enhance a prompt and return it under an **ENHANCED PROMPT (DOMAIN)** header."""
    try:
        enhanced = enhance_prompt_text(raw_prompt)
        domain = detect_domain(raw_prompt)
        return f"**ENHANCED PROMPT ({domain.upper()})**:\n\n{enhanced}"
    except Exception as e:
        return f"[Prompt Enhancer Error] {e}"
