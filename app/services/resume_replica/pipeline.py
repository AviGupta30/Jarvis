"""
pipeline.py — Reference resume (image/PDF) → exact template spec (cached per file hash).

  ingest  → page image at 200 dpi (viewer chrome trimmed)
  measure → OCR lines with ink/colour/weight, name/title/headings/columns/sections/item roles
  plate   → background with all content erased + transparent assets (heading decorations, bullets, icons,
            timeline node) + skill-graphic measurements + photo frame
  fonts   → family/weight/letter-spacing per text role from the reference's own words (fontmatch.py)
  tokens  → sizes, colours and the vertical rhythm (ink-top to ink-top gaps) in mm
The spec is everything exact_render.py needs; no vision-model call is involved.
"""
from __future__ import annotations

import json
import os
import re
import time

import numpy as np

from .ingest import PX_PER_MM, load_reference

SPEC_VERSION = 4
_BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
SPEC_DIR = os.path.join(_BASE, "app", "memory", "replica_docs")
ASSET_DIR = os.path.join(_BASE, "data", "uploads", "resumes", "replica")
MM = PX_PER_MM


def _mm(v) -> float:
    return round(float(v) / MM, 2)


def _file_hash(path: str) -> str:
    import hashlib
    h = hashlib.sha1()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def spec_path(sha1: str) -> str:
    return os.path.join(SPEC_DIR, f"exact_{sha1}.json")


def load_spec(sha1: str) -> dict | None:
    try:
        with open(spec_path(sha1), encoding="utf-8") as f:
            spec = json.load(f)
        if spec.get("v") == SPEC_VERSION and os.path.exists(spec["page"]["plate"]):
            return spec
    except Exception:
        pass
    return None


# ── fonts per style key ────────────────────────────────────────────────────────────────────────────

def _style_key(l: dict) -> str | None:
    r = l["role"]
    c = l.get("col", 0)
    if r in ("name", "title"):
        return r
    if r == "heading":
        return f"head{c}"
    if r in ("item_title", "sub", "meta", "meta_right"):
        return f"{r}{c}"
    if r in ("body", "list"):
        return f"{r}{c}"
    if r == "contact":
        return f"contact{c}"
    if r == "subhead":
        return f"subhead{c}"
    if r == "header_contact":
        return "hcontact"
    return None


def _mostly_lower(text: str) -> bool:
    letters = re.sub(r"[^A-Za-z]", "", text or "")
    return len(letters) >= 4 and sum(ch.islower() for ch in letters) >= 0.3 * len(letters)


