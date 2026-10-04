# rag_memory + mysql_db

> 53 nodes · cohesion 0.06

## Key Concepts

- **rag_memory.py** (27 connections) — `app/services/rag_memory.py`
- **recall()** (15 connections) — `app/services/rag_memory.py`
- **asyncio** (15 connections)
- **run_tool()** (13 connections) — `app/services/tool_runner.py`
- **init_rag_memory()** (12 connections) — `app/services/rag_memory.py`
- **get_mysql_pool()** (10 connections) — `app/core/mysql_db.py`
- **format_recall_for_prompt()** (10 connections) — `app/services/rag_memory.py`
- **test_rag_memory.py** (10 connections) — `scripts/test_rag_memory.py`
- **get_embedding()** (9 connections) — `app/services/embeddings.py`
- **tool_runner.py** (9 connections) — `app/services/tool_runner.py`
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
- *... and 28 more nodes in this community*

## Relationships

- [chat + llm](chat_+_llm.md) (21 shared connections)
- [memory + CLAUDE](memory_+_CLAUDE.md) (12 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (8 shared connections)
- [benchmark + server](benchmark_+_server.md) (6 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (6 shared connections)
- [main + screen_vision](main_+_screen_vision.md) (5 shared connections)
- [social_content_manager + tools](social_content_manager_+_tools.md) (3 shared connections)
- [tools](tools.md) (2 shared connections)
- [voice](voice.md) (2 shared connections)
- [memory](memory.md) (1 shared connections)
- [nlp_extractor + download_kokoro](nlp_extractor_+_download_kokoro.md) (1 shared connections)
- [assignment_assembler + smart_navigator](assignment_assembler_+_smart_navigator.md) (1 shared connections)

## Source Files

- `app/core/mysql_db.py`
- `app/services/embeddings.py`
- `app/services/rag_memory.py`
- `app/services/tool_runner.py`
- `docs/features/memory.md`
- `scripts/init_rag_memory.py`
- `scripts/test_rag_memory.py`

## Audit Trail

- EXTRACTED: 149 (94%)
- INFERRED: 9 (6%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*