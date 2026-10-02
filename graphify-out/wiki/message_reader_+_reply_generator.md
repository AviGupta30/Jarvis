# message_reader + reply_generator

> 77 nodes · cohesion 0.04

## Key Concepts

- **time** (46 connections)
- **typing** (29 connections)
- **reply_generator.py** (21 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **message_reader.py** (19 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **thread_extractor.py** (17 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **engine.py** (16 connections) — `neural_cache/engine.py`
- **pyautogui** (15 connections)
- **persistence.py** (14 connections) — `neural_cache/persistence.py`
- **subprocess** (12 connections)
- **whatsapp.py** (10 connections) — `app/services/whatsapp.py`
- **generate_reply_draft()** (10 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **extract_thread()** (9 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **dump_wa_ui.py** (9 connections) — `dump_wa_ui.py`
- **read_messages()** (8 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **pyperclip** (8 connections)
- **lru.py** (7 connections) — `neural_cache/lru.py`
- **pygetwindow** (7 connections)
- **_bring_whatsapp_to_front()** (6 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **_read_via_ocr()** (5 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **extract_thread_as_string()** (5 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **_get_whatsapp_window()** (4 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **_read_via_uia()** (4 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **_call_groq()** (4 connections) — `app/services/whatsapp_intelligence/reply_generator.py`
- **_open_contact_chat()** (4 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **find_call_btn.py** (4 connections) — `find_call_btn.py`
- *... and 52 more nodes in this community*

## Relationships

- [social_content_manager + ui_inspector](social_content_manager_+_ui_inspector.md) (24 shared connections)
- [server + protocol](server_+_protocol.md) (17 shared connections)
- [tools](tools.md) (8 shared connections)
- [style_profiler + refresh_docs](style_profiler_+_refresh_docs.md) (6 shared connections)
- [whatsapp_smart + tools](whatsapp_smart_+_tools.md) (6 shared connections)
- [persistence](persistence.md) (5 shared connections)
- [reply_generator](reply_generator.md) (4 shared connections)
- [whatsapp_call](whatsapp_call.md) (4 shared connections)
- [whatsapp](whatsapp.md) (3 shared connections)
- [lru](lru.md) (3 shared connections)
- [test_protocol + engine](test_protocol_+_engine.md) (3 shared connections)
- [spotify_service](spotify_service.md) (3 shared connections)

## Source Files

- `app/services/whatsapp.py`
- `app/services/whatsapp_intelligence/message_reader.py`
- `app/services/whatsapp_intelligence/reply_generator.py`
- `app/services/whatsapp_intelligence/thread_extractor.py`
- `dump_wa_ui.py`
- `find_call_btn.py`
- `get_btn_pos.py`
- `neural_cache/engine.py`
- `neural_cache/lru.py`
- `neural_cache/persistence.py`
- `test_call_btn.py`
- `test_spotify.py`
- `test_wa.py`

## Audit Trail

- EXTRACTED: 254 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*