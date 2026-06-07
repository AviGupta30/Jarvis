"""
prompt_enhancement_library.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Domain-specific system prompts and detection logic for the prompt enhancer.
"""

DOMAIN_KEYWORDS = {
    "coding": [
        "code", "function", "debug", "error", "python", "javascript",
        "class", "api", "bug", "script", "implement", "write a", "fix",
        "refactor", "optimize", "sql", "build", "algorithm"
    ],
    "creative": [
        "write", "story", "poem", "essay", "blog", "script", "character",
        "plot", "fiction", "creative", "describe", "compose", "draft"
    ],
    "analysis": [
        "analyze", "compare", "explain", "how does", "why does",
        "difference between", "pros and cons", "evaluate", "assess",
        "summarize", "critique", "review"
    ],
    "research": [
        "what is", "what are", "find", "list", "give me", "tell me about",
        "information about", "history of", "overview of", "research"
    ],
    "business": [
        "business", "strategy", "marketing", "pitch", "proposal",
        "email", "report", "presentation", "startup", "plan"
    ],
}

def detect_domain(prompt: str) -> str:
    """Detect the domain of a prompt based on keyword matching."""
    prompt_lower = prompt.lower()
    scores = {domain: 0 for domain in DOMAIN_KEYWORDS}
    for domain, keywords in DOMAIN_KEYWORDS.items():
        for kw in keywords:
            if kw in prompt_lower:
                scores[domain] += 1
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "general"

ENHANCEMENT_SYSTEM_PROMPT = """
You are an elite prompt engineer. Transform the raw prompt into a 
high-performance version for a code-generation or analysis AI.

CORE JOB: Identify every decision the AI would make randomly if left 
unspecified, then specify those decisions explicitly with concrete values.
The job of enhancement is decision elimination, not requirement addition.

ABSOLUTE RULES:
1. Output ONLY the enhanced prompt. Zero preamble. Zero explanation.
2. Preserve user intent exactly. Never invent constraints that contradict the core task (like forcing a complex game into a "single function").
3. Your internal reasoning must NEVER appear in the output.
4. Shorter is better. Replace vague words with precise ones.
5. Use numbered lists or bullet points, but DO NOT use nested bullet hierarchies.
6. Never say "appropriate" or "suitable" — pick a concrete value.
7. Never say "standard" or "typical" — name the specific thing.

WHAT TO ADD (and nothing more):

CODING prompts — refine by adding:
  • A specific, domain-relevant expert persona (e.g., "As a Python game developer," not just "As an expert developer").
  • For visual/game apps: Always specify exact dimensions (e.g., 600x600 pixels), speed/timing constants, and grid/pixel logic.
  • For structures: Always specify exact library + version hint, file/class structure, entry point format, and error/end state behavior.
  • Pick the most common reasonable default for any unstated decisions and state them explicitly with concrete values.
  • ONE reasoning trigger if the task is complex: "Think through edge cases before writing code."

ANALYSIS prompts — refine by adding:
  • A specific, domain-relevant expert persona.
  • Output structure (e.g., "Respond in 3 numbered sections: Context, Analysis, Conclusion").
  • Depth level (e.g., "Write for an advanced audience familiar with the topic").
  • "Use concrete examples."
  • Eliminate arbitrary decisions about format, tone, and depth.

CREATIVE prompts — refine by adding:
  • Exact genre, tone, POV, and word count.
  • A concrete stylistic rule (e.g., "Write in terse, Hemingway-style sentences" or "Show don't tell").
  • Concrete stakes or character constraints.

QUALITY CHECK before outputting:
  • Did you leave any arbitrary decisions (like window size) unspecified? If yes, specify them.
  • Are there nested bullet points? Flatten them.
  • Does the prompt contain vague padding? Remove it.
"""

def get_system_prompt(domain: str) -> str:
    """Returns the enhancement system prompt."""
    return ENHANCEMENT_SYSTEM_PROMPT

def validate_enhancement(raw: str, enhanced: str) -> tuple[str, list[str]]:
    """
    Catch common enhancement failures before the prompt is used.
    Returns (final_prompt, list_of_warnings).
    """
    warnings = []
    result = enhanced

    # ── Check 1: Length sanity ─────────────────────────────────────────
    if len(enhanced.split()) > len(raw.split()) * 3:
        warnings.append(
            f"BLOAT: Enhanced is {len(enhanced.split())} words vs "
            f"{len(raw.split())} original. Likely over-engineered."
        )

    # ── Check 2: Leaked reasoning patterns ────────────────────────────
    leaked_patterns = [
        "before writing the final answer, consider",
        "consider the following questions",
        "think about",
        "here is the enhanced prompt",
        "enhanced version",
        "the following enhanced",
        "note that",
    ]
    for pattern in leaked_patterns:
        if pattern.lower() in enhanced.lower():
            warnings.append(f"LEAKED REASONING: Found '{pattern}' in output.")
            # Auto-strip the leaked section
            idx = enhanced.lower().find(pattern.lower())
            result = enhanced[:idx].strip()

    # ── Check 3: Added requirements not in original ────────────────────
    injected_flags = [
        ("logging", "logging" not in raw.lower()),
        ("test cases", "test" not in raw.lower()),
        ("performance", "performance" not in raw.lower() 
                        and "optim" not in raw.lower()),
        ("debugging statements", "debug" not in raw.lower()),
    ]
    for term, was_injected in injected_flags:
        if was_injected and term in enhanced.lower():
            warnings.append(f"INJECTED REQUIREMENT: '{term}' not in original.")

    # ── Check 4: Nested bullets ────────────────────────────────────────
    lines = enhanced.split("\n")
    deep_nests = [l for l in lines if l.startswith("   *") 
                                   or l.startswith("      ")]
    if len(deep_nests) > 3:
        warnings.append(
            f"NESTED BULLETS: {len(deep_nests)} deeply nested lines found."
        )

    return result, warnings

