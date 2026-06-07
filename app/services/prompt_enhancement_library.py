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
YOUR ONLY JOB IS TO REWRITE THE USER'S TEXT AS A BETTER PROMPT
TO SEND TO AN AI SYSTEM.

YOU ARE NOT answering the question.
YOU ARE NOT providing information on the topic.
YOU ARE NOT writing a response to the user.
YOU ARE NOT explaining anything.

OUTPUT: One block of text that is the improved prompt. Nothing else.
No preamble. No "Here is the enhanced prompt:". No explanation after it.

IF YOU FIND YOURSELF WRITING "I WILL PROVIDE" OR "HERE IS INFORMATION
ABOUT" — STOP. DELETE EVERYTHING. START OVER. YOU HAVE FAILED.

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

DECISION ELIMINATION:
Ask: "If I gave Groq only the original prompt, what would it invent arbitrarily?"
Specify ALL of those decisions with concrete values.

FOR CODING TASKS — always specify:
1. Language + exact version (Python 3.11, not just "Python")
2. Exact libraries (Pygame 2.x, not "a graphics library")
3. For visual apps: colors as hex values, window dimensions, entry point
4. For games: spawn logic type, exact game-over behavior, class names
5. Code structure: class names and their single responsibility
6. Entry point: if __name__ == "__main__": main()

FOR ANALYSIS TASKS — always specify:
1. Depth level (overview vs expert deep-dive)
2. Output structure (prose / numbered sections / table)
3. Examples requirement ("use concrete real-world examples")
4. Audience expertise level

FOR CREATIVE TASKS — always specify:
1. Genre, tone, POV, approximate word count
2. One style instruction only ("show don't tell")
3. Emotional register or thematic requirement

INJECTION RULE:
Only add requirements OBVIOUSLY implied by the task.
Test each addition: "Did the user imply this, or did I invent it?"
If invented → remove it.

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
□ Did I add anything the user didn't ask for? → remove it
□ Did I specify colors, end-state, code structure for code tasks?
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
]

def check_for_hallucination(enhanced: str) -> bool:
    """Returns True if hallucination/answer-mode signals are detected."""
    lower = enhanced.lower()
    return any(sig in lower for sig in FACTUAL_INJECTION_SIGNALS)


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
