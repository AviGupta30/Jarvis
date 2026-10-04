"""
measure.py — Text layer of the reference page: OCR lines with measured ink/colour/weight, then the page
structure (name, title, header contact, headings, columns, sections, item roles) from pixel geometry.

Everything here is deterministic and local (RapidOCR + numpy/OpenCV); no LLM is involved, so the analysis
never depends on vision-model quota.
"""
from __future__ import annotations

import os
import re
import threading

import numpy as np

from .ingest import PX_PER_MM

_ocr = None
_ocr_lock = threading.Lock()

EMAIL_RX = re.compile(r"[\w.+-]+@[\w-]+(\.[\w-]+)+")
PHONE_RX = re.compile(r"(?:\+?\d[\d\s().\-/]{6,}\d)")
URL_RX = re.compile(r"(?i)(linkedin|github|behance|dribbble|www\.|https?://|\.(com|in|io|me|dev|org|net)\b/?|portfolio)")
DATE_RX = re.compile(r"(?i)\b((19|20)\d{2}|present|current|now|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\b")
BULLET_CHARS = "•●◦▪■□▸►‣–-*·○◆◇✓✔➤→"


def mm(px: float) -> float:
    return round(float(px) / PX_PER_MM, 2)


def _hex(c) -> str:
    b, g, r = [int(max(0, min(255, round(v)))) for v in c]
    return f"#{r:02x}{g:02x}{b:02x}"


_EN_REC = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
                       "data", "models", "en_PP-OCRv3_rec_infer.onnx")
_EN_REC_URL = "https://huggingface.co/SWHL/RapidOCR/resolve/main/PP-OCRv3/en_PP-OCRv3_rec_infer.onnx"


def _get_ocr():
    """RapidOCR with the English recogniser (the bundled Chinese one drops the spaces between English words)."""
    global _ocr
    with _ocr_lock:
        if _ocr is None:
            from rapidocr_onnxruntime import RapidOCR
            if not os.path.exists(_EN_REC):
                try:
                    import requests
                    r = requests.get(_EN_REC_URL, timeout=90)
                    if r.status_code == 200 and len(r.content) > 1_000_000:
                        os.makedirs(os.path.dirname(_EN_REC), exist_ok=True)
                        with open(_EN_REC, "wb") as f:
                            f.write(r.content)
                except Exception as e:
                    print(f"[replica] English OCR model download failed: {e}")
            _ocr = RapidOCR(rec_model_path=_EN_REC) if os.path.exists(_EN_REC) else RapidOCR()
    return _ocr


def ocr_lines(img: np.ndarray) -> list[dict]:
    res, _ = _get_ocr()(img)
    out = []
    for box, text, conf in res or []:
        text = str(text).strip()
        if not text:
            continue
        xs = [p[0] for p in box]
        ys = [p[1] for p in box]
        out.append({"text": text, "conf": float(conf),
                    "box": [int(min(xs)), int(min(ys)), int(max(xs)) + 1, int(max(ys)) + 1]})
    out = _merge_spaced(out)
    out.sort(key=lambda l: (l["box"][1], l["box"][0]))
    for i, l in enumerate(out):
        l["id"] = i
    return out


def _merge_spaced(lines: list[dict]) -> list[dict]:
    """OCR splits widely letter-spaced text ("ESTELLE   DARCY", "B U S I N E S S") into pieces: boxes on the
    same row with the same height and a gap below ~1.6 × their height are one line."""
    lines = sorted(lines, key=lambda l: (l["box"][1], l["box"][0]))
    merged: list[dict] = []
    used = [False] * len(lines)
    for i, a in enumerate(lines):
        if used[i]:
            continue
        cur = dict(a)
        used[i] = True
        changed = True
        while changed:
            changed = False
            for j, b in enumerate(lines):
                if used[j]:
                    continue
                ha, hb = cur["box"][3] - cur["box"][1], b["box"][3] - b["box"][1]
                ov = min(cur["box"][3], b["box"][3]) - max(cur["box"][1], b["box"][1])
                if ov < 0.7 * min(ha, hb) or not (0.8 < hb / max(1, ha) < 1.25):
                    continue
                gap = b["box"][0] - cur["box"][2] if b["box"][0] >= cur["box"][2] else cur["box"][0] - b["box"][2]
                if -2 <= gap <= 1.6 * min(ha, hb):
                    left, right = (cur, b) if cur["box"][0] <= b["box"][0] else (b, cur)
                    cur = {"text": (left["text"] + " " + right["text"]).strip(), "conf": min(cur["conf"], b["conf"]),
                           "box": [min(cur["box"][0], b["box"][0]), min(cur["box"][1], b["box"][1]),
                                   max(cur["box"][2], b["box"][2]), max(cur["box"][3], b["box"][3])]}
                    used[j] = True
                    changed = True
        merged.append(cur)
    return merged


