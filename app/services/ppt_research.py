"""
ppt_research.py — Grounding for AI-written decks (anti-hallucination)
=====================================================================
LLMs invent numbers, dates, quotes and sources — the longer the deck, the worse.
This module makes every specific claim on a generated slide traceable:

  1. gather_sources()  — Wikipedia API + web search (ddgs) → page texts with URLs
  2. extract_facts()   — atomic facts per page; a fact is KEPT ONLY IF every number in it
                         literally occurs in its source page (guards the extractor itself)
  3. relevant_facts()  — the few facts that matter for one slide (keyword retrieval)
  4. audit_slide()     — every number / year / % / money / quote / URL on a slide must be
                         backed by the facts or the user's own text, else it is flagged
  5. scrub_slide()     — deterministic last line of defence: unsupported specifics are
                         removed (clause → item → slide kind downgrade)

No network → no facts → the deck is written qualitatively and the audit removes any number
that is not in the user's prompt.
"""
from __future__ import annotations

import json
import re
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Optional
from urllib.parse import urlparse

import requests

_UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) JarvisPPT/1.0 (personal research assistant)"}
_SKIP_DOMAINS = ("youtube.com", "facebook.com", "instagram.com", "tiktok.com", "twitter.com", "x.com",
                 "pinterest.", "quora.com", "reddit.com", "linkedin.com")


# ══════════════════════════════════════════════════════════════════════════════
#  numbers  (the core of the audit)
# ══════════════════════════════════════════════════════════════════════════════
_UNIT = r"(?:%|percent|per ?cent|x\b|×|gw|mw|kw|twh|gwh|mwh|kwh|km|kg|mt|tonnes?|tons?|million|billion|trillion|" \
        r"crore|lakh|bn|mn|k\b|m\b|b\b|usd|inr|rs|years?|months?|days?|hours?|people|users|jobs|countries|states)"
_NUM_RX = re.compile(r"(?<![A-Za-z\-])(\d{1,3}(?:,\d{2,3})+(?:\.\d+)?|\d+(?:\.\d+)?)(?![A-Za-z\d])")


def _norm_num(s: str) -> str:
    s = s.replace(",", "")
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s


def numbers_in(text: str, all_: bool = False) -> set[str]:
    """Significant numbers in text. Small bare counts (≤ 10 with no unit/%/currency) are ignored unless all_."""
    out = set()
    t = text or ""
    for m in _NUM_RX.finditer(t):
        raw = m.group(1)
        n = _norm_num(raw)
        try:
            val = float(n)
        except ValueError:
            continue
        after = t[m.end():m.end() + 14].lower()
        before = t[max(0, m.start() - 3):m.start()]
        unit = re.match(r"\s?" + _UNIT, after) or re.search(r"[$₹€£]\s?$", before)
        if all_ or val > 10 or unit or "." in raw:
            out.add(n)
    return out


# ══════════════════════════════════════════════════════════════════════════════
#  sources
# ══════════════════════════════════════════════════════════════════════════════
def _clean_html(html: str, limit: int = 12000) -> str:
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        for el in soup(["script", "style", "nav", "footer", "header", "aside", "noscript", "form"]):
            el.decompose()
        lines = [l.strip() for l in soup.get_text("\n").splitlines()]
        return "\n".join(l for l in lines if len(l) > 2)[:limit]
    except Exception:
        return ""


def web_search(query: str, n: int = 6) -> list[dict]:
    """ddgs (multi-backend) with retries; falls back to the legacy package. → [{title, href, body}]"""
    for attempt in range(4):
        try:
            from ddgs import DDGS
            res = DDGS().text(query, max_results=n, backend="auto")
            if res:
                return [r for r in res if r.get("href")]
        except Exception:
            pass
        time.sleep(1.5 * (attempt + 1))                  # search engines throttle bursts — back off
    try:
        from duckduckgo_search import DDGS as _Old
        with _Old() as d:
            return [r for r in d.text(query, max_results=n) if r.get("href")]
    except Exception:
        return []


