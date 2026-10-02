# chat + youtube_control

> 34 nodes · cohesion 0.07

## Key Concepts

- **keyword_detect_tool()** (28 connections) — `app/api/chat.py`
- **Fixed on 2026-09-28** (16 connections) — `docs/KNOWN_ISSUES.md`
- **parse_youtube_followup()** (15 connections) — `app/services/youtube_control.py`
- **_media_compound()** (11 connections) — `app/api/chat.py`
- **_media_target()** (9 connections) — `app/api/chat.py`
- **get_last()** (9 connections) — `app/services/media_state.py`
- **youtube_tab_open()** (8 connections) — `app/services/youtube_control.py`
- **Gotchas** (8 connections) — `docs/features/os-control.md`
- **_media_intent_for()** (7 connections) — `app/api/chat.py`
- **Windows/OS control: windows, media, apps, files** (6 connections) — `docs/features/os-control.md`
- **_channel_name()** (5 connections) — `app/services/youtube_control.py`
- **_latest_of()** (5 connections) — `app/services/youtube_control.py`
- **_to_platform()** (4 connections) — `app/api/chat.py`
- **_is_positional()** (4 connections) — `app/services/youtube_control.py`
- **_last_media()** (3 connections) — `app/services/youtube_control.py`
- **flow_stream()** (1 connections) — `app/api/chat.py`
- **_is_open()** (1 connections) — `app/api/chat.py`
- **_plat()** (1 connections) — `app/api/chat.py`
- **Which player an ambiguous media command ("pause it", "next song") is for: named…** (1 connections) — `app/api/chat.py`
- **Media tool intent for one clause (YouTube-mode parser first, then keyword…** (1 connections) — `app/api/chat.py`
- **Re-target an unspecific media intent (pause/next/play X) to the given platform.** (1 connections) — `app/api/chat.py`
- **"close this song and play shape of you", "pause the video then open mrbeast's…** (1 connections) — `app/api/chat.py`
- **Fast, 100% reliable keyword-based tool detection. Runs BEFORE the LLM router to…** (1 connections) — `app/api/chat.py`
- **Last media app used within max_age seconds, else None.** (1 connections) — `app/services/media_state.py`
- **intent()** (1 connections) — `app/services/youtube_control.py`
- *... and 9 more nodes in this community*

## Relationships

- [chat + llm](chat_+_llm.md) (20 shared connections)
- [youtube_control](youtube_control.md) (12 shared connections)
- [youtube_player](youtube_player.md) (11 shared connections)
- [dag_executor + planner](dag_executor_+_planner.md) (8 shared connections)
- [tools](tools.md) (3 shared connections)
- [spotify_service](spotify_service.md) (3 shared connections)
- [tool-registry](tool-registry.md) (2 shared connections)
- [ppt + KNOWN_ISSUES](ppt_+_KNOWN_ISSUES.md) (2 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (2 shared connections)
- [window_layout](window_layout.md) (2 shared connections)
- [media_sessions](media_sessions.md) (2 shared connections)
- [ppt_studio](ppt_studio.md) (1 shared connections)

## Source Files

- `app/api/chat.py`
- `app/services/media_state.py`
- `app/services/youtube_control.py`
- `docs/KNOWN_ISSUES.md`
- `docs/features/os-control.md`

## Audit Trail

- EXTRACTED: 77 (66%)
- INFERRED: 40 (34%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*