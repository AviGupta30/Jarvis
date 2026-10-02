"""
ppt_content.py — Content brain for the PPT v6 engine
=====================================================
• detect_profile(prompt)            → purpose + density ("light" | "balanced" | "dense")
• split_request(prompt)             → instruction / source material / attachments
• parse_user_slides(text)           → STRICT slides from user-written content ("Slide 1: …"),
                                      text kept verbatim, only structure is inferred
• infer_kind(slide, i, n)           → layout kind from the content's shape (no rewriting)
• generate_deck(...)                → LLM outline + content (only for what the user did not give)
• apply_edit(deck, instruction, …)  → follow-up edits: deterministic ops first, LLM for the rest

Everything returns plain dicts (the deck spec) so the deck can be persisted as JSON.
"""
from __future__ import annotations

import copy
import json
import os
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional

KINDS = ["title", "agenda", "section", "content", "cards", "stats", "process", "timeline",
         "comparison", "table", "chart", "quote", "image", "gallery", "closing", "sections"]

_KIND_SYNONYMS = {
    "title": "title", "cover": "title", "intro slide": "title",
    "agenda": "agenda", "outline": "agenda", "contents": "agenda", "toc": "agenda",
    "section": "section", "divider": "section", "section header": "section",
    "bullets": "content", "bullet": "content", "list": "content", "text": "content", "content": "content",
    "cards": "cards", "card": "cards", "grid": "cards", "boxes": "cards", "features": "cards", "columns": "cards",
    "stats": "stats", "stat": "stats", "metrics": "stats", "numbers": "stats", "kpi": "stats", "kpis": "stats",
    "process": "process", "steps": "process", "flow": "process", "workflow": "process", "pipeline": "process",
    "timeline": "timeline", "roadmap": "timeline", "milestones": "timeline",
    "sections": "sections", "composite": "sections", "infographic": "sections", "rich": "sections",
    "comparison": "comparison", "compare": "comparison", "versus": "comparison", "vs": "comparison",
    "two columns": "comparison", "pros and cons": "comparison",
    "table": "table", "matrix": "table",
    "chart": "chart", "graph": "chart", "bar chart": "chart", "pie chart": "chart", "line chart": "chart",
    "quote": "quote", "testimonial": "quote",
    "image": "image", "picture": "image", "photo": "image", "full image": "image", "hero": "image",
    "gallery": "gallery", "collage": "gallery",
    "closing": "closing", "thank you": "closing", "end": "closing", "conclusion slide": "closing",
}

# ══════════════════════════════════════════════════════════════════════════════
#  LLM
# ══════════════════════════════════════════════════════════════════════════════
_client = None


def _groq():
    global _client
    if _client is None:
        from groq import Groq
        from app.core.config import settings
        _client = Groq(api_key=settings.GROQ_API_KEY)
    return _client


_BIG, _FAST = "openai/gpt-oss-120b", "openai/gpt-oss-20b"
_TPM = 7400                                  # Groq free tier: 8 000 tokens/min per model — keep a margin
_RL_LOCK = threading.Lock()
_RL_LOG: dict[str, list] = {}                # model → [[t, tokens], …] of the last minute


def _budget_left(model: str) -> int:
    now = time.time()
    with _RL_LOCK:
        log = [e for e in _RL_LOG.get(model, []) if now - e[0] < 60]
        _RL_LOG[model] = log
        return _TPM - sum(e[1] for e in log)


def _reserve(model: str, tokens: int) -> list:
    """Client-side pacing: wait until this call fits in the model's per-minute budget (no 429 storms)."""
    tokens = min(tokens, _TPM)
    while True:
        now = time.time()
        with _RL_LOCK:
            log = [e for e in _RL_LOG.get(model, []) if now - e[0] < 60]
            _RL_LOG[model] = log
            if sum(e[1] for e in log) + tokens <= _TPM or not log:
                entry = [now, tokens]
                log.append(entry)
                return entry
            wait = 60 - (now - log[0][0]) + 0.3
        time.sleep(max(0.5, min(wait, 4.0)))


_DAY_CAPPED: dict[str, float] = {}          # model → until when it is out of daily quota
_GEMINI = ["gemini-3.8-flash", "gemini-3.5-flash", "gemini-3.5-flash-lite"]


def _gemini_json(system: str, user: str, max_tokens: int, temperature: float) -> dict:
    """Backup provider when Groq's daily token cap is reached (same JSON contract)."""
    from app.core.config import settings
    key = getattr(settings, "GEMINI_API_KEY", "")
    if not key:
        raise RuntimeError("no GEMINI_API_KEY")
    import requests
    last = None
    ready = [m for m in _GEMINI if _DAY_CAPPED.get(m, 0) <= time.time()] or _GEMINI[-1:]
    for model in ready:
        for attempt in range(2):
            try:
                r = requests.post(
                    f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}",
                    json={"systemInstruction": {"parts": [{"text": system}]},
                          "contents": [{"role": "user", "parts": [{"text": user}]}],
                          "generationConfig": {"responseMimeType": "application/json", "temperature": temperature,
                                               "maxOutputTokens": max_tokens + 3000}},
                    timeout=120)
                if r.status_code in (429, 503, 500):
                    last = RuntimeError(f"{model} {r.status_code}")
                    if os.environ.get("PPT_DEBUG"):
                        print(f"[llm] gemini {model} {r.status_code}", flush=True)
                    if r.status_code == 429 and "per day" in r.text.lower():
                        _DAY_CAPPED[model] = time.time() + 3600
                        break
                    # overloaded / per-minute limited: let the next model take the call and rest this one
                    _DAY_CAPPED[model] = time.time() + (300 if r.status_code == 503 else 60)
                    break
                r.raise_for_status()
                if os.environ.get("PPT_DEBUG"):
                    print(f"[llm] gemini {model} ok", flush=True)
                parts = r.json()["candidates"][0]["content"]["parts"]
                raw = "".join(p.get("text", "") for p in parts if not p.get("thought"))
                raw = re.sub(r"```(?:json)?|```", "", raw).strip()
                return json.loads(raw[raw.find("{"): raw.rfind("}") + 1])
            except Exception as e:
                last = e
                time.sleep(1.0)
    raise RuntimeError(f"Gemini failed: {last}")


def _llm_json(system: str, user: str, max_tokens: int = 4000, temperature: float = 0.6, fast: bool = False,
              balance: bool = False, effort: Optional[str] = None) -> dict:
    """JSON completion with pacing + fallback.
    fast=True    → 20b first (copy/extraction work that is verified afterwards)
    balance=True → whichever model has more budget left (long decks: spreads load over both)
    effort       → gpt-oss reasoning effort ("low" saves tokens on copy-style tasks)"""
    order = [_FAST, _BIG] if fast else [_BIG, _FAST]
    if balance and _budget_left(_FAST) > _budget_left(_BIG) + 1500:
        order = [_FAST, _BIG]
    est = int(len(system + user) / 3.4) + int(max_tokens * 0.7)
    last = None
    order = [m for m in order if _DAY_CAPPED.get(m, 0) < time.time()]
    for model in order:
        for attempt in range(3):
            entry = _reserve(model, est)
            try:
                kw = {"reasoning_effort": effort} if effort else {}
                r = _groq().chat.completions.create(
                    model=model,
                    messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
                    max_tokens=min(max_tokens, 8000), temperature=temperature,
                    response_format={"type": "json_object"}, **kw)
                try:
                    entry[1] = int(r.usage.total_tokens)            # book the real usage
                except Exception:
                    pass
                if os.environ.get("PPT_DEBUG"):
                    print(f"[llm] groq {model} {entry[1]} tok", flush=True)
                raw = r.choices[0].message.content or ""
                raw = re.sub(r"```(?:json)?|```", "", raw).strip()
                return json.loads(raw[raw.find("{"): raw.rfind("}") + 1])
            except Exception as e:
                last = e
                msg = str(e).lower()
                if "413" in msg or "too large" in msg:
                    break
                if "429" in msg or "rate limit" in msg:
                    m = re.search(r"try again in (?:(\d+)m)?([\d.]+)s", msg)
                    wait = (int(m.group(1) or 0) * 60 + float(m.group(2))) if m else 8.0
                    if "per day" in msg or "tpd" in msg:
                        _DAY_CAPPED[model] = time.time() + 900    # daily cap → skip this model for a while
                        break
                    if wait > 40:
                        break                                     # long wait → other model
                    with _RL_LOCK:                                # the server says we're full: mark it
                        _RL_LOG.setdefault(model, []).append([time.time(), _TPM])
                    time.sleep(min(wait + 0.5, 40))
                    continue
                if isinstance(e, (json.JSONDecodeError, ValueError)) and attempt == 0:
                    continue                                      # malformed JSON → one more try
                time.sleep(1.2 * (attempt + 1))
    try:                                                          # Groq exhausted → Gemini keeps Jarvis working
        return _gemini_json(system, user, max_tokens, temperature)
    except Exception as e:
        raise RuntimeError(f"LLM call failed (Groq: {last}; Gemini: {e})")



# ══════════════════════════════════════════════════════════════════════════════
#  PROFILE
# ══════════════════════════════════════════════════════════════════════════════
_HACK = ("hackathon", "hack-a-thon", "sih", "smart india", "idea submission", "idea ppt", "pitch deck", "pitch", "startup", "investor", "demo day", "mvp",
         "shark tank", "prototype", "product launch", "incubator", "accelerator", "ideathon", "buildathon")
_DENSE = ("detailed", "in-depth", "in depth", "comprehensive", "content heavy", "content-heavy", "more content",
          "lots of content", "dense", "thorough", "technical deep", "elaborate", "full content", "descriptive")
_BAL = ("college", "class", "school", "university", "assignment", "seminar", "academic", "project report",
        "research", "thesis", "lecture", "workshop", "training", "report", "case study", "internship", "viva")
_LIGHT = ("minimal", "simple", "less text", "less content", "few words", "fewer words", "clean", "normal",
          "short", "brief", "concise", "visual", "keynote")


def detect_profile(prompt: str, purpose: Optional[str] = None) -> tuple[str, str]:
    low = (prompt or "").lower()
    has = lambda kws: any(k in low for k in kws)
    if purpose == "hackathon" or has(_HACK):
        p, d = "hackathon", "dense"
    elif has(_BAL):
        p, d = "academic", "balanced"
    elif re.search(r"\b(business|board|quarterly|client|sales|marketing|company|corporate)\b", low):
        p, d = "business", "balanced"
    else:
        p, d = (purpose or "general"), "light"
    if has(_DENSE):
        d = "dense"
    elif has(_LIGHT) and not has(_DENSE):
        d = "light" if p != "hackathon" else "balanced"
    return p, d


def slide_count(prompt: str) -> int:
    m = re.search(r"\b(\d{1,2})\s*(?:-|to)?\s*(\d{1,2})?\s*(?:slides?|pages?)\b", prompt or "", re.I)
    if not m:
        return 0
    n = int(m.group(2) or m.group(1))
    return max(3, min(30, n))


# ══════════════════════════════════════════════════════════════════════════════
#  REQUEST SPLITTING
# ══════════════════════════════════════════════════════════════════════════════
_ATTACH = re.compile(r"\[ATTACHED_FILE:\s*(.+?)\]", re.I)


def split_request(prompt: str) -> dict:
    """Separate the user's command, any pasted/attached content and attachment paths."""
    prompt = prompt or ""
    attachments = []
    for raw in _ATTACH.findall(prompt):
        parts = [p.strip() for p in raw.split("|")]
        desc = ""
        for p in parts[1:]:
            if p.upper().startswith("DESCRIPTION:"):
                desc = p.split(":", 1)[1].strip()
        attachments.append({"path": parts[0], "desc": desc})
    text = _ATTACH.sub("", prompt)
    attached_ctx = ""
    if "Attached Context:" in text:
        text, attached_ctx = text.split("Attached Context:", 1)
        attached_ctx = re.sub(r"^Content of .+?:\s*$", "", attached_ctx, flags=re.M).strip()
    text = text.strip()
    # command = first line / sentence before any slide content
    m = _SLIDE_HDR.search(text) or _INLINE_SLIDE.search(text)
    if m:
        command, body = text[:m.start()].strip(), text[m.start():].strip()
    else:
        lines = text.split("\n", 1)
        command = lines[0].strip()
        body = lines[1].strip() if len(lines) > 1 else ""
        # a long single paragraph after a colon is content too ("make a ppt from this: …")
        if not body and ":" in command and len(command) > 220:
            command, body = command.split(":", 1)
    return {"command": command.strip(), "body": body.strip(), "attached_text": attached_ctx[:24000],
            "attachments": attachments, "full": text}


# ══════════════════════════════════════════════════════════════════════════════
#  STRICT PARSER  (user-provided content → slides, text verbatim)
# ══════════════════════════════════════════════════════════════════════════════
_SLIDE_HDR = re.compile(
    r"^[ \t>]*(?:#{1,6}[ \t]*)?(?:\*\*|__)?[ \t]*slide[ \t]*(?:no\.?|number|#)?[ \t]*(\d{1,2})\b[ \t]*(?:\*\*|__)?"
    r"[ \t]*(?:[:\-–—.)|]+[ \t]*(.*?))?[ \t]*(?:\*\*|__)?[ \t]*$", re.I | re.M)
_INLINE_SLIDE = re.compile(r"\bslide\s*(\d{1,2})\s*[:\-–—]\s*", re.I)
_MD_HEAD = re.compile(r"^[ \t]*#{1,3}[ \t]+(\S.*)$", re.M)
_BULLET = re.compile(r"^([ \t]*)(?:[-*•▪◦·‣➢➤►✓✔→–]|\d{1,2}[.)]|[a-hA-H][.)])[ \t]+(.*)$")
_KEY = re.compile(
    r"^[ \t]*(?:[-*•][ \t]*)?(?:\*\*|__)?(title|heading|headline|subtitle|sub-title|tagline|speaker notes|notes?|"
    r"image|images|visual|picture|photo|layout|type|kind|design|quote|author|body|content|points|bullets|"
    r"description|text|caption|chart|data)(?:\*\*|__)?[ \t]*[:=\-–][ \t]*(.*)$", re.I)
_TABLE_ROW = re.compile(r"^\s*\|(.+)\|\s*$")


