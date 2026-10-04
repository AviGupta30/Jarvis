# youtube_player

> 14 nodes · cohesion 0.19

## Key Concepts

- **player_action()** (21 connections) — `app/services/youtube_player.py`
- **send_keys()** (11 connections) — `app/services/youtube_player.py`
- **_fallback()** (7 connections) — `app/services/youtube_player.py`
- **current_video_info()** (6 connections) — `app/services/youtube_player.py`
- **_js()** (5 connections) — `app/services/youtube_player.py`
- **fmt_span()** (4 connections) — `app/services/youtube_player.py`
- **fmt_time()** (3 connections) — `app/services/youtube_player.py`
- **_pos()** (3 connections) — `app/services/youtube_player.py`
- **_rate()** (3 connections) — `app/services/youtube_player.py`
- **Focus the YouTube tab and send shortcut keys. Returns an error string or None.** (1 connections) — `app/services/youtube_player.py`
- **10 → '10 seconds', 600 → '10 minutes', 90 → '1 minute 30 seconds'.** (1 connections) — `app/services/youtube_player.py`
- **Keyboard-only version of an action. Only used for Firefox (which blocks the…** (1 connections) — `app/services/youtube_player.py`
- **{title, author, t, d, ...} of the video in the front YouTube tab, or None.** (1 connections) — `app/services/youtube_player.py`
- **Precise YouTube player control. Returns a human-readable reply. action / amount…** (1 connections) — `app/services/youtube_player.py`

## Relationships

- [youtube_player](youtube_player.md) (16 shared connections)
- [youtube_control](youtube_control.md) (9 shared connections)
- [tools](tools.md) (4 shared connections)
- [youtube_control + os-control](youtube_control_+_os-control.md) (1 shared connections)
- [spotify_service + media_sessions](spotify_service_+_media_sessions.md) (1 shared connections)
- [tool-registry + vector_store](tool-registry_+_vector_store.md) (1 shared connections)

## Source Files

- `app/services/youtube_player.py`

## Audit Trail

- EXTRACTED: 45 (90%)
- INFERRED: 5 (10%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*