# assignment_pipeline

> 20 nodes · cohesion 0.18

## Key Concepts

- **assignment_pipeline.py** (22 connections) — `app/services/assignment_pipeline.py`
- **_browser_thread()** (13 connections) — `app/services/assignment_pipeline.py`
- **do_assignment()** (10 connections) — `app/services/assignment_pipeline.py`
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
- **Master orchestrator. Uses a background thread for all Playwright code. Yields…** (1 connections) — `app/services/assignment_pipeline.py`

## Relationships

- [assignment_tool](assignment_tool.md) (4 shared connections)
- [voice_agent + download_kokoro](voice_agent_+_download_kokoro.md) (3 shared connections)
- [message_reader + thread_extractor](message_reader_+_thread_extractor.md) (3 shared connections)
- [assignment_assembler](assignment_assembler.md) (2 shared connections)
- [assignment](assignment.md) (1 shared connections)
- [tool-registry + tools](tool-registry_+_tools.md) (1 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (1 shared connections)
- [tools](tools.md) (1 shared connections)

## Source Files

- `app/services/assignment_pipeline.py`

## Audit Trail

- EXTRACTED: 45 (90%)
- INFERRED: 5 (10%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*