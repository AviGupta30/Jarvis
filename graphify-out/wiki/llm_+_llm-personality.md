# llm + llm-personality

> 44 nodes · cohesion 0.08

## Key Concepts

- **llm.py** (35 connections) — `app/services/llm.py`
- **generate_chat_response()** (17 connections) — `app/services/llm.py`
- **check_for_tool_intent()** (12 connections) — `app/services/llm.py`
- **context_classifier.py** (8 connections) — `app/services/context_classifier.py`
- **_groq_generate()** (8 connections) — `app/services/llm.py`
- **pick_model()** (8 connections) — `app/services/llm.py`
- **LLM layer & Jarvis personality** (8 connections) — `docs/features/llm-personality.md`
- **classify_context()** (7 connections) — `app/services/context_classifier.py`
- **_mark_exhausted()** (6 connections) — `app/services/llm.py`
- **get_context_aware_prompt()** (6 connections) — `app/services/personality.py`
- **test_language.py** (6 connections) — `scripts/test_language.py`
- **_is_complex_response()** (5 connections) — `app/services/llm.py`
- **_maybe_compress_history()** (5 connections) — `app/services/llm.py`
- **personality.py** (5 connections) — `app/services/personality.py`
- **Flow of `generate_chat_response`** (5 connections) — `docs/features/llm-personality.md`
- **_is_rate_limit()** (4 connections) — `app/services/llm.py`
- **_other()** (4 connections) — `app/services/llm.py`
- **_parse_reset()** (4 connections) — `app/services/llm.py`
- **_track_limits()** (4 connections) — `app/services/llm.py`
- **_room()** (3 connections) — `app/services/llm.py`
- **Backend pieces that matter for voice** (3 connections) — `docs/features/voice.md`
- **Exception** (2 connections)
- **Models (Groq)** (2 connections) — `docs/features/llm-personality.md`
- **Router** (2 connections) — `docs/features/llm-personality.md`
- **context_classifier.py — Jarvis Situational Awareness…** (1 connections) — `app/services/context_classifier.py`
- *... and 19 more nodes in this community*

## Relationships

- [voice_agent + download_kokoro](voice_agent_+_download_kokoro.md) (8 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (8 shared connections)
- [voice_agent + voice](voice_agent_+_voice.md) (5 shared connections)
- [message_reader + thread_extractor](message_reader_+_thread_extractor.md) (3 shared connections)
- [rag_memory + tool_runner](rag_memory_+_tool_runner.md) (3 shared connections)
- [dag_executor + planner](dag_executor_+_planner.md) (3 shared connections)
- [task_ledger + rag_memory](task_ledger_+_rag_memory.md) (2 shared connections)
- [gmail_tool + memory_tool](gmail_tool_+_memory_tool.md) (2 shared connections)
- [memory](memory.md) (2 shared connections)
- [dynamic_skill + planner](dynamic_skill_+_planner.md) (2 shared connections)
- [CLAUDE](CLAUDE.md) (2 shared connections)
- [voice + voice](voice_+_voice.md) (1 shared connections)

## Source Files

- `app/services/context_classifier.py`
- `app/services/llm.py`
- `app/services/personality.py`
- `docs/features/llm-personality.md`
- `docs/features/voice.md`
- `scripts/test_language.py`

## Audit Trail

- EXTRACTED: 99 (86%)
- INFERRED: 16 (14%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*