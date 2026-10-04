# research_scraper + nlp_extractor

> 16 nodes · cohesion 0.15

## Key Concepts

- **ResearchScraper** (8 connections) — `app/services/research_scraper.py`
- **NLPExtractor** (6 connections) — `app/services/nlp_extractor.py`
- **research_topic()** (6 connections) — `app/services/research_pipeline.py`
- **.scrape_topic()** (4 connections) — `app/services/research_scraper.py`
- **_research_and_create_ppt()** (4 connections) — `app/services/tools.py`
- **.extract_facts()** (3 connections) — `app/services/nlp_extractor.py`
- **._parse()** (2 connections) — `app/services/nlp_extractor.py`
- **._clean_text()** (2 connections) — `app/services/research_scraper.py`
- **._fetch_page()** (2 connections) — `app/services/research_scraper.py`
- **._is_allowed()** (2 connections) — `app/services/research_scraper.py`
- **.__init__()** (1 connections) — `app/services/nlp_extractor.py`
- **Runs extraction on each scraped source and aggregates the results. Returns a…** (1 connections) — `app/services/nlp_extractor.py`
- **Scrapes the web for a topic and extracts verified facts and statistics. Yields…** (1 connections) — `app/services/research_pipeline.py`
- **Searches DDG for the topic, fetches the top N links concurrently, and returns…** (1 connections) — `app/services/research_scraper.py`
- **.__init__()** (1 connections) — `app/services/research_scraper.py`
- **Phase 3: Autonomous Research Aggregator. Scrapes live facts from the web,…** (1 connections) — `app/services/tools.py`

## Relationships

- [voice_agent + download_kokoro](voice_agent_+_download_kokoro.md) (4 shared connections)
- [tools](tools.md) (2 shared connections)
- [web_search + tools](web_search_+_tools.md) (2 shared connections)
- [ppt_router + ppt_tool](ppt_router_+_ppt_tool.md) (1 shared connections)

## Source Files

- `app/services/nlp_extractor.py`
- `app/services/research_pipeline.py`
- `app/services/research_scraper.py`
- `app/services/tools.py`

## Audit Trail

- EXTRACTED: 26 (96%)
- INFERRED: 1 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*