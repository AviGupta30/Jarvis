# memory

> 23 nodes · cohesion 0.12

## Key Concepts

- **api/memory.py** (21 connections) — `app/api/memory.py`
- **recall_memory()** (14 connections) — `app/api/memory.py`
- **format_recall_for_prompt()** (10 connections) — `app/services/rag_memory.py`
- **ingest_memory()** (7 connections) — `app/api/memory.py`
- **forget_memory()** (5 connections) — `app/api/memory.py`
- **get_history()** (5 connections) — `app/api/memory.py`
- **memory_stats()** (4 connections) — `app/api/memory.py`
- **get_history()** (4 connections) — `app/services/rag_memory.py`
- **ForgetRequest** (3 connections) — `app/api/memory.py`
- **IngestRequest** (3 connections) — `app/api/memory.py`
- **BaseModel** (3 connections)
- **RecallRequest** (3 connections) — `app/api/memory.py`
- **get** (2 connections)
- **post** (2 connections)
- **delete** (1 connections)
- **app/api/memory.py — Jarvis Long-Term Memory API Router…** (1 connections) — `app/api/memory.py`
- **Return statistics about Jarvis's long-term memory store. Includes total turns,…** (1 connections) — `app/api/memory.py`
- **Soft-delete conversation turns that are semantically related to the query.…** (1 connections) — `app/api/memory.py`
- **Ingest a knowledge chunk. Primary store: Postgres/pgvector (DATABASE_URL). If…** (1 connections) — `app/api/memory.py`
- **Semantic search over all stored conversation turns. Returns the most relevant…** (1 connections) — `app/api/memory.py`
- **Retrieve paginated conversation history from MySQL. Query params: limit (int):…** (1 connections) — `app/api/memory.py`
- **Format recalled memory turns into an injectable LLM context block with clear…** (1 connections) — `app/services/rag_memory.py`
- **Retrieve paginated conversation history from MySQL. Args: limit: Max rows to…** (1 connections) — `app/services/rag_memory.py`

## Relationships

- [chat + youtube_control](chat_+_youtube_control.md) (7 shared connections)
- [rag_memory + tool_runner](rag_memory_+_tool_runner.md) (6 shared connections)
- [mysql_db + rag_memory](mysql_db_+_rag_memory.md) (3 shared connections)
- [vector_store + database](vector_store_+_database.md) (2 shared connections)
- [tool-registry + tools](tool-registry_+_tools.md) (2 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (2 shared connections)
- [task_ledger + rag_memory](task_ledger_+_rag_memory.md) (2 shared connections)
- [resume_router](resume_router.md) (1 shared connections)
- [ppt_router + ppt_tool](ppt_router_+_ppt_tool.md) (1 shared connections)
- [message_reader + thread_extractor](message_reader_+_thread_extractor.md) (1 shared connections)
- [main](main.md) (1 shared connections)
- [CLAUDE](CLAUDE.md) (1 shared connections)

## Source Files

- `app/api/memory.py`
- `app/services/rag_memory.py`

## Audit Trail

- EXTRACTED: 56 (88%)
- INFERRED: 8 (12%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*