def _stroke(mask: np.ndarray) -> float:
    """Mean stroke width (px) = ink area / skeleton length."""
    import cv2
    try:
        sk = cv2.ximgproc.thinning(mask.astype(np.uint8) * 255)
        n = int((sk > 0).sum())
        return float(mask.sum()) / max(n, 1)
    except Exception:
        dt = cv2.distanceTransform(mask.astype(np.uint8), cv2.DIST_L2, 3)
        return float(2 * np.median(dt[mask])) if mask.any() else 0.0


def measure_line(img: np.ndarray, line: dict) -> None:
    """Adds fg/bg colour, tight ink box, stroke width and the ink mask (for font matching) to a line."""
    H, W = img.shape[:2]
    x0, y0, x1, y1 = line["box"]
    pad = 3
    X0, Y0, X1, Y1 = max(0, x0 - pad), max(0, y0 - pad), min(W, x1 + pad), min(H, y1 + pad)
    crop = img[Y0:Y1, X0:X1].astype(np.int16)
    ring = np.concatenate([crop[0], crop[-1], crop[:, 0], crop[:, -1]])
    bg = np.median(ring, axis=0)
    d = np.abs(crop - bg).sum(-1)
    p99 = float(np.percentile(d, 99.5)) if d.size else 0
    line["bg"] = _hex(bg)
    if p99 < 45:
        line["ink"] = None
        return
    ink = d > max(50, 0.42 * p99)
    core = d > 0.72 * p99
    fg = np.median(crop[core], axis=0) if core.any() else bg
    # vertically, only this line: the padding (and tight line spacing at low resolution) pulls in the
    # neighbours' ascenders/descenders, which inflates the measured size
    mpad = max(2, int(0.2 * (y1 - y0)))
    ink[:max(0, y0 - Y0 - mpad)] = False
    ink[max(0, y1 - Y0 + mpad):] = False
    rows = ink.sum(1)
    if rows.max() > 0:
        weak = rows < 0.06 * rows.max()
        top = 0
        while top < len(rows) and (rows[top] == 0 or weak[top]):
            top += 1
        bot = len(rows)
        while bot > top and (rows[bot - 1] == 0 or weak[bot - 1]):
            bot -= 1
        ink[:top] = False
        ink[bot:] = False
        # a skill bar / rule touching the line: rows that are one long solid run, not glyphs
        def solid(r):
            row = ink[r]
            if not row.any():
                return False
            xs_ = np.nonzero(row)[0]
            runs = 1 + int((np.diff(xs_) > 1).sum())
            return runs <= 2 and (xs_[-1] - xs_[0]) > 0.5 * max(1, int(ink.any(0).sum()))
        while bot > top + 3 and solid(bot - 1):
            ink[bot - 1] = False
            bot -= 1
        while bot > top + 3 and solid(top):
            ink[top] = False
            top += 1
        # and the blank rows that separated it from the text
        rows = ink.sum(1)
        nz = np.nonzero(rows)[0]
        if len(nz):
            ink[:nz[0]] = False
            ink[nz[-1] + 1:] = False
    if not ink.any():
        line["ink"] = None
        return
    ys, xs = np.nonzero(ink)
    ix0, iy0, ix1, iy1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
    line["fg"] = _hex(fg)
    m = ink[iy0:iy1, ix0:ix1]
    # a bullet the OCR box swallowed (". Performs", "•Deploys"): small first blob followed by a gap
    colany = m.any(0)
    hh = m.shape[0]
    if colany.any() and hh >= 6:
        a = int(np.argmax(colany))
        b = a
        while b < len(colany) and colany[b]:
            b += 1
        g = b
        while g < len(colany) and not colany[g]:
            g += 1
        rows = np.nonzero(m[:, a:b].any(1))[0]
        bh = (rows.max() - rows.min() + 1) if len(rows) else hh
        if (b - a) < 0.7 * hh and bh < 0.7 * hh and (g - b) > 0.22 * hh and g < len(colany) and \
                (line["text"][:1] in BULLET_CHARS + ".,:;" or bh < 0.45 * hh):
            line["inner_bullet"] = [int(X0 + ix0 + a), int(Y0 + iy0 + rows.min()), int(X0 + ix0 + b),
                                    int(Y0 + iy0 + rows.max() + 1)]
            line["text"] = line["text"].lstrip(BULLET_CHARS + ".,:; ").strip() if line["text"][:1] in BULLET_CHARS + ".,:;" \
                else line["text"]
            ix0 = ix0 + g
            m = ink[iy0:iy1, ix0:ix1]
            rows = np.nonzero(m.any(1))[0]
            if len(rows):
                iy0, iy1 = iy0 + rows.min(), iy0 + rows.max() + 1
                m = ink[iy0:iy1, ix0:ix1]
    line["ink"] = [int(X0 + ix0), int(Y0 + iy0), int(X0 + ix1), int(Y0 + iy1)]
    line["mask"] = m
    line["stroke"] = _stroke(line["mask"])
    line["ink_h"] = int(iy1 - iy0)


