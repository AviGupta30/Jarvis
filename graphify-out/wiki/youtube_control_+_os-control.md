# youtube_control + os-control

> 18 nodes · cohesion 0.12

## Key Concepts

- **parse_youtube_followup()** (15 connections) — `app/services/youtube_control.py`
- **Gotchas** (8 connections) — `docs/features/os-control.md`
- **Windows/OS control: windows, media, apps, files** (6 connections) — `docs/features/os-control.md`
- **_channel_name()** (5 connections) — `app/services/youtube_control.py`
- **_latest_of()** (5 connections) — `app/services/youtube_control.py`
- **_js_str()** (5 connections) — `app/services/youtube_player.py`
- **_is_positional()** (4 connections) — `app/services/youtube_control.py`
- **_last_media()** (3 connections) — `app/services/youtube_control.py`
- **intent()** (1 connections) — `app/services/youtube_control.py`
- **A pick by position, not by title: 'the first result', 'number 3', 'the latest…** (1 connections) — `app/services/youtube_control.py`
- **play mrbeast's latest video' / 'play the latest video of t series' → channel…** (1 connections) — `app/services/youtube_control.py`
- **Channel name from a request like 'open MrBeast's channel', else None.** (1 connections) — `app/services/youtube_control.py`
- **Interpret a message said while in YouTube mode. Returns a tool_intent dict…** (1 connections) — `app/services/youtube_control.py`
- **JSON-encode a value for embedding in the javascript: URL (no raw % or #).** (1 connections) — `app/services/youtube_player.py`
- **os-control.md** (1 connections) — `docs/features/os-control.md`
- **Files & symbols (auto-generated, line numbers are current)** (1 connections) — `docs/features/os-control.md`
- **Graphify** (1 connections) — `docs/features/os-control.md`
- **Purpose** (1 connections) — `docs/features/os-control.md`

## Relationships

- [youtube_control](youtube_control.md) (9 shared connections)
- [youtube_player](youtube_player.md) (5 shared connections)
- [planner + dynamic_skill](planner_+_dynamic_skill.md) (4 shared connections)
- [chat-routing + chat](chat-routing_+_chat.md) (3 shared connections)
- [spotify_service + media_sessions](spotify_service_+_media_sessions.md) (2 shared connections)
- [chat + llm](chat_+_llm.md) (1 shared connections)
- [tools](tools.md) (1 shared connections)

## Source Files

- `app/services/youtube_control.py`
- `app/services/youtube_player.py`
- `docs/features/os-control.md`

## Audit Trail

- EXTRACTED: 35 (81%)
- INFERRED: 8 (19%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*