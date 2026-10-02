# youtube_control + os-control

> 17 nodes · cohesion 0.12

## Key Concepts

- **parse_youtube_followup()** (15 connections) — `app/services/youtube_control.py`
- **Gotchas** (8 connections) — `docs/features/os-control.md`
- **Windows/OS control: windows, media, apps, files** (6 connections) — `docs/features/os-control.md`
- **_channel_name()** (5 connections) — `app/services/youtube_control.py`
- **_latest_of()** (5 connections) — `app/services/youtube_control.py`
- **_is_positional()** (4 connections) — `app/services/youtube_control.py`
- **_resolve_choice()** (4 connections) — `app/services/youtube_control.py`
- **intent()** (1 connections) — `app/services/youtube_control.py`
- **Map a spoken choice to a result index (0-based), or 'toggle' (resume current…** (1 connections) — `app/services/youtube_control.py`
- **A pick by position, not by title: 'the first result', 'number 3', 'the latest…** (1 connections) — `app/services/youtube_control.py`
- **play mrbeast's latest video' / 'play the latest video of t series' → channel…** (1 connections) — `app/services/youtube_control.py`
- **Channel name from a request like 'open MrBeast's channel', else None.** (1 connections) — `app/services/youtube_control.py`
- **Interpret a message said while in YouTube mode. Returns a tool_intent dict…** (1 connections) — `app/services/youtube_control.py`
- **os-control.md** (1 connections) — `docs/features/os-control.md`
- **Files & symbols (auto-generated, line numbers are current)** (1 connections) — `docs/features/os-control.md`
- **Graphify** (1 connections) — `docs/features/os-control.md`
- **Purpose** (1 connections) — `docs/features/os-control.md`

## Relationships

- [youtube_control + youtube_player](youtube_control_+_youtube_player.md) (10 shared connections)
- [chat-routing + CLAUDE](chat-routing_+_CLAUDE.md) (4 shared connections)
- [chat + rag_memory](chat_+_rag_memory.md) (4 shared connections)
- [youtube_player](youtube_player.md) (3 shared connections)
- [spotify_service + media_sessions](spotify_service_+_media_sessions.md) (2 shared connections)

## Source Files

- `app/services/youtube_control.py`
- `docs/features/os-control.md`

## Audit Trail

- EXTRACTED: 32 (80%)
- INFERRED: 8 (20%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*