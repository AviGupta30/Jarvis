# rag_memory

> 31 nodes · cohesion 0.11

## Key Concepts

- **rag_memory.py** (27 connections) — `app/services/rag_memory.py`
- **store_turn()** (18 connections) — `app/services/rag_memory.py`
- **recall()** (15 connections) — `app/services/rag_memory.py`
- **get_mysql_pool()** (10 connections) — `app/core/mysql_db.py`
- **test_rag_memory.py** (10 connections) — `scripts/test_rag_memory.py`
- **get_embedding()** (9 connections) — `app/services/embeddings.py`
- **forget_turns()** (7 connections) — `app/services/rag_memory.py`
- **get_memory_stats()** (7 connections) — `app/services/rag_memory.py`
- **test()** (6 connections) — `scripts/test_rag_memory.py`
- **smart_filter()** (5 connections) — `app/services/rag_memory.py`
- **_get_faiss_lock()** (4 connections) — `app/services/rag_memory.py`
- **get_history()** (4 connections) — `app/services/rag_memory.py`
- **_save_faiss_index_async()** (4 connections) — `app/services/rag_memory.py`
- **_extract_topics()** (3 connections) — `app/services/rag_memory.py`
- **_save_faiss_index()** (3 connections) — `app/services/rag_memory.py`
- **Return the shared MySQL connection pool, initializing it if needed.** (1 connections) — `app/core/mysql_db.py`
- **Runs the local fastembed ONNX model in a thread pool so it doesn't block the…** (1 connections) — `app/services/embeddings.py`
- **Lock** (1 connections)
- **rag_memory.py — Jarvis Long-Term RAG Memory Engine…** (1 connections) — `app/services/rag_memory.py`
- **Persist FAISS index and ID map to disk (sync, runs in thread executor).** (1 connections) — `app/services/rag_memory.py`
- **Run the sync FAISS save in a thread pool to avoid blocking the event loop.** (1 connections) — `app/services/rag_memory.py`
- **Returns True if the turn is meaningful enough to store. Skips trivial single-…** (1 connections) — `app/services/rag_memory.py`
- **Lightweight keyword-based topic extraction (no LLM call). Returns a CSV of the…** (1 connections) — `app/services/rag_memory.py`
- **Save a conversation turn to MySQL + FAISS. Silently skips trivial turns and…** (1 connections) — `app/services/rag_memory.py`
- **Semantically recall the most relevant past conversation turns. Args: query: The…** (1 connections) — `app/services/rag_memory.py`
- *... and 6 more nodes in this community*

## Relationships

- [memory](memory.md) (13 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (11 shared connections)
- [mysql_db + rag_memory](mysql_db_+_rag_memory.md) (8 shared connections)
- [social_content_manager + ui_inspector](social_content_manager_+_ui_inspector.md) (6 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (3 shared connections)
- [server + protocol](server_+_protocol.md) (2 shared connections)
- [memory + main](memory_+_main.md) (2 shared connections)
- [memory_tool + calendar_tool](memory_tool_+_calendar_tool.md) (1 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (1 shared connections)
- [tool_runner](tool_runner.md) (1 shared connections)

## Source Files

- `app/core/mysql_db.py`
- `app/services/embeddings.py`
- `app/services/rag_memory.py`
- `scripts/test_rag_memory.py`

## Audit Trail

- EXTRACTED: 95 (97%)
- INFERRED: 3 (3%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*