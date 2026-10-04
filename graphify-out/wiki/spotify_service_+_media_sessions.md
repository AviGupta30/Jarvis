# spotify_service + media_sessions

> 67 nodes · cohesion 0.05

## Key Concepts

- **spotify_service.py** (31 connections) — `app/services/spotify_service.py`
- **play_song_dynamic()** (20 connections) — `app/services/spotify_service.py`
- **media_sessions.py** (18 connections) — `app/services/media_sessions.py`
- **spotify_control()** (12 connections) — `app/services/spotify_service.py`
- **control()** (11 connections) — `app/services/media_sessions.py`
- **media_command()** (8 connections) — `app/services/media_sessions.py`
- **set_last()** (8 connections) — `app/services/media_state.py`
- **Gotchas** (8 connections) — `docs/features/os-control.md`
- **sessions()** (7 connections) — `app/services/media_sessions.py`
- **_find_spotify_window()** (7 connections) — `app/services/spotify_service.py`
- **_close_spotify()** (6 connections) — `app/services/spotify_service.py`
- **Windows/OS control: windows, media, apps, files** (6 connections) — `docs/features/os-control.md`
- **_buttons()** (5 connections) — `app/services/spotify_service.py`
- **_com_init()** (5 connections) — `app/services/spotify_service.py`
- **_page_matches()** (5 connections) — `app/services/spotify_service.py`
- **_player_bar()** (5 connections) — `app/services/spotify_service.py`
- **_label()** (4 connections) — `app/services/media_sessions.py`
- **_run()** (4 connections) — `app/services/media_sessions.py`
- **_mark_last()** (4 connections) — `app/services/spotify_service.py`
- **_restore()** (4 connections) — `app/services/spotify_service.py`
- **_title_match()** (4 connections) — `app/services/spotify_service.py`
- **_is_positional()** (4 connections) — `app/services/youtube_control.py`
- **run()** (3 connections) — `app/services/media_sessions.py`
- **_filter()** (3 connections) — `app/services/media_sessions.py`
- **_sessions_async()** (3 connections) — `app/services/media_sessions.py`
- *... and 42 more nodes in this community*

## Relationships

- [youtube_control](youtube_control.md) (8 shared connections)
- [youtube_player](youtube_player.md) (6 shared connections)
- [chat + chat-routing](chat_+_chat-routing.md) (4 shared connections)
- [benchmark + server](benchmark_+_server.md) (3 shared connections)
- [tools](tools.md) (3 shared connections)
- [assignment_assembler + smart_navigator](assignment_assembler_+_smart_navigator.md) (2 shared connections)
- [chat + llm](chat_+_llm.md) (2 shared connections)
- [whatsapp + dump_wa_ui](whatsapp_+_dump_wa_ui.md) (2 shared connections)
- [rag_memory + mysql_db](rag_memory_+_mysql_db.md) (1 shared connections)
- [voice_agent](voice_agent.md) (1 shared connections)
- [web_search](web_search.md) (1 shared connections)
- [chat + tools](chat_+_tools.md) (1 shared connections)

## Source Files

- `app/services/media_sessions.py`
- `app/services/media_state.py`
- `app/services/spotify_service.py`
- `app/services/youtube_control.py`
- `docs/features/os-control.md`

## Audit Trail

- EXTRACTED: 131 (90%)
- INFERRED: 15 (10%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*