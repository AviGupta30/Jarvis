"""
research_scraper.py — Autonomous Web Research Scraper
======================================================
Uses DuckDuckGo search and BeautifulSoup to scrape top links for a given topic.
"""
import requests
from bs4 import BeautifulSoup
from app.services.web_search import _duckduckgo_search
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

class ResearchScraper:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        # Avoid scraping massive video/social sites that won't yield good text
        self.blacklist = ["youtube.com", "facebook.com", "instagram.com", "tiktok.com", "twitter.com", "x.com"]

    def _is_allowed(self, url: str) -> bool:
        domain = urlparse(url).netloc.lower()
        for b in self.blacklist:
            if b in domain:
                return False
        if not url.startswith("http"):
            return False
        return True

    def _clean_text(self, html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")
        # Remove script, style, nav, footer, header
        for el in soup(["script", "style", "nav", "footer", "header", "aside", "noscript"]):
            el.decompose()
        
        text = soup.get_text(separator="\n")
        # Clean up whitespace
        lines = [line.strip() for line in text.splitlines()]
        chunks = [line for line in lines if line]
        return "\n".join(chunks)

    def _fetch_page(self, url: str) -> dict:
        print(f"[Scraper] Fetching: {url}")
        try:
            r = requests.get(url, headers=self.headers, timeout=10)
            if r.status_code == 200:
                text = self._clean_text(r.text)
                if len(text) > 200:
                    return {"url": url, "text": text[:4000], "status": "success"}
                else:
                    print(f"[Scraper] {url} fetched but text is too short ({len(text)} chars)")
            else:
                print(f"[Scraper] {url} failed with status {r.status_code}")
        except Exception as e:
            print(f"[Scraper] {url} failed: {e}")
            return {"url": url, "error": str(e), "status": "failed"}
        return {"url": url, "status": "failed"}

    def scrape_topic(self, topic: str, max_sources: int = 4) -> list[dict]:
        """
        Searches DDG for the topic, fetches the top N links concurrently,
        and returns the cleaned text from each source.
        """
        print(f"[Scraper] Searching DuckDuckGo (via Jarvis web_search) for: '{topic}'")
        try:
            results = _duckduckgo_search(topic)
        except Exception as e:
            print(f"[Scraper] DDG search failed: {e}")
            return []

        urls = []
        for r in results:
            url = r.get("href", "")
            if url and self._is_allowed(url):
                urls.append(url)
            if len(urls) >= max_sources:
                break

        if not urls:
            return []

        scraped_data = []
        with ThreadPoolExecutor(max_workers=max_sources) as executor:
            futures = [executor.submit(self._fetch_page, u) for u in urls]
            for f in futures:
                res = f.result()
                if res.get("status") == "success":
                    scraped_data.append(res)

        return scraped_data

if __name__ == "__main__":
    s = ResearchScraper()
    data = s.scrape_topic("DTU Placements 2024 highest package")
    for d in data:
        print(f"--- {d['url']} ---")
        print(d["text"][:200] + "...\n")
