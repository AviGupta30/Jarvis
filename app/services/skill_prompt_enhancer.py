"""
skill_prompt_enhancer.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Jarvis Prompt Enhancer — complete rewrite (bug report v1.0)

Pipeline:
  STEP 0  classify_prompt()  →  conversational | vague | technical
  STEP 1  _call_groq()       →  raw enhanced text
  STEP 2  strip_leaked_reasoning() + validate_enhancement()
  STEP 3  check_for_hallucination() → fallback to _light_clean()
  STEP 4  return labelled result string
"""

from groq import Groq
from app.core.config import settings
from app.services.prompt_enhancement_library import (
    ENHANCEMENT_SYSTEM_PROMPT,
    PROJECT_CONTEXT,
    classify_prompt,
    detect_domain,
    strip_leaked_reasoning,
    validate_enhancement,
    check_for_hallucination,
)

# ─────────────────────────────────────────────────────────────────────────────
# Internal Groq caller
# ─────────────────────────────────────────────────────────────────────────────
def _call_groq(
    messages: list,
    temperature: float = 0.3,
    max_tokens: int = 600,
) -> str:
    client = Groq(api_key=settings.GROQ_API_KEY)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content.strip()


# ─────────────────────────────────────────────────────────────────────────────
# Light clean — conversational inputs (spelling/grammar only)
# ─────────────────────────────────────────────────────────────────────────────
def _light_clean(raw: str) -> str:
    messages = [
        {
            "role": "system",
            "content": (
                "Fix spelling and grammar only. "
                "Do not change the meaning, tone, or structure. "
                "Do not add anything. Output only the corrected text."
            ),
        },
        {"role": "user", "content": raw},
    ]
    return _call_groq(messages, temperature=0.1, max_tokens=200)


# ─────────────────────────────────────────────────────────────────────────────
# Vague enhance — surface the implicit question, max 2 sentences
# ─────────────────────────────────────────────────────────────────────────────
def _vague_enhance(raw: str) -> str:
    messages = [
        {
            "role": "system",
            "content": (
                "The user has written a vague or incomplete thought. "
                "Rewrite it as a clear, direct question or instruction "
                "they can send to an AI. Keep it conversational. "
                "Do not add formal structure, sections, or bullet points. "
                "Maximum 2 sentences. Output only the rewritten prompt."
            ),
        },
        {"role": "user", "content": raw},
    ]
    return _call_groq(messages, temperature=0.2, max_tokens=150)


# ─────────────────────────────────────────────────────────────────────────────
# Full technical enhancement
# ─────────────────────────────────────────────────────────────────────────────
def _full_enhance(raw: str) -> str:
    messages = [
        {
            "role": "system",
            "content": ENHANCEMENT_SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": (
                f"PROJECT CONTEXT (reference only — do not include "
                f"in the enhanced prompt):\n{PROJECT_CONTEXT}\n\n"
                f"RAW PROMPT TO ENHANCE:\n{raw}"
            ),
        },
    ]

    enhanced = _call_groq(messages, temperature=0.3, max_tokens=600)

    # Post-processing pipeline
    enhanced = strip_leaked_reasoning(enhanced)
    enhanced, warnings = validate_enhancement(raw, enhanced)

    for w in warnings:
        print(f"[Enhancer Warning] {w}")

    # Hallucination safety net — if the LLM answered instead of enhancing,
    # fall back to a light spelling/grammar pass on the original.
    if check_for_hallucination(enhanced):
        print("[Enhancer] Hallucination detected — returning cleaned original.")
        enhanced = _light_clean(raw)

    return enhanced


# ─────────────────────────────────────────────────────────────────────────────
# Public entry point — called by chat.py intercept
# ─────────────────────────────────────────────────────────────────────────────
def enhance_prompt(raw_prompt: str) -> str:
    """
    Main enhancement function. Classifies, routes, and returns a labelled result.
    The **ENHANCED PROMPT (TYPE):** header is used by chat.py / overlay to
    present the result to the user.
    """
    try:
        prompt_type = classify_prompt(raw_prompt)

        if prompt_type == "conversational":
            cleaned = _light_clean(raw_prompt)
            return f"**ENHANCED PROMPT (CONVERSATIONAL)**:\n\n{cleaned}"

        if prompt_type == "vague":
            clarified = _vague_enhance(raw_prompt)
            return f"**ENHANCED PROMPT (CLARIFIED)**:\n\n{clarified}"

        # Technical — full pipeline
        domain  = detect_domain(raw_prompt)
        enhanced = _full_enhance(raw_prompt)
        return f"**ENHANCED PROMPT ({domain.upper()})**:\n\n{enhanced}"

    except Exception as e:
        return f"[Prompt Enhancer Error] {e}"


# ─────────────────────────────────────────────────────────────────────────────
# Two-stage helper (kept for completeness — not used by main flow)
# ─────────────────────────────────────────────────────────────────────────────
def enhance_and_respond(raw_prompt: str) -> str:
    """
    Enhance the prompt then also generate the answer with it.
    (Stage 1: enhance  →  Stage 2: respond using enhanced prompt)
    """
    try:
        enhanced_block = enhance_prompt(raw_prompt)
        # Extract just the clean prompt (strip the header line)
        lines = enhanced_block.split("\n")
        clean_lines = [l for l in lines if not l.startswith("**ENHANCED PROMPT")]
        enhanced_clean = "\n".join(clean_lines).strip()

        answer = _call_groq(
            messages=[{"role": "user", "content": enhanced_clean}],
            temperature=0.7,
            max_tokens=2048,
        )

        return (
            f"ENHANCED PROMPT:\n{enhanced_clean}\n\n"
            f"{'─' * 60}\n\n"
            f"ANSWER:\n{answer}"
        )

    except Exception as e:
        return f"[Enhance+Respond Error] {e}"
