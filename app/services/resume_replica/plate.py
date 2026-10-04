"""
plate.py — The reference page minus everything that depends on content = the exact background ("plate").

Fixed design (bands, sidebars, diagonal splits, waves, decor, rules that span the page) stays as the original
pixels. Content-dependent parts are cut out first as transparent assets, then erased and filled from the
nearest background pixel:
  * every OCR text glyph (name, title, headings, body…)
  * the photo (its frame/ring stays)
  * section contents: heading decorations, bullets, icons, skill bars/dots/chips, timeline line + nodes
Assets: heading decoration per heading (9-slice ready, text removed), leading glyph per section (bullet/icon),
contact icons by type, timeline (colour/width + node image), skill-graphic measurements.
"""
from __future__ import annotations

import os
import re

import numpy as np

from .ingest import PX_PER_MM
from .measure import _hex, contact_type

MM = PX_PER_MM


def _bgr(hexc: str) -> np.ndarray:
    return np.array([int(hexc[5:7], 16), int(hexc[3:5], 16), int(hexc[1:3], 16)], np.int16)


# ── background classification ──────────────────────────────────────────────────────────────────────

def background_mask(img: np.ndarray):
    """True where a pixel belongs to a large flat colour region (page, sidebar, header band, diagonal split…)."""
    import cv2
    H, W = img.shape[:2]
    small = cv2.resize(img, (W // 2, H // 2), interpolation=cv2.INTER_AREA)
    Z = small.reshape(-1, 3).astype(np.float32)
    sample = Z[np.random.default_rng(0).choice(len(Z), min(60000, len(Z)), replace=False)]
    k = 14
    _, _, centers = cv2.kmeans(sample, k, None, (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.5),
                               3, cv2.KMEANS_PP_CENTERS)
    d = np.sqrt(((Z[:, None, :] - centers[None, :, :]) ** 2).sum(-1))
    lab = d.argmin(1)
    lab[d.min(1) > 26] = -1
    lab = lab.reshape(small.shape[:2])
    bg = np.zeros(small.shape[:2], bool)
    regions = np.zeros(small.shape[:2], np.int32)          # one id per (colour cluster, connected piece)
    rid = 0
    area_min = 0.012 * small.shape[0] * small.shape[1]
    for c in range(k):
        m = (lab == c).astype(np.uint8)
        n, cc, stats, _ = cv2.connectedComponentsWithStats(m, connectivity=4)
        for i in range(1, n):
            x, y, w, h, a = stats[i]
            if (a >= area_min and h >= 18 * MM / 2) or a >= 0.05 * small.size / 3:
                piece = cc == i
                bg |= piece
                rid += 1
                regions[piece] = rid
    # (full-res mask, half-resolution region ids for _bg_model)
    return cv2.resize(bg.astype(np.uint8), (W, H), interpolation=cv2.INTER_NEAREST).astype(bool), regions


def _components(mask: np.ndarray):
    import cv2
    n, cc, stats, cent = cv2.connectedComponentsWithStats(mask.astype(np.uint8), connectivity=8)
    return n, cc, stats


def _rgba(img: np.ndarray, alpha: np.ndarray) -> np.ndarray:
    import cv2
    a = cv2.GaussianBlur(alpha.astype(np.float32), (3, 3), 0.6)
    out = np.dstack([img, (np.clip(a, 0, 1) * 255).astype(np.uint8)])
    return out


def _save(path: str, arr: np.ndarray) -> str:
    import cv2
    os.makedirs(os.path.dirname(path), exist_ok=True)
    ok, buf = cv2.imencode(".png", arr)
    if ok:
        buf.tofile(path)
    return path


# ── main ───────────────────────────────────────────────────────────────────────────────────────────

def build(img: np.ndarray, s: dict, out_dir: str, page_h_mm: float, overlays: list | None = None) -> dict:
    """s = measure.analyse() result. Writes plate.png / plate2.png / crops into out_dir. Returns asset info."""
    import cv2
    H, W = img.shape[:2]
    bg, regions = background_mask(img)
    lines = s["lines"]
    info: dict = {"crops": {}, "sections": {}, "photo": None, "header_icons": {}}

    # text ink (exact glyph pixels) for every OCR line
    text_mask = np.zeros((H, W), bool)
    for l in lines:
        if l.get("ink") and l.get("mask") is not None:
            x0, y0, x1, y1 = l["ink"]
            text_mask[y0:y1, x0:x1] |= l["mask"][:y1 - y0, :x1 - x0]
    nonbg = ~bg | text_mask
    erase = np.zeros((H, W), bool)
    # glyph erase mask: looser than the ink mask, so anti-aliased/upscaled edges don't leave a ghost outline
    soft_text = np.zeros((H, W), bool)
    for l in lines:
        if not l.get("ink"):
            continue
        x0, y0, x1, y1 = l["box"]
        x0, y0, x1, y1 = max(0, x0 - 3), max(0, y0 - 3), min(W, x1 + 3), min(H, y1 + 3)
        d = np.abs(img[y0:y1, x0:x1].astype(np.int16) - _bgr(l["bg"])).sum(-1)
        soft_text[y0:y1, x0:x1] |= d > 24
    soft_text &= cv2.dilate(text_mask.astype(np.uint8), np.ones((9, 9), np.uint8)).astype(bool)
    erase |= cv2.dilate(soft_text.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool)

    n, cc, stats = _components(nonbg & ~text_mask)

    def comps_in(x0, y0, x1, y1, frac=0.8, min_area=3):
        """component ids whose pixels lie mostly inside the rectangle."""
        x0, y0 = max(0, int(x0)), max(0, int(y0))
        x1, y1 = min(W, int(x1)), min(H, int(y1))
        if x1 <= x0 or y1 <= y0:
            return []
        ids, cnt = np.unique(cc[y0:y1, x0:x1], return_counts=True)
        out = []
        for i, c in zip(ids, cnt):
            if i == 0 or stats[i, 4] < min_area:
                continue
            if c >= frac * stats[i, 4]:
                out.append(int(i))
        return out

    # ── photo ──
    photo = _find_photo(img, s, bg)
    if photo:
        blob = photo.pop("blob", None)
        if blob is not None:                     # never leave any of the reference person behind
            bx0, by0, bx1, by1 = blob["box"]
            bm = cv2.dilate(blob["mask"].astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool)
            if photo["circle"]:                  # …but keep a ring/border around a round photo
                cx, cy = (photo["box"][0] + photo["box"][2]) / 2, (photo["box"][1] + photo["box"][3]) / 2
                yy, xx = np.mgrid[by0:by1, bx0:bx1]
                bm &= np.hypot(xx - cx, yy - cy) <= photo["radius_px"] + 2
            erase[by0:by1, bx0:bx1] |= bm
        x0, y0, x1, y1 = photo["box"]
        shape = np.zeros((H, W), np.uint8)
        r = int(photo["radius_px"])
        cv2.rectangle(shape, (x0 + r, y0), (x1 - r, y1), 1, -1)
        cv2.rectangle(shape, (x0, y0 + r), (x1, y1 - r), 1, -1)
        for cx, cy in ((x0 + r, y0 + r), (x1 - r, y0 + r), (x0 + r, y1 - r), (x1 - r, y1 - r)):
            cv2.circle(shape, (cx, cy), r, 1, -1)
        erase |= shape.astype(bool)
        info["photo"] = {k: v for k, v in photo.items()}
        # text lines inside the photo are not text (OCR noise on the picture)

    # ── per section: decoration crops, leading glyphs, graphics, then erase the section area ──
    cols = s["columns"]
    areas = []
    for sec in s["sections"]:
        col = cols[sec["col"]]
        h = sec.get("heading")
        # erase area: between the gutters; outer columns reach the page edge (bars/icons often stick out past
        # the text). Only non-background components mostly inside it are erased, so bands/sidebars survive.
        ax0 = max(col["sep0"], col["x0"] - int(6 * MM)) if sec["col"] > 0 else int(2 * MM)
        ax1 = min(col["sep1"] - int(1 * MM), col["x1"] + int(6 * MM)) if sec["col"] + 1 < len(cols) else W - int(2 * MM)
        if sec["col"] + 1 < len(cols):          # reach into the gutter up to the next column's content
            nxt = cols[sec["col"] + 1]
            ax1 = max(ax1, min(nxt["x0"] - int(2 * MM), col["x1"] + int(14 * MM)))
        y0 = sec["y0"]
        sinfo = {"area": [ax0, y0, ax1, sec["y1"]]}
        if h is not None:
            deco = _heading_deco(img, h, lines, col, nonbg, text_mask, cc, stats, comps_in, ax0, ax1, W, H)
            if deco:
                name = f"head_{sec['key']}_{sec['col']}_{y0}.png"
                deco["file"] = _save(os.path.join(out_dir, "crops", name), deco.pop("rgba"))
                sinfo["deco"] = deco
                y0 = min(y0, deco["box"][1])
                for i in deco.pop("comp_ids"):
                    erase |= cc == i
        sinfo["y0"] = y0
        sec_lines = [l for l in sec["lines"]]
        sinfo["leads"] = _leading_glyphs(img, sec_lines, nonbg, text_mask, comps_in, cc, stats, out_dir, sec, erase)
        sinfo["graphics"] = _section_graphics(img, sec, sec_lines, nonbg, text_mask, cc, stats, comps_in,
                                              [ax0, y0, ax1, sec["y1"]], out_dir, erase)
        areas.append((ax0, y0, ax1, sec["y1"]))
        # erase every non-background component that lies inside the section area
        for i in comps_in(ax0, y0 - 2, ax1, sec["y1"], 0.8):
            if photo and _inside(stats[i], photo["box"]):
                continue
            erase |= cc == i
        info["sections"][f"{sec['key']}@{sec['col']}@{sec['y0']}"] = sinfo

    # ── inside section areas, anything that differs from the local background is content (halos, ghosts) ──
    # clean background model: every flat region gets a smooth colour surface (robust fit), so the grey haze that
    # dense low-res text leaves between its lines is neither kept nor copied back into erased areas
    local_bg = _bg_model(img, regions)
    diff = np.abs(img.astype(np.int16) - local_bg.astype(np.int16)).sum(-1) > 10
    structural = np.zeros((H, W), bool)
    for i in range(1, n):
        x, y, w, h, a = stats[i]
        thin_v = h > 60 * MM and w < 2.5 * MM
        thin_h = w > 90 * MM and h < 1.5 * MM
        crosses = sum(1 for (ax0_, ay0_, ax1_, ay1_) in areas if y < ay1_ and y + h > ay0_ and x < ax1_ and x + w > ax0_)
        if (thin_v or thin_h) and crosses >= 2:
            structural |= cc == i
    structural |= _long_lines(diff, areas)
    if structural.any():
        structural = cv2.dilate(structural.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool)
        erase &= ~structural
    for (x0_, y0_, x1_, y1_) in areas:
        x0_, y0_ = max(0, int(x0_)), max(0, int(y0_) - 2)
        x1_, y1_ = min(W, int(x1_)), min(H, int(y1_))
        m_ = diff[y0_:y1_, x0_:x1_].copy() & ~structural[y0_:y1_, x0_:x1_]
        if photo:
            px0, py0, px1, py1 = photo["box"]
            m_[max(0, py0 - y0_):max(0, py1 - y0_), max(0, px0 - x0_):max(0, px1 - x0_)] = False
        erase[y0_:y1_, x0_:x1_] |= m_
    # …and the anti-aliasing halo around every text line (header text included)
    for l in lines:
        if not l.get("ink"):
            continue
        x0_, y0_, x1_, y1_ = l["box"]
        x0_, y0_, x1_, y1_ = max(0, x0_ - 6), max(0, y0_ - 6), min(W, x1_ + 6), min(H, y1_ + 6)
        if photo and _inside([x0_, y0_, x1_ - x0_, y1_ - y0_], photo["box"]):
            continue
        erase[y0_:y1_, x0_:x1_] |= diff[y0_:y1_, x0_:x1_]
        if l.get("role") in ("name", "title", "header_contact", "header_other", "loose"):
            # outside sections the whole text area goes (glyph-level erasing leaves ghosts of thin/spaced text)
            pad = max(2, int(0.25 * (l["box"][3] - l["box"][1])))
            bx0, by0, bx1, by1 = max(0, l["box"][0] - pad), max(0, l["box"][1] - pad), min(W, l["box"][2] + pad), \
                min(H, l["box"][3] + pad)
            erase[by0:by1, bx0:bx1] |= ~structural[by0:by1, bx0:bx1]

    # ── header contact icons (left of contact lines outside sections) ──
    for l in lines:
        if l["role"] in ("header_contact",):
            g = _lead_of(l, nonbg, text_mask, comps_in, stats, W)
            if g:
                gx0, gy0, gx1, gy1, ids = g
                ctype = l.get("ctype") or contact_type(l["text"]) or "website"
                crop = img[gy0:gy1, gx0:gx1]
                alpha = np.zeros((gy1 - gy0, gx1 - gx0), bool)
                for i in ids:
                    alpha |= (cc[gy0:gy1, gx0:gx1] == i)
                    erase |= cc == i
                f = _save(os.path.join(out_dir, "crops", f"hicon_{ctype}_{l['id']}.png"), _rgba(crop, alpha))
                info["header_icons"].setdefault(ctype, {"file": f, "box": [gx0, gy0, gx1, gy1]})
                l["icon_box"] = [gx0, gy0, gx1, gy1]

    # ── more icons in the same icon column as the header-contact icons (their lines may be unreadable) ──
    boxes = [l["icon_box"] for l in lines if l.get("icon_box")]
    if boxes:
        ix = float(np.median([b[0] for b in boxes]))
        iw = float(np.median([b[2] - b[0] for b in boxes]))
        ih_ = float(np.median([b[3] - b[1] for b in boxes]))
        ys = sorted(b[1] for b in boxes)
        pitch = float(np.median(np.diff(ys))) if len(ys) > 1 else 3 * ih_
        lo, hi = ys[0] - 3.5 * pitch, ys[-1] + 3.5 * pitch
        for i in range(1, n):
            x, y, w, h, a = stats[i]
            if abs(x - ix) < 2 * MM and lo <= y <= hi and 0.55 * iw <= w <= 1.6 * iw and 0.55 * ih_ <= h <= 1.6 * ih_:
                erase |= cc == i

    # ── fill: erased pixels take the clean local background (from the interior of background regions, so
    #    faint halo pixels next to the text can't smear back in), with a soft seam ──
    protect = [photo["box"]] if photo else []
    orn, orn_boxes = _ornaments(img, local_bg, lines, protect)     # ▶▶▶▶, ○○○○○, dot grids: the design's own
    info["ornaments"] = len(orn_boxes)
    info["ornament_boxes_mm"] = [[round(v / MM, 2) for v in b] for b in orn_boxes]

    erase |= _text_residue(img, local_bg, protect + orn_boxes)   # text OCR missed (tiny / low contrast)
    erase = cv2.dilate(erase.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool)
    erase &= ~orn
    soft = cv2.GaussianBlur(erase.astype(np.float32), (5, 5), 0)[..., None]
    plate = (local_bg.astype(np.float32) * soft + img.astype(np.float32) * (1 - soft)).round().astype(np.uint8)
    plate[erase] = local_bg[erase]
    plate, n_left = _ocr_verify(plate, local_bg, protect + orn_boxes)    # whatever text is still readable goes too
    info["erase_frac"] = round(float(erase.mean()), 3)
    info["ocr_leftovers_removed"] = n_left
    # room to the right of the name/title. A thin rule beside it ("Accountant ———") is "soft": a longer title
    # may cover it with the background colour. The photo or a block is "hard": the title must fit before it.
    # obstacles = design elements still in the plate that aren't background regions (region edges don't count)
    dplate = (~bg) & ~erase
    for l in s.get("name_lines", []) + s.get("title_lines", []):
        x0, y0, x1, y1 = l["ink"]
        start = x1 + int(1.5 * MM)
        hard_x = None
        if photo and photo["box"][1] < y1 + 2 * MM and photo["box"][3] > y0 - 2 * MM and photo["box"][0] > x1:
            hard_x = photo["box"][0] - int(1.5 * MM)
        band = dplate[max(0, y0 - int(2 * MM)):y1 + int(2 * MM), start:]
        cols_hit = np.nonzero(band.any(0))[0] if band.size else []
        if len(cols_hit):
            ox = start + int(cols_hit[0])
            run = band[:, cols_hit[0]:cols_hit[0] + int(3 * MM)]
            rows = np.nonzero(run.any(1))[0]
            thin = len(rows) and (rows.max() - rows.min() + 1) < 0.6 * (y1 - y0)
            if thin:
                l["room_px"] = int(ox - x0)
                l["room_kind"] = "rule"
                l["patch"] = _hex(np.median(plate[y0:y1, max(0, x0 - 6):x0 - 1].reshape(-1, 3), axis=0))                     if x0 > 7 else None
            else:
                hard_x = min(hard_x, ox) if hard_x else ox
        if hard_x:
            l["room_hard_px"] = int(hard_x - x0)

    # ── continuation plate (page 2+) and extension of a partial page ──
    full_h = int(round(297 * MM))
    tops = [c["top"] for c in cols] or [int(H * 0.3)]
    ya = int(min(H - 2, max(tops) + 10 * MM))
    yb = int(max(ya + 2, min(H - 2, H * 0.9)))
    profile = np.median(plate[ya:yb], axis=0).astype(np.uint8)          # (W, 3)
    plate2 = np.repeat(profile[None, :, :], full_h, axis=0)
    content_bottom = max([l["box"][3] for l in lines] or [0])
    if H - content_bottom > 8 * MM and H >= 0.93 * full_h:               # a footer strip below the content
        fh = int(min(H - content_bottom - 4 * MM, 40 * MM))
        plate2[full_h - fh:] = plate[H - fh:H]
    if H < full_h:
        ext = np.repeat(profile[None, :, :], full_h - H, axis=0)
        plate = np.vstack([plate, ext])
    elif H > full_h:
        plate = plate[:full_h]
    info["plate"] = _save_image(os.path.join(out_dir, "plate"), plate)
    info["plate2"] = _save_image(os.path.join(out_dir, "plate2"), plate2)
    return info


def _long_lines(diff: np.ndarray, areas: list) -> np.ndarray:
    """Thin straight lines that run ≥ 60 mm across ≥ 2 sections (a timeline joining all headings, a divider):
    found per column/row of the 'differs from background' mask, allowing gaps (faint lines break up)."""
    H, W = diff.shape
    out = np.zeros((H, W), bool)
    gap_max, min_len = int(2.5 * MM), int(60 * MM)

    def runs(v):
        idx = np.nonzero(v)[0]
        if len(idx) < min_len * 0.4:
            return []
        res, start, last = [], idx[0], idx[0]
        for i in idx[1:]:
            if i - last > gap_max:
                res.append((start, last))
                start = i
            last = i
        res.append((start, last))
        return [(a, b) for a, b in res if b - a >= min_len and v[a:b + 1].mean() > 0.4]

    def crosses(x0, y0, x1, y1):
        return sum(1 for (ax0, ay0, ax1, ay1) in areas if y0 < ay1 and y1 > ay0 and x0 < ax1 and x1 > ax0)
    for x in range(0, W, 1):
        for a, b in runs(diff[:, x]):
            # thin: the neighbours a few px away are not part of it
            l_ = diff[a:b + 1, max(0, x - int(2.5 * MM))].mean() if x >= int(2.5 * MM) else 0
            r_ = diff[a:b + 1, min(W - 1, x + int(2.5 * MM))].mean()
            if l_ < 0.3 and r_ < 0.3 and crosses(x, a, x + 1, b) >= 2:
                out[a:b + 1, x] |= diff[a:b + 1, x]
    for y in range(0, H, 1):
        for a, b in runs(diff[y, :]):
            u_ = diff[max(0, y - int(2 * MM)), a:b + 1].mean()
            d_ = diff[min(H - 1, y + int(2 * MM)), a:b + 1].mean()
            if u_ < 0.3 and d_ < 0.3 and crosses(a, y, b, y + 1) >= 2:
                out[y, a:b + 1] |= diff[y, a:b + 1]
    return out


def _ornaments(img: np.ndarray, local_bg: np.ndarray, lines: list, protect: list):
    """Decorative runs the plate must keep: ≥ 3 identical marks (same size and shape), evenly spaced in a row,
    with no text beside them (arrows ▶▶▶▶, circles ○○○○○, dot grids). Letters of a word differ in shape; rating
    dots / leader dots sit next to a text line, so those stay content. Returns (mask, boxes)."""
    import cv2
    H, W = img.shape[:2]
    d = (np.abs(img.astype(np.int16) - local_bg.astype(np.int16)).sum(-1) > 30).astype(np.uint8)
    n, cc, st, _ = cv2.connectedComponentsWithStats(d, connectivity=8)
    cand = [i for i in range(1, n) if st[i, 4] >= 3 and 0.35 * MM <= max(st[i, 2], st[i, 3]) <= 8 * MM
            and min(st[i, 2], st[i, 3]) >= 0.25 * MM]
    sig = {}
    for i in cand:
        x, y, w, h = st[i, :4]
        sig[i] = cv2.resize((cc[y:y + h, x:x + w] == i).astype(np.uint8) * 255, (12, 12), interpolation=cv2.INTER_AREA) > 127

    def alike(i, j):
        wi, hi, wj, hj = st[i, 2], st[i, 3], st[j, 2], st[j, 3]
        small = max(wi, hi, wj, hj) < 2.5 * MM          # low-res / JPEG: small marks vary more
        tol = 0.4 if small else 0.25
        if abs(wi - wj) > max(2, tol * max(wi, wj)) or abs(hi - hj) > max(2, tol * max(hi, hj)):
            return False
        if max(wi, hi) < 1.2 * MM:                 # tiny dots: size is the shape
            return True
        a, b = sig[i], sig[j]
        return (a & b).sum() / max(1, (a | b).sum()) >= (0.5 if small else 0.6)
    rows: list[list[int]] = []
    for i in sorted(cand, key=lambda i: (st[i, 1] + st[i, 3] / 2, st[i, 0])):
        cy = st[i, 1] + st[i, 3] / 2
        for r in rows:
            j = r[-1]
            if abs(st[j, 1] + st[j, 3] / 2 - cy) < max(2, 0.3 * st[j, 3]) and alike(i, j):
                r.append(i)
                break
        else:
            rows.append([i])
    text_boxes = [l["box"] for l in lines]
    mask = np.zeros((H, W), bool)
    boxes = []
    for r in rows:
        r.sort(key=lambda i: st[i, 0])
        runs, cur = [], [r[0]]
        for i in r[1:]:
            j = cur[-1]
            gap = st[i, 0] - (st[j, 0] + st[j, 2])
            if -max(2, 0.15 * st[j, 2]) <= gap <= 3 * max(st[j, 2], st[j, 3]) + 1.5 * MM:      # touching marks too
                cur.append(i)
            else:
                runs.append(cur)
                cur = [i]
        runs.append(cur)
        for run in runs:
            if len(run) < 3:
                continue
            gaps = [st[b, 0] - st[a, 0] for a, b in zip(run, run[1:])]
            if max(gaps) - min(gaps) > max(3, 0.3 * float(np.median(gaps))):
                continue                           # not evenly spaced
            x0 = min(st[i, 0] for i in run)
            y0 = min(st[i, 1] for i in run)
            x1 = max(st[i, 0] + st[i, 2] for i in run)
            y1 = max(st[i, 1] + st[i, 3] for i in run)
            if any(b[1] < y1 and b[3] > y0 and b[0] < x1 + 12 * MM and b[2] > x0 - 12 * MM for b in text_boxes):
                continue                           # beside text: rating dots, leaders, bullets → content
            if any(not (x1 < b[0] or x0 > b[2] or y1 < b[1] or y0 > b[3]) for b in protect):
                continue
            for i in run:
                mask |= cc == i
            boxes.append([int(x0), int(y0), int(x1), int(y1)])
    if mask.any():
        mask = cv2.dilate(mask.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool)
    return mask, boxes


def _text_residue(img: np.ndarray, local_bg: np.ndarray, protect: list) -> np.ndarray:
    """Anything that still looks like text (OCR can miss tiny/low-contrast lines on low-res references):
    rows of ≥ 3 small marks that close into a line-shaped blob with a text-like fill. Rules, pictures and
    bands don't qualify. Returns a mask to erase."""
    import cv2
    H, W = img.shape[:2]
    d = (np.abs(img.astype(np.int16) - local_bg.astype(np.int16)).sum(-1) > 30).astype(np.uint8)
    n, cc, st, _ = cv2.connectedComponentsWithStats(d, connectivity=8)
    ok = np.zeros(n, bool)
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if a > 0.01 * H * W or h > 7 * MM:
            continue                                            # pictures, bands, big shapes
        if (h <= 0.7 * MM and w > 6 * MM) or (w <= 0.7 * MM and h > 6 * MM):
            continue                                            # rules / dividers
        ok[i] = True
    small = ok[cc]
    kx, ky = int(1.6 * MM) | 1, max(1, int(0.3 * MM)) | 1
    blobs = cv2.morphologyEx(small.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((ky, kx), np.uint8))
    n2, cc2, st2, _ = cv2.connectedComponentsWithStats(blobs, connectivity=8)
    out = np.zeros((H, W), bool)
    for j in range(1, n2):
        x, y, w, h, a = st2[j]
        if not (0.9 * MM <= h <= 7 * MM and w >= 2.5 * h):
            continue
        sub = small[y:y + h, x:x + w]
        if not (0.06 <= sub.mean() <= 0.7):
            continue
        if len(np.unique(cc[y:y + h, x:x + w][sub])) < 3:
            continue
        if any(not (x + w < b[0] or x > b[2] or y + h < b[1] or y > b[3]) for b in protect):
            continue
        out[max(0, y - 2):y + h + 2, max(0, x - 2):x + w + 2] = True
    # spaced capitals ("B U S I N E S S"): ≥ 4 letter-sized marks of equal height in a row, gaps < 3.5 × height
    letters = [i for i in range(1, n) if ok[i] and 1.2 * MM <= st[i, 3] <= 7 * MM and 0.15 < st[i, 2] / st[i, 3] < 1.6]
    letters.sort(key=lambda i: (st[i, 1] + st[i, 3] // 2, st[i, 0]))
    rows: list[list[int]] = []
    for i in letters:
        cy = st[i, 1] + st[i, 3] / 2
        for r in rows:
            j = r[-1]
            if abs(st[j, 1] + st[j, 3] / 2 - cy) < 0.35 * st[j, 3] and abs(st[i, 3] - st[j, 3]) < 0.35 * st[j, 3]:
                r.append(i)
                break
        else:
            rows.append([i])
    for r in rows:
        r.sort(key=lambda i: st[i, 0])
        run = [r[0]]
        for i in r[1:] + [None]:
            j = run[-1]
            if i is not None and 0 <= st[i, 0] - (st[j, 0] + st[j, 2]) < 3.5 * st[j, 3]:
                run.append(i)
                continue
            if len(run) >= 4:
                x0_ = min(st[k, 0] for k in run)
                y0_ = min(st[k, 1] for k in run)
                x1_ = max(st[k, 0] + st[k, 2] for k in run)
                y1_ = max(st[k, 1] + st[k, 3] for k in run)
                if not any(not (x1_ < b[0] or x0_ > b[2] or y1_ < b[1] or y0_ > b[3]) for b in protect):
                    out[max(0, y0_ - 3):y1_ + 3, max(0, x0_ - 3):x1_ + 3] = True
            run = [i] if i is not None else []
    return out


def _ocr_verify(plate: np.ndarray, local_bg: np.ndarray, protect: list) -> tuple[np.ndarray, int]:
    """Last check: OCR the finished background; any text it still finds is replaced by background."""
    import cv2
    from .measure import ocr_lines
    try:
        found = ocr_lines(plate)
    except Exception:
        return plate, 0
    n = 0
    H, W = plate.shape[:2]
    for l in found:
        if l["conf"] < 0.5 or len(re.sub(r"[^A-Za-z0-9]", "", l["text"])) < 1:
            continue
        x0, y0, x1, y1 = l["box"]
        if not (0.8 * MM <= y1 - y0 <= 12 * MM):
            continue
        if any(not (x1 < b[0] or x0 > b[2] or y1 < b[1] or y0 > b[3]) for b in protect):
            continue
        x0, y0, x1, y1 = max(0, x0 - 3), max(0, y0 - 3), min(W, x1 + 3), min(H, y1 + 3)
        plate[y0:y1, x0:x1] = local_bg[y0:y1, x0:x1]
        n += 1
    return plate, n


def _bg_model(img: np.ndarray, regions: np.ndarray) -> np.ndarray:
    """Per background region (page, sidebar, band, diagonal half… — one colour cluster each): a 2nd-order colour
    surface fitted to its interior pixels with outlier trimming. Every pixel is evaluated with the model of its
    own (or nearest) region, so region edges stay sharp and text haze/ghosts disappear."""
    import cv2
    H, W = img.shape[:2]
    h, w = regions.shape[:2]
    sm = cv2.resize(img, (w, h), interpolation=cv2.INTER_AREA).astype(np.float32)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    xn, yn = xx / w, yy / h
    rng = np.random.default_rng(0)
    models = {}
    labk = np.zeros((h, w), np.int32)
    for i in range(1, int(regions.max()) + 1):
        m = regions == i
        corem = cv2.erode(m.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool)
        idx = np.flatnonzero(corem)
        if len(idx) < 200:
            continue
        labk[m] = i
        if len(idx) > 30000:
            idx = rng.choice(idx, 30000, replace=False)
        X = np.stack([np.ones(len(idx)), xn.flat[idx], yn.flat[idx], xn.flat[idx] ** 2,
                      xn.flat[idx] * yn.flat[idx], yn.flat[idx] ** 2], 1)
        Y = sm.reshape(-1, 3)[idx]
        sel = np.ones(len(idx), bool)
        coef = None
        for _ in range(3):
            coef, *_ = np.linalg.lstsq(X[sel], Y[sel], rcond=None)
            res = np.abs(X @ coef - Y).sum(1)
            new = res < max(6.0, np.percentile(res, 70) * 1.5)
            if new.sum() < 50 or (new == sel).all():
                break
            sel = new
        models[i] = coef
    if not models:
        return img.copy()
    # every pixel → its own region, or the nearest one
    _, near = cv2.distanceTransformWithLabels((labk == 0).astype(np.uint8), cv2.DIST_L2, 5,
                                              labelType=cv2.DIST_LABEL_PIXEL)
    zy, zx = np.nonzero(labk)
    lut = np.zeros(near.max() + 1, np.int32)
    lut[near[zy, zx]] = labk[zy, zx]
    full_lab = np.where(labk > 0, labk, lut[near])
    # local correction: the smooth surface can be a few levels off locally (visible as faint bands where text
    # was). Add back the residual of nearby *clean* pixels (core, away from text) with a masked blur.
    model_h = np.zeros_like(sm)
    for i, coef in models.items():
        m = full_lab == i
        F = np.stack([np.ones(m.sum(), np.float32), xn[m], yn[m], xn[m] ** 2, xn[m] * yn[m], yn[m] ** 2], 1)
        model_h[m] = F @ coef
    wmask = np.zeros((h, w), np.float32)
    for i in models:
        wmask[cv2.erode((regions == i).astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool)] = 1.0
    # only clean pixels inform the correction: text halos (a few levels off the surface) would darken it
    raw = np.abs(sm - model_h).sum(-1)
    wmask[raw > 12] = 0.0
    wmask = cv2.erode(wmask, np.ones((3, 3), np.uint8))
    resid = (sm - model_h) * wmask[..., None]
    num = cv2.GaussianBlur(resid, (0, 0), 6)
    den = cv2.GaussianBlur(wmask, (0, 0), 6)[..., None]
    corr = np.where(den > 0.05, num / np.maximum(den, 1e-3), 0)
    corr_full = cv2.resize(corr, (W, H), interpolation=cv2.INTER_LINEAR)
    big_lab = cv2.resize(full_lab.astype(np.float32), (W, H), interpolation=cv2.INTER_NEAREST).astype(np.int32)
    res = np.zeros((H, W, 3), np.uint8)
    Yf, Xf = np.mgrid[0:H, 0:W].astype(np.float32)
    fx, fy = Xf / W, Yf / H
    for i, coef in models.items():
        m = big_lab == i
        F = np.stack([np.ones(m.sum(), np.float32), fx[m], fy[m], fx[m] ** 2, fx[m] * fy[m], fy[m] ** 2], 1)
        res[m] = np.clip(F @ coef + corr_full[m], 0, 255).astype(np.uint8)
    return res


def _save_image(stem: str, arr: np.ndarray) -> str:
    import cv2
    ok, buf = cv2.imencode(".png", arr, [cv2.IMWRITE_PNG_COMPRESSION, 6])
    if ok and len(buf) < 1_400_000:
        path = stem + ".png"
    else:
        ok, buf = cv2.imencode(".jpg", arr, [cv2.IMWRITE_JPEG_QUALITY, 94])
        path = stem + ".jpg"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    buf.tofile(path)
    return path


def _inside(st, box) -> bool:
    x, y, w, h = st[:4]
    return x >= box[0] - 2 and y >= box[1] - 2 and x + w <= box[2] + 2 and y + h <= box[3] + 2


def _nearest_fill(img: np.ndarray, erase: np.ndarray, soften: bool = True) -> np.ndarray:
    import cv2
    # non-zero = pixels to fill; every zero (kept) pixel gets its own label, filled pixels the nearest one's
    dist, labels = cv2.distanceTransformWithLabels(erase.astype(np.uint8), cv2.DIST_L2, 5,
                                                   labelType=cv2.DIST_LABEL_PIXEL)
    zy, zx = np.nonzero(~erase)
    lut = np.zeros((labels.max() + 1, 3), np.uint8)
    lut[labels[zy, zx]] = img[zy, zx]
    out = img.copy()
    ey, ex = np.nonzero(erase)
    out[ey, ex] = lut[labels[ey, ex]]
    if not soften:
        return out
    # soften the Voronoi seams inside the filled areas only
    blur = cv2.GaussianBlur(out, (7, 7), 0)
    soft = cv2.GaussianBlur(erase.astype(np.float32), (5, 5), 0)[..., None]
    inner = cv2.erode(erase.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool)[..., None]
    out = np.where(inner, (blur * soft + out * (1 - soft)).astype(np.uint8), out)
    return out


# ── photo ──────────────────────────────────────────────────────────────────────────────────────────

def _find_photo(img: np.ndarray, s: dict, bg: np.ndarray | None = None) -> dict | None:
    import cv2
    from app.services.resume_builder import _grow_photo_box
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cascade = cv2.CascadeClassifier(os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_default.xml"))
    H, W = gray.shape
    faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=6, minSize=(int(8 * MM), int(8 * MM)))
    faces = sorted([tuple(int(v) for v in f) for f in faces], key=lambda f: -f[2] * f[3])
    if not len(faces):
        f = _skin_face(img, bg)                 # cartoon / illustrated avatar: no real face to detect
        if f is None:
            return None
        faces = [f]
    face = faces[0]
    fx, fy, fw, fh = face
    # photo blob: non-background components touching the face (the picture's own pixels)
    blob = None
    if bg is not None:
        n, cc, st, _ = cv2.connectedComponentsWithStats((~bg).astype(np.uint8), connectivity=8)
        ids = [int(i) for i in np.unique(cc[fy:fy + fh, fx:fx + fw]) if i]
        ids = [i for i in ids if st[i, 2] < 5 * fw and st[i, 3] < 7 * fh]
        if ids:
            bx0 = min(st[i, 0] for i in ids)
            by0 = min(st[i, 1] for i in ids)
            bx1 = max(st[i, 0] + st[i, 2] for i in ids)
            by1 = max(st[i, 1] + st[i, 3] for i in ids)
            m = np.isin(cc[by0:by1, bx0:bx1], ids)
            blob = {"box": [int(bx0), int(by0), int(bx1), int(by1)], "mask": m}
    fit = _photo_edges(img, face)
    if fit and fit["circle"]:
        if blob is not None:
            (cx, cy), r = ((fit["box"][0] + fit["box"][2]) / 2, (fit["box"][1] + fit["box"][3]) / 2), fit["radius_px"]
            ys, xs = np.nonzero(blob["mask"])
            inside = (np.hypot(xs + blob["box"][0] - cx, ys + blob["box"][1] - cy) <= r * 1.2 + 3).mean()   # a ring may hug it
            if inside < 0.85:                    # the circle cuts through the picture: not its frame
                fit = None
        if fit:
            fit["blob"] = blob
            return fit
    b_ok = blob is not None and (blob["box"][2] - blob["box"][0]) > 1.2 * fw and (blob["box"][3] - blob["box"][1]) > 1.2 * fh
    if fit and blob is not None and fit["box"][0] <= blob["box"][0] + 4 and fit["box"][1] <= blob["box"][1] + 4 \
            and fit["box"][2] >= blob["box"][2] - 4 and fit["box"][3] >= blob["box"][3] - 4:
        x0, y0, x1, y1 = fit["box"]            # the frame (e.g. a light square) holds the whole picture
    elif b_ok:
        x0, y0, x1, y1 = blob["box"]
    elif fit:
        x0, y0, x1, y1 = fit["box"]
    else:
        x0, y0, x1, y1 = _grow_photo_box(gray, face)
        # a grown box much wider/taller than a portrait ran into something else: clamp around the face
        if (x1 - x0) > 3.6 * fw:
            x0, x1 = max(x0, fx - int(1.3 * fw)), min(x1, fx + fw + int(1.3 * fw))
        if (y1 - y0) > 4.5 * fh:
            y0, y1 = max(y0, fy - int(1.2 * fh)), min(y1, fy + fh + int(2.4 * fh))
    w, h = x1 - x0, y1 - y0
    if w < 10 * MM or h < 10 * MM:
        return None
    # frame shape: walk the diagonal from each corner until the picture starts → corner radius
    outside = np.median(np.concatenate([img[max(0, y0 - 3), x0:x1], img[min(H - 1, y1 + 2), x0:x1]]), axis=0)
    gaps = []
    for (cx, cy, dx, dy) in ((x0, y0, 1, 1), (x1 - 1, y0, -1, 1), (x0, y1 - 1, 1, -1), (x1 - 1, y1 - 1, -1, -1)):
        k = 0
        while k < min(w, h) // 2:
            p = img[cy + dy * k, cx + dx * k].astype(int)
            if np.abs(p - outside).sum() > 60:
                break
            k += 1
        gaps.append(k)
    g = float(np.median(gaps))
    radius = min(min(w, h) / 2, g / 0.293) if g > 1 else 0
    circle = radius >= 0.45 * min(w, h)
    return {"box": [int(x0), int(y0), int(x1), int(y1)], "radius_px": int(min(min(w, h) / 2, radius)),
            "circle": bool(circle), "box_mm": [round(v / MM, 2) for v in (x0, y0, x1, y1)],
            "radius_mm": round(min(min(w, h) / 2, radius) / MM, 2), "blob": blob}


def _skin_face(img: np.ndarray, bg: np.ndarray | None):
    """Largest compact skin-tone area in the top half that isn't part of a big background region → a stand-in
    face box (x, y, w, h) for avatars/illustrations the face detector can't see."""
    import cv2
    H, W = img.shape[:2]
    ycc = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    y_, cr, cb = ycc[..., 0], ycc[..., 1], ycc[..., 2]
    skin = (cr > 135) & (cr < 178) & (cb > 78) & (cb < 130) & (y_ > 70)
    if bg is not None:
        skin &= ~bg
    skin[int(0.55 * H):] = False
    skin = cv2.morphologyEx(skin.astype(np.uint8), cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    n, cc, st, _ = cv2.connectedComponentsWithStats(skin, connectivity=8)
    best = None
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if not (5 * MM <= w <= 60 * MM and 5 * MM <= h <= 70 * MM) or a < 0.35 * w * h or a < 20 * MM * MM:
            continue
        if best is None or a > best[4]:
            best = (x, y, w, h, a)
    if best is None:
        return None
    x, y, w, h, _ = best
    return int(x), int(y), int(w), int(min(h, 1.3 * w))


def _photo_edges(img: np.ndarray, face) -> dict | None:
    """Frame of the photo: every strong colour edge along 96 rays from the face is a candidate; the circle (or
    axis-aligned rectangle) that the most rays agree on is the frame. Hair/shoulder edges are irregular and
    lose; with a ring/border the innermost well-supported circle is the picture edge."""
    H, W = img.shape[:2]
    fx, fy, fw, fh = face
    cx0, cy0 = fx + fw / 2, fy + fh / 2
    sm = img.astype(np.float32)
    rays = []                                     # per ray: array of candidate points (x, y)
    thetas = np.linspace(0, 2 * np.pi, 96, endpoint=False)
    for th in thetas:
        rs = np.arange(int(0.5 * fw), int(3.6 * fw))
        xs = (cx0 + rs * np.cos(th)).astype(int)
        ys = (cy0 + rs * np.sin(th)).astype(int)
        ok = (xs >= 0) & (xs < W) & (ys >= 0) & (ys < H)
        xs, ys = xs[ok], ys[ok]
        if len(xs) < 8:
            rays.append(np.zeros((0, 2)))
            continue
        c = sm[ys, xs]
        # wide derivative: upscaled low-res references have edges spread over several pixels
        g = np.zeros(len(c))
        g[3:-3] = np.abs(c[6:] - c[:-6]).sum(1)
        peaks = [i for i in range(1, len(g) - 1) if g[i] >= 36 and g[i] >= g[i - 1] and g[i] >= g[i + 1]]
        peaks = sorted(peaks, key=lambda i: -g[i])[:8]
        rays.append(np.array([(xs[i], ys[i]) for i in peaks], float).reshape(-1, 2))
    allp = [(k, p) for k, r in enumerate(rays) for p in r]
    if len(allp) < 30:
        return None
    rng = np.random.default_rng(3)
    nr = len(rays)
    # the face itself (an ellipse inside the detector's padded square), not the square's corners: a photo circle
    # that clips the box corners still holds the whole face
    face_r = 0.5 * max(fw, fh)

    def support_circle(ctr, r):
        tol = max(3.0, 0.025 * r)
        return sum(1 for pts in rays if len(pts) and np.min(np.abs(np.linalg.norm(pts - ctr, axis=1) - r)) < tol)

    def sample_circles(P, K, n_iter):
        out = []
        if len(P) < 3:
            return out
        for _ in range(n_iter):
            i = rng.choice(len(P), 3, replace=False)
            if len(set(K[i])) < 3:
                continue
            a, b, c = P[i]
            A = np.array([[b[0] - a[0], b[1] - a[1]], [c[0] - a[0], c[1] - a[1]]]) * 2
            if abs(np.linalg.det(A)) < 1e-6:
                continue
            ctr = np.linalg.solve(A, np.array([b @ b - a @ a, c @ c - a @ a]))
            r = float(np.linalg.norm(a - ctr))
            # the frame must contain the whole face
            if r < face_r * 1.05 or r > 3.4 * fw or np.hypot(*(ctr - [cx0, cy0])) + face_r > r * 1.02:
                continue
            out.append((ctr, r))
        return out
    P = np.array([p for _, p in allp])
    K = np.array([k for k, _ in allp])
    scored = [(support_circle(c, r), c, r) for c, r in sample_circles(P, K, 900)]
    if scored:                                    # second, focused search inside the best circle (a photo
        best = max(scored, key=lambda t: t[0])    # inside a larger round shape has fewer, inner edge points)
        inner = np.linalg.norm(P - best[1], axis=1) < best[2] - 2 * MM
        scored += [(support_circle(c, r), c, r) for c, r in sample_circles(P[inner], K[inner], 600)]
    circle = None
    if scored:
        top = max(s for s, _, _ in scored)
        if top >= 0.5 * nr:
            good = [t for t in scored if t[0] >= 0.85 * top]
            circle = min(good, key=lambda t: t[2])         # innermost well-supported circle
            # a photo inside a larger round shape (a band ending in a circle, a ring): the picture's own edge is
            # often less supported (a light shirt melts into the frame), so an inner circle with fair support whose
            # outside is flat (frame / ring / background, not more picture) is the photo edge
            fair = sorted((t for t in scored if t[0] >= max(0.6 * top, 0.4 * nr) and t[2] < circle[2] - 2 * MM),
                          key=lambda t: t[2])
            for t in fair:
                if _flat_outside(img, t[1], t[2]):
                    circle = t
                    break
    # rectangle: per side, the x (or y) most rays near that direction agree on
    def side(sel, axis, limit, outward):
        """Innermost edge position (beyond `limit` in the `outward` direction) that most rays agree on."""
        pts = [r for k, r in enumerate(rays) if sel(thetas[k]) and len(r)]
        if len(pts) < 4:
            return None, 0
        vals = np.concatenate([p[:, axis] for p in pts])
        vals = vals[(vals - limit) * outward > 0]
        sup = {}
        for v in np.unique(vals.astype(int)):
            sup[v] = sum(1 for p in pts if np.min(np.abs(p[:, axis] - v)) < 3)
        if not sup:
            return None, 0
        top = max(sup.values())
        good = [v for v, c in sup.items() if c >= 0.8 * top]
        best = min(good, key=lambda v: (v - limit) * outward)
        return best, sup[best] / len(pts)
    ang = lambda t: (t + np.pi) % (2 * np.pi) - np.pi
    m = 0.25 * fw
    L, sl = side(lambda t: abs(abs(ang(t)) - np.pi) < 0.6, 0, fx - m, -1)
    R, sr = side(lambda t: abs(ang(t)) < 0.6, 0, fx + fw + m, 1)
    T, st = side(lambda t: abs(ang(t) + np.pi / 2) < 0.6, 1, fy - m, -1)
    B, sb = side(lambda t: abs(ang(t) - np.pi / 2) < 0.6, 1, fy + fh + m, 1)
    rect_support = min(sl, sr, st, sb) if None not in (L, R, T, B) else 0
    circ_support = circle[0] / nr if circle else 0
    if circle and circ_support >= rect_support:
        _, (cx, cy), r = circle
        x0, y0, x1, y1 = int(cx - r), int(cy - r), int(cx + r), int(cy + r)
        return {"box": [x0, y0, x1, y1], "radius_px": int(r), "circle": True,
                "box_mm": [round(v / MM, 2) for v in (x0, y0, x1, y1)], "radius_mm": round(r / MM, 2)}
    if rect_support >= 0.6 and R - L > fw and B - T > fh and L < fx and R > fx + fw and T < fy and B > fy + fh:
        x0, y0, x1, y1 = int(L), int(T), int(R), int(B)
        return {"box": [x0, y0, x1, y1], "radius_px": 0, "circle": False,
                "box_mm": [round(v / MM, 2) for v in (x0, y0, x1, y1)], "radius_mm": 0}
    return None


def _flat_outside(img, ctr, r) -> bool:
    """Just outside the circle the colour is flat (a ring, frame or background), not more picture."""
    H, W = img.shape[:2]
    steps = []
    for a in np.linspace(0, 2 * np.pi, 72, endpoint=False):
        pts = [(int(ctr[0] + (r + k * MM) * np.cos(a)), int(ctr[1] + (r + k * MM) * np.sin(a))) for k in (0.7, 1.2, 1.7)]
        if all(0 <= x < W and 0 <= y < H for x, y in pts):
            c = [img[y, x].astype(int) for x, y in pts]
            steps.append(max(np.abs(c[1] - c[0]).sum(), np.abs(c[2] - c[1]).sum()))
    return len(steps) >= 36 and float(np.percentile(steps, 75)) < 30


def _stands_out(img, cc, stats, i, thr: int = 30) -> bool:
    """The component's colour differs visibly from what surrounds it. On photographed / JPEG references a
    background's shading can leave large 'non-background' blobs of nearly the same colour: those aren't boxes,
    chips or dots."""
    H, W = img.shape[:2]
    x, y, w, h, _ = stats[i]
    m = cc[y:y + h, x:x + w] == i
    if not m.any():
        return False
    col = np.median(img[y:y + h, x:x + w][m], axis=0).astype(int)
    p = max(3, int(1.5 * MM))
    X0, Y0, X1, Y1 = max(0, x - p), max(0, y - p), min(W, x + w + p), min(H, y + h + p)
    ring = np.ones((Y1 - Y0, X1 - X0), bool)
    ring[y - Y0:y - Y0 + h, x - X0:x - X0 + w] = False
    if not ring.any():
        return True
    sur = np.median(img[Y0:Y1, X0:X1][ring], axis=0).astype(int)
    return int(np.abs(col - sur).sum()) > thr


def _ring_contrast(img, cx, cy, r) -> float:
    """Colour difference just inside vs just outside a circle (high = a real frame edge)."""
    H, W = img.shape[:2]
    ang = np.linspace(0, 2 * np.pi, 72, endpoint=False)
    diffs = []
    for a in ang:
        xi, yi = int(cx + (r - 4) * np.cos(a)), int(cy + (r - 4) * np.sin(a))
        xo, yo = int(cx + (r + 4) * np.cos(a)), int(cy + (r + 4) * np.sin(a))
        if 0 <= xi < W and 0 <= yi < H and 0 <= xo < W and 0 <= yo < H:
            diffs.append(np.abs(img[yi, xi].astype(int) - img[yo, xo].astype(int)).sum())
    return float(np.median(diffs)) if diffs else 0.0


# ── heading decoration ─────────────────────────────────────────────────────────────────────────────

def _heading_deco(img, h, lines, col, nonbg, text_mask, cc, stats, comps_in, ax0, ax1, W, H):
    import cv2
    ix0, iy0, ix1, iy1 = h["ink"]
    ih = iy1 - iy0
    others = [l for l in lines if l is not h and l.get("role") != "heading_part" and l.get("ink")
              and l["box"][2] > ax0 and l["box"][0] < ax1]
    above = [l["ink"][3] for l in others if l["ink"][3] <= iy0]
    below = [l["ink"][1] for l in others if l["ink"][1] >= iy1]
    by0 = max(int(iy0 - 1.6 * ih), (max(above) + 2) if above else 0)
    by1 = min(int(iy1 + 1.6 * ih), (min(below) - 2) if below else H)
    ids = comps_in(ax0 - int(4 * MM), by0, ax1 + int(4 * MM), by1, 0.85)
    # keep components that touch the heading row band or sit just under/over it (underline, rule, icon, box)
    keep = []
    for i in ids:
        x, y, w, hh, a = stats[i]
        if hh > 6 * ih and w < 2 * ih:          # a tall thin line (timeline / divider) is not heading decoration
            continue
        if a < 4:
            continue
        if a > 40 and not _stands_out(img, cc, stats, i):
            continue                             # background shading, not a box
        keep.append(i)
    if keep:
        xs0 = min(stats[i, 0] for i in keep)
        ys0 = min(stats[i, 1] for i in keep)
        xs1 = max(stats[i, 0] + stats[i, 2] for i in keep)
        ys1 = max(stats[i, 1] + stats[i, 3] for i in keep)
        bx0, by0_, bx1, by1_ = min(xs0, ix0), min(ys0, iy0), max(xs1, ix1), max(ys1, iy1)
    else:
        bx0, by0_, bx1, by1_ = ix0, iy0, ix1, iy1
    pad = 2
    bx0, by0_ = max(0, bx0 - pad), max(0, by0_ - pad)
    bx1, by1_ = min(W, bx1 + pad), min(H, by1_ + pad)
    crop = img[by0_:by1_, bx0:bx1].copy()
    alpha = np.zeros(crop.shape[:2], bool)
    for i in keep:
        alpha |= cc[by0_:by1_, bx0:bx1] == i
    tmask = np.zeros(crop.shape[:2], bool)
    gx0, gy0 = ix0 - bx0, iy0 - by0_
    tmask[gy0:gy0 + h["mask"].shape[0], gx0:gx0 + h["mask"].shape[1]] = h["mask"]
    tmask = cv2.dilate(tmask.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool)
    # the reference's heading text is removed from the decoration. Text on a filled box → those pixels get the
    # box colour; text on the page → transparent. (Inpainting left smudges that looked like scribbles.)
    tx1_, ty1_ = gx0 + (ix1 - ix0), gy0 + (iy1 - iy0)
    rx0, ry0 = max(0, gx0 - 3), max(0, gy0 - 3)
    rx1, ry1 = min(crop.shape[1], tx1_ + 3), min(crop.shape[0], ty1_ + 3)
    ring = np.zeros(crop.shape[:2], bool)
    ring[ry0:ry1, rx0:rx1] = True
    ring[gy0:ty1_, gx0:tx1_] = False
    on_box_ring = bool(ring.any() and (alpha & ring).sum() / max(1, ring.sum()) > 0.7)
    if on_box_ring:
        fill_px = crop[alpha & ~tmask & ring]
        fill = np.median(fill_px, axis=0) if len(fill_px) else np.median(crop[alpha & ~tmask], axis=0)
        box_area = np.zeros(crop.shape[:2], bool)
        box_area[ry0:ry1, rx0:rx1] = True
        crop[tmask & box_area] = fill.astype(np.uint8)
        alpha = (alpha & ~tmask) | (tmask & box_area)
        na_, ca_, sa_, _ = cv2.connectedComponentsWithStats(alpha.astype(np.uint8), connectivity=8)
        if na_ > 1:
            j = 1 + int(np.argmax(sa_[1:, 4]))                   # the box itself
            x_, y_, w_, h_ = sa_[j, :4]
            inner = crop[y_ + 1:y_ + h_ - 1, x_ + 1:x_ + w_ - 1]
            off = np.abs(inner.astype(np.int16) - fill.astype(np.int16)).sum(-1) > 12
            inner[off] = fill.astype(np.uint8)
            alpha[y_ + 1:y_ + h_ - 1, x_ + 1:x_ + w_ - 1] |= True
    else:
        alpha = alpha & ~cv2.dilate(tmask.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool)
        # leftover letters the OCR mask missed (low-res text is wider than its OCR ink): on the text's rows,
        # keep only rules, big shapes and icons left of the text — everything else is old text
        na, ca, sa, _ = cv2.connectedComponentsWithStats(alpha.astype(np.uint8), connectivity=8)
        band0, band1 = max(0, gy0 - 2), ty1_ + 2
        for j in range(1, na):
            x_, y_, w_, h_, a_ = sa[j]
            if y_ + h_ < band0 or y_ > band1:
                continue                                    # not on the text's rows
            rule = w_ > 5 * max(1, h_) and h_ < 0.6 * ih and a_ > 0.5 * w_ * h_     # long, solid (blurred at low dpi)
            big = a_ > 0.25 * alpha.size or h_ > 2.2 * ih
            left_icon = x_ + w_ <= gx0 + 1
            if not (rule or big or left_icon):
                alpha[ca == j] = False
    # a rule trailing the text ("Contact Me ———"): measured separately, so it follows the new heading text
    rule = None
    if not on_box_ring and alpha.any():
        na, ca, sa, _ = cv2.connectedComponentsWithStats(alpha.astype(np.uint8), connectivity=8)
        cands = []
        for j in range(1, na):
            x_, y_, w_, h_, a_ = sa[j]
            if x_ >= tx1_ - 2 and w_ > 5 * max(1, h_) and h_ < 0.6 * ih and a_ > 0.5 * w_ * h_ \
                    and y_ + h_ >= gy0 - 0.3 * ih and y_ <= ty1_ + 0.3 * ih:
                cands.append(j)
        if cands:
            j = max(cands, key=lambda j: sa[j, 2])
            x_, y_, w_, h_, a_ = sa[j]
            m = ca == j
            colsum = m.sum(0)                                   # pixels per column = the rule's thickness
            thick = float(np.median(colsum[colsum > 0])) if (colsum > 0).any() else h_
            px_ = crop[m].astype(np.int16)
            lum_ = px_.sum(1)
            core_ = px_[lum_ <= np.percentile(lum_, 50)] if np.median(lum_) < 382 else px_[lum_ >= np.percentile(lum_, 50)]
            color = _hex(np.median(core_, axis=0))                 # the rule's core, not its blurred edge
            end_abs = bx0 + x_ + w_
            rule = {"color": color, "h": float(max(1.0, thick * 0.8)), "gap": float(x_ - tx1_), "len": float(w_),
                    "to_edge": bool(end_abs >= col["x1"] - 3 * MM), "dy": float(y_ + h_ / 2 - gy0)}
            alpha[m] = False
    # specks (leftover dots of the old text) are not decoration
    if alpha.any():
        na, ca, sa, _ = cv2.connectedComponentsWithStats(alpha.astype(np.uint8), connectivity=8)
        for j in range(1, na):
            if sa[j, 4] < 0.12 * ih * ih and not (sa[j, 0] + sa[j, 2] <= gx0 + 1):
                alpha[ca == j] = False
    has_deco = bool(alpha.sum() > 0.15 * ih * ih)
    if not has_deco:
        return {"kind": "none", "box": [ix0, iy0, ix1, iy1], "comp_ids": keep, "rgba": _rgba(crop, alpha),
                "text": [gx0, gy0, gx0 + (ix1 - ix0), gy0 + (iy1 - iy0)], "box_mm": None, "rule": rule}
    # shrink the decoration to what is left (a removed trailing rule must not keep the box wide)
    ys_, xs_ = np.nonzero(alpha)
    cx0, cx1 = min(xs_.min(), gx0), max(xs_.max() + 1, tx1_)
    cy0, cy1 = min(ys_.min(), gy0), max(ys_.max() + 1, ty1_)
    crop, alpha = crop[cy0:cy1, cx0:cx1], alpha[cy0:cy1, cx0:cx1]
    bx0, by0_, bx1, by1_ = bx0 + cx0, by0_ + cy0, bx0 + cx1, by0_ + cy1
    gx0, gy0, tx1_, ty1_ = gx0 - cx0, gy0 - cy0, tx1_ - cx0, ty1_ - cy0    # (rule.dy is relative to the ink top)
    col_w = max(1, col["x1"] - col["x0"])
    # "full" = the decoration spans under/over the text across the column; otherwise it hugs the text
    spans_text = bool(alpha[:, gx0:tx1_].any()) if tx1_ > gx0 else False
    full = (bx1 - bx0) > (ix1 - ix0) + 3 * ih and bx1 >= col["x0"] + 0.8 * col_w and spans_text
    on_box = on_box_ring
    return {"kind": "full" if full else "hug", "on_box": on_box, "box": [int(bx0), int(by0_), int(bx1), int(by1_)],
            "comp_ids": keep, "rgba": _rgba(crop, alpha), "rule": rule,
            "text": [int(gx0), int(gy0), int(gx0 + ix1 - ix0), int(gy0 + iy1 - iy0)]}


# ── leading glyphs (bullets / icons) ───────────────────────────────────────────────────────────────

def _lead_of(l, nonbg, text_mask, comps_in, stats, W, others=None):
    """Small graphic just left of a text line (bullet, icon). Returns (x0, y0, x1, y1, ids) or None.
    Marks inside another text line's box (e.g. the anti-aliased edge of a date column's digits) aren't glyphs."""
    if not l.get("ink"):
        return None
    ix0, iy0, ix1, iy1 = l["ink"]
    ih = max(4, iy1 - iy0)
    ids = comps_in(ix0 - 4.6 * ih, iy0 - 0.9 * ih, ix0 - 1, iy1 + 0.9 * ih, 0.85)
    ids = [i for i in ids if stats[i, 3] < 2.2 * ih and stats[i, 2] < 2.6 * ih]
    if others:
        def in_other(i):
            cx, cy = stats[i, 0] + stats[i, 2] / 2, stats[i, 1] + stats[i, 3] / 2
            return any(b[0] - 2 <= cx <= b[2] + 2 and b[1] - 2 <= cy <= b[3] + 2 for b in others)
        ids = [i for i in ids if not in_other(i)]
    if not ids:
        return None
    # nearest cluster to the text
    ids.sort(key=lambda i: -(stats[i, 0] + stats[i, 2]))
    right = stats[ids[0], 0] + stats[ids[0], 2]
    group = [i for i in ids if right - (stats[i, 0] + stats[i, 2]) < 2.4 * ih]
    x0 = min(stats[i, 0] for i in group)
    y0 = min(stats[i, 1] for i in group)
    x1 = max(stats[i, 0] + stats[i, 2] for i in group)
    y1 = max(stats[i, 1] + stats[i, 3] for i in group)
    if ix0 - x1 > 2.4 * ih:
        return None
    return int(x0), int(y0), int(x1), int(y1), group


def _leading_glyphs(img, sec_lines, nonbg, text_mask, comps_in, cc, stats, out_dir, sec, erase):
    """Per line: the bullet/icon left of it (outside the OCR box) or a bullet glyph at the start of its own ink."""
    W = img.shape[1]
    found = []
    for l in sec_lines:
        g = _lead_of(l, nonbg, text_mask, comps_in, stats, W, [o["box"] for o in sec_lines if o is not l])
        if g:
            x0, y0, x1, y1, ids = g
            alpha = np.zeros((y1 - y0, x1 - x0), bool)
            for i in ids:
                alpha |= cc[y0:y1, x0:x1] == i
            found.append({"line": l["id"], "box": [x0, y0, x1, y1], "alpha": alpha, "role": l["role"],
                          "ctype": l.get("ctype") or contact_type(l["text"])})
            l["lead_box"] = [x0, y0, x1, y1]
        elif l.get("inner_bullet"):
            found.append({"line": l["id"], "box": l["inner_bullet"], "alpha": None, "role": l["role"], "inner": True,
                          "ctype": ""})
            l["lead_box"] = l["inner_bullet"]
    out = []
    for i, f in enumerate(found):
        x0, y0, x1, y1 = f["box"]
        crop = img[y0:y1, x0:x1]
        alpha = f["alpha"]
        if alpha is None:
            # bullet inside the OCR box: alpha from contrast against the line's background
            line = next(l for l in sec_lines if l["id"] == f["line"])
            d = np.abs(crop.astype(np.int16) - _bgr(line["bg"])).sum(-1)
            alpha = d > 60
            erase[y0:y1, x0:x1] |= alpha
        name = f"lead_{sec['key']}_{sec['col']}_{f['line']}.png"
        file = _save(os.path.join(out_dir, "crops", name), _rgba(crop, alpha))
        out.append({"line": f["line"], "box": f["box"], "file": file, "role": f["role"], "ctype": f["ctype"],
                    "w_mm": round((x1 - x0) / MM, 2), "h_mm": round((y1 - y0) / MM, 2)})
    return out


# ── skill graphics, chips, timeline ────────────────────────────────────────────────────────────────

def _section_graphics(img, sec, sec_lines, nonbg, text_mask, cc, stats, comps_in, area, out_dir, erase) -> dict:
    import cv2
    ax0, ay0, ax1, ay1 = area
    W = img.shape[1]
    ids = comps_in(ax0, ay0, ax1, ay1, 0.8)
    lead_boxes = [l.get("lead_box") for l in sec_lines if l.get("lead_box")]
    text_boxes = [l["box"] for l in sec_lines]
    med_h = float(np.median([l["ink"][3] - l["ink"][1] for l in sec_lines])) if sec_lines else 3 * MM

    def overlaps(st, box, pad=0):
        x, y, w, h = st[:4]
        return not (x + w < box[0] - pad or x > box[2] + pad or y + h < box[1] - pad or y > box[3] + pad)

    free = [i for i in ids if not any(overlaps(stats[i], b) for b in lead_boxes)]
    res: dict = {}
    # timeline: tall thin vertical line
    tall = [i for i in free if stats[i, 3] > 12 * MM and stats[i, 3] > 6 * stats[i, 2]]
    if tall and sec["key"] in ("experience", "projects", "education"):
        i = max(tall, key=lambda i: stats[i, 3])
        x, y, w, h, a = stats[i]
        # line width = the most common horizontal run of the line's pixels
        m = cc[y:y + h, x:x + w] == i
        runs = m.sum(1)
        lw = float(np.median(runs[runs > 0])) if (runs > 0).any() else 1
        core = img[y:y + h, x:x + w][m]
        color = _hex(np.median(core, axis=0)) if len(core) else "#000000"
        lx = x + int(np.argmax(m.sum(0)))
        # nodes: blobs on the line at item-title rows (their crop includes the line segment)
        nodes = []
        for l in sec_lines:
            if l["role"] != "item_title":
                continue
            ny0, ny1 = l["ink"][1] - int(0.8 * med_h), l["ink"][3] + int(0.8 * med_h)
            band = m[max(0, ny0 - y):max(0, ny1 - y)]
            if band.size == 0:
                continue
            widths = band.sum(1)
            if widths.max() > 2.2 * lw:
                rows = np.nonzero(widths > 1.6 * lw)[0]
                cols_ = np.nonzero(band[rows].any(0))[0]
                nx0, nx1 = x + cols_.min(), x + cols_.max() + 1
                nyy0, nyy1 = max(0, ny0) + rows.min(), max(0, ny0) + rows.max() + 1
                nodes.append([int(nx0), int(nyy0), int(nx1), int(nyy1), l["id"]])
        node = None
        if nodes:
            nx0, ny0, nx1, ny1, lid = nodes[0]
            crop = img[ny0:ny1, nx0:nx1]
            alpha = np.abs(crop.astype(np.int16) - img[ny0:ny1, max(0, nx0 - 3):max(1, nx0 - 2)].astype(np.int16).mean((0, 1))).sum(-1) > 60
            node = {"file": _save(os.path.join(out_dir, "crops", f"node_{sec['key']}_{sec['col']}.png"), _rgba(crop, alpha)),
                    "w_mm": round((nx1 - nx0) / MM, 2), "h_mm": round((ny1 - ny0) / MM, 2),
                    "cx_mm": round(((nx0 + nx1) / 2) / MM, 2), "dy_mm": None}
            title = next((l for l in sec_lines if l["id"] == lid), None)
            if title:
                node["dy_mm"] = round(((ny0 + ny1) / 2 - title["ink"][1]) / MM, 2)
        res["timeline"] = {"x_mm": round(lx / MM, 2), "w_mm": round(max(lw, 1) / MM, 2), "color": color,
                           "top_mm": round(y / MM, 2), "bottom_mm": round((y + h) / MM, 2), "node": node}
        free = [j for j in free if j != i]
    # bars: wide flat rectangles (one component, or fill + track side by side)
    flat = [i for i in free if stats[i, 2] > 5 * stats[i, 3] and stats[i, 3] < 4.5 * MM and stats[i, 2] > 8 * MM
            and stats[i, 4] > 0.6 * stats[i, 2] * stats[i, 3]]     # solid (text halos / chip outlines are ~0.3)
    if len(flat) >= 2 and sec["key"] in ("skills", "languages", "competencies", "interests"):
        # rows by vertical overlap (fill + track pieces of one bar sit side by side)
        groups_: list[list[int]] = []
        for i in sorted(flat, key=lambda i: stats[i, 1] + stats[i, 3] / 2):
            y, h = stats[i, 1], stats[i, 3]
            g0 = groups_[-1] if groups_ else None
            if g0 is not None:
                gy0 = min(stats[j, 1] for j in g0)
                gy1 = max(stats[j, 1] + stats[j, 3] for j in g0)
                if min(gy1, y + h) - max(gy0, y) > 0.5 * min(h, gy1 - gy0):
                    g0.append(i)
                    continue
            groups_.append([i])
        # split each row at horizontal gaps: two bars side by side (2-column skills) are separate bars
        pieces = []
        for grp in groups_:
            grp = sorted(grp, key=lambda i: stats[i, 0])
            cur = [grp[0]]
            for i in grp[1:]:
                prev_end = max(stats[j, 0] + stats[j, 2] for j in cur)
                if stats[i, 0] - prev_end > 2 * MM:
                    pieces.append(cur)
                    cur = [i]
                else:
                    cur.append(i)
            pieces.append(cur)
        bars = []
        for grp in pieces:
            x0 = min(stats[i, 0] for i in grp)
            x1 = max(stats[i, 0] + stats[i, 2] for i in grp)
            y0 = min(stats[i, 1] for i in grp)
            y1 = max(stats[i, 1] + stats[i, 3] for i in grp)
            ym = (y0 + y1) // 2
            row = img[ym].astype(np.int16)
            span = max(4, x1 - x0)
            k = max(2, span // 12)
            fill = np.median(row[x0 + 1:x0 + 1 + k], axis=0)
            # the bar may continue in a light track that blends with the background: extend while it differs
            if x0 - 2 > ax0:
                bgc = np.median(row[max(ax0, x0 - int(3 * MM)):x0 - 2], axis=0)
            else:
                bgc = row[min(ax1, W - 1) - 3]
            d_bg = np.abs(row - bgc).sum(-1)
            d_fill = np.abs(row - fill).sum(-1)
            te, miss = x1, 0
            while te < min(W - 1, ax1) and miss <= 3:
                if d_bg[te] > 9 and d_fill[te] >= 30:
                    miss = 0
                else:
                    miss += 1
                te += 1
            end = max(x1, te - miss)
            right = np.median(row[max(x0, end - 1 - k):end - 1], axis=0)
            track = right if np.abs(right - fill).sum() > 40 else None
            fe = end
            if track is not None:
                closer = np.abs(row[x0:end] - track).sum(-1) < np.abs(row[x0:end] - fill).sum(-1)
                idx = np.nonzero(closer)[0]
                fe = x0 + int(idx[0]) if len(idx) else end
            bars.append({"x0": x0, "x1": end, "y0": y0, "y1": y1, "fill": _hex(fill),
                         "track": _hex(track) if track is not None else None, "level": (fe - x0) / max(1, end - x0)})
            erase[max(0, y0 - 2):y1 + 2, max(0, x0 - 2):end + 2] = True
        if len(bars) >= 2:
            bars.sort(key=lambda b: b["y0"])
            hgt = float(np.median([b["y1"] - b["y0"] for b in bars]))
            widths = [b["x1"] - b["x0"] for b in bars]
            labels = [l for l in sec_lines if l["role"] in ("list", "body")]
            # bar position relative to its label: below the label or on its right
            below = 0
            gaps = []
            for b in bars:
                lab = [l for l in labels if l["ink"][3] <= b["y0"] + 2 and b["y0"] - l["ink"][3] < 3 * med_h
                       and l["ink"][0] < b["x1"]]
                side = [l for l in labels if abs((l["ink"][1] + l["ink"][3]) / 2 - (b["y0"] + b["y1"]) / 2) < med_h
                        and l["ink"][2] < b["x0"]]
                if lab and not side:
                    below += 1
                    gaps.append(b["y0"] - lab[-1]["ink"][3])
            radius = _end_radius(img, bars[0], hgt)
            # bar columns (2-column skill grids) and each bar's offset from its label on the same row
            x0s = sorted(b_["x0"] for b_ in bars)
            clusters = [[x0s[0]]]
            for v in x0s[1:]:
                if v - clusters[-1][-1] > 10 * MM:
                    clusters.append([v])
                else:
                    clusters[-1].append(v)
            dxs = []
            for b_ in bars:
                side_l = [l for l in labels if abs((l["ink"][1] + l["ink"][3]) / 2 - (b_["y0"] + b_["y1"]) / 2) < med_h
                          and l["ink"][2] < b_["x0"] and b_["x0"] - l["ink"][0] < 45 * MM]
                if side_l:
                    dxs.append(b_["x0"] - max(side_l, key=lambda l: l["ink"][0])["ink"][0])
            label_dx = float(np.median(dxs)) if dxs else 0.0
            res["bars"] = {"place": "below" if below >= len(bars) / 2 else "right", "h_mm": round(hgt / MM, 2),
                           "columns": len(clusters), "label_dx_mm": round(label_dx / MM, 2),
                           "col_x_mm": [round((min(c) - label_dx) / MM, 2) for c in clusters],
                           "w_mm": round(float(np.median(widths)) / MM, 2),
                           "x0_mm": round(float(np.median([b["x0"] for b in bars])) / MM, 2),
                           "fill": max(set(b["fill"] for b in bars), key=[b["fill"] for b in bars].count),
                           "track": next((b["track"] for b in bars if b["track"]), None),
                           "gap_mm": round(float(np.median(gaps)) / MM, 2) if gaps else 1.0,
                           "radius_mm": round(radius / MM, 2),
                           "levels": [round(b["level"], 2) for b in bars]}
            free = [i for i in free if i not in flat]
    # dots: rows of ≥3 similar round blobs
    blobs = [i for i in free if 0.6 < stats[i, 2] / max(1, stats[i, 3]) < 1.6 and 1.2 * MM < stats[i, 3] < 5 * MM
             and not any(overlaps(stats[i], l["box"]) for l in sec_lines)     # dot leaders inside text lines
             and _stands_out(img, cc, stats, i)]
    if len(blobs) >= 6 and sec["key"] in ("skills", "languages", "competencies"):
        rows = {}
        for i in blobs:
            rows.setdefault(int(stats[i, 1] // max(2, stats[i, 3])), []).append(i)
        good = [sorted(r, key=lambda i: stats[i, 0]) for r in rows.values() if len(r) >= 3]
        if len(good) >= 2:
            r0 = good[0]
            d = float(np.median([stats[i, 3] for i in r0]))
            pitch = float(np.median(np.diff([stats[i, 0] for i in r0])))
            cols_ = [img[stats[i, 1] + stats[i, 3] // 2, stats[i, 0] + stats[i, 2] // 2].astype(int) for g in good for i in g]
            lum = [c.sum() for c in cols_]
            on = _hex(cols_[int(np.argmin(lum))])
            off = _hex(cols_[int(np.argmax(lum))])
            n = int(np.median([len(g) for g in good]))
            res["dots"] = {"d_mm": round(d / MM, 2), "pitch_mm": round(pitch / MM, 2), "on": on,
                           "off": off if off != on else None, "n": n,
                           "x0_mm": round(float(np.median([stats[g[0], 0] for g in good])) / MM, 2),
                           "place": "right"}
    # chips: outlined/filled rounded boxes around text
    chips = []
    for l in sec_lines:
        bx = l["box"]
        cand = comps_in(bx[0] - 3 * med_h, bx[1] - 1.5 * med_h, bx[2] + 3 * med_h, bx[3] + 1.5 * med_h, 0.95)
        for i in cand:
            x, y, w, h, a = stats[i]
            ih = l["ink"][3] - l["ink"][1]
            pad = 0.45 * MM
            if (x <= l["ink"][0] - pad and x + w >= l["ink"][2] + pad and y <= l["ink"][1] - 1
                    and y + h >= l["ink"][3] + 1 and 1.3 * ih <= h < 3.5 * med_h and _stands_out(img, cc, stats, i)):
                chips.append((l, i))
                break
    if len(chips) >= 2:
        hs = np.array([stats[i, 3] for _, i in chips], float)
        chips = [(l, i) for l, i in chips if abs(stats[i, 3] - np.median(hs)) <= 0.2 * np.median(hs)]
    if len(chips) >= 2:
        for _, i in chips:
            erase |= cc == i
        l, i = chips[0]
        x, y, w, h, a = stats[i]
        m = cc[y:y + h, x:x + w] == i
        filled = m.mean() > 0.6
        border = _hex(np.median(img[y:y + h, x:x + w][m], axis=0))
        inner = l["bg"]
        bw_px = None
        if filled:
            # a low-res outlined chip reads as one blob: compare its edge pixels with its inside
            midrow = img[y + h // 2, x:x + w].astype(np.int16)
            inside = np.median(img[y + h // 2, x + int(0.35 * (l["ink"][0] - x)):l["ink"][0] - 1].astype(np.int16), axis=0) \
                if l["ink"][0] - x > 3 else midrow[w // 2]
            edge = midrow[0:2].mean(0)
            if np.abs(edge - inside).sum() > 24:
                k = 0
                while k < w // 3 and np.abs(midrow[k] - edge).sum() < np.abs(midrow[k] - inside).sum():
                    k += 1
                bw_px = max(1, k)
                border, inner, filled = _hex(edge), _hex(inside), False
        res["chips"] = {"h_mm": round(h / MM, 2), "pad_x_mm": round((l["ink"][0] - x) / MM, 2),
                        "radius_mm": round(_end_radius(img, {"x0": x, "x1": x + w, "y0": y, "y1": y + h}, h) / MM, 2),
                        "border": border, "fill": border if filled else inner,
                        "border_w_mm": (round(bw_px / MM, 2) if bw_px else
                                        round(float(np.median(m.sum(1)[h // 3:2 * h // 3])) / 2 / MM, 2)) if not filled else 0,
                        "gap_x_mm": round(_chip_gap(chips, stats) / MM, 2), "gap_y_mm": round(_chip_gap_y(chips, stats) / MM, 2),
                        "text_color": l["fg"]}
    return res


def _chip_gap(chips, stats) -> float:
    gaps = []
    for (l1, i1), (l2, i2) in zip(chips, chips[1:]):
        a, b = stats[i1], stats[i2]
        if abs(a[1] - b[1]) < a[3] / 2 and b[0] > a[0]:
            gaps.append(b[0] - (a[0] + a[2]))
    return float(np.median(gaps)) if gaps else 2 * MM


def _chip_gap_y(chips, stats) -> float:
    ys = sorted({int(stats[i, 1]) for _, i in chips})
    hs = [stats[i, 3] for _, i in chips]
    gaps = [b - a - float(np.median(hs)) for a, b in zip(ys, ys[1:]) if b - a > np.median(hs) * 0.8]
    return float(np.median(gaps)) if gaps else 1.5 * MM


def _end_radius(img, b, hgt) -> float:
    """Corner radius of a bar/chip: how far the left end is rounded (0 = square)."""
    x0, y0, y1 = int(b["x0"]), int(b["y0"]), int(b["y1"])
    mid = img[(y0 + y1) // 2, x0 + 1].astype(int)
    top = img[y0, x0].astype(int)
    if np.abs(mid - top).sum() < 60:
        return 0.0
    return hgt / 2 if hgt < 3 * MM else hgt / 4
