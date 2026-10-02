# web_search + tools

> 34 nodes · cohesion 0.09

## Key Concepts

- **web_search.py** (15 connections) — `app/services/web_search.py`
- **search_site()** (10 connections) — `app/services/web_search.py`
- **smart_search()** (10 connections) — `app/services/web_search.py`
- **research_scraper.py** (9 connections) — `app/services/research_scraper.py`
- **scrape_url()** (9 connections) — `app/services/web_search.py`
- **get_info()** (8 connections) — `app/services/tools.py`
- **urllib_parse** (8 connections)
- **_duckduckgo_search()** (6 connections) — `app/services/web_search.py`
- **requests** (6 connections)
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
- *... and 9 more nodes in this community*

## Relationships

- [tools](tools.md) (12 shared connections)
- [social_content_manager + ui_inspector](social_content_manager_+_ui_inspector.md) (4 shared connections)
- [research_scraper + nlp_extractor](research_scraper_+_nlp_extractor.md) (2 shared connections)
- [whatsapp_smart + tools](whatsapp_smart_+_tools.md) (2 shared connections)
- [browser_tool](browser_tool.md) (2 shared connections)
- [ppt_research](ppt_research.md) (2 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (1 shared connections)
- [message_reader + reply_generator](message_reader_+_reply_generator.md) (1 shared connections)
- [agentic_web](agentic_web.md) (1 shared connections)
- [content_humanizer + content-tools](content_humanizer_+_content-tools.md) (1 shared connections)
- [browser_mail](browser_mail.md) (1 shared connections)
- [spotify_service](spotify_service.md) (1 shared connections)

## Source Files

- `app/services/research_scraper.py`
- `app/services/tools.py`
- `app/services/web_search.py`
- `docs/features/web.md`

## Audit Trail

- EXTRACTED: 67 (84%)
- INFERRED: 13 (16%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*