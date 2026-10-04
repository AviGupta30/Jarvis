"""
fontmatch.py — Font identification against the local library (fonts.py), all in a headless Chromium canvas.

For each reference text sample, every candidate face draws the reference's own words on a canvas. Its ink box is
resampled onto the reference grid with the reference's own softness (low-res references are blurry upscales,
which would otherwise make every match look bold), then compared by normalised cross-correlation plus an
ink-mass penalty (so stroke weight counts). Pass 1: shape with the width stretched to fit. Pass 2: the top K
re-drawn with the letter-spacing that makes the widths equal, scaled by height only.
Font/ink metrics come from canvas TextMetrics (the same numbers CSS layout uses).
"""
from __future__ import annotations

import numpy as np

from .fonts import FONT_ORIGIN, SYSTEM_FONTS, font_face_css, load_index, route_fonts

NORM_H = 32              # comparison height (px) of the reference ink box

_MATCH_JS = r"""async (a) => {
  const {text, ref, rw, rh, srcH, cands, topk} = a;
  const gamma = a.gamma || 0.7;          // screen text renderers darken partially covered pixels; mimic it
  const LUT = new Uint8ClampedArray(256); for (let i = 0; i < 256; i++) LUT[i] = Math.round(255 * Math.pow(i / 255, gamma));
  const PAD = 6;
  const R = Float32Array.from(ref);
  let mR = 0; for (const v of R) mR += v; const massR = mR; mR /= R.length;
  let vR = 0; for (const v of R) vR += (v - mR) * (v - mR);
  const big = new OffscreenCanvas(64, 64), bctx = big.getContext('2d', {willReadFrequently: true});
  const small = new OffscreenCanvas(rw, rh), sctx = small.getContext('2d', {willReadFrequently: true});
  sctx.imageSmoothingEnabled = true; sctx.imageSmoothingQuality = 'high';
  const n = Math.max(1, [...text].length - 1);
  const targetW = rw / rh * srcH;                 // reference ink width in source pixels
  function render(c) {
    const fam = `"${c[0]}", "Zz Missing", monospace`;
    bctx.font = `${c[1]} 100px ${fam}`; bctx.letterSpacing = '0px';
    const m = bctx.measureText(text);
    const inkHem = (m.actualBoundingBoxAscent + m.actualBoundingBoxDescent) / 100;
    if (!(inkHem > 0.05)) return null;
    // draw at the reference's own pixel size, so low-res stem snapping/AA thickens it the same way
    const fs = srcH / inkHem;
    const inkW0 = (m.actualBoundingBoxLeft + m.actualBoundingBoxRight) / 100 * fs;
    // lower-case text is practically never letter-spaced: lock it, so a wrong font can't "fit" by squeezing
    const ls = a.lockLs ? 0 : Math.max(-0.12 * fs, Math.min(1.2 * fs, (targetW - inkW0) / n));
    const font = `${c[1]} ${fs}px ${fam}`;
    bctx.font = font; bctx.letterSpacing = ls + 'px';
    const m2 = bctx.measureText(text);
    const w = Math.ceil(m2.width + Math.abs(ls) * 2 + PAD * 2 + fs), h = Math.ceil(fs * 2.4 + PAD);
    if (big.width < w || big.height < h) {
      big.width = Math.max(big.width, w); big.height = Math.max(big.height, h);
      bctx.font = font; bctx.letterSpacing = ls + 'px';
    }
    bctx.clearRect(0, 0, w, h);
    bctx.fillStyle = '#000';
    bctx.fillText(text, PAD + fs * 0.3, fs * 1.6);
    const img = bctx.getImageData(0, 0, w, h), d = img.data;
    let x0 = w, y0 = h, x1 = -1, y1 = -1;
    for (let y = 0; y < h; y++) {
      const row = y * w * 4;
      for (let x = 0; x < w; x++) {
        const k = row + x * 4 + 3;
        d[k] = LUT[d[k]];
        if (d[k] > 107) { if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; }
      }
    }
    if (x1 < 0) return null;
    bctx.putImageData(img, 0, 0);
    sctx.clearRect(0, 0, rw, rh);
    sctx.drawImage(big, x0, y0, x1 - x0 + 1, y1 - y0 + 1, 0, 0, rw, rh);
    const sd = sctx.getImageData(0, 0, rw, rh).data;
    let mC = 0; const C = new Float32Array(rw * rh);
    let mx = 0;
    for (let i = 0; i < C.length; i++) { C[i] = sd[i * 4 + 3] / 255; if (C[i] > mx) mx = C[i]; }
    let cs = 0, cn = 0;
    for (let i = 0; i < C.length; i++) if (C[i] > 0.72 * mx) { cs += C[i]; cn++; }
    const core = Math.max(1e-3, cs / Math.max(1, cn));
    for (let i = 0; i < C.length; i++) { C[i] = Math.min(1, C[i] / core); mC += C[i]; }
    const massC = mC; mC /= C.length;
    let cov = 0, vC = 0;
    for (let i = 0; i < C.length; i++) { const a1 = R[i] - mR, b1 = C[i] - mC; cov += a1 * b1; vC += b1 * b1; }
    const ncc = cov / Math.sqrt(vR * vC + 1e-9);
    const aspect = Math.abs(Math.log(((x1 - x0 + 1) / (y1 - y0 + 1)) / (rw / rh)));
    return {family: c[0], weight: c[1], score: ncc - 0.5 * Math.abs(Math.log((massC + 1e-3) / (massR + 1e-3))) - 0.5 * aspect,
            ncc, mass: massC / Math.max(1e-3, massR), ls_em: ls / fs,
            asc_em: m.fontBoundingBoxAscent / 100, desc_em: m.fontBoundingBoxDescent / 100,
            ink_asc_em: m.actualBoundingBoxAscent / 100, ink_desc_em: m.actualBoundingBoxDescent / 100,
            ink_left_em: -m.actualBoundingBoxLeft / 100, width_em: m.width / 100};
  }
  const out = [];
  for (const c of cands) { const r = render(c); if (r) out.push(r); }
  out.sort((x, y) => y.score - x.score);
  return out.slice(0, topk);
}"""

