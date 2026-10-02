# youtube_control

> 38 nodes · cohesion 0.11

## Key Concepts

- **youtube_control.py** (51 connections) — `app/services/youtube_control.py`
- **youtube_play_result()** (17 connections) — `app/services/youtube_control.py`
- **youtube_channel()** (15 connections) — `app/services/youtube_control.py`
- **youtube_search()** (13 connections) — `app/services/youtube_control.py`
- **youtube_control()** (12 connections) — `app/services/youtube_control.py`
- **set_last()** (8 connections) — `app/services/media_state.py`
- **_load()** (8 connections) — `app/services/youtube_control.py`
- **ensure_audible()** (8 connections) — `app/services/youtube_player.py`
- **_save()** (7 connections) — `app/services/youtube_control.py`
- **open_video()** (7 connections) — `app/services/youtube_player.py`
- **_mark_last()** (6 connections) — `app/services/youtube_control.py`
- **_short()** (6 connections) — `app/services/youtube_control.py`
- **youtube_list_results()** (6 connections) — `app/services/youtube_control.py`
- **youtube_open()** (6 connections) — `app/services/youtube_control.py`
- **_find_channel()** (5 connections) — `app/services/youtube_control.py`
- **_find_channel_at()** (5 connections) — `app/services/youtube_control.py`
- **_screen_results()** (5 connections) — `app/services/youtube_control.py`
- **_end_session()** (4 connections) — `app/services/youtube_control.py`
- **_initial_data()** (4 connections) — `app/services/youtube_control.py`
- **_resolve_choice()** (4 connections) — `app/services/youtube_control.py`
- **_dur_to_sec()** (3 connections) — `app/services/youtube_control.py`
- **walk()** (3 connections) — `app/services/youtube_control.py`
- **_format_results()** (3 connections) — `app/services/youtube_control.py`
- **app: 'spotify' | 'youtube'.** (1 connections) — `app/services/media_state.py`
- **sim()** (1 connections) — `app/services/youtube_control.py`
- *... and 13 more nodes in this community*

## Relationships

- [youtube_player](youtube_player.md) (28 shared connections)
- [youtube_control + youtube_player](youtube_control_+_youtube_player.md) (9 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (7 shared connections)
- [tools](tools.md) (6 shared connections)
- [media_state + youtube_control](media_state_+_youtube_control.md) (4 shared connections)
- [social_content_manager + ui_inspector](social_content_manager_+_ui_inspector.md) (3 shared connections)
- [media_sessions](media_sessions.md) (2 shared connections)
- [spotify_service](spotify_service.md) (2 shared connections)
- [os-control + youtube_control](os-control_+_youtube_control.md) (2 shared connections)
- [message_reader + reply_generator](message_reader_+_reply_generator.md) (1 shared connections)
- [voice_agent](voice_agent.md) (1 shared connections)
- [browser_mail](browser_mail.md) (1 shared connections)

## Source Files

- `app/services/media_state.py`
- `app/services/youtube_control.py`
- `app/services/youtube_player.py`

## Audit Trail

- EXTRACTED: 130 (89%)
- INFERRED: 16 (11%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*