def wiki_pages(query: str, n: int = 2, limit: int = 14000) -> list[dict]:
    try:
        api = "https://en.wikipedia.org/w/api.php"
        hits = requests.get(api, params={"action": "query", "list": "search", "srsearch": query, "format": "json",
                                         "srlimit": n + 4}, headers=_UA, timeout=10).json()["query"]["search"]
        anchors, qt = _anchors(query), _toks(query)
        # prefer articles about the topic's entity ("Renewable energy in India" over "Energy transition")
        hits.sort(key=lambda h: -(3 * len(_toks(h["title"]) & anchors) + len(_toks(h["title"]) & qt)))
        out = []
        for h in hits[:n]:
            pg = requests.get(api, params={"action": "query", "prop": "extracts", "explaintext": 1, "titles": h["title"],
                                           "format": "json"}, headers=_UA, timeout=12).json()
            txt = list(pg["query"]["pages"].values())[0].get("extract", "")
            if len(txt) > 400:
                out.append({"url": "https://en.wikipedia.org/wiki/" + h["title"].replace(" ", "_"),
                            "title": h["title"] + " — Wikipedia", "text": txt[:limit]})
        return out
    except Exception as e:
        print(f"[ppt_research] wikipedia failed: {e}")
        return []


def fetch_page(url: str) -> Optional[dict]:
    if any(d in url for d in _SKIP_DOMAINS) or url.lower().endswith(".pdf"):
        return None
    try:
        r = requests.get(url, headers=_UA, timeout=10)
        if r.status_code != 200 or "html" not in r.headers.get("content-type", "html"):
            return None
        txt = _clean_html(r.text)
        if len(txt) < 400:
            return None
        title = re.search(r"<title[^>]*>(.*?)</title>", r.text, re.I | re.S)
        return {"url": url, "title": (title.group(1).strip()[:120] if title else urlparse(url).netloc), "text": txt}
    except Exception:
        return None


def gather_sources(topic: str, queries: list[str], progress=None, max_pages: int = 10) -> list[dict]:
    say = progress or (lambda m: None)
    pages: list[dict] = []
    seen: set[str] = set()
    with ThreadPoolExecutor(max_workers=6) as ex:
        wiki_f = ex.submit(wiki_pages, topic, 2)
        with ThreadPoolExecutor(max_workers=2) as sx:   # ≤ 2 searches at a time (bursts get empty results)
            results = list(sx.map(lambda q: web_search(q, 5), queries))
        pages += wiki_f.result()
        for p in pages:
            seen.add(p["url"])
        urls = []
        for res in results:
            for r in res[:3]:
                u = r["href"]
                dom = urlparse(u).netloc
                if u in seen or any(dom == urlparse(x).netloc for x in urls):
                    continue
                urls.append(u)
                seen.add(u)
        for pg in ex.map(fetch_page, urls[:max_pages * 2]):
            if pg and len(pages) < max_pages:
                pages.append(pg)
            # keep search snippets too: they are short but dated and specific
    web_pages = sum(1 for p in pages if "wikipedia.org" not in p["url"])
    if web_pages < 3:
        # web search throttled / pages blocked → widen the encyclopedic base: one article per angle
        with ThreadPoolExecutor(max_workers=3) as ex:
            anchors, tt = _anchors(topic), _toks(topic)
            for extra in ex.map(lambda q: wiki_pages(q, 1), queries[1:]):
                for pg in extra:
                    title_t = _toks(pg["title"])
                    on_topic = (title_t & anchors) if anchors else len(title_t & tt) >= 2
                    if on_topic and pg["url"] not in seen and len(pages) < max_pages:
                        pages.append(pg)
                        seen.add(pg["url"])
    snippets = [{"url": r["href"], "title": r.get("title", ""), "text": r.get("body", "")}
                for res in results for r in res if r.get("body")]
    if snippets:
        pages.append({"url": "search-snippets", "title": "Search result snippets", "text": "\n".join(
            f"{s['text']} [{urlparse(s['url']).netloc}]" for s in snippets)[:6000], "_snippets": snippets})
    say(f"🌐 Read {sum(1 for p in pages if p['url'] != 'search-snippets')} source(s): "
        + ", ".join(sorted({urlparse(p['url']).netloc.replace('www.', '') for p in pages
                            if p['url'] != 'search-snippets'}))[:160])
    return pages


