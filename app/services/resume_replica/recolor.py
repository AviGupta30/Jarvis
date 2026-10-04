"""
recolor.py — "change this colour everywhere" for the raster parts of an exact copy
==================================================================================
An exact copy draws its background, heading boxes, icons and bars from images cut out of the reference, so a
colour change can't be CSS there. The editor's colour mode stores pairs [from_hex, to_hex] in design.free.recolor;
the page runtime swaps CSS colours, and this module swaps the same colours in those images (editor and PDF use the
same output, so they stay identical).

Anti-aliasing is kept by unmixing: an edge pixel p is a blend a·src + (1−a)·c of the colour being changed and some
other colour c of the image (one of its dominant colours, white or black), so it becomes p + a·(dst − src).
Pixels that are themselves another dominant colour of the image are never touched (a light tint used as a box
fill is its own colour, changeable separately). Work is done per unique colour, so a full A4 plate takes ~0.3 s.
"""

from __future__ import annotations

import io

import numpy as np

TOL = 14.0           # RGB distance: still "the same colour" (JPEG noise, resampling)
MERGE = 22.0         # dominant colours closer than this are one colour
SAME = 26.0          # this close to the colour being changed (and closer to it than to any other): it IS that colour


def _hex(c: str) -> np.ndarray | None:
    c = str(c or "").strip().lstrip("#")
    if len(c) == 3:
        c = "".join(ch * 2 for ch in c)
    try:
        return np.array([int(c[i:i + 2], 16) for i in (0, 2, 4)], np.float32) if len(c) == 6 else None
    except ValueError:
        return None


def clean_pairs(pairs) -> list[tuple[np.ndarray, np.ndarray]]:
    out = []
    for p in pairs or []:
        if isinstance(p, (list, tuple)) and len(p) == 2:
            a, b = _hex(p[0]), _hex(p[1])
            if a is not None and b is not None and np.abs(a - b).max() > 0:
                out.append((a, b))
    return out


def _unique(rgb: np.ndarray):
    flat = rgb.reshape(-1, 3)
    packed = (flat[:, 0].astype(np.int32) << 16) | (flat[:, 1].astype(np.int32) << 8) | flat[:, 2].astype(np.int32)
    uniq, inv, cnt = np.unique(packed, return_inverse=True, return_counts=True)
    U = np.stack([(uniq >> 16) & 255, (uniq >> 8) & 255, uniq & 255], 1).astype(np.float32)
    return U, inv, cnt


def dominant(U: np.ndarray, cnt: np.ndarray, min_share: float = 0.002, k: int = 16) -> list[tuple[np.ndarray, int]]:
    """Greedy merge of the most frequent colours → [(colour, pixel count)], most used first."""
    order = np.argsort(-cnt)
    total = float(cnt.sum()) or 1.0
    pal: list[list] = []
    for i in order[:4000]:
        if cnt[i] / total < min_share * 0.25:
            break
        c = U[i]
        for p in pal:
            if np.linalg.norm(p[0] - c) < MERGE:
                p[1] += int(cnt[i])
                break
        else:
            pal.append([c, int(cnt[i])])
    pal = [p for p in pal if p[1] / total >= min_share]
    pal.sort(key=lambda p: -p[1])
    # anti-aliasing shades: a little-used colour that is a mix of two more-used ones (or of one and white/black)
    kept: list[list] = []
    for c, n in pal:
        ends = kept + [[np.array([255, 255, 255], np.float32), total], [np.array([0, 0, 0], np.float32), total]]
        blend = False
        for i, (a, na) in enumerate(ends):
            for b, nb in ends[i + 1:]:
                v = a - b
                if float(v @ v) < 1.0:
                    continue
                t = float((c - b) @ v) / float(v @ v)
                if 0.06 < t < 0.94 and np.linalg.norm(c - (b + t * v)) < TOL * 0.8 and n < 0.25 * min(na, nb):
                    blend = True
                    break
            if blend:
                break
        if not blend:
            kept.append([c, n])
    return [(p[0], p[1]) for p in kept[:k]]


