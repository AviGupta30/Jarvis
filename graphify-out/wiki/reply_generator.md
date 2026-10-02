# reply_generator

> 27 nodes · cohesion 0.10

## Key Concepts

- **typing** (29 connections)
- **reply_generator.py** (21 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **generate_reply_draft()** (10 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **send_style_reply()** (9 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **lru.py** (7 connections) — `neural_cache/lru.py`
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
- *... and 2 more nodes in this community*

## Relationships

- [style_profiler](style_profiler.md) (6 shared connections)
- [thread_extractor](thread_extractor.md) (4 shared connections)
- [tools](tools.md) (3 shared connections)
- [whatsapp_smart + tools](whatsapp_smart_+_tools.md) (2 shared connections)
- [engine + test_protocol](engine_+_test_protocol.md) (2 shared connections)
- [lru](lru.md) (2 shared connections)
- [dag_executor + planner](dag_executor_+_planner.md) (2 shared connections)
- [server + test_concurrency](server_+_test_concurrency.md) (2 shared connections)
- [agentic_web](agentic_web.md) (1 shared connections)
- [task_ledger + test_task_resumption](task_ledger_+_test_task_resumption.md) (1 shared connections)
- [ssml_processor + debug_wa](ssml_processor_+_debug_wa.md) (1 shared connections)
- [client + test_concurrency](client_+_test_concurrency.md) (1 shared connections)

## Source Files

- `app/services/tools.py`
- `app/services/whatsapp_intelligence/reply_generator.py`
- `neural_cache/lru.py`

## Audit Trail

- EXTRACTED: 82 (99%)
- INFERRED: 1 (1%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*