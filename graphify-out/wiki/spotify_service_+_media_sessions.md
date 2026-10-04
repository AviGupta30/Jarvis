# spotify_service + media_sessions

> 59 nodes · cohesion 0.06

## Key Concepts

- **spotify_service.py** (31 connections) — `app/services/spotify_service.py`
- **play_song_dynamic()** (20 connections) — `app/services/spotify_service.py`
- **media_sessions.py** (18 connections) — `app/services/media_sessions.py`
- **spotify_control()** (12 connections) — `app/services/spotify_service.py`
- **control()** (11 connections) — `app/services/media_sessions.py`
- **media_command()** (8 connections) — `app/services/media_sessions.py`
- **set_last()** (8 connections) — `app/services/media_state.py`
- **sessions()** (7 connections) — `app/services/media_sessions.py`
- **_find_spotify_window()** (7 connections) — `app/services/spotify_service.py`
- **_close_spotify()** (6 connections) — `app/services/spotify_service.py`
- **_buttons()** (5 connections) — `app/services/spotify_service.py`
- **_com_init()** (5 connections) — `app/services/spotify_service.py`
- **_page_matches()** (5 connections) — `app/services/spotify_service.py`
- **_player_bar()** (5 connections) — `app/services/spotify_service.py`
- **_label()** (4 connections) — `app/services/media_sessions.py`
- **_run()** (4 connections) — `app/services/media_sessions.py`
- **_mark_last()** (4 connections) — `app/services/spotify_service.py`
- **_restore()** (4 connections) — `app/services/spotify_service.py`
- **_title_match()** (4 connections) — `app/services/spotify_service.py`
- **run()** (3 connections) — `app/services/media_sessions.py`
- **_filter()** (3 connections) — `app/services/media_sessions.py`
- **_sessions_async()** (3 connections) — `app/services/media_sessions.py`
- **_content_play_buttons()** (3 connections) — `app/services/spotify_service.py`
- **_is_playing()** (3 connections) — `app/services/spotify_service.py`
- **_now_playing_title()** (3 connections) — `app/services/spotify_service.py`
- *... and 34 more nodes in this community*

## Relationships

- [tools](tools.md) (6 shared connections)
- [youtube_player](youtube_player.md) (4 shared connections)
- [dump_wa_ui + test_wa](dump_wa_ui_+_test_wa.md) (4 shared connections)
- [benchmark + download_kokoro](benchmark_+_download_kokoro.md) (3 shared connections)
- [assignment_assembler + smart_navigator](assignment_assembler_+_smart_navigator.md) (2 shared connections)
- [chat-routing + chat](chat-routing_+_chat.md) (2 shared connections)
- [youtube_control](youtube_control.md) (2 shared connections)
- [youtube_control + os-control](youtube_control_+_os-control.md) (2 shared connections)
- [planner + dynamic_skill](planner_+_dynamic_skill.md) (1 shared connections)
- [voice_agent](voice_agent.md) (1 shared connections)
- [web_search + tools](web_search_+_tools.md) (1 shared connections)
- [tool-registry + vector_store](tool-registry_+_vector_store.md) (1 shared connections)

## Source Files

- `app/services/media_sessions.py`
- `app/services/media_state.py`
- `app/services/spotify_service.py`

## Audit Trail

- EXTRACTED: 122 (92%)
- INFERRED: 10 (8%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*