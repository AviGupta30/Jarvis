"""
Jarvis Assignment Tool — Phase 5: End-to-End Pipeline
=====================================================
Master orchestrator: File → Questions → Answers (Gemini/Edge) → Humanize → Word/PPT

THREADING NOTE: Playwright sync_api must NOT run inside an asyncio event loop.
We run all browser code in a daemon Thread that communicates via a Queue.
The generator reads from the Queue and yields status/result strings to the HTTP stream.
"""

import os
import re
import json
import time
import queue
import threading
from pathlib import Path

# ── Chrome/Edge Paths ──────────────────────────────────────────────────────────
_CHROME_EXE = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
_CHROME_PROFILE = os.path.expanduser(r"~\AppData\Local\Google\Chrome\User Data")

_EDGE_PATHS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]
_EDGE_EXE = next((p for p in _EDGE_PATHS if os.path.exists(p)), None)
_EDGE_DEFAULT_PROFILE = os.path.expanduser(r"~\AppData\Local\Microsoft\Edge\User Data")

# Persistent fallback profile dir
_EDGE_PROFILE = Path.home() / ".jarvis_edge_browser"

_SENTINEL = "__DONE__"
_ERROR_PREFIX = "__ERROR__:"


# ═══════════════════════════════════════════════════════════════════════════════
# Browser helpers (all sync — run inside thread)
# ═══════════════════════════════════════════════════════════════════════════════

def _get_browser_ctx(playwright, site_key: str, q: queue.Queue):
    """Try to use Edge Default profile, then Chrome, fallback to Jarvis custom profile."""
    kwargs = dict(
        headless=False,
        slow_mo=100,
        args=["--disable-blink-features=AutomationControlled", "--no-sandbox", "--start-maximized"],
        viewport=None,
    )
    
    # 1. Try Edge default profile first
    if _EDGE_EXE and os.path.exists(_EDGE_DEFAULT_PROFILE):
        try:
            kwargs["executable_path"] = _EDGE_EXE
            kwargs["user_data_dir"] = _EDGE_DEFAULT_PROFILE
            ctx = playwright.chromium.launch_persistent_context(channel="msedge", **kwargs)
            ctx.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined})")
            return ctx, "Edge Default"
        except Exception as e:
            if "in use" in str(e).lower() or "lock" in str(e).lower():
                q.put("⚠️ **Warning:** Microsoft Edge is currently open. Please close Edge to use your logged-in profile.")
    
    # 2. Try Chrome default profile next
    if os.path.exists(_CHROME_EXE) and os.path.exists(_CHROME_PROFILE):
        try:
            kwargs["executable_path"] = _CHROME_EXE
            kwargs["user_data_dir"] = _CHROME_PROFILE
            ctx = playwright.chromium.launch_persistent_context(**kwargs)
            ctx.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined})")
            return ctx, "Chrome Default"
        except Exception as e:
            if "in use" in str(e).lower() or "lock" in str(e).lower():
                pass
                
    # 3. Fallback to isolated Edge/Chrome profile
    profile_dir = _EDGE_PROFILE / site_key
    profile_dir.mkdir(parents=True, exist_ok=True)
    kwargs["user_data_dir"] = str(profile_dir)
    if _EDGE_EXE:
        kwargs["executable_path"] = _EDGE_EXE
    elif os.path.exists(_CHROME_EXE):
        kwargs["executable_path"] = _CHROME_EXE
        
    ctx = playwright.chromium.launch_persistent_context(**kwargs)
    ctx.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined})")
    return ctx, "Jarvis Isolated Profile"


def _find_el(page, selectors, timeout=8000):
    for sel in selectors:
        try:
            loc = page.locator(sel).first
            loc.wait_for(state="visible", timeout=timeout)
            return loc
        except Exception:
            continue
    return None


def _type_into(page, el, text: str):
    try:
        el.click()
        time.sleep(0.3)
        page.evaluate(
            """([el, txt]) => {
                el.focus();
                if (el.contentEditable === 'true') {
                    el.innerText = txt;
                    el.dispatchEvent(new InputEvent('input',{bubbles:true}));
                } else {
                    el.value = txt;
                    el.dispatchEvent(new Event('input',{bubbles:true}));
                }
            }""",
            [el.element_handle(), text],
        )
    except Exception:
        try:
            el.fill(text)
        except Exception:
            el.type(text, delay=8)


