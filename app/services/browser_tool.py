"""
browser_tool.py — Jarvis Browser Automation (Step 6 — ENHANCED)
--------------------------------------------------
Enhancements:
  - Anti-bot bypass: realistic viewport, user-agent, JS flag disabling
  - LLM structured extraction: page content intelligently parsed into usable results
  - Multi-page pagination: follow Next links up to N pages
  - Form filling: fill and submit web forms by field labels

Public API:
  browse_and_read(url)                    → str
  search_on_site(site_url, query)         → str
  click_element(page_url, text)           → str
  scroll_and_read(url, px=1500)           → str
  fill_form(url, fields)                  → str
  browse_and_paginate(url, pages=3)       → str
"""

import os
import re
from playwright.sync_api import sync_playwright

_REALISTIC_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)

def _clean_text(text: str) -> str:
    """Clean extracted text from browser by removing extra whitespace."""
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:4000]  # Increased cap for LLM extraction

def _ensure_url(url: str) -> str:
    """Ensure URL has http/https protocol."""
    if not url.startswith('http'):
        return f"https://{url}"
    return url

def _new_browser_page(playwright):
    """Launch an anti-bot-hardened Chromium browser page."""
    browser = playwright.chromium.launch(
        headless=True,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-setuid-sandbox"
        ]
    )
    context = browser.new_context(
        user_agent=_REALISTIC_UA,
        viewport={"width": 1280, "height": 900},
        locale="en-US",
        extra_http_headers={"Accept-Language": "en-US,en;q=0.9"}
    )
    # Disable navigator.webdriver flag to evade bot detection
    context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return browser, context.new_page()

def _llm_extract(url: str, raw_text: str, purpose: str = "general") -> str:
    """Pass scraped text through LLM for structured extraction."""
    try:
        from groq import Groq
        from app.core.config import settings
        client = Groq(api_key=settings.GROQ_API_KEY)
        prompt = (
            f"You are Jarvis. From the following webpage content ({url}), "
            f"extract the most useful {purpose} information in a numbered list (max 8 items). "
            f"Be concise. If it's a search results page, list the titles and key info of results. "
            f"If it's an article, summarize the key points.\n\nCONTENT:\n{raw_text[:3000]}"
        )
        resp = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.2
        )
        return resp.choices[0].message.content.strip()
    except Exception:
        return raw_text[:2000]

def browse_and_read(url: str) -> str:
    """Open a URL and extract the visible text on the page, with LLM structured extraction."""
    url = _ensure_url(url)
    try:
        with sync_playwright() as p:
            browser, page = _new_browser_page(p)
            page.goto(url, wait_until="domcontentloaded", timeout=15000)
            page.wait_for_timeout(2000)
            text = page.locator("body").inner_text()
            browser.close()
            cleaned = _clean_text(text)
            if not cleaned:
                return f"Successfully loaded {url} but found no readable text."
            extracted = _llm_extract(url, cleaned, "content")
            return f"Content of {url}:\n---\n{extracted}"
    except Exception as e:
        return f"Browser error while loading {url}: {e}"

def search_on_site(site_url: str, query: str) -> str:
    """
    Find a search box on the given site, type the query, submit, and return LLM-extracted results.
    """
    site_url = _ensure_url(site_url)
    try:
        with sync_playwright() as p:
            browser, page = _new_browser_page(p)
            page.goto(site_url, wait_until="domcontentloaded", timeout=15000)

            search_selectors = [
                "input[type='search']",
                "input[name='q']",
                "input[name='query']",
                "input[placeholder*='Search' i]",
                "input[placeholder*='search' i]",
                "input[aria-label*='Search' i]"
            ]

            search_input = None
            for selector in search_selectors:
                elements = page.locator(selector)
                if elements.count() > 0:
                    search_input = elements.first
                    break

            if not search_input:
                browser.close()
                return f"Could not find a search box on {site_url}."

            search_input.fill(query)
            search_input.press("Enter")
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_timeout(3000)

            text = page.locator("body").inner_text()
            browser.close()

            extracted = _llm_extract(site_url, _clean_text(text), f"results for '{query}'")
            return f"Search results for '{query}' on {site_url}:\n---\n{extracted}"
    except Exception as e:
        return f"Browser error searching {site_url}: {e}"

