# youtube_player

> 7 nodes · cohesion 0.33

## Key Concepts

- **parse_player_command()** (8 connections) — `app/services/youtube_player.py`
- **parse_duration()** (4 connections) — `app/services/youtube_player.py`
- **_num()** (3 connections) — `app/services/youtube_player.py`
- **parse_clock()** (3 connections) — `app/services/youtube_player.py`
- **Map a spoken player command to (action, amount, value), or None. `t` should…** (1 connections) — `app/services/youtube_player.py`
- **10 minutes' → 600, '1 hour 5 min' → 3900, 'half a minute' → 30, '90 s' → 90.…** (1 connections) — `app/services/youtube_player.py`
- **5:30' → 330, '1:02:03' → 3723, 'to 5 30' → 330. None if absent.** (1 connections) — `app/services/youtube_player.py`

## Relationships

- [youtube_player](youtube_player.md) (4 shared connections)
- [youtube_control + os-control](youtube_control_+_os-control.md) (1 shared connections)
- [youtube_control](youtube_control.md) (1 shared connections)
- [tools](tools.md) (1 shared connections)

## Source Files

- `app/services/youtube_player.py`

## Audit Trail

- EXTRACTED: 13 (93%)
- INFERRED: 1 (7%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*