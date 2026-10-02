# youtube_player

> 32 nodes · cohesion 0.11

## Key Concepts

- **youtube_player.py** (54 connections) — `app/services/youtube_player.py`
- **player_action()** (21 connections) — `app/services/youtube_player.py`
- **youtube_windows()** (13 connections) — `app/services/youtube_player.py`
- **send_keys()** (11 connections) — `app/services/youtube_player.py`
- **com_init()** (10 connections) — `app/services/youtube_player.py`
- **parse_player_command()** (8 connections) — `app/services/youtube_player.py`
- **_fallback()** (7 connections) — `app/services/youtube_player.py`
- **current_video_info()** (6 connections) — `app/services/youtube_player.py`
- **_focused_is_toolbar()** (5 connections) — `app/services/youtube_player.py`
- **_in_page()** (5 connections) — `app/services/youtube_player.py`
- **_js()** (5 connections) — `app/services/youtube_player.py`
- **_js_str()** (5 connections) — `app/services/youtube_player.py`
- **fmt_span()** (4 connections) — `app/services/youtube_player.py`
- **_focused_desc()** (4 connections) — `app/services/youtube_player.py`
- **parse_duration()** (4 connections) — `app/services/youtube_player.py`
- **fmt_time()** (3 connections) — `app/services/youtube_player.py`
- **_num()** (3 connections) — `app/services/youtube_player.py`
- **parse_clock()** (3 connections) — `app/services/youtube_player.py`
- **_pos()** (3 connections) — `app/services/youtube_player.py`
- **_rate()** (3 connections) — `app/services/youtube_player.py`
- **youtube_player.py — low-level bridge to the YouTube player in the user's…** (1 connections) — `app/services/youtube_player.py`
- **Is a UIA element inside the web page (has a Document ancestor)?** (1 connections) — `app/services/youtube_player.py`
- **Map a spoken player command to (action, amount, value), or None. `t` should…** (1 connections) — `app/services/youtube_player.py`
- **Focus the YouTube tab and send shortcut keys. Returns an error string or None.** (1 connections) — `app/services/youtube_player.py`
- **JSON-encode a value for embedding in the javascript: URL (no raw % or #).** (1 connections) — `app/services/youtube_player.py`
- *... and 7 more nodes in this community*

## Relationships

- [youtube_player](youtube_player.md) (38 shared connections)
- [youtube_control](youtube_control.md) (14 shared connections)
- [uia_local](uia_local.md) (5 shared connections)
- [social_content_manager + ui_inspector](social_content_manager_+_ui_inspector.md) (3 shared connections)
- [message_reader + reply_generator](message_reader_+_reply_generator.md) (3 shared connections)
- [media_state + youtube_control](media_state_+_youtube_control.md) (3 shared connections)
- [youtube_control + youtube_player](youtube_control_+_youtube_player.md) (3 shared connections)
- [window_layout + tools](window_layout_+_tools.md) (2 shared connections)
- [media_sessions](media_sessions.md) (2 shared connections)
- [content_humanizer + content-tools](content_humanizer_+_content-tools.md) (1 shared connections)
- [os-control + youtube_control](os-control_+_youtube_control.md) (1 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (1 shared connections)

## Source Files

- `app/services/youtube_player.py`

## Audit Trail

- EXTRACTED: 125 (94%)
- INFERRED: 8 (6%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*