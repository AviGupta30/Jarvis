# chat-routing + chat

> 34 nodes · cohesion 0.08

## Key Concepts

- **keyword_detect_tool()** (28 connections) — `app/api/chat.py`
- **`/chat` pipeline (`app/api/chat.py:chat_endpoint`, L1066)** (19 connections) — `docs/ARCHITECTURE.md`
- **Jump table for the big files** (15 connections) — `docs/CODEMAP.md`
- **Flow (`chat_endpoint`, order matters, first hit wins)** (12 connections) — `docs/features/chat-routing.md`
- **read_file()** (11 connections) — `app/services/file_ops.py`
- **is_complex_task()** (10 connections) — `app/services/planner.py`
- **is_dag_task()** (9 connections) — `app/services/dag_executor.py`
- **Chat pipeline & routing (/chat)** (8 connections) — `docs/features/chat-routing.md`
- **Jarvis — Claude Code guide** (7 connections) — `CLAUDE.md`
- **/chat request flow (short)** (5 connections) — `CLAUDE.md`
- **_semantic_window_adjust()** (4 connections) — `app/api/chat.py`
- **_clean_yt_query()** (3 connections) — `app/api/chat.py`
- **_named_app()** (3 connections) — `app/api/chat.py`
- **Adding / changing a tool (project rules, from JARVIS_ARCHITECTURE.md)** (3 connections) — `CLAUDE.md`
- **Purpose** (3 connections) — `docs/features/agents.md`
- **Change recipes** (2 connections) — `docs/features/chat-routing.md`
- **flow_stream()** (1 connections) — `app/api/chat.py`
- **spotify' / 'youtube' if the sentence names a player, else '' (= whatever is…** (1 connections) — `app/api/chat.py`
- **Fast, 100% reliable keyword-based tool detection. Runs BEFORE the LLM router to…** (1 connections) — `app/api/chat.py`
- **Remove trailing action phrases from a YouTube search query.** (1 connections) — `app/api/chat.py`
- **Returns True when the user's request requires a multi-branch DAG plan. More…** (1 connections) — `app/services/dag_executor.py`
- **Read and return the contents of a text file or PDF. Long files are…** (1 connections) — `app/services/file_ops.py`
- **Returns True when a task genuinely needs the multi-step agentic planner.…** (1 connections) — `app/services/planner.py`
- **CLAUDE.md** (1 connections) — `CLAUDE.md`
- **Gotchas** (1 connections) — `CLAUDE.md`
- *... and 9 more nodes in this community*

## Relationships

- [chat + llm](chat_+_llm.md) (15 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (9 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (7 shared connections)
- [chat + KNOWN_ISSUES](chat_+_KNOWN_ISSUES.md) (4 shared connections)
- [tool-registry + memory](tool-registry_+_memory.md) (4 shared connections)
- [youtube_control + youtube_player](youtube_control_+_youtube_player.md) (3 shared connections)
- [youtube_control](youtube_control.md) (3 shared connections)
- [tools + whatsapp_smart](tools_+_whatsapp_smart.md) (3 shared connections)
- [file_ops](file_ops.md) (3 shared connections)
- [ppt_tool](ppt_tool.md) (3 shared connections)
- [screen_vision + screen_reader](screen_vision_+_screen_reader.md) (2 shared connections)
- [ppt_studio](ppt_studio.md) (1 shared connections)

## Source Files

- `CLAUDE.md`
- `app/api/chat.py`
- `app/services/dag_executor.py`
- `app/services/file_ops.py`
- `app/services/planner.py`
- `docs/ARCHITECTURE.md`
- `docs/CODEMAP.md`
- `docs/features/agents.md`
- `docs/features/chat-routing.md`

## Audit Trail

- EXTRACTED: 54 (47%)
- INFERRED: 61 (53%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*