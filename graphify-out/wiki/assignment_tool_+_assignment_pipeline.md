# assignment_tool + assignment_pipeline

> 62 nodes · cohesion 0.05

## Key Concepts

- **assignment_tool.py** (25 connections) — `app/services/assignment_tool.py`
- **assignment_pipeline.py** (22 connections) — `app/services/assignment_pipeline.py`
- **_browser_thread()** (13 connections) — `app/services/assignment_pipeline.py`
- **extract_questions()** (12 connections) — `app/services/assignment_tool.py`
- **do_assignment()** (11 connections) — `app/services/assignment_pipeline.py`
- **_resolve_pdf_path()** (8 connections) — `app/services/assignment_tool.py`
- **_split_with_subquestions()** (7 connections) — `app/services/assignment_tool.py`
- **Assignment solver (5 phases)** (7 connections) — `docs/features/assignment.md`
- **_merge_and_deduplicate()** (6 connections) — `app/services/assignment_tool.py`
- **_extract_via_llm_text()** (5 connections) — `app/services/assignment_tool.py`
- **_extract_via_vision()** (5 connections) — `app/services/assignment_tool.py`
- **list_assignments()** (5 connections) — `app/services/assignment_tool.py`
- **_parse_llm_json_response()** (5 connections) — `app/services/assignment_tool.py`
- **_regex_extract_questions()** (5 connections) — `app/services/assignment_tool.py`
- **Phases** (5 connections) — `docs/features/assignment.md`
- **Triggers** (5 connections) — `docs/features/assignment.md`
- **_find_el()** (4 connections) — `app/services/assignment_pipeline.py`
- **_get_browser_ctx()** (4 connections) — `app/services/assignment_pipeline.py`
- **_humanize_browser()** (4 connections) — `app/services/assignment_pipeline.py`
- **_classify_question_type()** (4 connections) — `app/services/assignment_tool.py`
- **_clean_text()** (4 connections) — `app/services/assignment_tool.py`
- **_pdf_pages_to_text()** (4 connections) — `app/services/assignment_tool.py`
- **_get_answer()** (3 connections) — `app/services/assignment_pipeline.py`
- **_groq_answer()** (3 connections) — `app/services/assignment_pipeline.py`
- **_groq_humanize()** (3 connections) — `app/services/assignment_pipeline.py`
- *... and 37 more nodes in this community*

## Relationships

- [benchmark + download_kokoro](benchmark_+_download_kokoro.md) (6 shared connections)
- [assignment_assembler + smart_navigator](assignment_assembler_+_smart_navigator.md) (4 shared connections)
- [tools](tools.md) (3 shared connections)
- [assignment_answers](assignment_answers.md) (3 shared connections)
- [dump_wa_ui + test_wa](dump_wa_ui_+_test_wa.md) (2 shared connections)
- [test_lru](test_lru.md) (2 shared connections)
- [tool-registry + vector_store](tool-registry_+_vector_store.md) (2 shared connections)
- [server + persistence](server_+_persistence.md) (1 shared connections)
- [chat + llm](chat_+_llm.md) (1 shared connections)
- [repair](repair.md) (1 shared connections)
- [safe_executor](safe_executor.md) (1 shared connections)
- [assignment_humanizer](assignment_humanizer.md) (1 shared connections)

## Source Files

- `app/services/assignment_pipeline.py`
- `app/services/assignment_tool.py`
- `docs/features/assignment.md`

## Audit Trail

- EXTRACTED: 112 (88%)
- INFERRED: 16 (12%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*