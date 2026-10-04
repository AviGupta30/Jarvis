# chat + llm

> 26 nodes · cohesion 0.11

## Key Concepts

- **chat_endpoint()** (51 connections) — `app/api/chat.py`
- **Open** (15 connections) — `docs/KNOWN_ISSUES.md`
- **_save_session()** (11 connections) — `app/services/llm.py`
- **_run_direct_tool()** (7 connections) — `app/api/chat.py`
- **_run_direct_tools()** (7 connections) — `app/api/chat.py`
- **detect_whatsapp_call()** (6 connections) — `app/api/chat.py`
- **.is_echo()** (5 connections) — `app/services/voice.py`
- **test_wa_func.py** (5 connections) — `test_wa_func.py`
- **_dag_stream_with_history()** (4 connections) — `app/api/chat.py`
- **planner_stream()** (4 connections) — `app/api/chat.py`
- **response_stream_with_history()** (4 connections) — `app/api/chat.py`
- **ChatRequest** (4 connections) — `app/api/chat.py`
- **detect_whatsapp_send()** (4 connections) — `app/api/chat.py`
- **list_resume_templates()** (4 connections) — `app/services/resume_builder.py`
- **_run_media()** (3 connections) — `app/api/chat.py`
- **resume_stream()** (2 connections) — `app/api/chat.py`
- **tool_stream()** (2 connections) — `app/api/chat.py`
- **clarification_stream()** (1 connections) — `app/api/chat.py`
- **BaseModel** (1 connections)
- **post** (1 connections)
- **Run several media intents in order; one short combined reply.** (1 connections) — `app/api/chat.py`
- **Returns contact name if user wants to make a WhatsApp call, else None.** (1 connections) — `app/api/chat.py`
- **direct_stream()** (1 connections) — `app/api/chat.py`
- **direct_stream()** (1 connections) — `app/api/chat.py`
- **Call this whenever conversation_history is updated.** (1 connections) — `app/services/llm.py`
- *... and 1 more nodes in this community*

## Relationships

- [planner + dynamic_skill](planner_+_dynamic_skill.md) (18 shared connections)
- [resume_builder](resume_builder.md) (6 shared connections)
- [rag_memory + memory](rag_memory_+_memory.md) (6 shared connections)
- [tools](tools.md) (5 shared connections)
- [youtube_control](youtube_control.md) (5 shared connections)
- [dag_executor](dag_executor.md) (4 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (4 shared connections)
- [chat-routing + chat](chat-routing_+_chat.md) (3 shared connections)
- [task_ledger + test_task_resumption](task_ledger_+_test_task_resumption.md) (3 shared connections)
- [tool-registry + vector_store](tool-registry_+_vector_store.md) (3 shared connections)
- [resume_detector](resume_detector.md) (2 shared connections)
- [voice](voice.md) (2 shared connections)

## Source Files

- `app/api/chat.py`
- `app/services/llm.py`
- `app/services/resume_builder.py`
- `app/services/voice.py`
- `docs/KNOWN_ISSUES.md`
- `test_wa_func.py`

## Audit Trail

- EXTRACTED: 85 (77%)
- INFERRED: 26 (23%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*