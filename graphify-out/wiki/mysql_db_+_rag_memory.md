# mysql_db + rag_memory

> 14 nodes · cohesion 0.20

## Key Concepts

- **init_rag_memory()** (12 connections) — `app/services/rag_memory.py`
- **init_rag_memory.py** (8 connections) — `scripts/init_rag_memory.py`
- **mysql_db.py** (7 connections) — `app/core/mysql_db.py`
- **init_mysql()** (7 connections) — `app/core/mysql_db.py`
- **close_mysql()** (6 connections) — `app/core/mysql_db.py`
- **main()** (4 connections) — `scripts/init_rag_memory.py`
- **_load_faiss_index()** (3 connections) — `app/services/rag_memory.py`
- **aiomysql** (2 connections)
- **mysql_db.py — Jarvis Async MySQL Connection Pool…** (1 connections) — `app/core/mysql_db.py`
- **Gracefully close the MySQL connection pool on server shutdown.** (1 connections) — `app/core/mysql_db.py`
- **Initialize the MySQL connection pool and ensure all required tables exist. Safe…** (1 connections) — `app/core/mysql_db.py`
- **Boot the RAG memory system: 1. Initialize MySQL pool + ensure tables exist 2.…** (1 connections) — `app/services/rag_memory.py`
- **Load FAISS index from disk, or create a fresh one.** (1 connections) — `app/services/rag_memory.py`
- **scripts/init_rag_memory.py --------------------------- One-time initialization…** (1 connections) — `scripts/init_rag_memory.py`

## Relationships

- [memory + rag_memory](memory_+_rag_memory.md) (5 shared connections)
- [assignment_humanizer + task_ledger](assignment_humanizer_+_task_ledger.md) (4 shared connections)
- [main + screen_vision](main_+_screen_vision.md) (4 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (3 shared connections)
- [acoustic_tripwire](acoustic_tripwire.md) (1 shared connections)
- [safe_executor + refresh_docs](safe_executor_+_refresh_docs.md) (1 shared connections)
- [social_content_manager + content-tools](social_content_manager_+_content-tools.md) (1 shared connections)

## Source Files

- `app/core/mysql_db.py`
- `app/services/rag_memory.py`
- `scripts/init_rag_memory.py`

## Audit Trail

- EXTRACTED: 35 (95%)
- INFERRED: 2 (5%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*