def _upload_file(page, file_path: str) -> bool:
    try:
        # 1. Try finding and interacting directly with the hidden file input
        inputs = page.locator("input[type='file']")
        if inputs.count() > 0:
            inputs.first.set_input_files(file_path)
            time.sleep(3)
            return True
    except Exception:
        pass

    try:
        # 2. Try the modern + button (Upload image/file)
        plus_btn = _find_el(page, [
            "button[aria-label*='Upload']", "button[aria-label*='upload']",
            "button[aria-label*='Attach']", "button[aria-label*='Add file']",
            "button[aria-label*='Add image']", "button[mattooltip*='Upload']"
        ])
        if plus_btn:
            # Click the + button, which might open a menu
            plus_btn.click(force=True)
            time.sleep(1)
            
            # Now there might be a menu item like "Upload from computer"
            # However, clicking + might also just directly open the file chooser
            menu_item = page.locator("text='Upload from computer'")
            if menu_item.count() > 0:
                with page.expect_file_chooser(timeout=5000) as fc:
                    menu_item.first.click(force=True)
                fc.value.set_files(file_path)
                time.sleep(4)
                return True
                
            # If no menu, maybe it was a direct file chooser button
            with page.expect_file_chooser(timeout=5000) as fc:
                plus_btn.click(force=True)
            fc.value.set_files(file_path)
            time.sleep(4)
            return True
    except Exception:
        pass
        
    # 3. Fallback: Try dropping the file onto the chat input area
    try:
        page.evaluate("""(filepath) => {
            const input = document.querySelector("input[type='file']");
            if (input) {
                const dataTransfer = new DataTransfer();
                const file = new File([''], filepath);
                dataTransfer.items.add(file);
                input.files = dataTransfer.files;
                input.dispatchEvent(new Event('change', { bubbles: true }));
            }
        }""", file_path)
        time.sleep(2)
        # We can't actually spoof a real File object with full path via JS easily due to security,
        # so this is just a best effort.
    except Exception:
        pass
        
    return False


def _wait_done(page, max_secs=45):
    time.sleep(4)
    stop_sels = [
        "button[aria-label*='Stop']", "button[aria-label*='stop']",
        "[class*='loading']", "[class*='generating']",
    ]
    deadline = time.time() + max_secs
    while time.time() < deadline:
        still_generating = any(
            page.locator(s).count() > 0 and page.locator(s).first.is_visible()
            for s in stop_sels
        )
        if not still_generating:
            break
        time.sleep(2)
    time.sleep(2)


def _get_answer(page) -> str:
    """Try copy button, then DOM, then Groq vision."""
    try:
        import pyperclip
        copy_sels = [
            "button[aria-label*='Copy']", "button[aria-label*='copy']",
            "button[title*='Copy']", "[data-testid*='copy']",
        ]
        for sel in copy_sels:
            btns = page.locator(sel)
            c = btns.count()
            if c > 0:
                btns.nth(c - 1).click()
                time.sleep(1)
                txt = pyperclip.paste()
                if txt and len(txt) > 30:
                    return txt.strip()
    except Exception:
        pass

    dom_sels = [
        "model-response:last-of-type", ".response-content:last-child",
        "div[class*='response']:last-child",
    ]
    for sel in dom_sels:
        try:
            el = page.locator(sel).last
            txt = el.inner_text()
            if txt and len(txt) > 30:
                return txt.strip()
        except Exception:
            continue

    # Groq vision fallback
    try:
        import base64
        from groq import Groq
        from app.core.config import settings
        g = Groq(api_key=settings.GROQ_API_KEY)
        ss = page.screenshot(full_page=False)
        b64 = base64.b64encode(ss).decode()
        r = g.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
            messages=[{"role": "user", "content": [
                {"type": "text", "text": (
                    "Screenshot of Gemini AI chat. Extract ONLY the latest AI response. "
                    "Return just the answer text, no UI labels or prefixes."
                )},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}},
            ]}],
            max_tokens=3000, temperature=0.1,
        )
        return r.choices[0].message.content.strip()
    except Exception:
        return ""


