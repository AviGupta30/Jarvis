# task_ledger + test_task_resumption

> 28 nodes · cohesion 0.12

## Key Concepts

- **test_task_resumption.py** (23 connections) — `test_task_resumption.py`
- **task_ledger.py** (15 connections) — `app/services/task_ledger.py`
- **_load_ledger()** (10 connections) — `app/services/task_ledger.py`
- **get_task_ledger_for_prompt()** (8 connections) — `app/services/task_ledger.py`
- **get_recent_tasks_raw()** (7 connections) — `app/services/task_ledger.py`
- **log_task()** (7 connections) — `app/services/task_ledger.py`
- **find_resumable_task()** (5 connections) — `app/services/task_ledger.py`
- **get_recent_tasks()** (5 connections) — `app/services/task_ledger.py`
- **_save_ledger()** (5 connections) — `app/services/task_ledger.py`
- **update_task()** (5 connections) — `app/services/task_ledger.py`
- **_call_planner()** (4 connections) — `app/services/planner.py`
- **_ensure_ledger_file()** (4 connections) — `app/services/task_ledger.py`
- **Ask the LLM to produce a step-by-step plan.** (1 connections) — `app/services/planner.py`
- **task_ledger.py — Jarvis Task Context Ledger…** (1 connections) — `app/services/task_ledger.py`
- **Return a formatted string of the last N tasks, suitable for display or speech.…** (1 connections) — `app/services/task_ledger.py`
- **Return the last N raw ledger entries as a list of dicts. Used internally by…** (1 connections) — `app/services/task_ledger.py`
- **Fuzzy-search the ledger for the most recent resumable task matching the query.…** (1 connections) — `app/services/task_ledger.py`
- **Update an existing ledger entry by task_id. Used after successfully appending…** (1 connections) — `app/services/task_ledger.py`
- **Returns a compact, LLM-friendly summary of recent tasks for injection into…** (1 connections) — `app/services/task_ledger.py`
- **Create the data directory and ledger file if they don't exist.** (1 connections) — `app/services/task_ledger.py`
- **Load the ledger from disk. Returns empty list on any error.** (1 connections) — `app/services/task_ledger.py`
- **Persist the ledger to disk. Caps at _MAX_ENTRIES (FIFO).** (1 connections) — `app/services/task_ledger.py`
- **Record a completed (or in-progress) task to the persistent ledger. Args:…** (1 connections) — `app/services/task_ledger.py`
- **_backup_ledger()** (1 connections) — `test_task_resumption.py`
- **check()** (1 connections) — `test_task_resumption.py`
- *... and 3 more nodes in this community*

## Relationships

- [assignment_tool + assignment_humanizer](assignment_tool_+_assignment_humanizer.md) (8 shared connections)
- [chat + rag_memory](chat_+_rag_memory.md) (6 shared connections)
- [resume_detector](resume_detector.md) (3 shared connections)
- [tools](tools.md) (2 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (1 shared connections)
- [syllabus_auditor](syllabus_auditor.md) (1 shared connections)
- [calendar_tool](calendar_tool.md) (1 shared connections)
- [chat-routing + CLAUDE](chat-routing_+_CLAUDE.md) (1 shared connections)
- [main + screen_vision](main_+_screen_vision.md) (1 shared connections)
- [gmail_tool + download_kokoro](gmail_tool_+_download_kokoro.md) (1 shared connections)
- [dump_wa_ui + test_wa](dump_wa_ui_+_test_wa.md) (1 shared connections)

## Source Files

- `app/services/planner.py`
- `app/services/task_ledger.py`
- `test_task_resumption.py`

## Audit Trail

- EXTRACTED: 67 (96%)
- INFERRED: 3 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*