def _strip_md(s: str) -> str:
    s = re.sub(r"(\*\*|__)(.+?)\1", r"\2", s or "")
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"\1", s)
    s = re.sub(r"`([^`]+)`", r"\1", s)
    return s.strip()


def _split_head(raw: str) -> dict:
    """'**Head**: text' / 'Head: text' / 'Head – text' → {head, text}. Verbatim otherwise."""
    raw = raw.strip()
    m = re.match(r"^(?:\*\*|__)(.+?)(?:\*\*|__)\s*[:\-–—.]?\s*(.*)$", raw)
    if m and len(m.group(1).split()) <= 10:
        return {"head": _strip_md(m.group(1)).rstrip(":"), "text": _strip_md(m.group(2))}
    clean = _strip_md(raw)
    m = re.match(r"^([^:.!?]{2,60}?)\s*:\s+(.+)$", clean)
    if m and len(m.group(1).split()) <= 6 and not re.match(r"^https?$", m.group(1), re.I):
        return {"head": m.group(1).strip(), "text": m.group(2).strip()}
    m = re.match(r"^([^.!?]{2,50}?)\s+[–—-]\s+(.+)$", clean)
    if m and len(m.group(1).split()) <= 5:
        return {"head": m.group(1).strip(), "text": m.group(2).strip()}
    return {"head": "", "text": clean}


def _parse_block(num: int, header_rest: str, block: str) -> dict:
    sl: dict = {"n": num, "title": _strip_md(header_rest or "").strip(" :-–—"), "bullets": [], "_body": [],
                "_groups": [], "locked": True}
    cur_group = None
    table_rows = []
    mode = None                              # current multi-line key (notes/body/quote)
    for line in block.split("\n"):
        if not line.strip():
            mode = None if mode in ("notes",) else mode
            continue
        tr = _TABLE_ROW.match(line)
        if tr:
            cells = [c.strip() for c in tr.group(1).split("|")]
            if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
                table_rows.append([_strip_md(c) for c in cells])
            continue
        km = _KEY.match(line)
        if km:
            key, val = km.group(1).lower(), km.group(2).strip()
            if key in ("title", "heading", "headline"):
                sl["title"] = _strip_md(val)
                mode = None
            elif key in ("subtitle", "sub-title", "tagline"):
                sl["subtitle"] = _strip_md(val)
                mode = None
            elif key in ("notes", "note", "speaker notes"):
                sl["notes"] = val
                mode = "notes"
            elif key in ("image", "images", "visual", "picture", "photo"):
                sl["image_hint"] = val
                mode = None
            elif key in ("layout", "type", "kind", "design"):
                sl["layout_hint"] = val.lower()
                mode = None
            elif key == "quote":
                sl["quote"] = {"text": _strip_md(val).strip('"“”'), "author": ""}
                mode = "quote"
            elif key == "author":
                sl.setdefault("quote", {"text": "", "author": ""})["author"] = _strip_md(val)
            elif key == "caption":
                sl.setdefault("captions", []).append(_strip_md(val))
            elif key in ("chart", "data"):
                sl["_chart_raw"] = (sl.get("_chart_raw", "") + "\n" + val).strip()
                mode = "chart"
            else:                             # body/content/points/bullets/description/text
                if val:
                    sl["_body"].append(_strip_md(val))
                mode = "body"
            continue
        if mode == "notes":
            sl["notes"] = (sl.get("notes", "") + " " + line.strip()).strip()
            continue
        if mode == "chart" and re.search(r"\d", line):
            sl["_chart_raw"] += "\n" + line.strip()
            continue
        bm = _BULLET.match(line)
        if bm:
            indent = len(bm.group(1).replace("\t", "    "))
            item = _split_head(bm.group(2))
            target = cur_group["points"] if cur_group is not None else sl["bullets"]
            if indent >= 2 and target:
                prev = target[-1]
                if isinstance(prev, dict):
                    prev["text"] = (prev["text"] + ("; " if prev["text"] else "") +
                                    ((item["head"] + ": ") if item["head"] else "") + item["text"]).strip()
                else:
                    target[-1] = prev + "; " + item["text"]
            elif cur_group is not None:
                target.append(((item["head"] + ": ") if item["head"] else "") + item["text"])
            else:
                target.append(item)
            continue
        plain = _strip_md(line.strip().lstrip("#").strip())
        # "Group heading:" line → column group (comparison)
        if plain.endswith(":") and len(plain.split()) <= 6:
            cur_group = {"heading": plain.rstrip(":").strip(), "points": []}
            sl["_groups"].append(cur_group)
            continue
        if not sl["title"]:
            sl["title"] = plain
            continue
        if mode == "quote" and sl.get("quote"):
            sl["quote"]["text"] = (sl["quote"]["text"] + " " + plain).strip()
            continue
        if cur_group is not None:
            cur_group["points"].append(plain)
            continue
        sl["_body"].append(plain)
    if table_rows:
        sl["table"] = {"header": table_rows[0], "rows": table_rows[1:]}
    groups = [g for g in sl.pop("_groups") if g["points"]]
    if len(groups) >= 2:
        sl["columns"] = groups
    elif groups:                                   # a single group is just a list with a lead-in
        sl["_body"].append(groups[0]["heading"] + ":") if not sl["bullets"] else None
        sl["bullets"] += [_split_head(p) for p in groups[0]["points"]]
    body = sl.pop("_body")
    if body:
        sl["body"] = "\n".join(body)
    if sl.get("_chart_raw"):
        ch = _parse_chart(sl.pop("_chart_raw"))
        if ch:
            sl["chart"] = ch
    return sl


def _parse_chart(raw: str) -> Optional[dict]:
    """'Type: bar' + lines like 'Label: 42' or 'A=1, B=2' → chart dict (numbers verbatim)."""
    ctype = "column"
    m = re.search(r"\b(bar|column|line|pie|doughnut|donut|area)\b", raw, re.I)
    if m:
        ctype = m.group(1).lower()
    pairs = re.findall(r"([A-Za-z][\w %&/().'-]{0,40}?)\s*[:=]\s*(-?[\d,]*\.?\d+)\s*(%?)", raw)
    if len(pairs) < 2:
        return None
    unit = "%" if any(p[2] for p in pairs) else ""
    return {"type": ctype, "labels": [p[0].strip() for p in pairs],
            "series": [{"name": "", "values": [float(p[1].replace(",", "")) for p in pairs]}], "unit": unit}


def parse_user_slides(text: str) -> list[dict]:
    """Return strict slides if the text is written slide-by-slide, else []."""
    if not text or not text.strip():
        return []
    heads = list(_SLIDE_HDR.finditer(text))
    if heads and len(_INLINE_SLIDE.findall(text)) > len(heads):
        heads = []                     # "slide 1: …, slide 2: …" written on one line
    blocks = []
    if heads:
        for i, m in enumerate(heads):
            end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
            blocks.append((int(m.group(1)), m.group(2) or "", text[m.end():end]))
    else:
        inl = list(_INLINE_SLIDE.finditer(text))
        if len(inl) >= 2:
            for i, m in enumerate(inl):
                end = inl[i + 1].start() if i + 1 < len(inl) else len(text)
                seg = text[m.end():end].strip().rstrip(",;")
                # "Slide 2: Title - point, point" → title + bullets
                first, _, rest = (re.split(r"(\s[-–—]\s|\n)", seg, maxsplit=1) + ["", ""])[:3]
                pts = [p.strip() for p in re.split(r"[;\n]|,\s(?=[A-Z])", rest) if p.strip()] if rest else []
                blocks.append((int(m.group(1)), first, "\n".join(f"- {p}" for p in pts)))
        else:
            mds = list(_MD_HEAD.finditer(text))
            if len(mds) >= 3:
                for i, m in enumerate(mds):
                    end = mds[i + 1].start() if i + 1 < len(mds) else len(text)
                    blocks.append((i + 1, m.group(1), text[m.end():end]))
    if not blocks:
        return []
    slides = [_parse_block(n, h, b) for n, h, b in blocks]
    slides.sort(key=lambda s: s["n"])
    # de-duplicate slide numbers (keep order)
    for i, s in enumerate(slides):
        s["n"] = i + 1
    return slides


def slide_has_content(sl: dict) -> bool:
    return bool(sl.get("bullets") or sl.get("body") or sl.get("stats") or sl.get("steps") or sl.get("columns")
                or sl.get("table") or sl.get("chart") or sl.get("quote") or sl.get("subtitle"))


# ══════════════════════════════════════════════════════════════════════════════
#  KIND INFERENCE  (structure only — never rewrites text)
# ══════════════════════════════════════════════════════════════════════════════
_NUM = r"(?:[$€£₹¥]\s?)?\d[\d,.]*\s?(?:%|x|×|k|K|M|B|bn|mn|Mn|Bn|million|billion|crore|cr|lakh|L|\+|/\d+|hrs?|ms|s|kg|km|GW|MW|TB|GB)?\+?"
_STAT_A = re.compile(rf"^({_NUM})\s*(?:[-–—:|]\s*)?(.{{2,90}})$")
_STAT_B = re.compile(rf"^(.{{2,60}}?)\s*[:\-–—|]\s*({_NUM})$")
_DATE = re.compile(r"^(?:(?:19|20)\d{2}s?(?:\s*[-–]\s*(?:19|20)?\d{2,4})?|Q[1-4](?:\s*'?\d{2,4})?|H[12]\s*\d{2,4}|"
                   r"(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\.?(?:\s*\d{1,4})?|"
                   r"phase\s*\d+|week\s*\d+|month\s*\d+|day\s*\d+|year\s*\d+|stage\s*\d+|milestone\s*\d+|"
                   r"(?:\d{1,2}(?:st|nd|rd|th)\s+century))\b", re.I)


def _as_stat(it: dict) -> Optional[dict]:
    head, txt = it.get("head", ""), it.get("text", "")
    if head and re.fullmatch(_NUM, head.strip()):
        return {"value": head.strip(), "label": txt, "desc": ""}
    if head and re.fullmatch(_NUM, txt.strip()):
        return {"value": txt.strip(), "label": head, "desc": ""}
    full = ((head + ": ") if head else "") + txt
    m = _STAT_A.match(full.strip())
    if m and len(m.group(2).split()) <= 12:
        return {"value": m.group(1).strip(), "label": m.group(2).strip(" :-–—"), "desc": ""}
    m = _STAT_B.match(full.strip())
    if m and len(m.group(1).split()) <= 8:
        return {"value": m.group(2).strip(), "label": m.group(1).strip(), "desc": ""}
    return None


def _as_dated(it: dict) -> Optional[dict]:
    head, txt = it.get("head", ""), it.get("text", "")
    if head and _DATE.match(head) and len(head.split()) <= 4:
        rest = _split_head(txt) if txt else {"head": "", "text": ""}
        return {"date": head, "head": rest["head"], "text": rest["text"]}
    m = _DATE.match(txt)
    if m and not head:
        date = m.group(0)
        rest = txt[len(date):].strip(" :-–—,")
        r2 = _split_head(rest)
        return {"date": date, "head": r2["head"], "text": r2["text"]}
    return None


def infer_kind(sl: dict, i: int, n: int) -> str:
    hint = (sl.get("layout_hint") or "").strip().lower()
    if hint:
        for k, v in sorted(_KIND_SYNONYMS.items(), key=lambda kv: -len(kv[0])):
            if k in hint:
                return v
    title = (sl.get("title") or "").lower()
    items = [b if isinstance(b, dict) else {"head": "", "text": str(b)} for b in (sl.get("bullets") or [])]
    body = sl.get("body") or ""
    if sl.get("kind") in KINDS and sl.get("kind") not in ("content",):
        return sl["kind"]
    if i == 0 and len(items) <= 2 and len(body.split()) <= 40:
        return "title"
    if i == n - 1 and n > 2 and re.search(r"thank|questions|q\s*&\s*a|contact|let'?s connect|the end|get in touch", title):
        return "closing"
    if sl.get("table"):
        return "table"
    if sl.get("chart"):
        return "chart"
    if sl.get("quote") and sl["quote"].get("text"):
        return "quote"
    if sl.get("columns"):
        return "comparison"
    if not items and not body and sl.get("images"):
        return "image" if len(sl["images"]) == 1 else "gallery"
    if re.fullmatch(r"(agenda|outline|contents|table of contents|overview|index|topics( covered)?)", title.strip()) \
            and items and all(len((it["head"] + " " + it["text"]).split()) <= 8 for it in items):
        return "agenda"
    if not items and body and re.match(r'^["“].+["”]\s*(?:[-–—]\s*.+)?$', body.strip(), re.S) and len(body.split()) <= 60:
        return "quote"
    if 2 <= len(items) <= 6:
        stats = [_as_stat(it) for it in items]
        if sum(1 for s_ in stats if s_) >= max(2, round(len(items) * 0.75)):
            return "stats"
        dated = [_as_dated(it) for it in items]
        if 3 <= len(items) and sum(1 for d in dated if d) >= round(len(items) * 0.75):
            return "timeline"
        if re.search(r"\b(how it works|process|workflow|pipeline|methodology|procedure|steps|working|approach|flow)\b", title) \
                or all(re.match(r"^(step\s*\d+|\d+\s*[.)])", (it["head"] or it["text"]), re.I) for it in items):
            return "process"
    if len(items) > 6:
        dated = [_as_dated(it) for it in items]
        if sum(1 for d in dated if d) >= round(len(items) * 0.75):
            return "timeline"
    if re.search(r"thank you|thanks|questions\??$", title) and i == n - 1:
        return "closing"
    return "content"


