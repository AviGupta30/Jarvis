"""
web_search.py — Jarvis Reliable Web Search (Step 3)
----------------------------------------------------
Completely isolated module. Nothing in existing Jarvis code depends on this
until tools.py explicitly imports it. Safe to develop and test independently.

STRATEGY (in priority order):
  1. DuckDuckGo text search  — free, no API key, rarely rate-limited
  2. Wikipedia API           — clean structured text for factual/definition queries
  3. Direct URL scraping     — requests + BeautifulSoup for specific pages
  4. Graceful fallback       — always returns something meaningful, never crashes

Public API:
  smart_search(query, site=None)    → str   general search, optional site filter
  scrape_url(url)                   → str   read and clean a specific URL
  search_site(query, site_url)      → str   search within a specific website
"""

import re
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode, urlparse, quote_plus

# ── Constants ─────────────────────────────────────────────────────────────────

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}
_TIMEOUT = 6          # seconds per HTTP request
_MAX_RESULT_CHARS = 2500   # cap result length for LLM consumption

# Wikipedia topics (expand results for these)
_WIKI_KEYWORDS = [
    "who is", "what is", "define", "definition of", "meaning of",
    "history of", "biography", "wikipedia", "explain", "about ",
    "inventor of", "founded by", "when was", "where is",
]


# ── Layer 1: DuckDuckGo Text Search ──────────────────────────────────────────

def _duckduckgo_search(query: str) -> list[dict]:
    """
    Search DuckDuckGo using direct HTML scraping (faster, no brittle dependencies).
    Returns a list of {title, body, href} dicts.
    Falls back to empty list on any failure.
    """
    try:
        url = "https://html.duckduckgo.com/html/"
        data = {"q": query}
        headers = _HEADERS.copy()
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        
        resp = requests.post(url, data=data, headers=headers, timeout=_TIMEOUT)
        resp.raise_for_status()
        
        soup = BeautifulSoup(resp.text, "html.parser")
        results = []
        for result in soup.find_all("div", class_="result"):
            title_tag = result.find("a", class_="result__a")
            snippet_tag = result.find("a", class_="result__snippet")
            if title_tag and snippet_tag:
                results.append({
                    "title": title_tag.get_text(strip=True),
                    "body": snippet_tag.get_text(strip=True),
                    "href": title_tag.get("href", "")
                })
            if len(results) >= 5:
                break
        return results
    except Exception as e:
        return []


def _format_ddg_results(results: list[dict], max_chars: int = _MAX_RESULT_CHARS) -> str:
    """
    Convert DDG result list into a clean readable string for the LLM.
    """
    parts = []
    for r in results[:4]:
        title = r.get("title", "").strip()
        body = r.get("body", "").strip()
        if body:
            parts.append(f"• {title}: {body}")
    combined = "\n".join(parts)
    return combined[:max_chars] if combined else ""


# ── Layer 2: Wikipedia API ─────────────────────────────────────────────────

