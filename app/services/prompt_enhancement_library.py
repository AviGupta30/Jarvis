"""
prompt_enhancement_library.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Prompt text + validators for the Jarvis Prompt Enhancer.

Design (v2, "faithful rewrite"):
  - The enhancer rewrites the user's prompt so another AI (ChatGPT, Claude,
    Gemini, Copilot, a coding agent…) gives a better answer — WITHOUT adding
    things the user didn't ask for (tech stack, implementation steps, invented
    requirements). The receiving AI decides the "how".
  - Pasted code / logs (``` fenced blocks) are swapped for [[BLOCK_n]]
    placeholders before the LLM call and restored afterwards, so they are
    never paraphrased.
  - Output guards: chatbot/answering signals and bloat trigger one stricter
    retry, then a fallback to the user's original text.
"""

import re as _re

# ─────────────────────────────────────────────────────────────────────────────
# PROJECT CONTEXT  (only injected when the prompt explicitly says "jarvis")
# ─────────────────────────────────────────────────────────────────────────────
PROJECT_CONTEXT = """
"Jarvis" is the user's own personal AI assistant for Windows 11: a Python
FastAPI backend with a React UI and a voice agent, using Groq LLMs, tool
calling (OS control, WhatsApp, web search, PPT generation, memory) and a
multi-step planner. When the user says "Jarvis" they mean THIS project,
never Iron Man's AI or any other product.
"""

# ─────────────────────────────────────────────────────────────────────────────
# SYSTEM PROMPT
# ─────────────────────────────────────────────────────────────────────────────
ENHANCEMENT_SYSTEM_PROMPT = """
You rewrite a user's rough prompt into a clearer, stronger prompt that they will send to another AI assistant (ChatGPT, Claude, Gemini, Copilot, a coding agent, etc.). You are NOT that assistant: never answer, solve, or start doing the task yourself.

GOAL
The rewritten prompt must get a noticeably better answer than the original because it is unambiguous, says what the user actually wants, and says what a good result looks like, while asking for exactly the same thing.

DO
- Keep the user's intent, scope and every concrete detail (names, numbers, files, code, errors, links, constraints, tone). Never drop information.
- Fix spelling, grammar and messy phrasing. Hinglish or broken English becomes clear English (keep names and quoted text as they are).
- Make the implicit explicit: state the real goal and what the response should contain.
- When the user asks for something to be built or written, describe WHAT it should do or be: the standard behaviour anyone would expect from the thing they named, plus a quality bar (complete, working, polished, concise, ...).
- Keep the request type. A question stays a question: "how do I ..." stays a how-to/explanation request and never becomes "Build ...". A request to write or build stays that.
- Keep the user's point of view ("I", "my", "me").
- Scale the length to the input: a one-line prompt becomes about 2 to 5 sentences; a long prompt gets tightened and organised, never padded. Stay under 150 words, not counting text the user supplied.
- Write plain prose. Use a short list only when the user gave several separate requirements.

DO NOT ADD
- Technology choices: programming languages, frameworks, libraries, engines, tools, platforms, file structure, architecture, databases or APIs, unless the user named them. The receiving AI decides how to do it.
- Implementation steps, algorithms, step-by-step build plans or instructions on how to build it.
- New features, requirements, numbers, versions, deadlines, audiences or facts the user did not state or clearly imply.
- Role-play openers ("Act as ...", "You are an expert ..."), greetings, "Please" padding, meta-commentary or sign-offs.
- Headings, markdown formatting, quotes around the output, or labels such as "Enhanced prompt:".
- Questions back to the user. If a detail is missing, do not invent it: leave a placeholder like [topic] or ask the AI to state its assumptions.

SPECIAL CASES
- Casual chat, greetings or feedback (e.g. "thanks it works"): only fix spelling and grammar.
- Already clear and specific: make minimal edits.
- Placeholders like [[BLOCK_1]] stand for code or text the user pasted. Keep every placeholder exactly once, unchanged, where it belongs.

OUTPUT: only the rewritten prompt text, nothing before or after it.

EXAMPLES

Input: create a snake game
Output: Create a complete, playable Snake game. The snake moves continuously and the player steers it, it grows each time it eats food, and the game ends when it hits a wall or itself. Show the current score and let me restart after a game over. Make sure it is fully working.

Input: how do i make my website load faster
Output: How can I make my website load faster? Explain how to find out what is slowing it down and the most effective fixes for each cause, starting with the changes that usually make the biggest difference.

Input: write email to my professor asking for extension on assignment bcoz i was sick
Output: Write a short, polite email to my professor asking for an extension on my assignment because I was sick. Briefly explain the situation, keep a respectful tone, and ask for a new deadline. Use placeholders for names, the course and dates.

Input: fix this error [[BLOCK_1]]
Output: Help me fix this error. Explain what is causing it, then give me the corrected code or the exact steps to resolve it.

[[BLOCK_1]]

Input: explain recursion
Output: Explain recursion clearly: what it is, how a recursive function works (base case and recursive case), and when it is a better choice than a loop. Include one simple example.

Input: thanks bro it works now
Output: Thanks, it works now.
"""