def apply_structure(sl: dict, kind: str) -> dict:
    """Move a slide's existing text into the fields `kind` needs. Text is not changed."""
    sl = dict(sl)
    items = [b if isinstance(b, dict) else {"head": "", "text": str(b)} for b in (sl.get("bullets") or [])]
    if kind == "stats" and not sl.get("stats"):
        stats, rest = [], []
        for it in items:
            st = _as_stat(it)
            (stats.append(st) if st else rest.append(it))
        if stats:
            sl["stats"], sl["bullets"] = stats, rest
            if rest and not sl.get("body"):
                sl["body"] = " ".join(((r["head"] + ": ") if r["head"] else "") + r["text"] for r in rest)
                sl["bullets"] = []
    elif kind == "timeline" and not sl.get("steps"):
        steps = []
        for it in items:
            d = _as_dated(it)
            steps.append(d or {"date": it["head"], "head": "", "text": it["text"]} if it["head"] else d or
                         {"date": "", "head": "", "text": it["text"]})
        sl["steps"], sl["bullets"] = steps, []
    elif kind == "process" and not sl.get("steps") and items:
        sl["steps"], sl["bullets"] = items, []
    elif kind == "comparison" and not sl.get("columns") and items:
        half = (len(items) + 1) // 2
        sl["columns"] = [{"heading": "", "points": [((i["head"] + ": ") if i["head"] else "") + i["text"] for i in part]}
                         for part in (items[:half], items[half:])]
    elif kind == "quote" and not sl.get("quote"):
        body = sl.get("body") or (items[0]["text"] if items else "")
        m = re.match(r'^["“](.+?)["”]\s*(?:[-–—]\s*(.+))?$', body.strip(), re.S)
        sl["quote"] = {"text": m.group(1) if m else body, "author": (m.group(2) or "") if m else ""}
    elif kind == "table" and not sl.get("table") and items:
        sl["table"] = {"header": ["", ""], "rows": [[i["head"], i["text"]] for i in items]}
    elif kind == "closing" and items and not sl.get("subtitle") and not sl.get("body"):
        pass
    elif kind == "title":
        if not sl.get("subtitle"):
            if sl.get("body"):
                parts = sl["body"].split("\n", 1)
                sl["subtitle"] = parts[0]
                sl["body"] = parts[1] if len(parts) > 1 else ""
            elif items:
                sl["subtitle"] = ((items[0]["head"] + ": ") if items[0]["head"] else "") + items[0]["text"]
                items = items[1:]
                sl["bullets"] = items
        if items and not sl.get("body"):
            sl["body"] = " · ".join(((i["head"] + ": ") if i["head"] else "") + i["text"] for i in items)
            sl["bullets"] = []
    return sl


# ══════════════════════════════════════════════════════════════════════════════
#  NORMALISATION
# ══════════════════════════════════════════════════════════════════════════════
def _s(v) -> str:
    return re.sub(r"\s+", " ", str(v)).strip() if v is not None else ""


_WRAPPERS = set(KINDS) | {"fields", "data", "content", "details", "slide", "payload"}
_FIELDS = ("subtitle", "body", "bullets", "stats", "steps", "columns", "table", "chart", "quote", "notes", "items",
           "cards", "points")


def _flatten(sl: dict) -> dict:
    """LLMs love nesting: {"cards": {"bullets": […]}}, {"subtitle": {"subtitle": "…"}} → flat slide."""
    out = dict(sl)
    for _ in range(2):
        for k in list(out.keys()):
            v = out.get(k)
            if not isinstance(v, dict):
                continue
            if k in ("chart", "table", "quote") and not any(f in v for f in _FIELDS if f != k):
                inner = v.get(k)
                if isinstance(inner, dict):
                    out[k] = inner
                continue
            if k in _WRAPPERS or k in _FIELDS:
                inner = out.pop(k)
                for ik, iv in inner.items():
                    if ik == k and not isinstance(iv, dict):
                        out[ik] = iv
                    elif iv not in (None, "", [], {}) and (not out.get(ik) or ik not in out or isinstance(out.get(ik), dict)):
                        out[ik] = iv
    for k in ("subtitle", "body", "notes", "title"):
        if isinstance(out.get(k), (list, tuple)):
            out[k] = "\n".join(str(x) for x in out[k])
    if not out.get("bullets"):
        for alt in ("cards", "items", "points"):
            if isinstance(out.get(alt), list) and out[alt]:
                out["bullets"] = out[alt]
                break
    return out


def normalize_slide(sl: dict) -> dict:
    sl = _flatten(sl)
    out = {k: v for k, v in sl.items() if not k.startswith("_")}
    out["title"] = _s(out.get("title"))
    for k in ("subtitle", "notes"):
        if k in out:
            out[k] = _s(out[k])
    if "body" in out:
        out["body"] = "\n".join(_s(x) for x in str(out["body"] or "").split("\n") if _s(x))
    items = []
    for b in out.get("bullets") or []:
        if isinstance(b, str):
            b = {"head": "", "text": b}
        if isinstance(b, dict):
            h = _s(b.get("head") or b.get("bold") or b.get("header") or b.get("title"))
            t = _s(b.get("text") or b.get("desc") or b.get("description") or b.get("detail"))
            if h or t:
                items.append({"head": h, "text": t})
    out["bullets"] = items
    if out.get("steps"):
        steps = []
        for b in out["steps"]:
            if isinstance(b, str):
                b = {"text": b}
            if isinstance(b, dict):
                st = {"date": _s(b.get("date") or b.get("when") or b.get("year")),
                      "head": _s(b.get("head") or b.get("title") or b.get("header")),
                      "text": _s(b.get("text") or b.get("desc") or b.get("description"))}
                if st["head"] or st["text"] or st["date"]:
                    steps.append(st)
        out["steps"] = steps
    if out.get("stats"):
        out["stats"] = [{"value": _s(x.get("value")), "label": _s(x.get("label")), "desc": _s(x.get("desc"))}
                        for x in out["stats"] if isinstance(x, dict) and _s(x.get("value"))]
    if out.get("columns"):
        cols = []
        for c in out["columns"]:
            if isinstance(c, dict):
                pts = [(_s(p) if not isinstance(p, dict) else _s(((p.get("head") or "") + ": " if p.get("head") else "")
                                                                   + (p.get("text") or ""))) for p in c.get("points") or []]
                cols.append({"heading": _s(c.get("heading") or c.get("title")), "points": [p for p in pts if p]})
        out["columns"] = cols
    if isinstance(out.get("quote"), str):
        out["quote"] = {"text": out["quote"], "author": ""}
    if out.get("subtitle") and out["subtitle"].strip().lower() == out["title"].strip().lower():
        out["subtitle"] = ""            # models love echoing the title as a subtitle
    kind = out.get("kind")
    if kind not in KINDS:
        kind = _KIND_SYNONYMS.get(str(kind or "").lower(), "content")
    # downgrade kinds whose data is missing
    need = {"stats": "stats", "comparison": "columns", "table": "table", "chart": "chart", "quote": "quote"}
    if kind in need and not out.get(need[kind]):
        if kind in ("stats", "comparison", "quote", "table"):
            out = apply_structure(out, kind)
        if not out.get(need[kind]):
            kind = "content"
    if kind in ("process", "timeline") and not out.get("steps") and out["bullets"]:
        out = apply_structure(out, kind)
    if kind in ("process", "timeline") and not out.get("steps"):
        kind = "content"
    if kind in ("image", "gallery") and not out.get("images"):
        kind = "content"
    if kind == "sections" and not out.get("sections"):
        kind = "content"
    out["kind"] = kind
    out["images"] = [p for p in out.get("images") or [] if p]
    return out


def finalize_slides(slides: list[dict]) -> list[dict]:
    out = [normalize_slide(s) for s in slides]
    sec = 0
    for s in out:
        if s["kind"] == "section":
            sec += 1
            s["_section_no"] = sec
    return out


# ══════════════════════════════════════════════════════════════════════════════
#  CONTENT ARCHITECT  (user content → designed slide structure, wording kept)
# ══════════════════════════════════════════════════════════════════════════════
def repair_text(t: str) -> str:
    """Restore structure that copy-paste destroyed ("Title and OverviewEvent: …", "Features:Engine: …")."""
    if not t:
        return t
    t = t.replace("\r\n", "\n").replace(" ", " ")
    # "…text.Slide 3: …" / "text Slide 3 - …" → marker on its own line
    t = re.sub(r"(?<=\S)[ \t]*(?=\b[Ss]lide\s*\d{1,2}\s*[:\-–—])", "\n", t)

    words = re.findall(r"[A-Za-z][A-Za-z0-9]+", t)
    freq: dict[str, int] = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1

    def _glued(m):
        left, lab = m.group(1), m.group(2)
        joined = left + re.match(r"[A-Za-z0-9]+", lab).group(0)
        # a real camel-case name (KarmaSkill, MoSPI, iGOT) shows up elsewhere or has a tiny left part
        if freq.get(joined, 0) >= 2 or sum(ch.islower() for ch in left) < 3 or not 1 <= len(lab.split()) <= 7:
            return m.group(0)
        return left + "\n" + lab
    # "OverviewEvent:" → "Overview\nEvent:"
    t = re.sub(r"\b([A-Za-z]*[a-z0-9\)\]%])([A-Z][A-Za-z0-9&/'’\-\(\) ]{1,60}?:)(?=\s|[A-Z])", _glued, t)
    # ". Hybrid AI Course Recommender: Fuses …" / ". Before vs. After X:" → the label starts a new line
    cuts = []
    for m in re.finditer(r"([.;!?])[ \t]+(?=[A-Za-z])", t):
        if re.search(r"(?:\bvs|\be\.g|\bi\.e|\betc|\bNo|\bDr|\bMr|\bMs|\bSt|\bapprox|\bincl)\.$",
                     t[max(0, m.start() - 6):m.start() + 1], re.I):
            continue
        lm = re.match(r"((?:[^\n:.!?]|\bvs\.)+?):(?=\s|[A-Za-z]|$)", t[m.end():m.end() + 90])
        if lm and len(lm.group(1).split()) <= 7:
            cuts.append((m.start(1) + 1, m.end()))
    for a, b in reversed(cuts):
        t = t[:a] + "\n" + t[b:]
    # "Key Features:Evidence-Based" → "Key Features:\nEvidence-Based"
    t = re.sub(r"(?<=[A-Za-z\)]):(?=[A-Za-z])", ":\n", t)
    return re.sub(r"\n{3,}", "\n\n", t)


_INSTR_LINE = re.compile(
    r"^\s*(?:[-*•]\s*)?(?:please\s+|also\s+|and\s+|kindly\s+|note\s*[:\-]\s*)*"
    r"(use|create|make|put|add|keep|place|include|don'?t|do not|set|apply|give|generate|insert|show|arrange|design|"
    r"follow|limit|only|ensure|match|copy|mimic)\b.*\b(ppt|slides?|images?|photos?|pictures?|screenshots?|theme|"
    r"colou?rs?|fonts?|layout|design|format|deck|presentation|style)\b", re.I)
_IMG_WORD = r"\b(images?|photos?|pics?|pictures?|screenshots?|screen ?shots?|snaps?|logos?|mockups?)\b"
_META_VERB = (r"\b(come|comes|go|goes|put|place|placed|add|added|use|used|insert|show|shown|appear|be|keep|kept|"
              r"include|included|attach|attached|upload|uploaded|uploading|should|must|need|needs|want|has to|have to)\b")
_ORD_SLIDE = {"first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5, "sixth": 6, "seventh": 7, "eighth": 8,
              "ninth": 9, "tenth": 10, "1st": 1, "2nd": 2, "3rd": 3, "4th": 4, "5th": 5, "6th": 6, "7th": 7,
              "8th": 8, "9th": 9, "10th": 10, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
              "seven": 7, "eight": 8, "nine": 9, "ten": 10}


def _is_instruction(p: str) -> bool:
    """A sentence that talks ABOUT the deck (images, slide count, theme…) rather than being slide content."""
    s = p.strip()
    if not s or len(s.split()) > 45 or re.match(r"^\s*slide\s*\d", s, re.I):
        return False
    # "Label: text" is content — unless the label itself is a meta label
    lab = re.match(r"^([^:]{2,40}):\s", s)
    if lab and not re.search(r"\b(note|instructions?|important|images?|photos?|format|design|theme|layout)\b",
                             lab.group(1), re.I):
        return False
    about_deck = re.search(r"\b(ppt|pptx|slides?|deck|presentation|powerpoint)\b", s, re.I)
    if _INSTR_LINE.match(s) and (about_deck or (len(s.split()) <= 8 and re.search(r"\b(theme|colou?rs?|fonts?|style)\b",
                                                                                 s, re.I))):
        return True
    if re.search(_IMG_WORD, s, re.I) and re.search(r"\bslides?\s*\d|\b(first|second|third|fourth|fifth|sixth|last|"
                                                  r"title|1st|2nd|3rd|[4-9]th)\s+slide\b", s, re.I) and \
            not re.search(r"\b(users?|customers?|farmers?|patients?|students?|citizens?)\b", s, re.I):
        return True                                    # "first image on slide 3", "pics → second slide"
    if re.search(_IMG_WORD, s, re.I) and re.search(_META_VERB, s, re.I) and \
            re.search(r"\b(slides?|section|uploaded|uploading|attached|attaching|i (?:am |have )?(?:upload|attach))", s, re.I):
        return True                                    # "both of the images uploaded have to come under … slide 2"
    if about_deck and re.search(r"\b(\d{1,2}|one|two|three|four|five|six|seven|eight|nine|ten)\s+slides?\b", s, re.I) \
            and re.search(r"\b(create|make|generate|build|keep|limit|only|total|of)\b", s, re.I):
        return True
    return False


def split_instructions(text: str) -> tuple[str, list[str]]:
    """Pull instruction sentences ("use the images in slide 2 only", "both images go in the prototype section of
    slide 2", "make 6 slides") out of the content, wherever they appear."""
    keep, instr = [], []
    for line in (text or "").split("\n"):
        parts = re.split(r"(?<=[.!?])\s+", line)
        kept = []
        for p in parts:
            if _is_instruction(p):
                instr.append(p.strip())
            else:
                kept.append(p)
        if any(k.strip() for k in kept) or not line.strip():
            keep.append(" ".join(kept))
    return "\n".join(keep), instr


def _slide_ref(seg: str, titles: list[str]) -> Optional[int]:
    """'slide 2' / 'second slide' / 'slide two' / 'the solution slide' → slide number."""
    m = re.search(r"\bslides?\s*(?:no\.?|number|#)?\s*(\d{1,2})\b", seg, re.I)
    if m:
        return int(m.group(1))
    m = re.search(r"\bslide\s+(one|two|three|four|five|six|seven|eight|nine|ten)\b", seg, re.I)
    if m:
        return _ORD_SLIDE[m.group(1).lower()]
    m = re.search(r"\b(first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|1st|2nd|3rd|[4-9]th|10th)"
                  r"\s+slide\b", seg, re.I)
    if m:
        return _ORD_SLIDE[m.group(1).lower()]
    if re.search(r"\b(last|final|closing)\s+slide\b", seg, re.I) and titles:
        return len(titles)
    if re.search(r"\b(title|cover|opening)\s+slide\b", seg, re.I):
        return 1
    m = re.search(r"\b(?:the|on|in|to)\s+([\w &/-]{3,40}?)\s+slide\b", seg, re.I)
    if m and titles:                                     # "the solution slide" → best title match
        words = set(re.findall(r"[a-z]{3,}", m.group(1).lower())) - {"the", "and", "for"}
        best, best_k = 0, None
        for k, t in enumerate(titles):
            sc = len(words & set(re.findall(r"[a-z]{3,}", (t or "").lower())))
            if sc > best:
                best, best_k = sc, k + 1
        return best_k
    return None


