"""
prompt_enhancement_library.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
All prompt engineering logic for the Jarvis Prompt Enhancer.

Fixes implemented (per bug report v1.0):
  A1 — Job guard at top of system prompt
  A2 — PROJECT_CONTEXT injected into every enhancement call
  A3 — Hallucination detector with fallback
  B1 — 3-way input classifier (conversational / vague / technical)
  B2 — 250-word cap + leaked-reasoning stripper
  B3 — Injection boundary rule + game mechanic sanity check
  B4 — Removed hardcoded format templates; format rule added
  B5 — Decision-elimination checklist for code tasks
"""

# ─────────────────────────────────────────────────────────────────────────────
# PROJECT CONTEXT  (injected into every enhancement call — not in the output)
# ─────────────────────────────────────────────────────────────────────────────
PROJECT_CONTEXT = """
The user is building a personal AI OS agent called Jarvis.
It is a Python-based ReAct agent running on Windows 11.

ALREADY IMPLEMENTED:
- Voice I/O: Whisper STT + ElevenLabs TTS (Hinglish support)
- OS Control: volume, clipboard, keyboard simulation, app launch
- Window Manager: focus, snap, maximize via win32gui + pygetwindow
- UIA Engine: pywinauto accessibility tree walker, no mouse needed
- Web Search: DuckDuckGo + BeautifulSoup scraper + Wikipedia
- Communication: WhatsApp automation, Windows Copilot handoff
- Memory: ChromaDB vector store with fastembed ONNX embeddings
- Presentation: PPTX generator
- Prompt Enhancer: this feature, using Groq as LLM backend
- ReAct Planner: multi-step Thought → Action → Observation loop
- Overlay: floating Tkinter prompt-enhancer popup (Ctrl+Space)

LLM BACKEND: Groq (Llama 3.3 70B versatile)
LANGUAGE: Python 3.11+, Windows-only

When the user refers to "Jarvis", "the agent", "the system",
or "my project" — they mean THIS system described above.
Never assume they mean Iron Man's AI, Zuckerberg's home project,
or any other external tool or fictional AI.
"""

