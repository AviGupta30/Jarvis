# agentic_web

> 24 nodes · cohesion 0.11

## Key Concepts

- **Fixed on 2026-09-28** (16 connections) — `docs/KNOWN_ISSUES.md`
- **agentic_web.py** (14 connections) — `app/services/agentic_web.py`
- **agentic_web_action()** (8 connections) — `app/services/agentic_web.py`
- **_run()** (8 connections) — `app/services/agentic_web.py`
- **_fetch_page_text()** (7 connections) — `app/services/agentic_web.py`
- **test_agentic_web.py** (4 connections) — `test_agentic_web.py`
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

- [social_content_manager + ui_inspector](social_content_manager_+_ui_inspector.md) (3 shared connections)
- [server + protocol](server_+_protocol.md) (3 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (3 shared connections)
- [email-calendar + tools](email-calendar_+_tools.md) (2 shared connections)
- [web_search + tools](web_search_+_tools.md) (1 shared connections)
- [tools](tools.md) (1 shared connections)
- [ppt + KNOWN_ISSUES](ppt_+_KNOWN_ISSUES.md) (1 shared connections)
- [media_state + youtube_control](media_state_+_youtube_control.md) (1 shared connections)
- [file_ops](file_ops.md) (1 shared connections)
- [assignment + assignment_answers](assignment_+_assignment_answers.md) (1 shared connections)
- [vector_store + database](vector_store_+_database.md) (1 shared connections)
- [ppt_router + ppt_tool](ppt_router_+_ppt_tool.md) (1 shared connections)

## Source Files

- `app/services/agentic_web.py`
- `docs/KNOWN_ISSUES.md`
- `test_agentic_web.py`

## Audit Trail

- EXTRACTED: 36 (64%)
- INFERRED: 20 (36%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*