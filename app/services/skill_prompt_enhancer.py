"""
skill_prompt_enhancer.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Jarvis Prompt Enhancer — complete rewrite (bug report v1.0 + intent fix)

Pipeline:
  STEP 0  classify_prompt()           →  conversational | vague | technical
  STEP 0b _detect_intent_type()       →  how_to | explanation | creation
  STEP 1  _call_groq()                →  raw enhanced text
  STEP 2  strip_leaked_reasoning() + validate_enhancement()
  STEP 3  check_for_hallucination()   →  fallback to _light_clean()
  STEP 4  return labelled result string

Key rules:
  - PROJECT_CONTEXT is ONLY injected when the prompt explicitly
    references Jarvis, the agent, or the user's project.
  - 'how should I / how do I / how to' prompts are NEVER converted
    into 'create / build / make' commands. Intent is preserved exactly.
"""

from groq import Groq
from app.core.config import settings
from app.services.prompt_enhancement_library import (
    ENHANCEMENT_SYSTEM_PROMPT,
    PROJECT_CONTEXT,
    classify_prompt,
    detect_domain,
    strip_leaked_reasoning,
    strip_chatbot_filler,
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
                "You are an internal text cleaner. "
                "Fix spelling and grammar only. "
                "Do NOT change the meaning, tone, or structure. "
                "Do NOT add anything new. "
                "Do NOT address the user. Do NOT ask questions. "
                "Output only the corrected text, nothing else."
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
                "You are an internal prompt translator. "
                "The input is a vague or incomplete human thought. "
                "Your job: rewrite it as a precise, direct instruction that an AI can act on immediately. "
                "\n\n"
                "STRICT RULES:\n"
                "- Output ONLY the rewritten prompt. Nothing else.\n"
                "- NEVER address the user (no 'you', 'your', 'I see you want')\n"
                "- NEVER ask a clarifying question back\n"
                "- NEVER say 'Sure!', 'Great!', 'Of course!' or any filler\n"
                "- NEVER start with 'I will...' or 'Let me...'\n"
                "- NEVER end with a question mark directed at a human\n"
                "- Preserve every specific name, tool, or term the user mentioned\n"
                "- Output must start with an action verb or expert role\n"
                "- Maximum 3 sentences. Be precise, not wordy."
            ),
        },
        {"role": "user", "content": raw},
    ]
    result = _call_groq(messages, temperature=0.2, max_tokens=200)
    return strip_chatbot_filler(result)


# ─────────────────────────────────────────────────────────────────────────────
# Intent-type detector — preserves question type
# ─────────────────────────────────────────────────────────────────────────────
def _detect_intent_type(raw: str) -> str:
    """
    Returns 'how_to' | 'creation' | 'explanation'
    Used to stop 'how should I...' being rewritten as 'Create a...'
    """
    lower = raw.lower().strip()
    HOW_TO_SIGNALS = [
        "how should i", "how do i", "how to", "how can i",
        "what is the best way", "what is a good way",
        "walk me through", "guide me", "explain how",
    ]
    if any(s in lower for s in HOW_TO_SIGNALS):
        return "how_to"
    CREATION_SIGNALS = [
        "write", "create", "build", "make", "generate", "implement",
        "develop", "code", "produce",
    ]
    if any(lower.startswith(s) or f" {s} " in f" {lower} " for s in CREATION_SIGNALS):
        return "creation"
    return "explanation"


# ─────────────────────────────────────────────────────────────────────────────
# Project-context relevance check
# ─────────────────────────────────────────────────────────────────────────────
JARVIS_KEYWORDS = [
    "jarvis", "my project", "the agent", "my agent",
    "my system", "the system", "our project",
]

def _is_jarvis_related(raw: str) -> bool:
    """Only inject PROJECT_CONTEXT when the prompt is explicitly about Jarvis."""
    lower = raw.lower()
    return any(kw in lower for kw in JARVIS_KEYWORDS)


# ─────────────────────────────────────────────────────────────────────────────
# Full technical enhancement
# ─────────────────────────────────────────────────────────────────────────────
def _full_enhance(raw: str) -> str:
    intent = _detect_intent_type(raw)

    # Build intent-preservation instruction
    if intent == "how_to":
        intent_rule = (
            "CRITICAL: The user's prompt is a HOW-TO question. "
            "Your enhanced output MUST remain a question or explanation request. "
            "Do NOT convert it into a 'Create...' or 'Build...' command. "
            "Preserve the question format exactly."
        )
    else:
        intent_rule = ""

    # Build system message — PROJECT_CONTEXT goes here (background knowledge)
    # so the LLM treats it as what it already knows, not content to output
    if _is_jarvis_related(raw):
        system_with_context = (
            ENHANCEMENT_SYSTEM_PROMPT.strip()
            + "\n\n"
            + "════════════════════════════════════════════════════\n"
            + "BACKGROUND KNOWLEDGE (INTERNAL USE ONLY — DO NOT OUTPUT)\n"
            + "════════════════════════════════════════════════════\n"
            + "You silently know the following about the user's system.\n"
            + "Use this ONLY to write a better role prime and smarter constraints.\n"
            + "NEVER list, quote, or paraphrase this in your output.\n\n"
            + PROJECT_CONTEXT.strip()
        )
    else:
        system_with_context = ENHANCEMENT_SYSTEM_PROMPT

    user_content = ""
    if intent_rule:
        user_content += f"{intent_rule}\n\n"
    user_content += f"RAW PROMPT TO ENHANCE:\n{raw}"

    messages = [
        {"role": "system", "content": system_with_context},
        {"role": "user",   "content": user_content.strip()},
    ]

    enhanced = _call_groq(messages, temperature=0.3, max_tokens=600)

    # Post-processing pipeline
    enhanced = strip_chatbot_filler(enhanced)
    enhanced = strip_leaked_reasoning(enhanced)
    enhanced, warnings = validate_enhancement(raw, enhanced)

    for w in warnings:
        print(f"[Enhancer Warning] {w}")

    # Hallucination safety net
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