# ─────────────────────────────────────────────────────────────────────────────
# SYSTEM PROMPT  (complete rewrite — job guard FIRST, always)
# ─────────────────────────────────────────────────────────────────────────────
ENHANCEMENT_SYSTEM_PROMPT = """
════════════════════════════════════════════════════
IDENTITY: INTERNAL PROMPT OPTIMIZER — NOT A CHATBOT
════════════════════════════════════════════════════

YOU ARE AN INTERNAL TRANSLATION ENGINE.
Your job: turn a messy human prompt into a precise, constraint-driven
instruction that an AI can execute perfectly.

OUTPUT: One block of text — the improved prompt. Nothing else.
No preamble. No "Here is the enhanced prompt:". No explanation after.

ANTI-CHATBOT RULES:
✗ NEVER say "Sure!", "Great!", "Of course!", or any affirmation
✗ NEVER address the user directly (no "you", "your question")
✗ NEVER ask a clarifying question back at the user
✗ NEVER start with "I will...", "I can...", "Let me..."
✗ NEVER end with a question mark directed at a human

IF YOU FIND YOURSELF WRITING "I WILL PROVIDE" OR ASKING THE USER A QUESTION
— STOP. DELETE EVERYTHING. START OVER.

════════════════════════════════════════════════════
CRITICAL: PROJECT CONTEXT IS BACKGROUND KNOWLEDGE ONLY
════════════════════════════════════════════════════

If PROJECT CONTEXT is provided, it is your internal reference ONLY.
It tells you what system the user is working on.

YOU MUST NEVER:
✗ List, enumerate, or paraphrase the existing components from the context
✗ Mention "Python 3.11", "Groq LLM", "ChromaDB", "FastAPI" etc. in the output
   UNLESS the user explicitly named those in their raw prompt
✗ Include a summary of what the system already does
✗ Use the context as a description to inject into the prompt

YOU SHOULD:
✓ Use the context ONLY to understand the domain deeply
✓ Use it to write SMARTER constraints and BETTER role primes
✓ Reference it silently — the output must look like the user wrote it,
   not like an agent dumped a spec sheet

════════════════════════════════════════════════════
FULL ENHANCEMENT RULES
════════════════════════════════════════════════════

WORD LIMIT:
Enhanced prompt must be under 250 words. Shorter + precise > longer + vague.

ROLE PRIMING TEMPLATE:
Always open with a role prime using this format:
  "Act as [specific expert role] for [specific system/domain]."

Examples:
  "Act as the Core System Architect for [system name]."
  "Act as a senior ML engineer specializing in NLP classification."
  "Act as a game developer building a classic Snake game."

The role prime MUST be specific to the exact task — never generic like
"Act as an expert" or "As an AI assistant".

FEATURE / SUGGESTION REQUESTS:
When the user asks for ideas, features, or improvements to add to a system:
  1. Open with: "Act as [expert role] for [the user's system]."
  2. Define the task precisely: "Generate a prioritized list of [N] advanced,
     non-generic [features/improvements] that [specific goal]."
  3. Add 2-3 architectural constraints derived from the domain
     (e.g. "must leverage existing [relevant component]",
          "must not require external APIs",
          "must integrate with the current [architecture]")
  4. End with an output directive (see OUTPUT DIRECTIVE below)

NO-INVENTION RULE:
BEFORE ADDING ANY DETAIL, ask:
  "Did the user mention or clearly imply this — or am I inventing it?"
  If invented → DO NOT add it.

NEVER add these unless the user stated them:
✗ Specific numbers ("10,000 samples", "80-20 split")
✗ Specific versions ("Python 3.11", "Pygame 2.x")
✗ Specific model/class/dataset names the user didn't mention
✗ Evaluation metrics, logging, test cases the user didn't ask for
✗ Any component names from PROJECT CONTEXT unless user named them

OUTPUT DIRECTIVE RULE:
Every enhanced technical prompt MUST end with a clear output format instruction.
Template: "Output [format]. Omit all [type of fluff]."

Examples:
  "Output as a numbered technical specification. Omit introductions."
  "Output clean, modular code with no placeholder comments."
  "Output a direct answer with examples. No preamble."

FORMAT RULE:
- Technical task → role prime first, then task, then constraints, then output directive
- Conversational → natural prose, no sections
- Never impose nested bullets

LEAKED REASONING RULE:
NEVER include:
- "Before writing, consider..."
- Any question directed at the AI about HOW to approach the task

SELF-CHECK before outputting:
□ Does it start with "Act as [specific role]"?
□ Does it end with an output directive ("Output as X. Omit Y.")?
□ Is it under 250 words?
□ Did I mention any component from PROJECT CONTEXT the user didn't name? → remove it
□ Did I invent a number, version, class name, or model? → remove it
□ Does the output read as a command TO an AI, not a chatbot response FROM one?
"""


# ─────────────────────────────────────────────────────────────────────────────
# CLASSIFIER
# ─────────────────────────────────────────────────────────────────────────────
def classify_prompt(raw: str) -> str:
    """
    Returns: 'conversational' | 'vague' | 'technical'
    """
    raw_lower = raw.lower()
    word_count = len(raw.split())

    TECHNICAL_VERBS = [
        "write", "create", "build", "make", "generate", "code",
        "implement", "develop", "design", "fix", "debug", "explain",
        "analyze", "compare", "summarize", "refactor", "optimize",
        "calculate", "convert", "translate", "render", "find",
        "search", "list", "give me a list", "show me how",
        # Request / recommendation verbs (e.g. "add features", "suggest ideas")
        "add", "suggest", "recommend", "tell me", "give me",
        "what should i", "what can i", "what features", "what more",
        "how should i", "how do i", "what are the best",
    ]
    CONVERSATIONAL_SIGNALS = [
        "its working", "it's working", "that's great", "this is great",
        "finally working", "i'm stuck", "not working", "help me think",
        "what do you think", "let's talk", "let's think",
        "we need to think", "what should we", "any ideas", "thoughts?",
        "hey", "btw", "by the way", "just wanted to", "quick question",
        "how are you", "what's up", "checking in", "it works",
        "i think", "we should", "can we", "should we",
    ]

    has_technical_verb = any(v in raw_lower for v in TECHNICAL_VERBS)
    has_conversational = any(s in raw_lower for s in CONVERSATIONAL_SIGNALS)

    if has_conversational and not has_technical_verb:
        return "conversational"
    if has_technical_verb and word_count >= 4:
        return "technical"
    if word_count < 15 and not has_technical_verb:
        return "vague"

    return "technical"  # safe default