def _wikipedia_search(query: str) -> str:
    """
    Query the Wikipedia API for clean, factual information.
    Returns the first 3 paragraphs of the best matching article.
    Returns empty string on failure.
    """
    try:
        # Step 1: search for the best matching page title
        search_url = "https://en.wikipedia.org/w/api.php"
        search_params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
            "srlimit": 1,
        }
        resp = requests.get(search_url, params=search_params,
                            headers=_HEADERS, timeout=_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        search_hits = data.get("query", {}).get("search", [])
        if not search_hits:
            return ""
        page_title = search_hits[0]["title"]

        # Step 2: get the intro extract of that page
        extract_params = {
            "action": "query",
            "prop": "extracts",
            "exintro": True,
            "explaintext": True,
            "titles": page_title,
            "format": "json",
            "redirects": 1,
        }
        resp2 = requests.get(search_url, params=extract_params,
                             headers=_HEADERS, timeout=_TIMEOUT)
        resp2.raise_for_status()
        pages = resp2.json().get("query", {}).get("pages", {})
        for page in pages.values():
            extract = page.get("extract", "").strip()
            if extract and len(extract) > 50:
                # Return first 2000 chars (enough for a good summary)
                return f"[Wikipedia — {page_title}]\n{extract[:2000]}"
        return ""
    except Exception:
        return ""


# ── Layer 3: Direct URL Scraping ─────────────────────────────────────────────

def _clean_html_text(html: str, max_chars: int = _MAX_RESULT_CHARS) -> str:
    """
    Parse HTML and extract readable text. Removes scripts, styles, navbars, footers.
    Returns clean paragraph text capped at max_chars.
    """
    soup = BeautifulSoup(html, "html.parser")

    # Remove noise elements
    for tag in soup(["script", "style", "nav", "footer", "header",
                     "aside", "form", "noscript", "iframe", "button"]):
        tag.decompose()

    # Try to find main content area first
    main = (
        soup.find("main")
        or soup.find("article")
        or soup.find(id=re.compile(r"content|main|article", re.I))
        or soup.find(class_=re.compile(r"content|main|article|post|body", re.I))
        or soup.body
    )
    if not main:
        main = soup

    # Extract all paragraph-like text
    paragraphs = []
    for tag in main.find_all(["p", "li", "h1", "h2", "h3", "td"]):
        text = tag.get_text(separator=" ", strip=True)
        if len(text) > 25:  # skip tiny fragments
            paragraphs.append(text)

    combined = "\n".join(paragraphs)
    # Collapse whitespace runs
    combined = re.sub(r"\s{3,}", "\n\n", combined)
    return combined[:max_chars]


def scrape_url(url: str) -> str:
    """
    PUBLIC TOOL: Read and extract readable text from any URL.
    Called when user says 'read this page', 'open [url] and tell me what it says', etc.
    Returns clean text content.
    """
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    try:
        resp = requests.get(url, headers=_HEADERS, timeout=_TIMEOUT, allow_redirects=True)
        resp.raise_for_status()
        text = _clean_html_text(resp.text)
        if not text.strip():
            return f"Opened {url} but could not extract readable text."
        domain = urlparse(url).netloc
        return f"[Content from {domain}]\n\n{text}"
    except requests.Timeout:
        return f"Request timed out for {url}. The site may be slow or blocking requests."
    except requests.HTTPError as e:
        return f"HTTP {e.response.status_code} error accessing {url}."
    except Exception as e:
        return f"Could not read {url}: {e}"


# ── Layer 4: Site-specific search ─────────────────────────────────────────────

def search_site(query: str, site_url: str) -> str:
    """
    PUBLIC TOOL: Search for a query within a specific website.
    Uses DuckDuckGo with the 'site:' operator, then scrapes the top result.
    E.g. search_site('Python asyncio error', 'stackoverflow.com')
    """
    # Clean up site URL to just the domain
    if site_url.startswith(("http://", "https://")):
        domain = urlparse(site_url).netloc
    else:
        domain = site_url.replace("www.", "")

    site_query = f"site:{domain} {query}"

    # Try DuckDuckGo first
    results = _duckduckgo_search(site_query)
    if results:
        formatted = _format_ddg_results(results)
        if formatted:
            return f"[Search results from {domain} for '{query}']\n\n{formatted}"

    # Fallback: scrape the site's own search if it has one
    # Common search URL patterns
    search_patterns = [
        f"https://{domain}/search?q={quote_plus(query)}",
        f"https://{domain}/?s={quote_plus(query)}",
        f"https://{domain}/search?query={quote_plus(query)}",
    ]
    for search_url in search_patterns[:1]:  # Try first pattern only to avoid spam
        try:
            result = scrape_url(search_url)
            if result and len(result) > 100:
                return f"[Results from {domain}]\n\n{result[:_MAX_RESULT_CHARS]}"
        except Exception:
            continue

    return f"Could not find results for '{query}' on {domain}."


# ── Main Public Function ──────────────────────────────────────────────────────

def smart_search(query: str, site: str | None = None) -> str:
    """
    PRIMARY PUBLIC FUNCTION — used by get_info() in tools.py.

    Enhanced with:
      - Multi-source synthesis: top DDG results + Wikipedia combined via LLM
      - News vs knowledge routing based on time-sensitive keywords
      - Automatic 2s retry on DDG rate limit

    Returns:
        Clean, synthesized text answer, max ~2500 chars
    """
    query = query.strip()
    if not query:
        return "No search query provided."

    # If a specific site was requested, use search_site()
    if site:
        return search_site(query, site)

    lower = query.lower()

    # Detect if query is time-sensitive (route to DDG only, Wikipedia is stale)
    time_sensitive_kw = [
        "today", "now", "latest", "current", "2024", "2025", "this week",
        "right now", "live", "score", "price", "weather", "breaking"
    ]
    is_time_sensitive = any(kw in lower for kw in time_sensitive_kw)

    # Detect factual/definitional queries (Wikipedia first)
    is_factual = any(kw in lower for kw in _WIKI_KEYWORDS)

    # ── Gather sources ────────────────────────────────────────────────────────
    sources = []

    if not is_time_sensitive and is_factual:
        wiki = _wikipedia_search(query)
        if wiki:
            sources.append(wiki)

    # DDG with retry
    ddg_results = []
    for attempt in range(2):
        ddg_results = _duckduckgo_search(query)
        if ddg_results:
            break
        if attempt == 0:
            time.sleep(2)

    if ddg_results:
        sources.append(_format_ddg_results(ddg_results, max_chars=1500))

    # Try Wikipedia as fallback even if not factual
    if not sources:
        wiki = _wikipedia_search(query)
        if wiki:
            sources.append(wiki)

    if not sources:
        return f"I couldn't find reliable information about '{query}'. Please try rephrasing."

    # ── Synthesize with LLM if we have multiple sources ───────────────────────
    if len(sources) >= 2:
        combined_raw = "\n\n---\n\n".join(sources)
        synthesized = _synthesize_with_llm(query, combined_raw)
        if synthesized:
            return synthesized

    # Single source — return directly
    return sources[0][:_MAX_RESULT_CHARS]


def _synthesize_with_llm(query: str, raw_sources: str) -> str:
    """
    Use a fast LLM call to synthesize multiple search sources into a
    single coherent, concise answer ready to be spoken aloud.
    """
    try:
        from groq import Groq
        from app.core.config import settings
        client = Groq(api_key=settings.GROQ_API_KEY)
        prompt = (
            f"You are Jarvis, a voice assistant. Based ONLY on the sources below, "
            f"write a single concise answer (2-4 sentences, no bullet points, ready to speak aloud) "
            f"for the query: '{query}'\n\nSOURCES:\n{raw_sources[:2500]}"
        )
        resp = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.3
        )
        return resp.choices[0].message.content.strip()
    except Exception:
        return ""
