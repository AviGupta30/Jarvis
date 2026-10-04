# style_profiler + reply_generator

> 53 nodes · cohesion 0.06

## Key Concepts

- **typing** (30 connections)
- **reply_generator.py** (21 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **style_profiler.py** (21 connections) — `app/services/whatsapp_intelligence/style_profiler.py`
- **generate_reply_draft()** (10 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **send_style_reply()** (9 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **_load_profile()** (9 connections) — `app/services/whatsapp_intelligence/style_profiler.py`
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
- *... and 28 more nodes in this community*

## Relationships

- [message_reader + thread_extractor](message_reader_+_thread_extractor.md) (6 shared connections)
- [tools](tools.md) (5 shared connections)
- [social_content_manager + content-tools](social_content_manager_+_content-tools.md) (3 shared connections)
- [assignment_humanizer + task_ledger](assignment_humanizer_+_task_ledger.md) (3 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (3 shared connections)
- [smart_navigator + ssml_processor](smart_navigator_+_ssml_processor.md) (2 shared connections)
- [whatsapp_smart + tools](whatsapp_smart_+_tools.md) (2 shared connections)
- [server](server.md) (2 shared connections)
- [client + test_concurrency](client_+_test_concurrency.md) (1 shared connections)
- [safe_executor + refresh_docs](safe_executor_+_refresh_docs.md) (1 shared connections)
- [memory + rag_memory](memory_+_rag_memory.md) (1 shared connections)
- [ppt_router + ppt_tool](ppt_router_+_ppt_tool.md) (1 shared connections)

## Source Files

- `app/services/tools.py`
- `app/services/whatsapp_intelligence/reply_generator.py`
- `app/services/whatsapp_intelligence/style_profiler.py`

## Audit Trail

- EXTRACTED: 128 (98%)
- INFERRED: 2 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*