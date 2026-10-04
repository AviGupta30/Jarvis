# task_ledger + resume_detector

> 43 nodes · cohesion 0.07

## Key Concepts

- **test_task_resumption.py** (23 connections) — `test_task_resumption.py`
- **task_ledger.py** (15 connections) — `app/services/task_ledger.py`
- **resume_detector.py** (11 connections) — `app/services/resume_detector.py`
- **detect_resume_intent()** (11 connections) — `app/services/resume_detector.py`
- **_load_ledger()** (10 connections) — `app/services/task_ledger.py`
- **get_recent_tasks_raw()** (7 connections) — `app/services/task_ledger.py`
- **log_task()** (7 connections) — `app/services/task_ledger.py`
- **get_resume_context_string()** (5 connections) — `app/services/resume_detector.py`
- **find_resumable_task()** (5 connections) — `app/services/task_ledger.py`
- **get_recent_tasks()** (5 connections) — `app/services/task_ledger.py`
- **_save_ledger()** (5 connections) — `app/services/task_ledger.py`
- **update_task()** (5 connections) — `app/services/task_ledger.py`
- **_ensure_ledger_file()** (4 connections) — `app/services/task_ledger.py`
- **uuid** (4 connections)
- **_extract_task_resource()** (3 connections) — `app/services/resume_detector.py`
- **_find_best_task_match()** (3 connections) — `app/services/resume_detector.py`
- **_has_continuation_verb()** (3 connections) — `app/services/resume_detector.py`
- **_has_fresh_task_indicator()** (3 connections) — `app/services/resume_detector.py`
- **_has_reference_phrase()** (3 connections) — `app/services/resume_detector.py`
- **shutil** (3 connections)
- **resume_detector.py — Jarvis Resume Intent Classifier…** (1 connections) — `app/services/resume_detector.py`
- **Return True if the text contains a strong resume-intent reference phrase.** (1 connections) — `app/services/resume_detector.py`
- **Return True if the text clearly indicates a FRESH (new) task, not a…** (1 connections) — `app/services/resume_detector.py`
- **Return True if the text contains an action verb suggesting continuation.** (1 connections) — `app/services/resume_detector.py`
- **Extract the most human-readable resource identifier from a ledger entry. E.g.,…** (1 connections) — `app/services/resume_detector.py`
- *... and 18 more nodes in this community*

## Relationships

- [chat](chat.md) (4 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (4 shared connections)
- [jarvis_overlay + prompt_overlay](jarvis_overlay_+_prompt_overlay.md) (4 shared connections)
- [server + persistence](server_+_persistence.md) (3 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (3 shared connections)
- [llm-personality + ARCHITECTURE](llm-personality_+_ARCHITECTURE.md) (2 shared connections)
- [tools + window_layout](tools_+_window_layout.md) (2 shared connections)
- [assignment_assembler + smart_navigator](assignment_assembler_+_smart_navigator.md) (1 shared connections)
- [calendar_tool + email-calendar](calendar_tool_+_email-calendar.md) (1 shared connections)
- [main](main.md) (1 shared connections)
- [file_ops](file_ops.md) (1 shared connections)
- [gmail_tool](gmail_tool.md) (1 shared connections)

## Source Files

- `app/services/resume_detector.py`
- `app/services/task_ledger.py`
- `test_task_resumption.py`

## Audit Trail

- EXTRACTED: 90 (96%)
- INFERRED: 4 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*