def _humanize_browser(page, text: str) -> str:
    try:
        page.goto("https://www.paraphraser.io/", wait_until="domcontentloaded", timeout=20000)
        time.sleep(3)
        inp = _find_el(page, [
            "textarea#inputText", "textarea[placeholder*='Enter']",
            "textarea[placeholder*='Paste']", "textarea",
        ])
        if not inp:
            return text
            
        btn = _find_el(page, [
            "button[id*='paraphrase']", "button[class*='paraphrase']",
            "button:has-text('Paraphrase')", "button:has-text('Humanize')",
        ])
        if not btn:
            return text
            
        # Paraphraser often has an 800-1000 char limit. Split text into safe chunks.
        # Split by sentences or paragraphs if possible, otherwise hard chunks.
        chunks = []
        words = text.split(' ')
        current_chunk = ""
        for word in words:
            if len(current_chunk) + len(word) + 1 < 750:
                current_chunk += word + " "
            else:
                chunks.append(current_chunk.strip())
                current_chunk = word + " "
        if current_chunk:
            chunks.append(current_chunk.strip())
            
        humanized_chunks = []
        for idx, chunk in enumerate(chunks):
            if len(chunk) < 20:
                humanized_chunks.append(chunk)
                continue
                
            _type_into(page, inp, chunk)
            time.sleep(0.5)
            btn.click()
            time.sleep(12) # Wait for humanization
            
            chunk_result = chunk
            for sel in ["textarea#outputText", ".output-area textarea", "textarea:nth-of-type(2)"]:
                try:
                    el = page.locator(sel).first
                    el.wait_for(state="visible", timeout=5000)
                    val = page.evaluate("el => el.value || el.innerText", el.element_handle())
                    if val and len(val.strip()) > 10 and val.strip() != chunk.strip():
                        chunk_result = val.strip()
                        break
                except Exception:
                    continue
            
            humanized_chunks.append(chunk_result)
            
            # Clear input for next chunk
            if idx < len(chunks) - 1:
                page.evaluate("el => { el.value = ''; el.innerText = ''; }", inp.element_handle())
                time.sleep(0.5)
                
        return " ".join(humanized_chunks)
    except Exception:
        pass
    return text


def _groq_answer(question: str, q_type: str = "long_answer", has_fig: bool = False) -> str:
    """Groq API fallback for a single question."""
    from groq import Groq
    from app.core.config import settings
    g = Groq(api_key=settings.GROQ_API_KEY)
    sys = (
        "You are an expert academic assistant. Answer the question clearly, completely, "
        "and in a way suitable for a university-level student submission. "
        "Include all relevant details, show workings for calculations, and use proper formatting."
    )
    note = " [This question may refer to a figure in the PDF]" if has_fig else ""
    for model in ["llama-3.3-70b-versatile", "llama3-8b-8192", "gemma2-9b-it"]:
        try:
            r = g.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": sys},
                    {"role": "user", "content": question + note},
                ],
                max_tokens=3000, temperature=0.3,
            )
            return r.choices[0].message.content.strip()
        except Exception:
            continue
    return f"[Could not generate answer for: {question[:80]}]"


def _groq_humanize(text: str) -> str:
    """Groq API humanization fallback."""
    from groq import Groq
    from app.core.config import settings
    g = Groq(api_key=settings.GROQ_API_KEY)
    prompt = (
        "Rewrite the following answer as if written by a university student. "
        "Make it sound natural, slightly less formal, use first-person perspective occasionally, "
        "add small imperfections like minor transitions or casual phrasing. "
        "Keep all technical content, facts, formulas, and code EXACTLY the same. "
        "DO NOT summarize or remove content — just rewrite the tone.\n\nAnswer:\n" + text
    )
    for model in ["llama-3.3-70b-versatile", "llama3-8b-8192"]:
        try:
            r = g.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=4000, temperature=0.7,
            )
            return r.choices[0].message.content.strip()
        except Exception:
            continue
    return text


# ═══════════════════════════════════════════════════════════════════════════════
# Browser thread — runs entirely in a daemon thread (no asyncio conflict)
# ═══════════════════════════════════════════════════════════════════════════════

