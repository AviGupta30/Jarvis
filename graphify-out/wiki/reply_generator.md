# reply_generator

> 14 nodes · cohesion 0.20

## Key Concepts

- **reply_generator.py** (21 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **generate_reply_draft()** (10 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **_call_groq()** (4 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **_build_system_prompt()** (3 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **_build_user_prompt()** (3 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **_get_groq_api_key()** (3 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **_parse_drafts_from_response()** (3 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **reply_generator.py — Jarvis WhatsApp Intelligence: Reply Generator…** (1 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **Builds the LLM system prompt that injects the user's style profile. The LLM is…** (1 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **Builds the per-request prompt with thread context.** (1 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **Parses the LLM JSON response into a clean list of draft dicts. Handles…** (1 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **Tool-registry entry point. Reads the thread, loads the style profile, calls the…** (1 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **Resolves the Groq API key. Priority: env var → app.core.config settings (if…** (1 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **Synchronous Groq call — kept sync intentionally so this module can be called…** (1 connections) — `app/services/whatsapp_intelligence/reply_generator.py`

## Relationships

- [style_profiler + reply_generator](style_profiler_+_reply_generator.md) (8 shared connections)
- [assignment_tool + assignment_humanizer](assignment_tool_+_assignment_humanizer.md) (3 shared connections)
- [message_reader + thread_extractor](message_reader_+_thread_extractor.md) (3 shared connections)
- [tools](tools.md) (2 shared connections)
- [whatsapp_smart + whatsapp_call](whatsapp_smart_+_whatsapp_call.md) (1 shared connections)
- [persistence + server](persistence_+_server.md) (1 shared connections)

## Source Files

- `app/services/whatsapp_intelligence/reply_generator.py`

## Audit Trail

- EXTRACTED: 36 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*