# llm + llm-personality

> 50 nodes · cohesion 0.07

## Key Concepts

- **llm.py** (35 connections) — `app/services/llm.py`
- **Flow (`scripts/voice_agent.py`)** (20 connections) — `docs/features/voice.md`
- **generate_chat_response()** (17 connections) — `app/services/llm.py`
- **check_for_tool_intent()** (12 connections) — `app/services/llm.py`
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
- **Flow of `generate_chat_response`** (5 connections) — `docs/features/llm-personality.md`
- **_is_rate_limit()** (4 connections) — `app/services/llm.py`
- **_other()** (4 connections) — `app/services/llm.py`
- **_parse_reset()** (4 connections) — `app/services/llm.py`
- **_track_limits()** (4 connections) — `app/services/llm.py`
- **language_mismatch()** (4 connections) — `app/services/voice.py`
- **_reply_language_note()** (3 connections) — `app/services/llm.py`
- **_room()** (3 connections) — `app/services/llm.py`
- **Backend pieces that matter for voice** (3 connections) — `docs/features/voice.md`
- *... and 25 more nodes in this community*

## Relationships

- [voice_agent](voice_agent.md) (12 shared connections)
- [smart_navigator + rag_memory](smart_navigator_+_rag_memory.md) (11 shared connections)
- [voice](voice.md) (10 shared connections)
- [chat-routing + chat](chat-routing_+_chat.md) (7 shared connections)
- [chat + llm](chat_+_llm.md) (6 shared connections)
- [agents + tool_runner](agents_+_tool_runner.md) (4 shared connections)
- [gmail_tool + memory_tool](gmail_tool_+_memory_tool.md) (2 shared connections)
- [voice + voice](voice_+_voice.md) (2 shared connections)
- [memory + rag_memory](memory_+_rag_memory.md) (1 shared connections)
- [refresh_docs](refresh_docs.md) (1 shared connections)
- [hinglish_normalizer](hinglish_normalizer.md) (1 shared connections)
- [server + test_concurrency](server_+_test_concurrency.md) (1 shared connections)

## Source Files

- `app/services/context_classifier.py`
- `app/services/llm.py`
- `app/services/personality.py`
- `app/services/voice.py`
- `docs/features/llm-personality.md`
- `docs/features/voice.md`
- `scripts/test_language.py`

## Audit Trail

- EXTRACTED: 108 (76%)
- INFERRED: 35 (24%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*