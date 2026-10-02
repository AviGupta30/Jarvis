# mysql_db + rag_memory

> 19 nodes · cohesion 0.14

## Key Concepts

- **init_rag_memory()** (12 connections) — `app/services/rag_memory.py`
- **get_mysql_pool()** (10 connections) — `app/core/mysql_db.py`
- **init_rag_memory.py** (8 connections) — `scripts/init_rag_memory.py`
- **mysql_db.py** (7 connections) — `app/core/mysql_db.py`
- **init_mysql()** (7 connections) — `app/core/mysql_db.py`
- **close_mysql()** (6 connections) — `app/core/mysql_db.py`
- **get_history()** (4 connections) — `app/services/rag_memory.py`
- **main()** (4 connections) — `scripts/init_rag_memory.py`
- **_load_faiss_index()** (3 connections) — `app/services/rag_memory.py`
- **aiomysql** (2 connections)
- **mysql_db.py — Jarvis Async MySQL Connection Pool…** (1 connections) — `app/core/mysql_db.py`
- **Gracefully close the MySQL connection pool on server shutdown.** (1 connections) — `app/core/mysql_db.py`
- **Return the shared MySQL connection pool, initializing it if needed.** (1 connections) — `app/core/mysql_db.py`
- **Initialize the MySQL connection pool and ensure all required tables exist. Safe…** (1 connections) — `app/core/mysql_db.py`
- **Boot the RAG memory system: 1. Initialize MySQL pool + ensure tables exist 2.…** (1 connections) — `app/services/rag_memory.py`
- **Retrieve paginated conversation history from MySQL. Args: limit: Max rows to…** (1 connections) — `app/services/rag_memory.py`
- **Load FAISS index from disk, or create a fresh one.** (1 connections) — `app/services/rag_memory.py`
- **Pool** (1 connections)
- **scripts/init_rag_memory.py --------------------------- One-time initialization…** (1 connections) — `scripts/init_rag_memory.py`

## Relationships

- [smart_navigator + rag_memory](smart_navigator_+_rag_memory.md) (8 shared connections)
- [memory + rag_memory](memory_+_rag_memory.md) (8 shared connections)
- [main](main.md) (3 shared connections)
- [screen_vision + screen_reader](screen_vision_+_screen_reader.md) (1 shared connections)
- [agents + tool_runner](agents_+_tool_runner.md) (1 shared connections)
- [main + screen_vision](main_+_screen_vision.md) (1 shared connections)
- [ARCHITECTURE + acoustic_tripwire](ARCHITECTURE_+_acoustic_tripwire.md) (1 shared connections)
- [server + test_concurrency](server_+_test_concurrency.md) (1 shared connections)

## Source Files

- `app/core/mysql_db.py`
- `app/services/rag_memory.py`
- `scripts/init_rag_memory.py`

## Audit Trail

- EXTRACTED: 46 (96%)
- INFERRED: 2 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*