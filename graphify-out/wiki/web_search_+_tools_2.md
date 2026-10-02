# web_search + tools

> 6 nodes · cohesion 0.33

## Key Concepts

- **scrape_url()** (9 connections) — `app/services/web_search.py`
- **scrape_url_tool()** (3 connections) — `app/services/tools.py`
- **_clean_html_text()** (3 connections) — `app/services/web_search.py`
- **Read and extract readable text content from a specific URL.** (1 connections) — `app/services/tools.py`
- **Parse HTML and extract readable text. Removes scripts, styles, navbars,…** (1 connections) — `app/services/web_search.py`
- **PUBLIC TOOL: Read and extract readable text from any URL. Called when user says…** (1 connections) — `app/services/web_search.py`

## Relationships

- [tools](tools.md) (4 shared connections)
- [web_search](web_search.md) (2 shared connections)
- [web_search + tools](web_search_+_tools.md) (1 shared connections)
- [tools + web](tools_+_web.md) (1 shared connections)

## Source Files

- `app/services/tools.py`
- `app/services/web_search.py`

## Audit Trail

- EXTRACTED: 9 (69%)
- INFERRED: 4 (31%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*