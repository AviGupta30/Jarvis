# whatsapp_call + dump_wa_ui

> 31 nodes · cohesion 0.09

## Key Concepts

- **pyautogui** (15 connections)
- **subprocess** (12 connections)
- **whatsapp_call.py** (11 connections) — `app/services/whatsapp_call.py`
- **whatsapp.py** (10 connections) — `app/services/whatsapp.py`
- **dump_wa_ui.py** (9 connections) — `dump_wa_ui.py`
- **confirm_whatsapp_call()** (8 connections) — `app/services/whatsapp_call.py`
- **pyperclip** (8 connections)
- **pygetwindow** (7 connections)
- **_click_voice_call_button()** (4 connections) — `app/services/whatsapp_call.py`
- **_focus_or_open_whatsapp()** (4 connections) — `app/services/whatsapp_call.py`
- **find_call_btn.py** (4 connections) — `find_call_btn.py`
- **get_btn_pos.py** (4 connections) — `get_btn_pos.py`
- **test_call_btn.py** (4 connections) — `test_call_btn.py`
- **test_spotify.py** (4 connections) — `test_spotify.py`
- **test_wa.py** (4 connections) — `test_wa.py`
- **flow_stream()** (3 connections) — `app/api/chat.py`
- **_get_whatsapp_window()** (3 connections) — `app/services/whatsapp_call.py`
- **find_controls()** (3 connections) — `dump_wa_ui.py`
- **search_tree()** (3 connections) — `dump_wa_ui.py`
- **_type_via_clipboard()** (2 connections) — `app/services/whatsapp_call.py`
- **uiautomation** (2 connections)
- **whatsapp_call.py — Jarvis Smart WhatsApp Calling Integration (Fully Isolated)…** (1 connections) — `app/services/whatsapp_call.py`
- **Focus the WhatsApp window or open it if not running. Returns True on success.** (1 connections) — `app/services/whatsapp_call.py`
- **Click the audio call button in the WhatsApp Desktop chat header. Position is…** (1 connections) — `app/services/whatsapp_call.py`
- **WhatsApp Windows Desktop App Automation Uses the native Windows app via…** (1 connections) — `app/services/whatsapp.py`
- *... and 6 more nodes in this community*

## Relationships

- [smart_navigator + rag_memory](smart_navigator_+_rag_memory.md) (9 shared connections)
- [tools + whatsapp_smart](tools_+_whatsapp_smart.md) (7 shared connections)
- [message_reader + thread_extractor](message_reader_+_thread_extractor.md) (6 shared connections)
- [tools](tools.md) (4 shared connections)
- [whatsapp](whatsapp.md) (3 shared connections)
- [server + test_concurrency](server_+_test_concurrency.md) (3 shared connections)
- [chat + llm](chat_+_llm.md) (2 shared connections)
- [spotify_service + media_sessions](spotify_service_+_media_sessions.md) (2 shared connections)
- [youtube_player](youtube_player.md) (2 shared connections)
- [screen_vision + screen_reader](screen_vision_+_screen_reader.md) (1 shared connections)
- [dark_enhancement + dark_video_enhancement](dark_enhancement_+_dark_video_enhancement.md) (1 shared connections)
- [ppt_tool](ppt_tool.md) (1 shared connections)

## Source Files

- `app/api/chat.py`
- `app/services/whatsapp.py`
- `app/services/whatsapp_call.py`
- `dump_wa_ui.py`
- `find_call_btn.py`
- `get_btn_pos.py`
- `test_call_btn.py`
- `test_spotify.py`
- `test_wa.py`

## Audit Trail

- EXTRACTED: 87 (98%)
- INFERRED: 2 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*