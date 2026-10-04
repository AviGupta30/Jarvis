# memory + tool_runner

> 40 nodes · cohesion 0.07

## Key Concepts

- **api/memory.py** (21 connections) — `app/api/memory.py`
- **recall()** (15 connections) — `app/services/rag_memory.py`
- **recall_memory()** (14 connections) — `app/api/memory.py`
- **run_tool()** (13 connections) — `app/services/tool_runner.py`
- **format_recall_for_prompt()** (10 connections) — `app/services/rag_memory.py`
- **api/tools.py** (9 connections) — `app/api/tools.py`
- **get_embedding()** (9 connections) — `app/services/embeddings.py`
- **tool_runner.py** (9 connections) — `app/services/tool_runner.py`
- **ingest_memory()** (7 connections) — `app/api/memory.py`
- **concurrent_futures** (7 connections)
- **forget_memory()** (5 connections) — `app/api/memory.py`
- **get_history()** (5 connections) — `app/api/memory.py`
- **embeddings.py** (5 connections) — `app/services/embeddings.py`
- **memory_stats()** (4 connections) — `app/api/memory.py`
- **execute_tool()** (4 connections) — `app/api/tools.py`
- **pydantic** (4 connections)
- **ForgetRequest** (3 connections) — `app/api/memory.py`
- **IngestRequest** (3 connections) — `app/api/memory.py`
- **BaseModel** (3 connections)
- **RecallRequest** (3 connections) — `app/api/memory.py`
- **ToolExecuteRequest** (3 connections) — `app/api/tools.py`
- **get** (2 connections)
- **post** (2 connections)
- **_call_sync()** (2 connections) — `app/services/tool_runner.py`
- **delete** (1 connections)
- *... and 15 more nodes in this community*

## Relationships

- [rag_memory + mysql_db](rag_memory_+_mysql_db.md) (15 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (6 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (6 shared connections)
- [tools + window_layout](tools_+_window_layout.md) (4 shared connections)
- [llm + context_classifier](llm_+_context_classifier.md) (4 shared connections)
- [ppt_router + resume_router](ppt_router_+_resume_router.md) (3 shared connections)
- [chat](chat.md) (3 shared connections)
- [vector_store + database](vector_store_+_database.md) (2 shared connections)
- [server + persistence](server_+_persistence.md) (2 shared connections)
- [main](main.md) (2 shared connections)
- [CLAUDE + agents](CLAUDE_+_agents.md) (2 shared connections)
- [memory_tool + memory](memory_tool_+_memory.md) (2 shared connections)

## Source Files

- `app/api/memory.py`
- `app/api/tools.py`
- `app/services/embeddings.py`
- `app/services/rag_memory.py`
- `app/services/tool_runner.py`

## Audit Trail

- EXTRACTED: 108 (91%)
- INFERRED: 11 (9%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*