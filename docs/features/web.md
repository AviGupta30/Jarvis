# Web search, research & browser automation

## Purpose
Live information and browsing.

| Tool | Module | Behaviour |
|---|---|---|
| `get_info(query)` | tools.py → `web_search.smart_search` | weather via wttr.in; DDG HTML + Wikipedia → LLM synthesis |
| `search_site(query, site_url)` / `scrape_url(url)` | web_search | DDG `site:` search / requests+BS4 text extraction |
| `agentic_web_action(site_or_task, specific_task)` | agentic_web | generator: known listing URLs + DDG queries → parallel fetch → LLM extracts listings (hackathons, internships…) |
| `browse_and_read`, `search_on_site`, `click_element`, `scroll_and_read`, `fill_form`, `browse_and_paginate` | browser_tool | Playwright anti-bot Chromium + LLM extraction |
| `smart_web_action(site_name, task)` | registry maps to agentic_web (smart_navigator is legacy, visible browser) | |

## Triggers
chat.py: weather/news/sports/finance keywords → `get_info`; "go to <site> and find…", "find X on <site>", "find me / latest / hackathons…" → `agentic_web_action`; "search X on <site>" → `search_site`; URL + "read this page" → `scrape_url`.

## Gotchas
- The sports keyword appends " 2025" to the query (hardcoded year in chat.py).
- DDG HTML scraping breaks when their markup changes.

## Graphify
`graphify explain "smart_search"` · `graphify explain "agentic_web_action"`

<!-- AUTO:BEGIN (scripts/refresh_docs.py) -->
## Files & symbols (auto-generated, line numbers are current)

- `app/services/web_search.py` (347 lines): web_search.py — Jarvis Reliable Web Search (Step 3)
  L27 _HEADERS · L36 _TIMEOUT · L37 _MAX_RESULT_CHARS · L40 _WIKI_KEYWORDS · L49 _duckduckgo_search() · L82 _format_ddg_results() · L98 _wikipedia_search() · L149 _clean_html_text() · L185 scrape_url() · L211 search_site() · L252 smart_search() · L324 _synthesize_with_llm()
- `app/services/agentic_web.py` (324 lines): agentic_web.py — Smart Web Research Engine for Jarvis
  L20 SITE_LISTING_URLS · L45 _get_api_key() · L56 _resolve_listing_urls() · L72 _build_search_queries() · L94 _search_web() · L104 _fetch_page_text() · L155 _synthesize() · L205 agentic_web_action() · L227 _run()
- `app/services/browser_tool.py` (264 lines): browser_tool.py — Jarvis Browser Automation (Step 6 — ENHANCED)
  L23 _REALISTIC_UA · L29 _clean_text() · L36 _ensure_url() · L42 _new_browser_page() · L62 _llm_extract() · L84 browse_and_read() · L102 search_on_site() · L145 click_element() · L168 scroll_and_read() · L185 fill_form() · L234 browse_and_paginate()
- `app/services/smart_navigator.py` (195 lines): smart_navigator.py — Isolated Smart Web Navigator for Jarvis
  L22 _get_api_key() · L35 _llm_extract() · L60 _resolve_url() · L78 smart_web_action()
- `app/services/tools.py` (1217 lines): Jarvis Tool Registry — All callable actions Jarvis can perform.  *(filtered to this feature)*
  L48 _extract_location() · L57 get_weather() · L87 get_info() · L182 open_google_search_in_browser() · L784 search_site_tool() · L792 scrape_url_tool()
<!-- AUTO:END -->
