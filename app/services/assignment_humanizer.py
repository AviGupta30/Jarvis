"""
Jarvis Assignment Tool — Phase 3: Answer Humanizer
===================================================
STRICT ISOLATION: This module does NOT import from any other Jarvis tool module.
Uses only external libraries and standard Python.

Humanization Strategy (tried in priority order):
  1. paraphraser.io    — free, no login, clean DOM, handles long text
  2. scribbr.com       — free, no login, academic-focused paraphrasing
  3. quillbot.com      — free tier up to 10K chars, high quality
  4. Groq LLM rewrite  — always works, preserves technical content perfectly
                         Uses "write like a university student" system prompt
                         Model chain: llama-3.3-70b → llama-3.1-8b → gemma2-9b

Text is automatically chunked at sentence boundaries so long answers
don't exceed site character limits. Chunks are reassembled after humanization.

Technical content (formulas, equations, variable names) is preserved exactly
using a pre/post substitution pattern — placeholders replace them before
humanizing, then they are restored in the final output.

Public Functions:
  humanize_text(text, force_site=None)    -- humanize a single text block
  humanize_all_answers(qa_json)           -- batch humanize QA_JSON from Phase 2
"""

import re
import json
import time
import base64
from pathlib import Path
from groq import Groq
from app.core.config import settings

_groq = Groq(api_key=settings.GROQ_API_KEY)

# Persistent browser profile (shared with Phase 2)
_BROWSER_PROFILE = Path.home() / ".jarvis_ai_browser"

_REALISTIC_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)

# ── Humanizer Site Configurations ─────────────────────────────────────────────
_HUMANIZER_SITES = {
    "paraphraser": {
        "name": "Paraphraser.io",
        "url": "https://www.paraphraser.io/",
        "max_chars": 5000,
        "input_selectors": [
            "textarea#inputText",
            "textarea[placeholder*='Enter']",
            "textarea[placeholder*='Paste']",
            "textarea[placeholder*='Type']",
            ".input-area textarea",
            "textarea",
        ],
        "button_selectors": [
            "button[id*='paraphrase']",
            "button[class*='paraphrase']",
            "button:has-text('Paraphrase')",
            "button:has-text('Humanize')",
            "input[type='submit']",
        ],
        "output_selectors": [
            "textarea#outputText",
            ".output-area textarea",
            ".result-text textarea",
            "textarea:nth-of-type(2)",
        ],
        "wait_seconds": 20,
        "needs_login": False,
    },
    "scribbr": {
        "name": "Scribbr",
        "url": "https://www.scribbr.com/paraphrasing-tool/",
        "max_chars": 6000,
        "input_selectors": [
            "textarea[placeholder*='Paste']",
            "textarea[placeholder*='Enter']",
            ".editor-input textarea",
            "div[contenteditable='true']",
            "textarea",
        ],
        "button_selectors": [
            "button:has-text('Paraphrase')",
            "button[class*='paraphrase']",
            "button[type='submit']",
            "button:has-text('Rewrite')",
        ],
        "output_selectors": [
            ".editor-output textarea",
            ".paraphrase-output",
            "div[contenteditable='true']:nth-of-type(2)",
        ],
        "wait_seconds": 25,
        "needs_login": False,
    },
    "quillbot": {
        "name": "QuillBot",
        "url": "https://quillbot.com/",
        "max_chars": 10000,
        "input_selectors": [
            "#paraphraser-input-box div[contenteditable='true']",
            "div[contenteditable='true'][data-testid='input-editor']",
            "div[contenteditable='true']",
        ],
        "button_selectors": [
            "button[data-testid='paraphrase-button']",
            "button:has-text('Paraphrase')",
            "#paraphrase-button",
        ],
        "output_selectors": [
            "#paraphraser-output-box div[contenteditable='true']",
            "div[contenteditable='true'][data-testid='output-editor']",
            "div[contenteditable='true']:nth-of-type(2)",
        ],
        "wait_seconds": 20,
        "needs_login": False,
    },
}

# ── Technical Content Preservation ────────────────────────────────────────────
# These patterns are replaced with placeholders before humanizing so the
# humanizer doesn't corrupt formulas, equations, and variable names.

