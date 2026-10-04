# assignment_tool

> 20 nodes · cohesion 0.15

## Key Concepts

- **assignment_tool.py** (25 connections) — `app/services/assignment_tool.py`
- **_split_with_subquestions()** (7 connections) — `app/services/assignment_tool.py`
- **_extract_via_vision()** (5 connections) — `app/services/assignment_tool.py`
- **_parse_llm_json_response()** (5 connections) — `app/services/assignment_tool.py`
- **_regex_extract_questions()** (5 connections) — `app/services/assignment_tool.py`
- **_classify_question_type()** (4 connections) — `app/services/assignment_tool.py`
- **_clean_text()** (4 connections) — `app/services/assignment_tool.py`
- **_extract_marks()** (3 connections) — `app/services/assignment_tool.py`
- **_has_figure_reference()** (3 connections) — `app/services/assignment_tool.py`
- **_pdf_pages_to_images()** (3 connections) — `app/services/assignment_tool.py`
- **Jarvis Assignment Tool — Phase 1: Smart Question Extractor…** (1 connections) — `app/services/assignment_tool.py`
- **Render each PDF page to a base64-encoded JPEG using PyMuPDF.** (1 connections) — `app/services/assignment_tool.py`
- **Heuristically classify a question type based on its text.** (1 connections) — `app/services/assignment_tool.py`
- **Clean up PDF text extraction artifacts.** (1 connections) — `app/services/assignment_tool.py`
- **Smart regex-based question extractor for structured, numbered assignments.…** (1 connections) — `app/services/assignment_tool.py`
- **Given a parent question body, split out sub-questions (i, ii, iii, a, b, c) and…** (1 connections) — `app/services/assignment_tool.py`
- **Extract marks from question text if mentioned.** (1 connections) — `app/services/assignment_tool.py`
- **Check if question references a figure or diagram.** (1 connections) — `app/services/assignment_tool.py`
- **Render each PDF page as an image and extract questions using Groq Vision. Best…** (1 connections) — `app/services/assignment_tool.py`
- **Robustly parse an LLM response expected to be a JSON array of question dicts.** (1 connections) — `app/services/assignment_tool.py`

## Relationships

- [assignment_tool](assignment_tool.md) (7 shared connections)
- [voice_agent + download_kokoro](voice_agent_+_download_kokoro.md) (4 shared connections)
- [message_reader + thread_extractor](message_reader_+_thread_extractor.md) (2 shared connections)
- [dynamic_skill + planner](dynamic_skill_+_planner.md) (2 shared connections)
- [repair + assignment_humanizer](repair_+_assignment_humanizer.md) (1 shared connections)
- [assignment_humanizer](assignment_humanizer.md) (1 shared connections)
- [assignment](assignment.md) (1 shared connections)

## Source Files

- `app/services/assignment_tool.py`

## Audit Trail

- EXTRACTED: 46 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*