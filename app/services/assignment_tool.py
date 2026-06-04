"""
Jarvis Assignment Tool — Phase 1: Smart Question Extractor
==========================================================
STRICT ISOLATION: This module does NOT import from any other Jarvis tool module.
It uses only external libraries and standard Python.

Accessible via BOTH:
  - Frontend UI chat (POST /chat)
  - Voice interface (voice.py -> POST /chat)
through the unified /chat backend route (Rule #4 compliance).

Extraction Strategy (Hybrid — Best of Both Worlds):
  Track A — TEXT REGEX (Primary for structured PDFs):
    pdfplumber extracts raw text page-by-page ->
    Smart regex splits at question boundaries (1], 2], Q1., etc.) ->
    Handles sub-questions (i, ii, a, b) as children of parent question ->
    Very fast, no API cost, handles standard numbered formats

  Track B — VISION (Primary for image/scanned PDFs + figures):
    PyMuPDF renders each PDF page to a high-res image ->
    Groq Vision (llama-3.2-11b-vision) reads each page like a human ->
    Catches questions WITH figures, diagrams, tables ->
    Works on scanned + image-based PDFs

  Track C — LLM TEXT (Fallback when regex misses questions):
    Each page text sent to Groq LLM as separate request (no char cap) ->
    LLM reconstructs broken questions from PDF artifacts

Phase 1 Functions:
  extract_questions(pdf_path)  -- Extract ALL questions including those with figures
  list_assignments()           -- List PDFs found on Desktop/Documents/Downloads
"""

import os
import re
import json
import time
import base64
import io
from pathlib import Path
from groq import Groq
from app.core.config import settings

# ── LLM Client (isolated — no shared state) ───────────────────────────────────
_groq = Groq(api_key=settings.GROQ_API_KEY)

# ── Question type classifier vocabulary ───────────────────────────────────────
_TYPE_HINTS = {
    "mcq":          ["which of the following", "choose the correct", "select the",
                     "options:", "a)", "b)", "c)", "d)", "(a)", "(b)", "(c)", "(d)"],
    "numerical":    ["calculate", "compute", "find the", "show that", "determine",
                     "prove", "derive", "how many", "how much", "what is the value"],
    "code":         ["write a program", "write code", "implement", "code for",
                     "algorithm for", "function to", "write a function", "write a class",
                     "write an algorithm", "pseudocode"],
    "presentation": ["create a presentation", "make a ppt", "prepare slides",
                     "prepare a presentation", "powerpoint", "make slides"],
    "report":       ["write a report", "prepare a report", "create a report",
                     "research report", "detailed report", "project report"],
    "essay":        ["write an essay", "discuss in detail", "explain in detail",
                     "elaborate", "write about", "long answer", "in not less than"],
    "short_answer": ["what is", "who is", "when did", "where is", "define",
                     "state", "list", "name", "briefly explain", "short note",
                     "give one example", "mention", "what do you mean by"],
    "long_answer":  ["explain", "describe", "how does", "why is", "compare",
                     "differentiate", "analyze", "discuss", "with the help of diagram"],
}


def _resolve_pdf_path(raw_path: str) -> str | None:
    """Resolve PDF path: handles full paths, filenames, partial names."""
    if os.path.isabs(raw_path) and os.path.isfile(raw_path):
        return raw_path

    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    uploads_dir = Path(base_dir) / "data" / "uploads"
    
    search_dirs = [
        uploads_dir,
        Path.home() / "Desktop",
        Path.home() / "Documents",
        Path.home() / "Downloads",
    ]

    name_lower = raw_path.lower().strip()
    name_lower_pdf = name_lower if name_lower.endswith(".pdf") else name_lower + ".pdf"

    for folder in search_dirs:
        if not folder.exists():
            continue
        try:
            for f in folder.iterdir():
                fname = f.name.lower()
                if fname == name_lower or fname == name_lower_pdf or name_lower in fname:
                    return str(f)
        except PermissionError:
            continue

    return None


def _pdf_pages_to_text(pdf_path: str) -> list[str]:
    """Extract text from each PDF page separately. Returns list of page strings."""
    try:
        import pdfplumber
        pages = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                pages.append(text.strip() if text else "")
        if any(p.strip() for p in pages):
            return pages
    except ImportError:
        pass
    except Exception:
        pass

    try:
        import fitz
        doc = fitz.open(pdf_path)
        pages = [page.get_text().strip() for page in doc]
        doc.close()
        if any(p.strip() for p in pages):
            return pages
    except ImportError:
        pass
    except Exception:
        pass

    return []


