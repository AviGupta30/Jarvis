# llm + context_classifier

> 35 nodes · cohesion 0.11

## Key Concepts

- **llm.py** (35 connections) — `app/services/llm.py`
- **generate_chat_response()** (17 connections) — `app/services/llm.py`
- **check_for_tool_intent()** (12 connections) — `app/services/llm.py`
- **context_classifier.py** (8 connections) — `app/services/context_classifier.py`
- **_groq_generate()** (8 connections) — `app/services/llm.py`
- **pick_model()** (8 connections) — `app/services/llm.py`
- **classify_context()** (7 connections) — `app/services/context_classifier.py`
- **_mark_exhausted()** (6 connections) — `app/services/llm.py`
- **get_context_aware_prompt()** (6 connections) — `app/services/personality.py`
- **test_language.py** (6 connections) — `scripts/test_language.py`
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
- **context_classifier.py — Jarvis Situational Awareness…** (1 connections) — `app/services/context_classifier.py`
- **Classify the situation from user input. Returns a dict with keys: urgency :…** (1 connections) — `app/services/context_classifier.py`
- **_load_session()** (1 connections) — `app/services/llm.py`
- **llm.py — Jarvis LLM Brain --------------------------- Model routing (all Groq):…** (1 connections) — `app/services/llm.py`
- *... and 10 more nodes in this community*

## Relationships

- [llm-personality + ARCHITECTURE](llm-personality_+_ARCHITECTURE.md) (6 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (5 shared connections)
- [voice + context_classifier](voice_+_context_classifier.md) (4 shared connections)
- [server + persistence](server_+_persistence.md) (4 shared connections)
- [memory + tool_runner](memory_+_tool_runner.md) (4 shared connections)
- [jarvis_overlay + prompt_overlay](jarvis_overlay_+_prompt_overlay.md) (3 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (3 shared connections)
- [chat](chat.md) (3 shared connections)
- [calendar_tool + email-calendar](calendar_tool_+_email-calendar.md) (2 shared connections)
- [assignment_assembler + smart_navigator](assignment_assembler_+_smart_navigator.md) (2 shared connections)
- [voice_agent](voice_agent.md) (2 shared connections)
- [memory_tool + memory](memory_tool_+_memory.md) (2 shared connections)

## Source Files

- `app/services/context_classifier.py`
- `app/services/llm.py`
- `app/services/personality.py`
- `docs/features/llm-personality.md`
- `docs/features/voice.md`
- `scripts/test_language.py`

## Audit Trail

- EXTRACTED: 91 (86%)
- INFERRED: 15 (14%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*