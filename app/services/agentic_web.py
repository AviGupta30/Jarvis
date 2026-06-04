"""
agentic_web.py — Smart Web Research Engine for Jarvis
======================================================
Works exactly like Claude/Gemini browsing:
  1. SEARCH  — Precise DuckDuckGo search targeting listing pages
  2. DIRECT  — Hit known listing URLs for popular sites directly
  3. FETCH   — Parallel download of top pages, extract clean text
  4. SYNTHESIZE — LLM extracts specific items (names, prizes, dates, links)

Fast (< 10s), accurate, returns REAL listings not homepage fluff.
Complies with Rule #4 (Universal Connectivity & Isolation).
"""

import os
import re
import threading
import queue

# ── Known listing page patterns for popular sites ──────────────────────────────
SITE_LISTING_URLS = {
    # Unstop
    ("unstop", "hackathon"):    ["https://unstop.com/hackathons", "https://unstop.com/competitions"],
    ("unstop", "competition"):  ["https://unstop.com/competitions"],
    ("unstop", "internship"):   ["https://unstop.com/internships"],
    ("unstop", "job"):          ["https://unstop.com/jobs"],
    ("unstop", "contest"):      ["https://unstop.com/competitions"],
    # Devfolio
    ("devfolio", "hackathon"):  ["https://devfolio.co/hackathons"],
    # HackerEarth
    ("hackerearth", "hackathon"):  ["https://www.hackerearth.com/challenges/hackathon/"],
    ("hackerearth", "challenge"):  ["https://www.hackerearth.com/challenges/"],
    # LeetCode
    ("leetcode", "contest"):    ["https://leetcode.com/contest/"],
    # Internshala
    ("internshala", "internship"): ["https://internshala.com/internships/"],
    ("internshala", "job"):     ["https://internshala.com/jobs/"],
    # LinkedIn
    ("linkedin", "job"):        ["https://www.linkedin.com/jobs/"],
    # Codeforces
    ("codeforces", "contest"):  ["https://codeforces.com/contests"],
    # HackerRank
    ("hackerrank", "challenge"):["https://www.hackerrank.com/contests"],
}

def _get_api_key():
    api_key = os.environ.get("GROQ_API_KEY", "")
    if not api_key:
        try:
            from app.core.config import settings
            api_key = settings.GROQ_API_KEY
        except Exception:
            pass
    return api_key


def _resolve_listing_urls(site: str, task: str) -> list[str]:
    """Return known direct listing URLs for a site+task combo."""
    task_lower = task.lower()
    for (s, t), urls in SITE_LISTING_URLS.items():
        if s == site.lower() and t in task_lower:
            return urls
    # Generic fallback: try site.com/<keyword>
    keywords = ["hackathon", "contest", "competition", "internship", "job", "challenge"]
    for kw in keywords:
        if kw in task_lower:
            clean = re.sub(r'[^a-zA-Z0-9]', '', site).lower()
            return [f"https://www.{clean}.com/{kw}s", f"https://{clean}.com/{kw}s"]
    clean = re.sub(r'[^a-zA-Z0-9]', '', site).lower()
    return [f"https://www.{clean}.com"]


def _build_search_queries(site: str | None, task: str) -> list[str]:
    """Build 2-3 specific search queries that will hit listing pages, not homepages."""
    import datetime
    year = datetime.datetime.now().year

    # Strip filler words from task
    task_clean = re.sub(r'\b(find|me|get|show|list|search for|please|can you|i want|i need)\b', '', task, flags=re.I).strip()
    task_clean = re.sub(r'\s+', ' ', task_clean).strip()

    queries = []
    if site:
        site_domain = f"{site}.com"
        # Primary: very specific query on the site
        queries.append(f"{task_clean} {year} site:{site_domain}")
        # Secondary: without site filter but mentioning it
        queries.append(f"{task_clean} {site} {year} list upcoming")
    else:
        queries.append(f"{task_clean} {year} list upcoming")
        queries.append(f"{task_clean} {year}")
    return queries


def _search_web(query: str, max_results: int = 5) -> list[dict]:
    """Run a DuckDuckGo search, return list of {title, href, body}."""
    try:
        from duckduckgo_search import DDGS
        results = DDGS().text(query, max_results=max_results)
        return results or []
    except Exception:
        return []


def _fetch_page_text(url: str, timeout: int = 10) -> str:
    """Download a page and return clean readable text (no HTML tags)."""
    try:
        import urllib.request
        from html.parser import HTMLParser

        class _TextExtractor(HTMLParser):
            def __init__(self):
                super().__init__()
                self._skip = False
                self._depth = 0
                self.chunks = []
                self._skip_tags = {'script', 'style', 'nav', 'footer', 'head', 'noscript', 'iframe', 'svg'}
            def handle_starttag(self, tag, attrs):
                if tag in self._skip_tags:
                    self._skip = True
                    self._depth += 1
                elif self._skip:
                    self._depth += 1
            def handle_endtag(self, tag):
                if self._skip:
                    self._depth -= 1
                    if self._depth <= 0:
                        self._skip = False
                        self._depth = 0
            def handle_data(self, data):
                if not self._skip:
                    stripped = data.strip()
                    if len(stripped) > 3:  # skip tiny fragments
                        self.chunks.append(stripped)

        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
            }
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            html = resp.read().decode("utf-8", errors="ignore")

        parser = _TextExtractor()
        parser.feed(html)
        text = " | ".join(parser.chunks)
        text = re.sub(r'\s+', ' ', text).strip()
        return text[:8000]  # more text for listings
    except Exception as e:
        return f"[Could not fetch {url}: {e}]"