def _pdf_pages_to_images(pdf_path: str, dpi: int = 150) -> list[str]:
    """Render each PDF page to a base64-encoded JPEG using PyMuPDF."""
    try:
        import fitz
        doc = fitz.open(pdf_path)
        images = []
        for page in doc:
            mat = fitz.Matrix(dpi / 72, dpi / 72)
            pix = page.get_pixmap(matrix=mat, colorspace=fitz.csRGB)
            try:
                from PIL import Image
                pil = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                buf = io.BytesIO()
                pil.save(buf, format="JPEG", quality=85)
                b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
            except ImportError:
                jpeg_bytes = pix.tobytes("jpeg")
                b64 = base64.b64encode(jpeg_bytes).decode("utf-8")
            images.append(b64)
        doc.close()
        return images
    except ImportError:
        return []
    except Exception:
        return []


def _classify_question_type(question_text: str) -> str:
    """Heuristically classify a question type based on its text."""
    lower = question_text.lower()
    for q_type, hints in _TYPE_HINTS.items():
        if any(hint in lower for hint in hints):
            return q_type
    word_count = len(question_text.split())
    return "long_answer" if word_count > 15 else "short_answer"


def _clean_text(text: str) -> str:
    """Clean up PDF text extraction artifacts."""
    # Collapse excessive whitespace while preserving line structure
    text = re.sub(r"[ \t]+", " ", text)
    # Join hyphenated line-breaks (PDF word wrap)
    text = re.sub(r"-\n(\w)", r"\1", text)
    # Join broken lines that are clearly mid-sentence (no ending punctuation)
    text = re.sub(r"(?<=[a-z,])\n(?=[a-z])", " ", text)
    return text.strip()


# ── TRACK A: Smart Regex Extractor ───────────────────────────────────────────

def _regex_extract_questions(page_text: str, page_num: int) -> list[dict]:
    """
    Smart regex-based question extractor for structured, numbered assignments.

    Handles these numbering formats:
      1]  2]  3]   (bracket style — common in Indian university assignments)
      1.  2.  3.   (period style)
      Q1. Q2. Q3.  (Q prefix)
      1)  2)  3)   (paren style)

    Sub-questions (i, ii, iii, a, b, c) are kept as part of parent question
    unless they appear standalone without parent context.
    """
    if not page_text.strip():
        return []

    text = _clean_text(page_text)
    questions = []

    # ── Pattern 1: "N]" style (e.g., "1] Question text" "2] Next question")
    bracket_pattern = re.compile(
        r"(?:^|\n)\s*(\d+)\]\s+(.+?)(?=\n\s*\d+\]|\Z)",
        re.DOTALL
    )
    bracket_matches = bracket_pattern.findall(text)

    if bracket_matches:
        for num, body in bracket_matches:
            body = body.strip()
            if len(body) < 5:
                continue
            # Extract sub-questions from the body
            questions.extend(_split_with_subquestions(num, body, page_num))
        return questions

    # ── Pattern 2: "N." style at line start
    period_pattern = re.compile(
        r"(?:^|\n)\s*(\d+)\.\s+(.+?)(?=\n\s*\d+\.|\Z)",
        re.DOTALL
    )
    period_matches = period_pattern.findall(text)

    if period_matches and len(period_matches) >= 2:
        for num, body in period_matches:
            body = body.strip()
            if len(body) < 5:
                continue
            questions.extend(_split_with_subquestions(num, body, page_num))
        return questions

    # ── Pattern 3: "Q1." or "Q1:" style
    q_pattern = re.compile(
        r"(?:^|\n)\s*Q\.?\s*(\d+)[\.:\)]\s+(.+?)(?=\n\s*Q\.?\s*\d+[\.:\)]|\Z)",
        re.DOTALL | re.IGNORECASE
    )
    q_matches = q_pattern.findall(text)

    if q_matches and len(q_matches) >= 2:
        for num, body in q_matches:
            body = body.strip()
            if len(body) < 5:
                continue
            questions.extend(_split_with_subquestions(num, body, page_num))
        return questions

    # ── Pattern 4: "1)" style
    paren_pattern = re.compile(
        r"(?:^|\n)\s*(\d+)\)\s+(.+?)(?=\n\s*\d+\)|\Z)",
        re.DOTALL
    )
    paren_matches = paren_pattern.findall(text)

    if paren_matches and len(paren_matches) >= 2:
        for num, body in paren_matches:
            body = body.strip()
            if len(body) < 5:
                continue
            questions.extend(_split_with_subquestions(num, body, page_num))
        return questions

    return []


