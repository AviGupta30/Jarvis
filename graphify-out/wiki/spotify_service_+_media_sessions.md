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

- [youtube_player](youtube_player.md) (7 shared connections)
- [voice_agent + download_kokoro](voice_agent_+_download_kokoro.md) (6 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (3 shared connections)
- [tools](tools.md) (3 shared connections)
- [youtube_control](youtube_control.md) (2 shared connections)
- [message_reader + thread_extractor](message_reader_+_thread_extractor.md) (2 shared connections)
- [os-control + youtube_control](os-control_+_youtube_control.md) (2 shared connections)
- [rag_memory + tool_runner](rag_memory_+_tool_runner.md) (1 shared connections)
- [window_layout](window_layout.md) (1 shared connections)
- [refresh_docs + whatsapp](refresh_docs_+_whatsapp.md) (1 shared connections)
- [web_search + tools](web_search_+_tools.md) (1 shared connections)

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