def parse_instructions(lines: list[str], n_images: int, titles: Optional[list] = None) -> dict:
    """Deterministic reading of the user's instructions.
    image_rules: [{"images": "all" | [0-based idx…], "slide": n, "section": "Prototype" | ""}]"""
    titles = titles or []
    txt = " ".join(lines)
    out: dict = {"count": slide_count(txt), "image_slides": {}, "images_only_on": None, "image_section": {},
                 "image_rules": [], "text": txt, "image_sentences": []}
    ords = {"first": 0, "1st": 0, "second": 1, "2nd": 1, "third": 2, "3rd": 2, "fourth": 3, "4th": 3, "fifth": 4}
    sents = []
    for sent in re.split(r"(?<=[.!?;])\s+|\n", txt):
        if len(re.findall(r"\bslides?\s*\d|\b\w+\s+slide\b", sent, re.I)) >= 2:      # two rules in one sentence
            sents += [x for x in re.split(r",|\band\b|\bthen\b", sent) if x.strip()]
        else:
            sents.append(sent)
    for sent in sents:
        if not re.search(_IMG_WORD, sent, re.I):
            continue
        out["image_sentences"].append(sent.strip())
        slide = _slide_ref(sent, titles)
        sec = ""
        m = re.search(r"(.{1,80}?)\s+(?:section|part|block|area|box|panel|column)\b", sent, re.I)
        if m:                                           # "...come under prototype section" → "prototype"
            pre = re.split(r"\b(?:under|into|inside|within|in|on|to|at|of)\b", m.group(1), flags=re.I)[-1]
            sec = re.sub(r"^(?:the|a|an)\s+", "", pre.strip(" '\"“”"), flags=re.I).strip()
            if not re.search(r"[A-Za-z]", sec) or len(sec.split()) > 5:
                sec = ""
        which: object = "all"
        m1 = re.search(r"\b(first|second|third|fourth|fifth|1st|2nd|3rd|4th)\s+(?:image|photo|pic|picture|screenshot)",
                       sent, re.I)
        m2 = re.search(r"\b(?:image|photo|pic|picture|screenshot)\s*(?:no\.?|number|#)?\s*(\d)\b", sent, re.I)
        if m1:
            which = [ords[m1.group(1).lower()]]
        elif m2 and not re.search(r"\bslides?\s*" + m2.group(1) + r"\b", sent, re.I):
            which = [int(m2.group(1)) - 1]
        if slide or sec:
            out["image_rules"].append({"images": which, "slide": slide, "section": sec})
    for rule in out["image_rules"]:
        if not rule["slide"]:
            continue
        if rule["images"] == "all":
            out["images_only_on"] = rule["slide"]
        else:
            for i in rule["images"]:
                out["image_slides"][i] = rule["slide"]
        if rule["section"]:
            out["image_section"][rule["slide"]] = rule["section"]
    return out


def interpret_image_instructions(sentences: list[str], titles: list[str], n_images: int,
                                 image_descs: Optional[list] = None) -> list[dict]:
    """LLM fallback for phrasings the regexes can't resolve. Returns image_rules (same shape as above)."""
    if not sentences or not n_images:
        return []
    user = "\n".join([
        "SLIDES:\n" + "\n".join(f"{i + 1}. {t}" for i, t in enumerate(titles)),
        f"UPLOADED IMAGES: {n_images}" + ("\n" + "\n".join(f"image {i + 1}: {d}" for i, d in enumerate(image_descs or [])
                                                          if d) if image_descs else ""),
        "USER INSTRUCTIONS ABOUT IMAGES:\n" + "\n".join(sentences),
        'Return JSON {"rules": [{"images": "all" or [image numbers starting at 1], "slide": <slide number>, '
        '"section": "section name the user mentioned or empty"}]}. Only rules the user actually stated.',
    ])
    try:
        data = _llm_json("You convert a user's instructions about where to put images in a presentation into "
                         "structured rules. Output valid JSON only.", user, max_tokens=600, temperature=0.0)
    except Exception:
        return []
    rules = []
    for rr in data.get("rules") or []:
        if not isinstance(rr, dict):
            continue
        try:
            slide = int(rr.get("slide"))
        except Exception:
            continue
        imgs = rr.get("images")
        which = "all" if imgs in ("all", None) or not isinstance(imgs, list) else \
            [int(i) - 1 for i in imgs if str(i).isdigit() and 1 <= int(i) <= n_images]
        if 1 <= slide <= max(1, len(titles)):
            rules.append({"images": which or "all", "slide": slide, "section": _s(rr.get("section"))})
    return rules


def raw_slide_blocks(text: str) -> list[tuple[int, str, str]]:
    """[(n, heading, raw content)] split on 'Slide N:' markers of repaired text."""
    heads = list(_SLIDE_HDR.finditer(text))
    out = []
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        out.append((int(m.group(1)), (m.group(2) or "").strip(), text[m.end():end].strip()))
    return out


def needs_architect(blocks: list[tuple[int, str, str]]) -> bool:
    """Rich / paragraph-style content needs real restructuring, not a bullet dump."""
    for _, _, body in blocks:
        words = len(body.split())
        bullets = sum(1 for l in body.split("\n") if _BULLET.match(l))
        if words > 45 or (words > 20 and bullets == 0):
            return True
    return False


_SYS_ARCH = ("You are a principal presentation designer who turns a founder's raw notes into a world-class pitch deck "
             "(better than Gamma). You restructure; you NEVER invent content. Output valid JSON only.")

_ARCH_GUIDE = """SLIDE TYPES
- "title": opening slide. title = the product/project name if the content gives one (else the topic, ≤ 6 words);
  subtitle = tagline or event; lead = one short sentence; sections = [{"heading": "Details", "style": "fields",
  "items": [{"head": "Problem Statement ID", "text": "26101"}, …]}] for IDs / theme / category / team facts.
- "sections": a rich composed slide = "lead" (the single most important sentence, ≤ 32 words) + 2–4 sections.
  Section styles:
    cards     – 3–8 named features/points: head = the name (2–6 words), text = 8–24 words
    list      – short points without names
    steps     – an ordered process / pipeline (3–6 steps: head + short text)
    stats     – numbers: items {"value": "46 lakh", "label": "central employees", "desc": "optional"}
    fields    – key: value facts
    table     – comparisons / before-after: {"header": ["Aspect","Before","After"], "rows": [[…]]}
    paragraph – only when nothing else fits
  Mark ONE section "highlight": true for differentiators / benefits / why-us (bottom band, 3–5 short cards,
  optional "lead" tagline for the band).
  If the slide has images, add ONE section {"heading": "Prototype" (or what the content calls them),
  "style": "gallery", "items": [one caption per image, in order: head = screen/component name, text ≤ 8 words]}
  using the content's own words about those screens/components.
- "stats" / "timeline" / "process" / "comparison" / "table" / "quote" / "closing": use only when the slide is
  purely that one thing (same fields as a section of that style: stats → "stats", timeline/process → "steps",
  comparison → "columns", table → "table").
RULES
1. Use ONLY the user's content. Keep their wording: you may split sentences into items, drop filler words
   ("Utilizes a", "It also") and trim, but never add facts, numbers, names, technologies or claims.
2. Keep every concrete fact (numbers, names, technologies, standards) somewhere on the slide.
3. Wrap 1–3 key phrases per item (and 1–2 in the lead) in **double asterisks** — they render bold.
4. Section headings: 1–4 words, Title Case. Slide titles: the user's heading, ≤ 7 words.
5. Aim for a designed, scannable slide: no item longer than 26 words; split long paragraphs into cards/steps.
6. Every slide gets "notes": 2 sentences the presenter can say (from the content).
7. Never repeat: a fact used in the lead or title must not get its own section/card again (e.g. no
   "Product Name" section when the product is the title and the overview is the lead)."""


_CONNECTORS = set("with that this these those from into using uses used which their there than then also "
                  "while where when each every across over under about through within without other more most "
                  "such only very enables enabling provides provide allows allowing helps help make makes".split())


def _tok(s: str) -> list[str]:
    s = re.sub(r"(?<=\w)[-‑–](?=\w)", "", plain_md(s).lower())          # micro-services == microservices
    return [w[:6] for w in re.findall(r"[a-z0-9]+", s)
            if (len(w) >= 4 or w.isdigit()) and w not in _CONNECTORS]


def plain_md(s: str) -> str:
    return re.sub(r"\*\*(.+?)\*\*", r"\1", s or "")


def _spec_texts(sl: dict) -> list[str]:
    out = [sl.get("lead") or "", sl.get("subtitle") or ""]
    for sec in sl.get("sections") or []:
        if not isinstance(sec, dict):
            continue
        out.append(sec.get("lead") or "")
        for it in sec.get("items") or []:
            if isinstance(it, dict):
                out += [str(it.get(k) or "") for k in ("head", "text", "value", "label", "desc")]
            else:
                out.append(str(it))
        for row in sec.get("rows") or []:
            out += [str(c) for c in row] if isinstance(row, (list, tuple)) else []
    for k in ("stats", "steps", "columns", "bullets"):
        out.append(json.dumps(sl.get(k) or "", ensure_ascii=False))
    return [x for x in out if x]


def extractive_ok(sl: dict, source: str, min_ratio: float = 0.82) -> bool:
    """True if the slide only re-uses the user's words (≥ min_ratio of tokens) and invents no numbers."""
    src = set(_tok(source))
    toks = [w for s in _spec_texts(sl) for w in _tok(s)]
    if not toks:
        return False
    nums = [w for w in toks if w.isdigit()]
    if any(n not in src for n in nums):
        return False
    return sum(1 for w in toks if w in src) / len(toks) >= min_ratio


def sections_fallback(n: int, heading: str, raw: str) -> dict:
    """Deterministic structure: 'Label:' lines start sections, 'Head: text' lines become cards."""
    secs, cur, lead = [], None, ""
    for line in [l.strip() for l in raw.split("\n") if l.strip()]:
        line = re.sub(r"^[-*•▪◦·]\s*", "", line)
        m = re.match(r"^((?:[^:.!?]|\bvs\.|\be\.g\.)(?:[^:!?]|\bvs\.){1,60}?):\s*(.*)$", line)
        if m and not m.group(2) and len(m.group(1).split()) <= 6:
            cur = {"heading": m.group(1).strip(), "style": "cards", "items": []}
            secs.append(cur)
            continue
        if m and len(m.group(1).split()) <= 7:
            item = {"head": m.group(1).strip(), "text": m.group(2).strip()}
        elif not lead and not secs:
            lead = line
            continue
        else:
            item = {"head": "", "text": line}
        if cur is None:
            cur = {"heading": "", "style": "cards", "items": []}
            secs.append(cur)
        # a run of one-word labels (Collect / Analyse / Explain) is a pipeline; when multi-word labels
        # follow, they are separate components, not more steps → new (unnamed) group
        prev = [len(i["head"].split()) for i in cur["items"] if i["head"]]
        if item["head"] and len(prev) >= 2 and all(p == 1 for p in prev) and len(item["head"].split()) >= 2:
            cur = {"heading": "", "style": "cards", "items": []}
            secs.append(cur)
        cur["items"].append(item)
    for sec in secs:
        if sec["items"] and all(not i["head"] for i in sec["items"]):
            sec["style"] = "list"
        elif len(sec["items"]) >= 3 and all(i["head"] and len(i["head"].split()) == 1 for i in sec["items"]):
            sec["style"] = "steps"                        # Collect → Analyse → Explain
    return {"n": n, "kind": "sections" if secs else "content", "title": heading, "lead": lead, "sections": secs,
            "body": lead if not secs else ""}


def deck_facts(text: str) -> str:
    """Names worth knowing on every slide (product, team, event) — pulled verbatim from the content."""
    facts = []
    for rx in (r"\b(?:product|project|app|platform|solution|brand|startup)\s+name\s*(?:is|:|-)\s*([^\n.;]{2,60})",
               r"\bteam\s+name\s*(?:is|:|-)\s*([^\n.;,]{2,40})", r"\bevent\s*(?:is|:|-)\s*([^\n.;]{2,60})"):
        m = re.search(rx, text, re.I)
        if m:
            facts.append(m.group(0).strip())
    return "; ".join(facts)


def _missing_parts(sl: dict, body: str) -> list[str]:
    """Labelled parts of the user's content ('Skill Gaps: …', 'Before vs. After …:') absent from the design."""
    out_toks = set(w for s in _spec_texts(sl) for w in _tok(s))
    for sec in sl.get("sections") or []:
        if isinstance(sec, dict):
            out_toks |= set(_tok(str(sec.get("heading") or "")))
    missing = []
    for lab, val in re.findall(r"^([^:\n]{2,70}):[ \t]*(.*)$", body, re.M):
        ws = [w for w in _tok(val)[:16]] if val.strip() else [w for w in _tok(lab) if not w.isdigit()]
        if len(ws) >= 2 and sum(1 for w in ws if w in out_toks) / len(ws) < 0.45:
            missing.append(lab.strip())
    return missing


