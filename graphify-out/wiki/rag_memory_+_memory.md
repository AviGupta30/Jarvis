# rag_memory + memory

> 74 nodes · cohesion 0.05

## Key Concepts

- **rag_memory.py** (27 connections) — `app/services/rag_memory.py`
- **api/memory.py** (21 connections) — `app/api/memory.py`
- **store_turn()** (18 connections) — `app/services/rag_memory.py`
- **recall()** (15 connections) — `app/services/rag_memory.py`
- **recall_memory()** (14 connections) — `app/api/memory.py`
- **logging** (14 connections)
- **init_rag_memory()** (12 connections) — `app/services/rag_memory.py`
- **get_mysql_pool()** (10 connections) — `app/core/mysql_db.py`
- **format_recall_for_prompt()** (10 connections) — `app/services/rag_memory.py`
- **test_rag_memory.py** (10 connections) — `scripts/test_rag_memory.py`
- **get_embedding()** (9 connections) — `app/services/embeddings.py`
- **init_rag_memory.py** (8 connections) — `scripts/init_rag_memory.py`
- **ingest_memory()** (7 connections) — `app/api/memory.py`
- **mysql_db.py** (7 connections) — `app/core/mysql_db.py`
- **init_mysql()** (7 connections) — `app/core/mysql_db.py`
- **forget_turns()** (7 connections) — `app/services/rag_memory.py`
- **get_memory_stats()** (7 connections) — `app/services/rag_memory.py`
- **Memory: RAG, facts, task ledger, resume, skills** (7 connections) — `docs/features/memory.md`
- **close_mysql()** (6 connections) — `app/core/mysql_db.py`
- **test()** (6 connections) — `scripts/test_rag_memory.py`
- **forget_memory()** (5 connections) — `app/api/memory.py`
- **get_history()** (5 connections) — `app/api/memory.py`
- **smart_filter()** (5 connections) — `app/services/rag_memory.py`
- **RAG details** (5 connections) — `docs/features/memory.md`
- **memory_stats()** (4 connections) — `app/api/memory.py`
- *... and 49 more nodes in this community*

## Relationships

- [chat + llm](chat_+_llm.md) (17 shared connections)
- [main](main.md) (5 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (5 shared connections)
- [agents + tool_runner](agents_+_tool_runner.md) (4 shared connections)
- [dag_executor + planner](dag_executor_+_planner.md) (3 shared connections)
- [agentic_web](agentic_web.md) (3 shared connections)
- [server + test_concurrency](server_+_test_concurrency.md) (3 shared connections)
- [vector_store + database](vector_store_+_database.md) (2 shared connections)
- [memory_tool](memory_tool.md) (2 shared connections)
- [tool-registry](tool-registry.md) (2 shared connections)
- [task_ledger + test_task_resumption](task_ledger_+_test_task_resumption.md) (2 shared connections)
- [main + screen_vision](main_+_screen_vision.md) (2 shared connections)

## Source Files

- `app/api/memory.py`
- `app/core/mysql_db.py`
- `app/services/embeddings.py`
- `app/services/rag_memory.py`
- `docs/features/memory.md`
- `scripts/init_rag_memory.py`
- `scripts/test_rag_memory.py`

## Audit Trail

- EXTRACTED: 182 (93%)
- INFERRED: 14 (7%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*