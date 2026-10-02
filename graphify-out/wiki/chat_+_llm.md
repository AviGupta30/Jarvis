# chat + llm

> 33 nodes · cohesion 0.10

## Key Concepts

- **chat.py** (77 connections) — `app/api/chat.py`
- **chat_endpoint()** (50 connections) — `app/api/chat.py`
- **_save_session()** (11 connections) — `app/services/llm.py`
- **_run_direct_tool()** (7 connections) — `app/api/chat.py`
- **_run_direct_tools()** (7 connections) — `app/api/chat.py`
- **detect_whatsapp_call()** (6 connections) — `app/api/chat.py`
- **get_resume_context_string()** (5 connections) — `app/services/resume_detector.py`
- **test_wa_func.py** (5 connections) — `test_wa_func.py`
- **_dag_stream_with_history()** (4 connections) — `app/api/chat.py`
- **planner_stream()** (4 connections) — `app/api/chat.py`
- **response_stream_with_history()** (4 connections) — `app/api/chat.py`
- **ChatRequest** (4 connections) — `app/api/chat.py`
- **detect_whatsapp_send()** (4 connections) — `app/api/chat.py`
- **list_resume_templates()** (4 connections) — `app/services/resume_builder.py`
- **clear_history()** (3 connections) — `app/api/chat.py`
- **detect_note_intent()** (3 connections) — `app/api/chat.py`
- **_run_media()** (3 connections) — `app/api/chat.py`
- **test_routing.py** (3 connections) — `scripts/test_routing.py`
- **resume_stream()** (2 connections) — `app/api/chat.py`
- **tool_stream()** (2 connections) — `app/api/chat.py`
- **app_memory** (2 connections)
- **functools** (2 connections)
- **clarification_stream()** (1 connections) — `app/api/chat.py`
- **BaseModel** (1 connections)
- **delete** (1 connections)
- *... and 8 more nodes in this community*

## Relationships

- [chat-routing + chat](chat-routing_+_chat.md) (15 shared connections)
- [memory + rag_memory](memory_+_rag_memory.md) (13 shared connections)
- [resume_builder](resume_builder.md) (10 shared connections)
- [chat + KNOWN_ISSUES](chat_+_KNOWN_ISSUES.md) (9 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (8 shared connections)
- [youtube_control](youtube_control.md) (7 shared connections)
- [task_ledger + test_task_resumption](task_ledger_+_test_task_resumption.md) (6 shared connections)
- [agents + tool_runner](agents_+_tool_runner.md) (6 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (6 shared connections)
- [smart_navigator + rag_memory](smart_navigator_+_rag_memory.md) (5 shared connections)
- [youtube_control + youtube_player](youtube_control_+_youtube_player.md) (4 shared connections)
- [screen_vision + screen_reader](screen_vision_+_screen_reader.md) (4 shared connections)

## Source Files

- `app/api/chat.py`
- `app/services/llm.py`
- `app/services/resume_builder.py`
- `app/services/resume_detector.py`
- `scripts/test_routing.py`
- `test_wa_func.py`

## Audit Trail

- EXTRACTED: 157 (92%)
- INFERRED: 13 (8%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*