def _complete_from_source(sl: dict, n: int, heading: str, body: str) -> tuple[dict, int]:
    """Guarantee no content loss: labelled parts of the user's text that the designed slide still lacks are
    appended verbatim (as the deterministic parser structures them)."""
    def _copy_sec(x):
        items = x.get("items") or []
        if isinstance(items, dict):                       # a table sent as {"header": …, "rows": …}
            return dict(x, style="table", header=items.get("header") or x.get("header") or [],
                        rows=items.get("rows") or x.get("rows") or [], items=[])
        if isinstance(x.get("table"), dict):              # … or as {"table": {…}}
            return dict(x, style="table", header=x["table"].get("header") or [], rows=x["table"].get("rows") or [],
                        items=list(items))
        return dict(x, items=list(items))
    sl = dict(sl)
    sl["sections"] = [_copy_sec(x) for x in (sl.get("sections") or []) if isinstance(x, dict)]
    miss = set(_missing_parts(sl, body))                  # measured on the normalised slide (tables included)
    if not miss:
        return sl, 0
    fb = sections_fallback(n, heading, body)
    add, count = [], 0
    by_head = {(x.get("heading") or "").strip().lower(): x for x in sl["sections"]}
    for sec in fb.get("sections") or []:
        if sec.get("heading") and sec["heading"] in miss:
            items = sec["items"]                          # the whole group is missing
        else:
            items = [it for it in sec["items"] if it.get("head") in miss]
        if not items:
            continue
        count += len(items)
        rest = []
        for it in items:
            home = by_head.get((it.get("head") or "").strip().lower())
            if home is not None:                          # "Architecture Stack: …" → into the designer's own group
                home["items"].append({"head": "", "text": it.get("text", "")})
                continue
            # the designer condensed this part into an existing card → restore the user's full wording there
            src = set(_tok((it.get("head") or "") + " " + (it.get("text") or "")))
            best, best_sc = None, 0.0
            for x in sl["sections"]:
                for d in x["items"]:
                    if not isinstance(d, dict):
                        continue
                    dt = set(_tok(" ".join(str(d.get(k) or "") for k in ("head", "text", "value", "label", "desc"))))
                    sc = len(src & dt) / max(1, len(dt))   # share of the card that comes from this part
                    if sc > best_sc:
                        best, best_sc = d, sc
            if best is not None and best_sc >= 0.5:
                best["head"] = best.get("head") or it.get("head", "")
                best["text"] = it.get("text", "")
                best.pop("value", None), best.pop("label", None), best.pop("desc", None)
            else:
                rest.append(it)
        if rest:
            add.append({"heading": sec.get("heading") or "", "style": sec.get("style", "cards"),
                        "highlight": False, "lead": "", "items": rest})
    if count:
        sl["sections"] = sl["sections"] + add
        if sl.get("kind") not in ("sections", "title"):
            sl["kind"] = "sections"
    return sl, count


def architect_slides(blocks: list[tuple[int, str, str]], purpose: str, images_per_slide: dict,
                     deck_hint: str = "", progress=None, image_sections: Optional[dict] = None) -> list[dict]:
    """LLM restructures each slide's raw content (wording kept, verified); deterministic fallback per slide."""
    say = progress or (lambda m: None)
    overview = "\n".join(f"{n}. {h}" for n, h, _ in blocks)
    facts = deck_facts(deck_hint)
    chunks = [blocks[i:i + 2] for i in range(0, len(blocks), 2)]
    results: dict[int, dict] = {}

    def ask(chunk, extra=""):
        parts = []
        for n, h, body in chunk:
            k = images_per_slide.get(n, 0)
            sec = (image_sections or {}).get(n, "")
            img_note = (f"images on this slide: {k}" + (f" — the user wants them in the \"{sec}\" section: make that "
                                                        f"the gallery section (heading \"{sec.title()}\")" if sec else "")
                        + "\n") if k else ""
            parts.append(f"[slide {n}] heading: {h}\n" + img_note
                         + f"content:\n{body[:5000]}")
        user = "\n\n".join([
            f"PURPOSE: {purpose}\nDECK FACTS (verbatim from the content): {facts or '—'}\nALL SLIDES:\n{overview}",
            _ARCH_GUIDE,
            "EXTRA: the title slide's title is the product/project name from DECK FACTS when there is one. "
            "\"subtitle\" is ONLY for the title slide — leave it empty on other slides.",
            "SLIDES TO DESIGN:\n" + "\n\n".join(parts),
            extra,
            'Return JSON: {"slides": [{"n": <number>, "kind": "...", "title": "...", "subtitle": "...", "lead": "...", '
            '"sections": [{"heading": "...", "style": "...", "highlight": false, "lead": "", "items": [...]}], '
            '"notes": "..."}]}',
        ])
        return _llm_json(_SYS_ARCH, user, max_tokens=6500, temperature=0.3)

    def run(chunk):
        return chunk, ask(chunk)

    retry = []
    with ThreadPoolExecutor(max_workers=2) as ex:
        futs = [ex.submit(run, c) for c in chunks]
        for f in as_completed(futs):
            try:
                chunk, data = f.result()
                got = {s.get("n"): s for s in data.get("slides") or [] if isinstance(s, dict)}
                for n, h, body in chunk:
                    sl = got.get(n)
                    if sl and extractive_ok(sl, h + "\n" + body + "\n" + deck_hint):
                        results[n] = sl
                        miss = _missing_parts(sl, body)
                        if miss and len(miss) >= 1:
                            retry.append(((n, h, body), miss))
                    else:                           # rewrote the user's words (or missing) → one strict retry
                        retry.append(((n, h, body), None))
                say(f"🧩 Designed slides {', '.join(str(c[0]) for c in chunk)}")
            except Exception as e:
                say(f"⚠️ Designer pass failed ({e}); structuring those slides directly.")
    def _retry(item):
        blk, miss = item
        n, h, body = blk
        if miss:
            note = ("YOU DROPPED THESE PARTS LAST TIME — they MUST appear on the slide (e.g. as their own section "
                    "or table): " + " | ".join(miss))
        else:
            note = ("LAST TIME YOU REWROTE THE USER'S WORDS. Copy phrases exactly from the content — only split, "
                    "trim filler and add ** around key phrases. Do not paraphrase or summarise.")
        try:
            data = ask([blk], note)
            sl = next((s for s in data.get("slides") or [] if isinstance(s, dict)), None)
            if sl and extractive_ok(sl, h + "\n" + body + "\n" + deck_hint) and \
                    (not miss or len(_missing_parts(sl, body)) < len(miss)):
                return n, sl, None
            return n, None, "still not faithful"
        except Exception as e:
            return n, None, str(e)

    if retry:
        say(f"🔁 Refining slide(s) {', '.join(str(b[0][0]) for b in retry)} (keeping your exact wording / "
            f"adding parts that were left out)…")
        with ThreadPoolExecutor(max_workers=2) as ex:
            for n, sl, err in ex.map(_retry, retry):
                if sl:
                    results[n] = sl
                elif n not in results:
                    say(f"⚠️ Slide {n}: using your text as-is ({err}).")
    out = []
    for n, h, body in blocks:
        sl = results.get(n)
        if sl:
            sl, added = _complete_from_source(sl, n, h, body)
            if added:
                say(f"🧷 Slide {n}: restored {added} part(s) the designer left out, in your own words.")
        else:
            sl = sections_fallback(n, h, body)
        sl["n"] = n
        sl["title"] = plain_md(sl.get("title") or h) or h
        if sl.get("kind") == "title":                  # "KarmaSkill by Team Karmic" → "KarmaSkill" (team is in details)
            m = re.match(r"^(.{2,40}?)\s+by\s+(?:team\s+)?(\S.{1,40})$", sl["title"], re.I)
            if m:
                sl["title"] = m.group(1).strip()
        sl["locked"] = True
        out.append(sl)
    return out


# ══════════════════════════════════════════════════════════════════════════════
#  GENERATION
# ══════════════════════════════════════════════════════════════════════════════
_DENSITY_RULES = {
    "light": ("NORMAL presentation → MINIMAL text, big ideas. content/cards: 3-4 items; each item = a 2-4 word "
              "head + text of at most 12 words. Optional lead sentence ≤ 15 words. Never write paragraphs."),
    "balanced": ("Balanced academic/business deck. 3-5 items per slide; head 2-5 words + text of 12-20 words. "
                 "Concrete facts, examples, definitions. Lead sentence ≤ 22 words."),
    "dense": ("HACKATHON / PITCH-GRADE deck → information-rich but scannable. 4-6 items per slide; head 2-5 words "
              "+ text of 15-28 words with concrete specifics (numbers, named technologies, mechanisms, outcomes). "
              "Prefer cards / stats / process / comparison / table over plain lists."),
}
_PURPOSE_RULES = {
    "hackathon": ("Hackathon/pitch story: title → problem (with real stats) → why existing solutions fail → our "
                  "solution → how it works (process) → key features (cards) → tech stack/architecture (cards or table) "
                  "→ impact & metrics (stats) → comparison vs alternatives → business model / feasibility → "
                  "roadmap (timeline) → team → closing with a clear ask. Use the 'sections' kind for the 2-4 densest "
                  "slides (solution, architecture, feasibility, impact)."),
    "academic": ("Academic story: title → agenda (if ≥8 slides) → introduction/background → key concepts → "
                 "details/mechanisms (process, comparison, table) → applications/case study → advantages & "
                 "limitations → future scope → conclusion → closing (Thank you / Questions)."),
    "business": ("Business story: title → executive summary → context/market (stats, chart) → problem/opportunity "
                 "→ strategy/solution → plan (process/timeline) → financials/metrics → risks → next steps → closing."),
    "general": ("Engaging story: title → hook/why it matters → core ideas (varied layouts) → evidence/examples → "
                "implications → conclusion → closing."),
}
_KIND_GUIDE = """AVAILABLE SLIDE KINDS (pick the one that fits the idea, not a default):
- title: opening slide (slide 1 only)
- agenda: list of sections (only if the deck has 8+ slides)
- section: a divider between parts (only for 12+ slide decks)
- content: headline + a few points (optionally one lead sentence)
- cards: 3-6 parallel ideas (features, benefits, pillars, types) each with a short head
- stats: 2-4 BIG numbers with labels — ONLY with real, credible figures
- process: 3-5 sequential steps (how it works, methodology, workflow)
- timeline: 3-6 dated milestones (history, evolution, roadmap)
- comparison: 2-3 columns contrasting options (before/after, us vs them, pros/cons, types)
- table: structured rows (specs, feature matrix, comparison of many attributes)
- chart: a numeric series (trend, market size, shares) — ONLY with real/credible numbers
- quote: one real, attributable quotation
- closing: final slide (thank you / call to action / questions)
- sections: a rich composed slide (lead sentence + 2-3 titled groups of cards / steps / stats / table, optional
  highlight band) — the best choice for dense hackathon/pitch slides (solution, architecture, feasibility, impact)"""

_SCHEMA = """FIELDS PER KIND (fill only what the kind needs):
title:      {"subtitle": "one crisp line", "body": "presenter / team / date ONLY if the user gave them, else empty"}
agenda:     {"bullets": [{"head": "section name", "text": ""}]}
section:    {"subtitle": "one line"}
content:    {"body": "optional one-sentence lead or empty", "bullets": [{"head": "2-4 words", "text": "..."}]}
cards:      {"bullets": [{"head": "2-4 words", "text": "..."}]}
stats:      {"stats": [{"value": "47%", "label": "2-5 words", "desc": "context + source/year"}], "body": ""}
process:    {"steps": [{"head": "2-3 words", "text": "..."}]}
timeline:   {"steps": [{"date": "2019", "head": "2-4 words", "text": "..."}]}
comparison: {"columns": [{"heading": "...", "points": ["...", "..."]}]}
table:      {"table": {"header": ["...", "..."], "rows": [["...", "..."]]}}
chart:      {"chart": {"type": "column|bar|line|pie|doughnut", "labels": ["..."], "series": [{"name": "...", "values": [1, 2]}], "unit": "%|$|"}, "bullets": [{"head": "", "text": "takeaway"}]}
quote:      {"quote": {"text": "...", "author": "..."}}
closing:    {"subtitle": "key takeaway or call to action", "bullets": [only contact details the USER gave; else []]}
sections:   {"lead": "one key sentence with **bold** key words", "sections": [{"heading": "2-4 words", "style":
            "cards|list|steps|stats|table", "highlight": false, "items": [{"head": "2-5 words", "text": "8-22 words,
            **bold** key phrase"}]}]}  (mark one group "highlight": true for differentiators/benefits)
Every slide ALSO gets "notes": 2-3 sentences the presenter can say.
Put these fields DIRECTLY on the slide object (flat, e.g. {"n": 3, "kind": "cards", "title": "…", "bullets": […],
"notes": "…"}); never nest them under the kind name."""


_GROUND_RULES = (
    "FACT DISCIPLINE (most important rule): every number, percentage, money amount, year/date, ranking, capacity, "
    "named report/study/survey and every quote MUST be copied from the FACTS listed for that slide (or the user's "
    "source material). If the facts don't give a figure, write the point qualitatively with NO number. Never "
    "compute new numbers (no sums, averages, growth rates), never round differently, never invent people, quotes, "
    "organisations, programmes, sources or URLs.")


def _outline_prompt(req, purpose, density, count, source, fixed, images, facts=None, grounded=False) -> str:
    cnt = (f"EXACTLY {count} slides (including title and closing)." if count else
           {"light": "7 to 9 slides.", "balanced": "9 to 11 slides.", "dense": "10 to 12 slides."}[density])
    parts = [f"REQUEST: {req}", f"PURPOSE: {purpose}. {_PURPOSE_RULES.get(purpose, _PURPOSE_RULES['general'])}",
             f"DENSITY: {_DENSITY_RULES[density]}", f"SLIDE COUNT: {cnt}"]
    if source:
        parts.append("SOURCE MATERIAL (build the deck ONLY from these facts; do not invent numbers):\n" + source[:9000])
    if grounded:
        if facts:
            from app.services.ppt_research import relevant_facts
            top = relevant_facts(facts, req, 60) or facts[:60]
            top += [f for f in facts if f not in top][:max(0, 60 - len(top))]
            parts.append("VERIFIED FACTS (from real sources — the ONLY allowed origin of figures, dates, named "
                         "reports and quotes):\n" + "\n".join(f"{f['id']}: {f['fact'][:170]}" for f in top))
        elif not source:
            parts.append("NO VERIFIED FACTS ARE AVAILABLE: plan a conceptual, qualitative deck. Do NOT plan stats, "
                         "chart, table, timeline or quote slides.")
    if fixed:
        parts.append("FIXED SLIDES — keep these titles, order and count exactly; only choose a kind and goal:\n" +
                     "\n".join(f"{s['n']}. {s['title']}" for s in fixed))
    if images:
        parts.append("USER IMAGES (assign each index to the ONE slide where it fits best via \"image\"; the title "
                     "slide may take a cover photo):\n" + "\n".join(f"[{i}] {d}" for i, d in enumerate(images)))
    parts.append(_KIND_GUIDE)
    rules = ("RULES: tell a story; titles are insights, max 8 words (\"Drip irrigation halves water use\", not "
             "\"Water usage\"); never the same kind 3 times in a row; decks of 8+ slides use at least 5 kinds; "
             "slide 1 is title, last slide is closing. Give EVERY slide 2-4 \"points\" it must cover — no point may "
             "appear on two slides (no repetition across the deck).")
    if count and count >= 12:
        rules += (" This is a long deck: organise it into 3-6 parts that progress logically (context → core → "
                  "evidence → implications → conclusion); use 'section' divider slides only for 14+ slides.")
    if grounded:
        rules += (" List in \"facts\" the ids of the facts each slide will use. Use stats / chart / table / timeline "
                  "ONLY when the listed facts contain those numbers/dates (a chart needs ≥ 3 comparable figures "
                  "from the facts; a timeline needs ≥ 3 dated facts); a quote slide only if a fact contains a real "
                  "quotation.")
    parts.append(rules)
    parts.append('Return JSON: {"title": "...", "subtitle": "...", "slides": [{"n": 1, "kind": "title", '
                 '"title": "...", "goal": "what this slide must convey", "points": ["..."], "facts": ["F3"], '
                 '"image": null}]}')
    return "\n\n".join(parts)


