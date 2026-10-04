# memory + CLAUDE

> 41 nodes · cohesion 0.06

## Key Concepts

- **api/memory.py** (21 connections) — `app/api/memory.py`
- **recall_memory()** (14 connections) — `app/api/memory.py`
- **ingest_memory()** (7 connections) — `app/api/memory.py`
- **Jarvis — Claude Code guide** (7 connections) — `CLAUDE.md`
- **Memory: RAG, facts, task ledger, resume, skills** (7 connections) — `docs/features/memory.md`
- **forget_memory()** (5 connections) — `app/api/memory.py`
- **get_history()** (5 connections) — `app/api/memory.py`
- **database.py** (5 connections) — `app/core/database.py`
- **get_db_pool()** (5 connections) — `app/core/database.py`
- **vector_store.py** (5 connections) — `app/services/vector_store.py`
- **save_document_chunk()** (5 connections) — `app/services/vector_store.py`
- **search_similar_chunks()** (5 connections) — `app/services/vector_store.py`
- **memory_stats()** (4 connections) — `app/api/memory.py`
- **ForgetRequest** (3 connections) — `app/api/memory.py`
- **IngestRequest** (3 connections) — `app/api/memory.py`
- **BaseModel** (3 connections)
- **RecallRequest** (3 connections) — `app/api/memory.py`
- **init_db()** (3 connections) — `app/core/database.py`
- **Adding / changing a tool (project rules, from JARVIS_ARCHITECTURE.md)** (3 connections) — `CLAUDE.md`
- **get** (2 connections)
- **post** (2 connections)
- **Gotchas** (2 connections) — `docs/features/memory.md`
- **delete** (1 connections)
- **app/api/memory.py — Jarvis Long-Term Memory API Router…** (1 connections) — `app/api/memory.py`
- **Return statistics about Jarvis's long-term memory store. Includes total turns,…** (1 connections) — `app/api/memory.py`
- *... and 16 more nodes in this community*

## Relationships

- [rag_memory + mysql_db](rag_memory_+_mysql_db.md) (12 shared connections)
- [chat + llm](chat_+_llm.md) (5 shared connections)
- [chat + chat-routing](chat_+_chat-routing.md) (3 shared connections)
- [chat + tools](chat_+_tools.md) (3 shared connections)
- [memory_tool + email-calendar](memory_tool_+_email-calendar.md) (2 shared connections)
- [resume_router](resume_router.md) (1 shared connections)
- [ppt_router](ppt_router.md) (1 shared connections)
- [social_content_manager + tools](social_content_manager_+_tools.md) (1 shared connections)
- [main + screen_vision](main_+_screen_vision.md) (1 shared connections)
- [tool-registry](tool-registry.md) (1 shared connections)
- [tools](tools.md) (1 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (1 shared connections)

## Source Files

- `CLAUDE.md`
- `app/api/memory.py`
- `app/core/database.py`
- `app/services/vector_store.py`
- `docs/features/memory.md`

## Audit Trail

- EXTRACTED: 75 (88%)
- INFERRED: 10 (12%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*