def _split_with_subquestions(parent_num: str, body: str, page_num: int) -> list[dict]:
    """
    Given a parent question body, split out sub-questions (i, ii, iii, a, b, c)
    and return the parent + subs as separate question dicts.

    The parent question text is the part before the first sub-question.
    Sub-questions are labeled as "1i", "1ii", "1a", "1b" etc.
    """
    questions = []

    # Try to find sub-question markers: "i)" "ii)" "iii)" or "a)" "b)" "c)"
    sub_roman = re.compile(
        r"(?:^|\n)\s*(i{1,3}v?|vi{0,3}|ix|x|iv)[\.\)]\s*(.+?)(?=\n\s*(?:i{1,3}v?|vi{0,3}|ix|x|iv)[\.\)]|\Z)",
        re.DOTALL
    )
    sub_alpha = re.compile(
        r"(?:^|\n)\s*([a-e])[\.\)]\s*(.+?)(?=\n\s*[a-e][\.\)]|\Z)",
        re.DOTALL
    )

    roman_subs = sub_roman.findall(body)
    alpha_subs = sub_alpha.findall(body)

    # Determine which sub-pattern is active (if any)
    subs = roman_subs if len(roman_subs) >= 2 else (alpha_subs if len(alpha_subs) >= 2 else [])
    sub_pattern = sub_roman if roman_subs else sub_alpha

    if subs:
        # Find where first sub-question starts — everything before is the main question
        first_sub_match = sub_pattern.search(body)
        main_body = body[:first_sub_match.start()].strip() if first_sub_match else body

        # Add parent question (without sub-question text)
        if len(main_body) > 10:
            questions.append({
                "number": parent_num,
                "question": _clean_text(main_body),
                "type": _classify_question_type(main_body),
                "marks": _extract_marks(main_body),
                "has_figure": _has_figure_reference(main_body),
                "_source_page": page_num,
            })

        # Add each sub-question as its own entry
        for sub_num, sub_body in subs:
            sub_body = sub_body.strip()
            if len(sub_body) < 3:
                continue
            label = f"{parent_num}{sub_num}"
            questions.append({
                "number": label,
                "question": _clean_text(sub_body),
                "type": _classify_question_type(sub_body),
                "marks": _extract_marks(sub_body),
                "has_figure": _has_figure_reference(sub_body),
                "_source_page": page_num,
            })
    else:
        # No sub-questions — add the full body as-is
        questions.append({
            "number": parent_num,
            "question": _clean_text(body),
            "type": _classify_question_type(body),
            "marks": _extract_marks(body),
            "has_figure": _has_figure_reference(body),
            "_source_page": page_num,
        })

    return questions


def _extract_marks(text: str) -> int | None:
    """Extract marks from question text if mentioned."""
    m = re.search(r"\[(\d+)\s*(?:marks?|M|m)\]|\((\d+)\s*(?:marks?|M|m)\)", text, re.I)
    if m:
        return int(m.group(1) or m.group(2))
    return None


def _has_figure_reference(text: str) -> bool:
    """Check if question references a figure or diagram."""
    fig_kw = ["figure", "diagram", "shown below", "as shown", "the figure",
              "circuit diagram", "draw", "sketch", "waveform", "graph"]
    lower = text.lower()
    return any(kw in lower for kw in fig_kw)


# ── TRACK B: Vision Extractor ─────────────────────────────────────────────────

_VISION_PROMPT = """\
You are analyzing a page from a student assignment PDF.
Extract EVERY question on this page as separate items.

For EACH question, return a JSON object:
{
  "number": "<e.g. 1, 2, 1i, 1a — use the EXACT number shown>",
  "question": "<complete question text. For sub-questions (i, ii, a, b), include only that sub-question. If a figure is referenced, add [Figure: brief description]>",
  "type": "<mcq | short_answer | long_answer | numerical | code | essay | presentation | report>",
  "marks": <integer or null>,
  "has_figure": <true if question references a diagram/figure/circuit, else false>
}

CRITICAL RULES:
- Split sub-questions (i, ii, iii OR a, b, c) into SEPARATE objects
- Do NOT merge multiple numbered questions into one
- The parent question (e.g. Q3) body text before the subs is its own item
- If a question says "as shown in figure below" set has_figure=true

Output ONLY a JSON array. No other text. If no questions on page, output [].
"""


