# llm + llm-personality

> 47 nodes · cohesion 0.07

## Key Concepts

- **llm.py** (35 connections) — `app/services/llm.py`
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
- **_reply_language_note()** (3 connections) — `app/services/llm.py`
- **_room()** (3 connections) — `app/services/llm.py`
- **Backend pieces that matter for voice** (3 connections) — `docs/features/voice.md`
- **Exception** (2 connections)
- **Models (Groq)** (2 connections) — `docs/features/llm-personality.md`
- *... and 22 more nodes in this community*

## Relationships

- [chat + youtube_control](chat_+_youtube_control.md) (8 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (6 shared connections)
- [assignment_humanizer + task_ledger](assignment_humanizer_+_task_ledger.md) (4 shared connections)
- [voice_agent](voice_agent.md) (4 shared connections)
- [voice + voice](voice_+_voice.md) (4 shared connections)
- [memory + rag_memory](memory_+_rag_memory.md) (4 shared connections)
- [smart_navigator + ssml_processor](smart_navigator_+_ssml_processor.md) (2 shared connections)
- [voice](voice.md) (2 shared connections)
- [gmail_tool + memory_tool](gmail_tool_+_memory_tool.md) (2 shared connections)
- [safe_executor + refresh_docs](safe_executor_+_refresh_docs.md) (2 shared connections)
- [chat-routing + chat](chat-routing_+_chat.md) (2 shared connections)
- [social_content_manager + content-tools](social_content_manager_+_content-tools.md) (1 shared connections)

## Source Files

- `app/services/context_classifier.py`
- `app/services/llm.py`
- `app/services/personality.py`
- `docs/features/llm-personality.md`
- `docs/features/voice.md`
- `scripts/test_language.py`

## Audit Trail

- EXTRACTED: 105 (85%)
- INFERRED: 18 (15%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*