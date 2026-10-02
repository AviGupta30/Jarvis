# chat + youtube_control

> 71 nodes · cohesion 0.05

## Key Concepts

- **chat.py** (76 connections) — `app/api/chat.py`
- **chat_endpoint()** (49 connections) — `app/api/chat.py`
- **keyword_detect_tool()** (28 connections) — `app/api/chat.py`
- **`/chat` pipeline (`app/api/chat.py:chat_endpoint`, L1066)** (19 connections) — `docs/ARCHITECTURE.md`
- **generate_chat_response()** (17 connections) — `app/services/llm.py`
- **parse_youtube_followup()** (15 connections) — `app/services/youtube_control.py`
- **Jump table for the big files** (15 connections) — `docs/CODEMAP.md`
- **Flow (`chat_endpoint`, order matters, first hit wins)** (12 connections) — `docs/features/chat-routing.md`
- **_media_compound()** (11 connections) — `app/api/chat.py`
- **_save_session()** (11 connections) — `app/services/llm.py`
- **is_complex_task()** (10 connections) — `app/services/planner.py`
- **is_dag_task()** (9 connections) — `app/services/dag_executor.py`
- **_media_intent_for()** (7 connections) — `app/api/chat.py`
- **_run_direct_tool()** (7 connections) — `app/api/chat.py`
- **_run_direct_tools()** (7 connections) — `app/api/chat.py`
- **youtube_session_active()** (7 connections) — `app/services/youtube_control.py`
- **detect_whatsapp_call()** (6 connections) — `app/api/chat.py`
- **concurrent_futures** (6 connections)
- **embeddings.py** (5 connections) — `app/services/embeddings.py`
- **get_resume_context_string()** (5 connections) — `app/services/resume_detector.py`
- **_channel_name()** (5 connections) — `app/services/youtube_control.py`
- **_latest_of()** (5 connections) — `app/services/youtube_control.py`
- **/chat request flow (short)** (5 connections) — `CLAUDE.md`
- **test_wa_func.py** (5 connections) — `test_wa_func.py`
- **_dag_stream_with_history()** (4 connections) — `app/api/chat.py`
- *... and 46 more nodes in this community*

## Relationships

- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (25 shared connections)
- [rag_memory](rag_memory.md) (11 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (11 shared connections)
- [media_state + youtube_control](media_state_+_youtube_control.md) (9 shared connections)
- [tools](tools.md) (9 shared connections)
- [memory](memory.md) (8 shared connections)
- [youtube_player](youtube_player.md) (8 shared connections)
- [resume_builder](resume_builder.md) (7 shared connections)
- [youtube_control](youtube_control.md) (7 shared connections)
- [task_ledger + test_task_resumption](task_ledger_+_test_task_resumption.md) (6 shared connections)
- [screen_vision + screen_reader](screen_vision_+_screen_reader.md) (5 shared connections)
- [context_classifier + personality](context_classifier_+_personality.md) (5 shared connections)

## Source Files

- `CLAUDE.md`
- `app/api/chat.py`
- `app/services/dag_executor.py`
- `app/services/embeddings.py`
- `app/services/llm.py`
- `app/services/planner.py`
- `app/services/resume_detector.py`
- `app/services/youtube_control.py`
- `docs/ARCHITECTURE.md`
- `docs/CODEMAP.md`
- `docs/features/agents.md`
- `docs/features/chat-routing.md`
- `test_wa_func.py`

## Audit Trail

- EXTRACTED: 223 (75%)
- INFERRED: 74 (25%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*