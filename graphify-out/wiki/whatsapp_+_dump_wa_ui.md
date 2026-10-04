# whatsapp + dump_wa_ui

> 25 nodes · cohesion 0.10

## Key Concepts

- **pyautogui** (15 connections)
- **subprocess** (12 connections)
- **whatsapp.py** (10 connections) — `app/services/whatsapp.py`
- **dump_wa_ui.py** (9 connections) — `dump_wa_ui.py`
- **pyperclip** (8 connections)
- **pygetwindow** (7 connections)
- **_focus_or_open_whatsapp()** (4 connections) — `app/services/whatsapp.py`
- **open_whatsapp()** (4 connections) — `app/services/whatsapp.py`
- **find_call_btn.py** (4 connections) — `find_call_btn.py`
- **get_btn_pos.py** (4 connections) — `get_btn_pos.py`
- **test_call_btn.py** (4 connections) — `test_call_btn.py`
- **test_spotify.py** (4 connections) — `test_spotify.py`
- **test_wa.py** (4 connections) — `test_wa.py`
- **find_controls()** (3 connections) — `dump_wa_ui.py`
- **search_tree()** (3 connections) — `dump_wa_ui.py`
- **uiautomation** (2 connections)
- **WhatsApp Windows Desktop App Automation Uses the native Windows app via…** (1 connections) — `app/services/whatsapp.py`
- **Focus the WhatsApp window or open it if not running. Returns True on success.** (1 connections) — `app/services/whatsapp.py`
- **Opens the WhatsApp desktop app.** (1 connections) — `app/services/whatsapp.py`
- **Dump WhatsApp Desktop UI tree to find the Voice Call button name. Run this…** (1 connections) — `dump_wa_ui.py`
- **Find the Voice Call button position in WhatsApp Desktop window. Run this while…** (1 connections) — `find_call_btn.py`
- **Step 1: Open WhatsApp, go to any chat (e.g. Archit Shukla) Step 2: Hover your…** (1 connections) — `get_btn_pos.py`
- **pywinauto** (1 connections)
- **Validate the computed call button position and take a screenshot to verify. Run…** (1 connections) — `test_call_btn.py`
- **focus_whatsapp()** (1 connections) — `test_wa.py`

## Relationships

- [benchmark + server](benchmark_+_server.md) (10 shared connections)
- [tools](tools.md) (7 shared connections)
- [whatsapp_call](whatsapp_call.md) (3 shared connections)
- [message_reader](message_reader.md) (3 shared connections)
- [thread_extractor](thread_extractor.md) (3 shared connections)
- [whatsapp_smart](whatsapp_smart.md) (3 shared connections)
- [spotify_service + media_sessions](spotify_service_+_media_sessions.md) (2 shared connections)
- [youtube_player](youtube_player.md) (2 shared connections)
- [chat + llm](chat_+_llm.md) (1 shared connections)
- [screen_vision + screen_reader](screen_vision_+_screen_reader.md) (1 shared connections)
- [dark_enhancement + dark_video_enhancement](dark_enhancement_+_dark_video_enhancement.md) (1 shared connections)
- [ppt_tool](ppt_tool.md) (1 shared connections)

## Source Files

- `app/services/whatsapp.py`
- `dump_wa_ui.py`
- `find_call_btn.py`
- `get_btn_pos.py`
- `test_call_btn.py`
- `test_spotify.py`
- `test_wa.py`

## Audit Trail

- EXTRACTED: 73 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*