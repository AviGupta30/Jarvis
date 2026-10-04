# mysql_db + rag_memory

> 20 nodes · cohesion 0.14

## Key Concepts

- **init_rag_memory()** (12 connections) — `app/services/rag_memory.py`
- **get_mysql_pool()** (10 connections) — `app/core/mysql_db.py`
- **init_rag_memory.py** (8 connections) — `scripts/init_rag_memory.py`
- **mysql_db.py** (7 connections) — `app/core/mysql_db.py`
- **init_mysql()** (7 connections) — `app/core/mysql_db.py`
- **forget_turns()** (7 connections) — `app/services/rag_memory.py`
- **close_mysql()** (6 connections) — `app/core/mysql_db.py`
- **RAG details** (5 connections) — `docs/features/memory.md`
- **main()** (4 connections) — `scripts/init_rag_memory.py`
- **_load_faiss_index()** (3 connections) — `app/services/rag_memory.py`
- **aiomysql** (2 connections)
- **mysql_db.py — Jarvis Async MySQL Connection Pool…** (1 connections) — `app/core/mysql_db.py`
- **Gracefully close the MySQL connection pool on server shutdown.** (1 connections) — `app/core/mysql_db.py`
- **Return the shared MySQL connection pool, initializing it if needed.** (1 connections) — `app/core/mysql_db.py`
- **Initialize the MySQL connection pool and ensure all required tables exist. Safe…** (1 connections) — `app/core/mysql_db.py`
- **Boot the RAG memory system: 1. Initialize MySQL pool + ensure tables exist 2.…** (1 connections) — `app/services/rag_memory.py`
- **Soft-delete turns semantically related to a query. Removes from MySQL. FAISS…** (1 connections) — `app/services/rag_memory.py`
- **Load FAISS index from disk, or create a fresh one.** (1 connections) — `app/services/rag_memory.py`
- **Pool** (1 connections)
- **scripts/init_rag_memory.py --------------------------- One-time initialization…** (1 connections) — `scripts/init_rag_memory.py`

## Relationships

- [task_ledger + rag_memory](task_ledger_+_rag_memory.md) (6 shared connections)
- [rag_memory + tool_runner](rag_memory_+_tool_runner.md) (6 shared connections)
- [memory](memory.md) (4 shared connections)
- [main](main.md) (2 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (2 shared connections)
- [main + screen_vision](main_+_screen_vision.md) (2 shared connections)
- [voice_agent + download_kokoro](voice_agent_+_download_kokoro.md) (2 shared connections)
- [message_reader + thread_extractor](message_reader_+_thread_extractor.md) (1 shared connections)
- [dynamic_skill + planner](dynamic_skill_+_planner.md) (1 shared connections)
- [voice_agent + main](voice_agent_+_main.md) (1 shared connections)
- [acoustic_tripwire](acoustic_tripwire.md) (1 shared connections)

## Source Files

- `app/core/mysql_db.py`
- `app/services/rag_memory.py`
- `docs/features/memory.md`
- `scripts/init_rag_memory.py`

## Audit Trail

- EXTRACTED: 49 (91%)
- INFERRED: 5 (9%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*