def _browser_thread(file_path: str, questions: list, humanize: bool, q: queue.Queue):
    """
    Runs all Playwright browser automation in a separate thread.
    Puts status strings and the final result list into `q`.
    Sends _SENTINEL when done, _ERROR_PREFIX+msg on fatal error.
    """
    qa_results = []

    try:
        from playwright.sync_api import sync_playwright

        q.put("🌐 **Step 2:** Opening Browser → Gemini AI…")

        with sync_playwright() as pw:
            ctx, profile_name = _get_browser_ctx(pw, "gemini", q)
            page = ctx.new_page()
            page.goto("https://gemini.google.com/app", wait_until="domcontentloaded", timeout=30000)
            time.sleep(4)

            # Login check
            if any(x in page.url.lower() for x in ["login", "signin", "accounts.google"]):
                q.put(f"🔐 **Login Required:** Please log into Gemini in the {profile_name} window. Waiting…")
                deadline = time.time() + 120
                while time.time() < deadline:
                    time.sleep(3)
                    if "gemini.google.com" in page.url:
                        break
                time.sleep(3)

            # Upload file
            q.put(f"📎 **Uploading** `{os.path.basename(file_path)}` to Gemini…")
            uploaded = _upload_file(page, file_path)
            if uploaded:
                q.put("✅ **File uploaded.** Prompting Gemini to read it…")
                time.sleep(2)
                inp_sels = [
                    "div.ql-editor[contenteditable='true']",
                    "rich-textarea div[contenteditable='true']",
                    "div[contenteditable='true'][role='textbox']",
                    "div[contenteditable='true']", "textarea",
                ]
                inp = _find_el(page, inp_sels)
                if inp:
                    _type_into(page, inp,
                        "I have uploaded my assignment file. Read everything carefully. "
                        "I will ask you each question individually. Give complete, detailed answers. "
                        "IMPORTANT: Do not use conversational filler (like 'Here is the answer'). Just give the direct pastable answer."
                    )
                    page.keyboard.press("Enter")
                    _wait_done(page, 20)
            else:
                q.put("⚠️ **File upload skipped** — couldn't find upload button. Will ask as text.")

            total = len(questions)
            inp_sels = [
                "div.ql-editor[contenteditable='true']",
                "rich-textarea div[contenteditable='true']",
                "div[contenteditable='true'][role='textbox']",
                "div[contenteditable='true']", "textarea",
            ]

            for i, qobj in enumerate(questions):
                q_text = qobj.get("question", "").strip()
                q_num = qobj.get("number", i + 1)
                q_type = qobj.get("type", "long_answer")
                has_fig = qobj.get("has_figure", False)
                if not q_text:
                    continue

                q.put(f"💬 **Question {q_num}/{total}:** Sending to Gemini…")
                prompt = (
                    f"Question {q_num}: {q_text}\n\n"
                    "Provide a complete, detailed, step-by-step answer. "
                    "SMART LENGTH: Analyze the complexity of the question. If it's a simple definitional question (e.g. 'What is Python?'), treat it as a 2-mark question and write a concise answer of 50-100 words. For complex or multi-part questions, provide a longer, more detailed answer proportional to its apparent weight.\n"
                    "If this is a mathematical or coding question, you MUST show all steps clearly. "
                    "CRITICAL MATH INSTRUCTIONS: DO NOT use LaTeX formatting (like \\frac, \\sqrt, $$, or \\) for math equations! Microsoft Word cannot render raw LaTeX. You MUST use plain text, standard keyboard symbols, and Unicode for all equations (e.g., use '1/sqrt(2*pi*sigma^2)' instead of '\\frac{1}{\\sqrt{2\\pi\\sigma^2}}').\n"
                    "CRITICAL: Give ONLY the direct answer. DO NOT add any conversational filler like 'Here is the answer' or 'Sure!'. "
                    "DO NOT use horizontal rules like ---. Just output the final, direct answer text."
                )
                if has_fig:
                    prompt += "\n[Refer to the uploaded file for any figures.]"

                inp = _find_el(page, inp_sels)
                if inp:
                    _type_into(page, inp, prompt)
                    page.keyboard.press("Enter")
                    _wait_done(page, 50)
                    answer = _get_answer(page)
                else:
                    answer = ""

                if not answer or len(answer) < 20:
                    q.put(f"   ↳ ⚡ Gemini answer empty — using Groq API fallback…")
                    answer = _groq_answer(q_text, q_type, has_fig)

                q.put(f"   ↳ ✅ Answer received ({len(answer)} chars)")
                qa_results.append({**qobj, "answer": answer, "source": "gemini_edge"})
                time.sleep(2)

            # Humanize in a second tab
            if humanize and qa_results:
                q.put("✍️ **Step 4:** Humanizing answers (opening Paraphraser tab)…")
                hum_page = ctx.new_page()
                for i, qa in enumerate(qa_results):
                    raw_ans = qa.get("answer", "")
                    if not raw_ans or len(raw_ans) < 50:
                        continue
                    q.put(f"   ↳ 🔄 Humanizing Q{qa.get('number', i+1)}/{total}…")
                    humanized = _humanize_browser(hum_page, raw_ans)
                    if not humanized or humanized.strip() == raw_ans.strip() or len(humanized) < 30:
                        q.put("   ↳ ⚡ Browser humanizer failed — using Groq LLM fallback…")
                        humanized = _groq_humanize(raw_ans)
                    qa_results[i]["answer"] = humanized
                    q.put(f"   ↳ ✅ Q{qa.get('number', i+1)} humanized")
                    time.sleep(0.5)
                hum_page.close()

            ctx.close()

    except Exception as e:
        q.put(f"⚠️ **Browser error:** {e} — falling back to Groq API for all questions…")
        qa_results = []  # reset, will re-generate below

    # If browser mode failed entirely, fall back to API for all
    if not qa_results:
        for i, qobj in enumerate(questions):
            q_text = qobj.get("question", "").strip()
            q_num = qobj.get("number", i + 1)
            if not q_text:
                continue
            q.put(f"   ↳ ⚡ Q{q_num} via Groq API…")
            answer = _groq_answer(q_text, qobj.get("type", "long_answer"), qobj.get("has_figure", False))
            qa_results.append({**qobj, "answer": answer, "source": "groq_api"})

    # Signal done with the result list serialized as JSON
    q.put(_SENTINEL + json.dumps(qa_results, ensure_ascii=False))