_PRESERVE_PATTERNS = [
    # Math/LaTeX
    (re.compile(r"\$\$.*?\$\$", re.DOTALL), "MATH_BLOCK"),
    (re.compile(r"\$[^$\n]+?\$"), "MATH_INLINE"),
    # Code
    (re.compile(r"```.*?```", re.DOTALL), "CODE_BLOCK"),
    (re.compile(r"`[^`\n]+`"), "CODE_INLINE"),
    # Equations
    (re.compile(r"(?:Eq\.|Equation)\s*\([0-9]+\)", re.IGNORECASE), "EQ_REF"),
    # Scientific / Units (e.g. 5X10-9 W/Hz, 10mV)
    (re.compile(r"\b\d+(?:\.\d+)?[Xx]?\d*\^?-?\d+\s*(?:W/Hz|V|mV|kbps|dB|MHz|GHz|kHz)\b"), "SCI_NUM"),
    # Subscripts/Superscripts (e.g. P_e, s_1(t))
    (re.compile(r"\b[A-Za-z][_^][A-Za-z0-9]+\b"), "SUBSCRIPT"),
]


def _protect_technical(text: str) -> tuple[str, dict]:
    """
    Replace technical content with numbered placeholders.
    Returns (modified_text, placeholder_map) for later restoration.
    """
    placeholder_map = {}
    counter = [0]

    def make_placeholder(label: str, match_text: str) -> str:
        key = f"__JARVIS_{label}_{counter[0]}__"
        counter[0] += 1
        placeholder_map[key] = match_text
        return key

    for pattern, label in _PRESERVE_PATTERNS:
        text = pattern.sub(lambda m: make_placeholder(label, m.group(0)), text)

    return text, placeholder_map


def _restore_technical(text: str, placeholder_map: dict) -> str:
    """Restore original technical content from placeholders."""
    for key, original in placeholder_map.items():
        text = text.replace(key, original)
    return text


# ── Text Chunking ──────────────────────────────────────────────────────────────

def _split_into_chunks(text: str, max_chars: int = 2000) -> list[str]:
    """
    Split text into chunks at sentence boundaries, each ≤ max_chars.
    Ensures no sentence is split in the middle.
    """
    if len(text) <= max_chars:
        return [text]

    # Split at sentence boundaries
    sentence_endings = re.compile(r"(?<=[.!?])\s+")
    sentences = sentence_endings.split(text)

    chunks = []
    current = ""
    for sentence in sentences:
        if len(current) + len(sentence) + 1 <= max_chars:
            current = (current + " " + sentence).strip()
        else:
            if current:
                chunks.append(current)
            # If single sentence is too long, hard-split at word boundary
            if len(sentence) > max_chars:
                words = sentence.split()
                current = ""
                for word in words:
                    if len(current) + len(word) + 1 <= max_chars:
                        current = (current + " " + word).strip()
                    else:
                        if current:
                            chunks.append(current)
                        current = word
            else:
                current = sentence
    if current:
        chunks.append(current)

    return chunks if chunks else [text]


# ── Browser Humanizer ─────────────────────────────────────────────────────────

def _get_browser_page(playwright, site_key: str):
    """Get a persistent browser page (non-headless, saves session)."""
    profile_dir = _BROWSER_PROFILE / f"humanizer_{site_key}"
    profile_dir.mkdir(parents=True, exist_ok=True)

    context = playwright.chromium.launch_persistent_context(
        user_data_dir=str(profile_dir),
        headless=False,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-infobars",
            "--start-maximized",
        ],
        user_agent=_REALISTIC_UA,
        viewport=None,
        locale="en-US",
    )
    context.add_init_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    page = context.new_page()
    return context, page


def _find_element(page, selectors: list, timeout: int = 6000):
    """Try multiple CSS selectors to find a visible element."""
    for sel in selectors:
        try:
            loc = page.locator(sel).first
            loc.wait_for(state="visible", timeout=timeout)
            return loc
        except Exception:
            continue
    return None


