# rag_memory + memory

> 62 nodes · cohesion 0.06

## Key Concepts

- **rag_memory.py** (27 connections) — `app/services/rag_memory.py`
- **api/memory.py** (21 connections) — `app/api/memory.py`
- **store_turn()** (18 connections) — `app/services/rag_memory.py`
- **recall()** (15 connections) — `app/services/rag_memory.py`
- **init_rag_memory()** (12 connections) — `app/services/rag_memory.py`
- **get_mysql_pool()** (10 connections) — `app/core/mysql_db.py`
- **test_rag_memory.py** (10 connections) — `scripts/test_rag_memory.py`
- **get_embedding()** (9 connections) — `app/services/embeddings.py`
- **init_rag_memory.py** (8 connections) — `scripts/init_rag_memory.py`
- **ingest_memory()** (7 connections) — `app/api/memory.py`
- **mysql_db.py** (7 connections) — `app/core/mysql_db.py`
- **init_mysql()** (7 connections) — `app/core/mysql_db.py`
- **forget_turns()** (7 connections) — `app/services/rag_memory.py`
- **get_memory_stats()** (7 connections) — `app/services/rag_memory.py`
- **close_mysql()** (6 connections) — `app/core/mysql_db.py`
- **test()** (6 connections) — `scripts/test_rag_memory.py`
- **forget_memory()** (5 connections) — `app/api/memory.py`
- **get_history()** (5 connections) — `app/api/memory.py`
- **smart_filter()** (5 connections) — `app/services/rag_memory.py`
- **RAG details** (5 connections) — `docs/features/memory.md`
- **memory_stats()** (4 connections) — `app/api/memory.py`
- **_get_faiss_lock()** (4 connections) — `app/services/rag_memory.py`
- **get_history()** (4 connections) — `app/services/rag_memory.py`
- **_save_faiss_index_async()** (4 connections) — `app/services/rag_memory.py`
- **main()** (4 connections) — `scripts/init_rag_memory.py`
- *... and 37 more nodes in this community*

## Relationships

- [benchmark + download_kokoro](benchmark_+_download_kokoro.md) (7 shared connections)
- [planner + dynamic_skill](planner_+_dynamic_skill.md) (7 shared connections)
- [tool-registry + vector_store](tool-registry_+_vector_store.md) (6 shared connections)
- [main](main.md) (6 shared connections)
- [chat + llm](chat_+_llm.md) (6 shared connections)
- [agents + tool_runner](agents_+_tool_runner.md) (4 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (3 shared connections)
- [resume_router + tools](resume_router_+_tools.md) (2 shared connections)
- [server + persistence](server_+_persistence.md) (2 shared connections)
- [style_profiler + reply_generator](style_profiler_+_reply_generator.md) (1 shared connections)
- [memory](memory.md) (1 shared connections)
- [assignment_assembler + smart_navigator](assignment_assembler_+_smart_navigator.md) (1 shared connections)

## Source Files

- `app/api/memory.py`
- `app/core/mysql_db.py`
- `app/services/embeddings.py`
- `app/services/rag_memory.py`
- `docs/features/memory.md`
- `scripts/init_rag_memory.py`
- `scripts/test_rag_memory.py`

## Audit Trail

- EXTRACTED: 154 (96%)
- INFERRED: 6 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*