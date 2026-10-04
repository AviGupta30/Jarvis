# reply_generator

> 24 nodes · cohesion 0.11

## Key Concepts

- **reply_generator.py** (21 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **generate_reply_draft()** (10 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **send_style_reply()** (9 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **_call_groq()** (4 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **generate_reply_draft()** (3 connections) — `app/services/tools.py`
- **_build_system_prompt()** (3 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **_build_user_prompt()** (3 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **get_cached_contact()** (3 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **get_cached_drafts()** (3 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **get_cached_incoming()** (3 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **_get_groq_api_key()** (3 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **_parse_drafts_from_response()** (3 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **Read the latest WhatsApp thread with a contact and generate 3 reply drafts that…** (1 connections) — `app/services/tools.py`
- **reply_generator.py — Jarvis WhatsApp Intelligence: Reply Generator…** (1 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **Builds the LLM system prompt that injects the user's style profile. The LLM is…** (1 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **Builds the per-request prompt with thread context.** (1 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **Parses the LLM JSON response into a clean list of draft dicts. Handles…** (1 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **Tool-registry entry point. Reads the thread, loads the style profile, calls the…** (1 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **Returns the in-memory draft cache. Used by send_style_reply() in tools.py.** (1 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **Returns the contact name from the last draft generation.** (1 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **Returns the incoming message from the last draft generation.** (1 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **Picks draft N from the cache and sends it via confirm_whatsapp_send. Args:…** (1 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **Resolves the Groq API key. Priority: env var → app.core.config settings (if…** (1 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **Synchronous Groq call — kept sync intentionally so this module can be called…** (1 connections) — `app/services/whatsapp_intelligence/reply_generator.py`

## Relationships

- [style_profiler](style_profiler.md) (5 shared connections)
- [tools + window_layout](tools_+_window_layout.md) (3 shared connections)
- [thread_extractor](thread_extractor.md) (3 shared connections)
- [jarvis_overlay + prompt_overlay](jarvis_overlay_+_prompt_overlay.md) (2 shared connections)
- [whatsapp_smart](whatsapp_smart.md) (2 shared connections)
- [assignment_assembler + smart_navigator](assignment_assembler_+_smart_navigator.md) (1 shared connections)
- [server + persistence](server_+_persistence.md) (1 shared connections)
- [client](client.md) (1 shared connections)

## Source Files

- `app/services/tools.py`
- `app/services/whatsapp_intelligence/reply_generator.py`

## Audit Trail

- EXTRACTED: 48 (98%)
- INFERRED: 1 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*