def recolor_rgb(rgb: np.ndarray, pairs) -> np.ndarray:
    """rgb: H×W×3 uint8 (RGB order). Returns a recoloured copy."""
    pairs = clean_pairs(pairs)
    if not pairs:
        return rgb
    U, inv, cnt = _unique(rgb)
    pal = [c for c, _ in dominant(U, cnt)]
    ends = pal + [np.array([255, 255, 255], np.float32), np.array([0, 0, 0], np.float32)]
    shift = np.zeros_like(U)
    for src, dst in pairs:
        others = [c for c in ends if np.linalg.norm(c - src) > MERGE]
        best_res = np.linalg.norm(U - src, axis=1)
        best_a = np.ones(len(U), np.float32)
        for c in others:
            v = src - c
            a = np.clip(((U - c) @ v) / float(v @ v), 0.0, 1.0)
            res = np.linalg.norm(U - (c + a[:, None] * v), axis=1)
            better = res < best_res
            best_res = np.where(better, res, best_res)
            best_a = np.where(better, a, best_a)
        hit = (best_res < TOL) & (best_a > 0.03)
        d_src = np.linalg.norm(U - src, axis=1)
        nearest_other = np.full(len(U), 1e9, np.float32)
        for c in pal:                                  # another colour of the design stays itself
            if np.linalg.norm(c - src) > MERGE:
                dc = np.linalg.norm(U - c, axis=1)
                hit &= dc >= TOL * 0.75
                nearest_other = np.minimum(nearest_other, dc)
        # the colour itself, with its faint noise (JPEG, erased-text residue): a full shift keeps the noise as faint as
        # it was — unmixing it against white would turn it into visible light specks on a dark new colour
        same = (d_src < SAME) & (d_src < nearest_other)
        best_a = np.where(same, 1.0, best_a)
        hit |= same
        shift[hit] += best_a[hit, None] * (dst - src)
    out = np.clip(U + shift, 0, 255).round().astype(np.uint8)
    return out[inv.reshape(-1)].reshape(rgb.shape)


def recolor_file(path: str, pairs) -> bytes | None:
    """PNG bytes of the recoloured image (alpha kept), or None when nothing applies / unreadable."""
    try:
        from PIL import Image
        im = Image.open(path)
        im.load()
        alpha = im.getchannel("A") if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info) else None
        rgb = np.asarray(im.convert("RGB"))
        new = recolor_rgb(rgb, pairs)
        if new is rgb:
            return None
        out = Image.fromarray(new, "RGB")
        if alpha is not None:
            out.putalpha(alpha)
        buf = io.BytesIO()
        out.save(buf, "PNG", optimize=False, compress_level=3)
        return buf.getvalue()
    except Exception as e:
        print(f"[replica] recolour failed for {path}: {e}")
        return None


def palette_of(paths: list[str], k: int = 14) -> list[str]:
    """The dominant colours over a set of images (weighted by pixels) as hex, most used first."""
    from PIL import Image
    acc: list[list] = []
    for p in paths:
        try:
            im = Image.open(p).convert("RGBA")
            im.thumbnail((420, 600))
            a = np.asarray(im)
            rgb = a[:, :, :3][a[:, :, 3] > 200]
            if not len(rgb):
                continue
            U, _, cnt = _unique(rgb.reshape(-1, 1, 3))
            for c, n in dominant(U, cnt, min_share=0.004):
                for q in acc:
                    if np.linalg.norm(q[0] - c) < MERGE:
                        q[1] += n
                        break
                else:
                    acc.append([c, n])
        except Exception:
            continue
    acc.sort(key=lambda q: -q[1])
    return ["#%02x%02x%02x" % tuple(int(round(x)) for x in q[0]) for q in acc[:k]]
