# task_ledger + rag_memory

> 38 nodes · cohesion 0.08

## Key Concepts

- **rag_memory.py** (27 connections) — `app/services/rag_memory.py`
- **test_task_resumption.py** (23 connections) — `test_task_resumption.py`
- **task_ledger.py** (15 connections) — `app/services/task_ledger.py`
- **datetime** (11 connections)
- **_load_ledger()** (10 connections) — `app/services/task_ledger.py`
- **get_recent_tasks_raw()** (7 connections) — `app/services/task_ledger.py`
- **log_task()** (7 connections) — `app/services/task_ledger.py`
- **find_resumable_task()** (5 connections) — `app/services/task_ledger.py`
- **get_recent_tasks()** (5 connections) — `app/services/task_ledger.py`
- **_save_ledger()** (5 connections) — `app/services/task_ledger.py`
- **update_task()** (5 connections) — `app/services/task_ledger.py`
- **_get_faiss_lock()** (4 connections) — `app/services/rag_memory.py`
- **_save_faiss_index_async()** (4 connections) — `app/services/rag_memory.py`
- **_ensure_ledger_file()** (4 connections) — `app/services/task_ledger.py`
- **uuid** (4 connections)
- **_extract_topics()** (3 connections) — `app/services/rag_memory.py`
- **_save_faiss_index()** (3 connections) — `app/services/rag_memory.py`
- **shutil** (3 connections)
- **Lock** (1 connections)
- **rag_memory.py — Jarvis Long-Term RAG Memory Engine…** (1 connections) — `app/services/rag_memory.py`
- **Persist FAISS index and ID map to disk (sync, runs in thread executor).** (1 connections) — `app/services/rag_memory.py`
- **Run the sync FAISS save in a thread pool to avoid blocking the event loop.** (1 connections) — `app/services/rag_memory.py`
- **Lightweight keyword-based topic extraction (no LLM call). Returns a CSV of the…** (1 connections) — `app/services/rag_memory.py`
- **Lazily create the FAISS lock inside a running event loop.** (1 connections) — `app/services/rag_memory.py`
- **task_ledger.py — Jarvis Task Context Ledger…** (1 connections) — `app/services/task_ledger.py`
- *... and 13 more nodes in this community*

## Relationships

- [chat + youtube_control](chat_+_youtube_control.md) (10 shared connections)
- [voice_agent + download_kokoro](voice_agent_+_download_kokoro.md) (9 shared connections)
- [mysql_db + rag_memory](mysql_db_+_rag_memory.md) (6 shared connections)
- [rag_memory + tool_runner](rag_memory_+_tool_runner.md) (4 shared connections)
- [message_reader + thread_extractor](message_reader_+_thread_extractor.md) (4 shared connections)
- [memory](memory.md) (3 shared connections)
- [dynamic_skill + planner](dynamic_skill_+_planner.md) (3 shared connections)
- [tools](tools.md) (3 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (2 shared connections)
- [gmail_tool + memory_tool](gmail_tool_+_memory_tool.md) (2 shared connections)
- [file_ops](file_ops.md) (2 shared connections)
- [resume_detector](resume_detector.md) (2 shared connections)

## Source Files

- `app/services/rag_memory.py`
- `app/services/task_ledger.py`
- `test_task_resumption.py`

## Audit Trail

- EXTRACTED: 107 (96%)
- INFERRED: 4 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*