def _fill_input(page, input_el, text: str):
    """Fill an input area with text using the most reliable method available."""
    try:
        input_el.click()
        time.sleep(0.3)
        # Try JS value injection (works for textarea and contenteditable)
        try:
            tag = page.evaluate("el => el.tagName.toLowerCase()", input_el.element_handle())
            if tag == "textarea":
                page.evaluate(
                    "([el, val]) => { el.value = val; el.dispatchEvent(new Event('input', {bubbles:true})); }",
                    [input_el.element_handle(), text],
                )
            else:
                page.evaluate(
                    "([el, val]) => { el.innerText = val; el.dispatchEvent(new InputEvent('input', {bubbles:true})); }",
                    [input_el.element_handle(), text],
                )
        except Exception:
            input_el.fill(text)
        time.sleep(0.3)
    except Exception:
        try:
            input_el.fill(text)
        except Exception:
            # Last resort: clipboard paste
            import pyperclip
            pyperclip.copy(text)
            input_el.click()
            page.keyboard.press("Control+a")
            page.keyboard.press("Control+v")


def _extract_output_text(page, output_selectors: list) -> str:
    """Extract text from the output area of the humanizer."""
    for sel in output_selectors:
        try:
            el = page.locator(sel).first
            el.wait_for(state="visible", timeout=5000)
            # Try different methods to get text
            try:
                tag = page.evaluate("el => el.tagName.toLowerCase()", el.element_handle())
                if tag == "textarea":
                    text = page.evaluate("el => el.value", el.element_handle())
                else:
                    text = page.evaluate("el => el.innerText || el.textContent", el.element_handle())
                if text and len(text.strip()) > 20:
                    return text.strip()
            except Exception:
                text = el.inner_text()
                if text and len(text.strip()) > 20:
                    return text.strip()
        except Exception:
            continue

    # Fallback: try clipboard via copy button
    copy_selectors = ["button[aria-label*='Copy']", "button:has-text('Copy')", ".copy-btn"]
    for sel in copy_selectors:
        try:
            btns = page.locator(sel)
            if btns.count() > 0:
                btns.last.click()
                time.sleep(0.8)
                import pyperclip
                text = pyperclip.paste()
                if text and len(text.strip()) > 20:
                    return text.strip()
        except Exception:
            continue

    return ""


