# style_profiler + reply_generator

> 58 nodes · cohesion 0.05

## Key Concepts

- **reply_generator.py** (21 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **style_profiler.py** (21 connections) — `app/services/whatsapp_intelligence/style_profiler.py`
- **generate_reply_draft()** (10 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **send_style_reply()** (9 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **_load_profile()** (9 connections) — `app/services/whatsapp_intelligence/style_profiler.py`
- **extract_thread()** (9 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **_save_profile()** (8 connections) — `app/services/whatsapp_intelligence/style_profiler.py`
- **build_style_profile()** (7 connections) — `app/services/whatsapp_intelligence/style_profiler.py`
- **record_sent_reply()** (6 connections) — `app/services/whatsapp_intelligence/style_profiler.py`
- **_compute_profile_stats()** (5 connections) — `app/services/whatsapp_intelligence/style_profiler.py`
- **get_profile()** (5 connections) — `app/services/whatsapp_intelligence/style_profiler.py`
- **_call_groq()** (4 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **add_deflection_phrase()** (4 connections) — `app/services/whatsapp_intelligence/style_profiler.py`
- **_empty_profile()** (4 connections) — `app/services/whatsapp_intelligence/style_profiler.py`
- **mark_contact_formal()** (4 connections) — `app/services/whatsapp_intelligence/style_profiler.py`
- **_now()** (4 connections) — `app/services/whatsapp_intelligence/style_profiler.py`
- **_safe_filename()** (4 connections) — `app/services/whatsapp_intelligence/style_profiler.py`
- **build_style_profile()** (3 connections) — `app/services/tools.py`
- **generate_reply_draft()** (3 connections) — `app/services/tools.py`
- **_build_system_prompt()** (3 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **_build_user_prompt()** (3 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **get_cached_contact()** (3 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **get_cached_drafts()** (3 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **get_cached_incoming()** (3 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **_get_groq_api_key()** (3 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- *... and 33 more nodes in this community*

## Relationships

- [tools](tools.md) (6 shared connections)
- [assignment_tool + safe_executor](assignment_tool_+_safe_executor.md) (6 shared connections)
- [message_reader + whatsapp](message_reader_+_whatsapp.md) (6 shared connections)
- [whatsapp_smart + whatsapp_call](whatsapp_smart_+_whatsapp_call.md) (2 shared connections)
- [ui_inspector + lru](ui_inspector_+_lru.md) (2 shared connections)
- [client](client.md) (1 shared connections)
- [calendar_tool](calendar_tool.md) (1 shared connections)
- [voice_agent + acoustic_tripwire](voice_agent_+_acoustic_tripwire.md) (1 shared connections)

## Source Files

- `app/services/tools.py`
- `app/services/whatsapp_intelligence/reply_generator.py`
- `app/services/whatsapp_intelligence/style_profiler.py`
- `app/services/whatsapp_intelligence/thread_extractor.py`

## Audit Trail

- EXTRACTED: 111 (98%)
- INFERRED: 2 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*