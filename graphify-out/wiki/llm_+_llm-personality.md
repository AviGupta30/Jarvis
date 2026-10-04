# llm + llm-personality

> 52 nodes · cohesion 0.07

## Key Concepts

- **llm.py** (35 connections) — `app/services/llm.py`
- **Flow (`scripts/voice_agent.py`)** (20 connections) — `docs/features/voice.md`
- **generate_chat_response()** (17 connections) — `app/services/llm.py`
- **check_for_tool_intent()** (12 connections) — `app/services/llm.py`
- **datetime** (11 connections)
- **detect_language()** (10 connections) — `app/services/context_classifier.py`
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
- **/chat request flow (short)** (5 connections) — `CLAUDE.md`
- **Flow of `generate_chat_response`** (5 connections) — `docs/features/llm-personality.md`
- **_is_rate_limit()** (4 connections) — `app/services/llm.py`
- **_other()** (4 connections) — `app/services/llm.py`
- **_parse_reset()** (4 connections) — `app/services/llm.py`
- **_track_limits()** (4 connections) — `app/services/llm.py`
- **language_mismatch()** (4 connections) — `app/services/voice.py`
- **_reply_language_note()** (3 connections) — `app/services/llm.py`
- *... and 27 more nodes in this community*

## Relationships

- [voice_agent](voice_agent.md) (12 shared connections)
- [voice](voice.md) (10 shared connections)
- [planner + dynamic_skill](planner_+_dynamic_skill.md) (6 shared connections)
- [benchmark + download_kokoro](benchmark_+_download_kokoro.md) (5 shared connections)
- [gmail_tool + memory_tool](gmail_tool_+_memory_tool.md) (4 shared connections)
- [chat + llm](chat_+_llm.md) (4 shared connections)
- [dag_executor](dag_executor.md) (4 shared connections)
- [rag_memory + memory](rag_memory_+_memory.md) (3 shared connections)
- [assignment_assembler + smart_navigator](assignment_assembler_+_smart_navigator.md) (2 shared connections)
- [agents + tool_runner](agents_+_tool_runner.md) (2 shared connections)
- [style_profiler + reply_generator](style_profiler_+_reply_generator.md) (2 shared connections)
- [chat-routing + chat](chat-routing_+_chat.md) (2 shared connections)

## Source Files

- `CLAUDE.md`
- `app/services/context_classifier.py`
- `app/services/llm.py`
- `app/services/personality.py`
- `app/services/voice.py`
- `docs/features/llm-personality.md`
- `docs/features/voice.md`
- `scripts/test_language.py`

## Audit Trail

- EXTRACTED: 118 (76%)
- INFERRED: 37 (24%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*