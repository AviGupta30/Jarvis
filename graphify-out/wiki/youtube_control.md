# youtube_control

> 38 nodes · cohesion 0.11

## Key Concepts

- **youtube_control.py** (51 connections) — `app/services/youtube_control.py`
- **youtube_play_result()** (17 connections) — `app/services/youtube_control.py`
- **youtube_channel()** (15 connections) — `app/services/youtube_control.py`
- **youtube_search()** (13 connections) — `app/services/youtube_control.py`
- **youtube_windows()** (13 connections) — `app/services/youtube_player.py`
- **youtube_control()** (12 connections) — `app/services/youtube_control.py`
- **_load()** (8 connections) — `app/services/youtube_control.py`
- **youtube_tab_open()** (8 connections) — `app/services/youtube_control.py`
- **ensure_audible()** (8 connections) — `app/services/youtube_player.py`
- **_media_intent_for()** (7 connections) — `app/api/chat.py`
- **_fetch_results()** (7 connections) — `app/services/youtube_control.py`
- **_save()** (7 connections) — `app/services/youtube_control.py`
- **youtube_session_active()** (7 connections) — `app/services/youtube_control.py`
- **open_video()** (7 connections) — `app/services/youtube_player.py`
- **_mark_last()** (6 connections) — `app/services/youtube_control.py`
- **_short()** (6 connections) — `app/services/youtube_control.py`
- **youtube_list_results()** (6 connections) — `app/services/youtube_control.py`
- **youtube_open()** (6 connections) — `app/services/youtube_control.py`
- **_end_session()** (4 connections) — `app/services/youtube_control.py`
- **_initial_data()** (4 connections) — `app/services/youtube_control.py`
- **_resolve_choice()** (4 connections) — `app/services/youtube_control.py`
- **_format_results()** (3 connections) — `app/services/youtube_control.py`
- **Media tool intent for one clause (YouTube-mode parser first, then keyword…** (1 connections) — `app/api/chat.py`
- **youtube_control.py — YouTube search, result picking, player control and…** (1 connections) — `app/services/youtube_control.py`
- **Scrape YouTube's results page → [{id,title,channel,duration,seconds,views}]; []…** (1 connections) — `app/services/youtube_control.py`
- *... and 13 more nodes in this community*

## Relationships

- [youtube_player](youtube_player.md) (24 shared connections)
- [tools](tools.md) (14 shared connections)
- [youtube_control](youtube_control.md) (12 shared connections)
- [youtube_control + os-control](youtube_control_+_os-control.md) (9 shared connections)
- [planner + dynamic_skill](planner_+_dynamic_skill.md) (4 shared connections)
- [benchmark + download_kokoro](benchmark_+_download_kokoro.md) (4 shared connections)
- [chat + llm](chat_+_llm.md) (4 shared connections)
- [chat-routing + chat](chat-routing_+_chat.md) (2 shared connections)
- [spotify_service + media_sessions](spotify_service_+_media_sessions.md) (2 shared connections)
- [tool-registry + vector_store](tool-registry_+_vector_store.md) (2 shared connections)
- [chat](chat.md) (1 shared connections)
- [assignment_assembler + smart_navigator](assignment_assembler_+_smart_navigator.md) (1 shared connections)

## Source Files

- `app/api/chat.py`
- `app/services/youtube_control.py`
- `app/services/youtube_player.py`

## Audit Trail

- EXTRACTED: 140 (88%)
- INFERRED: 20 (12%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*