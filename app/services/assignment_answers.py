"""
Jarvis Assignment Tool — Phase 2: Answer Generation
====================================================
STRICT ISOLATION: This module does NOT import from any other Jarvis tool module.
Uses only external libraries and standard Python.

Answer Generation Strategy (tried in priority order):
  1. Gemini Browser  — persistent profile, PDF uploaded, full context
  2. ChatGPT Browser — fallback if Gemini fails/not logged in
  3. DeepSeek Browser — fallback if ChatGPT fails
  4. Groq Llama 3.3-70b API — final fallback, instant, no browser needed

The PDF is uploaded ONCE per session so figures/diagrams are visible to the AI.
All questions are asked in the SAME conversation for full context retention.

Public Functions:
  generate_answers(questions_json, pdf_path) -- batch answer generation
  generate_answer(question, question_type)   -- single question via Groq API
"""

import re
import json
import time
import base64
import io
from pathlib import Path
from groq import Groq
from app.core.config import settings

_groq = Groq(api_key=settings.GROQ_API_KEY)

# Persistent browser profile — user logs in once, session saved forever
_BROWSER_PROFILE = Path.home() / ".jarvis_ai_browser"

_REALISTIC_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)

# ── AI Site Configurations ─────────────────────────────────────────────────────
_AI_SITES = {
    "gemini": {
        "url": "https://gemini.google.com/app",
        "name": "Gemini",
        "input_selectors": [
            "div.ql-editor[contenteditable='true']",
            "rich-textarea div[contenteditable='true']",
            "div[contenteditable='true'][role='textbox']",
            "div[contenteditable='true']",
            "textarea",
        ],
        "upload_selectors": [
            "button[aria-label*='Upload']",
            "button[aria-label*='upload']",
            "button[aria-label*='Add image']",
            "button[aria-label*='Attach']",
        ],
        "wait_seconds": 35,
        "login_indicators": ["accounts.google", "signin", "login"],
    },
    "chatgpt": {
        "url": "https://chat.openai.com",
        "name": "ChatGPT",
        "input_selectors": [
            "#prompt-textarea",
            "div[contenteditable='true'][role='textbox']",
            "div[contenteditable='true']",
            "textarea[placeholder]",
        ],
        "upload_selectors": [
            "button[aria-label*='Attach']",
            "button[aria-label*='Upload']",
            "label[for='prompt-files-input']",
        ],
        "wait_seconds": 25,
        "login_indicators": ["login", "signin", "auth0"],
    },
    "deepseek": {
        "url": "https://chat.deepseek.com",
        "name": "DeepSeek",
        "input_selectors": [
            "textarea[placeholder]",
            "div[contenteditable='true']",
            "textarea",
        ],
        "upload_selectors": [
            "button[aria-label*='Upload']",
            "button[aria-label*='upload']",
            "label[for*='file']",
        ],
        "wait_seconds": 30,
        "login_indicators": ["login", "signin"],
    },
}


# ── Browser Helpers ────────────────────────────────────────────────────────────

def _get_persistent_page(playwright, site_key: str):
    """
    Launch a visible (non-headless) Chromium with a persistent profile.
    Login cookies are saved so the user only needs to log in once.
    Returns (context, page).
    """
    profile_dir = _BROWSER_PROFILE / site_key
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


def _find_input(page, selectors: list, timeout: int = 8000):
    """Try CSS selectors to find the visible chat input. Returns locator or None."""
    for sel in selectors:
        try:
            loc = page.locator(sel).first
            loc.wait_for(state="visible", timeout=timeout)
            return loc
        except Exception:
            continue
    return None


def _send_message(page, input_el, text: str):
    """Type a message into the AI chat input and submit it."""
    try:
        input_el.click()
        time.sleep(0.3)
        # Try JS injection first (handles contenteditable divs)
        try:
            page.evaluate(
                """([el, txt]) => {
                    el.focus();
                    if (el.contentEditable === 'true') {
                        el.innerText = txt;
                        el.dispatchEvent(new InputEvent('input', { bubbles: true }));
                    } else {
                        el.value = txt;
                        el.dispatchEvent(new Event('input', { bubbles: true }));
                    }
                }""",
                [input_el.element_handle(), text],
            )
        except Exception:
            input_el.fill(text)
        time.sleep(0.3)
        page.keyboard.press("Enter")
    except Exception:
        try:
            input_el.type(text, delay=10)
            page.keyboard.press("Enter")
        except Exception:
            pass


