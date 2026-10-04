# chat-routing + chat

> 24 nodes · cohesion 0.08

## Key Concepts

- **keyword_detect_tool()** (28 connections) — `app/api/chat.py`
- **enhance_prompt()** (9 connections) — `app/services/skill_prompt_enhancer.py`
- **Chat pipeline & routing (/chat)** (8 connections) — `docs/features/chat-routing.md`
- **Jarvis — Claude Code guide** (7 connections) — `CLAUDE.md`
- **/chat request flow (short)** (5 connections) — `CLAUDE.md`
- **_clean_yt_query()** (3 connections) — `app/api/chat.py`
- **_named_app()** (3 connections) — `app/api/chat.py`
- **Change recipes** (2 connections) — `docs/features/chat-routing.md`
- **flow_stream()** (1 connections) — `app/api/chat.py`
- **spotify' / 'youtube' if the sentence names a player, else '' (= whatever is…** (1 connections) — `app/api/chat.py`
- **Fast, 100% reliable keyword-based tool detection. Runs BEFORE the LLM router to…** (1 connections) — `app/api/chat.py`
- **Remove trailing action phrases from a YouTube search query.** (1 connections) — `app/api/chat.py`
- **Enhance a prompt and return it under an **ENHANCED PROMPT (DOMAIN)** header.** (1 connections) — `app/services/skill_prompt_enhancer.py`
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

- [chat + youtube_control](chat_+_youtube_control.md) (13 shared connections)
- [prompt_enhancement_library + skill_prompt_enhancer](prompt_enhancement_library_+_skill_prompt_enhancer.md) (4 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (3 shared connections)
- [youtube_control + youtube_player](youtube_control_+_youtube_player.md) (2 shared connections)
- [prompt_enhancer_button + prompt-enhancer](prompt_enhancer_button_+_prompt-enhancer.md) (2 shared connections)
- [memory + rag_memory](memory_+_rag_memory.md) (2 shared connections)
- [tools](tools.md) (2 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (2 shared connections)
- [ppt_studio](ppt_studio.md) (1 shared connections)
- [media_sessions + media_state](media_sessions_+_media_state.md) (1 shared connections)
- [safe_executor + refresh_docs](safe_executor_+_refresh_docs.md) (1 shared connections)
- [agentic_web + email-calendar](agentic_web_+_email-calendar.md) (1 shared connections)

## Source Files

- `CLAUDE.md`
- `app/api/chat.py`
- `app/services/skill_prompt_enhancer.py`
- `docs/features/chat-routing.md`

## Audit Trail

- EXTRACTED: 41 (71%)
- INFERRED: 17 (29%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*