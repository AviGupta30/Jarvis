# chat + rag_memory

> 54 nodes · cohesion 0.06

## Key Concepts

- **chat.py** (77 connections) — `app/api/chat.py`
- **chat_endpoint()** (50 connections) — `app/api/chat.py`
- **store_turn()** (18 connections) — `app/services/rag_memory.py`
- **recall()** (15 connections) — `app/services/rag_memory.py`
- **_media_compound()** (11 connections) — `app/api/chat.py`
- **_save_session()** (11 connections) — `app/services/llm.py`
- **get_embedding()** (9 connections) — `app/services/embeddings.py`
- **_run_direct_tool()** (7 connections) — `app/api/chat.py`
- **_run_direct_tools()** (7 connections) — `app/api/chat.py`
- **detect_whatsapp_call()** (6 connections) — `app/api/chat.py`
- **concurrent_futures** (6 connections)
- **embeddings.py** (5 connections) — `app/services/embeddings.py`
- **test_wa_func.py** (5 connections) — `test_wa_func.py`
- **_dag_stream_with_history()** (4 connections) — `app/api/chat.py`
- **planner_stream()** (4 connections) — `app/api/chat.py`
- **response_stream_with_history()** (4 connections) — `app/api/chat.py`
- **ChatRequest** (4 connections) — `app/api/chat.py`
- **detect_whatsapp_send()** (4 connections) — `app/api/chat.py`
- **_to_platform()** (4 connections) — `app/api/chat.py`
- **_get_faiss_lock()** (4 connections) — `app/services/rag_memory.py`
- **_clean_yt_query()** (3 connections) — `app/api/chat.py`
- **clear_history()** (3 connections) — `app/api/chat.py`
- **_explicit_platform()** (3 connections) — `app/api/chat.py`
- **_named_app()** (3 connections) — `app/api/chat.py`
- **_run_media()** (3 connections) — `app/api/chat.py`
- *... and 29 more nodes in this community*

## Relationships

- [chat-routing + CLAUDE](chat-routing_+_CLAUDE.md) (19 shared connections)
- [assignment_tool + assignment_humanizer](assignment_tool_+_assignment_humanizer.md) (13 shared connections)
- [memory + memory](memory_+_memory.md) (12 shared connections)
- [youtube_control + youtube_player](youtube_control_+_youtube_player.md) (11 shared connections)
- [resume_builder](resume_builder.md) (9 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (9 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (8 shared connections)
- [task_ledger + test_task_resumption](task_ledger_+_test_task_resumption.md) (6 shared connections)
- [tools](tools.md) (5 shared connections)
- [rag_memory + test_rag_memory](rag_memory_+_test_rag_memory.md) (5 shared connections)
- [youtube_control + os-control](youtube_control_+_os-control.md) (4 shared connections)
- [resume_detector](resume_detector.md) (4 shared connections)

## Source Files

- `app/api/chat.py`
- `app/services/embeddings.py`
- `app/services/llm.py`
- `app/services/rag_memory.py`
- `test_wa_func.py`

## Audit Trail

- EXTRACTED: 204 (92%)
- INFERRED: 17 (8%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*