# agentic_web

> 22 nodes · cohesion 0.12

## Key Concepts

- **agentic_web.py** (14 connections) — `app/services/agentic_web.py`
- **agentic_web_action()** (8 connections) — `app/services/agentic_web.py`
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

- [jarvis_overlay + prompt_overlay](jarvis_overlay_+_prompt_overlay.md) (3 shared connections)
- [server + persistence](server_+_persistence.md) (2 shared connections)
- [assignment_assembler + smart_navigator](assignment_assembler_+_smart_navigator.md) (1 shared connections)
- [tool-registry + tools](tool-registry_+_tools.md) (1 shared connections)
- [web_search + tools](web_search_+_tools.md) (1 shared connections)
- [file_ops](file_ops.md) (1 shared connections)
- [tools + window_layout](tools_+_window_layout.md) (1 shared connections)

## Source Files

- `app/services/agentic_web.py`

## Audit Trail

- EXTRACTED: 33 (85%)
- INFERRED: 6 (15%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*