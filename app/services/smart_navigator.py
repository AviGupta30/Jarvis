"""
smart_navigator.py — Isolated Smart Web Navigator for Jarvis
============================================================
COMPLETELY ISOLATED — imports nothing from the rest of Jarvis except config for the API key.
Safe to modify without affecting any other functionality.

FEATURES:
  - Takes a verbal name like "unstop" or "leetcode" and resolves it to a real URL.
  - Launches a VISIBLE browser (headless=False) so the user can watch it happen.
  - Automatically locates the search bar on the site and types the query.
  - Uses an LLM to read the search results from the page and return a concise summary.

PUBLIC API:
  smart_web_action(site_name: str, task: str) -> str
"""

import time
import re
import os
from playwright.sync_api import sync_playwright

def _get_api_key():
    """Attempt to find the GROQ API key safely."""
    api_key = os.environ.get("GROQ_API_KEY", "")
    if not api_key:
        try:
            import sys
            sys.path.insert(0, str(__import__('pathlib').Path(__file__).parent.parent.parent))
            from app.core.config import settings
            api_key = settings.GROQ_API_KEY
        except Exception:
            pass
    return api_key

def _llm_extract(url: str, raw_text: str, purpose: str) -> str:
    """Pass scraped text through LLM for structured extraction."""
    api_key = _get_api_key()
    if not api_key:
        return raw_text[:1000] + "\n\n(No LLM key configured to summarize results)"

    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        prompt = (
            f"You are Jarvis. From the following webpage content ({url}), "
            f"extract the most useful information regarding: '{purpose}'. "
            f"Provide a concise summary or a numbered list of the top results (max 5 items). "
            f"Ignore navigation links, footers, and cookie banners.\n\nCONTENT:\n{raw_text[:4000]}"
        )
        resp = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.2
        )
        return resp.choices[0].message.content.strip()
    except Exception:
        return raw_text[:1000]

def _resolve_url(site_name: str) -> str:
    """Resolve a verbal site name like 'unstop' to a URL like 'https://unstop.com'."""
    try:
        from duckduckgo_search import DDGS
        results = DDGS().text(site_name, max_results=3)
        if results:
            for r in results:
                href = r.get('href', '')
                if not any(blocked in href for blocked in ['wikipedia.org', 'facebook.com', 'twitter.com', 'linkedin.com']):
                    return href
            return results[0]['href']
    except Exception:
        pass
    
    # Fallback heuristic
    clean = re.sub(r'[^a-zA-Z0-9]', '', site_name).lower()
    return f"https://www.{clean}.com"

def smart_web_action(site_name: str, task: str) -> str:
    """
    Resolves site name, opens a VISIBLE browser, and performs a search or action task.
    """
    url = _resolve_url(site_name)
    
    try:
        with sync_playwright() as p:
            # headless=False so the user can visually see Jarvis opening the site and typing!
            browser = p.chromium.launch(
                headless=False,
                args=[
                    "--start-maximized", 
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox"
                ]
            )
            context = browser.new_context(no_viewport=True)
            # Evade basic bot detection
            context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            page = context.new_page()
            page.goto(url, wait_until="domcontentloaded", timeout=20000)
            page.wait_for_timeout(2000)
            
            # If the task looks like a search task
            task_lower = task.lower()
            if "search" in task_lower or "find" in task_lower:
                # Extract the query
                query = task
                if "search for" in task_lower:
                    query = task_lower.split("search for")[-1].strip()
                elif "search" in task_lower:
                    query = task_lower.split("search")[-1].strip()
                elif "find" in task_lower:
                    query = task_lower.split("find")[-1].strip()
                
                # Try common search input selectors
                search_selectors = [
                    "input[type='search']",
                    "input[name='q']",
                    "input[name='query']",
                    "input[placeholder*='Search' i]",
                    "input[placeholder*='search' i]",
                    "input[aria-label*='Search' i]",
                    ".search-input",
                    "#search"
                ]
                
                search_input = None
                for selector in search_selectors:
                    elements = page.locator(selector)
                    if elements.count() > 0:
                        search_input = elements.first
                        break
                
                # If we still can't find it, maybe there's a search button we need to click first
                if not search_input:
                    search_btns = [
                        "button[aria-label*='Search' i]",
                        "button:has-text('Search')",
                        ".search-icon"
                    ]
                    for btn_sel in search_btns:
                        btn = page.locator(btn_sel)
                        if btn.count() > 0:
                            try:
                                btn.first.click(timeout=1000)
                                page.wait_for_timeout(1000)
                                # Try finding the input again
                                for selector in search_selectors:
                                    elements = page.locator(selector)
                                    if elements.count() > 0:
                                        search_input = elements.first
                                        break
                            except Exception:
                                pass
                        if search_input:
                            break

                if search_input:
                    try:
                        search_input.click(timeout=2000)
                        time.sleep(0.5)
                        search_input.fill(query)
                        time.sleep(0.5)
                        search_input.press("Enter")
                        
                        # Wait for results page to load
                        page.wait_for_load_state("domcontentloaded", timeout=10000)
                        page.wait_for_timeout(4000) # Give it time to render results visually
                        
                        raw_text = page.locator("body").inner_text()
                        clean_text = re.sub(r'\s+', ' ', raw_text).strip()
                        browser.close()
                        
                        extracted = _llm_extract(page.url, clean_text, f"search results for '{query}'")
                        return f"I opened {site_name} ({url}) and searched for '{query}'.\n\nResults:\n{extracted}"
                        
                    except Exception as e:
                        pass
                
                # Fallback if no search box found
                browser.close()
                return f"I opened {url} but couldn't find a search box to search for '{query}'."
            
            # If it wasn't a search task, just read the main page
            page.wait_for_timeout(3000)
            raw_text = page.locator("body").inner_text()
            clean_text = re.sub(r'\s+', ' ', raw_text).strip()
            browser.close()
            
            extracted = _llm_extract(page.url, clean_text, task)
            return f"I went to {url}.\n\nInformation regarding '{task}':\n{extracted}"
            
    except Exception as e:
        return f"Browser error while navigating to {site_name}: {e}"
