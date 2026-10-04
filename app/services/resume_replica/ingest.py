"""
ingest.py — Reference file → clean page image at a fixed working resolution.

* PDF references are rasterised from the vector source (pixel-exact at any resolution).
* Images: viewer chrome (grey/dark uniform borders around the page) is trimmed, the page is scaled so its
  width is A4 (210 mm) at PX_PER_MM, and the effective source DPI is reported so the caller can warn.
* A screenshot that shows only the top of a page keeps its real height (page_h_mm < 297); the plate builder
  extends it.
"""
from __future__ import annotations

import os

import numpy as np

PX_PER_MM = 1654 / 210.0          # 200 dpi working resolution
PAGE_W_MM = 210.0
PAGE_H_MM = 297.0


def _imread(path: str):
    import cv2
    data = np.fromfile(path, dtype=np.uint8)            # unicode-safe on Windows
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    return img


def _uniform(line: np.ndarray) -> bool:
    return float(line.std(axis=0).max()) < 9.0


def _viewerish(color: np.ndarray) -> bool:
    """Grey/dark colours typical of a viewer background (a white or tinted border is more likely page margin)."""
    c = color.astype(float)
    lum = (0.299 * c[2] + 0.587 * c[1] + 0.114 * c[0]) / 255
    sat = (c.max() - c.min()) / 255
    return lum < 0.88 and sat < 0.12


def _trim(img: np.ndarray) -> tuple[int, int, int, int]:
    """Trims uniform viewer-coloured borders. Returns x0, y0, x1, y1."""
    h, w = img.shape[:2]
    x0, y0, x1, y1 = 0, 0, w, h
    for _ in range(4):
        changed = False
        while y1 - y0 > h * 0.3 and _uniform(img[y0, x0:x1]) and _viewerish(img[y0, x0:x1].mean(0)):
            y0 += 1
            changed = True
        while y1 - y0 > h * 0.3 and _uniform(img[y1 - 1, x0:x1]) and _viewerish(img[y1 - 1, x0:x1].mean(0)):
            y1 -= 1
            changed = True
        while x1 - x0 > w * 0.3 and _uniform(img[y0:y1, x0]) and _viewerish(img[y0:y1, x0].mean(0)):
            x0 += 1
            changed = True
        while x1 - x0 > w * 0.3 and _uniform(img[y0:y1, x1 - 1]) and _viewerish(img[y0:y1, x1 - 1].mean(0)):
            x1 -= 1
            changed = True
        if not changed:
            break
    # thin dark rule near an edge (viewer frame line), possibly a few pixels in: trim through it
    lim = max(3, int(0.012 * (y1 - y0)))
    rows = [y for y in range(y0, min(y1, y0 + lim)) if img[y, x0:x1].mean() < 110 and _uniform(img[y, x0:x1])]
    if rows:
        y0 = rows[-1] + 1
    rows = [y for y in range(max(y0, y1 - lim), y1) if img[y, x0:x1].mean() < 110 and _uniform(img[y, x0:x1])]
    if rows:
        y1 = rows[0]
    for _ in range(4):
        if y1 - y0 > 50 and img[y0, x0:x1].mean() < 90 and _uniform(img[y0, x0:x1]):
            y0 += 1
        if x1 - x0 > 50 and img[y0:y1, x0].mean() < 90 and _uniform(img[y0:y1, x0]):
            x0 += 1
        if x1 - x0 > 50 and img[y0:y1, x1 - 1].mean() < 90 and _uniform(img[y0:y1, x1 - 1]):
            x1 -= 1
    return x0, y0, x1, y1