def _font_styles(ref: dict, s: dict, log) -> dict:
    """Matches a font for every style key and measures size / letter-spacing / colour / pitch."""
    from .fontmatch import FontMatcher, ref_map
    img = ref["img"]
    src_scale = img.shape[1] / max(1, ref["src_size"][0]) if not ref.get("is_pdf") else 1.0
    groups: dict[str, list] = {}
    for l in s["lines"]:
        k = _style_key(l)
        if k and l.get("ink"):
            l["skey"] = k
            groups.setdefault(k, []).append(l)
    samples, owners = [], []
    for k, ls in groups.items():
        good = [l for l in ls if l["conf"] >= 0.8 and 3 <= len(l["text"]) <= 44 and not l.get("inner_bullet")]
        good = good or [l for l in ls if len(l["text"]) >= 2]
        good.sort(key=lambda l: (-(min(len(l["text"]), 28)) * (1.0 if not l["upper"] else 0.8)))
        for l in good[:1 if k in ("name", "title") or len(ls) <= 2 else 2]:
            r = ref_map(img, l, src_scale)
            if r:
                samples.append({"text": l["text"], "ref": r[0], "rw": r[1], "rh": r[2], "src_h": r[3],
                                "lock_ls": _mostly_lower(l["text"])})
                owners.append(k)
    styles: dict = {}
    if not samples:
        return styles
    t0 = time.time()
    log(f"🔤 Identifying fonts ({len(samples)} text samples × the font library)…")
    from .fontmatch import identify
    res = identify(samples, workers=4, log=log)
    per_key: dict[str, dict] = {}
    for k, r in zip(owners, res):
        if not r:
            continue
        floor = r[-1]["score"]
        d = per_key.setdefault(k, {"n": 0, "scores": {}, "ls": {}})
        d["n"] += 1
        seen = set()
        for x in r:
            fw = (x["family"], x["weight"])
            d["scores"][fw] = d["scores"].get(fw, 0.0) + x["score"]
            d["ls"].setdefault(fw, []).append(x["ls_em"])
            seen.add(fw)
        for fw in list(d["scores"]):
            if fw not in seen:
                d["scores"][fw] += floor - 0.05
    choice = _choose_families(per_key)
    # metrics of every line in its key's font → size from the line's own ink height
    items, refs = [], []
    for k, ls in groups.items():
        if k not in choice:
            continue
        f, w = choice[k]
        lsv = float(np.median(per_key[k]["ls"].get((f, w), [0.0])))
        if sum(_mostly_lower(l["text"]) for l in ls) > len(ls) / 2:
            lsv = 0.0                                   # lower-case text: no tracking (see fontmatch lockLs)
        per_key[k]["ls_final"] = lsv
        for l in ls:
            items.append({"text": l["text"], "family": f, "weight": w, "ls": lsv})
            refs.append((k, l))
    with FontMatcher(faces=sorted(set(choice.values()))) as fm:
        mets = fm.metrics(items)
    log(f"   fonts matched in {time.time() - t0:.0f}s")
    sizes: dict[str, list] = {}
    for (k, l), m in zip(refs, mets):
        if not m:
            continue
        ink_em = m["ink_asc_em"] + m["ink_desc_em"]
        if ink_em <= 0.05:
            continue
        fs = (l["ink"][3] - l["ink"][1]) / ink_em / MM
        # long lower-case lines: the ink *width* gives the size far more precisely than the (blurred) height
        w_em = m.get("ink_right_em", 0) + m.get("ink_left_em", 0) * -1
        if _mostly_lower(l["text"]) and len(l["text"]) >= 6 and w_em > 0.5:
            fs_w = (l["ink"][2] - l["ink"][0]) / w_em / MM
            if 0.6 < fs_w / fs < 1.4:
                fs = 0.75 * fs_w + 0.25 * fs
        sizes.setdefault(k, []).append((fs, m))
        l["fs_mm"] = fs
        l["m"] = m
    for k, (f, w) in choice.items():
        ls = groups[k]
        szs = sizes.get(k) or []
        fs = float(np.median([x[0] for x in szs])) if szs else 3.5
        m0 = szs[0][1] if szs else {"asc_em": 0.9, "desc_em": 0.25, "ink_asc_em": 0.72, "ink_desc_em": 0.0}
        cols = np.array([[int(l["fg"][i:i + 2], 16) for i in (1, 3, 5)] for l in ls])
        color = "#%02x%02x%02x" % tuple(int(v) for v in np.median(cols, axis=0))
        votes = [l["upper"] for l in ls if len(re.sub(r"[^A-Za-z]", "", l["text"])) >= 5]
        upper = sum(votes) > len(votes) / 2 if votes else (all(l["upper"] for l in ls) and
                                                             k.startswith(("head", "subhead", "name", "title")))
        ink_asc = float(np.median([x[1]["ink_asc_em"] for x in szs])) if szs else 0.72
        def _lum(h):
            v = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
            v = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in v]
            return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]
        rcs = []
        for l in ls:
            a_, b_ = _lum(l["fg"]), _lum(l["bg"])
            rcs.append((max(a_, b_) + 0.05) / (min(a_, b_) + 0.05))
        styles[k] = {"ref_contrast": round(float(np.median(rcs)), 2) if rcs else 4.5,
                     "family": f, "weight": int(w), "size": round(fs, 3),
                     "ls": round(float(per_key[k].get("ls_final", np.median(per_key[k]["ls"].get((f, w), [0.0])))), 4),
                     "color": color, "upper": bool(upper), "asc": round(m0["asc_em"], 4), "desc": round(m0["desc_em"], 4),
                     "ink_asc": round(ink_asc, 4), "n": len(ls)}
    return styles


