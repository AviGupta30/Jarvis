# media_state + youtube_control

> 13 nodes · cohesion 0.18

## Key Concepts

- **_media_target()** (9 connections) — `app/api/chat.py`
- **media_state.py** (9 connections) — `app/services/media_state.py`
- **get_last()** (9 connections) — `app/services/media_state.py`
- **_get_process_name()** (9 connections) — `app/services/window_layout.py`
- **youtube_tab_open()** (8 connections) — `app/services/youtube_control.py`
- **spotify_running()** (6 connections) — `app/services/media_state.py`
- **_last_media()** (3 connections) — `app/services/youtube_control.py`
- **Which player an ambiguous media command ("pause it", "next song") is for: named…** (1 connections) — `app/api/chat.py`
- **media_state.py — which media app the user used last (Spotify or YouTube)…** (1 connections) — `app/services/media_state.py`
- **Last media app used within max_age seconds, else None.** (1 connections) — `app/services/media_state.py`
- **True if the Spotify desktop app has a window (cheap: EnumWindows, no UIA).** (1 connections) — `app/services/media_state.py`
- **Get the executable name of the process owning this HWND.** (1 connections) — `app/services/window_layout.py`
- **True if some browser window's active tab is YouTube.** (1 connections) — `app/services/youtube_control.py`

## Relationships

- [chat + youtube_control](chat_+_youtube_control.md) (9 shared connections)
- [youtube_player](youtube_player.md) (6 shared connections)
- [window_layout + tools](window_layout_+_tools.md) (5 shared connections)
- [youtube_control](youtube_control.md) (4 shared connections)
- [social_content_manager + ui_inspector](social_content_manager_+_ui_inspector.md) (2 shared connections)
- [media_sessions](media_sessions.md) (2 shared connections)
- [agentic_web](agentic_web.md) (1 shared connections)
- [tools](tools.md) (1 shared connections)
- [message_reader + reply_generator](message_reader_+_reply_generator.md) (1 shared connections)

## Source Files

- `app/api/chat.py`
- `app/services/media_state.py`
- `app/services/window_layout.py`
- `app/services/youtube_control.py`

## Audit Trail

- EXTRACTED: 41 (91%)
- INFERRED: 4 (9%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*