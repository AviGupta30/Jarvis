# memory + rag_memory

> 49 nodes · cohesion 0.06

## Key Concepts

- **api/memory.py** (21 connections) — `app/api/memory.py`
- **store_turn()** (18 connections) — `app/services/rag_memory.py`
- **asyncio** (15 connections)
- **test_rag_memory.py** (10 connections) — `scripts/test_rag_memory.py`
- **get_embedding()** (9 connections) — `app/services/embeddings.py`
- **ingest_memory()** (7 connections) — `app/api/memory.py`
- **forget_turns()** (7 connections) — `app/services/rag_memory.py`
- **get_memory_stats()** (7 connections) — `app/services/rag_memory.py`
- **concurrent_futures** (6 connections)
- **test()** (6 connections) — `scripts/test_rag_memory.py`
- **forget_memory()** (5 connections) — `app/api/memory.py`
- **get_history()** (5 connections) — `app/api/memory.py`
- **database.py** (5 connections) — `app/core/database.py`
- **get_db_pool()** (5 connections) — `app/core/database.py`
- **embeddings.py** (5 connections) — `app/services/embeddings.py`
- **smart_filter()** (5 connections) — `app/services/rag_memory.py`
- **vector_store.py** (5 connections) — `app/services/vector_store.py`
- **save_document_chunk()** (5 connections) — `app/services/vector_store.py`
- **search_similar_chunks()** (5 connections) — `app/services/vector_store.py`
- **RAG details** (5 connections) — `docs/features/memory.md`
- **memory_stats()** (4 connections) — `app/api/memory.py`
- **_get_faiss_lock()** (4 connections) — `app/services/rag_memory.py`
- **ForgetRequest** (3 connections) — `app/api/memory.py`
- **IngestRequest** (3 connections) — `app/api/memory.py`
- **BaseModel** (3 connections)
- *... and 24 more nodes in this community*

## Relationships

- [smart_navigator + rag_memory](smart_navigator_+_rag_memory.md) (13 shared connections)
- [chat + llm](chat_+_llm.md) (13 shared connections)
- [agents + tool_runner](agents_+_tool_runner.md) (9 shared connections)
- [mysql_db + rag_memory](mysql_db_+_rag_memory.md) (8 shared connections)
- [tool-registry + memory](tool-registry_+_memory.md) (4 shared connections)
- [voice](voice.md) (2 shared connections)
- [main](main.md) (1 shared connections)
- [chat + KNOWN_ISSUES](chat_+_KNOWN_ISSUES.md) (1 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (1 shared connections)
- [safe_executor + ui_inspector](safe_executor_+_ui_inspector.md) (1 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (1 shared connections)
- [spotify_service + media_sessions](spotify_service_+_media_sessions.md) (1 shared connections)

## Source Files

- `app/api/memory.py`
- `app/core/database.py`
- `app/services/embeddings.py`
- `app/services/rag_memory.py`
- `app/services/vector_store.py`
- `docs/features/memory.md`
- `scripts/test_rag_memory.py`

## Audit Trail

- EXTRACTED: 129 (96%)
- INFERRED: 5 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*