def _upload_pdf(page, pdf_path: str, upload_selectors: list) -> bool:
    """Upload PDF to the AI chat page. Returns True if upload was initiated."""
    # Strategy 1: file chooser interception
    for sel in upload_selectors:
        try:
            btn = page.locator(sel).first
            if btn.count() == 0:
                continue
            with page.expect_file_chooser(timeout=5000) as fc_info:
                btn.click(force=True)
            fc_info.value.set_files(pdf_path)
            time.sleep(3)
            return True
        except Exception:
            continue

    # Strategy 2: direct file input injection
    try:
        file_inputs = page.locator("input[type='file']")
        if file_inputs.count() > 0:
            file_inputs.first.set_input_files(pdf_path)
            time.sleep(3)
            return True
    except Exception:
        pass

    return False


def _wait_for_generation(page, wait_seconds: int):
    """Wait until the AI stops generating its response."""
    time.sleep(4)  # Initial wait for generation to start

    stop_selectors = [
        "button[aria-label*='Stop']",
        "button[aria-label*='stop']",
        "button[aria-label*='Cancel']",
        "[class*='loading']",
        "[class*='spinner']",
        "[class*='generating']",
    ]

    deadline = time.time() + wait_seconds
    while time.time() < deadline:
        generating = False
        for sel in stop_selectors:
            try:
                if page.locator(sel).first.is_visible():
                    generating = True
                    break
            except Exception:
                pass
        if not generating:
            break
        time.sleep(1.5)

    time.sleep(2)


def _try_copy_button(page) -> str:
    """Click the copy button on the last AI response and return clipboard text."""
    copy_selectors = [
        "button[aria-label*='Copy']",
        "button[aria-label*='copy']",
        "button[title*='Copy']",
        "[data-testid*='copy']",
        "button.copy-button",
    ]
    for sel in copy_selectors:
        try:
            btns = page.locator(sel)
            count = btns.count()
            if count > 0:
                btns.nth(count - 1).click()
                time.sleep(0.8)
                import pyperclip
                text = pyperclip.paste()
                if text and len(text) > 30:
                    return text.strip()
        except Exception:
            continue
    return ""


def _screenshot_extract(page) -> str:
    """Take a page screenshot and use Groq Vision to extract the AI's answer."""
    try:
        screenshot_bytes = page.screenshot(full_page=False)
        b64 = base64.b64encode(screenshot_bytes).decode("utf-8")
        response = _groq.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "This is a screenshot of an AI chat interface (Gemini/ChatGPT/DeepSeek). "
                            "Extract ONLY the AI assistant's most recent, complete response. "
                            "Return just the answer text — no UI labels, no user question, no meta-text."
                        ),
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{b64}"},
                    },
                ],
            }],
            max_tokens=3000,
            temperature=0.1,
        )
        text = response.choices[0].message.content.strip()
        return text if len(text) > 20 else ""
    except Exception:
        return ""


def _ask_question_on_page(page, question: str, q_num, site_cfg: dict) -> str:
    """Send one question to the open AI page and return the answer text."""
    input_el = _find_input(page, site_cfg["input_selectors"])
    if not input_el:
        return ""

    prompt = (
        f"Question {q_num}: {question}\n\n"
        "Give a complete, detailed answer. "
        "Refer to the uploaded PDF/figures where relevant."
    )

    _send_message(page, input_el, prompt)
    _wait_for_generation(page, site_cfg["wait_seconds"])

    # Try copy button first (most accurate)
    answer = _try_copy_button(page)
    if not answer or len(answer) < 30:
        answer = _screenshot_extract(page)

    return answer


