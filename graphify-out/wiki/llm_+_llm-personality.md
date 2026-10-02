# llm + llm-personality

> 30 nodes · cohesion 0.10

## Key Concepts

- **llm.py** (35 connections) — `app/services/llm.py`
- **check_for_tool_intent()** (12 connections) — `app/services/llm.py`
- **_groq_generate()** (8 connections) — `app/services/llm.py`
- **pick_model()** (8 connections) — `app/services/llm.py`
- **LLM layer & Jarvis personality** (8 connections) — `docs/features/llm-personality.md`
- **_mark_exhausted()** (6 connections) — `app/services/llm.py`
- **_is_complex_response()** (5 connections) — `app/services/llm.py`
- **_is_rate_limit()** (4 connections) — `app/services/llm.py`
- **_other()** (4 connections) — `app/services/llm.py`
- **_parse_reset()** (4 connections) — `app/services/llm.py`
- **_track_limits()** (4 connections) — `app/services/llm.py`
- **_room()** (3 connections) — `app/services/llm.py`
- **Backend pieces that matter for voice** (3 connections) — `docs/features/voice.md`
- **Exception** (2 connections)
- **Models (Groq)** (2 connections) — `docs/features/llm-personality.md`
- **Router** (2 connections) — `docs/features/llm-personality.md`
- **_load_session()** (1 connections) — `app/services/llm.py`
- **llm.py — Jarvis LLM Brain --------------------------- Model routing (all Groq):…** (1 connections) — `app/services/llm.py`
- **Stream a response from a Groq chat model (fails over between the gpt-oss…** (1 connections) — `app/services/llm.py`
- **Decide whether to use DEEP_MODEL (complex reasoning) vs FAST_MODEL. Complex =…** (1 connections) — `app/services/llm.py`
- **Analyzes user prompt + conversation history to decide on tool use. Retries once…** (1 connections) — `app/services/llm.py`
- **Groq reset strings: '30.56s', '577ms', '1m2.5s'.** (1 connections) — `app/services/llm.py`
- **Preferred model unless its bucket can't fit `need` tokens and the other has…** (1 connections) — `app/services/llm.py`
- **A 429 (per-minute OR per-day) parks that model until Groq's 'try again in …'.** (1 connections) — `app/services/llm.py`
- **llm-personality.md** (1 connections) — `docs/features/llm-personality.md`
- *... and 5 more nodes in this community*

## Relationships

- [chat + youtube_control](chat_+_youtube_control.md) (11 shared connections)
- [context_classifier + personality](context_classifier_+_personality.md) (8 shared connections)
- [social_content_manager + ui_inspector](social_content_manager_+_ui_inspector.md) (3 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (3 shared connections)
- [message_reader + reply_generator](message_reader_+_reply_generator.md) (2 shared connections)
- [voice_agent](voice_agent.md) (1 shared connections)
- [memory_tool + calendar_tool](memory_tool_+_calendar_tool.md) (1 shared connections)
- [memory](memory.md) (1 shared connections)
- [rag_memory](rag_memory.md) (1 shared connections)
- [server + protocol](server_+_protocol.md) (1 shared connections)
- [style_profiler + refresh_docs](style_profiler_+_refresh_docs.md) (1 shared connections)
- [voice](voice.md) (1 shared connections)

## Source Files

- `app/services/llm.py`
- `docs/features/llm-personality.md`
- `docs/features/voice.md`

## Audit Trail

- EXTRACTED: 70 (89%)
- INFERRED: 9 (11%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*