def _choose_families(per_key: dict, max_fams: int = 3) -> dict:
    """Designs use 1–3 families: pick the family set that best explains every text role together, then the
    best weight per role within it (look-alike faces at low resolution otherwise scatter across families)."""
    if not per_key:
        return {}
    mean = {k: {fw: sc / d["n"] for fw, sc in d["scores"].items()} for k, d in per_key.items()}
    # digits / e-mails / dates hardly tell typefaces apart (a mono font "fits" a phone number): those roles
    # don't vote on the design's families, they only pick within them
    weight = {k: (0 if k.startswith(("contact", "hcontact", "meta")) else d["n"]) for k, d in per_key.items()}
    if not any(weight.values()):
        weight = {k: d["n"] for k, d in per_key.items()}
    fams = {fw[0] for m in mean.values() for fw in m}

    def best_in(k, F):
        c = [(sc, fw) for fw, sc in mean[k].items() if fw[0] in F]
        return max(c) if c else (min(mean[k].values()) - 0.1, None)

    def total(F):
        return sum(weight[k] * best_in(k, F)[0] for k in mean)
    F: set = set()
    base = sum(weight.values())
    while len(F) < max_fams:
        cand = max(fams - F, key=lambda f: total(F | {f}), default=None)
        if cand is None:
            break
        gain = total(F | {cand}) - (total(F) if F else -1e9)
        if F and gain < 0.012 * base:
            break
        F.add(cand)
    out = {}
    main_fam = max(F, key=lambda f: sum(weight[k] for k in mean if (best_in(k, {f})[1] or ("", 0))[0] == f)) if F else None
    from .fonts import load_index
    idx = load_index()
    for k in mean:
        fw = best_in(k, F)[1]
        if fw is None:
            # none of the design's families among this role's candidates: use the main family at the weight
            # this role's own best match had (an outsider family from 1–2 blurry lines is usually wrong)
            own = max(mean[k].items(), key=lambda t: t[1])[0]
            ws = [int(w) for w in (idx.get(main_fam) or {}).get("weights", {})] if main_fam else []
            fw = (main_fam, min(ws, key=lambda w: abs(w - own[1]))) if ws else own
        out[k] = fw
    return out


# ── rhythm ─────────────────────────────────────────────────────────────────────────────────────────

def _ink_top(l) -> float:
    return l["ink"][1] / MM


def _pitch_of(lines: list, key: str) -> float | None:
    """Line pitch (mm) of wrapped lines of one style: consecutive same-key lines without a new bullet."""
    vals = []
    ls = sorted([l for l in lines if l.get("skey") == key], key=lambda l: (l.get("col", 0), l["ink"][1]))
    widest = {}
    for l in ls:
        widest[l.get("col")] = max(widest.get(l.get("col"), 0), l["ink"][2] - l["ink"][0])
    for a, b in zip(ls, ls[1:]):
        if a.get("col") != b.get("col") or b.get("lead_box") or a.get("sec") != b.get("sec"):
            continue
        if a["ink"][2] - a["ink"][0] < 0.55 * widest.get(a.get("col"), 1):
            continue                                  # only a line that ran to the edge wraps
        d = _ink_top(b) - _ink_top(a)
        fs = a.get("fs_mm") or 3
        if 0.9 * fs < d < 1.9 * fs:
            vals.append(d)
    return float(np.median(vals)) if vals else None