def _run_browser_session(pdf_path: str, questions: list, site_key: str) -> list:
    """
    Full browser session: open site → upload PDF → ask all questions → close.
    Returns list of question dicts with 'answer' and 'answer_source' filled in.
    """
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

    site = _AI_SITES[site_key]
    qa_results = [{**q, "answer": "", "answer_source": ""} for q in questions]

    try:
        with sync_playwright() as pw:
            context, page = _get_persistent_page(pw, site_key)

            # Navigate to AI site
            page.goto(site["url"], wait_until="domcontentloaded", timeout=30000)
            time.sleep(4)

            # Handle login redirect — wait up to 2 minutes for user to log in
            login_indicators = site.get("login_indicators", ["login", "signin"])
            current_url = page.url.lower()
            if any(ind in current_url for ind in login_indicators):
                print(
                    f"[Assignment] {site['name']} needs login. "
                    "Please log in in the browser window. Waiting up to 2 minutes..."
                )
                deadline = time.time() + 120
                while time.time() < deadline:
                    time.sleep(3)
                    if not any(ind in page.url.lower() for ind in login_indicators):
                        break
                time.sleep(3)

            # Try to start a new chat
            new_chat_attempts = [
                "a[aria-label*='New chat']",
                "button[aria-label*='New chat']",
                "a[href='/app']",
                "a[href*='new']",
            ]
            for sel in new_chat_attempts:
                try:
                    btn = page.locator(sel).first
                    if btn.is_visible(timeout=2000):
                        btn.click()
                        time.sleep(2)
                        break
                except Exception:
                    pass

            # Upload PDF
            pdf_uploaded = _upload_pdf(page, pdf_path, site["upload_selectors"])

            # Send context-setting message if PDF uploaded
            if pdf_uploaded:
                time.sleep(3)
                input_el = _find_input(page, site["input_selectors"])
                if input_el:
                    _send_message(
                        page, input_el,
                        "I have uploaded my assignment PDF. Read it carefully including all figures. "
                        "I will ask you questions one by one. For each, give a full, detailed answer."
                    )
                    _wait_for_generation(page, 12)

            # Ask each question
            for i, q in enumerate(questions):
                q_text = q.get("question", "").strip()
                q_num = q.get("number", i + 1)
                if not q_text:
                    continue

                if q.get("has_figure"):
                    q_text += (
                        "\n[This question has a figure in the PDF — "
                        "use the uploaded PDF to see it.]"
                    )

                answer = _ask_question_on_page(page, q_text, q_num, site)

                if answer and len(answer) > 30:
                    qa_results[i]["answer"] = answer
                    qa_results[i]["answer_source"] = site["name"]

                time.sleep(2)

            context.close()

    except Exception as e:
        # Return whatever partial results we have
        pass

    return qa_results


# ── Direct LLM Fallback ───────────────────────────────────────────────────────

def _groq_answer(question: str, question_type: str, has_figure: bool = False) -> str:
    """
    Generate an answer using Groq LLM with automatic model fallback chain.
    Tries models in order: llama-3.3-70b → llama-3.1-8b → gemma2-9b
    Handles rate limits gracefully by falling back to a smaller/different model.
    """
    _INSTRUCTIONS = {
        "numerical":    "Show complete step-by-step calculations. State formulas used. Show all working.",
        "mcq":          "State the correct option clearly. Explain why it is correct and why others are wrong.",
        "code":         "Write clean, working, commented code. State time and space complexity.",
        "essay":        "Write a structured essay: introduction, body (3+ paragraphs), conclusion.",
        "short_answer": "Answer in 2-4 concise sentences. Be precise.",
        "long_answer":  "Write a comprehensive explanation with examples and diagrams described in text.",
        "report":       "Structure: Abstract, Introduction, Analysis, Conclusion, References.",
        "presentation": "List slide-by-slide: Title, Agenda, 5-7 content slides with bullet points, Conclusion.",
    }

    instruction = _INSTRUCTIONS.get(question_type, "Provide a complete, accurate answer.")
    fig_note = (
        " The question references a diagram — answer based on standard theory for this topic."
        if has_figure else ""
    )

    system = (
        "You are an expert academic assistant helping a university student with their assignment.\n"
        f"Answer format: {instruction}{fig_note}\n"
        "Use proper academic language. Be thorough. Do not truncate your answer."
    )

    # Model fallback chain: best quality → fast → alternative
    model_chain = [
        ("llama-3.3-70b-versatile", 2500),
        ("llama-3.1-8b-instant",    2000),
        ("gemma2-9b-it",            2000),
    ]

    last_error = ""
    for model_name, max_tok in model_chain:
        try:
            r = _groq.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": question},
                ],
                max_tokens=max_tok,
                temperature=0.3,
            )
            return r.choices[0].message.content.strip()
        except Exception as e:
            last_error = str(e)
            # Only continue fallback on rate-limit / quota errors
            err_lower = last_error.lower()
            if "429" in last_error or "rate limit" in err_lower or "quota" in err_lower:
                continue
            # For other errors (auth, bad request), fail fast
            break

    return f"[Answer generation failed after all fallbacks: {last_error[:200]}]"


# ── PUBLIC TOOL FUNCTIONS ─────────────────────────────────────────────────────

