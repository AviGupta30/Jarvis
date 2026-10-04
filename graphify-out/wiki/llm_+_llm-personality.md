# llm + llm-personality

> 49 nodes · cohesion 0.07

## Key Concepts

- **llm.py** (35 connections) — `app/services/llm.py`
- **generate_chat_response()** (17 connections) — `app/services/llm.py`
- **check_for_tool_intent()** (12 connections) — `app/services/llm.py`
- **datetime** (11 connections)
- **detect_language()** (10 connections) — `app/services/context_classifier.py`
- **context_classifier.py** (8 connections) — `app/services/context_classifier.py`
- **_groq_generate()** (8 connections) — `app/services/llm.py`
- **pick_model()** (8 connections) — `app/services/llm.py`
- **collections** (8 connections)
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
- *... and 24 more nodes in this community*

## Relationships

- [chat + llm](chat_+_llm.md) (7 shared connections)
- [chat + chat-routing](chat_+_chat-routing.md) (7 shared connections)
- [rag_memory + mysql_db](rag_memory_+_mysql_db.md) (6 shared connections)
- [voice_agent](voice_agent.md) (5 shared connections)
- [voice + voice_agent](voice_+_voice_agent.md) (3 shared connections)
- [voice](voice.md) (3 shared connections)
- [benchmark + server](benchmark_+_server.md) (3 shared connections)
- [memory_tool + email-calendar](memory_tool_+_email-calendar.md) (3 shared connections)
- [assignment_assembler + smart_navigator](assignment_assembler_+_smart_navigator.md) (2 shared connections)
- [nlp_extractor + download_kokoro](nlp_extractor_+_download_kokoro.md) (2 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (2 shared connections)
- [style_profiler](style_profiler.md) (2 shared connections)

## Source Files

- `app/services/context_classifier.py`
- `app/services/llm.py`
- `app/services/personality.py`
- `docs/features/llm-personality.md`
- `docs/features/voice.md`
- `scripts/test_language.py`

## Audit Trail

- EXTRACTED: 121 (87%)
- INFERRED: 18 (13%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*