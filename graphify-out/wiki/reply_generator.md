# reply_generator

> 12 nodes · cohesion 0.17

## Key Concepts

- **generate_reply_draft()** (10 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **_call_groq()** (4 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **_build_system_prompt()** (3 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **_build_user_prompt()** (3 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **_get_groq_api_key()** (3 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **_parse_drafts_from_response()** (3 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **Builds the LLM system prompt that injects the user's style profile. The LLM is…** (1 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **Builds the per-request prompt with thread context.** (1 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **Parses the LLM JSON response into a clean list of draft dicts. Handles…** (1 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **Tool-registry entry point. Reads the thread, loads the style profile, calls the…** (1 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **Resolves the Groq API key. Priority: env var → app.core.config settings (if…** (1 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **Synchronous Groq call — kept sync intentionally so this module can be called…** (1 connections) — `app/services/whatsapp_intelligence/reply_generator.py`

## Relationships

- [smart_navigator + rag_memory](smart_navigator_+_rag_memory.md) (6 shared connections)
- [tools](tools.md) (2 shared connections)
- [message_reader + thread_extractor](message_reader_+_thread_extractor.md) (1 shared connections)
- [style_profiler + reply_generator](style_profiler_+_reply_generator.md) (1 shared connections)

## Source Files

- `app/services/whatsapp_intelligence/reply_generator.py`

## Audit Trail

- EXTRACTED: 21 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*