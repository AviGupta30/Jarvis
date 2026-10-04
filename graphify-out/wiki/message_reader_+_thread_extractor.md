# message_reader + thread_extractor

> 62 nodes · cohesion 0.05

## Key Concepts

- **time** (52 connections)
- **message_reader.py** (19 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **thread_extractor.py** (17 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **pyautogui** (15 connections)
- **subprocess** (12 connections)
- **whatsapp.py** (10 connections) — `app/services/whatsapp.py`
- **extract_thread()** (9 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **dump_wa_ui.py** (9 connections) — `dump_wa_ui.py`
- **read_messages()** (8 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **pyperclip** (8 connections)
- **lru.py** (7 connections) — `neural_cache/lru.py`
- **pygetwindow** (7 connections)
- **_bring_whatsapp_to_front()** (6 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **_read_via_ocr()** (5 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **extract_thread_as_string()** (5 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **_focus_or_open_whatsapp()** (4 connections) — `app/services/whatsapp.py`
- **_get_whatsapp_window()** (4 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **_read_via_uia()** (4 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **_open_contact_chat()** (4 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **open_whatsapp()** (4 connections) — `app/services/whatsapp.py`
- **dump_spotify.py** (4 connections) — `dump_spotify.py`
- **find_call_btn.py** (4 connections) — `find_call_btn.py`
- **get_btn_pos.py** (4 connections) — `get_btn_pos.py`
- **test_call_btn.py** (4 connections) — `test_call_btn.py`
- **test_spotify.py** (4 connections) — `test_spotify.py`
- *... and 37 more nodes in this community*

## Relationships

- [tools](tools.md) (8 shared connections)
- [style_profiler + reply_generator](style_profiler_+_reply_generator.md) (6 shared connections)
- [social_content_manager + content-tools](social_content_manager_+_content-tools.md) (5 shared connections)
- [whatsapp_smart + tools](whatsapp_smart_+_tools.md) (5 shared connections)
- [screen_vision + screen_reader](screen_vision_+_screen_reader.md) (4 shared connections)
- [whatsapp_call](whatsapp_call.md) (4 shared connections)
- [smart_navigator + ssml_processor](smart_navigator_+_ssml_processor.md) (3 shared connections)
- [safe_executor + refresh_docs](safe_executor_+_refresh_docs.md) (3 shared connections)
- [spotify_service](spotify_service.md) (3 shared connections)
- [youtube_player](youtube_player.md) (3 shared connections)
- [engine + test_protocol](engine_+_test_protocol.md) (2 shared connections)
- [test_lru](test_lru.md) (2 shared connections)

## Source Files

- `app/services/whatsapp.py`
- `app/services/whatsapp_intelligence/message_reader.py`
- `app/services/whatsapp_intelligence/thread_extractor.py`
- `dump_spotify.py`
- `dump_wa_ui.py`
- `find_call_btn.py`
- `get_btn_pos.py`
- `neural_cache/lru.py`
- `test_call_btn.py`
- `test_spotify.py`
- `test_wa.py`

## Audit Trail

- EXTRACTED: 185 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*