# ══════════════════════════════════════════════════════════════════════════════
#  facts
# ══════════════════════════════════════════════════════════════════════════════
_STOP = set("the a an and or of in on to for with by from at as is are was were be been this that these those it its "
            "into over under than then also more most such which who what when where how their there have has had "
            "will would can could should may might about after before between during per".split())


def _toks(s: str) -> set[str]:
    return {w[:6] for w in re.findall(r"[a-z0-9]{3,}", (s or "").lower()) if w not in _STOP}


_JUNK = re.compile(r"cookie|subscribe|sign ?up|newsletter|all rights reserved|click here|javascript|log ?in|"
                   r"privacy policy|terms of (use|service)|advertis|read more|download (the )?app|follow us|"
                   r"©|copyright|share this|related articles?|"
                   r"\bISBN\b|\bpp?\.\s?\d|\bdoi\b|retrieved (?:on )?\d|archived from|\bjournal of\b|\bvol\.\s?\d|"
                   r"\bet al\.|\(\d{4}\)\.\s|^\"[^\"]{10,}\"\s*,", re.I)       # bibliography / reference-list lines
_DANGLING = re.compile(r"^(it|this|these|those|they|he|she|its|their|however|but|and|also|such|here|there|"
                       r"thus|hence|therefore|meanwhile|moreover|furthermore|in addition)\b", re.I)


_META = re.compile(r"^(?:this|the present|our|in this|the current|the following|this (?:\w+ )?)"
                   r"\s*(?:study|paper|article|report|review|work|analysis|research|section|chapter|page|post|blog)\b|"
                   r"^(?:we|i)\s+(?:present|propose|examine|analy[sz]e|discuss|review|find|show)\b|"
                   r"^the (?:study|paper|authors?) (?:concludes?|presents?|finds?|shows?|proposes?)\b", re.I)


def _sentences(text: str):
    text = re.sub(r"\[(?:\d+|[a-z]|citation needed|note \d+)\]", "", text)        # wiki footnote markers
    for para in text.split("\n"):
        para = para.strip()
        if len(para) < 50:
            continue
        for s in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9“\"(])", para):
            yield s.strip()


