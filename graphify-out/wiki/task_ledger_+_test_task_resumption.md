# task_ledger + test_task_resumption

> 36 nodes · cohesion 0.09

## Key Concepts

- **json** (41 connections)
- **test_task_resumption.py** (23 connections) — `test_task_resumption.py`
- **task_ledger.py** (15 connections) — `app/services/task_ledger.py`
- **_load_ledger()** (10 connections) — `app/services/task_ledger.py`
- **nlp_extractor.py** (8 connections) — `app/services/nlp_extractor.py`
- **get_task_ledger_for_prompt()** (8 connections) — `app/services/task_ledger.py`
- **get_recent_tasks_raw()** (7 connections) — `app/services/task_ledger.py`
- **log_task()** (7 connections) — `app/services/task_ledger.py`
- **traceback** (7 connections)
- **find_resumable_task()** (5 connections) — `app/services/task_ledger.py`
- **get_recent_tasks()** (5 connections) — `app/services/task_ledger.py`
- **_save_ledger()** (5 connections) — `app/services/task_ledger.py`
- **update_task()** (5 connections) — `app/services/task_ledger.py`
- **_ensure_ledger_file()** (4 connections) — `app/services/task_ledger.py`
- **dotenv** (3 connections)
- **test_api.py** (3 connections) — `test_api.py`
- **test_fastapi.py** (3 connections) — `test_fastapi.py`
- **urllib_request** (3 connections)
- **uuid** (3 connections)
- **nlp_extractor.py — LLM-Powered Fact & Entity Extractor…** (1 connections) — `app/services/nlp_extractor.py`
- **task_ledger.py — Jarvis Task Context Ledger…** (1 connections) — `app/services/task_ledger.py`
- **Return a formatted string of the last N tasks, suitable for display or speech.…** (1 connections) — `app/services/task_ledger.py`
- **Return the last N raw ledger entries as a list of dicts. Used internally by…** (1 connections) — `app/services/task_ledger.py`
- **Fuzzy-search the ledger for the most recent resumable task matching the query.…** (1 connections) — `app/services/task_ledger.py`
- **Update an existing ledger entry by task_id. Used after successfully appending…** (1 connections) — `app/services/task_ledger.py`
- *... and 11 more nodes in this community*

## Relationships

- [chat + llm](chat_+_llm.md) (10 shared connections)
- [dag_executor + planner](dag_executor_+_planner.md) (7 shared connections)
- [research_scraper + nlp_extractor](research_scraper_+_nlp_extractor.md) (3 shared connections)
- [assignment_tool](assignment_tool.md) (3 shared connections)
- [agentic_web](agentic_web.md) (2 shared connections)
- [tools](tools.md) (2 shared connections)
- [prompt_enhancer_button](prompt_enhancer_button.md) (2 shared connections)
- [gmail_tool](gmail_tool.md) (2 shared connections)
- [ppt_tool](ppt_tool.md) (2 shared connections)
- [rag_memory + memory](rag_memory_+_memory.md) (2 shared connections)
- [safe_executor](safe_executor.md) (2 shared connections)
- [youtube_control](youtube_control.md) (2 shared connections)

## Source Files

- `app/services/nlp_extractor.py`
- `app/services/task_ledger.py`
- `test_api.py`
- `test_fastapi.py`
- `test_task_resumption.py`

## Audit Trail

- EXTRACTED: 125 (98%)
- INFERRED: 3 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*