# ── helpers ────────────────────────────────────────────────────────────────────────────────────────

def _letters(t: str) -> str:
    return re.sub(r"[^A-Za-z]", "", t)


def _is_upper(t: str) -> bool:
    L = _letters(t)
    return len(L) >= 2 and L.upper() == L


def _cdist(a: str, b: str) -> float:
    pa = np.array([int(a[i:i + 2], 16) for i in (1, 3, 5)], float)
    pb = np.array([int(b[i:i + 2], 16) for i in (1, 3, 5)], float)
    return float(np.sqrt(((pa - pb) ** 2).sum()))


def _size_key(l: dict) -> float:
    """Comparable size proxy: OCR box height (stable per font size, independent of the letters)."""
    return float(l["box"][3] - l["box"][1])


def _same_style(a: dict, b: dict, tol_h: float = 0.22, tol_c: float = 70) -> bool:
    if not a.get("ink") or not b.get("ink"):
        return False
    if abs(np.log(_size_key(a) / max(1.0, _size_key(b)))) > tol_h:
        return False
    if _cdist(a["fg"], b["fg"]) > tol_c:
        return False
    if a["upper"] != b["upper"] and len(_letters(a["text"])) >= 5 and len(_letters(b["text"])) >= 5:
        return False                     # case only tells styles apart on real words ("SQL", "HSC" don't count)
    sa, sb = a["stroke"] / max(1, _size_key(a)), b["stroke"] / max(1, _size_key(b))
    return abs(np.log(max(sa, 1e-3) / max(sb, 1e-3))) < 0.35


def _v_overlap(a, b) -> float:
    lo, hi = max(a[1], b[1]), min(a[3], b[3])
    return max(0, hi - lo) / max(1, min(a[3] - a[1], b[3] - b[1]))


def _h_overlap(a, b) -> float:
    lo, hi = max(a[0], b[0]), min(a[2], b[2])
    return max(0, hi - lo) / max(1, min(a[2] - a[0], b[2] - b[0]))


_TITLE_KEYS = [   # same vocabulary as resume_builder._TITLE_KEYS, but tolerant to OCR-dropped spaces
    (r"profile|summary|about|objective|introduction|overview|personal\s*statement", "profile"),
    (r"highlight|key\s*facts|at\s*a\s*glance", "highlights"),
    (r"contact|personal\s*(?:info|details|data)|reach\s*me|get\s*in\s*touch", "contact"),
    (r"competenc|expertise|strength|core\s*areas|areas\s*of", "competencies"),
    (r"skill|abilit|^\s*tools\s*$|tech\s*stack|^\s*technologies\s*$|^\s*softwares?\s*$", "skills"),
    (r"experience|employment|internship|work\s*history|career\s*history|professional\s*history|^\s*work\s*$", "experience"),
    (r"education|academic|qualification|study|studies", "education"),
    (r"achievement|award|honou?r|accomplish", "achievements"),
    (r"certif|training|course|licen", "certifications"), (r"language", "languages"),
    (r"interest|hobb|passion", "interests"), (r"project|portfolio", "projects"), (r"reference|referee", "references"),
]


_FUZZY_WORDS = {"profile": "profile", "summary": "profile", "objective": "profile", "contact": "contact",
                "skills": "skills", "expertise": "competencies", "experience": "experience", "employment": "experience",
                "education": "education", "academic": "education", "achievements": "achievements",
                "awards": "achievements", "certifications": "certifications", "certificates": "certifications",
                "courses": "certifications", "languages": "languages", "language": "languages",
                "interests": "interests", "hobbies": "interests", "projects": "projects", "references": "references",
                "highlights": "highlights", "competencies": "competencies"}


