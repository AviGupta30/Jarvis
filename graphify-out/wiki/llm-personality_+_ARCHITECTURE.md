# llm-personality + ARCHITECTURE

> 19 nodes · cohesion 0.11

## Key Concepts

- **`/chat` pipeline (`app/api/chat.py:chat_endpoint`, L1066)** (19 connections) — `docs/ARCHITECTURE.md`
- **Architecture** (8 connections) — `docs/ARCHITECTURE.md`
- **LLM layer & Jarvis personality** (8 connections) — `docs/features/llm-personality.md`
- **_is_complex_response()** (5 connections) — `app/services/llm.py`
- **_semantic_window_adjust()** (4 connections) — `app/api/chat.py`
- **detect_note_intent()** (3 connections) — `app/api/chat.py`
- **HTTP endpoints** (2 connections) — `docs/ARCHITECTURE.md`
- **Models (Groq)** (2 connections) — `docs/features/llm-personality.md`
- **Router** (2 connections) — `docs/features/llm-personality.md`
- **Decide whether to use DEEP_MODEL (complex reasoning) vs FAST_MODEL. Complex =…** (1 connections) — `app/services/llm.py`
- **ARCHITECTURE.md** (1 connections) — `docs/ARCHITECTURE.md`
- **LLM usage** (1 connections) — `docs/ARCHITECTURE.md`
- **Memory layers (five separate stores)** (1 connections) — `docs/ARCHITECTURE.md`
- **Processes** (1 connections) — `docs/ARCHITECTURE.md`
- **llm-personality.md** (1 connections) — `docs/features/llm-personality.md`
- **Files & symbols (auto-generated, line numbers are current)** (1 connections) — `docs/features/llm-personality.md`
- **Gotchas** (1 connections) — `docs/features/llm-personality.md`
- **Graphify** (1 connections) — `docs/features/llm-personality.md`
- **Purpose** (1 connections) — `docs/features/llm-personality.md`

## Relationships

- [llm + context_classifier](llm_+_context_classifier.md) (6 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (4 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (4 shared connections)
- [task_ledger + resume_detector](task_ledger_+_resume_detector.md) (2 shared connections)
- [chat](chat.md) (1 shared connections)
- [youtube_player](youtube_player.md) (1 shared connections)
- [frontend](frontend.md) (1 shared connections)
- [acoustic_tripwire](acoustic_tripwire.md) (1 shared connections)
- [CLAUDE + agents](CLAUDE_+_agents.md) (1 shared connections)
- [dark_enhancement + dark_video_enhancement](dark_enhancement_+_dark_video_enhancement.md) (1 shared connections)
- [file_ops](file_ops.md) (1 shared connections)
- [content_humanizer + content-tools](content_humanizer_+_content-tools.md) (1 shared connections)

## Source Files

- `app/api/chat.py`
- `app/services/llm.py`
- `docs/ARCHITECTURE.md`
- `docs/features/llm-personality.md`

## Audit Trail

- EXTRACTED: 22 (49%)
- INFERRED: 23 (51%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*