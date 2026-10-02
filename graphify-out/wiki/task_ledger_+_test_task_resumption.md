# task_ledger + test_task_resumption

> 24 nodes · cohesion 0.14

## Key Concepts

- **test_task_resumption.py** (23 connections) — `test_task_resumption.py`
- **task_ledger.py** (15 connections) — `app/services/task_ledger.py`
- **_load_ledger()** (10 connections) — `app/services/task_ledger.py`
- **get_recent_tasks_raw()** (7 connections) — `app/services/task_ledger.py`
- **log_task()** (7 connections) — `app/services/task_ledger.py`
- **find_resumable_task()** (5 connections) — `app/services/task_ledger.py`
- **get_recent_tasks()** (5 connections) — `app/services/task_ledger.py`
- **_save_ledger()** (5 connections) — `app/services/task_ledger.py`
- **update_task()** (5 connections) — `app/services/task_ledger.py`
- **_ensure_ledger_file()** (4 connections) — `app/services/task_ledger.py`
- **task_ledger.py — Jarvis Task Context Ledger…** (1 connections) — `app/services/task_ledger.py`
- **Return a formatted string of the last N tasks, suitable for display or speech.…** (1 connections) — `app/services/task_ledger.py`
- **Return the last N raw ledger entries as a list of dicts. Used internally by…** (1 connections) — `app/services/task_ledger.py`
- **Fuzzy-search the ledger for the most recent resumable task matching the query.…** (1 connections) — `app/services/task_ledger.py`
- **Update an existing ledger entry by task_id. Used after successfully appending…** (1 connections) — `app/services/task_ledger.py`
- **Create the data directory and ledger file if they don't exist.** (1 connections) — `app/services/task_ledger.py`
- **Load the ledger from disk. Returns empty list on any error.** (1 connections) — `app/services/task_ledger.py`
- **Persist the ledger to disk. Caps at _MAX_ENTRIES (FIFO).** (1 connections) — `app/services/task_ledger.py`
- **Record a completed (or in-progress) task to the persistent ledger. Args:…** (1 connections) — `app/services/task_ledger.py`
- **_backup_ledger()** (1 connections) — `test_task_resumption.py`
- **check()** (1 connections) — `test_task_resumption.py`
- **test_task_resumption.py -- Comprehensive automated verification for the Task…** (1 connections) — `test_task_resumption.py`
- **_restore_ledger()** (1 connections) — `test_task_resumption.py`
- **section()** (1 connections) — `test_task_resumption.py`

## Relationships

- [chat + youtube_control](chat_+_youtube_control.md) (6 shared connections)
- [social_content_manager + ui_inspector](social_content_manager_+_ui_inspector.md) (5 shared connections)
- [server + protocol](server_+_protocol.md) (3 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (3 shared connections)
- [tools](tools.md) (2 shared connections)
- [resume_detector](resume_detector.md) (2 shared connections)
- [memory_tool + calendar_tool](memory_tool_+_calendar_tool.md) (1 shared connections)
- [main](main.md) (1 shared connections)
- [safe_executor + ui_inspector](safe_executor_+_ui_inspector.md) (1 shared connections)

## Source Files

- `app/services/task_ledger.py`
- `test_task_resumption.py`

## Audit Trail

- EXTRACTED: 59 (95%)
- INFERRED: 3 (5%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*