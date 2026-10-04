# chat + chat-routing

> 43 nodes · cohesion 0.06

## Key Concepts

- **keyword_detect_tool()** (28 connections) — `app/api/chat.py`
- **`/chat` pipeline (`app/api/chat.py:chat_endpoint`, L1066)** (19 connections) — `docs/ARCHITECTURE.md`
- **parse_youtube_followup()** (15 connections) — `app/services/youtube_control.py`
- **Flow (`chat_endpoint`, order matters, first hit wins)** (12 connections) — `docs/features/chat-routing.md`
- **is_complex_task()** (10 connections) — `app/services/planner.py`
- **is_dag_task()** (9 connections) — `app/services/dag_executor.py`
- **get_last()** (9 connections) — `app/services/media_state.py`
- **enhance_prompt()** (9 connections) — `app/services/skill_prompt_enhancer.py`
- **Chat pipeline & routing (/chat)** (8 connections) — `docs/features/chat-routing.md`
- **Agents: DAG executor, linear planner, dynamic skills** (6 connections) — `docs/features/agents.md`
- **_channel_name()** (5 connections) — `app/services/youtube_control.py`
- **_latest_of()** (5 connections) — `app/services/youtube_control.py`
- **/chat request flow (short)** (5 connections) — `CLAUDE.md`
- **_semantic_window_adjust()** (4 connections) — `app/api/chat.py`
- **_clean_yt_query()** (3 connections) — `app/api/chat.py`
- **detect_note_intent()** (3 connections) — `app/api/chat.py`
- **_named_app()** (3 connections) — `app/api/chat.py`
- **_last_media()** (3 connections) — `app/services/youtube_control.py`
- **Purpose** (3 connections) — `docs/features/agents.md`
- **Gotchas** (2 connections) — `docs/features/agents.md`
- **Change recipes** (2 connections) — `docs/features/chat-routing.md`
- **flow_stream()** (1 connections) — `app/api/chat.py`
- **spotify' / 'youtube' if the sentence names a player, else '' (= whatever is…** (1 connections) — `app/api/chat.py`
- **Fast, 100% reliable keyword-based tool detection. Runs BEFORE the LLM router to…** (1 connections) — `app/api/chat.py`
- **Remove trailing action phrases from a YouTube search query.** (1 connections) — `app/api/chat.py`
- *... and 18 more nodes in this community*

## Relationships

- [chat + llm](chat_+_llm.md) (19 shared connections)
- [youtube_control](youtube_control.md) (12 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (11 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (7 shared connections)
- [spotify_service + media_sessions](spotify_service_+_media_sessions.md) (4 shared connections)
- [prompt_enhancement_library + skill_prompt_enhancer](prompt_enhancement_library_+_skill_prompt_enhancer.md) (4 shared connections)
- [chat + tools](chat_+_tools.md) (3 shared connections)
- [memory + CLAUDE](memory_+_CLAUDE.md) (3 shared connections)
- [prompt-enhancer + prompt_enhancer_button](prompt-enhancer_+_prompt_enhancer_button.md) (2 shared connections)
- [tools](tools.md) (2 shared connections)
- [file_ops](file_ops.md) (2 shared connections)
- [ppt_studio + ppt_designer](ppt_studio_+_ppt_designer.md) (1 shared connections)

## Source Files

- `CLAUDE.md`
- `app/api/chat.py`
- `app/services/dag_executor.py`
- `app/services/media_state.py`
- `app/services/planner.py`
- `app/services/skill_prompt_enhancer.py`
- `app/services/youtube_control.py`
- `docs/ARCHITECTURE.md`
- `docs/features/agents.md`
- `docs/features/chat-routing.md`

## Audit Trail

- EXTRACTED: 80 (60%)
- INFERRED: 53 (40%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*