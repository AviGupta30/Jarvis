# assignment_humanizer + task_ledger

> 70 nodes · cohesion 0.05

## Key Concepts

- **json** (50 connections)
- **pathlib** (28 connections)
- **rag_memory.py** (27 connections) — `app/services/rag_memory.py`
- **test_task_resumption.py** (23 connections) — `test_task_resumption.py`
- **assignment_humanizer.py** (20 connections) — `app/services/assignment_humanizer.py`
- **task_ledger.py** (15 connections) — `app/services/task_ledger.py`
- **datetime** (11 connections)
- **_load_ledger()** (10 connections) — `app/services/task_ledger.py`
- **_humanize_via_browser()** (8 connections) — `app/services/assignment_humanizer.py`
- **get_task_ledger_for_prompt()** (8 connections) — `app/services/task_ledger.py`
- **humanize_text()** (7 connections) — `app/services/assignment_humanizer.py`
- **_humanize_via_llm()** (7 connections) — `app/services/assignment_humanizer.py`
- **get_recent_tasks_raw()** (7 connections) — `app/services/task_ledger.py`
- **log_task()** (7 connections) — `app/services/task_ledger.py`
- **traceback** (7 connections)
- **_humanize_chunk_via_browser()** (6 connections) — `app/services/assignment_humanizer.py`
- **humanize_all_answers()** (5 connections) — `app/services/assignment_humanizer.py`
- **_protect_technical()** (5 connections) — `app/services/assignment_humanizer.py`
- **find_resumable_task()** (5 connections) — `app/services/task_ledger.py`
- **get_recent_tasks()** (5 connections) — `app/services/task_ledger.py`
- **_save_ledger()** (5 connections) — `app/services/task_ledger.py`
- **update_task()** (5 connections) — `app/services/task_ledger.py`
- **_restore_technical()** (4 connections) — `app/services/assignment_humanizer.py`
- **_split_into_chunks()** (4 connections) — `app/services/assignment_humanizer.py`
- **_get_faiss_lock()** (4 connections) — `app/services/rag_memory.py`
- *... and 45 more nodes in this community*

## Relationships

- [chat + youtube_control](chat_+_youtube_control.md) (14 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (9 shared connections)
- [memory + rag_memory](memory_+_rag_memory.md) (7 shared connections)
- [gmail_tool + memory_tool](gmail_tool_+_memory_tool.md) (7 shared connections)
- [safe_executor + refresh_docs](safe_executor_+_refresh_docs.md) (6 shared connections)
- [tools](tools.md) (5 shared connections)
- [mysql_db + rag_memory](mysql_db_+_rag_memory.md) (4 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (4 shared connections)
- [social_content_manager + content-tools](social_content_manager_+_content-tools.md) (3 shared connections)
- [style_profiler + reply_generator](style_profiler_+_reply_generator.md) (3 shared connections)
- [assignment_answers](assignment_answers.md) (3 shared connections)
- [ppt_tool](ppt_tool.md) (3 shared connections)

## Source Files

- `app/services/assignment_humanizer.py`
- `app/services/rag_memory.py`
- `app/services/task_ledger.py`
- `test_api.py`
- `test_task_resumption.py`

## Audit Trail

- EXTRACTED: 235 (97%)
- INFERRED: 7 (3%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*