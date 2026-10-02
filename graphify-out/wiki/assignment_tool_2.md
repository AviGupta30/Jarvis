# assignment_tool

> 18 nodes · cohesion 0.12

## Key Concepts

- **extract_questions()** (12 connections) — `app/services/assignment_tool.py`
- **_merge_and_deduplicate()** (6 connections) — `app/services/assignment_tool.py`
- **_extract_via_llm_text()** (5 connections) — `app/services/assignment_tool.py`
- **_extract_via_vision()** (5 connections) — `app/services/assignment_tool.py`
- **_parse_llm_json_response()** (5 connections) — `app/services/assignment_tool.py`
- **_classify_question_type()** (4 connections) — `app/services/assignment_tool.py`
- **_pdf_pages_to_text()** (4 connections) — `app/services/assignment_tool.py`
- **_pdf_pages_to_images()** (3 connections) — `app/services/assignment_tool.py`
- **is_duplicate()** (1 connections) — `app/services/assignment_tool.py`
- **sort_key()** (1 connections) — `app/services/assignment_tool.py`
- **Extract text from each PDF page separately. Returns list of page strings.** (1 connections) — `app/services/assignment_tool.py`
- **Render each PDF page to a base64-encoded JPEG using PyMuPDF.** (1 connections) — `app/services/assignment_tool.py`
- **Heuristically classify a question type based on its text.** (1 connections) — `app/services/assignment_tool.py`
- **Render each PDF page as an image and extract questions using Groq Vision. Best…** (1 connections) — `app/services/assignment_tool.py`
- **LLM-based text extraction as fallback for when regex fails.** (1 connections) — `app/services/assignment_tool.py`
- **Robustly parse an LLM response expected to be a JSON array of question dicts.** (1 connections) — `app/services/assignment_tool.py`
- **Merge questions from all three tracks. Priority: regex > vision > llm text. A…** (1 connections) — `app/services/assignment_tool.py`
- **Extract ALL questions from an assignment PDF using a 3-track hybrid system.…** (1 connections) — `app/services/assignment_tool.py`

## Relationships

- [social_content_manager + ui_inspector](social_content_manager_+_ui_inspector.md) (8 shared connections)
- [assignment + assignment_answers](assignment_+_assignment_answers.md) (4 shared connections)
- [assignment_tool](assignment_tool.md) (2 shared connections)
- [assignment_pipeline](assignment_pipeline.md) (1 shared connections)
- [tools](tools.md) (1 shared connections)

## Source Files

- `app/services/assignment_tool.py`

## Audit Trail

- EXTRACTED: 31 (89%)
- INFERRED: 4 (11%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*