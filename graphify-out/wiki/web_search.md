# web_search

> 17 nodes · cohesion 0.18

## Key Concepts

- **web_search.py** (15 connections) — `app/services/web_search.py`
- **smart_search()** (10 connections) — `app/services/web_search.py`
- **research_scraper.py** (9 connections) — `app/services/research_scraper.py`
- **urllib_parse** (8 connections)
- **_duckduckgo_search()** (6 connections) — `app/services/web_search.py`
- **requests** (6 connections)
- **_format_ddg_results()** (4 connections) — `app/services/web_search.py`
- **_synthesize_with_llm()** (3 connections) — `app/services/web_search.py`
- **_wikipedia_search()** (3 connections) — `app/services/web_search.py`
- **bs4** (2 connections)
- **research_scraper.py — Autonomous Web Research Scraper…** (1 connections) — `app/services/research_scraper.py`
- **web_search.py — Jarvis Reliable Web Search (Step 3)…** (1 connections) — `app/services/web_search.py`
- **PRIMARY PUBLIC FUNCTION — used by get_info() in tools.py. Enhanced with: -…** (1 connections) — `app/services/web_search.py`
- **Use a fast LLM call to synthesize multiple search sources into a single…** (1 connections) — `app/services/web_search.py`
- **Search DuckDuckGo using direct HTML scraping (faster, no brittle dependencies).…** (1 connections) — `app/services/web_search.py`
- **Convert DDG result list into a clean readable string for the LLM.** (1 connections) — `app/services/web_search.py`
- **Query the Wikipedia API for clean, factual information. Returns the first 3…** (1 connections) — `app/services/web_search.py`

## Relationships

- [web_search + web](web_search_+_web.md) (6 shared connections)
- [tools](tools.md) (3 shared connections)
- [research_scraper](research_scraper.md) (2 shared connections)
- [benchmark + server](benchmark_+_server.md) (2 shared connections)
- [ppt_research](ppt_research.md) (2 shared connections)
- [nlp_extractor + download_kokoro](nlp_extractor_+_download_kokoro.md) (1 shared connections)
- [chat + llm](chat_+_llm.md) (1 shared connections)
- [assignment_assembler + smart_navigator](assignment_assembler_+_smart_navigator.md) (1 shared connections)
- [browser_tool](browser_tool.md) (1 shared connections)
- [content_humanizer](content_humanizer.md) (1 shared connections)
- [social_content_manager + tools](social_content_manager_+_tools.md) (1 shared connections)
- [browser_mail](browser_mail.md) (1 shared connections)

## Source Files

- `app/services/research_scraper.py`
- `app/services/web_search.py`

## Audit Trail

- EXTRACTED: 48 (98%)
- INFERRED: 1 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*