RETRY_REMINDER = (
    "Your previous output broke the rules (it answered the prompt, talked to the user, "
    "or added things the user never asked for, or was too long). Rewrite the ORIGINAL "
    "prompt again: same request, clearer wording, nothing invented, no tech stack or "
    "implementation steps, under 150 words. Output only the rewritten prompt."
)


# ─────────────────────────────────────────────────────────────────────────────
# CODE-BLOCK PROTECTION
# ─────────────────────────────────────────────────────────────────────────────
_FENCE_RE = _re.compile(r"```.*?```", _re.DOTALL)


def protect_blocks(raw: str) -> tuple[str, list[str]]:
    """Replace ``` fenced blocks with [[BLOCK_n]] placeholders."""
    blocks: list[str] = []

    def _sub(m):
        blocks.append(m.group(0))
        return f"[[BLOCK_{len(blocks)}]]"

    return _FENCE_RE.sub(_sub, raw), blocks


def restore_blocks(text: str, blocks: list[str]) -> str:
    """Put protected blocks back; append any the model dropped."""
    for i, block in enumerate(blocks, 1):
        tag = f"[[BLOCK_{i}]]"
        if tag in text:
            text = text.replace(tag, block, 1).replace(tag, "")
        else:
            text = text.rstrip() + "\n\n" + block
    return text


# ─────────────────────────────────────────────────────────────────────────────
# OUTPUT CLEANUP + GUARDS
# ─────────────────────────────────────────────────────────────────────────────
_LABEL_RE = _re.compile(
    r"^\s*(\*\*)?\s*(enhanced|improved|rewritten|refined|optimi[sz]ed)?\s*prompt\s*(\*\*)?\s*:\s*(\*\*)?\s*",
    _re.IGNORECASE,
)
_OUTPUT_LABEL_RE = _re.compile(r"^\s*output\s*:\s*", _re.IGNORECASE)


def clean_output(text: str) -> str:
    """Strip labels, wrapping quotes and code fences the model sometimes adds."""
    t = (text or "").strip()
    # gpt-oss likes non-breaking hyphens / narrow spaces; they look odd in chat boxes
    t = t.replace("‑", "-").replace(" ", " ").replace(" ", " ")
    t = _LABEL_RE.sub("", t, count=1)
    t = _OUTPUT_LABEL_RE.sub("", t, count=1).strip()
    if len(t) >= 2 and t[0] == t[-1] and t[0] in "\"'“”`":
        t = t[1:-1].strip()
    if t.startswith("“") and t.endswith("”"):
        t = t[1:-1].strip()
    return t


# Phrases that mean the model answered / chatted instead of rewriting.
# START signals only count at the very beginning of the output.
CHATBOT_START_SIGNALS = [
    "sure", "great!", "of course", "absolutely", "certainly", "okay,", "ok,",
    "here is", "here's", "below is",
]
CHATBOT_SIGNALS = [
    "happy to help", "i'd be happy", "i would be happy",
    "enhanced prompt", "rewritten prompt", "improved prompt",
    "as an ai", "i see you want", "it sounds like you", "it seems like you",
    "can you tell me more", "what do you mean by", "tony stark", "in the marvel",
]


def check_for_hallucination(enhanced: str, raw: str = "") -> bool:
    """True if the output looks like a chatbot reply rather than a rewritten prompt.
    Signals that already appear in the user's own prompt are ignored."""
    lower = enhanced.lower().lstrip()
    raw_lower = raw.lower().lstrip()
    if any(lower.startswith(s) and not raw_lower.startswith(s) for s in CHATBOT_START_SIGNALS):
        return True
    return any(sig in lower and sig not in raw_lower for sig in CHATBOT_SIGNALS)


def is_bloated(raw: str, enhanced: str) -> bool:
    """True if the rewrite is far longer than the input warrants."""
    raw_words = len(raw.split())
    enh_words = len(enhanced.split())
    return enh_words > max(170, int(raw_words * 2.5) + 60)


# ─────────────────────────────────────────────────────────────────────────────
# DOMAIN DETECTOR (used for the chat header label only)
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
