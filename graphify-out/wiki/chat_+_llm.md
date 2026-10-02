# chat + llm

> 44 nodes · cohesion 0.07

## Key Concepts

- **chat.py** (77 connections) — `app/api/chat.py`
- **chat_endpoint()** (50 connections) — `app/api/chat.py`
- **sys** (29 connections)
- **asyncio** (15 connections)
- **_save_session()** (11 connections) — `app/services/llm.py`
- **_run_direct_tool()** (7 connections) — `app/api/chat.py`
- **_run_direct_tools()** (7 connections) — `app/api/chat.py`
- **detect_whatsapp_call()** (6 connections) — `app/api/chat.py`
- **concurrent_futures** (6 connections)
- **embeddings.py** (5 connections) — `app/services/embeddings.py`
- **get_resume_context_string()** (5 connections) — `app/services/resume_detector.py`
- **test_wa_func.py** (5 connections) — `test_wa_func.py`
- **_dag_stream_with_history()** (4 connections) — `app/api/chat.py`
- **planner_stream()** (4 connections) — `app/api/chat.py`
- **response_stream_with_history()** (4 connections) — `app/api/chat.py`
- **ChatRequest** (4 connections) — `app/api/chat.py`
- **detect_whatsapp_send()** (4 connections) — `app/api/chat.py`
- **list_resume_templates()** (4 connections) — `app/services/resume_builder.py`
- **_clean_yt_query()** (3 connections) — `app/api/chat.py`
- **clear_history()** (3 connections) — `app/api/chat.py`
- **detect_note_intent()** (3 connections) — `app/api/chat.py`
- **_explicit_platform()** (3 connections) — `app/api/chat.py`
- **_named_app()** (3 connections) — `app/api/chat.py`
- **_run_media()** (3 connections) — `app/api/chat.py`
- **test_routing.py** (3 connections) — `scripts/test_routing.py`
- *... and 19 more nodes in this community*

## Relationships

- [dag_executor + planner](dag_executor_+_planner.md) (24 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (20 shared connections)
- [rag_memory + memory](rag_memory_+_memory.md) (17 shared connections)
- [resume_builder](resume_builder.md) (11 shared connections)
- [task_ledger + test_task_resumption](task_ledger_+_test_task_resumption.md) (10 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (8 shared connections)
- [tools](tools.md) (5 shared connections)
- [youtube_control](youtube_control.md) (4 shared connections)
- [vector_store + database](vector_store_+_database.md) (3 shared connections)
- [resume_detector](resume_detector.md) (3 shared connections)
- [memory](memory.md) (3 shared connections)
- [youtube_player](youtube_player.md) (3 shared connections)

## Source Files

- `app/api/chat.py`
- `app/services/embeddings.py`
- `app/services/llm.py`
- `app/services/resume_builder.py`
- `app/services/resume_detector.py`
- `patch_window.py`
- `scripts/test_routing.py`
- `test_wa_func.py`

## Audit Trail

- EXTRACTED: 210 (94%)
- INFERRED: 13 (6%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*