def title_key(title: str) -> str:
    t = (title or "").lower()
    for rx, key in _TITLE_KEYS:
        if re.search(rx, t):
            return key
    # OCR typos ("LANCUAGE", "EDUCATlON"): close match of a word to a heading word
    import difflib
    for w in re.findall(r"[a-z]{5,}", t):
        m = difflib.get_close_matches(w, list(_FUZZY_WORDS), n=1, cutoff=0.8)
        if m:
            return _FUZZY_WORDS[m[0]]
    return ""


def _space_gaps(mask: np.ndarray) -> int:
    """Number of word gaps visible in an ink mask (column runs without ink wider than ~0.45 ink height)."""
    if mask is None or mask.size == 0:
        return 0
    col = mask.any(0)
    h = mask.shape[0]
    gaps, run = 0, 0
    for v in col:
        if not v:
            run += 1
        else:
            if run > 0.45 * h:
                gaps += 1
            run = 0
    return gaps


def contact_type(text: str) -> str:
    t = text.strip()
    if EMAIL_RX.search(t):
        return "email"
    if re.search(r"(?i)linkedin|\bin/", t):
        return "linkedin"
    if re.search(r"(?i)\bm[ao][il1|]|e-?mail|gmail|yahoo|outlook|hotmail", t) and "www" not in t.lower() \
            and re.search(r"\.\w{2,4}\s*$", t):
        return "email"                       # OCR often drops the "@" ("mail@site.com" → "maiigrsite.com")
    if URL_RX.search(t) and not re.search(r"\s{1}\w+\s\w+\s\w+", t):
        return "website"
    if PHONE_RX.search(t) and len(re.sub(r"\D", "", t)) >= 7:
        return "phone"
    return ""


# ── structure ─────────────────────────────────────────────────────────────────────────────────────

