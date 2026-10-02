# task_ledger + test_task_resumption

> 25 nodes · cohesion 0.10

## Key Concepts

- **test_task_resumption.py** (23 connections) — `test_task_resumption.py`
- **_load_ledger()** (10 connections) — `app/services/task_ledger.py`
- **get_recent_tasks_raw()** (7 connections) — `app/services/task_ledger.py`
- **log_task()** (7 connections) — `app/services/task_ledger.py`
- **traceback** (7 connections)
- **find_resumable_task()** (5 connections) — `app/services/task_ledger.py`
- **get_recent_tasks()** (5 connections) — `app/services/task_ledger.py`
- **_save_ledger()** (5 connections) — `app/services/task_ledger.py`
- **update_task()** (5 connections) — `app/services/task_ledger.py`
- **_ensure_ledger_file()** (4 connections) — `app/services/task_ledger.py`
- **test_fastapi.py** (3 connections) — `test_fastapi.py`
- **Return a formatted string of the last N tasks, suitable for display or speech.…** (1 connections) — `app/services/task_ledger.py`
- **Return the last N raw ledger entries as a list of dicts. Used internally by…** (1 connections) — `app/services/task_ledger.py`
- **Fuzzy-search the ledger for the most recent resumable task matching the query.…** (1 connections) — `app/services/task_ledger.py`
- **Update an existing ledger entry by task_id. Used after successfully appending…** (1 connections) — `app/services/task_ledger.py`
- **Create the data directory and ledger file if they don't exist.** (1 connections) — `app/services/task_ledger.py`
- **Load the ledger from disk. Returns empty list on any error.** (1 connections) — `app/services/task_ledger.py`
- **Persist the ledger to disk. Caps at _MAX_ENTRIES (FIFO).** (1 connections) — `app/services/task_ledger.py`
- **Record a completed (or in-progress) task to the persistent ledger. Args:…** (1 connections) — `app/services/task_ledger.py`
- **fastapi_testclient** (1 connections)
- **_backup_ledger()** (1 connections) — `test_task_resumption.py`
- **check()** (1 connections) — `test_task_resumption.py`
- **test_task_resumption.py -- Comprehensive automated verification for the Task…** (1 connections) — `test_task_resumption.py`
- **_restore_ledger()** (1 connections) — `test_task_resumption.py`
- **section()** (1 connections) — `test_task_resumption.py`

## Relationships

- [smart_navigator + rag_memory](smart_navigator_+_rag_memory.md) (14 shared connections)
- [chat + llm](chat_+_llm.md) (6 shared connections)
- [tools + whatsapp_smart](tools_+_whatsapp_smart.md) (2 shared connections)
- [resume_detector](resume_detector.md) (2 shared connections)
- [chat-routing + chat](chat-routing_+_chat.md) (1 shared connections)
- [main](main.md) (1 shared connections)
- [persistence + engine](persistence_+_engine.md) (1 shared connections)
- [file_ops](file_ops.md) (1 shared connections)
- [server + test_concurrency](server_+_test_concurrency.md) (1 shared connections)
- [dark_enhancement + dark_video_enhancement](dark_enhancement_+_dark_video_enhancement.md) (1 shared connections)
- [safe_executor + ui_inspector](safe_executor_+_ui_inspector.md) (1 shared connections)
- [download_kokoro](download_kokoro.md) (1 shared connections)

## Source Files

- `app/services/task_ledger.py`
- `test_fastapi.py`
- `test_task_resumption.py`

## Audit Trail

- EXTRACTED: 61 (95%)
- INFERRED: 3 (5%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*