# web_search + tools

> 33 nodes · cohesion 0.09

## Key Concepts

- **web_search.py** (15 connections) — `app/services/web_search.py`
- **search_site()** (10 connections) — `app/services/web_search.py`
- **smart_search()** (10 connections) — `app/services/web_search.py`
- **research_scraper.py** (9 connections) — `app/services/research_scraper.py`
- **scrape_url()** (9 connections) — `app/services/web_search.py`
- **get_info()** (8 connections) — `app/services/tools.py`
- **urllib_parse** (8 connections)
- **_duckduckgo_search()** (6 connections) — `app/services/web_search.py`
- **Triggers** (5 connections) — `docs/features/web.md`
- **_format_ddg_results()** (4 connections) — `app/services/web_search.py`
- **_extract_location()** (3 connections) — `app/services/tools.py`
- **get_weather()** (3 connections) — `app/services/tools.py`
- **scrape_url_tool()** (3 connections) — `app/services/tools.py`
- **search_site_tool()** (3 connections) — `app/services/tools.py`
- **_clean_html_text()** (3 connections) — `app/services/web_search.py`
- **_synthesize_with_llm()** (3 connections) — `app/services/web_search.py`
- **_wikipedia_search()** (3 connections) — `app/services/web_search.py`
- **bs4** (2 connections)
- **research_scraper.py — Autonomous Web Research Scraper…** (1 connections) — `app/services/research_scraper.py`
- **Pulls a clean location name out of a weather query.** (1 connections) — `app/services/tools.py`
- **Get current weather using wttr.in — returns a clean spoken string.** (1 connections) — `app/services/tools.py`
- **Search for a query within a specific website using DuckDuckGo site: operator.** (1 connections) — `app/services/tools.py`
- **Read and extract readable text content from a specific URL.** (1 connections) — `app/services/tools.py`
- **Smart information lookup (Step 3 upgrade): - Weather queries -> wttr.in (real-…** (1 connections) — `app/services/tools.py`
- **web_search.py — Jarvis Reliable Web Search (Step 3)…** (1 connections) — `app/services/web_search.py`
- *... and 8 more nodes in this community*

## Relationships

- [tools](tools.md) (14 shared connections)
- [voice_agent + download_kokoro](voice_agent_+_download_kokoro.md) (4 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (2 shared connections)
- [research_scraper + nlp_extractor](research_scraper_+_nlp_extractor.md) (2 shared connections)
- [browser_tool](browser_tool.md) (2 shared connections)
- [message_reader + thread_extractor](message_reader_+_thread_extractor.md) (1 shared connections)
- [browser_mail](browser_mail.md) (1 shared connections)
- [spotify_service + media_sessions](spotify_service_+_media_sessions.md) (1 shared connections)
- [youtube_control](youtube_control.md) (1 shared connections)
- [ppt_research](ppt_research.md) (1 shared connections)
- [prompt_enhancer_button](prompt_enhancer_button.md) (1 shared connections)

## Source Files

- `app/services/research_scraper.py`
- `app/services/tools.py`
- `app/services/web_search.py`
- `docs/features/web.md`

## Audit Trail

- EXTRACTED: 63 (83%)
- INFERRED: 13 (17%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*