def analyse(img: np.ndarray) -> dict:
    """Returns the structure dict (lines with roles, headings, columns, sections, name/title lines)."""
    H, W = img.shape[:2]
    lines = ocr_lines(img)
    for l in lines:
        measure_line(img, l)
    lines = [l for l in lines if l.get("ink")]
    for l in lines:
        t = l["text"]
        l["words"] = max(len(t.split()), int(len(t) / 7.5))      # robust to OCR-dropped spaces
        l["upper"] = _is_upper(t)
        l["ctype"] = contact_type(t)
        l["role"] = ""
    if not lines:
        return {"lines": [], "columns": [], "headings": []}

    longish = [l for l in lines if l["words"] >= 4 and not l["upper"]] or lines
    body_size = float(np.median([_size_key(l) for l in longish]))
    body_stroke = float(np.median([l["stroke"] / _size_key(l) for l in longish]))

    # 1) section headings: short lines whose text names a section, in a consistent distinctive style
    cands = []
    for l in lines:
        t = l["text"].strip(" :|-")
        if l["words"] > 5 or len(t) > 36 or l["ctype"] or re.search(r"\d{3,}|@", t):
            continue
        key = title_key(t)
        if not key:
            continue
        # a date beside it ("Course Name … 2014-2017") makes it an item title, not a section heading
        if any(o is not l and _v_overlap(o["box"], l["box"]) > 0.5 and o["box"][0] > l["box"][2]
               and o["box"][0] - l["box"][2] < 0.45 * W and DATE_RX.search(o["text"]) for o in lines):
            continue
        distinct = (l["upper"] + (_size_key(l) > body_size * 1.12) +
                    (l["stroke"] / _size_key(l) > body_stroke * 1.18) + (_cdist(l["fg"], longish[0]["fg"]) > 60))
        l["_key"] = key
        l["_distinct"] = distinct
        cands.append(l)
    groups: list[list[dict]] = []
    for l in sorted(cands, key=lambda l: (-l["_distinct"], l["box"][1])):
        for g in groups:
            if any(_same_style(l, m, 0.18, 55) for m in g):      # single linkage: like any member
                g.append(l)
                break
        else:
            groups.append([l])

    def gscore(g):
        keys = [x["_key"] for x in g]
        return len(set(keys)) * 2 - (len(keys) - len(set(keys))) * 3 + np.mean([x["_distinct"] for x in g])
    groups.sort(key=lambda g: -gscore(g))
    headings: list[dict] = []
    if groups:
        main = groups[0]
        headings = list(main)
        main_keys = {x["_key"] for x in main}
        # a second style group (e.g. sidebar headings in a different colour) counts if it is as distinctive,
        # names sections the first group doesn't, and doesn't repeat a key (repeats = item titles)
        for g in groups[1:]:
            keys = [x["_key"] for x in g]
            far = all(min(abs(x["box"][0] - m["box"][0]) for m in main) > 0.12 * W for x in g)
            if (len(g) >= 2 and np.mean([x["_distinct"] for x in g]) >= 1.5 or len(g) == 1 and g[0]["_distinct"] >= 2 and far) \
                    and len(set(keys)) == len(keys) and not set(keys) & main_keys:
                headings += g
        # rescue: a short keyword line that clearly stands apart (blur at low dpi can split a heading style
        # into one-member groups, e.g. a sidebar's "Contact Me." / "About Me.")
        used = {x["_key"] for x in headings}
        for g in groups[1:]:
            for l in g:
                if l in headings or l["_key"] in used or l["words"] > 3 or l["_distinct"] < 1:
                    continue
                above = [o for o in lines if o is not l and o["box"][3] <= l["box"][1] + 2
                         and _h_overlap(o["box"], l["box"]) > 0.2]
                gap = (l["box"][1] - max(o["box"][3] for o in above)) if above else 9e9
                beside = [o for o in lines if o is not l and _v_overlap(o["box"], l["box"]) > 0.5
                          and 0 < o["box"][0] - l["box"][2] < 0.12 * W]
                if gap > 1.2 * _size_key(l) and not beside:
                    headings.append(l)
                    used.add(l["_key"])
        top_y = min(h["box"][1] for h in headings) - int(0.02 * H)
        # same-style lines without a known keyword are headings too (custom section titles)
        for l in lines:
            if l in headings or l["words"] > 5 or l["ctype"] or re.search(r"\d{3,}|@", l["text"]) or l["box"][1] < top_y:
                continue
            above = [o for o in lines if o is not l and o["box"][3] <= l["box"][1] and _h_overlap(o["box"], l["box"]) > 0.2]
            gap = (l["box"][1] - max(o["box"][3] for o in above)) if above else 9e9
            aligned = any(abs(l["box"][0] - h["box"][0]) < 0.04 * W or
                          abs(l["box"][0] + l["box"][2] - h["box"][0] - h["box"][2]) < 0.08 * W for h in main)
            if sum(_same_style(l, h, 0.07, 28) for h in main) >= 2 and l["upper"] == main[0]["upper"] and \
                    gap > 1.2 * _size_key(l) and aligned:
                l["_key"] = title_key(l["text"]) or "x_" + re.sub(r"[^a-z0-9]+", "_", l["text"].lower()).strip("_")[:24]
                headings.append(l)
    # a heading must not be a single word that is also a body list item in the same style as neighbours
    headings = [h for h in headings if not (h["words"] == 1 and not h["upper"] and h.get("_distinct", 0) < 2)]
    # a heading directly under another heading of the same column is an item title ("EDUCATION" → "DEGREE NAME")
    headings.sort(key=lambda h: (h["box"][1], h["box"][0]))
    keep = []
    for h in headings:
        above = [k for k in keep if _h_overlap(k["box"], h["box"]) > 0.2 or abs(k["box"][0] - h["box"][0]) < 0.04 * W]
        above = [k for k in above if 0 <= h["box"][1] - k["box"][3] < 2.2 * _size_key(k)]
        between = [l for l in lines if above and above[-1]["box"][3] <= l["box"][1] < h["box"][1]
                   and _h_overlap(l["box"], h["box"]) > 0.2]
        if above and not between:
            k = above[-1]
            if _same_style(h, k, 0.1, 35) and h["box"][1] - k["box"][3] < 0.8 * _size_key(k):
                # two-line heading ("CAREER" / "HIGHLIGHTS") → one heading
                k["text"] = k["text"] + " " + h["text"]
                k["box"] = [min(k["box"][0], h["box"][0]), k["box"][1], max(k["box"][2], h["box"][2]), h["box"][3]]
                k["ink"] = [min(k["ink"][0], h["ink"][0]), k["ink"][1], max(k["ink"][2], h["ink"][2]), h["ink"][3]]
                k["_key"] = title_key(k["text"]) or k["_key"]
                k["lines2"] = True
                h["role"] = "heading_part"
            continue
        keep.append(h)
    # repeated keys: a later instance inside the earlier same-key section is an item title ("PROJECT TITLE ONE")
    headings = []
    for h in keep:
        prev = [k for k in headings if k["_key"] == h["_key"] and k["box"][1] < h["box"][1]
                and (abs(k["box"][0] - h["box"][0]) < 0.08 * W or _h_overlap(k["box"], h["box"]) > 0.3)]
        if prev:
            p0 = prev[-1]
            between = [k for k in keep if k is not h and k is not p0 and k["_key"] != h["_key"]
                       and p0["box"][1] < k["box"][1] < h["box"][1]
                       and (abs(k["box"][0] - h["box"][0]) < 0.08 * W or _h_overlap(k["box"], h["box"]) > 0.3)]
            if not between:
                continue
        headings.append(h)
    seen_keys = set()
    for h in sorted(headings, key=lambda h: (h["box"][1], h["box"][0])):
        h["role"] = "heading"
        k = h["_key"]
        if k in seen_keys:                       # "Education" twice → keep both, suffix the second
            k = k + "_2"
        seen_keys.add(k)
        h["key"] = k

    # 2) name, title
    heads_y = min([h["box"][1] for h in headings] or [H])
    name_c = [l for l in lines if l["role"] == "" and not l["ctype"] and not re.search(r"[\d@]", l["text"])
              and 1 <= l["words"] <= 4 and l["box"][1] < H * 0.45 and len(_letters(l["text"])) >= 2]
    above = [l for l in name_c if l["box"][3] <= heads_y + 2]          # the name sits above the sections
    if above:
        name_c = above
    name_lines = []
    if name_c:
        top = max(name_c, key=lambda l: l["ink_h"] * (1.0 if l["upper"] else 1.12))
        if top["ink_h"] > 1.25 * float(np.median([l["ink_h"] for l in lines])):
            name_lines = [top]
            # stacked / split name lines of similar size right above or below
            for l in sorted(name_c, key=lambda l: abs(l["box"][1] - top["box"][1])):
                if l is top or len(name_lines) >= 3:
                    continue
                ref = name_lines[-1] if l["box"][1] > top["box"][1] else name_lines[0]
                gap = l["box"][1] - ref["box"][3] if l["box"][1] > ref["box"][1] else ref["box"][1] - l["box"][3]
                if 0.7 < l["ink_h"] / top["ink_h"] < 1.4 and gap < 1.0 * top["ink_h"] and \
                        (_h_overlap(l["box"], top["box"]) > 0.3 or abs(l["box"][0] - top["box"][0]) < top["ink_h"]):
                    name_lines.append(l)
            name_lines.sort(key=lambda l: l["box"][1])
    for l in name_lines:
        l["role"] = "name"
    title_lines = []
    if name_lines:
        nb = [min(l["box"][0] for l in name_lines), name_lines[0]["box"][1],
              max(l["box"][2] for l in name_lines), name_lines[-1]["box"][3]]
        nh = name_lines[0]["ink_h"]
        cand = [l for l in lines if l["role"] == "" and not l["ctype"] and l["words"] <= 9
                and (_h_overlap(l["box"], nb) > 0.2 or abs(l["box"][0] - nb[0]) < nh * 1.5)
                and (0 <= l["box"][1] - nb[3] < nh * 3.2 or 0 <= nb[1] - l["box"][3] < nh * 1.6)]
        cand.sort(key=lambda l: abs(l["box"][1] - nb[3]))
        if cand:
            t0 = cand[0]
            title_lines = [t0]
            for l in cand[1:]:
                if _same_style(l, t0, 0.2, 50) and abs(l["box"][1] - title_lines[-1]["box"][3]) < t0["ink_h"] * 1.6:
                    title_lines.append(l)
            title_lines.sort(key=lambda l: l["box"][1])
    for l in title_lines:
        l["role"] = "title"

    # 3) columns from heading x positions
    xs = sorted(h["box"][0] for h in headings)
    clusters: list[list[int]] = []
    for x in xs:
        if clusters and x - clusters[-1][-1] < W * 0.12:
            clusters[-1].append(x)
        else:
            clusters.append([x])
    lefts = [min(c) for c in clusters] or [0]
    # separator between two heading clusters: the widest gap between line start positions in that range
    # (a heading with an icon before it starts right of its column's body text, so "just left of the
    # heading" would hand that column's lines to its neighbour)
    content_top = min([h["box"][1] for h in headings] or [0])
    body_boxes = [l["box"] for l in lines if l["role"] not in ("name", "title") and l["box"][1] >= content_top - 4]
    seps = [0]
    for i in range(1, len(lefts)):
        lo, hi = lefts[i - 1] + 4, lefts[i]
        xs = list(range(int(lo), int(hi), 3)) or [int(hi) - 1]
        cross = [sum(1 for b in body_boxes if b[0] < x < b[2]) for x in xs]
        m = min(cross)
        # the longest run of x positions crossed by the fewest lines = the gutter; split in its middle…
        best, run = (0, xs[0], xs[0]), None
        for x, c_ in zip(xs, cross):
            if c_ == m:
                run = (run[0], x) if run else (x, x)
                if run[1] - run[0] > best[0]:
                    best = (run[1] - run[0], run[0], run[1])
            else:
                run = None
        g0, g1 = best[1], best[2]
        # …and the right column begins where its own lines start
        right_starts = [b[0] for b in body_boxes if g1 <= b[0] <= hi]
        seps.append(int(min(right_starts) - W * 0.01) if right_starts else int((g0 + g1) / 2))
    seps.append(W)

    def col_of(x: float) -> int:
        for i in range(len(lefts)):
            if seps[i] <= x < seps[i + 1]:
                return i
        return len(lefts) - 1

    for l in lines:
        l["col"] = col_of(l["box"][0])
    columns = []
    for ci in range(len(lefts)):
        cl = [l for l in lines if l["col"] == ci and l["role"] not in ("name", "title")]
        hs = sorted([h for h in headings if h["col"] == ci], key=lambda h: h["box"][1])
        body = [l for l in cl if l["role"] == ""]
        x0 = min([l["box"][0] for l in cl] or [lefts[ci]])
        rights = sorted([l["box"][2] for l in cl if l["box"][2] <= seps[ci + 1] + W * 0.02] or [seps[ci + 1]])
        x1 = rights[-2] if len(rights) > 3 else rights[-1]
        top = hs[0]["box"][1] if hs else min([l["box"][1] for l in body] or [0])
        bottom = max([l["box"][3] for l in cl] or [H])
        columns.append({"i": ci, "x0": x0, "x1": x1, "sep0": seps[ci], "sep1": seps[ci + 1], "top": top,
                        "bottom": bottom, "headings": hs})

    # 4) header contact (above the first heading of its column, or anywhere outside sections)
    for l in lines:
        if l["role"] == "" and l["ctype"] and l["box"][1] < columns[l["col"]]["top"]:
            l["role"] = "header_contact"
    hc = [l for l in lines if l["role"] == "header_contact"]
    if hc:
        for l in lines:
            if l["role"] != "" or l["box"][1] >= columns[l["col"]]["top"] or l["words"] > 8:
                continue
            near = [o for o in hc if abs(o["box"][0] - l["box"][0]) < 3 * PX_PER_MM
                    and abs(o["box"][1] - l["box"][1]) < 3.2 * (o["box"][3] - o["box"][1])]
            if near:
                l["role"] = "header_contact"
                l["ctype"] = "location" if re.search(r"\d|,", l["text"]) else "website"

    # 5) sections and item roles
    sections = []
    # a contact heading with its details beside it (a horizontal strip, e.g. "■ CONTACT  ☎ 000…  ✉ mail") owns
    # every short line in its band, whichever column those lines fall in
    strip: dict = {}
    for h in headings:
        if h.get("key") != "contact":
            continue
        hh = h["box"][3] - h["box"][1]
        band = [l for l in lines if l["role"] == "" and l is not h and l["words"] <= 6
                and h["box"][1] - 3.2 * hh <= l["box"][1] <= h["box"][3] + 1.5 * hh
                and (l["box"][0] > h["box"][2] or (l["ctype"] and _v_overlap(l["box"], h["box"]) > 0.3))]
        beside = [l for l in band if _v_overlap(l["box"], h["box"]) > 0.4 and l["ctype"]]
        band = [l for l in band if l["ctype"] or len(l["text"]) <= 30]
        if beside:
            for l in band:
                strip[l["id"]] = h["key"]
    for col in columns:
        hs = col["headings"]
        for i, h in enumerate(hs):
            y0 = h["box"][1]
            y1 = hs[i + 1]["box"][1] if i + 1 < len(hs) else col["bottom"] + int(3 * PX_PER_MM)
            sl = [l for l in lines if l["col"] == col["i"] and l["role"] == "" and y0 < l["box"][1] < y1
                  and l is not h and l["id"] not in strip]
            if h.get("key") == "contact":
                sl += [l for l in lines if strip.get(l["id"]) == h["key"] and l["role"] == "" and l not in sl]
            # lines further right that belong to this column's rows (right-aligned dates) are in col already
            for l in sl:
                l["sec"] = h["key"]
            key = re.sub(r"_2$", "", h["key"])
            paras = [l for l in sl if l["words"] >= 6]
            if (key == "contact" or key.startswith("x_")) and len(paras) >= 2 and                     sum(l["words"] for l in paras) >= 20 and not any(l["ctype"] for l in sl):
                key = "profile"                  # "PERSONAL INFORMATION" holding a summary paragraph
            sec = {"key": key, "heading": h,
                   "col": col["i"], "y0": y0, "y1": y1, "lines": sl}
            _item_roles(sec)
            sections.append(sec)
        # implicit profile: a paragraph above the column's first heading (no title in the reference)
        above = [l for l in lines if l["col"] == col["i"] and l["role"] == "" and l["box"][1] < col["top"]
                 and l["words"] >= 4]
        if len(above) >= 2 and not any(s["key"] == "profile" for s in sections):
            y0 = min(l["box"][1] for l in above)
            for l in above:
                l["role"] = "body"
                l["sec"] = "profile"
            sections.append({"key": "profile", "heading": None, "col": col["i"], "y0": y0,
                             "y1": max(l["box"][3] for l in above) + 2, "lines": above, "implicit": True})
            col["top"] = min(col["top"], y0)
    for l in lines:
        if l["role"] == "" and l.get("sec") is None:
            l["role"] = "header_other" if l["box"][1] < columns[l["col"]]["top"] else "loose"
    return {"lines": lines, "headings": headings, "columns": columns, "sections": sections,
            "name_lines": name_lines, "title_lines": title_lines, "body_size": body_size, "W": W, "H": H}


