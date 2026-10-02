# agentic_web

> 18 nodes · cohesion 0.16

## Key Concepts

- **os** (50 connections)
- **agentic_web.py** (14 connections) — `app/services/agentic_web.py`
- **agentic_web_action()** (8 connections) — `app/services/agentic_web.py`
- **_run()** (8 connections) — `app/services/agentic_web.py`
- **test_agentic_web.py** (4 connections) — `test_agentic_web.py`
- **_build_search_queries()** (3 connections) — `app/services/agentic_web.py`
- **_resolve_listing_urls()** (3 connections) — `app/services/agentic_web.py`
- **_search_web()** (3 connections) — `app/services/agentic_web.py`
- **_synthesize()** (3 connections) — `app/services/agentic_web.py`
- **_worker()** (2 connections) — `app/services/agentic_web.py`
- **_get_api_key()** (2 connections) — `app/services/agentic_web.py`
- **fetch_one()** (2 connections) — `app/services/agentic_web.py`
- **agentic_web.py — Smart Web Research Engine for Jarvis…** (1 connections) — `app/services/agentic_web.py`
- **Use the LLM to extract specific listings from the fetched content.** (1 connections) — `app/services/agentic_web.py`
- **Generator that streams progress and final answer.** (1 connections) — `app/services/agentic_web.py`
- **Return known direct listing URLs for a site+task combo.** (1 connections) — `app/services/agentic_web.py`
- **Build 2-3 specific search queries that will hit listing pages, not homepages.** (1 connections) — `app/services/agentic_web.py`
- **Run a DuckDuckGo search, return list of {title, href, body}.** (1 connections) — `app/services/agentic_web.py`

## Relationships

- [rag_memory + memory](rag_memory_+_memory.md) (3 shared connections)
- [benchmark](benchmark.md) (2 shared connections)
- [agentic_web](agentic_web.md) (2 shared connections)
- [tools](tools.md) (2 shared connections)
- [dag_executor + planner](dag_executor_+_planner.md) (2 shared connections)
- [browser_tool + smart_navigator](browser_tool_+_smart_navigator.md) (2 shared connections)
- [dark_enhancement + dark_video_enhancement](dark_enhancement_+_dark_video_enhancement.md) (2 shared connections)
- [task_ledger + test_task_resumption](task_ledger_+_test_task_resumption.md) (2 shared connections)
- [whatsapp + dump_wa_ui](whatsapp_+_dump_wa_ui.md) (2 shared connections)
- [ssml_processor + debug_wa](ssml_processor_+_debug_wa.md) (1 shared connections)
- [server + test_concurrency](server_+_test_concurrency.md) (1 shared connections)
- [tool-registry](tool-registry.md) (1 shared connections)

## Source Files

- `app/services/agentic_web.py`
- `test_agentic_web.py`

## Audit Trail

- EXTRACTED: 77 (93%)
- INFERRED: 6 (7%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*