# chat-routing + CLAUDE

> 37 nodes · cohesion 0.07

## Key Concepts

- **keyword_detect_tool()** (28 connections) — `app/api/chat.py`
- **`/chat` pipeline (`app/api/chat.py:chat_endpoint`, L1066)** (19 connections) — `docs/ARCHITECTURE.md`
- **Flow (`chat_endpoint`, order matters, first hit wins)** (12 connections) — `docs/features/chat-routing.md`
- **read_file()** (11 connections) — `app/services/file_ops.py`
- **is_complex_task()** (10 connections) — `app/services/planner.py`
- **is_dag_task()** (9 connections) — `app/services/dag_executor.py`
- **Chat pipeline & routing (/chat)** (8 connections) — `docs/features/chat-routing.md`
- **_media_intent_for()** (7 connections) — `app/api/chat.py`
- **youtube_session_active()** (7 connections) — `app/services/youtube_control.py`
- **Jarvis — Claude Code guide** (7 connections) — `CLAUDE.md`
- **/chat request flow (short)** (5 connections) — `CLAUDE.md`
- **_semantic_window_adjust()** (4 connections) — `app/api/chat.py`
- **detect_note_intent()** (3 connections) — `app/api/chat.py`
- **_maybe_summarize()** (3 connections) — `app/services/file_ops.py`
- **Adding / changing a tool (project rules, from JARVIS_ARCHITECTURE.md)** (3 connections) — `CLAUDE.md`
- **Purpose** (3 connections) — `docs/features/agents.md`
- **test_routing.py** (3 connections) — `scripts/test_routing.py`
- **Change recipes** (2 connections) — `docs/features/chat-routing.md`
- **flow_stream()** (1 connections) — `app/api/chat.py`
- **Media tool intent for one clause (YouTube-mode parser first, then keyword…** (1 connections) — `app/api/chat.py`
- **Fast, 100% reliable keyword-based tool detection. Runs BEFORE the LLM router to…** (1 connections) — `app/api/chat.py`
- **Returns True when the user's request requires a multi-branch DAG plan. More…** (1 connections) — `app/services/dag_executor.py`
- **Read and return the contents of a text file or PDF. Long files are…** (1 connections) — `app/services/file_ops.py`
- **For files longer than 1000 chars, generate an LLM summary AND return the raw…** (1 connections) — `app/services/file_ops.py`
- **Returns True when a task genuinely needs the multi-step agentic planner.…** (1 connections) — `app/services/planner.py`
- *... and 12 more nodes in this community*

## Relationships

- [chat + rag_memory](chat_+_rag_memory.md) (19 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (10 shared connections)
- [youtube_control + youtube_player](youtube_control_+_youtube_player.md) (8 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (7 shared connections)
- [youtube_control + os-control](youtube_control_+_os-control.md) (4 shared connections)
- [file_ops](file_ops.md) (3 shared connections)
- [ppt_studio + ppt_content](ppt_studio_+_ppt_content.md) (2 shared connections)
- [tools](tools.md) (2 shared connections)
- [memory + memory](memory_+_memory.md) (2 shared connections)
- [prompt_enhancement_library + skill_prompt_enhancer](prompt_enhancement_library_+_skill_prompt_enhancer.md) (1 shared connections)
- [prompt-enhancer + prompt_enhancer_button](prompt-enhancer_+_prompt_enhancer_button.md) (1 shared connections)
- [agentic_web + email-calendar](agentic_web_+_email-calendar.md) (1 shared connections)

## Source Files

- `CLAUDE.md`
- `app/api/chat.py`
- `app/services/dag_executor.py`
- `app/services/file_ops.py`
- `app/services/planner.py`
- `app/services/youtube_control.py`
- `docs/ARCHITECTURE.md`
- `docs/features/agents.md`
- `docs/features/chat-routing.md`
- `scripts/test_routing.py`

## Audit Trail

- EXTRACTED: 66 (56%)
- INFERRED: 51 (44%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*