def _extract_via_vision(pdf_path: str) -> list[dict]:
    """
    Render each PDF page as an image and extract questions using Groq Vision.
    Best for: figures, diagrams, scanned PDFs, handwritten marks.
    """
    page_images = _pdf_pages_to_images(pdf_path)
    if not page_images:
        return []

    all_questions = []
    seen_keys = set()

    for page_num, b64_img in enumerate(page_images, start=1):
        try:
            response = _groq.chat.completions.create(
                model="llama-3.2-11b-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": _VISION_PROMPT},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{b64_img}"},
                            },
                        ],
                    }
                ],
                temperature=0.05,
                max_tokens=2500,
            )
            content = response.choices[0].message.content
            page_qs = _parse_llm_json_response(content)

            for q in page_qs:
                key = re.sub(r"\s+", " ", q["question"].lower()[:60]).strip()
                if key and key not in seen_keys and len(key) > 5:
                    seen_keys.add(key)
                    q["_source_page"] = page_num
                    all_questions.append(q)

        except Exception:
            continue

    return all_questions


# ── TRACK C: LLM Text Extractor (Fallback) ───────────────────────────────────

_LLM_TEXT_PROMPT = """\
You are analyzing text from ONE PAGE of a student assignment PDF.
The text may have PDF extraction artifacts (broken line-breaks, subscripts as plain text).

Extract EVERY question as a separate JSON object:
{
  "number": "<exact number shown: 1, 2, 1i, 1a, etc.>",
  "question": "<reconstruct the full question text, fixing line-break artifacts>",
  "type": "<mcq | short_answer | long_answer | numerical | code | essay | presentation | report>",
  "marks": <integer or null>,
  "has_figure": <true if question references a figure/diagram/circuit>
}

RULES:
- Split sub-questions (i/ii/iii or a/b/c) into SEPARATE objects
- Parent question body (before subs) is its own object
- Fix broken text: e.g. "Pe\\nwhen" -> "Pe when" (Pe is error probability)
- Output ONLY a JSON array. No other text. If no questions, output [].
"""


def _extract_via_llm_text(pdf_path: str) -> list[dict]:
    """LLM-based text extraction as fallback for when regex fails."""
    page_texts = _pdf_pages_to_text(pdf_path)
    if not page_texts:
        return []

    all_questions = []
    seen_keys = set()

    for page_num, page_text in enumerate(page_texts, start=1):
        if not page_text.strip() or len(page_text.strip()) < 20:
            continue
        try:
            response = _groq.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": _LLM_TEXT_PROMPT},
                    {"role": "user", "content": f"Page {page_num} text:\n\n{page_text}"}
                ],
                response_format={"type": "json_object"},
                max_tokens=3000,
                temperature=0.05,
            )
            content = response.choices[0].message.content
            page_qs = _parse_llm_json_response(content)

            for q in page_qs:
                key = re.sub(r"\s+", " ", q["question"].lower()[:60]).strip()
                if key and key not in seen_keys and len(key) > 5:
                    seen_keys.add(key)
                    q["_source_page"] = page_num
                    all_questions.append(q)
        except Exception:
            continue

    return all_questions


def _parse_llm_json_response(content: str) -> list[dict]:
    """Robustly parse an LLM response expected to be a JSON array of question dicts."""
    if not content or not content.strip():
        return []

    # Strip markdown code fences
    content = re.sub(r"```(?:json)?", "", content).strip().rstrip("`").strip()

    # Try direct parse
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        # Try to find a JSON array or object in the text
        arr_match = re.search(r"\[.*\]", content, re.DOTALL)
        obj_match = re.search(r"\{.*\}", content, re.DOTALL)
        if arr_match:
            try:
                parsed = json.loads(arr_match.group(0))
            except Exception:
                return []
        elif obj_match:
            try:
                parsed = json.loads(obj_match.group(0))
            except Exception:
                return []
        else:
            return []

    # Normalize to list
    if isinstance(parsed, list):
        questions = parsed
    elif isinstance(parsed, dict):
        for key in ["questions", "items", "data", "results"]:
            if key in parsed and isinstance(parsed[key], list):
                questions = parsed[key]
                break
        else:
            questions = [v for v in parsed.values() if isinstance(v, list)]
            questions = questions[0] if questions else []
    else:
        return []

    valid_types = set(_TYPE_HINTS.keys()) | {"long_answer", "short_answer"}

    cleaned = []
    for i, q in enumerate(questions):
        if not isinstance(q, dict):
            continue
        question_text = str(q.get("question", "")).strip()
        if len(question_text) < 5:
            continue
        q_type = str(q.get("type", "")).strip()
        if q_type not in valid_types:
            q_type = _classify_question_type(question_text)
        marks = q.get("marks")
        if marks is not None:
            try:
                marks = int(marks)
            except (ValueError, TypeError):
                marks = None
        cleaned.append({
            "number": q.get("number", i + 1),
            "question": question_text,
            "type": q_type,
            "marks": marks,
            "has_figure": bool(q.get("has_figure", False)),
        })

    return cleaned


