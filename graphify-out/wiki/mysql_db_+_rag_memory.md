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

- [syllabus_auditor + syllabus-auditor](syllabus_auditor_+_syllabus-auditor.md) (5 shared connections)
- [rag_memory + memory](rag_memory_+_memory.md) (5 shared connections)
- [main + screen_vision](main_+_screen_vision.md) (4 shared connections)
- [assignment_tool + safe_executor](assignment_tool_+_safe_executor.md) (3 shared connections)
- [ARCHITECTURE + acoustic_tripwire](ARCHITECTURE_+_acoustic_tripwire.md) (1 shared connections)
- [chat](chat.md) (1 shared connections)

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