# mysql_db + init_rag_memory

> 15 nodes · cohesion 0.17

## Key Concepts

- **get_mysql_pool()** (10 connections) — `app/core/mysql_db.py`
- **init_rag_memory.py** (8 connections) — `scripts/init_rag_memory.py`
- **mysql_db.py** (7 connections) — `app/core/mysql_db.py`
- **init_mysql()** (7 connections) — `app/core/mysql_db.py`
- **close_mysql()** (6 connections) — `app/core/mysql_db.py`
- **get_history()** (4 connections) — `app/services/rag_memory.py`
- **main()** (4 connections) — `scripts/init_rag_memory.py`
- **aiomysql** (2 connections)
- **mysql_db.py — Jarvis Async MySQL Connection Pool…** (1 connections) — `app/core/mysql_db.py`
- **Gracefully close the MySQL connection pool on server shutdown.** (1 connections) — `app/core/mysql_db.py`
- **Return the shared MySQL connection pool, initializing it if needed.** (1 connections) — `app/core/mysql_db.py`
- **Initialize the MySQL connection pool and ensure all required tables exist. Safe…** (1 connections) — `app/core/mysql_db.py`
- **Retrieve paginated conversation history from MySQL. Args: limit: Max rows to…** (1 connections) — `app/services/rag_memory.py`
- **Pool** (1 connections)
- **scripts/init_rag_memory.py --------------------------- One-time initialization…** (1 connections) — `scripts/init_rag_memory.py`

## Relationships

- [assignment_tool + assignment_humanizer](assignment_tool_+_assignment_humanizer.md) (7 shared connections)
- [rag_memory + test_rag_memory](rag_memory_+_test_rag_memory.md) (4 shared connections)
- [main + screen_vision](main_+_screen_vision.md) (2 shared connections)
- [memory + memory](memory_+_memory.md) (2 shared connections)
- [chat + rag_memory](chat_+_rag_memory.md) (2 shared connections)
- [persistence + server](persistence_+_server.md) (1 shared connections)
- [dump_wa_ui + test_wa](dump_wa_ui_+_test_wa.md) (1 shared connections)

## Source Files

- `app/core/mysql_db.py`
- `app/services/rag_memory.py`
- `scripts/init_rag_memory.py`

## Audit Trail

- EXTRACTED: 37 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*