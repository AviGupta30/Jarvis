# assignment_pipeline + assignment_tool

> 38 nodes · cohesion 0.08

## Key Concepts

- **assignment_pipeline.py** (22 connections) — `app/services/assignment_pipeline.py`
- **_browser_thread()** (13 connections) — `app/services/assignment_pipeline.py`
- **extract_questions()** (12 connections) — `app/services/assignment_tool.py`
- **do_assignment()** (10 connections) — `app/services/assignment_pipeline.py`
- **_resolve_pdf_path()** (8 connections) — `app/services/assignment_tool.py`
- **Assignment solver (5 phases)** (7 connections) — `docs/features/assignment.md`
- **_merge_and_deduplicate()** (6 connections) — `app/services/assignment_tool.py`
- **list_assignments()** (5 connections) — `app/services/assignment_tool.py`
- **Phases** (5 connections) — `docs/features/assignment.md`
- **Triggers** (5 connections) — `docs/features/assignment.md`
- **_find_el()** (4 connections) — `app/services/assignment_pipeline.py`
- **_get_browser_ctx()** (4 connections) — `app/services/assignment_pipeline.py`
- **_humanize_browser()** (4 connections) — `app/services/assignment_pipeline.py`
- **_get_answer()** (3 connections) — `app/services/assignment_pipeline.py`
- **_groq_answer()** (3 connections) — `app/services/assignment_pipeline.py`
- **_groq_humanize()** (3 connections) — `app/services/assignment_pipeline.py`
- **Queue** (3 connections)
- **_type_into()** (3 connections) — `app/services/assignment_pipeline.py`
- **_upload_file()** (3 connections) — `app/services/assignment_pipeline.py`
- **_wait_done()** (2 connections) — `app/services/assignment_pipeline.py`
- **Jarvis Assignment Tool — Phase 5: End-to-End Pipeline…** (1 connections) — `app/services/assignment_pipeline.py`
- **Try copy button, then DOM, then Groq vision.** (1 connections) — `app/services/assignment_pipeline.py`
- **Groq API fallback for a single question.** (1 connections) — `app/services/assignment_pipeline.py`
- **Groq API humanization fallback.** (1 connections) — `app/services/assignment_pipeline.py`
- **Runs all Playwright browser automation in a separate thread. Puts status…** (1 connections) — `app/services/assignment_pipeline.py`
- *... and 13 more nodes in this community*

## Relationships

- [assignment_tool](assignment_tool.md) (8 shared connections)
- [benchmark + server](benchmark_+_server.md) (4 shared connections)
- [assignment_assembler + smart_navigator](assignment_assembler_+_smart_navigator.md) (3 shared connections)
- [tools](tools.md) (3 shared connections)
- [assignment_answers](assignment_answers.md) (3 shared connections)
- [chat + tools](chat_+_tools.md) (2 shared connections)
- [nlp_extractor + download_kokoro](nlp_extractor_+_download_kokoro.md) (1 shared connections)
- [assignment_humanizer](assignment_humanizer.md) (1 shared connections)

## Source Files

- `app/services/assignment_pipeline.py`
- `app/services/assignment_tool.py`
- `docs/features/assignment.md`

## Audit Trail

- EXTRACTED: 69 (82%)
- INFERRED: 15 (18%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*