def _section_tokens(sec: dict, lines_sorted: list, deco_bottom_mm: float | None) -> dict:
    """Ink-top → ink-top gaps between line roles inside one section (mm)."""
    t: dict[str, list] = {}

    def add(name, v):
        t.setdefault(name, []).append(round(v, 2))
    if lines_sorted:
        if deco_bottom_mm is not None:
            add("head_first", _ink_top(lines_sorted[0]) - deco_bottom_mm)
        prev = None
        for l in lines_sorted:
            if l["role"] == "meta_right":
                continue
            if prev is not None:
                d = _ink_top(l) - _ink_top(prev)
                ra, rb = prev["role"], l["role"]
                if rb == "item_title":
                    add("item_gap", d)
                elif ra == "item_title" and rb in ("sub", "meta"):
                    add("title_sub", d)
                elif ra in ("sub",) and rb == "meta":
                    add("sub_meta", d)
                elif ra in ("item_title", "sub", "meta") and rb in ("body", "list"):
                    add("head_body", d)
                elif ra in ("body", "list", "contact") and rb in ("body", "list", "contact"):
                    add("new_item" if l.get("lead_box") or prev.get("skey") != l.get("skey") else "wrap", d)
            prev = l
    return {k: float(np.median(v)) for k, v in t.items()}


# ── spec ───────────────────────────────────────────────────────────────────────────────────────────

def _align(lines: list, page_w_px: int) -> str:
    """left / center / right for a stacked group (name + title) from their ink boxes."""
    if len(lines) < 2:
        x0, _, x1, _ = lines[0]["ink"]
        c = (x0 + x1) / 2
        return "center" if abs(c - page_w_px / 2) < 0.02 * page_w_px else "left"
    lefts = [l["ink"][0] for l in lines]
    rights = [l["ink"][2] for l in lines]
    cents = [(l["ink"][0] + l["ink"][2]) / 2 for l in lines]
    sl, sr, sc = np.ptp(lefts), np.ptp(rights), np.ptp(cents)
    m = min(sl, sr, sc)
    return "left" if m == sl else ("right" if m == sr else "center")


def _safe_print(msg: str) -> None:
    try:
        print(msg)
    except Exception:
        print(msg.encode("ascii", "replace").decode())


