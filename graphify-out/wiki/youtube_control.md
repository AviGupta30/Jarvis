# youtube_control

> 18 nodes · cohesion 0.12

## Key Concepts

- **Open** (9 connections) — `docs/KNOWN_ISSUES.md`
- **page_videos()** (8 connections) — `app/services/youtube_player.py`
- **_fetch_results()** (7 connections) — `app/services/youtube_control.py`
- **_parse_videos()** (7 connections) — `app/services/youtube_control.py`
- **_find_channel_at()** (5 connections) — `app/services/youtube_control.py`
- **_screen_results()** (5 connections) — `app/services/youtube_control.py`
- **_initial_data()** (4 connections) — `app/services/youtube_control.py`
- **add()** (4 connections) — `app/services/youtube_control.py`
- **walk()** (4 connections) — `app/services/youtube_control.py`
- **_dur_to_sec()** (3 connections) — `app/services/youtube_control.py`
- **walk()** (3 connections) — `app/services/youtube_control.py`
- **_views()** (3 connections) — `app/services/youtube_control.py`
- **sim()** (1 connections) — `app/services/youtube_control.py`
- **Collect videos from ytInitialData: classic videoRenderer (search) and the newer…** (1 connections) — `app/services/youtube_control.py`
- **Scrape YouTube's results page → [{id,title,channel,duration,seconds,views}]; []…** (1 connections) — `app/services/youtube_control.py`
- **Replace the session's result list with the videos actually on screen in the…** (1 connections) — `app/services/youtube_control.py`
- **1,234,567 views' / '82 million views' / '1.2M' → int.** (1 connections) — `app/services/youtube_control.py`
- **Read the videos actually shown in the front YouTube tab (what the user sees,…** (1 connections) — `app/services/youtube_player.py`

## Relationships

- [youtube_control + youtube_player](youtube_control_+_youtube_player.md) (16 shared connections)
- [youtube_player](youtube_player.md) (4 shared connections)
- [ppt_content](ppt_content.md) (2 shared connections)
- [uia_local + youtube_player](uia_local_+_youtube_player.md) (1 shared connections)
- [chat + rag_memory](chat_+_rag_memory.md) (1 shared connections)
- [voice](voice.md) (1 shared connections)
- [calendar_tool](calendar_tool.md) (1 shared connections)

## Source Files

- `app/services/youtube_control.py`
- `app/services/youtube_player.py`
- `docs/KNOWN_ISSUES.md`

## Audit Trail

- EXTRACTED: 36 (77%)
- INFERRED: 11 (23%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*