# ═══════════════════════════════════════════════════════════════════════════════
# Public generator — safe to call from asyncio (uses threading)
# ═══════════════════════════════════════════════════════════════════════════════

def do_assignment(pdf_path: str, output_format: str = "word", humanize: bool = True):
    """
    Master orchestrator. Uses a background thread for all Playwright code.
    Yields clean, human-readable status strings for live streaming.
    """
    from app.services.assignment_tool import extract_questions, _resolve_pdf_path

    # ── Step 1: Find and extract questions ────────────────────────────────────
    yield "📋 **Step 1:** Extracting questions from file…"
    time.sleep(0.3)

    file_path = pdf_path.strip() if pdf_path else ""

    if not file_path:
        yield "❌ **Error:** No file name detected in your message. Please say e.g. *'do my assignment from MyFile.pdf'*"
        return

    # Try absolute path first
    if not (os.path.isabs(file_path) and os.path.exists(file_path)):
        resolved = _resolve_pdf_path(file_path)
        if not resolved:
            yield f"❌ **Error:** Cannot find `{file_path}`. Make sure it is uploaded or saved on Desktop/Documents/Downloads."
            return
        file_path = resolved

    try:
        extracted = extract_questions(file_path)
    except Exception as e:
        yield f"❌ **Extraction failed:** {e}"
        return

    # Parse question list
    raw = extracted
    for tag in ("QUESTIONS_JSON:", "QA_JSON:"):
        if tag in raw:
            raw = raw.split(tag)[-1].strip()
            break
    raw = re.sub(r"```(?:json)?", "", raw).strip().rstrip("`").strip()

    try:
        questions = json.loads(raw)
        if not isinstance(questions, list):
            raise ValueError("Not a list")
    except Exception:
        yield "❌ **Error:** Could not parse questions from the file. Make sure it contains readable text questions."
        return

    total = len(questions)
    yield f"✅ **Step 1 Done:** Found **{total} questions** in `{os.path.basename(file_path)}`"
    time.sleep(0.3)

    # ── Step 2-4: Browser thread (answers + humanize) ──────────────────────────
    result_queue = queue.Queue()
    t = threading.Thread(
        target=_browser_thread,
        args=(file_path, questions, humanize, result_queue),
        daemon=True,
    )
    t.start()

    qa_results = []
    while True:
        try:
            msg = result_queue.get(timeout=180)  # max 3 min per item
        except queue.Empty:
            yield "⚠️ **Timeout:** Browser took too long. Moving to assembly with partial results."
            break

        if msg.startswith(_SENTINEL):
            # Final result
            try:
                qa_results = json.loads(msg[len(_SENTINEL):])
            except Exception:
                qa_results = []
            break
        else:
            yield msg

    if not qa_results:
        yield "❌ **No answers generated.** Check if Gemini is logged in and try again."
        return

    # ── Step 5: Assemble document ──────────────────────────────────────────────
    yield f"📄 **Step 5:** Assembling **{output_format.upper()}** document…"

    try:
        from app.services.assignment_assembler import assemble_assignment
        qa_json_str = json.dumps(qa_results, ensure_ascii=False)
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        # Strip timestamp suffix if present (e.g., MyFile_1780587438 → MyFile)
        base_name = re.sub(r'_\d{9,}$', '', base_name)
        out_filename = f"{base_name}_Completed"
        result = assemble_assignment(qa_json_str, out_filename, output_format)
        yield f"✅ **Done!** {result}"
    except Exception as e:
        yield f"❌ **Document assembly failed:** {e}"
