# rag_memory + memory

> 58 nodes · cohesion 0.05

## Key Concepts

- **api/memory.py** (21 connections) — `app/api/memory.py`
- **store_turn()** (18 connections) — `app/services/rag_memory.py`
- **recall()** (15 connections) — `app/services/rag_memory.py`
- **recall_memory()** (14 connections) — `app/api/memory.py`
- **get_mysql_pool()** (10 connections) — `app/core/mysql_db.py`
- **test_rag_memory.py** (10 connections) — `scripts/test_rag_memory.py`
- **get_embedding()** (9 connections) — `app/services/embeddings.py`
- **ingest_memory()** (7 connections) — `app/api/memory.py`
- **forget_turns()** (7 connections) — `app/services/rag_memory.py`
- **get_memory_stats()** (7 connections) — `app/services/rag_memory.py`
- **Jarvis — Claude Code guide** (7 connections) — `CLAUDE.md`
- **Memory: RAG, facts, task ledger, resume, skills** (7 connections) — `docs/features/memory.md`
- **test()** (6 connections) — `scripts/test_rag_memory.py`
- **forget_memory()** (5 connections) — `app/api/memory.py`
- **get_history()** (5 connections) — `app/api/memory.py`
- **smart_filter()** (5 connections) — `app/services/rag_memory.py`
- **RAG details** (5 connections) — `docs/features/memory.md`
- **memory_stats()** (4 connections) — `app/api/memory.py`
- **_get_faiss_lock()** (4 connections) — `app/services/rag_memory.py`
- **get_history()** (4 connections) — `app/services/rag_memory.py`
- **ForgetRequest** (3 connections) — `app/api/memory.py`
- **IngestRequest** (3 connections) — `app/api/memory.py`
- **BaseModel** (3 connections)
- **RecallRequest** (3 connections) — `app/api/memory.py`
- **_extract_topics()** (3 connections) — `app/services/rag_memory.py`
- *... and 33 more nodes in this community*

## Relationships

- [syllabus_auditor + syllabus-auditor](syllabus_auditor_+_syllabus-auditor.md) (11 shared connections)
- [chat](chat.md) (11 shared connections)
- [mysql_db + rag_memory](mysql_db_+_rag_memory.md) (5 shared connections)
- [agents + tool_runner](agents_+_tool_runner.md) (4 shared connections)
- [vector_store + database](vector_store_+_database.md) (2 shared connections)
- [ppt_router + resume_router](ppt_router_+_resume_router.md) (2 shared connections)
- [main + screen_vision](main_+_screen_vision.md) (2 shared connections)
- [dag_executor + planner](dag_executor_+_planner.md) (2 shared connections)
- [gmail_tool + memory_tool](gmail_tool_+_memory_tool.md) (2 shared connections)
- [agentic_web + email-calendar](agentic_web_+_email-calendar.md) (2 shared connections)
- [youtube_control](youtube_control.md) (2 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (2 shared connections)

## Source Files

- `CLAUDE.md`
- `app/api/memory.py`
- `app/core/mysql_db.py`
- `app/services/embeddings.py`
- `app/services/rag_memory.py`
- `docs/features/memory.md`
- `scripts/test_rag_memory.py`

## Audit Trail

- EXTRACTED: 124 (91%)
- INFERRED: 13 (9%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*