# ─────────────────────────────────────────────────────────────────────────────
# HALLUCINATION DETECTOR
# ─────────────────────────────────────────────────────────────────────────────
# HALLUCINATION DETECTOR
# ─────────────────────────────────────────────────────────────────────────────
FACTUAL_INJECTION_SIGNALS = [
    "is a real-life",
    "was developed by",
    "was created by",
    "is a fictional",
    "in the marvel",
    "tony stark",
    "zuckerberg",
    "according to",
    "historically",
    "in reality",
    "fun fact",
    "i will provide",
    "here is information about",
    "here are some",
    "as an ai",
    # Chatbot-mode signals
    "sure!",
    "great!",
    "of course!",
    "absolutely!",
    "can you tell me more",
    "what do you mean by",
    "i see you want",
    "it sounds like you",
    "it seems like you",
    "happy to help",
    "i'd be happy",
    "i would be happy",
    "let me know if",
    "feel free to",
]

def check_for_hallucination(enhanced: str) -> bool:
    """Returns True if hallucination or chatbot-mode signals are detected."""
    lower = enhanced.lower()
    return any(sig in lower for sig in FACTUAL_INJECTION_SIGNALS)


# ─────────────────────────────────────────────────────────────────────────────
# CHATBOT FILLER STRIPPER  (Python-level safety net)
# ─────────────────────────────────────────────────────────────────────────────
_CHATBOT_OPENERS = [
    "sure!", "sure,", "great!", "of course!", "absolutely!",
    "happy to help", "i'd be happy", "i would be happy",
    "i can help", "i will help", "let me help",
    "you're looking", "you are looking", "it sounds like", "it seems like",
]

def strip_chatbot_filler(text: str) -> str:
    """
    If the output starts with a chatbot filler opener, strip the first sentence.
    If the output ends with a question mark (user-directed question), strip the
    last sentence.
    """
    stripped = text.strip()
    lower = stripped.lower()

    # Strip chatbot opener sentence
    for opener in _CHATBOT_OPENERS:
        if lower.startswith(opener):
            # Remove everything up to the first sentence break
            for sep in ['. ', '! ', '\n']:
                idx = stripped.find(sep)
                if idx != -1:
                    stripped = stripped[idx + len(sep):].strip()
                    lower = stripped.lower()
                    break
            break

    # Strip trailing user-directed question
    if stripped.endswith('?'):
        lines = [s.strip() for s in stripped.replace('\n', ' ').split('.') if s.strip()]
        if len(lines) > 1:
            stripped = '. '.join(lines[:-1]).strip()
            if not stripped.endswith('.'):
                stripped += '.'

    return stripped


# ─────────────────────────────────────────────────────────────────────────────
# LEAKED REASONING STRIPPER
# ─────────────────────────────────────────────────────────────────────────────
LEAKED_PATTERNS = [
    "before writing the final answer, consider",
    "consider the following questions",
    "consider the following",
    "think about the following",
    "here is the enhanced prompt",
    "enhanced version of",
    "the following enhanced",
    "note that",
    "keep in mind that",
    "it's worth noting",
    "it is worth noting",
]

