# web_search + tools

> 6 nodes · cohesion 0.33

## Key Concepts

- **search_site()** (10 connections) — `app/services/web_search.py`
- **_format_ddg_results()** (4 connections) — `app/services/web_search.py`
- **search_site_tool()** (3 connections) — `app/services/tools.py`
- **Search for a query within a specific website using DuckDuckGo site: operator.** (1 connections) — `app/services/tools.py`
- **PUBLIC TOOL: Search for a query within a specific website. Uses DuckDuckGo with…** (1 connections) — `app/services/web_search.py`
- **Convert DDG result list into a clean readable string for the LLM.** (1 connections) — `app/services/web_search.py`

## Relationships

- [web_search](web_search.md) (5 shared connections)
- [tools](tools.md) (3 shared connections)
- [web_search + tools](web_search_+_tools.md) (1 shared connections)
- [tools + web](tools_+_web.md) (1 shared connections)

## Source Files

- `app/services/tools.py`
- `app/services/web_search.py`

## Audit Trail

- EXTRACTED: 12 (80%)
- INFERRED: 3 (20%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*