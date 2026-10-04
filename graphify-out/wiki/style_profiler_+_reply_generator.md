# style_profiler + reply_generator

> 82 nodes · cohesion 0.04

## Key Concepts

- **typing** (30 connections)
- **reply_generator.py** (21 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **style_profiler.py** (21 connections) — `app/services/whatsapp_intelligence/style_profiler.py`
- **message_reader.py** (19 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **thread_extractor.py** (17 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **generate_reply_draft()** (10 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **send_style_reply()** (9 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **_load_profile()** (9 connections) — `app/services/whatsapp_intelligence/style_profiler.py`
- **extract_thread()** (9 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **read_messages()** (8 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **_save_profile()** (8 connections) — `app/services/whatsapp_intelligence/style_profiler.py`
- **build_style_profile()** (7 connections) — `app/services/whatsapp_intelligence/style_profiler.py`
- **_bring_whatsapp_to_front()** (6 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **record_sent_reply()** (6 connections) — `app/services/whatsapp_intelligence/style_profiler.py`
- **_read_via_ocr()** (5 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **_compute_profile_stats()** (5 connections) — `app/services/whatsapp_intelligence/style_profiler.py`
- **get_profile()** (5 connections) — `app/services/whatsapp_intelligence/style_profiler.py`
- **extract_thread_as_string()** (5 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **_get_whatsapp_window()** (4 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **_read_via_uia()** (4 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **_call_groq()** (4 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **add_deflection_phrase()** (4 connections) — `app/services/whatsapp_intelligence/style_profiler.py`
- **_empty_profile()** (4 connections) — `app/services/whatsapp_intelligence/style_profiler.py`
- **mark_contact_formal()** (4 connections) — `app/services/whatsapp_intelligence/style_profiler.py`
- **_now()** (4 connections) — `app/services/whatsapp_intelligence/style_profiler.py`
- *... and 57 more nodes in this community*

## Relationships

- [dump_wa_ui + test_wa](dump_wa_ui_+_test_wa.md) (8 shared connections)
- [benchmark + download_kokoro](benchmark_+_download_kokoro.md) (7 shared connections)
- [tools](tools.md) (6 shared connections)
- [server + persistence](server_+_persistence.md) (5 shared connections)
- [assignment_assembler + smart_navigator](assignment_assembler_+_smart_navigator.md) (4 shared connections)
- [whatsapp_smart + tools](whatsapp_smart_+_tools.md) (3 shared connections)
- [screen_vision + screen_reader](screen_vision_+_screen_reader.md) (2 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (2 shared connections)
- [client + test_concurrency](client_+_test_concurrency.md) (1 shared connections)
- [refresh_docs](refresh_docs.md) (1 shared connections)
- [rag_memory + memory](rag_memory_+_memory.md) (1 shared connections)
- [ppt_router + ppt_tool](ppt_router_+_ppt_tool.md) (1 shared connections)

## Source Files

- `app/services/whatsapp_intelligence/message_reader.py`
- `app/services/whatsapp_intelligence/reply_generator.py`
- `app/services/whatsapp_intelligence/style_profiler.py`
- `app/services/whatsapp_intelligence/thread_extractor.py`

## Audit Trail

- EXTRACTED: 188 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*