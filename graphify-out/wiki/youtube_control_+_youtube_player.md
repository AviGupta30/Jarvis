# youtube_control + youtube_player

> 22 nodes · cohesion 0.10

## Key Concepts

- **parse_youtube_followup()** (15 connections) — `app/services/youtube_control.py`
- **parse_player_command()** (8 connections) — `app/services/youtube_player.py`
- **Gotchas** (8 connections) — `docs/features/os-control.md`
- **Windows/OS control: windows, media, apps, files** (6 connections) — `docs/features/os-control.md`
- **_channel_name()** (5 connections) — `app/services/youtube_control.py`
- **_latest_of()** (5 connections) — `app/services/youtube_control.py`
- **_is_positional()** (4 connections) — `app/services/youtube_control.py`
- **parse_duration()** (4 connections) — `app/services/youtube_player.py`
- **_num()** (3 connections) — `app/services/youtube_player.py`
- **parse_clock()** (3 connections) — `app/services/youtube_player.py`
- **intent()** (1 connections) — `app/services/youtube_control.py`
- **A pick by position, not by title: 'the first result', 'number 3', 'the latest…** (1 connections) — `app/services/youtube_control.py`
- **play mrbeast's latest video' / 'play the latest video of t series' → channel…** (1 connections) — `app/services/youtube_control.py`
- **Channel name from a request like 'open MrBeast's channel', else None.** (1 connections) — `app/services/youtube_control.py`
- **Interpret a message said while in YouTube mode. Returns a tool_intent dict…** (1 connections) — `app/services/youtube_control.py`
- **Map a spoken player command to (action, amount, value), or None. `t` should…** (1 connections) — `app/services/youtube_player.py`
- **10 minutes' → 600, '1 hour 5 min' → 3900, 'half a minute' → 30, '90 s' → 90.…** (1 connections) — `app/services/youtube_player.py`
- **5:30' → 330, '1:02:03' → 3723, 'to 5 30' → 330. None if absent.** (1 connections) — `app/services/youtube_player.py`
- **os-control.md** (1 connections) — `docs/features/os-control.md`
- **Files & symbols (auto-generated, line numbers are current)** (1 connections) — `docs/features/os-control.md`
- **Graphify** (1 connections) — `docs/features/os-control.md`
- **Purpose** (1 connections) — `docs/features/os-control.md`

## Relationships

- [youtube_control](youtube_control.md) (10 shared connections)
- [youtube_player](youtube_player.md) (6 shared connections)
- [chat + llm](chat_+_llm.md) (4 shared connections)
- [chat-routing + chat](chat-routing_+_chat.md) (3 shared connections)
- [chat + KNOWN_ISSUES](chat_+_KNOWN_ISSUES.md) (2 shared connections)
- [spotify_service + media_sessions](spotify_service_+_media_sessions.md) (2 shared connections)

## Source Files

- `app/services/youtube_control.py`
- `app/services/youtube_player.py`
- `docs/features/os-control.md`

## Audit Trail

- EXTRACTED: 41 (82%)
- INFERRED: 9 (18%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*