def _humanize_chunk_via_browser(page, chunk: str, site_cfg: dict) -> str:
    """
    Humanize a single text chunk on an already-open browser page.
    Returns humanized text or empty string if failed.
    """
    # Find input area
    input_el = _find_element(page, site_cfg["input_selectors"])
    if not input_el:
        return ""

    # Clear existing content and fill with new text
    try:
        input_el.click()
        page.keyboard.press("Control+a")
        page.keyboard.press("Delete")
        time.sleep(0.2)
    except Exception:
        pass

    _fill_input(page, input_el, chunk)
    time.sleep(0.5)

    # Click the humanize/paraphrase button
    btn = _find_element(page, site_cfg["button_selectors"])
    if not btn:
        return ""

    try:
        btn.click()
    except Exception:
        try:
            page.evaluate("el => el.click()", btn.element_handle())
        except Exception:
            return ""

    # Wait for processing
    time.sleep(site_cfg["wait_seconds"] // 2)

    # Poll for output to appear
    deadline = time.time() + site_cfg["wait_seconds"]
    while time.time() < deadline:
        output = _extract_output_text(page, site_cfg["output_selectors"])
        if output and len(output) > 20 and output.strip() != chunk.strip():
            return output
        time.sleep(2)

    # One final attempt
    return _extract_output_text(page, site_cfg["output_selectors"])


def _humanize_via_browser(text: str, site_key: str) -> str:
    """
    Open a humanizer site in browser, process text in chunks, return humanized result.
    """
    from playwright.sync_api import sync_playwright

    site = _HUMANIZER_SITES[site_key]
    max_chars = site["max_chars"]

    # Protect technical content
    protected_text, placeholder_map = _protect_technical(text)

    # Split into chunks
    chunks = _split_into_chunks(protected_text, max_chars=max_chars)

    humanized_chunks = []

    try:
        with sync_playwright() as pw:
            context, page = _get_browser_page(pw, site_key)
            page.goto(site["url"], wait_until="domcontentloaded", timeout=25000)
            time.sleep(3)

            for chunk in chunks:
                if not chunk.strip():
                    humanized_chunks.append(chunk)
                    continue

                result = _humanize_chunk_via_browser(page, chunk, site)
                if result and len(result) > 20:
                    humanized_chunks.append(result)
                else:
                    # Keep original chunk if humanization failed
                    humanized_chunks.append(chunk)

            context.close()

    except Exception:
        return ""

    humanized = " ".join(humanized_chunks).strip()
    if not humanized or len(humanized) < 20:
        return ""

    # Restore technical content
    humanized = _restore_technical(humanized, placeholder_map)
    return humanized


# ── LLM Humanizer (Always-Available Fallback) ─────────────────────────────────

_LLM_HUMANIZE_SYSTEM = """\
You are rewriting academic text to sound like it was written by a university student \
who genuinely understands the subject matter — NOT an AI.

REWRITING RULES:
1. Vary sentence lengths. Mix short, punchy sentences with longer explanatory ones.
2. Use occasional first-person voice: "I think", "In my view", "As I understand it"
3. Use natural student connectors: "So basically", "The key idea here is", "In other words", \
"This makes sense because", "What this means is"
4. Replace formal transitions: "Furthermore" → "Also" / "Another thing is", \
"Moreover" → "On top of that", "Nevertheless" → "Even so"
5. Add occasional hedging: "essentially", "roughly", "in simple terms"
6. Use contractions where they fit: it's, that's, we've, doesn't, isn't
7. Keep ALL technical terms, variable names, formulas, and numbers EXACTLY as-is
8. Do NOT add new technical content or change any facts
9. Length should be roughly the same as the original
10. Sound genuinely engaged with the material — like a student who finds it interesting

CRITICAL: Preserve all formulas (like Pe, N0, η/2, 10^-9) exactly. \
Only change the prose/writing style around them."""

_LLM_HUMANIZE_USER = "Rewrite the following in a natural student voice:\n\n{text}"


def _humanize_via_llm(text: str) -> str:
    """
    Humanize text using Groq LLM with 'write like a student' prompt.
    Model fallback chain: llama-3.3-70b → llama-3.1-8b → gemma2-9b.
    This method is safe for technical content (formulas preserved via placeholder pattern).
    """
    # Protect technical content before LLM rewrite
    protected_text, placeholder_map = _protect_technical(text)

    # Split into chunks (LLM handles larger chunks well)
    chunks = _split_into_chunks(protected_text, max_chars=3000)

    model_chain = [
        ("llama-3.1-8b-instant", 3000),
        ("llama-3.1-8b-instant",    2500),
        ("gemma2-9b-it",            2500),
    ]

    humanized_chunks = []
    for chunk in chunks:
        if not chunk.strip():
            humanized_chunks.append(chunk)
            continue

        chunk_humanized = ""
        last_error = ""

        for model_name, max_tok in model_chain:
            try:
                r = _groq.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": _LLM_HUMANIZE_SYSTEM},
                        {"role": "user", "content": _LLM_HUMANIZE_USER.format(text=chunk)},
                    ],
                    max_tokens=max_tok,
                    temperature=0.7,  # Higher temp = more human-like variation
                )
                chunk_humanized = r.choices[0].message.content.strip()
                break
            except Exception as e:
                last_error = str(e)
                err_lower = last_error.lower()
                if "429" in last_error or "rate limit" in err_lower or "quota" in err_lower:
                    continue
                break

        # Use humanized version, fall back to original if LLM completely failed
        humanized_chunks.append(chunk_humanized if chunk_humanized else chunk)

    result = " ".join(humanized_chunks).strip()

    # Restore technical content
    result = _restore_technical(result, placeholder_map)
    return result


# ── PUBLIC TOOL FUNCTIONS ─────────────────────────────────────────────────────