_ITEM_SECTIONS = {"experience", "projects", "education"}


def _item_roles(sec: dict) -> None:
    """Assigns item_title / sub / meta / meta_right / body / list / subhead roles inside one section."""
    ls = sorted(sec["lines"], key=lambda l: (l["box"][1], l["box"][0]))
    if not ls:
        return
    key = sec["key"]
    if key == "contact":
        for l in ls:
            l["role"] = "contact"
        return
    # body style = the most common style among the section's lines
    best, best_n = ls[0], -1
    for l in ls:
        n = sum(_same_style(l, o, 0.15, 40) for o in ls)
        if n > best_n:
            best, best_n = l, n
    body = best
    if key not in _ITEM_SECTIONS or len(ls) < 2:
        role = "body" if key in ("profile",) else "list"
        for l in ls:
            l["role"] = role
            # an uppercase line inside a mostly lower-case list ("OTHER TECHNOLOGIES") is a sub-heading
            lower_share = sum(1 for o in ls if not o["upper"] and len(_letters(o["text"])) >= 4) / max(1, len(ls))
            if role == "list" and l["upper"] and len(_letters(l["text"])) >= 6 and l is not ls[0] and \
                    lower_share >= 0.5 and len(l["text"]) <= 30:
                l["role"] = "subhead"
        return
    first = ls[0]
    title_style = first if not _same_style(first, body, 0.12, 35) or first["words"] <= 8 else None
    for l in ls:
        if title_style is not None and _same_style(l, title_style, 0.12, 40) and                 not (_same_style(l, body, 0.08, 25) and l["words"] > 8):
            l["role"] = "item_title"
    # a title-style line directly under a title (no gap) is the item's second line → sub
    titles = [l for l in ls if l["role"] == "item_title"]
    for a, b in zip(titles, titles[1:]):
        if a["role"] == "item_title" and 0 <= b["box"][1] - a["box"][3] < 0.55 * _size_key(a) and                 not any(o for o in ls if a["box"][3] <= o["box"][1] < b["box"][1] and o is not b and o["role"] != "meta_right"):
            b["role"] = "sub"
    titles = [l for l in ls if l["role"] == "item_title"]
    for l in ls:
        if l["role"]:
            continue
        same_row = [t for t in titles if _v_overlap(l["box"], t["box"]) > 0.5 and l["box"][0] > t["box"][2]]
        if same_row:
            l["role"] = "meta_right"
            l["meta_of"] = same_row[0]["id"]
    for l in ls:
        if l["role"]:
            continue
        prev = [t for t in ls if t["box"][3] <= l["box"][1] + 2 and t is not l and t["role"] != "meta_right"]
        prev = prev[-1] if prev else None
        pr = prev.get("role") if prev is not None else None
        short = len(l["text"]) < 48
        if pr == "item_title" and not _same_style(l, body, 0.1, 30) and short:
            l["role"] = "meta" if DATE_RX.search(l["text"]) and len(l["text"]) < 40 else "sub"
            continue
        if pr in ("sub",) and short and (DATE_RX.search(l["text"]) or not _same_style(l, body, 0.08, 25))                 and not l.get("inner_bullet"):
            l["role"] = "meta"
            continue
        l["role"] = "body"
