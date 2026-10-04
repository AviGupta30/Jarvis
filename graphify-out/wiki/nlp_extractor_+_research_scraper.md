# nlp_extractor + research_scraper

> 21 nodes · cohesion 0.12

## Key Concepts

- **nlp_extractor.py** (8 connections) — `app/services/nlp_extractor.py`
- **ResearchScraper** (8 connections) — `app/services/research_scraper.py`
- **research_pipeline.py** (7 connections) — `app/services/research_pipeline.py`
- **NLPExtractor** (6 connections) — `app/services/nlp_extractor.py`
- **research_topic()** (6 connections) — `app/services/research_pipeline.py`
- **.scrape_topic()** (4 connections) — `app/services/research_scraper.py`
- **_research_and_create_ppt()** (4 connections) — `app/services/tools.py`
- **.extract_facts()** (3 connections) — `app/services/nlp_extractor.py`
- **dotenv** (3 connections)
- **._parse()** (2 connections) — `app/services/nlp_extractor.py`
- **._clean_text()** (2 connections) — `app/services/research_scraper.py`
- **._fetch_page()** (2 connections) — `app/services/research_scraper.py`
- **._is_allowed()** (2 connections) — `app/services/research_scraper.py`
- **.__init__()** (1 connections) — `app/services/nlp_extractor.py`
- **nlp_extractor.py — LLM-Powered Fact & Entity Extractor…** (1 connections) — `app/services/nlp_extractor.py`
- **Runs extraction on each scraped source and aggregates the results. Returns a…** (1 connections) — `app/services/nlp_extractor.py`
- **research_pipeline.py — End-to-End Autonomous Research Orchestrator…** (1 connections) — `app/services/research_pipeline.py`
- **Scrapes the web for a topic and extracts verified facts and statistics. Yields…** (1 connections) — `app/services/research_pipeline.py`
- **Searches DDG for the topic, fetches the top N links concurrently, and returns…** (1 connections) — `app/services/research_scraper.py`
- **.__init__()** (1 connections) — `app/services/research_scraper.py`
- **Phase 3: Autonomous Research Aggregator. Scrapes live facts from the web,…** (1 connections) — `app/services/tools.py`

## Relationships

- [web_search + tools](web_search_+_tools.md) (3 shared connections)
- [assignment_humanizer + task_ledger](assignment_humanizer_+_task_ledger.md) (2 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (2 shared connections)
- [tools](tools.md) (2 shared connections)
- [social_content_manager + content-tools](social_content_manager_+_content-tools.md) (1 shared connections)
- [smart_navigator + ssml_processor](smart_navigator_+_ssml_processor.md) (1 shared connections)
- [ppt_router + ppt_tool](ppt_router_+_ppt_tool.md) (1 shared connections)
- [prompt_enhancer_button](prompt_enhancer_button.md) (1 shared connections)

## Source Files

- `app/services/nlp_extractor.py`
- `app/services/research_pipeline.py`
- `app/services/research_scraper.py`
- `app/services/tools.py`

## Audit Trail

- EXTRACTED: 38 (97%)
- INFERRED: 1 (3%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*