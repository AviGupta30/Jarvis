# research_scraper

> 7 nodes · cohesion 0.38

## Key Concepts

- **ResearchScraper** (8 connections) — `app/services/research_scraper.py`
- **.scrape_topic()** (4 connections) — `app/services/research_scraper.py`
- **._clean_text()** (2 connections) — `app/services/research_scraper.py`
- **._fetch_page()** (2 connections) — `app/services/research_scraper.py`
- **._is_allowed()** (2 connections) — `app/services/research_scraper.py`
- **Searches DDG for the topic, fetches the top N links concurrently, and returns…** (1 connections) — `app/services/research_scraper.py`
- **.__init__()** (1 connections) — `app/services/research_scraper.py`

## Relationships

- [web_search](web_search.md) (2 shared connections)
- [nlp_extractor + research_pipeline](nlp_extractor_+_research_pipeline.md) (1 shared connections)
- [assignment_tool + safe_executor](assignment_tool_+_safe_executor.md) (1 shared connections)

## Source Files

- `app/services/research_scraper.py`

## Audit Trail

- EXTRACTED: 12 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*