_METRICS_JS = r"""(items) => {
  const c = new OffscreenCanvas(16, 16), ctx = c.getContext('2d');
  return items.map(it => {
    ctx.font = `${it.weight} 100px "${it.family}", "Zz Missing", monospace`;
    ctx.letterSpacing = (it.ls || 0) * 100 + 'px';
    const m = ctx.measureText(it.text || 'Hxg');
    return {asc_em: m.fontBoundingBoxAscent / 100, desc_em: m.fontBoundingBoxDescent / 100,
            ink_asc_em: m.actualBoundingBoxAscent / 100, ink_desc_em: m.actualBoundingBoxDescent / 100,
            ink_left_em: -m.actualBoundingBoxLeft / 100, ink_right_em: m.actualBoundingBoxRight / 100,
            width_em: m.width / 100};
  });
}"""


def _core_norm(t: np.ndarray) -> np.ndarray:
    """Scale so the stroke cores read 1.0 (same rule as the JS side: mean of values above 0.72 × max)."""
    mx = float(t.max())
    if mx <= 0:
        return t
    core = t[t > 0.72 * mx]
    return np.clip(t / max(1e-3, float(core.mean())), 0, 1)


def ref_map(img: np.ndarray, line: dict, src_scale: float):
    """Reference intensity map (0 = background, 1 = text colour) of a line's ink box at height NORM_H.
    Returns (flat list, rw, rh, ink height in source pixels) or None."""
    import cv2
    x0, y0, x1, y1 = line["ink"]
    crop = img[y0:y1, x0:x1].astype(np.float32)
    if crop.size == 0 or y1 - y0 < 3:
        return None
    bg = np.array([int(line["bg"][i:i + 2], 16) for i in (5, 3, 1)], np.float32)
    fg = np.array([int(line["fg"][i:i + 2], 16) for i in (5, 3, 1)], np.float32)
    span = float(np.abs(fg - bg).sum()) or 1.0
    t = np.clip(np.abs(crop - bg).sum(-1) / span, 0, 1)
    rh = NORM_H
    rw = max(4, int(round((x1 - x0) * rh / (y1 - y0))))
    if rw > 1100:
        return None
    t = cv2.resize(t, (rw, rh), interpolation=cv2.INTER_AREA)
    t = _core_norm(t)
    ink_h_src = (y1 - y0) / max(1.0, src_scale)
    return t.flatten().round(3).tolist(), rw, rh, float(max(3.0, ink_h_src))


