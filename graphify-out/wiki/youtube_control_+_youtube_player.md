# youtube_control + youtube_player

> 36 nodes · cohesion 0.12

## Key Concepts

- **youtube_control.py** (51 connections) — `app/services/youtube_control.py`
- **Key pieces** (49 connections) — `docs/features/os-control.md`
- **youtube_play_result()** (17 connections) — `app/services/youtube_control.py`
- **Fixed on 2026-09-28** (16 connections) — `docs/KNOWN_ISSUES.md`
- **youtube_channel()** (15 connections) — `app/services/youtube_control.py`
- **youtube_search()** (13 connections) — `app/services/youtube_control.py`
- **youtube_control()** (12 connections) — `app/services/youtube_control.py`
- **_media_target()** (9 connections) — `app/api/chat.py`
- **get_last()** (9 connections) — `app/services/media_state.py`
- **_load()** (8 connections) — `app/services/youtube_control.py`
- **youtube_tab_open()** (8 connections) — `app/services/youtube_control.py`
- **ensure_audible()** (8 connections) — `app/services/youtube_player.py`
- **_save()** (7 connections) — `app/services/youtube_control.py`
- **open_video()** (7 connections) — `app/services/youtube_player.py`
- **_mark_last()** (6 connections) — `app/services/youtube_control.py`
- **_short()** (6 connections) — `app/services/youtube_control.py`
- **youtube_list_results()** (6 connections) — `app/services/youtube_control.py`
- **youtube_open()** (6 connections) — `app/services/youtube_control.py`
- **_find_channel()** (5 connections) — `app/services/youtube_control.py`
- **_end_session()** (4 connections) — `app/services/youtube_control.py`
- **_format_results()** (3 connections) — `app/services/youtube_control.py`
- **_last_media()** (3 connections) — `app/services/youtube_control.py`
- **Which player an ambiguous media command ("pause it", "next song") is for: named…** (1 connections) — `app/api/chat.py`
- **Last media app used within max_age seconds, else None.** (1 connections) — `app/services/media_state.py`
- **youtube_control.py — YouTube search, result picking, player control and…** (1 connections) — `app/services/youtube_control.py`
- *... and 11 more nodes in this community*

## Relationships

- [youtube_player](youtube_player.md) (34 shared connections)
- [youtube_control](youtube_control.md) (16 shared connections)
- [chat + rag_memory](chat_+_rag_memory.md) (11 shared connections)
- [tools](tools.md) (10 shared connections)
- [youtube_control + os-control](youtube_control_+_os-control.md) (10 shared connections)
- [chat-routing + CLAUDE](chat-routing_+_CLAUDE.md) (8 shared connections)
- [spotify_service + media_sessions](spotify_service_+_media_sessions.md) (8 shared connections)
- [tools + ui_inspector](tools_+_ui_inspector.md) (8 shared connections)
- [window_layout](window_layout.md) (3 shared connections)
- [assignment_tool + assignment_humanizer](assignment_tool_+_assignment_humanizer.md) (3 shared connections)
- [uia_local + youtube_player](uia_local_+_youtube_player.md) (2 shared connections)
- [file_ops](file_ops.md) (2 shared connections)

## Source Files

- `app/api/chat.py`
- `app/services/media_state.py`
- `app/services/youtube_control.py`
- `app/services/youtube_player.py`
- `docs/KNOWN_ISSUES.md`
- `docs/features/os-control.md`

## Audit Trail

- EXTRACTED: 134 (65%)
- INFERRED: 72 (35%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*