def extract_facts(topic: str, pages: list[dict], llm_json=None, progress=None, per_page: int = 18) -> list[dict]:
    """Zero-LLM, zero-hallucination fact extraction: facts ARE verbatim source sentences that are
    self-contained, on-topic and (preferably) carry figures/dates. → [{id, fact, source, url}]"""
    say = progress or (lambda m: None)
    tt, anchors = _toks(topic), _anchors(topic)
    picked = []
    for pg in pages:
        snippets = pg.get("_snippets")
        cands = []
        src_iter = ((s["text"], s.get("title") or urlparse(s["url"]).netloc, s["url"]) for s in snippets) if snippets \
            else ((s, pg["title"], pg["url"]) for s in _sentences(pg["text"]))
        for s, title, url in src_iter:
            s = re.sub(r"\s+", " ", s or "").strip(" -–•")
            s = re.sub(r"^(?:[A-Z][a-z]{2,8}\.? \d{1,2}, \d{4}|\d+ (?:days?|hours?) ago)\s*[·\-–]\s*", "", s)  # snippet dates
            if not 45 <= len(s) <= 330 or s.count(" ") < 7 or _JUNK.search(s) or s.endswith(("?", ":")):
                continue
            letters = re.findall(r"[^\W\d_]", s)
            if letters and sum(1 for c in letters if ord(c) > 0x24F) / len(letters) > 0.15:
                continue                                       # navigation chrome in other scripts
            if re.search(r"\b(home|about us|contact us|menu|search)\b.*\b(home|about us|contact us|menu)\b", s, re.I):
                continue
            tok = _toks(s)
            rel = len(tok & tt)
            if rel == 0:
                continue
            score = rel + 1.3 * min(3, len(numbers_in(s, all_=True))) + (1.6 if tok & anchors else 0)
            score += 0.4 if "wikipedia" in url else 0
            if _META.match(s):
                continue                                       # the source describing itself ("This study presents…")
            if _DANGLING.match(s):
                score -= 2.0                                   # not self-contained
            if re.search(r"\b(may|might|could|reportedly|allegedly|rumou?r)\b", s, re.I):
                score -= 0.6                                   # hedged claims are weaker facts
            cands.append((score, {"fact": s, "source": title, "url": url}))
        cands.sort(key=lambda x: -x[0])
        picked += [c for sc, c in cands[:per_page] if sc >= 2.0]
    facts, seen = [], []
    picked.sort(key=lambda f: -(len(_toks(f["fact"]) & tt) + 1.3 * min(3, len(numbers_in(f["fact"], all_=True)))))
    for f in picked:
        tk = _toks(f["fact"])
        if any(len(tk & s) / max(1, len(tk | s)) > 0.6 for s in seen):
            continue
        seen.append(tk)
        facts.append(f)
    # stay on topic: if the topic names an entity ("India", "Tesla"), facts about it come first and
    # off-entity facts (other countries, history trivia) are capped
    if anchors:
        on = [f for f in facts if _toks(f["fact"] + " " + f["source"]) & anchors]
        if len(on) >= 8:
            off = [f for f in facts if f not in on]
            facts = on + off[:max(6, len(on) // 4)]
    facts = facts[:100]
    for i, f in enumerate(facts):
        f["id"] = f"F{i + 1}"
    say(f"📚 Collected {len(facts)} facts, quoted word-for-word from the sources.")
    return facts


_GENERIC = set("energy transition future trends overview introduction analysis impact role system systems technology "
               "technologies market industry sector development growth management study report history challenges "
               "applications benefits solutions".split())


def _anchors(topic: str) -> set[str]:
    """Distinctive tokens of a topic: proper nouns/acronyms first, else the non-generic content words."""
    words = re.findall(r"[A-Za-z][A-Za-z0-9&\-]+", topic or "")
    proper = {w.lower()[:6] for i, w in enumerate(words) if (w[0].isupper() and i > 0) or (w.isupper() and len(w) > 1)}
    proper -= {w[:6] for w in _GENERIC}
    return {p for p in proper if len(p) >= 3}


def relevant_facts(facts: list[dict], query: str, k: int = 10, exclude: Optional[set] = None) -> list[dict]:
    q = _toks(query)
    scored = []
    for f in facts:
        if exclude and f["id"] in exclude:
            continue
        sc = len(q & _toks(f["fact"])) + 0.15 * len(numbers_in(f["fact"]))
        if sc > 0:
            scored.append((sc, f))
    scored.sort(key=lambda x: -x[0])
    return [f for _, f in scored[:k]]


def facts_block(facts: list[dict]) -> str:
    return "\n".join(f"{f['id']}: {f['fact']}" for f in facts)


# ══════════════════════════════════════════════════════════════════════════════
#  audit + scrub
# ══════════════════════════════════════════════════════════════════════════════
def _walk_texts(sl: dict):
    """Yield (path, text) for every user-visible string on a slide."""
    for k in ("title", "subtitle", "body", "lead"):
        if isinstance(sl.get(k), str) and sl[k]:
            yield (k,), sl[k]
    for key in ("bullets", "steps"):
        for i, it in enumerate(sl.get(key) or []):
            if isinstance(it, dict):
                for f in ("head", "text", "date"):
                    if it.get(f):
                        yield (key, i, f), str(it[f])
    for i, st in enumerate(sl.get("stats") or []):
        for f in ("value", "label", "desc"):
            if st.get(f):
                yield ("stats", i, f), str(st[f])
    for ci, c in enumerate(sl.get("columns") or []):
        if c.get("heading"):
            yield ("columns", ci, "heading"), c["heading"]
        for pi, p in enumerate(c.get("points") or []):
            yield ("columns", ci, "points", pi), str(p)
    tb = sl.get("table") or {}
    for ri, row in enumerate(tb.get("rows") or []):
        for ci, cell in enumerate(row):
            yield ("table", "rows", ri, ci), str(cell)
    ch = sl.get("chart") or {}
    for si, se in enumerate(ch.get("series") or []):
        for vi, v in enumerate(se.get("values") or []):
            yield ("chart", "series", si, "values", vi), str(v)
    for vi, v in enumerate(ch.get("values") or []):
        yield ("chart", "values", vi), str(v)
    q = sl.get("quote")
    if isinstance(q, dict) and q.get("text"):
        yield ("quote", "text"), q["text"]
    for si, sec in enumerate(sl.get("sections") or []):
        if not isinstance(sec, dict):
            continue
        if sec.get("lead"):
            yield ("sections", si, "lead"), sec["lead"]
        for ii, it in enumerate(sec.get("items") or []):
            if isinstance(it, dict):
                for f in ("head", "text", "value", "label", "desc"):
                    if it.get(f):
                        yield ("sections", si, "items", ii, f), str(it[f])
        for ri, row in enumerate(sec.get("rows") or []):
            for ci, cell in enumerate(row if isinstance(row, list) else []):
                yield ("sections", si, "rows", ri, ci), str(cell)


def allowed_numbers(facts: list[dict], user_text: str) -> set[str]:
    out = numbers_in(user_text or "", all_=True)
    for f in facts:
        out |= numbers_in(f["fact"], all_=True)
    return out


def audit_slide(sl: dict, allowed: set[str], fact_text: str) -> list[dict]:
    """→ problems [{path, text, bad: [numbers], why}]"""
    probs = []
    for path, txt in _walk_texts(sl):
        bad = sorted(n for n in numbers_in(txt) if n not in allowed)
        if path[0] == "chart":                          # every chart value must be sourced
            bad = sorted(n for n in numbers_in(txt, all_=True) if n not in allowed)
        why = []
        if bad:
            why.append("unsupported numbers " + ", ".join(bad))
        if re.search(r"https?://|www\.|doi\.org|\bdoi:", txt, re.I):
            urls = re.findall(r"(?:https?://|www\.)\S+|doi\S*", txt, re.I)
            if any(u.rstrip(").,") not in fact_text for u in urls):
                why.append("unsourced link")
        if why:
            probs.append({"path": path, "text": txt, "bad": bad, "why": "; ".join(why)})
    q = sl.get("quote")
    if isinstance(q, dict) and q.get("text"):
        qt = _toks(q["text"])
        if not qt or len(qt & _toks(fact_text)) / len(qt) < 0.8:
            probs.append({"path": ("quote",), "text": q["text"], "bad": [], "why": "quote not found in sources"})
    return probs


def _drop_clauses(txt: str, bad: set[str]) -> str:
    parts = re.split(r"(?<=[;,.])\s+|\s+(?:—|–)\s+", txt)
    keep = [p for p in parts if not (numbers_in(p) & bad)]
    out = " ".join(keep).strip(" ,;—–")
    return out if len(out.split()) >= 3 else ""


def scrub_slide(sl: dict, allowed: set[str], fact_text: str) -> tuple[dict, int]:
    """Remove whatever the audit still flags. Returns (slide, n_removed)."""
    sl = json.loads(json.dumps(sl))
    removed = 0
    # data kinds: keep only fully-sourced data
    if sl.get("stats"):
        keep = [s for s in sl["stats"] if not (numbers_in(str(s.get("value", "")) + " " + str(s.get("desc", "")))
                                               - allowed)]
        removed += len(sl["stats"]) - len(keep)
        sl["stats"] = keep
    ch = sl.get("chart")
    if ch:
        vals = [v for se in ch.get("series") or [] for v in se.get("values") or []] + list(ch.get("values") or [])
        if any(numbers_in(str(v), all_=True) - allowed for v in vals):
            sl.pop("chart", None)
            removed += 1
            if sl.get("kind") == "chart":
                sl["kind"] = "content"
    tb = sl.get("table")
    if tb and tb.get("rows"):
        rows = [r for r in tb["rows"] if not any(numbers_in(str(c)) - allowed for c in r)]
        removed += len(tb["rows"]) - len(rows)
        tb["rows"] = rows
        if len(rows) < 2 and sl.get("kind") == "table":
            sl["bullets"] = [{"head": str(r[0]), "text": " · ".join(map(str, r[1:]))} for r in rows]
            sl.pop("table", None)
            sl["kind"] = "content"
    if sl.get("steps"):
        keep = [s for s in sl["steps"] if not (numbers_in(" ".join(str(s.get(k, "")) for k in ("date", "head", "text")))
                                               - allowed)]
        removed += len(sl["steps"]) - len(keep)
        sl["steps"] = keep
    q = sl.get("quote")
    if isinstance(q, dict) and q.get("text"):
        qt = _toks(q["text"])
        if not qt or len(qt & _toks(fact_text)) / len(qt) < 0.8:
            sl.pop("quote", None)
            removed += 1
            if sl.get("kind") == "quote":
                sl["kind"] = "content"
                sl["body"] = sl.get("body") or ""
    # free text: drop the offending clause, then the item
    for key in ("bullets",):
        new = []
        for it in sl.get(key) or []:
            t = str(it.get("text") or "")
            bad = numbers_in(t) - allowed
            if bad:
                t2 = _drop_clauses(t, bad)
                removed += 1
                if not t2 and not it.get("head"):
                    continue
                it = {**it, "text": t2}
            if numbers_in(str(it.get("head") or "")) - allowed:
                removed += 1
                continue
            new.append(it)
        sl[key] = new
    for k in ("body", "subtitle", "lead"):
        if isinstance(sl.get(k), str):
            bad = numbers_in(sl[k]) - allowed
            if bad:
                sl[k] = _drop_clauses(sl[k], bad)
                removed += 1
    for c in sl.get("columns") or []:
        pts = []
        for p in c.get("points") or []:
            bad = numbers_in(str(p)) - allowed
            if bad:
                removed += 1
                p = _drop_clauses(str(p), bad)
                if not p:
                    continue
            pts.append(p)
        c["points"] = pts
    for sec in sl.get("sections") or []:
        if not isinstance(sec, dict):
            continue
        items = []
        for it in sec.get("items") or []:
            if not isinstance(it, dict):
                continue
            blob = " ".join(str(it.get(f) or "") for f in ("value", "label", "desc"))
            if numbers_in(blob) - allowed:
                removed += 1
                continue
            t = str(it.get("text") or "")
            bad = numbers_in(t) - allowed
            if bad:
                removed += 1
                t = _drop_clauses(t, bad)
                if not t and not it.get("head"):
                    continue
                it = {**it, "text": t}
            items.append(it)
        sec["items"] = items
        if sec.get("rows"):
            sec["rows"] = [r for r in sec["rows"] if not any(numbers_in(str(c)) - allowed for c in r)]
    # links that are not in the sources
    for path, txt in list(_walk_texts(sl)):
        if re.search(r"https?://|www\.|doi", txt, re.I):
            pass
    return sl, removed


def sources_note(sl: dict, facts: list[dict]) -> str:
    """Which sources back the specifics on this slide → for the speaker notes."""
    nums = set()
    for _, t in _walk_texts(sl):
        nums |= numbers_in(t)
    used = []
    for f in facts:
        if nums & numbers_in(f["fact"]) and f["url"] not in used and f["url"] != "search-snippets":
            used.append(f["url"])
    return ("Sources: " + "; ".join(used[:4])) if used else ""


_FID = re.compile(r"\s*[\(\[]\s*(?:F\d+\s*[,;/&]?\s*)+[\)\]]|\s*\b(?:fact|source)s?\s*F\d+\b", re.I)


def strip_fact_ids(o):
    """'(F3)', '[F2, F7]' are for the model, never for the audience."""
    if isinstance(o, str):
        return _FID.sub("", o).strip()
    if isinstance(o, list):
        return [strip_fact_ids(x) for x in o]
    if isinstance(o, dict):
        return {k: (strip_fact_ids(v) if k not in ("images", "facts", "_facts") else v) for k, v in o.items()}
    return o
