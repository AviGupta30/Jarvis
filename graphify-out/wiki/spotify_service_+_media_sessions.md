# spotify_service + media_sessions

> 61 nodes · cohesion 0.06

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
- **play_music()** (4 connections) — `app/services/tools.py`
- **run()** (3 connections) — `app/services/media_sessions.py`
- **_filter()** (3 connections) — `app/services/media_sessions.py`
- **_sessions_async()** (3 connections) — `app/services/media_sessions.py`
- **_content_play_buttons()** (3 connections) — `app/services/spotify_service.py`
- **_is_playing()** (3 connections) — `app/services/spotify_service.py`
- *... and 36 more nodes in this community*

## Relationships

- [smart_navigator + rag_memory](smart_navigator_+_rag_memory.md) (5 shared connections)
- [youtube_control](youtube_control.md) (5 shared connections)
- [youtube_player](youtube_player.md) (4 shared connections)
- [chat + KNOWN_ISSUES](chat_+_KNOWN_ISSUES.md) (3 shared connections)
- [server + test_concurrency](server_+_test_concurrency.md) (2 shared connections)
- [whatsapp_call + dump_wa_ui](whatsapp_call_+_dump_wa_ui.md) (2 shared connections)
- [youtube_control + youtube_player](youtube_control_+_youtube_player.md) (2 shared connections)
- [tools](tools.md) (2 shared connections)
- [tools + whatsapp_smart](tools_+_whatsapp_smart.md) (2 shared connections)
- [memory + rag_memory](memory_+_rag_memory.md) (1 shared connections)
- [voice_agent](voice_agent.md) (1 shared connections)
- [web_search + tools](web_search_+_tools.md) (1 shared connections)

## Source Files

- `app/services/media_sessions.py`
- `app/services/media_state.py`
- `app/services/spotify_service.py`
- `app/services/tools.py`

## Audit Trail

- EXTRACTED: 123 (91%)
- INFERRED: 12 (9%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*