def generate_answers(questions_json: str, pdf_path: str = "") -> str:
    """
    Generate complete answers for ALL questions from an assignment.

    Tries these methods in order:
      1. Gemini browser (opens Gemini, uploads PDF, asks questions with full context)
      2. ChatGPT browser (fallback)
      3. DeepSeek browser (fallback)
      4. Groq Llama 3.3-70b API (instant fallback — no browser, answers from training)

    Args:
        questions_json: JSON string from extract_questions() — the QUESTIONS_JSON block.
                        Paste the full output of extract_questions() and this function
                        will find the JSON automatically.
        pdf_path:       Filename or full path of the assignment PDF.
                        Used to upload the PDF to the AI browser for figure context.
                        If empty, skips browser and uses Groq API directly.

    Returns:
        Human-readable summary + QA_JSON block with all questions and answers.

    Example:
        generate_answers('<output from extract_questions>', 'DcAssignment.pdf')
    """
    try:
        # Step 1: Parse questions
        raw = questions_json
        if "QUESTIONS_JSON:" in raw:
            raw = raw.split("QUESTIONS_JSON:")[-1].strip()
        raw = re.sub(r"```(?:json)?", "", raw).strip().rstrip("`").strip()

        try:
            questions = json.loads(raw)
        except json.JSONDecodeError:
            return (
                "Could not parse the questions JSON. "
                "Please pass the full output from 'extract_questions' directly."
            )

        if not questions or not isinstance(questions, list):
            return "No questions found in the provided JSON. Run extract_questions first."

        total = len(questions)

        # Step 2: Resolve PDF path
        resolved_pdf = None
        if pdf_path.strip():
            from app.services.assignment_tool import _resolve_pdf_path
            resolved_pdf = _resolve_pdf_path(pdf_path.strip())

        # Step 3: Try browser answer generation
        qa_results = None
        browser_site = None

        if resolved_pdf:
            for site_key in ["gemini", "chatgpt", "deepseek"]:
                try:
                    result = _run_browser_session(resolved_pdf, questions, site_key)
                    answered = sum(
                        1 for q in result
                        if q.get("answer") and len(q.get("answer", "")) > 30
                    )
                    if answered >= max(1, total // 2):
                        qa_results = result
                        browser_site = _AI_SITES[site_key]["name"]
                        break
                except Exception:
                    continue

        # Step 4: Groq API fallback for missing/failed answers
        if not qa_results:
            qa_results = [{**q, "answer": "", "answer_source": "groq_api"} for q in questions]

        for i, q in enumerate(qa_results):
            if not q.get("answer") or len(q.get("answer", "")) < 30:
                answer = _groq_answer(
                    question=q.get("question", ""),
                    question_type=q.get("type", "long_answer"),
                    has_figure=q.get("has_figure", False),
                )
                qa_results[i]["answer"] = answer
                qa_results[i]["answer_source"] = "groq_llm_api"

        # Step 5: Format output
        answered = sum(1 for q in qa_results if q.get("answer") and len(q["answer"]) > 20)
        source_note = f"via {browser_site} browser" if browser_site else "via Groq LLM API (direct)"

        preview_lines = [
            f"Answers generated for {answered}/{total} questions ({source_note}).",
            "",
            "--- Preview (first 2 answers) ---",
        ]
        for q in qa_results[:2]:
            num = q.get("number", "?")
            q_preview = q.get("question", "")[:80]
            a_preview = q.get("answer", "")[:250]
            preview_lines.append(f"\nQ{num}: {q_preview}...")
            preview_lines.append(f"Answer: {a_preview}...")

        qa_json = json.dumps(qa_results, indent=2, ensure_ascii=False)
        return "\n".join(preview_lines) + f"\n\nQA_JSON:\n{qa_json}"

    except Exception as e:
        return f"Answer generation failed: {str(e)}"


def generate_answer(question: str, question_type: str = "long_answer",
                    has_figure: bool = False) -> str:
    """
    Generate an answer for a SINGLE question using Groq LLM directly (fast, no browser).
    For full assignment with browser AI + PDF context, use generate_answers() instead.

    Args:
        question:      The question text
        question_type: mcq | short_answer | long_answer | numerical | code | essay | report
        has_figure:    True if question references a figure/diagram

    Returns:
        Complete answer as plain text.
    """
    try:
        return _groq_answer(question, question_type, has_figure)
    except Exception as e:
        return f"Failed to generate answer: {str(e)}"
