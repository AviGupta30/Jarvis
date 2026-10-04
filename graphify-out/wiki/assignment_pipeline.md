# assignment_pipeline

> 18 nodes · cohesion 0.20

## Key Concepts

- **assignment_pipeline.py** (22 connections) — `app/services/assignment_pipeline.py`
- **_browser_thread()** (13 connections) — `app/services/assignment_pipeline.py`
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
- **Try to use Edge Default profile, then Chrome, fallback to Jarvis custom profile.** (1 connections) — `app/services/assignment_pipeline.py`

## Relationships

- [assignment_tool + assignment_pipeline](assignment_tool_+_assignment_pipeline.md) (4 shared connections)
- [assignment_humanizer + task_ledger](assignment_humanizer_+_task_ledger.md) (2 shared connections)
- [social_content_manager + content-tools](social_content_manager_+_content-tools.md) (1 shared connections)
- [smart_navigator + ssml_processor](smart_navigator_+_ssml_processor.md) (1 shared connections)
- [message_reader + thread_extractor](message_reader_+_thread_extractor.md) (1 shared connections)
- [server](server.md) (1 shared connections)
- [assignment_assembler](assignment_assembler.md) (1 shared connections)

## Source Files

- `app/services/assignment_pipeline.py`

## Audit Trail

- EXTRACTED: 41 (98%)
- INFERRED: 1 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*