def _content_prompt(req, purpose, density, source, outline, chunk, facts=None, grounded=False) -> str:
    parts = [f"DECK REQUEST: {req}", f"PURPOSE: {purpose}", f"DENSITY: {_DENSITY_RULES[density]}"]
    if source:
        parts.append("SOURCE MATERIAL (use ONLY these facts; keep the author's wording where possible):\n" + source[:7000])
    parts.append("FULL OUTLINE (for context — don't repeat other slides' points):\n" +
                 "\n".join(f"{s['n']}. [{s['kind']}] {s['title']}" for s in outline))
    blocks = []
    for s in chunk:
        b = {k: s.get(k) for k in ("n", "kind", "title", "goal", "points")}
        if grounded:
            b["FACTS"] = [f"{f['id']}: {f['fact']}" for f in s.get("_facts") or []] or \
                ["(none — write this slide qualitatively, without numbers)"]
        blocks.append(b)
    parts.append("WRITE SLIDES:\n" + json.dumps(blocks, ensure_ascii=False, indent=1))
    parts.append(_schema_for({s["kind"] for s in chunk}))
    if grounded:
        parts.append(_GROUND_RULES)
    parts.append("\"goal\" and \"points\" are planning notes: turn them into real slide copy, never paste them "
                 "verbatim, and never write fact ids like (F3) in the text. "
                 "Keep each given title and kind exactly. Cover exactly the slide's points. Be specific and factual; "
                 "no filler like \"plays a crucial role\". NEVER invent people, names, emails, phone numbers, team "
                 "names or URLs. Return JSON: {\"slides\": [{\"n\": .., \"kind\": .., \"title\": .., ...}]}")
    return "\n\n".join(parts)


_SYS_OUTLINE = ("You are a principal presentation designer and storyteller whose decks beat Gamma and Pitch. "
                "You plan crisp, well-structured decks. Output valid JSON only.")
_SYS_CONTENT = ("You write slide copy for a senior designer: concise, concrete, specific, zero filler, and strictly "
                "faithful to the facts you are given. Output valid JSON only.")


def _schema_for(kinds: set) -> str:
    """Only the schema lines for the kinds in this chunk (saves ~400 tokens per call on the free tier)."""
    lines = _SCHEMA.split("\n")
    out, keep = [lines[0]], False
    for ln in lines[1:]:
        m = re.match(r"^([a-z]+):", ln)
        if m:
            keep = m.group(1) in kinds
        elif not ln.startswith(" "):
            keep = True                                  # the general trailing rules
        if keep:
            out.append(ln)
    return "\n".join(out)


def plan_queries(topic: str, purpose: str, count: int) -> list[str]:
    """4-6 web queries covering the angles a deck on `topic` needs. Templates, not an LLM call:
    zero tokens (the Groq free tier is 200k tokens/day) and no invented search angles."""
    n = 6 if count >= 12 else 4
    t = re.sub(r"\s+", " ", topic).strip()
    if purpose == "hackathon":
        qs = [t, f"{t} problem statistics", f"{t} existing solutions", f"{t} market size", f"{t} technology",
              f"{t} government scheme"]
    elif purpose == "business":
        qs = [t, f"{t} market size growth", f"{t} key players", f"{t} trends", f"{t} challenges",
              f"{t} outlook forecast"]
    else:
        qs = [t, f"{t} statistics latest data", f"{t} history milestones", f"{t} challenges",
              f"{t} future outlook", f"{t} key facts examples"]
    return qs[:n]


def research_facts(topic: str, purpose: str, count: int, progress=None) -> list[dict]:
    """Web + Wikipedia → verified facts. [] when offline (the deck is then written qualitatively)."""
    from app.services import ppt_research as pr
    say = progress or (lambda m: None)
    say("🔎 Researching the topic so every figure on the slides comes from a real source…")
    try:
        pages = pr.gather_sources(topic, plan_queries(topic, purpose, count), say,
                                  max_pages=10 if count >= 12 else 7)
        if not pages:
            say("⚠️ No sources reachable — the deck will be written without specific figures.")
            return []
        return pr.extract_facts(topic, pages, _llm_json, say)
    except Exception as e:
        say(f"⚠️ Research failed ({e}) — the deck will be written without specific figures.")
        return []


def ground_slides(slides: list[dict], facts: list[dict], user_text: str, progress=None,
                  skip_locked: bool = True) -> tuple[list[dict], dict]:
    """Audit every generated slide; LLM-repair flagged ones with their facts; scrub what survives;
    remove cross-slide repeats; add source notes. → (slides, stats)"""
    from app.services import ppt_research as pr
    say = progress or (lambda m: None)
    allowed = pr.allowed_numbers(facts, user_text)
    fact_text = "\n".join(f["fact"] + " " + f.get("url", "") for f in facts) + "\n" + (user_text or "")
    stats = {"checked": 0, "flagged": 0, "repaired": 0, "removed": 0, "dupes": 0}
    for i, sl in enumerate(slides):                    # hygiene before the audit
        if skip_locked and sl.get("locked"):
            continue
        sl = pr.strip_fact_ids(sl)
        sl["bullets"] = [b for b in sl.get("bullets") or []
                         if not (isinstance(b, dict) and (b.get("text") or "").count("|") >= 2)]  # stray table rows
        if sl.get("kind") == "section" and len(sl.get("bullets") or []) >= 2:
            sl["kind"] = "content"                     # a divider that got real points would hide them
        slides[i] = sl
    flagged = {}
    for i, sl in enumerate(slides):
        if skip_locked and sl.get("locked"):
            continue
        stats["checked"] += 1
        probs = pr.audit_slide(sl, allowed, fact_text)
        if probs:
            flagged[i] = probs
    stats["flagged"] = len(flagged)
    if flagged:
        say(f"🧪 Fact-check: {len(flagged)} slide(s) had claims not backed by sources — fixing them…")
        idx = list(flagged)

        def repair(batch):
            payload, fx = [], []
            for i in batch:
                sl = slides[i]
                rel = pr.relevant_facts(facts, sl.get("title", "") + " " + json.dumps(sl, ensure_ascii=False)[:1500], 10)
                fx += [f for f in rel if f not in fx]
                payload.append({"n": i + 1, "slide": _compact(sl),
                                "problems": [f"{p['why']}: \"{p['text'][:160]}\"" for p in flagged[i]]})
            user = "\n\n".join([
                "FACTS (the only allowed origin of figures/dates/quotes):\n" + (pr.facts_block(fx) or "(none)"),
                _GROUND_RULES,
                "SLIDES WITH PROBLEMS:\n" + json.dumps(payload, ensure_ascii=False),
                "Fix ONLY the flagged texts: replace an unsupported figure with the matching FACT figure, or rewrite "
                "the point qualitatively without the figure. Remove unsourced quotes/links. Keep everything else, the "
                "title and the kind. Return JSON {\"slides\": [{\"n\": .., ...full slide...}]}",
            ])
            try:
                data = _llm_json(_SYS_CONTENT, user, max_tokens=3200, temperature=0.2, balance=True, effort="low")
            except Exception:
                return {}
            return {s.get("n"): s for s in data.get("slides") or [] if isinstance(s, dict)}

        with ThreadPoolExecutor(max_workers=2) as ex:
            for res in ex.map(repair, [idx[k:k + 3] for k in range(0, len(idx), 3)]):
                for n, s in res.items():
                    if isinstance(n, int) and 1 <= n <= len(slides):
                        base = slides[n - 1]
                        fixed = normalize_slide({**{k: v for k, v in base.items()
                                                    if k in ("images", "image_section", "locked", "variant", "n")},
                                                 **_flatten(s), "kind": s.get("kind") or base.get("kind"),
                                                 "title": base.get("title")})
                        if slide_has_content(fixed) or fixed["kind"] in ("title", "closing", "section"):
                            slides[n - 1] = fixed
                            stats["repaired"] += 1
    # deterministic last line of defence
    for i, sl in enumerate(slides):
        if skip_locked and sl.get("locked"):
            continue
        if pr.audit_slide(sl, allowed, fact_text):
            new, rem = pr.scrub_slide(sl, allowed, fact_text)
            stats["removed"] += rem
            slides[i] = normalize_slide(new)
    # repetition across slides (long decks love restating the same point)
    seen: list[set] = []
    for sl in slides:
        if skip_locked and sl.get("locked"):
            continue
        for key in ("bullets",):
            items = sl.get(key) or []
            keep = []
            for it in items:
                tk = pr._toks((it.get("head") or "") + " " + (it.get("text") or ""))
                if len(tk) >= 4 and any(len(tk & s) / max(1, len(tk | s)) > 0.6 for s in seen) and len(items) - \
                        (len(items) - len(keep)) > 2:
                    stats["dupes"] += 1
                    continue
                keep.append(it)
                if len(tk) >= 4:
                    seen.append(tk)
            sl[key] = keep
    # sources in the speaker notes
    for sl in slides:
        note = pr.sources_note(sl, facts)
        if note and note not in (sl.get("notes") or ""):
            sl["notes"] = ((sl.get("notes") or "") + "\n" + note).strip()
    say(f"✅ Fact-check done: {stats['checked']} slides checked · {stats['repaired']} repaired · "
        f"{stats['removed']} unsupported claim(s) removed · {stats['dupes']} repeat(s) removed.")
    return slides, stats


