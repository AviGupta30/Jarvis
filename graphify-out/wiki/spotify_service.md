# spotify_service

> 40 nodes · cohesion 0.09

## Key Concepts

- **spotify_service.py** (31 connections) — `app/services/spotify_service.py`
- **play_song_dynamic()** (20 connections) — `app/services/spotify_service.py`
- **spotify_control()** (12 connections) — `app/services/spotify_service.py`
- **Gotchas** (8 connections) — `docs/features/os-control.md`
- **_find_spotify_window()** (7 connections) — `app/services/spotify_service.py`
- **_close_spotify()** (6 connections) — `app/services/spotify_service.py`
- **_buttons()** (5 connections) — `app/services/spotify_service.py`
- **_com_init()** (5 connections) — `app/services/spotify_service.py`
- **_page_matches()** (5 connections) — `app/services/spotify_service.py`
- **_player_bar()** (5 connections) — `app/services/spotify_service.py`
- **_mark_last()** (4 connections) — `app/services/spotify_service.py`
- **_restore()** (4 connections) — `app/services/spotify_service.py`
- **_title_match()** (4 connections) — `app/services/spotify_service.py`
- **_is_positional()** (4 connections) — `app/services/youtube_control.py`
- **_content_play_buttons()** (3 connections) — `app/services/spotify_service.py`
- **_is_playing()** (3 connections) — `app/services/spotify_service.py`
- **_now_playing_title()** (3 connections) — `app/services/spotify_service.py`
- **_pick_target()** (3 connections) — `app/services/spotify_service.py`
- **_press()** (3 connections) — `app/services/spotify_service.py`
- **_spotify_pids()** (3 connections) — `app/services/spotify_service.py`
- **_tokens()** (3 connections) — `app/services/spotify_service.py`
- **_vision_fallback()** (3 connections) — `app/services/spotify_service.py`
- **_clean_query()** (2 connections) — `app/services/spotify_service.py`
- **_cb()** (2 connections) — `app/services/spotify_service.py`
- **_cb()** (1 connections) — `app/services/spotify_service.py`
- *... and 15 more nodes in this community*

## Relationships

- [youtube_control + youtube_player](youtube_control_+_youtube_player.md) (5 shared connections)
- [youtube_player](youtube_player.md) (4 shared connections)
- [message_reader + thread_extractor](message_reader_+_thread_extractor.md) (3 shared connections)
- [tools](tools.md) (3 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (3 shared connections)
- [media_sessions + media_state](media_sessions_+_media_state.md) (2 shared connections)
- [social_content_manager + content-tools](social_content_manager_+_content-tools.md) (1 shared connections)
- [smart_navigator + ssml_processor](smart_navigator_+_ssml_processor.md) (1 shared connections)
- [voice_agent](voice_agent.md) (1 shared connections)
- [web_search + tools](web_search_+_tools.md) (1 shared connections)
- [safe_executor + refresh_docs](safe_executor_+_refresh_docs.md) (1 shared connections)
- [os-control](os-control.md) (1 shared connections)

## Source Files

- `app/services/spotify_service.py`
- `app/services/youtube_control.py`
- `docs/features/os-control.md`

## Audit Trail

- EXTRACTED: 81 (85%)
- INFERRED: 14 (15%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*