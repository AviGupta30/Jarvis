# chat + youtube_control

> 64 nodes · cohesion 0.05

## Key Concepts

- **chat.py** (77 connections) — `app/api/chat.py`
- **keyword_detect_tool()** (28 connections) — `app/api/chat.py`
- **parse_youtube_followup()** (15 connections) — `app/services/youtube_control.py`
- **Flow (`chat_endpoint`, order matters, first hit wins)** (12 connections) — `docs/features/chat-routing.md`
- **_media_compound()** (11 connections) — `app/api/chat.py`
- **is_complex_task()** (10 connections) — `app/services/planner.py`
- **_media_target()** (9 connections) — `app/api/chat.py`
- **get_last()** (9 connections) — `app/services/media_state.py`
- **enhance_prompt()** (9 connections) — `app/services/skill_prompt_enhancer.py`
- **youtube_tab_open()** (8 connections) — `app/services/youtube_control.py`
- **Chat pipeline & routing (/chat)** (8 connections) — `docs/features/chat-routing.md`
- **Gotchas** (8 connections) — `docs/features/os-control.md`
- **_media_intent_for()** (7 connections) — `app/api/chat.py`
- **_run_direct_tool()** (7 connections) — `app/api/chat.py`
- **_run_direct_tools()** (7 connections) — `app/api/chat.py`
- **detect_whatsapp_call()** (6 connections) — `app/api/chat.py`
- **_channel_name()** (5 connections) — `app/services/youtube_control.py`
- **_latest_of()** (5 connections) — `app/services/youtube_control.py`
- **test_wa_func.py** (5 connections) — `test_wa_func.py`
- **ChatRequest** (4 connections) — `app/api/chat.py`
- **detect_whatsapp_send()** (4 connections) — `app/api/chat.py`
- **_to_platform()** (4 connections) — `app/api/chat.py`
- **_is_positional()** (4 connections) — `app/services/youtube_control.py`
- **_clean_yt_query()** (3 connections) — `app/api/chat.py`
- **clear_history()** (3 connections) — `app/api/chat.py`
- *... and 39 more nodes in this community*

## Relationships

- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (15 shared connections)
- [chat](chat.md) (15 shared connections)
- [youtube_control](youtube_control.md) (13 shared connections)
- [youtube_player](youtube_player.md) (12 shared connections)
- [tools + window_layout](tools_+_window_layout.md) (10 shared connections)
- [memory + tool_runner](memory_+_tool_runner.md) (6 shared connections)
- [file_ops](file_ops.md) (5 shared connections)
- [CLAUDE + agents](CLAUDE_+_agents.md) (5 shared connections)
- [llm + context_classifier](llm_+_context_classifier.md) (5 shared connections)
- [resume_builder + integrate](resume_builder_+_integrate.md) (4 shared connections)
- [task_ledger + resume_detector](task_ledger_+_resume_detector.md) (4 shared connections)
- [llm-personality + ARCHITECTURE](llm-personality_+_ARCHITECTURE.md) (4 shared connections)

## Source Files

- `app/api/chat.py`
- `app/services/media_state.py`
- `app/services/planner.py`
- `app/services/skill_prompt_enhancer.py`
- `app/services/youtube_control.py`
- `docs/features/chat-routing.md`
- `docs/features/os-control.md`
- `scripts/test_routing.py`
- `test_wa_func.py`

## Audit Trail

- EXTRACTED: 178 (79%)
- INFERRED: 47 (21%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*