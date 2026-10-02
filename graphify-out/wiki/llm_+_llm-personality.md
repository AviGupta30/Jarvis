# llm + llm-personality

> 45 nodes · cohesion 0.08

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
- **_reply_language_note()** (3 connections) — `app/services/llm.py`
- **_room()** (3 connections) — `app/services/llm.py`
- **Backend pieces that matter for voice** (3 connections) — `docs/features/voice.md`
- **Exception** (2 connections)
- **Models (Groq)** (2 connections) — `docs/features/llm-personality.md`
- **Router** (2 connections) — `docs/features/llm-personality.md`
- *... and 20 more nodes in this community*

## Relationships

- [assignment_tool + safe_executor](assignment_tool_+_safe_executor.md) (9 shared connections)
- [chat](chat.md) (7 shared connections)
- [dag_executor + planner](dag_executor_+_planner.md) (7 shared connections)
- [voice + context_classifier](voice_+_context_classifier.md) (4 shared connections)
- [voice_agent + acoustic_tripwire](voice_agent_+_acoustic_tripwire.md) (3 shared connections)
- [calendar_tool](calendar_tool.md) (2 shared connections)
- [gmail_tool + memory_tool](gmail_tool_+_memory_tool.md) (2 shared connections)
- [agents + tool_runner](agents_+_tool_runner.md) (2 shared connections)
- [rag_memory + memory](rag_memory_+_memory.md) (2 shared connections)
- [ui_inspector + lru](ui_inspector_+_lru.md) (1 shared connections)
- [voice](voice.md) (1 shared connections)

## Source Files

- `app/services/context_classifier.py`
- `app/services/llm.py`
- `app/services/personality.py`
- `docs/features/llm-personality.md`
- `docs/features/voice.md`
- `scripts/test_language.py`

## Audit Trail

- EXTRACTED: 99 (85%)
- INFERRED: 17 (15%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*