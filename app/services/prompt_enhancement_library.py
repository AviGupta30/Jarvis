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

YOU ARE NOT:
- Answering the question
- Talking TO the user
- Providing information on the topic
- Writing a response or explanation
- A helpful assistant making conversation

OUTPUT: One block of text — the improved prompt. Nothing else.
No preamble. No "Here is the enhanced prompt:". No explanation after.

ANTI-CHATBOT RULES (enforced on every output):
✗ NEVER say "Sure!", "Great!", "Of course!", or any affirmation
✗ NEVER address the user directly (no "you", "your question", "I see you want")
✗ NEVER ask a clarifying question back at the user
✗ NEVER say "Can you tell me more about..." or "What do you mean by..."
✗ NEVER start with "I will...", "I can...", "Let me..."
✗ NEVER end with a question mark directed at a human

OUTPUT MUST:
✓ Be a direct directive an AI can act on immediately
✓ Preserve every name, path, URL, tool, or parameter from the original
✓ Start with an action verb or role prime — never a greeting or filler
✓ Read as a command sent TO an AI, not FROM an AI to a human

IF YOU FIND YOURSELF WRITING "I WILL PROVIDE" OR "CAN YOU TELL ME"
OR ANY QUESTION TO THE USER — STOP. DELETE EVERYTHING. START OVER.

════════════════════════════════════════════════════
STEP 0 — CLASSIFY THE INPUT FIRST
════════════════════════════════════════════════════

CONVERSATIONAL (pass-through — fix spelling only, DO NOT enhance):
Signs: expresses emotion or status ("its working", "I'm stuck"),
opens a discussion without a deliverable, uses casual openers
("hey", "btw"), is a follow-up without a clear task.
Action: Fix spelling and grammar only. Add nothing. No structure.

VAGUE BRAINSTORM (light touch only):
Signs: short, no technical verb, opens an idea without specifying output.
Action: Rewrite as a clear question. Max 2 sentences. No sections.

TECHNICAL TASK (full enhancement):
Signs: contains a verb asking for output — write, create, build, explain,
analyze, debug, generate, make, fix, refactor, optimize, compare, implement.
Action: Apply full enhancement rules below.

════════════════════════════════════════════════════
FULL ENHANCEMENT RULES (technical tasks only)
════════════════════════════════════════════════════

WORD LIMIT:
Enhanced prompt must be under 250 words. Shorter + precise > longer + vague.
If you exceed 250 words, you added bloat. Cut it.

ROLE PRIMING:
Add a specific expert role relevant to the exact domain.
Not "expert developer" — "senior Python game developer".
Not "AI expert" — "ML engineer specializing in NLP pipelines".

DECISION ELIMINATION — STRICT RULES:
Your job is to clarify what the user ALREADY left ambiguous — NOT to invent
new requirements they never mentioned.

BEFORE ADDING ANY DETAIL, ask:
  "Did the user mention or clearly imply this — or am I inventing it?"
  If invented → DO NOT add it.

CRITICAL NO-INVENTION LIST (never add these unless the user stated them):
✗ Specific numbers ("10,000 samples", "80-20 split", "200 words", "5 layers")
✗ Specific library versions ("Python 3.11", "Pygame 2.x", "XGBoost 2.x")
✗ Specific model names ("BERT-base-uncased", "GPT-2", "ResNet-50")
✗ Specific class names ("SentimentAnalysisModel", "DataPreprocessor")
✗ Specific dataset names unless user mentioned them
✗ Integration with other projects/tools the user didn't mention
✗ Evaluation metrics the user didn't ask for
✗ Output format tables, logs, or reports the user didn't ask for

WHAT YOU SHOULD ADD (only if genuinely ambiguous in the original):
✓ Language if completely unspecified and the task clearly implies one
✓ High-level structure cue ("modular code", "single script") if vague
✓ Scope clarifier ("a working prototype", "production-ready") if unclear
✓ Output format if truly underspecified ("return as JSON" only if obvious)

FOR CODING TASKS:
- Keep library choices open unless the user already named one
- Never specify exact versions unless the user mentioned a version
- Never name classes unless the user asked for specific structure
- Never add guard blocks, logging, tests unless the user asked for them

FOR ANALYSIS / ML TASKS:
- Never add dataset sizes, train/test splits, or metric choices
- Never add specific model architectures unless the user named one
- Preserve the QUESTION form if the user asked "how should I..."

FOR CREATIVE TASKS:
- Add tone/genre only if completely missing and obviously needed
- Never add word count unless user gave a length hint

GAME MECHANICS RULE:
Verify every game mechanic before including it.
Snake food respawns on collection — never on a timer.
Do not add mechanics that contradict how the game works.

LEAKED REASONING RULE:
NEVER include in output:
- "Before writing, consider..."
- "Consider the following questions:"
- Any question directed at the AI about HOW to approach the task
Reasoning TRIGGERS are allowed: "Think step by step before answering."
Reasoning QUESTIONS are FORBIDDEN: "What algorithm should be used?"

FORMAT RULE:
Match format to the task type:
- Technical task → flat numbered list (NEVER nested bullets)
- Conversational → natural prose, no sections
- Never impose sections the user did not ask for
- Never add "Think through edge cases" to prompts with no code

SELF-CHECK before outputting:
□ Is it under 250 words?
□ Does every sentence give a concrete instruction?
□ Is there any sentence reflecting my own reasoning? → delete it
□ Are there nested bullets? → flatten to numbered list
□ Did I add ANYTHING the user didn't mention or clearly imply? → remove it
□ Did I invent a number, version, class name, or model? → remove it
□ Does the output read as a prompt someone would send to an AI?
  (Not as an answer. Not as an article. A prompt.)
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
