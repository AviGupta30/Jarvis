# youtube_control + youtube_player

> 11 nodes · cohesion 0.20

## Key Concepts

- **Open** (9 connections) — `docs/KNOWN_ISSUES.md`
- **page_videos()** (8 connections) — `app/services/youtube_player.py`
- **_fetch_results()** (7 connections) — `app/services/youtube_control.py`
- **_parse_videos()** (7 connections) — `app/services/youtube_control.py`
- **add()** (4 connections) — `app/services/youtube_control.py`
- **walk()** (4 connections) — `app/services/youtube_control.py`
- **_views()** (3 connections) — `app/services/youtube_control.py`
- **Collect videos from ytInitialData: classic videoRenderer (search) and the newer…** (1 connections) — `app/services/youtube_control.py`
- **Scrape YouTube's results page → [{id,title,channel,duration,seconds,views}]; []…** (1 connections) — `app/services/youtube_control.py`
- **1,234,567 views' / '82 million views' / '1.2M' → int.** (1 connections) — `app/services/youtube_control.py`
- **Read the videos actually shown in the front YouTube tab (what the user sees,…** (1 connections) — `app/services/youtube_player.py`

## Relationships

- [youtube_control](youtube_control.md) (9 shared connections)
- [youtube_player](youtube_player.md) (8 shared connections)
- [ppt + KNOWN_ISSUES](ppt_+_KNOWN_ISSUES.md) (1 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (1 shared connections)
- [voice](voice.md) (1 shared connections)
- [ppt_content](ppt_content.md) (1 shared connections)
- [memory_tool + calendar_tool](memory_tool_+_calendar_tool.md) (1 shared connections)

## Source Files

- `app/services/youtube_control.py`
- `app/services/youtube_player.py`
- `docs/KNOWN_ISSUES.md`

## Audit Trail

- EXTRACTED: 23 (68%)
- INFERRED: 11 (32%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*