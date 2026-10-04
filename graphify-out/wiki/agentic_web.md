# agentic_web

> 22 nodes · cohesion 0.12

## Key Concepts

- **agentic_web.py** (14 connections) — `app/services/agentic_web.py`
- **agentic_web_action()** (9 connections) — `app/services/agentic_web.py`
- **_run()** (8 connections) — `app/services/agentic_web.py`
- **_fetch_page_text()** (7 connections) — `app/services/agentic_web.py`
- **_build_search_queries()** (3 connections) — `app/services/agentic_web.py`
- **__init__()** (3 connections) — `app/services/agentic_web.py`
- **_resolve_listing_urls()** (3 connections) — `app/services/agentic_web.py`
- **_search_web()** (3 connections) — `app/services/agentic_web.py`
- **_synthesize()** (3 connections) — `app/services/agentic_web.py`
- **_worker()** (2 connections) — `app/services/agentic_web.py`
- **_get_api_key()** (2 connections) — `app/services/agentic_web.py`
- **fetch_one()** (2 connections) — `app/services/agentic_web.py`
- **handle_data()** (1 connections) — `app/services/agentic_web.py`
- **handle_endtag()** (1 connections) — `app/services/agentic_web.py`
- **handle_starttag()** (1 connections) — `app/services/agentic_web.py`
- **agentic_web.py — Smart Web Research Engine for Jarvis…** (1 connections) — `app/services/agentic_web.py`
- **Download a page and return clean readable text (no HTML tags).** (1 connections) — `app/services/agentic_web.py`
- **Use the LLM to extract specific listings from the fetched content.** (1 connections) — `app/services/agentic_web.py`
- **Generator that streams progress and final answer.** (1 connections) — `app/services/agentic_web.py`
- **Return known direct listing URLs for a site+task combo.** (1 connections) — `app/services/agentic_web.py`
- **Build 2-3 specific search queries that will hit listing pages, not homepages.** (1 connections) — `app/services/agentic_web.py`
- **Run a DuckDuckGo search, return list of {title, href, body}.** (1 connections) — `app/services/agentic_web.py`

## Relationships

- [benchmark + download_kokoro](benchmark_+_download_kokoro.md) (3 shared connections)
- [server + persistence](server_+_persistence.md) (2 shared connections)
- [tool-registry + vector_store](tool-registry_+_vector_store.md) (2 shared connections)
- [assignment_assembler + smart_navigator](assignment_assembler_+_smart_navigator.md) (1 shared connections)
- [modes](modes.md) (1 shared connections)
- [web_search + tools](web_search_+_tools.md) (1 shared connections)
- [tools](tools.md) (1 shared connections)

## Source Files

- `app/services/agentic_web.py`

## Audit Trail

- EXTRACTED: 33 (82%)
- INFERRED: 7 (18%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*