def humanize_text(text: str, force_site: str = "") -> str:
    """
    Humanize a single block of AI-generated text to sound like a student wrote it.

    Tries methods in order:
      1. Paraphraser.io browser (free, no login)
      2. Scribbr browser (free, academic-focused)
      3. QuillBot browser (free tier, 10K chars)
      4. Groq LLM rewrite (always works, safest for technical content)

    Technical content (formulas, equations, code) is automatically preserved.
    Long text is split into chunks and reassembled.

    Args:
        text:       The AI-generated text to humanize
        force_site: Optional — force a specific site: 'paraphraser', 'scribbr',
                    'quillbot', or 'llm'. Leave empty to try all in order.

    Returns:
        Humanized text string.

    Example:
        humanize_text('The bit error probability Pe is given by...')
    """
    if not text or not text.strip():
        return text

    # If a specific site is forced, use only that
    if force_site:
        if force_site == "llm":
            return _humanize_via_llm(text)
        if force_site in _HUMANIZER_SITES:
            result = _humanize_via_browser(text, force_site)
            return result if result else _humanize_via_llm(text)

    # Try browser sites in priority order
    for site_key in ["paraphraser", "scribbr", "quillbot"]:
        try:
            result = _humanize_via_browser(text, site_key)
            if result and len(result) > 30:
                return result
        except Exception:
            continue

    # Final fallback — LLM rewrite (always available)
    return _humanize_via_llm(text)


def humanize_all_answers(qa_json: str) -> str:
    """
    Humanize ALL answers in a QA_JSON block from Phase 2 (generate_answers).
    Each answer is processed through the humanizer chain.
    Returns a new QA_JSON with humanized answers + original preserved as 'answer_raw'.

    Args:
        qa_json: JSON string from generate_answers() — the QA_JSON block.
                 Paste the full output of generate_answers() and this function
                 will find the JSON automatically.

    Returns:
        Human-readable summary + HUMANIZED_QA_JSON block ready for Phase 4 (Word doc).

    Example:
        humanize_all_answers('<output from generate_answers>')
    """
    try:
        # Parse QA JSON
        raw = qa_json
        if "QA_JSON:" in raw:
            raw = raw.split("QA_JSON:")[-1].strip()
        raw = re.sub(r"```(?:json)?", "", raw).strip().rstrip("`").strip()

        try:
            qa_list = json.loads(raw)
        except json.JSONDecodeError:
            return (
                "Could not parse QA JSON. "
                "Please pass the full output from 'generate_answers' directly."
            )

        if not qa_list or not isinstance(qa_list, list):
            return "No Q&A pairs found. Run generate_answers first."

        total = len(qa_list)
        humanized_count = 0
        results = []

        for i, qa in enumerate(qa_list):
            answer = qa.get("answer", "").strip()
            q_num = qa.get("number", i + 1)
            q_type = qa.get("type", "long_answer")

            if not answer or len(answer) < 20:
                results.append({**qa, "answer_raw": answer, "answer_humanized": answer})
                continue

            # Short answers (< 100 chars) and MCQ don't need heavy humanization
            if q_type in ("mcq",) or len(answer) < 100:
                # Light LLM touch only
                humanized = _humanize_via_llm(answer)
            else:
                humanized = humanize_text(answer)

            if humanized and len(humanized) > 20:
                humanized_count += 1
            else:
                humanized = answer  # Keep original if humanization failed

            results.append({
                **qa,
                "answer_raw": answer,        # Original AI answer preserved
                "answer": humanized,         # Humanized version (used in doc)
                "answer_humanized": humanized,
                "humanized": True,
            })

        # Format output
        preview_lines = [
            f"Humanization complete: {humanized_count}/{total} answers humanized.",
            "",
            "--- Preview (first 2 humanized answers) ---",
        ]
        for qa in results[:2]:
            num = qa.get("number", "?")
            q_preview = qa.get("question", "")[:70]
            h_preview = qa.get("answer_humanized", "")[:200]
            preview_lines.append(f"\nQ{num}: {q_preview}...")
            preview_lines.append(f"Humanized: {h_preview}...")

        humanized_json = json.dumps(results, indent=2, ensure_ascii=False)
        return "\n".join(preview_lines) + f"\n\nHUMANIZED_QA_JSON:\n{humanized_json}"

    except Exception as e:
        return f"Humanization failed: {str(e)}"