def generate_deck(request: str, purpose: str, density: str, count: int = 0, source: str = "",
                  fixed: Optional[list] = None, image_descs: Optional[list] = None, progress=None,
                  facts: Optional[list] = None, grounded: bool = True) -> dict:
    """LLM outline + content, grounded in `facts` and fact-checked afterwards.
    `fixed` = strict slides (titles/content locked; content only filled if missing)."""
    from app.services import ppt_research as pr
    say = progress or (lambda m: None)
    fixed = fixed or []
    facts = facts or []
    if fixed:
        count = len(fixed)
    outline_raw = _llm_json(_SYS_OUTLINE, _outline_prompt(request, purpose, density, count, source, fixed, image_descs,
                                                          facts, grounded),
                            max_tokens=4200 if count and count >= 12 else 2800, temperature=0.4)
    by_id = {f["id"]: f for f in facts}
    outline = []
    for i, s in enumerate(outline_raw.get("slides") or []):
        if not isinstance(s, dict):
            continue
        k = _KIND_SYNONYMS.get(str(s.get("kind", "")).lower(), "content")
        outline.append({"n": i + 1, "kind": k, "title": _s(s.get("title")), "goal": _s(s.get("goal")),
                        "points": [_s(p) for p in s.get("points") or [] if _s(p)][:4],
                        "fact_ids": [str(x) for x in s.get("facts") or [] if str(x) in by_id],
                        "image": s.get("image")})
    if fixed:                                   # the user's titles win, always
        by_n = {o["n"]: o for o in outline}
        outline = []
        for f in fixed:
            o = by_n.get(f["n"], {})
            outline.append({"n": f["n"], "title": f["title"], "goal": o.get("goal", ""), "image": o.get("image"),
                            "points": o.get("points", []), "fact_ids": o.get("fact_ids", []),
                            "kind": infer_kind(f, f["n"] - 1, len(fixed)) if f.get("layout_hint") or slide_has_content(f)
                            else o.get("kind", "content")})
    # long decks: the outline JSON can come back short (truncated / lazy model) → continue it, never shrink the deck
    for _ in range(3):
        if fixed or not count or len(outline) >= count:
            break
        have = len(outline)
        closing_planned = bool(outline) and outline[-1]["kind"] == "closing"
        base = outline[:-1] if closing_planned else outline
        say(f"📋 Outline has {have}/{count} slides — planning slides {len(base) + 1}–{count}…")
        cont = _outline_prompt(request, purpose, density, count, source, fixed, image_descs, facts, grounded) + \
            "\n\nALREADY PLANNED (keep, don't repeat their points):\n" + \
            "\n".join(f"{o['n']}. [{o['kind']}] {o['title']} — {'; '.join(o['points'])}" for o in base) + \
            f"\n\nNow return ONLY slides {len(base) + 1} to {count} (the last one is the closing slide), " \
            'as JSON {"slides": [...]} with the same fields.'
        try:
            more = _llm_json(_SYS_OUTLINE, cont, max_tokens=3600, temperature=0.4).get("slides") or []
        except Exception as e:
            say(f"⚠️ Could not extend the outline ({e}).")
            break
        added = []
        for s in more:
            if not isinstance(s, dict) or not _s(s.get("title")):
                continue
            if any(_s(s.get("title")).lower() == o["title"].lower() for o in base + added):
                continue
            added.append({"n": 0, "kind": _KIND_SYNONYMS.get(str(s.get("kind", "")).lower(), "content"),
                          "title": _s(s.get("title")), "goal": _s(s.get("goal")),
                          "points": [_s(p) for p in s.get("points") or [] if _s(p)][:4],
                          "fact_ids": [str(x) for x in s.get("facts") or [] if str(x) in by_id],
                          "image": s.get("image")})
        if not added:
            break
        outline = base + added
        if closing_planned and outline[-1]["kind"] != "closing":
            outline.append({"n": 0, "kind": "closing", "title": "Thank You", "goal": "", "points": [],
                            "fact_ids": [], "image": None})
    if count and len(outline) > count:
        outline = outline[:count - 1] + [outline[-1]]
    if count and len(outline) < count and not fixed:
        say(f"⚠️ Could only plan {len(outline)} of {count} slides.")
    if not outline:
        raise RuntimeError("empty outline")
    outline[0]["kind"] = outline[0]["kind"] if fixed else "title"
    no_data = grounded and not facts and not source
    for i, o in enumerate(outline):
        o["n"] = i + 1
        if no_data and o["kind"] in ("stats", "chart", "table", "timeline", "quote"):
            o["kind"] = "cards" if o["kind"] == "stats" else "content"
        # each slide gets its planned facts + the most relevant others (retrieval keeps prompts small and on-topic)
        mine = [by_id[x] for x in o["fact_ids"]]
        rel = pr.relevant_facts(facts, f"{o['title']} {o['goal']} {' '.join(o['points'])} {request}", 8,
                                exclude={f["id"] for f in mine})
        o["_facts"] = (mine + rel)[:12]
    say(f"📋 Outline: {len(outline)} slides — " + ", ".join(o["kind"] for o in outline))

    todo = [o for o in outline if not (fixed and slide_has_content(fixed[o["n"] - 1]))]
    results: dict[int, dict] = {}
    chunks = [todo[i:i + 3] for i in range(0, len(todo), 3)]

    long_deck = len(outline) >= 12

    def run(chunk):
        # long decks: spread chunks over both models and use low reasoning effort (free-tier token budget);
        # the fact-check afterwards keeps the smaller model honest
        data = _llm_json(_SYS_CONTENT, _content_prompt(request, purpose, density, source, outline, chunk, facts,
                                                       grounded),
                         max_tokens=2800 if long_deck else 3600, temperature=0.35, balance=long_deck,
                         effort="low" if long_deck else None)
        return chunk, data

    def _is_note(txt, o):
        """Slide text that is really the planner's note (goal/points) pasted verbatim."""
        tk = set(re.findall(r"[a-z]{3,}", (txt or "").lower()))
        for note in [o.get("goal") or ""]:
            nk = set(re.findall(r"[a-z]{3,}", note.lower()))
            if tk and nk and len(tk & nk) / len(tk | nk) >= 0.6:
                return True
        return False

    def take(chunk, data):
        got = [s for s in data.get("slides") or [] if isinstance(s, dict)]
        for j, o in enumerate(chunk):
            m = next((s for s in got if s.get("n") == o["n"]), None) or \
                next((s for s in got if _s(s.get("title")).lower() == o["title"].lower()), None) or \
                (got[j] if j < len(got) and len(got) == len(chunk) else None)
            if not m:
                continue
            m = _flatten(m)
            for k in ("body", "subtitle", "lead"):
                if isinstance(m.get(k), str) and _is_note(m[k], o):
                    m[k] = ""
            if isinstance(m.get("bullets"), list):
                m["bullets"] = [b for b in m["bullets"] if not (isinstance(b, dict) and not b.get("head")
                                                                  and _is_note(b.get("text"), o))]
            if slide_has_content(m) or o["kind"] in ("title", "closing", "section"):
                results[o["n"]] = m

    if chunks:
        with ThreadPoolExecutor(max_workers=2 if len(chunks) > 4 else 3) as ex:
            futs = [ex.submit(run, c) for c in chunks]
            for f in as_completed(futs):
                try:
                    chunk, data = f.result()
                    take(chunk, data)
                    say(f"✍️ Wrote slides {chunk[0]['n']}–{chunk[-1]['n']}")
                except Exception as e:
                    say(f"⚠️ A content batch failed ({e}); retrying those slides one by one.")
    # slides that came back empty → retry alone (never ship planning notes as slide text)
    missing = [o for o in todo if o["n"] not in results and o["kind"] not in ("title", "closing", "section")]
    for o in missing:
        try:
            take([o], _llm_json(_SYS_CONTENT, _content_prompt(request, purpose, density, source, outline, [o], facts,
                                                              grounded), max_tokens=2500, temperature=0.3))
        except Exception:
            pass

    slides = []
    for o in outline:
        if fixed and slide_has_content(fixed[o["n"] - 1]):
            sl = apply_structure(fixed[o["n"] - 1], o["kind"])
            sl["kind"] = o["kind"]
        else:
            gen = _flatten(results.get(o["n"], {}))
            sl = {**gen, "kind": o["kind"], "title": o["title"] or gen.get("title", "")}
            if fixed:
                f = fixed[o["n"] - 1]
                sl["title"] = f["title"] or sl["title"]
                for k in ("subtitle", "notes", "image_hint", "images", "locked"):
                    if f.get(k):
                        sl[k] = f[k]
                sl.pop("locked", None) if not slide_has_content(f) else None
            if not slide_has_content(sl) and o["kind"] not in ("title", "closing", "section"):
                if o.get("points"):                    # the planned points, never the internal "goal" note
                    sl["kind"] = "content"
                    sl["bullets"] = [{"head": "", "text": p} for p in o["points"]]
                else:
                    sl["kind"] = "section"
        if isinstance(o.get("image"), int):
            sl["_image_idx"] = o["image"]
        sl["n"] = o["n"]
        slides.append(sl)
    if grounded:
        idx = [s.get("_image_idx") for s in slides]
        slides = [normalize_slide(s) if not s.get("locked") else s for s in slides]
        slides, _ = ground_slides(slides, facts, request + "\n" + (source or ""), say)
        for s, i in zip(slides, idx):
            if isinstance(i, int):
                s["_image_idx"] = i
    return {"title": _s(outline_raw.get("title")) or (slides[0].get("title") if slides else request[:60]),
            "subtitle": _s(outline_raw.get("subtitle")), "slides": slides, "facts": facts}


# ══════════════════════════════════════════════════════════════════════════════
#  EDITS
# ══════════════════════════════════════════════════════════════════════════════
_ORD = {"first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5, "sixth": 6, "seventh": 7, "eighth": 8,
        "ninth": 9, "tenth": 10, "eleventh": 11, "twelfth": 12}
_STOP = set("the a an of in on to for and or with slide slides this that it make change update edit modify "
            "please add remove put use into as is be more less".split())


def find_targets(instr: str, deck: dict) -> list[int]:
    """1-based slide numbers referenced by the instruction."""
    n = len(deck.get("slides", []))
    low = instr.lower()
    out: list[int] = []
    for m in re.finditer(r"slides?\s*(?:no\.?|number|#)?\s*(\d{1,2}(?:\s*(?:,|and|&|to|-|–|through)\s*\d{1,2})*)", low):
        seg = m.group(1)
        for a, b in re.findall(r"(\d{1,2})\s*(?:to|-|–|through)\s*(\d{1,2})", seg):
            out += list(range(int(a), int(b) + 1))
        out += [int(x) for x in re.findall(r"\d{1,2}", seg)]
    for m in re.finditer(r"\b(\d{1,2})(?:st|nd|rd|th)\s+slide", low):
        out.append(int(m.group(1)))
    for w, k in _ORD.items():
        if re.search(rf"\b{w}\s+slide", low) and not re.search(rf"\b{w}\s+slide\s*\d", low):
            out.append(k)
    if re.search(r"\b(second|2nd)[\s-]+(to[\s-]+)?last\s+slide", low):
        out.append(n - 1)
    elif re.search(r"\b(last|final|closing|ending|thank[- ]you)\s+slide", low):
        out.append(n)
    if re.search(r"\b(title|cover|first|opening|intro(?:duction)?)\s+slide\b", low):
        out.append(1)
    if not out and "slide" in low:                   # "the roadmap slide"
        words = set(re.findall(r"[a-z]{3,}", low)) - _STOP
        best, best_n = 0, None
        for i, s in enumerate(deck.get("slides", [])):
            tw = set(re.findall(r"[a-z]{3,}", (s.get("title") or "").lower())) - _STOP
            sc = len(words & tw)
            if sc > best:
                best, best_n = sc, i + 1
        if best_n:
            out.append(best_n)
    seen = []
    for x in out:
        if 1 <= x <= n and x not in seen:
            seen.append(x)
    return seen


def _clauses(instr: str) -> list[str]:
    parts = re.split(r"\n+|;\s*|\.\s+(?=[A-Z])|\s+(?:and then|then|also)\s+", instr.strip())
    return [p.strip(" .") for p in parts if p and p.strip(" .")]


def _quoted(s: str) -> list[str]:
    # a single quote followed by a letter is an apostrophe ("India's"), not a closing quote
    return [a or b or c for a, b, c in re.findall(r"\"([^\"]+)\"|“([^”]+)”|(?<!\w)'(.+?)'(?!\w)", s)]


def _replace_everywhere(obj, old: str, new: str):
    if isinstance(obj, str):
        return obj.replace(old, new)
    if isinstance(obj, list):
        return [_replace_everywhere(x, old, new) for x in obj]
    if isinstance(obj, dict):
        return {k: (_replace_everywhere(v, old, new) if k not in ("images", "kind") else v) for k, v in obj.items()}
    return obj


def _kind_from_text(low: str) -> Optional[str]:
    m = re.search(r"\b(?:into|as|to|a|an|use|using|with)\s+(?:a\s+|an\s+)?(timeline|comparison|table|chart|bar chart|pie chart|"
                  r"line chart|cards?|grid|process|steps|flow|stats|metrics|numbers|quote|two columns|columns|list|"
                  r"bullets?|section|agenda|gallery|title)\b(?:\s+(?:layout|slide|format|style|view))?", low)
    if not m:
        return None
    return _KIND_SYNONYMS.get(m.group(1).rstrip("s") if m.group(1) not in ("stats", "steps", "metrics", "numbers",
                                                                             "columns", "two columns", "bullets")
                              else m.group(1), None) or _KIND_SYNONYMS.get(m.group(1))


