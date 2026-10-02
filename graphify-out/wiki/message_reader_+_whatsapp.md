# message_reader + whatsapp

> 50 nodes · cohesion 0.06

## Key Concepts

- **message_reader.py** (19 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **thread_extractor.py** (17 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **pyautogui** (15 connections)
- **subprocess** (12 connections)
- **whatsapp.py** (10 connections) — `app/services/whatsapp.py`
- **dump_wa_ui.py** (9 connections) — `dump_wa_ui.py`
- **read_messages()** (8 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **pyperclip** (8 connections)
- **pygetwindow** (7 connections)
- **_bring_whatsapp_to_front()** (6 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **_read_via_ocr()** (5 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **_focus_or_open_whatsapp()** (4 connections) — `app/services/whatsapp.py`
- **_get_whatsapp_window()** (4 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **_read_via_uia()** (4 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **_open_contact_chat()** (4 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **open_whatsapp()** (4 connections) — `app/services/whatsapp.py`
- **find_call_btn.py** (4 connections) — `find_call_btn.py`
- **get_btn_pos.py** (4 connections) — `get_btn_pos.py`
- **test_call_btn.py** (4 connections) — `test_call_btn.py`
- **test_spotify.py** (4 connections) — `test_spotify.py`
- **test_wa.py** (4 connections) — `test_wa.py`
- **_heuristic_parse_ocr_lines()** (3 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **_parse_uia_message_string()** (3 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **read_messages_as_string()** (3 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **find_controls()** (3 connections) — `dump_wa_ui.py`
- *... and 25 more nodes in this community*

## Relationships

- [assignment_tool + safe_executor](assignment_tool_+_safe_executor.md) (17 shared connections)
- [tools](tools.md) (8 shared connections)
- [style_profiler + reply_generator](style_profiler_+_reply_generator.md) (6 shared connections)
- [whatsapp_smart + whatsapp_call](whatsapp_smart_+_whatsapp_call.md) (6 shared connections)
- [ui_inspector + lru](ui_inspector_+_lru.md) (3 shared connections)
- [spotify_service](spotify_service.md) (2 shared connections)
- [youtube_player](youtube_player.md) (2 shared connections)
- [screen_reader](screen_reader.md) (1 shared connections)
- [dark_enhancement + dark_video_enhancement](dark_enhancement_+_dark_video_enhancement.md) (1 shared connections)
- [ppt_tool + ppt_image_engine](ppt_tool_+_ppt_image_engine.md) (1 shared connections)
- [refresh_docs](refresh_docs.md) (1 shared connections)
- [voice_agent + acoustic_tripwire](voice_agent_+_acoustic_tripwire.md) (1 shared connections)

## Source Files

- `app/services/whatsapp.py`
- `app/services/whatsapp_intelligence/message_reader.py`
- `app/services/whatsapp_intelligence/thread_extractor.py`
- `dump_wa_ui.py`
- `find_call_btn.py`
- `get_btn_pos.py`
- `test_call_btn.py`
- `test_spotify.py`
- `test_wa.py`

## Audit Trail

- EXTRACTED: 123 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*