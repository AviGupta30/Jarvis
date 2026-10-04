# youtube_control

> 11 nodes · cohesion 0.20

## Key Concepts

- **page_videos()** (8 connections) — `app/services/youtube_player.py`
- **_parse_videos()** (7 connections) — `app/services/youtube_control.py`
- **_screen_results()** (5 connections) — `app/services/youtube_control.py`
- **add()** (4 connections) — `app/services/youtube_control.py`
- **walk()** (4 connections) — `app/services/youtube_control.py`
- **_dur_to_sec()** (3 connections) — `app/services/youtube_control.py`
- **_views()** (3 connections) — `app/services/youtube_control.py`
- **Collect videos from ytInitialData: classic videoRenderer (search) and the newer…** (1 connections) — `app/services/youtube_control.py`
- **Replace the session's result list with the videos actually on screen in the…** (1 connections) — `app/services/youtube_control.py`
- **1,234,567 views' / '82 million views' / '1.2M' → int.** (1 connections) — `app/services/youtube_control.py`
- **Read the videos actually shown in the front YouTube tab (what the user sees,…** (1 connections) — `app/services/youtube_player.py`

## Relationships

- [youtube_control](youtube_control.md) (8 shared connections)
- [youtube_player](youtube_player.md) (3 shared connections)
- [tools](tools.md) (2 shared connections)
- [chat + llm](chat_+_llm.md) (1 shared connections)

## Source Files

- `app/services/youtube_control.py`
- `app/services/youtube_player.py`

## Audit Trail

- EXTRACTED: 23 (88%)
- INFERRED: 3 (12%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*