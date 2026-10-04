# chat-routing + chat

> 25 nodes · cohesion 0.08

## Key Concepts

- **keyword_detect_tool()** (29 connections) — `app/api/chat.py`
- **get_last()** (9 connections) — `app/services/media_state.py`
- **Chat pipeline & routing (/chat)** (8 connections) — `docs/features/chat-routing.md`
- **Jarvis — Claude Code guide** (7 connections) — `CLAUDE.md`
- **_clean_yt_query()** (3 connections) — `app/api/chat.py`
- **_named_app()** (3 connections) — `app/api/chat.py`
- **Adding / changing a tool (project rules, from JARVIS_ARCHITECTURE.md)** (3 connections) — `CLAUDE.md`
- **test_routing.py** (3 connections) — `scripts/test_routing.py`
- **Change recipes** (2 connections) — `docs/features/chat-routing.md`
- **flow_stream()** (1 connections) — `app/api/chat.py`
- **spotify' / 'youtube' if the sentence names a player, else '' (= whatever is…** (1 connections) — `app/api/chat.py`
- **Fast, 100% reliable keyword-based tool detection. Runs BEFORE the LLM router to…** (1 connections) — `app/api/chat.py`
- **Remove trailing action phrases from a YouTube search query.** (1 connections) — `app/api/chat.py`
- **Last media app used within max_age seconds, else None.** (1 connections) — `app/services/media_state.py`
- **CLAUDE.md** (1 connections) — `CLAUDE.md`
- **Gotchas** (1 connections) — `CLAUDE.md`
- **graphify** (1 connections) — `CLAUDE.md`
- **Run** (1 connections) — `CLAUDE.md`
- **Where things are** (1 connections) — `CLAUDE.md`
- **chat-routing.md** (1 connections) — `docs/features/chat-routing.md`
- **Files & symbols (auto-generated, line numbers are current)** (1 connections) — `docs/features/chat-routing.md`
- **Gotchas** (1 connections) — `docs/features/chat-routing.md`
- **Graphify** (1 connections) — `docs/features/chat-routing.md`
- **Purpose** (1 connections) — `docs/features/chat-routing.md`
- **Response formats** (1 connections) — `docs/features/chat-routing.md`

## Relationships

- [planner + dynamic_skill](planner_+_dynamic_skill.md) (8 shared connections)
- [tool-registry + vector_store](tool-registry_+_vector_store.md) (4 shared connections)
- [chat + llm](chat_+_llm.md) (3 shared connections)
- [youtube_control + os-control](youtube_control_+_os-control.md) (3 shared connections)
- [dag_executor](dag_executor.md) (3 shared connections)
- [ppt_studio + ppt_designer](ppt_studio_+_ppt_designer.md) (2 shared connections)
- [youtube_control](youtube_control.md) (2 shared connections)
- [tools](tools.md) (2 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (2 shared connections)
- [spotify_service + media_sessions](spotify_service_+_media_sessions.md) (2 shared connections)
- [prompt_enhancement_library + skill_prompt_enhancer](prompt_enhancement_library_+_skill_prompt_enhancer.md) (1 shared connections)
- [prompt_enhancer_button](prompt_enhancer_button.md) (1 shared connections)

## Source Files

- `CLAUDE.md`
- `app/api/chat.py`
- `app/services/media_state.py`
- `docs/features/chat-routing.md`
- `scripts/test_routing.py`

## Audit Trail

- EXTRACTED: 46 (78%)
- INFERRED: 13 (22%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*