def apply_edit(deck: dict, instruction: str, new_images: Optional[list] = None,
               theme_resolver=None, progress=None) -> tuple[dict, list[str]]:
    """Returns (new_deck, list of human-readable change notes)."""
    say = progress or (lambda m: None)
    deck = copy.deepcopy(deck)
    slides = deck["slides"]
    original_slides = copy.deepcopy(slides)
    notes: list[str] = []
    llm_jobs: list[tuple[str, list[int]]] = []
    new_images = [p for p in (new_images or []) if p]
    images_used = False

    for clause in _clauses(instruction) or [instruction]:
        low = clause.lower()
        tg = find_targets(clause, deck) or find_targets(instruction, deck)
        q = _quoted(clause)

        # ── delete slides ──────────────────────────────────────────────────
        if re.search(r"\b(delete|remove|drop|get rid of)\b", low) and re.search(r"\bslides?\b", low) and tg and \
                not re.search(r"\b(image|picture|photo|bullet|point|line|word|sentence|text|title|subtitle|chart|table|logo)\b", low):
            for k in sorted(tg, reverse=True):
                slides.pop(k - 1)
            notes.append(f"Deleted slide(s) {', '.join(map(str, sorted(tg)))}")
            continue
        # ── move / swap ────────────────────────────────────────────────────
        m = re.search(r"\bswap\s+slides?\s*(\d+)\s*(?:and|with|&)\s*(?:slide\s*)?(\d+)", low)
        if m:
            a, b = int(m.group(1)) - 1, int(m.group(2)) - 1
            if 0 <= a < len(slides) and 0 <= b < len(slides):
                slides[a], slides[b] = slides[b], slides[a]
                notes.append(f"Swapped slides {a + 1} and {b + 1}")
            continue
        m = re.search(r"\bmove\s+(?:the\s+)?slide\s*(\d+)\s+(to|after|before)\s+(?:position\s*|slide\s*)?(\d+)", low)
        if m:
            a, how, b = int(m.group(1)) - 1, m.group(2), int(m.group(3))
            if 0 <= a < len(slides):
                s_ = slides.pop(a)
                pos = b - 1 if how in ("to", "before") else b
                if how == "after" and a < b - 1:
                    pos -= 1
                if how == "before" and a < b - 1:
                    pos -= 1
                slides.insert(max(0, min(len(slides), pos)), s_)
                notes.append(f"Moved slide {a + 1} {how} {b}")
            continue
        # ── exact title / subtitle ─────────────────────────────────────────
        m = re.search(r"\b(?:change|rename|set|make|update|edit|replace)\b.*?\b(title|heading|subtitle|sub-title|tagline)\b"
                      r".*?\b(?:to|as|with|into|:)\s+(.+)$", clause, re.I)
        if m and tg:
            raw = m.group(2).strip()
            if len(raw) >= 2 and raw[0] in "\"'“" and raw[-1] in "\"'”":
                val = raw[1:-1].strip()
            else:
                val = (q[-1] if q else raw).strip().strip("\"“”")
            field = "subtitle" if m.group(1).lower() in ("subtitle", "sub-title", "tagline") else "title"
            for k in tg:
                slides[k - 1][field] = val
                if field == "title":
                    slides[k - 1]["replace_title"] = True     # fixed-format decks keep headings unless asked
            notes.append(f"Set {field} of slide {', '.join(map(str, tg))} to “{val}”")
            continue
        # ── exact text replace ─────────────────────────────────────────────
        m = re.search(r"\b(?:replace|change|swap)\b", low)
        if m and len(q) >= 2 and re.search(r"\b(with|to|by|into)\b", low):
            old, new = q[0], q[1]
            scope = tg or list(range(1, len(slides) + 1))
            hit = 0
            for k in scope:
                before = json.dumps(slides[k - 1], ensure_ascii=False)
                slides[k - 1] = _replace_everywhere(slides[k - 1], old, new)
                hit += before != json.dumps(slides[k - 1], ensure_ascii=False)
            if hit:
                notes.append(f"Replaced “{old}” → “{new}” on {hit} slide(s)")
                continue
        # ── move existing images ("move the screenshots to slide 3 under the architecture section") ──
        if not new_images and re.search(r"\b(move|shift|put|place|bring|transfer|keep)\b", low) and \
                re.search(r"\b(image|picture|photo|pic|screenshot|img)s?\b", low):
            titles = [x.get("title", "") for x in slides]
            rules = parse_instructions([clause], 0, titles)
            dest = rules["images_only_on"] or (tg[-1] if tg else None)
            m_src = re.search(r"\bfrom\s+(?:the\s+)?(?:slide\s*(\d{1,2})|(\w+)\s+slide)", low)
            src = [int(m_src.group(1))] if m_src and m_src.group(1) else \
                [i + 1 for i, x in enumerate(slides) if x.get("images") and i + 1 != dest]
            if dest and 1 <= dest <= len(slides) and src:
                moved = []
                for k in src:
                    if 1 <= k <= len(slides) and k != dest:
                        moved += slides[k - 1].get("images") or []
                        slides[k - 1]["images"] = []
                if moved:
                    slides[dest - 1]["images"] = (slides[dest - 1].get("images") or []) + moved
                    sec = rules["image_section"].get(dest)
                    if sec:
                        slides[dest - 1]["image_section"] = sec
                    notes.append(f"Moved {len(moved)} image(s) to slide {dest}" + (f" ({sec} section)" if sec else ""))
                    continue
        # ── images ─────────────────────────────────────────────────────────
        if re.search(r"\b(image|picture|photo|pic|screenshot|logo|img)s?\b", low):
            if re.search(r"\b(remove|delete|drop|without|no)\b", low) and tg:
                for k in tg:
                    slides[k - 1]["images"] = []
                notes.append(f"Removed image(s) from slide {', '.join(map(str, tg))}")
                continue
            if "logo" in low and new_images and not tg:
                deck["logo"] = new_images[0]
                images_used = True
                notes.append("Added your logo to every slide")
                continue
            if new_images:
                if not tg:
                    tg = [next((i + 1 for i, s in enumerate(slides) if s.get("kind") == "content" and not s.get("images")),
                               2 if len(slides) > 1 else 1)]
                add = bool(re.search(r"\b(add|another|also|more|second|extra|along)\b", low)) and \
                    not re.search(r"\b(replace|change|swap|instead)\b", low)
                for k in tg:
                    cur = slides[k - 1].get("images") or []
                    slides[k - 1]["images"] = (cur + new_images) if add else list(new_images)
                    if slides[k - 1].get("kind") in ("stats", "table", "chart", "timeline") and len(new_images) > 1:
                        slides[k - 1]["kind"] = "content"
                images_used = True
                notes.append(f"{'Added' if add else 'Placed'} {len(new_images)} image(s) on slide {', '.join(map(str, tg))}")
                if not re.search(r"\b(and|also|make|change|rewrite|text|title)\b.*\b(text|title|point|bullet|content)\b", low):
                    continue
            m2 = re.search(r"image\s+(?:on\s+the\s+)?(left|right)|(left|right)\s+side", low)
            if m2 and tg:
                side = m2.group(1) or m2.group(2)
                for k in tg:
                    slides[k - 1]["image_side"] = side
                notes.append(f"Image on the {side} for slide {', '.join(map(str, tg))}")
                continue
        # ── theme / colours / font ─────────────────────────────────────────
        if re.search(r"\b(theme|colou?rs?|palette|background|dark|light|style|look)\b", low) and not tg and theme_resolver:
            new_t = theme_resolver(clause, deck)
            if new_t:
                deck["theme"] = new_t
                notes.append(f"Theme → {new_t.get('name', 'custom')}")
                continue
        m = re.search(r"\b(?:font|typeface)\b.*?\b(segoe ui|georgia|calibri|cambria|bahnschrift|century gothic|arial|"
                      r"verdana|tahoma|candara|corbel|constantia|trebuchet ms|times new roman|aptos)\b", low)
        if m:
            fam = m.group(1).title().replace("Ui", "UI").replace("Ms", "MS")
            if "heading" in low or "title" in low:
                deck["theme"]["head_font"] = fam
            elif "body" in low:
                deck["theme"]["body_font"] = fam
            else:
                deck["theme"]["head_font"] = deck["theme"]["body_font"] = fam
            notes.append(f"Font → {fam}")
            continue
        # ── density (whole deck) ───────────────────────────────────────────
        if not tg and re.search(r"\b(less|fewer|reduce|shorter|concise|minimal)\b.*\b(text|words|content)\b", low):
            deck["density"] = "light"
            llm_jobs.append((clause, list(range(1, len(slides) + 1))))
            continue
        if not tg and re.search(r"\b(more|add|richer|detailed|expand)\b.*\b(content|detail|text|information)\b", low):
            deck["density"] = "dense"
            llm_jobs.append((clause, list(range(1, len(slides) + 1))))
            continue
        # ── layout change ──────────────────────────────────────────────────
        if tg and re.search(r"\b(layout|convert|turn|show|make|change|display|present|format)\b", low):
            k_new = _kind_from_text(low)
            if k_new and not re.search(r"\b(add|write|rewrite|include|mention|explain)\b", low):
                for k in tg:
                    sl = slides[k - 1]
                    if sl.get("sections") and not sl.get("bullets") and k_new != "sections":
                        # composite slide → plain items so any other layout can use the same words
                        sl["bullets"] = [{"head": plain_md(i.get("head") or i.get("value") or ""),
                                          "text": plain_md(i.get("text") or i.get("label") or "")}
                                         for sec in sl["sections"] if isinstance(sec, dict)
                                         for i in (sec.get("items") or []) if isinstance(i, dict)]
                        sl["body"] = sl.get("body") or plain_md(sl.get("lead") or "")
                        sl.pop("sections", None)
                    if k_new == "cards":
                        sl["kind"], sl["variant"] = "content", "cards"
                        if sl.get("steps") and not sl.get("bullets"):
                            sl["bullets"] = [{"head": x.get("head") or x.get("date"), "text": x.get("text")} for x in sl["steps"]]
                    elif k_new == "content":
                        sl["kind"], sl["variant"] = "content", "list"
                        if sl.get("steps") and not sl.get("bullets"):
                            sl["bullets"] = [{"head": x.get("head") or x.get("date"), "text": x.get("text")} for x in sl["steps"]]
                        if sl.get("stats") and not sl.get("bullets"):
                            sl["bullets"] = [{"head": x["value"], "text": (x["label"] + (" — " + x["desc"] if x.get("desc") else ""))}
                                             for x in sl["stats"]]
                    else:
                        if sl.get("steps") and not sl.get("bullets"):
                            sl["bullets"] = [{"head": x.get("date") or x.get("head"),
                                              "text": ((x.get("head") + ": ") if x.get("date") and x.get("head") else "") + x.get("text", "")}
                                             for x in sl["steps"]]
                            sl["steps"] = []
                        conv = apply_structure({**sl, "kind": k_new}, k_new)
                        conv["kind"] = k_new
                        if normalize_slide(conv)["kind"] == k_new:
                            slides[k - 1] = conv
                        else:                          # needs new data (e.g. chart numbers) → LLM
                            llm_jobs.append((clause, [k]))
                            continue
                notes.append(f"Slide {', '.join(map(str, tg))} → {k_new} layout")
                continue
        # ── add a slide ────────────────────────────────────────────────────
        m = re.search(r"\b(add|insert|create|include)\b\s+(?:a\s+|an\s+|one\s+|new\s+|another\s+)*(?:\w+\s+){0,3}?slide\b", low)
        if m:
            pos = len(slides) - (1 if slides and slides[-1].get("kind") == "closing" else 0)
            mp = re.search(r"\b(after|before)\s+slide\s*(\d+)", low) or re.search(r"\bat\s+(?:position\s*)?(\d+)", low)
            if mp and mp.lastindex == 2:
                pos = int(mp.group(2)) if mp.group(1) == "after" else int(mp.group(2)) - 1
            elif mp:
                pos = int(mp.group(1)) - 1
            elif re.search(r"\b(at the )?(start|beginning)\b", low):
                pos = 1
            given = clause.split(":", 1)[1] if ":" in clause else ""
            strict = parse_user_slides("Slide 1: " + given.strip()) if given.strip() and \
                ("\n" in given or re.search(r"\b(title|points?|bullets?)\s*:", given, re.I) or len(given) > 80) else []
            if strict:
                new_sl = strict[0]
                new_sl["kind"] = infer_kind(new_sl, pos, len(slides) + 1)
                new_sl = apply_structure(new_sl, new_sl["kind"])
            else:
                new_sl = _llm_new_slide(deck, clause, pos)
                new_sl["_fresh"] = True
            if new_images and not images_used:
                new_sl["images"] = list(new_images)
                images_used = True
            slides.insert(max(0, min(len(slides), pos)), new_sl)
            notes.append(f"Added slide {pos + 1}: {new_sl.get('title', '')}")
            continue
        # ── everything else → LLM on the targets ───────────────────────────
        llm_jobs.append((clause, tg))

    # merge LLM jobs (same targets → one call)
    if llm_jobs:
        merged: dict[tuple, list[str]] = {}
        for clause, tg in llm_jobs:
            merged.setdefault(tuple(tg), []).append(clause)
        for tg, cls in merged.items():
            tgt = list(tg) or _guess_targets(deck, " ".join(cls))
            for i in range(0, len(tgt), 4):
                part = tgt[i:i + 4]
                say(f"🧠 Rewriting slide(s) {', '.join(map(str, part))}…")
                try:
                    changed, summary = _llm_edit(deck, "; ".join(cls), part)
                    for k, sl in changed.items():
                        if 1 <= k <= len(slides):
                            if not sl.get("images") and slides[k - 1].get("images") and \
                                    not re.search(r"\b(remove|delete)\b.*\b(image|picture|photo)", " ".join(cls).lower()):
                                sl["images"] = slides[k - 1]["images"]
                            sl["_fresh"] = True              # AI-written → fact-check below
                            slides[k - 1] = sl
                    if summary:
                        notes.append(summary)
                except Exception as e:
                    notes.append(f"⚠️ Could not apply “{'; '.join(cls)[:80]}” ({e})")
    if new_images and not images_used:
        k = next((i + 1 for i, s in enumerate(slides) if s.get("kind") == "content" and not s.get("images")), None)
        if k:
            slides[k - 1]["images"] = list(new_images)
            notes.append(f"Placed the attached image(s) on slide {k}")
    fresh = [i for i, s_ in enumerate(slides) if s_.get("_fresh")]
    if fresh:                                         # same fact discipline as generation
        known = "\n".join([instruction, deck.get("source_text") or "",
                           json.dumps(original_slides, ensure_ascii=False)])
        sub = [{k: v for k, v in slides[i].items() if k != "_fresh"} for i in fresh]
        sub, st = ground_slides(sub, deck.get("facts") or [], known, say, skip_locked=False)
        for i, s_ in zip(fresh, sub):
            slides[i] = s_
        if st["removed"]:
            notes.append(f"Fact-check removed {st['removed']} unsupported claim(s) from the rewritten slide(s)")
    deck["slides"] = finalize_slides(slides)
    return deck, notes


def _guess_targets(deck, instr) -> list[int]:
    n = len(deck["slides"])
    return list(range(1, n + 1))


def _compact(sl: dict) -> dict:
    return {k: v for k, v in sl.items() if k not in ("images", "locked", "image_hint", "_section_no", "variant",
                                                     "image_side") and v not in (None, "", [], {})}


_SYS_EDIT = ("You edit slides of an existing presentation. Apply the user's instruction EXACTLY and MINIMALLY. "
             "Anything the instruction does not ask to change must be copied verbatim, character for character. "
             "If the user gives exact wording, use it verbatim. Keep the JSON schema. Output valid JSON only.")


def _edit_facts(deck: dict, query: str) -> str:
    """Facts relevant to an edit + the fact discipline (edits must not hallucinate either)."""
    facts = deck.get("facts") or []
    block = ""
    if facts:
        from app.services.ppt_research import relevant_facts, facts_block
        block = "FACTS (verified; the only allowed new figures/dates/quotes besides the user's instruction):\n" + \
            facts_block(relevant_facts(facts, query, 12))
    return (block + "\n" + _GROUND_RULES).strip()


def _llm_edit(deck: dict, instruction: str, targets: list[int]) -> tuple[dict, str]:
    slides = deck["slides"]
    payload = [{"n": k, **_compact(slides[k - 1])} for k in targets]
    user = "\n\n".join([
        f"DECK: {deck.get('title', '')} (purpose: {deck.get('purpose', 'general')}, {len(slides)} slides)",
        f"DENSITY: {_DENSITY_RULES.get(deck.get('density', 'light'))}",
        "OTHER SLIDE TITLES: " + " | ".join(f"{i + 1}. {s.get('title', '')}" for i, s in enumerate(slides)),
        _SCHEMA,
        "SLIDES TO EDIT:\n" + json.dumps(payload, ensure_ascii=False),
        _edit_facts(deck, instruction + " " + json.dumps(payload, ensure_ascii=False)[:1500]),
        f"INSTRUCTION: {instruction}",
        'Return JSON: {"slides": [ {full edited slide incl. "n" and "kind"} ], "summary": "one short line saying what '
        'changed"}. Only include slides you actually changed.',
    ])
    data = _llm_json(_SYS_EDIT, user, max_tokens=5000, temperature=0.3)
    out = {}
    for s in data.get("slides") or []:
        if isinstance(s, dict) and isinstance(s.get("n"), int) and s["n"] in targets:
            k = s.pop("n")
            base = slides[k - 1]
            merged = {**{kk: vv for kk, vv in base.items() if kk in ("images", "locked", "image_side", "variant")}, **s}
            out[k] = normalize_slide(merged)
    return out, _s(data.get("summary"))


def _llm_new_slide(deck: dict, instruction: str, pos: int) -> dict:
    slides = deck["slides"]
    user = "\n\n".join([
        f"DECK: {deck.get('title', '')} (purpose: {deck.get('purpose', 'general')})",
        f"DENSITY: {_DENSITY_RULES.get(deck.get('density', 'light'))}",
        "SLIDES: " + " | ".join(f"{i + 1}. {s.get('title', '')}" for i, s in enumerate(slides)),
        _KIND_GUIDE, _SCHEMA,
        _edit_facts(deck, instruction),
        f"The new slide goes at position {pos + 1}. INSTRUCTION: {instruction}",
        'Return JSON: {"slide": {"kind": "...", "title": "...", ...fields}}',
    ])
    data = _llm_json(_SYS_CONTENT, user, max_tokens=2500)
    return normalize_slide(data.get("slide") or {"kind": "content", "title": instruction[:60]})