class FontMatcher:
    """One warm Chromium page with the whole font library loaded. Use as a context manager."""

    def __init__(self, faces: list | None = None):
        self._pw = None
        self.browser = None
        self.page = None
        self.families: list[tuple[str, int]] = []
        self.gamma = 0.75
        self._only = [tuple(f) for f in faces] if faces is not None else None

    def __enter__(self):
        from playwright.sync_api import sync_playwright
        self._pw = sync_playwright().start()
        try:
            self.browser = self._pw.chromium.launch(headless=True)
        except Exception:
            self.browser = self._pw.chromium.launch(headless=True, channel="msedge")
        self.page = self.browser.new_page()
        route_fonts(self.page)
        idx = load_index()
        self.page.set_content(f"<!doctype html><html><head><base href='{FONT_ORIGIN}'><style>{font_face_css()}</style>"
                              "</head><body></body></html>")
        faces = [(fam, int(w)) for fam, info in idx.items() for w in info["weights"]]
        if self._only is not None:
            want = set(self._only)
            faces = [f for f in faces if f in want]
        self.page.evaluate("""async (faces) => { await Promise.all(faces.map(([f, w]) =>
            document.fonts.load(`${w} 32px "${f}"`).catch(() => null))); return true; }""", faces)
        sysf = self._installed_system_fonts()
        if self._only is not None:
            sysf = [f for f in sysf if f in set(self._only)]
        self.families = faces + sysf
        return self

    def __exit__(self, *a):
        try:
            self.browser.close()
        finally:
            self._pw.stop()

    def _installed_system_fonts(self) -> list[tuple[str, int]]:
        js = """(names) => { const c = document.createElement('canvas').getContext('2d'); const t = 'abcdefghijklmnopqrstuvwxyz0123456789 WMQ';
          const w = f => { c.font = '40px ' + f; return c.measureText(t).width; };
          const b1 = w('monospace'), b2 = w('serif');
          return names.filter(n => w(`'${n}', monospace`) !== b1 || w(`'${n}', serif`) !== b2); }"""
        try:
            names = self.page.evaluate(js, SYSTEM_FONTS)
        except Exception:
            names = []
        out = []
        for n in names:
            out += [(n, 400), (n, 700)]
        return out

    def match(self, samples: list[dict], top_k: int = 24, candidates: list | None = None) -> list[list[dict]]:
        """samples: [{text, ref, rw, rh, src_h}] (see ref_map). Returns per sample a ranked candidate list."""
        cands = [list(c) for c in (candidates or self.families)]
        out = []
        for smp in samples:
            try:
                out.append(self.page.evaluate(_MATCH_JS, {"text": smp["text"], "ref": smp["ref"], "rw": smp["rw"],
                                                          "rh": smp["rh"], "srcH": smp["src_h"], "cands": cands,
                                                          "topk": top_k, "gamma": self.gamma,
                                                          "lockLs": bool(smp.get("lock_ls"))}))
            except Exception as e:
                print(f"[replica] font match failed: {e}")
                out.append([])
        return out

    def metrics(self, items: list[dict]) -> list[dict]:
        """items: [{text, family, weight, ls}] → font/ink metrics in em (for the CSS half-leading model)."""
        try:
            return self.page.evaluate(_METRICS_JS, items)
        except Exception as e:
            print(f"[replica] font metrics failed: {e}")
            return [None] * len(items)


# ── parallel two-stage search ──────────────────────────────────────────────────────────────────────

def _worker(jobs: list) -> list:
    """Runs in a separate process: jobs = [(sample, candidates, top_k)] → result lists."""
    faces = sorted({tuple(c) for _, cands, _ in jobs for c in cands})
    out = []
    with FontMatcher(faces=faces) as fm:
        for smp, cands, k in jobs:
            out.append(fm.match([smp], top_k=k, candidates=cands)[0])
    return out


def run_jobs(jobs: list, workers: int = 4) -> list:
    """[(sample, candidates, top_k)] → results, spread over worker processes (one Chromium each)."""
    if not jobs:
        return []
    workers = max(1, min(workers, len(jobs)))
    if workers == 1:
        return _worker(jobs)
    from concurrent.futures import ProcessPoolExecutor
    chunks = [jobs[i::workers] for i in range(workers)]
    results: list = [None] * len(jobs)
    with ProcessPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(_worker, ch) for ch in chunks]
        for wi, f in enumerate(futs):
            for j, r in enumerate(f.result()):
                results[wi + j * workers] = r
    return results


def all_faces() -> list[tuple[str, int]]:
    idx = load_index()
    if not idx:                                   # fresh machine: fetch the library once (popular families first)
        from .fonts import ensure_library
        idx = ensure_library(top_n=200)
    faces = [(fam, int(w)) for fam, info in idx.items() for w in info["weights"]]
    return faces + [(n, w) for n in SYSTEM_FONTS for w in (400, 700)]


def identify(samples: list[dict], workers: int = 4, log=None) -> list[list[dict]]:
    """Stage 1: regular + bold of every family. Stage 2: every weight of each sample's 10 best families."""
    faces = all_faces()
    by_fam: dict[str, list[int]] = {}
    for f, w in faces:
        by_fam.setdefault(f, []).append(w)
    stage1 = []
    for f, ws in by_fam.items():
        pick = {min(ws, key=lambda w: abs(w - 400)), min(ws, key=lambda w: abs(w - 700))}
        stage1 += [(f, w) for w in sorted(pick)]
    r1 = run_jobs([(smp, stage1, 80) for smp in samples], workers)
    jobs2 = []
    for smp, r in zip(samples, r1):
        fams = []
        for x in r or []:
            if x["family"] not in fams:
                fams.append(x["family"])
            if len(fams) >= 10:
                break
        jobs2.append((smp, [(f, w) for f in fams for w in sorted(by_fam.get(f, [400]))], 60))
    if log:
        log("   refining weights…")
    return run_jobs(jobs2, workers)