def analyse_reference(image_path: str, log=_safe_print, force: bool = False) -> dict | None:
    """Returns the exact-template spec for a reference resume image/PDF (cached), or None if it isn't a resume."""
    sha1 = _file_hash(image_path)
    if not force:
        cached = load_spec(sha1)
        if cached:
            return cached
    from . import measure, plate
    t0 = time.time()
    ref = load_reference(image_path)
    img = ref["img"]
    H, W = img.shape[:2]
    log("🔍 Reading the layout (text, columns, sections)…")
    s = measure.analyse(img)
    if not s["sections"] and not s["name_lines"]:
        return None
    out_dir = os.path.join(ASSET_DIR, sha1[:16])
    log("🧽 Separating the design from its sample text (background plate, headings, icons)…")
    info = plate.build(img, s, out_dir, ref["page_h_mm"], overlays=ref.get("overlays"))
    styles = _font_styles(ref, s, log)

    lines = s["lines"]
    spec: dict = {"v": SPEC_VERSION, "sha1": sha1, "source": os.path.basename(image_path),
                  "source_path": os.path.abspath(image_path),
                  "page": {"h_mm": 297.0, "ref_h_mm": round(ref["page_h_mm"], 1), "plate": info["plate"],
                           "plate2": info["plate2"], "src_dpi": ref["src_dpi"], "partial": ref["partial"],
                           "letter": ref["letter"]},
                  "styles": styles, "created": time.time()}
    fonts: dict = {}
    for st in styles.values():
        fonts.setdefault(st["family"], set()).add(st["weight"])
    spec["fonts"] = {f: sorted(w) for f, w in fonts.items()}

    def line_box(l):
        x0, y0, x1, y1 = l["ink"]
        return {"x": _mm(x0), "y": _mm(y0), "x1": _mm(x1), "y1": _mm(y1), "key": l.get("skey"),
                "text": l["text"], "fs": round(l.get("fs_mm") or 0, 3),
                "room": _mm(l["room_px"]) if l.get("room_px") else None, "bg": l.get("patch") or l.get("bg"),
                "room_kind": l.get("room_kind"), "room_hard": _mm(l["room_hard_px"]) if l.get("room_hard_px") else None}

    # header: name / title as absolute slots
    if s["name_lines"]:
        al = _align(s["name_lines"] + s["title_lines"], W)
        spec["name"] = {"align": al, "lines": [line_box(l) for l in s["name_lines"]]}
    if s["title_lines"]:
        al = _align(s["name_lines"] + s["title_lines"], W) if s["name_lines"] else "left"
        spec["title"] = {"align": al, "lines": [line_box(l) for l in s["title_lines"]]}
    if info.get("photo"):
        p = info["photo"]
        spec["photo"] = {"box": p["box_mm"], "radius": p["radius_mm"], "circle": p["circle"]}
    hc = []
    for l in lines:
        if l["role"] == "header_contact":
            b = line_box(l)
            b["type"] = l.get("ctype") or measure.contact_type(l["text"]) or "website"
            ic = info["header_icons"].get(b["type"])
            if ic and l.get("icon_box"):
                b["icon"] = {"file": ic["file"], "box": [_mm(v) for v in l["icon_box"]]}
            hc.append(b)
    spec["hcontact"] = hc

    # columns + sections
    pitches = {k: _pitch_of(lines, k) for k in styles}
    for k, st in styles.items():
        st["pitch"] = round(pitches[k], 3) if pitches.get(k) else round(st["size"] * 1.32, 3)
    cols = []
    for col in s["columns"]:
        csecs = sorted([x for x in s["sections"] if x["col"] == col["i"]], key=lambda x: x["y0"])
        body_lines = [l for x in csecs if x["key"] != "contact" for l in x["lines"]
                      if l["role"] in ("body", "list") and not l.get("lead_box")]
        # column-level bullet position: only real bullets (body lines of item sections), never icon rows
        bullet_lines = [l for x in csecs if x["key"] in ("experience", "projects", "education") for l in x["lines"]
                        if l.get("lead_box") and l["role"] == "body"]
        c = {"x0": _mm(col["x0"]), "x1": _mm(col["x1"]), "top": _mm(col["top"]),
             "bottom": _mm(max([l["ink"][3] for x in csecs for l in x["lines"]] or [col["bottom"]])),
             "text_x": _mm(np.median([l["ink"][0] for l in body_lines])) if body_lines else _mm(col["x0"]),
             "sections": []}
        if bullet_lines:
            c["bullet_x"] = _mm(np.median([l["lead_box"][0] for l in bullet_lines]))
            c["bullet_text_x"] = _mm(np.median([l["ink"][0] for l in bullet_lines]))
        prev_last = None
        for x in csecs:
            sid = f"{x['key']}@{x['col']}@{x['y0']}"
            si = info["sections"].get(sid, {})
            h = x.get("heading")
            ls = sorted(x["lines"], key=lambda l: (l["ink"][1], l["ink"][0]))
            sec = {"key": x["key"], "title": h["text"] if h else "", "implicit": bool(x.get("implicit")),
                   "head_key": h.get("skey") if h else None}
            deco = si.get("deco")
            if h is not None:
                sec["head_ink"] = [_mm(v) for v in h["ink"]]
            if deco and deco.get("kind") != "none":
                bx0, by0, bx1, by1 = deco["box"]
                tx0, ty0, tx1, ty1 = deco["text"]
                sec["deco"] = {"file": deco["file"], "box": [_mm(bx0), _mm(by0), _mm(bx1), _mm(by1)],
                               "text": [_mm(tx0), _mm(ty0), _mm(tx1), _mm(ty1)], "kind": deco["kind"],
                               "on_box": deco.get("on_box", False)}
                top_mm, bottom_mm = _mm(by0), _mm(by1)
            elif h is not None:
                top_mm, bottom_mm = _mm(h["ink"][1]), _mm(h["ink"][3])
            else:
                top_mm = bottom_mm = _mm(ls[0]["ink"][1]) if ls else _mm(x["y0"])
            r = (si.get("deco") or {}).get("rule")
            if r:
                sec["rule"] = {"color": r["color"], "h": _mm(r["h"]), "gap": _mm(r["gap"]), "len": _mm(r["len"]),
                               "to_edge": r["to_edge"], "dy": _mm(r["dy"])}
            sec["top"] = top_mm
            sec["head_bottom"] = bottom_mm
            sec["tokens"] = _section_tokens(x, ls, bottom_mm if h is not None else None)
            if prev_last is not None:
                sec["tokens"]["sec_gap"] = round(top_mm - _ink_top(prev_last), 2)
                sec["tokens"]["prev_key"] = prev_last.get("skey")
            prev_last = ls[-1] if ls else (h if h else prev_last)
            # leading glyphs: representative bullet (body/list) and per-type contact icons
            leads = si.get("leads") or []
            rep = [g for g in leads if g["role"] in ("body", "list")]
            if rep:
                g = rep[len(rep) // 2]
                ln = next((l for l in ls if l["id"] == g["line"]), None)
                sec["lead"] = {"file": g["file"], "w": g["w_mm"], "h": g["h_mm"],
                               "dx": round(_mm(ln["ink"][0]) - _mm(g["box"][0]), 2) if ln else 3.0,
                               "dy": round(_mm(g["box"][1]) - _mm(ln["ink"][1]), 2) if ln else 0.0,
                               "all_same": len({(round(x_["w_mm"]), round(x_["h_mm"])) for x_ in rep}) == 1}
            icons = [g for g in leads if g["role"] in ("contact",) or x["key"] == "contact"]
            if icons:
                sec["icons"] = []
                for g in icons:
                    ln = next((l for l in ls if l["id"] == g["line"]), None)
                    sec["icons"].append({"file": g["file"], "w": g["w_mm"], "h": g["h_mm"], "ctype": g.get("ctype") or "",
                                         "dx": round(_mm(ln["ink"][0]) - _mm(g["box"][0]), 2) if ln else 3.0,
                                         "dy": round(_mm(g["box"][1]) - _mm(ln["ink"][1]), 2) if ln else 0.0})
            if x["key"] == "contact":
                # label/value pairs ("Phone" / "+123…"): short non-contact lines followed by a value line
                labels = [l for l in ls if not l.get("ctype") and re.fullmatch(
                    r"(?i)\s*(phone|mobile|tel(ephone)?|e-?mail|mail|address|location|web(site)?|linked\s*in|github|portfolio)\s*:?\s*",
                    l["text"])]
                values = [l for l in ls if l not in labels]
                if len(labels) >= 2 and len(values) >= 2:
                    sec["contact_labels"] = {"key": labels[0].get("skey"), "texts": [l["text"] for l in labels]}
            sh = [l for l in ls if l["role"] == "subhead"]
            if sh:
                l0 = sh[0]
                before = [l for l in ls if l["ink"][1] < l0["ink"][1]]
                after = [l for l in ls if l["ink"][1] > l0["ink"][1]]
                sec["subhead"] = {"text": l0["text"], "key": l0.get("skey"), "x": _mm(l0["ink"][0]),
                                  "after": round(_mm(after[0]["ink"][1]) - _mm(l0["ink"][1]), 2) if after else None}
            g = si.get("graphics") or {}
            gm = {}
            for gk, gv in g.items():
                gm[gk] = gv
            sec["graphics"] = gm
            sec["roles"] = [{"role": l["role"], "key": l.get("skey"), "x": _mm(l["ink"][0]), "x1": _mm(l["ink"][2]),
                             "y": _mm(l["ink"][1]), "lead": bool(l.get("lead_box")), "text": l["text"][:60]}
                            for l in ls]
            c["sections"].append(sec)
        cols.append(c)
    spec["columns"] = cols
    spec["analysis_s"] = round(time.time() - t0, 1)
    os.makedirs(SPEC_DIR, exist_ok=True)
    with open(spec_path(sha1), "w", encoding="utf-8") as f:
        json.dump(spec, f, ensure_ascii=False, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    return spec
