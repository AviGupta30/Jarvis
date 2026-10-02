# nlp_extractor + research_pipeline

> 9 nodes · cohesion 0.25

## Key Concepts

- **NLPExtractor** (6 connections) — `app/services/nlp_extractor.py`
- **research_topic()** (6 connections) — `app/services/research_pipeline.py`
- **_research_and_create_ppt()** (4 connections) — `app/services/tools.py`
- **.extract_facts()** (3 connections) — `app/services/nlp_extractor.py`
- **._parse()** (2 connections) — `app/services/nlp_extractor.py`
- **.__init__()** (1 connections) — `app/services/nlp_extractor.py`
- **Runs extraction on each scraped source and aggregates the results. Returns a…** (1 connections) — `app/services/nlp_extractor.py`
- **Scrapes the web for a topic and extracts verified facts and statistics. Yields…** (1 connections) — `app/services/research_pipeline.py`
- **Phase 3: Autonomous Research Aggregator. Scrapes live facts from the web,…** (1 connections) — `app/services/tools.py`

## Relationships

- [assignment_tool + safe_executor](assignment_tool_+_safe_executor.md) (3 shared connections)
- [tools](tools.md) (2 shared connections)
- [research_scraper](research_scraper.md) (1 shared connections)
- [ppt_tool + ppt_image_engine](ppt_tool_+_ppt_image_engine.md) (1 shared connections)

## Source Files

- `app/services/nlp_extractor.py`
- `app/services/research_pipeline.py`
- `app/services/tools.py`

## Audit Trail

- EXTRACTED: 15 (94%)
- INFERRED: 1 (6%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*