def _merge_and_deduplicate(regex_qs: list[dict], vision_qs: list[dict],
                            llm_qs: list[dict]) -> list[dict]:
    """
    Merge questions from all three tracks.
    Priority: regex > vision > llm text.
    A question is a duplicate if 60%+ of the first 60 words overlap.
    """
    final = list(regex_qs)
    existing_keys = {
        re.sub(r"\s+", " ", q["question"].lower()[:60]).strip()
        for q in final
    }

    def is_duplicate(new_q: dict) -> bool:
        new_key = re.sub(r"\s+", " ", new_q["question"].lower()[:60]).strip()
        new_words = set(new_key.split())
        for ek in existing_keys:
            ek_words = set(ek.split())
            if not new_words or not ek_words:
                continue
            overlap = len(new_words & ek_words) / max(len(new_words), len(ek_words))
            if overlap > 0.55:
                return True
        return False

    for q in vision_qs:
        if not is_duplicate(q):
            existing_keys.add(re.sub(r"\s+", " ", q["question"].lower()[:60]).strip())
            final.append(q)

    for q in llm_qs:
        if not is_duplicate(q):
            existing_keys.add(re.sub(r"\s+", " ", q["question"].lower()[:60]).strip())
            final.append(q)

    # Sort by page, then by numeric part of question number
    def sort_key(q):
        page = q.get("_source_page", 99)
        num_str = re.sub(r"[^0-9]", "", str(q.get("number", "99")))
        num = int(num_str) if num_str else 99
        return (page, num, str(q.get("number", "")))

    final.sort(key=sort_key)
    return final


# ── PUBLIC TOOL FUNCTIONS ─────────────────────────────────────────────────────

