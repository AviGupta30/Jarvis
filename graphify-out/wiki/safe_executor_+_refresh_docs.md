# safe_executor + refresh_docs

> 34 nodes · cohesion 0.08

## Key Concepts

- **sys** (30 connections)
- **safe_executor.py** (22 connections) — `app/services/safe_executor.py`
- **refresh_docs.py** (15 connections) — `scripts/refresh_docs.py`
- **SecurityError** (8 connections) — `app/services/safe_executor.py`
- **collections** (8 connections)
- **SafetyVisitor** (6 connections) — `app/services/safe_executor.py`
- **_safe_import()** (4 connections) — `app/services/safe_executor.py`
- **_safe_open()** (4 connections) — `app/services/safe_executor.py`
- **_validate_code()** (4 connections) — `app/services/safe_executor.py`
- **auto_block()** (4 connections) — `scripts/refresh_docs.py`
- **_js_symbols()** (3 connections) — `scripts/refresh_docs.py`
- **label_communities()** (3 connections) — `scripts/refresh_docs.py`
- **_py_symbols()** (3 connections) — `scripts/refresh_docs.py`
- **test_routing.py** (3 connections) — `scripts/test_routing.py`
- **.visit_Call()** (2 connections) — `app/services/safe_executor.py`
- **.visit_Import()** (2 connections) — `app/services/safe_executor.py`
- **.visit_ImportFrom()** (2 connections) — `app/services/safe_executor.py`
- **ast** (2 connections)
- **Path** (2 connections)
- **refresh_graph()** (2 connections) — `scripts/refresh_docs.py`
- **write_docs()** (2 connections) — `scripts/refresh_docs.py`
- **test_exec.py** (2 connections) — `test_exec.py`
- **Exception** (1 connections)
- **Safe Code Executor for Jarvis ------------------------------- Runs LLM-…** (1 connections) — `app/services/safe_executor.py`
- **Restricted open(): blocks writes to system paths.** (1 connections) — `app/services/safe_executor.py`
- *... and 9 more nodes in this community*

## Relationships

- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (11 shared connections)
- [assignment_humanizer + task_ledger](assignment_humanizer_+_task_ledger.md) (6 shared connections)
- [social_content_manager + content-tools](social_content_manager_+_content-tools.md) (3 shared connections)
- [message_reader + thread_extractor](message_reader_+_thread_extractor.md) (3 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (2 shared connections)
- [prompt_enhancer_button](prompt_enhancer_button.md) (2 shared connections)
- [voice_agent](voice_agent.md) (2 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (2 shared connections)
- [assignment_answers](assignment_answers.md) (1 shared connections)
- [smart_navigator + ssml_processor](smart_navigator_+_ssml_processor.md) (1 shared connections)
- [screen_vision + screen_reader](screen_vision_+_screen_reader.md) (1 shared connections)
- [voice](voice.md) (1 shared connections)

## Source Files

- `app/services/safe_executor.py`
- `patch_window.py`
- `scripts/refresh_docs.py`
- `scripts/test_routing.py`
- `test_exec.py`

## Audit Trail

- EXTRACTED: 98 (98%)
- INFERRED: 2 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*