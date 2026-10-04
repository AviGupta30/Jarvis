# chat + youtube_control

> 74 nodes · cohesion 0.05

## Key Concepts

- **chat.py** (77 connections) — `app/api/chat.py`
- **chat_endpoint()** (50 connections) — `app/api/chat.py`
- **keyword_detect_tool()** (28 connections) — `app/api/chat.py`
- **store_turn()** (18 connections) — `app/services/rag_memory.py`
- **Fixed on 2026-09-28** (16 connections) — `docs/KNOWN_ISSUES.md`
- **parse_youtube_followup()** (15 connections) — `app/services/youtube_control.py`
- **Flow (`chat_endpoint`, order matters, first hit wins)** (12 connections) — `docs/features/chat-routing.md`
- **_media_compound()** (11 connections) — `app/api/chat.py`
- **_save_session()** (11 connections) — `app/services/llm.py`
- **is_complex_task()** (10 connections) — `app/services/planner.py`
- **_media_target()** (9 connections) — `app/api/chat.py`
- **get_embedding()** (9 connections) — `app/services/embeddings.py`
- **get_last()** (9 connections) — `app/services/media_state.py`
- **agentic_web_action()** (8 connections) — `app/services/agentic_web.py`
- **youtube_tab_open()** (8 connections) — `app/services/youtube_control.py`
- **_media_intent_for()** (7 connections) — `app/api/chat.py`
- **_run_direct_tool()** (7 connections) — `app/api/chat.py`
- **_run_direct_tools()** (7 connections) — `app/api/chat.py`
- **concurrent_futures** (7 connections)
- **detect_whatsapp_call()** (6 connections) — `app/api/chat.py`
- **embeddings.py** (5 connections) — `app/services/embeddings.py`
- **get_resume_context_string()** (5 connections) — `app/services/resume_detector.py`
- **_channel_name()** (5 connections) — `app/services/youtube_control.py`
- **_latest_of()** (5 connections) — `app/services/youtube_control.py`
- **test_wa_func.py** (5 connections) — `test_wa_func.py`
- *... and 49 more nodes in this community*

## Relationships

- [dag_executor + planner](dag_executor_+_planner.md) (22 shared connections)
- [youtube_control](youtube_control.md) (13 shared connections)
- [youtube_player](youtube_player.md) (12 shared connections)
- [task_ledger + rag_memory](task_ledger_+_rag_memory.md) (10 shared connections)
- [memory](memory.md) (10 shared connections)
- [tools](tools.md) (9 shared connections)
- [resume_builder + integrate](resume_builder_+_integrate.md) (8 shared connections)
- [rag_memory + tool_runner](rag_memory_+_tool_runner.md) (8 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (8 shared connections)
- [dynamic_skill + planner](dynamic_skill_+_planner.md) (6 shared connections)
- [voice_agent + download_kokoro](voice_agent_+_download_kokoro.md) (6 shared connections)
- [vector_store + database](vector_store_+_database.md) (4 shared connections)

## Source Files

- `app/api/chat.py`
- `app/services/agentic_web.py`
- `app/services/embeddings.py`
- `app/services/llm.py`
- `app/services/media_state.py`
- `app/services/planner.py`
- `app/services/rag_memory.py`
- `app/services/resume_detector.py`
- `app/services/youtube_control.py`
- `docs/KNOWN_ISSUES.md`
- `docs/features/chat-routing.md`
- `scripts/test_routing.py`
- `test_wa_func.py`

## Audit Trail

- EXTRACTED: 241 (80%)
- INFERRED: 62 (20%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*