def click_element(page_url: str, text: str) -> str:
    """Navigate to a page, click an element containing the specific text, return new page content."""
    page_url = _ensure_url(page_url)
    try:
        with sync_playwright() as p:
            browser, page = _new_browser_page(p)
            page.goto(page_url, wait_until="domcontentloaded", timeout=15000)
            element = page.get_by_text(text, exact=False).first
            if element.count() == 0:
                browser.close()
                return f"Could not find any element containing text '{text}' on {page_url}."
            element.click()
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_timeout(3000)
            new_url = page.url
            new_text = page.locator("body").inner_text()
            browser.close()
            extracted = _llm_extract(new_url, _clean_text(new_text), "content")
            return f"Clicked '{text}'. Now at: {new_url}\n---\n{extracted}"
    except Exception as e:
        return f"Browser error clicking '{text}' on {page_url}: {e}"


def scroll_and_read(url: str, px: int = 1500) -> str:
    """Open a URL, scroll down to load dynamic content, extract and return structured results."""
    url = _ensure_url(url)
    try:
        with sync_playwright() as p:
            browser, page = _new_browser_page(p)
            page.goto(url, wait_until="domcontentloaded", timeout=15000)
            page.evaluate(f"window.scrollBy(0, {px})")
            page.wait_for_timeout(2000)
            text = page.locator("body").inner_text()
            browser.close()
            extracted = _llm_extract(url, _clean_text(text), "content")
            return f"Content of {url} after scrolling:\n---\n{extracted}"
    except Exception as e:
        return f"Browser error scrolling {url}: {e}"


def fill_form(url: str, fields: dict) -> str:
    """
    Navigate to a URL, find form fields by label/placeholder, fill them, optionally submit.
    fields: dict like {"Name": "Avi", "Email": "avi@example.com", "__submit": True}
    """
    url = _ensure_url(url)
    try:
        with sync_playwright() as p:
            browser, page = _new_browser_page(p)
            page.goto(url, wait_until="domcontentloaded", timeout=15000)
            page.wait_for_timeout(2000)

            filled = []
            should_submit = fields.pop("__submit", False)

            for label, value in fields.items():
                selectors = [
                    f"input[placeholder*='{label}' i]",
                    f"input[name*='{label}' i]",
                    f"input[aria-label*='{label}' i]",
                    f"textarea[placeholder*='{label}' i]",
                ]
                done = False
                for sel in selectors:
                    el = page.locator(sel).first
                    if el.count() > 0:
                        el.fill(str(value))
                        filled.append(label)
                        done = True
                        break
                if not done:
                    filled.append(f"{label} (not found)")

            if should_submit:
                page.keyboard.press("Enter")
                page.wait_for_load_state("domcontentloaded")
                page.wait_for_timeout(2000)

            result_text = page.locator("body").inner_text()
            browser.close()
            return (
                f"Form fill complete on {url}.\n"
                f"Fields processed: {', '.join(filled)}.\n"
                f"Page after: {_clean_text(result_text)[:500]}"
            )
    except Exception as e:
        return f"Browser form fill error on {url}: {e}"


def browse_and_paginate(url: str, pages: int = 3) -> str:
    """Open a URL, follow 'Next' pagination links up to N pages, aggregate all results."""
    url = _ensure_url(url)
    all_text = []
    try:
        with sync_playwright() as p:
            browser, page = _new_browser_page(p)
            for page_num in range(pages):
                page.goto(url if page_num == 0 else url, wait_until="domcontentloaded", timeout=15000)
                page.wait_for_timeout(2000)
                text = page.locator("body").inner_text()
                all_text.append(f"--- Page {page_num + 1} ---\n{_clean_text(text)[:1000]}")

                # Try to find a 'Next' button
                next_btn = page.get_by_text("Next", exact=False).first
                if next_btn.count() == 0:
                    break
                try:
                    next_btn.click()
                    page.wait_for_load_state("domcontentloaded")
                    page.wait_for_timeout(2000)
                    url = page.url
                except Exception:
                    break
            browser.close()
        combined = "\n\n".join(all_text)
        extracted = _llm_extract(url, combined, "all results across pages")
        return f"Multi-page results:\n---\n{extracted}"
    except Exception as e:
        return f"Browser pagination error: {e}"
