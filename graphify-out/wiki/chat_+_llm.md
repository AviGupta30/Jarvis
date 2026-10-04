# chat + llm

> 40 nodes · cohesion 0.08

## Key Concepts

- **chat.py** (77 connections) — `app/api/chat.py`
- **chat_endpoint()** (50 connections) — `app/api/chat.py`
- **sys** (30 connections)
- **store_turn()** (18 connections) — `app/services/rag_memory.py`
- **_save_session()** (11 connections) — `app/services/llm.py`
- **_run_direct_tool()** (7 connections) — `app/api/chat.py`
- **_run_direct_tools()** (7 connections) — `app/api/chat.py`
- **concurrent_futures** (7 connections)
- **detect_whatsapp_call()** (6 connections) — `app/api/chat.py`
- **embeddings.py** (5 connections) — `app/services/embeddings.py`
- **get_resume_context_string()** (5 connections) — `app/services/resume_detector.py`
- **test_wa_func.py** (5 connections) — `test_wa_func.py`
- **_dag_stream_with_history()** (4 connections) — `app/api/chat.py`
- **planner_stream()** (4 connections) — `app/api/chat.py`
- **response_stream_with_history()** (4 connections) — `app/api/chat.py`
- **ChatRequest** (4 connections) — `app/api/chat.py`
- **detect_whatsapp_send()** (4 connections) — `app/api/chat.py`
- **list_resume_templates()** (4 connections) — `app/services/resume_builder.py`
- **clear_history()** (3 connections) — `app/api/chat.py`
- **_explicit_platform()** (3 connections) — `app/api/chat.py`
- **_run_media()** (3 connections) — `app/api/chat.py`
- **test_routing.py** (3 connections) — `scripts/test_routing.py`
- **resume_stream()** (2 connections) — `app/api/chat.py`
- **tool_stream()** (2 connections) — `app/api/chat.py`
- **app_memory** (2 connections)
- *... and 15 more nodes in this community*

## Relationships

- [rag_memory + mysql_db](rag_memory_+_mysql_db.md) (21 shared connections)
- [chat + chat-routing](chat_+_chat-routing.md) (19 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (15 shared connections)
- [youtube_control](youtube_control.md) (10 shared connections)
- [task_ledger](task_ledger.md) (8 shared connections)
- [resume_builder + integrate](resume_builder_+_integrate.md) (7 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (7 shared connections)
- [chat + tools](chat_+_tools.md) (6 shared connections)
- [memory + CLAUDE](memory_+_CLAUDE.md) (5 shared connections)
- [tools](tools.md) (5 shared connections)
- [benchmark + server](benchmark_+_server.md) (5 shared connections)
- [screen_vision + screen_reader](screen_vision_+_screen_reader.md) (4 shared connections)

## Source Files

- `app/api/chat.py`
- `app/services/embeddings.py`
- `app/services/llm.py`
- `app/services/rag_memory.py`
- `app/services/resume_builder.py`
- `app/services/resume_detector.py`
- `patch_window.py`
- `scripts/test_routing.py`
- `test_wa_func.py`

## Audit Trail

- EXTRACTED: 207 (94%)
- INFERRED: 13 (6%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*