def strip_leaked_reasoning(text: str) -> str:
    """Cut the output at the first leaked-reasoning pattern found."""
    text_lower = text.lower()
    for pattern in LEAKED_PATTERNS:
        idx = text_lower.find(pattern)
        if idx != -1:
            text = text[:idx].strip()
            text_lower = text.lower()
    return text


# ─────────────────────────────────────────────────────────────────────────────
# INJECTION / BLOAT VALIDATOR  (kept from v1 + updated)
# ─────────────────────────────────────────────────────────────────────────────
import re as _re

_VERSION_RE = _re.compile(r'\bpython\s+3\.\d+\b', _re.IGNORECASE)
_NUMBER_RE  = _re.compile(r'\b\d[\d,]+\b')

def validate_enhancement(raw: str, enhanced: str) -> tuple[str, list[str]]:
    """
    Validate the enhanced prompt for common failure modes.
    Returns (possibly_cleaned_text, list_of_warnings).
    """
    warnings = []
    result = enhanced

    # Word-count cap
    if len(enhanced.split()) > 250:
        warnings.append(
            f"BLOAT: Enhanced is {len(enhanced.split())} words "
            f"(limit 250). Likely over-engineered."
        )

    # Injected requirements
    injected_flags = [
        ("logging",               "logging"     not in raw.lower()),
        ("test cases",            "test"        not in raw.lower()),
        ("performance",           "performance" not in raw.lower()
                                  and "optim"   not in raw.lower()),
        ("debugging statements",  "debug"       not in raw.lower()),
    ]
    for term, was_injected in injected_flags:
        if was_injected and term in enhanced.lower():
            warnings.append(f"INJECTED REQUIREMENT: '{term}' not in original.")

    # Injected Python version strings (e.g. "Python 3.11") not in original
    if _VERSION_RE.search(enhanced) and not _VERSION_RE.search(raw):
        warnings.append("INJECTED VERSION: explicit Python version not in original.")

    # Injected bare large numbers not in original (e.g. "10,000", "80")
    enh_nums = set(_NUMBER_RE.findall(enhanced))
    raw_nums = set(_NUMBER_RE.findall(raw))
    new_nums = enh_nums - raw_nums
    if new_nums:
        warnings.append(f"INJECTED NUMBERS: {new_nums} not in original prompt.")

    # Nested bullets
    deep_nests = [
        ln for ln in enhanced.split("\n")
        if ln.startswith("   *") or ln.startswith("      ")
    ]
    if len(deep_nests) > 3:
        warnings.append(
            f"NESTED BULLETS: {len(deep_nests)} deeply nested lines found."
        )

    return result, warnings


# ─────────────────────────────────────────────────────────────────────────────
# DOMAIN DETECTOR  (kept for the header label)
# ─────────────────────────────────────────────────────────────────────────────
DOMAIN_KEYWORDS = {
    "coding": [
        "code", "function", "debug", "error", "python", "javascript",
        "class", "api", "bug", "script", "implement", "write a", "fix",
        "refactor", "optimize", "sql", "build", "algorithm", "game",
    ],
    "creative": [
        "story", "poem", "essay", "blog", "character", "plot",
        "fiction", "creative", "describe", "compose", "draft",
    ],
    "analysis": [
        "analyze", "compare", "explain", "how does", "why does",
        "difference between", "pros and cons", "evaluate", "assess",
        "summarize", "critique", "review",
    ],
    "research": [
        "what is", "what are", "find", "list", "tell me about",
        "information about", "history of", "overview of", "research",
    ],
    "business": [
        "business", "strategy", "marketing", "pitch", "proposal",
        "email", "report", "presentation", "startup", "plan",
    ],
}

def detect_domain(prompt: str) -> str:
    prompt_lower = prompt.lower()
    scores = {domain: 0 for domain in DOMAIN_KEYWORDS}
    for domain, keywords in DOMAIN_KEYWORDS.items():
        for kw in keywords:
            if kw in prompt_lower:
                scores[domain] += 1
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "general"
