# memory + rag_memory

> 51 nodes · cohesion 0.06

## Key Concepts

- **api/memory.py** (21 connections) — `app/api/memory.py`
- **recall()** (15 connections) — `app/services/rag_memory.py`
- **recall_memory()** (14 connections) — `app/api/memory.py`
- **run_tool()** (13 connections) — `app/services/tool_runner.py`
- **get_mysql_pool()** (10 connections) — `app/core/mysql_db.py`
- **format_recall_for_prompt()** (10 connections) — `app/services/rag_memory.py`
- **test_rag_memory.py** (10 connections) — `scripts/test_rag_memory.py`
- **tool_runner.py** (9 connections) — `app/services/tool_runner.py`
- **ingest_memory()** (7 connections) — `app/api/memory.py`
- **forget_turns()** (7 connections) — `app/services/rag_memory.py`
- **get_memory_stats()** (7 connections) — `app/services/rag_memory.py`
- **Memory: RAG, facts, task ledger, resume, skills** (7 connections) — `docs/features/memory.md`
- **test()** (6 connections) — `scripts/test_rag_memory.py`
- **forget_memory()** (5 connections) — `app/api/memory.py`
- **get_history()** (5 connections) — `app/api/memory.py`
- **smart_filter()** (5 connections) — `app/services/rag_memory.py`
- **RAG details** (5 connections) — `docs/features/memory.md`
- **memory_stats()** (4 connections) — `app/api/memory.py`
- **get_history()** (4 connections) — `app/services/rag_memory.py`
- **ForgetRequest** (3 connections) — `app/api/memory.py`
- **IngestRequest** (3 connections) — `app/api/memory.py`
- **BaseModel** (3 connections)
- **RecallRequest** (3 connections) — `app/api/memory.py`
- **Adding / changing a tool (project rules, from JARVIS_ARCHITECTURE.md)** (3 connections) — `CLAUDE.md`
- **get** (2 connections)
- *... and 26 more nodes in this community*

## Relationships

- [chat + youtube_control](chat_+_youtube_control.md) (17 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (7 shared connections)
- [assignment_humanizer + task_ledger](assignment_humanizer_+_task_ledger.md) (7 shared connections)
- [resume_router + tools](resume_router_+_tools.md) (5 shared connections)
- [mysql_db + rag_memory](mysql_db_+_rag_memory.md) (5 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (4 shared connections)
- [tools](tools.md) (3 shared connections)
- [main + screen_vision](main_+_screen_vision.md) (2 shared connections)
- [gmail_tool + memory_tool](gmail_tool_+_memory_tool.md) (2 shared connections)
- [agentic_web + email-calendar](agentic_web_+_email-calendar.md) (2 shared connections)
- [chat-routing + chat](chat-routing_+_chat.md) (2 shared connections)
- [style_profiler + reply_generator](style_profiler_+_reply_generator.md) (1 shared connections)

## Source Files

- `CLAUDE.md`
- `app/api/memory.py`
- `app/core/mysql_db.py`
- `app/services/rag_memory.py`
- `app/services/tool_runner.py`
- `docs/features/memory.md`
- `scripts/test_rag_memory.py`

## Audit Trail

- EXTRACTED: 119 (88%)
- INFERRED: 16 (12%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*