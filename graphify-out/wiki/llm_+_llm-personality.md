# llm + llm-personality

> 42 nodes · cohesion 0.08

## Key Concepts

- **llm.py** (35 connections) — `app/services/llm.py`
- **generate_chat_response()** (17 connections) — `app/services/llm.py`
- **check_for_tool_intent()** (12 connections) — `app/services/llm.py`
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
- **Classify the situation from user input. Returns a dict with keys: urgency :…** (1 connections) — `app/services/context_classifier.py`
- **_load_session()** (1 connections) — `app/services/llm.py`
- *... and 17 more nodes in this community*

## Relationships

- [chat + rag_memory](chat_+_rag_memory.md) (8 shared connections)
- [assignment_tool + assignment_humanizer](assignment_tool_+_assignment_humanizer.md) (7 shared connections)
- [chat-routing + CLAUDE](chat-routing_+_CLAUDE.md) (7 shared connections)
- [voice_agent + ui_inspector](voice_agent_+_ui_inspector.md) (5 shared connections)
- [voice_agent](voice_agent.md) (4 shared connections)
- [persistence + server](persistence_+_server.md) (2 shared connections)
- [memory_tool](memory_tool.md) (2 shared connections)
- [agents + tool_runner](agents_+_tool_runner.md) (2 shared connections)
- [calendar_tool](calendar_tool.md) (1 shared connections)
- [hinglish_normalizer + voice](hinglish_normalizer_+_voice.md) (1 shared connections)
- [dump_wa_ui + test_wa](dump_wa_ui_+_test_wa.md) (1 shared connections)

## Source Files

- `app/services/context_classifier.py`
- `app/services/llm.py`
- `app/services/personality.py`
- `docs/features/llm-personality.md`
- `docs/features/voice.md`
- `scripts/test_language.py`

## Audit Trail

- EXTRACTED: 94 (85%)
- INFERRED: 16 (15%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*