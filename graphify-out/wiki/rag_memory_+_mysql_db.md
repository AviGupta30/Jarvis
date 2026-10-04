# rag_memory + mysql_db

> 42 nodes · cohesion 0.08

## Key Concepts

- **rag_memory.py** (27 connections) — `app/services/rag_memory.py`
- **store_turn()** (18 connections) — `app/services/rag_memory.py`
- **init_rag_memory()** (12 connections) — `app/services/rag_memory.py`
- **get_mysql_pool()** (10 connections) — `app/core/mysql_db.py`
- **test_rag_memory.py** (10 connections) — `scripts/test_rag_memory.py`
- **init_rag_memory.py** (8 connections) — `scripts/init_rag_memory.py`
- **mysql_db.py** (7 connections) — `app/core/mysql_db.py`
- **init_mysql()** (7 connections) — `app/core/mysql_db.py`
- **forget_turns()** (7 connections) — `app/services/rag_memory.py`
- **get_memory_stats()** (7 connections) — `app/services/rag_memory.py`
- **close_mysql()** (6 connections) — `app/core/mysql_db.py`
- **test()** (6 connections) — `scripts/test_rag_memory.py`
- **smart_filter()** (5 connections) — `app/services/rag_memory.py`
- **RAG details** (5 connections) — `docs/features/memory.md`
- **_get_faiss_lock()** (4 connections) — `app/services/rag_memory.py`
- **get_history()** (4 connections) — `app/services/rag_memory.py`
- **_save_faiss_index_async()** (4 connections) — `app/services/rag_memory.py`
- **main()** (4 connections) — `scripts/init_rag_memory.py`
- **_extract_topics()** (3 connections) — `app/services/rag_memory.py`
- **_load_faiss_index()** (3 connections) — `app/services/rag_memory.py`
- **_save_faiss_index()** (3 connections) — `app/services/rag_memory.py`
- **aiomysql** (2 connections)
- **mysql_db.py — Jarvis Async MySQL Connection Pool…** (1 connections) — `app/core/mysql_db.py`
- **Gracefully close the MySQL connection pool on server shutdown.** (1 connections) — `app/core/mysql_db.py`
- **Return the shared MySQL connection pool, initializing it if needed.** (1 connections) — `app/core/mysql_db.py`
- *... and 17 more nodes in this community*

## Relationships

- [memory + tool_runner](memory_+_tool_runner.md) (15 shared connections)
- [jarvis_overlay + prompt_overlay](jarvis_overlay_+_prompt_overlay.md) (6 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (4 shared connections)
- [chat](chat.md) (4 shared connections)
- [server + persistence](server_+_persistence.md) (3 shared connections)
- [main + screen_vision](main_+_screen_vision.md) (3 shared connections)
- [main](main.md) (2 shared connections)
- [memory + tools](memory_+_tools.md) (1 shared connections)
- [assignment_assembler + smart_navigator](assignment_assembler_+_smart_navigator.md) (1 shared connections)
- [task_ledger + resume_detector](task_ledger_+_resume_detector.md) (1 shared connections)
- [calendar_tool + email-calendar](calendar_tool_+_email-calendar.md) (1 shared connections)
- [llm-personality + ARCHITECTURE](llm-personality_+_ARCHITECTURE.md) (1 shared connections)

## Source Files

- `app/core/mysql_db.py`
- `app/services/rag_memory.py`
- `docs/features/memory.md`
- `scripts/init_rag_memory.py`
- `scripts/test_rag_memory.py`

## Audit Trail

- EXTRACTED: 107 (95%)
- INFERRED: 6 (5%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*