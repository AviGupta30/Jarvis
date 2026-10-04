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

- [assignment_tool + assignment_pipeline](assignment_tool_+_assignment_pipeline.md) (6 shared connections)
- [assignment_tool](assignment_tool.md) (3 shared connections)
- [assignment_humanizer + task_ledger](assignment_humanizer_+_task_ledger.md) (2 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (2 shared connections)
- [social_content_manager + content-tools](social_content_manager_+_content-tools.md) (1 shared connections)
- [smart_navigator + ssml_processor](smart_navigator_+_ssml_processor.md) (1 shared connections)
- [message_reader + thread_extractor](message_reader_+_thread_extractor.md) (1 shared connections)
- [screen_vision + screen_reader](screen_vision_+_screen_reader.md) (1 shared connections)
- [assignment_answers](assignment_answers.md) (1 shared connections)

## Source Files

- `app/services/assignment_tool.py`

## Audit Trail

- EXTRACTED: 46 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*