def extract_questions(pdf_path: str) -> str:
    """
    Extract ALL questions from an assignment PDF using a 3-track hybrid system.

    Track A — Smart Regex (instant, no API cost):
      Splits at numbered question boundaries (1] 2] 3] or 1. 2. 3.)
      Handles sub-questions (i, ii, a, b) correctly

    Track B — Vision (Groq Vision per page):
      Sees figures, diagrams, tables embedded in questions
      Works on scanned/image-based PDFs

    Track C — LLM Text (Groq text LLM per page, fallback):
      Catches questions that regex patterns miss
      Reconstructs broken PDF text artifacts

    Results merged, de-duplicated, and returned as structured JSON.

    Args:
        pdf_path: Full path or filename (auto-searched Desktop/Documents/Downloads)
    """
    try:
        # Step 1: Resolve path
        resolved = _resolve_pdf_path(pdf_path)
        if not resolved:
            return (
                f"Could not find '{pdf_path}'. "
                f"Make sure the PDF is on your Desktop, Documents, or Downloads. "
                f"Say 'list my assignments' to see all available PDFs."
            )

        filename = os.path.basename(resolved)

        # Step 2: Page count
        page_count = 0
        try:
            import fitz
            doc = fitz.open(resolved)
            page_count = len(doc)
            doc.close()
        except Exception:
            try:
                import pdfplumber
                with pdfplumber.open(resolved) as pdf:
                    page_count = len(pdf.pages)
            except Exception:
                page_count = 0

        pages_str = f"{page_count}-page " if page_count > 0 else ""

        # Step 3: Track A — Regex extraction (primary, instant)
        page_texts = _pdf_pages_to_text(resolved)
        regex_questions = []
        for page_num, page_text in enumerate(page_texts, start=1):
            regex_questions.extend(_regex_extract_questions(page_text, page_num))

        # Step 4: Track B — Vision extraction (always, for figures)
        vision_questions = _extract_via_vision(resolved)

        # Step 5: Track C — LLM text fallback (only if regex + vision both got < expected)
        expected_min = max(2, len(page_texts))  # expect at least 1 Q per page
        llm_questions = []
        merged_so_far = _merge_and_deduplicate(regex_questions, vision_questions, [])
        if len(merged_so_far) < expected_min:
            llm_questions = _extract_via_llm_text(resolved)

        # Step 6: Final merge
        questions = _merge_and_deduplicate(regex_questions, vision_questions, llm_questions)

        # Step 7: Last-resort if still nothing
        if not questions:
            raw_text = "\n\n".join(page_texts)
            questions = _regex_extract_questions(raw_text, 1) or []

        if not questions:
            raw_preview = "\n\n".join(page_texts)[:600] if page_texts else ""
            return (
                f"Found the {pages_str}PDF '{filename}' but could not identify questions. "
                f"The PDF may be fully image-based with no recognizable question patterns."
                + (f"\n\nRaw text preview:\n{raw_preview}..." if raw_preview else "")
            )

        # Step 8: Clean internal keys before output
        for q in questions:
            q.pop("_source_page", None)

        # Step 9: Format output
        total = len(questions)
        type_counts: dict[str, int] = {}
        figure_count = 0
        for q in questions:
            qt = q.get("type", "unknown")
            type_counts[qt] = type_counts.get(qt, 0) + 1
            if q.get("has_figure"):
                figure_count += 1

        type_summary = ", ".join(f"{count} {qtype}" for qtype, count in type_counts.items())
        figure_note = f" ({figure_count} with figures/diagrams)" if figure_count > 0 else ""

        source_note = f"[Regex: {len(regex_questions)}  Vision: {len(vision_questions)}  LLM: {len(llm_questions)}  Final unique: {total}]"

        question_lines = []
        for q in questions:
            num = q.get("number", "?")
            text = q.get("question", "")
            qtype = q.get("type", "")
            marks = q.get("marks")
            has_fig = q.get("has_figure", False)
            mark_str = f" [{marks}M]" if marks else ""
            fig_str = " [+figure]" if has_fig else ""
            preview = text[:140] + ("..." if len(text) > 140 else "")
            question_lines.append(f"  Q{num}{mark_str}{fig_str} [{qtype}]: {preview}")

        question_list_str = "\n".join(question_lines)
        questions_json = json.dumps(questions, indent=2, ensure_ascii=False)

        result = (
            f"Assignment analysis complete for '{filename}' ({pages_str}PDF).\n"
            f"Found {total} question(s): {type_summary}{figure_note}.\n"
            f"{source_note}\n\n"
            f"Questions:\n{question_list_str}\n\n"
            f"QUESTIONS_JSON:\n{questions_json}"
        )
        return result

    except Exception as e:
        return f"Assignment extraction failed: {str(e)}"


def list_assignments() -> str:
    """Scan Desktop, Documents, and Downloads for PDF files."""
    try:
        search_dirs = [
            Path.home() / "Desktop",
            Path.home() / "Documents",
            Path.home() / "Downloads",
        ]

        found_pdfs = []
        for folder in search_dirs:
            if not folder.exists():
                continue
            try:
                for f in folder.iterdir():
                    if f.suffix.lower() == ".pdf":
                        stat = f.stat()
                        size_kb = stat.st_size // 1024
                        mod_time = time.strftime("%d %b %Y", time.localtime(stat.st_mtime))
                        found_pdfs.append({
                            "name": f.name,
                            "path": str(f),
                            "folder": folder.name,
                            "size_kb": size_kb,
                            "modified": mod_time,
                        })
            except PermissionError:
                continue

        if not found_pdfs:
            return (
                "No PDF files found on your Desktop, Documents, or Downloads. "
                "Please save your assignment PDF there."
            )

        lines = [f"Found {len(found_pdfs)} PDF file(s):\n"]
        for pdf in found_pdfs:
            lines.append(
                f"  - {pdf['name']} ({pdf['size_kb']} KB) | {pdf['folder']} | Modified: {pdf['modified']}"
            )
            lines.append(f"    Path: {pdf['path']}")

        lines.append("\nTo extract questions, say: 'extract questions from <filename>'")
        return "\n".join(lines)

    except Exception as e:
        return f"Could not list PDFs: {str(e)}"