def _remove_viewer_overlays(img: np.ndarray) -> list:
    """Phone screenshots carry app overlays on top of the page: Google Lens' dark rounded button in the
    bottom-right corner and Chrome's dark URL pill ("storage.googleapis.com"). Both are removed (each row is
    interpolated between the colours just left and right of the overlay). Deliberately specific: a dark box
    of the design itself (a black heading bar…) never matches both the shape and the place."""
    import cv2
    H, W = img.shape[:2]
    mm = W / PAGE_W_MM
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sat = img.max(2).astype(int) - img.min(2).astype(int)
    dark = ((g < 70) & (sat < 22)).astype(np.uint8)
    dark = cv2.morphologyEx(dark, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    n, cc, st, _ = cv2.connectedComponentsWithStats(dark, connectivity=8)
    removed = []
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if a < 0.6 * w * h:
            continue
        inner = g[y:y + h, x:x + w]
        bright = float((inner > 190).mean())
        lens = (0.75 < w / max(1, h) < 1.35 and 7 * mm < w < 32 * mm and x + w > W - 30 * mm and y + h > H - 36 * mm
                and 0.02 < bright < 0.5)
        pill = (w / max(1, h) > 3.5 and 5 * mm < h < 26 * mm and abs(x + w / 2 - W / 2) < 0.18 * W
                and y > 0.55 * H and 0.03 < bright < 0.5 and w < 0.85 * W)
        if pill:
            # Chrome's URL pill starts with a blue site icon; a dark tab of the design itself does not
            lq = img[y:y + h, x:x + max(1, w // 4)].astype(int)
            blue = (lq[..., 0] > 150) & (lq[..., 2] < 140) & (lq[..., 0] - lq[..., 2] > 60)
            pill = blue.mean() > 0.01
        if not (lens or pill):
            continue
        x0, y0, x1, y1 = max(0, x - 4), max(0, y - 4), min(W, x + w + 4), min(H, y + h + 4)
        if w > h and y0 > 3 and y1 < H - 3:
            # wide pill: fill each column from the rows just above and below (keeps vertical edges such as a
            # sidebar boundary exact; a horizontal blend would smear a dark wedge across the page)
            top = img[max(0, y0 - 3):y0].astype(np.float32).mean(0)
            bot = img[y1:min(H, y1 + 3)].astype(np.float32).mean(0)
            t = np.linspace(0, 1, y1 - y0)[:, None, None]
            img[y0:y1, x0:x1] = (top[None, x0:x1] * (1 - t) + bot[None, x0:x1] * t).astype(np.uint8)
            removed.append(("lens" if lens else "pill", [int(x0), int(y0), int(x1), int(y1)]))
            continue
        left = img[y0:y1, max(0, x0 - 3):x0].astype(np.float32).mean(1) if x0 > 3 else None
        right = img[y0:y1, x1:min(W, x1 + 3)].astype(np.float32).mean(1) if x1 < W - 3 else None
        if left is None:
            left = right
        if right is None:
            right = left
        t = np.linspace(0, 1, x1 - x0)[None, :, None]
        img[y0:y1, x0:x1] = (left[:, None, :] * (1 - t) + right[:, None, :] * t).astype(np.uint8)
        removed.append(("lens" if lens else "pill", [int(x0), int(y0), int(x1), int(y1)]))
    return removed


def load_reference(path: str) -> dict:
    """Returns {img (BGR, page width = 210 mm at PX_PER_MM), page_h_mm, src_dpi, partial, letter, src_size}."""
    import cv2
    ext = os.path.splitext(path)[1].lower()
    target_w = int(round(PAGE_W_MM * PX_PER_MM))
    if ext == ".pdf":
        import fitz
        doc = fitz.open(path)
        pg = doc[0]
        zoom = target_w / pg.rect.width
        pix = pg.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
        img = np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, pix.n)[:, :, :3][:, :, ::-1].copy()
        doc.close()
        src_dpi = 200.0
        src_size = (img.shape[1], img.shape[0])
        x0, y0, x1, y1 = 0, 0, img.shape[1], img.shape[0]
    else:
        img = _imread(path)
        if img is None:
            raise ValueError(f"can't read image {path}")
        src_size = (img.shape[1], img.shape[0])
        x0, y0, x1, y1 = _trim(img)
        img = img[y0:y1, x0:x1]
        src_dpi = img.shape[1] / (PAGE_W_MM / 25.4)
    h, w = img.shape[:2]
    aspect = h / max(w, 1)
    letter = abs(aspect - 279.4 / 215.9) < 0.02
    f = target_w / w
    interp = cv2.INTER_AREA if f < 1 else cv2.INTER_CUBIC
    work = cv2.resize(img, (target_w, int(round(h * f))), interpolation=interp)
    if f > 1.6:                                         # upscaled: soften JPEG blocks / ringing on flat colour
        work = cv2.bilateralFilter(work, 5, 18, 5)
    overlays = [] if ext == ".pdf" else _remove_viewer_overlays(work)
    page_h_mm = work.shape[0] / PX_PER_MM
    if page_h_mm > PAGE_H_MM * 1.03:                    # taller than A4: keep the first page only
        work = work[:int(PAGE_H_MM * PX_PER_MM)]
        page_h_mm = PAGE_H_MM
    return {"img": work, "page_h_mm": page_h_mm, "src_dpi": round(src_dpi, 1),
            "partial": page_h_mm < PAGE_H_MM * 0.93, "letter": letter, "src_size": src_size,
            "crop": [int(x0), int(y0), int(x1), int(y1)], "is_pdf": ext == ".pdf", "overlays": overlays}
