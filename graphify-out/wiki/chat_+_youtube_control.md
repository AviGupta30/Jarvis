# chat + youtube_control

> 74 nodes · cohesion 0.05

## Key Concepts

- **chat.py** (77 connections) — `app/api/chat.py`
- **chat_endpoint()** (50 connections) — `app/api/chat.py`
- **store_turn()** (18 connections) — `app/services/rag_memory.py`
- **Fixed on 2026-09-28** (16 connections) — `docs/KNOWN_ISSUES.md`
- **parse_youtube_followup()** (15 connections) — `app/services/youtube_control.py`
- **Flow (`chat_endpoint`, order matters, first hit wins)** (12 connections) — `docs/features/chat-routing.md`
- **_media_compound()** (11 connections) — `app/api/chat.py`
- **read_file()** (11 connections) — `app/services/file_ops.py`
- **_save_session()** (11 connections) — `app/services/llm.py`
- **is_complex_task()** (10 connections) — `app/services/planner.py`
- **is_dag_task()** (9 connections) — `app/services/dag_executor.py`
- **get_embedding()** (9 connections) — `app/services/embeddings.py`
- **_media_intent_for()** (7 connections) — `app/api/chat.py`
- **_run_direct_tool()** (7 connections) — `app/api/chat.py`
- **_run_direct_tools()** (7 connections) — `app/api/chat.py`
- **youtube_session_active()** (7 connections) — `app/services/youtube_control.py`
- **concurrent_futures** (7 connections)
- **detect_whatsapp_call()** (6 connections) — `app/api/chat.py`
- **database.py** (5 connections) — `app/core/database.py`
- **get_db_pool()** (5 connections) — `app/core/database.py`
- **embeddings.py** (5 connections) — `app/services/embeddings.py`
- **get_resume_context_string()** (5 connections) — `app/services/resume_detector.py`
- **vector_store.py** (5 connections) — `app/services/vector_store.py`
- **save_document_chunk()** (5 connections) — `app/services/vector_store.py`
- **search_similar_chunks()** (5 connections) — `app/services/vector_store.py`
- *... and 49 more nodes in this community*

## Relationships

- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (28 shared connections)
- [youtube_control + youtube_player](youtube_control_+_youtube_player.md) (20 shared connections)
- [memory + rag_memory](memory_+_rag_memory.md) (17 shared connections)
- [assignment_humanizer + task_ledger](assignment_humanizer_+_task_ledger.md) (14 shared connections)
- [chat-routing + chat](chat-routing_+_chat.md) (13 shared connections)
- [resume_builder + integrate](resume_builder_+_integrate.md) (8 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (8 shared connections)
- [tools](tools.md) (6 shared connections)
- [screen_vision + screen_reader](screen_vision_+_screen_reader.md) (5 shared connections)
- [file_ops](file_ops.md) (4 shared connections)
- [media_sessions + media_state](media_sessions_+_media_state.md) (3 shared connections)
- [resume_detector](resume_detector.md) (3 shared connections)

## Source Files

- `app/api/chat.py`
- `app/core/database.py`
- `app/services/dag_executor.py`
- `app/services/embeddings.py`
- `app/services/file_ops.py`
- `app/services/llm.py`
- `app/services/planner.py`
- `app/services/rag_memory.py`
- `app/services/resume_detector.py`
- `app/services/vector_store.py`
- `app/services/youtube_control.py`
- `docs/KNOWN_ISSUES.md`
- `docs/features/agents.md`
- `docs/features/chat-routing.md`
- `test_wa_func.py`

## Audit Trail

- EXTRACTED: 238 (82%)
- INFERRED: 52 (18%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*