def _synthesize(original_query: str, site: str | None, sources: list[dict], api_key: str) -> str:
    """Use the LLM to extract specific listings from the fetched content."""
    from groq import Groq
    client = Groq(api_key=api_key)

    context_parts = []
    for i, s in enumerate(sources, 1):
        title = s.get("title", "")
        url = s.get("url", "")
        text = s.get("text", "")
        snippet = s.get("snippet", "")
        content = text if (text and not text.startswith("[Could")) else snippet
        context_parts.append(f"[Source {i}] {title}\nURL: {url}\n{content[:2500]}")

    context = "\n\n---\n\n".join(context_parts)

    site_hint = f" specifically on {site.capitalize()}" if site else ""

    system_prompt = (
        "You are Jarvis, a smart AI assistant. "
        "The user wants specific items from a website — NOT a description of the website. "
        "Read the web page content below and extract ACTUAL SPECIFIC LISTINGS with real details. "
        "For hackathons: name, prize pool/amount, deadline/date, registration link if visible. "
        "For jobs/internships: company, role, stipend/salary, deadline, location. "
        "For contests: name, platform, date, prizes. "
        "Format as a numbered list. Include ALL details you can find. "
        "If a page has cookie/login walls and no real data, SKIP IT and use the others. "
        "DO NOT say 'visit the website for more details' — extract what's there. "
        "DO NOT describe what the platform is. Just list the actual items."
    )

    user_prompt = (
        f"User query: '{original_query}'{site_hint}\n\n"
        f"Web page content fetched:\n\n{context}"
    )

    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=1500,
        temperature=0.2,
    )
    return resp.choices[0].message.content.strip()


# ── Main entry point ───────────────────────────────────────────────────────────

def agentic_web_action(site_or_task: str, specific_task: str = None):
    """Generator that streams progress and final answer."""
    q = queue.Queue()

    def _worker():
        try:
            for update in _run(site_or_task, specific_task):
                q.put(update)
            q.put(None)
        except Exception as e:
            q.put(f"Error: {e}")
            q.put(None)

    t = threading.Thread(target=_worker, daemon=True)
    t.start()
    while True:
        item = q.get()
        if item is None:
            break
        yield item


def _run(site_or_task: str, specific_task: str = None):
    api_key = _get_api_key()
    if not api_key:
        yield "❌ GROQ_API_KEY is not configured."
        return

    # ── Step 1: Figure out site and task ──────────────────────────────────────
    raw = site_or_task.strip()
    task = specific_task or ""

    site = None
    # "go to <site> and <task>"
    m = re.search(r'(?:go to|open|browse|on|check)\s+([a-zA-Z0-9]+)\s+(?:and\s+)?(.+)', raw, re.I)
    if m:
        site = m.group(1).strip().lower()
        task = task or m.group(2).strip()
    elif specific_task:
        # site_or_task is just the site name
        site = raw.lower().strip()
        task = specific_task

    if not task:
        task = raw

    if site:
        yield f"🔍 Searching **{site.capitalize()}** for: *{task}*"
    else:
        yield f"🔍 Searching the web for: *{task}*"

    # ── Step 2: Collect URLs to fetch ─────────────────────────────────────────
    # A) Direct listing pages for known site+task combos
    direct_urls = _resolve_listing_urls(site, task) if site else []

    # B) DuckDuckGo search queries
    queries = _build_search_queries(site, task)
    
    search_results = []
    for q_str in queries[:2]:
        results = _search_web(q_str, max_results=4)
        for r in results:
            if not any(x.get("href") == r.get("href") for x in search_results):
                search_results.append(r)
        if len(search_results) >= 5:
            break

    search_urls = [r.get("href", "") for r in search_results if r.get("href")]

    # Combine: direct listing URLs first, then search results (deduplicated)
    all_urls = []
    for u in direct_urls:
        if u not in all_urls:
            all_urls.append(u)
    for u in search_urls:
        if u not in all_urls:
            all_urls.append(u)

    top_urls = all_urls[:5]  # fetch at most 5 pages
    
    if not top_urls:
        yield "❌ Could not find any sources. Try a more specific query."
        return

    yield f"📄 Reading {len(top_urls)} pages in parallel..."

    # ── Step 3: Fetch all pages in parallel ───────────────────────────────────
    sources = [None] * len(top_urls)

    def fetch_one(idx, url):
        text = _fetch_page_text(url)
        # Find title/snippet from search results if available
        snippet = next((r.get("body", "") for r in search_results if r.get("href") == url), "")
        title = next((r.get("title", url) for r in search_results if r.get("href") == url), url)
        sources[idx] = {"url": url, "title": title, "text": text, "snippet": snippet}

    threads = [threading.Thread(target=fetch_one, args=(i, u), daemon=True) for i, u in enumerate(top_urls)]
    for th in threads:
        th.start()
    for th in threads:
        th.join(timeout=10)

    # Filter out completely failed fetches
    valid_sources = [s for s in sources if s and s.get("text") and not s["text"].startswith("[Could not fetch")]
    if not valid_sources:
        # Use search snippets as fallback
        valid_sources = [{"url": r.get("href",""), "title": r.get("title",""), "text": r.get("body",""), "snippet":""} for r in search_results[:5]]

    yield "🧠 Extracting listings and preparing your answer..."

    # ── Step 4: Synthesize ────────────────────────────────────────────────────
    original_query = specific_task or site_or_task
    try:
        answer = _synthesize(original_query, site, valid_sources, api_key)
        yield f"\n{answer}"
    except Exception as e:
        # Fallback: format search snippets
        lines = [f"**{r.get('title','')}**\n{r.get('body','')}\n{r.get('href','')}" for r in search_results[:5]]
        yield "Here are the top results:\n\n" + "\n\n".join(lines)
