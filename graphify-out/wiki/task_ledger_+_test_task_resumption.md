# task_ledger + test_task_resumption

> 28 nodes · cohesion 0.11

## Key Concepts

- **test_task_resumption.py** (23 connections) — `test_task_resumption.py`
- **task_ledger.py** (15 connections) — `app/services/task_ledger.py`
- **_load_ledger()** (10 connections) — `app/services/task_ledger.py`
- **get_recent_tasks_raw()** (7 connections) — `app/services/task_ledger.py`
- **log_task()** (7 connections) — `app/services/task_ledger.py`
- **traceback** (7 connections)
- **find_resumable_task()** (5 connections) — `app/services/task_ledger.py`
- **get_recent_tasks()** (5 connections) — `app/services/task_ledger.py`
- **_save_ledger()** (5 connections) — `app/services/task_ledger.py`
- **update_task()** (5 connections) — `app/services/task_ledger.py`
- **_ensure_ledger_file()** (4 connections) — `app/services/task_ledger.py`
- **uuid** (4 connections)
- **test_fastapi.py** (3 connections) — `test_fastapi.py`
- **task_ledger.py — Jarvis Task Context Ledger…** (1 connections) — `app/services/task_ledger.py`
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
- *... and 3 more nodes in this community*

## Relationships

- [benchmark + download_kokoro](benchmark_+_download_kokoro.md) (5 shared connections)
- [planner + dynamic_skill](planner_+_dynamic_skill.md) (5 shared connections)
- [chat + llm](chat_+_llm.md) (3 shared connections)
- [resume_detector](resume_detector.md) (3 shared connections)
- [test_lru](test_lru.md) (2 shared connections)
- [tools](tools.md) (2 shared connections)
- [main](main.md) (2 shared connections)
- [safe_executor](safe_executor.md) (2 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (1 shared connections)
- [dag_executor](dag_executor.md) (1 shared connections)
- [dark_enhancement + dark_video_enhancement](dark_enhancement_+_dark_video_enhancement.md) (1 shared connections)
- [gmail_tool + memory_tool](gmail_tool_+_memory_tool.md) (1 shared connections)

## Source Files

- `app/services/task_ledger.py`
- `test_fastapi.py`
- `test_task_resumption.py`

## Audit Trail

- EXTRACTED: 70 (96%)
- INFERRED: 3 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*