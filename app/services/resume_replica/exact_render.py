"""
exact_render.py — Exact-template spec (pipeline.py) + resume content → print-ready HTML.

Layers:
  1. the reference's own background plate (page 1) and its continuation plate (pages 2+, position:fixed)
  2. header slots at their measured positions: name, title, photo frame, header contact (+ original icons)
  3. the columns, flowing with the measured fonts / sizes / letter-spacing / colours and the measured vertical
     rhythm (every gap is an ink-top → ink-top distance from the reference, converted to CSS margins with the
     font's half-leading), heading decorations as 9-slice images cut from the reference, bullets/icons/timeline
     nodes as the reference's own pixels, skill graphics redrawn from their measurements.
The DOM mirrors the legacy renderer's editor hooks (section.sec.sec-<key> > h2, data-f spans, data-item).
"""
from __future__ import annotations

import base64
import difflib
import json
import os
import re

_SPEC_CACHE: dict = {}
_URI_CACHE: dict = {}

_SIDE_KEYS = {"contact", "skills", "languages", "interests", "certifications", "achievements", "highlights",
              "references", "competencies"}
_MAIN_KEYS = {"profile", "experience", "projects", "education"}
_TITLES = ["Work Experience", "Professional Experience", "Experience", "Employment History", "Education",
           "Academic Background", "Skills", "Technical Skills", "Software Skills", "Key Skills", "Contact",
           "Contact Me", "My Contact", "Profile", "About Me", "About Myself", "Summary", "Professional Summary",
           "Overview", "Objective", "Certifications", "Certificates", "Courses", "Training and Courses",
           "Achievements", "Awards", "Honors and Awards", "Languages", "Language", "Interests", "Hobbies",
           "Favourite Hobbies", "Projects", "References", "Reference", "Personal Information", "Personal Details",
           "Core Competencies", "Expertise", "Areas of Expertise", "Career Highlights", "Highlights",
           "Strengths", "Tools", "Technologies", "Publications", "Volunteer Experience", "Other Technologies"]


def load_spec(sha1: str) -> dict | None:
    if sha1 in _SPEC_CACHE:
        return _SPEC_CACHE[sha1]
    from .pipeline import load_spec as _load
    spec = _load(sha1)
    if spec:
        _SPEC_CACHE[sha1] = spec
    return spec


def _uri(path: str) -> str:
    if not path or not os.path.exists(path):
        return ""
    key = (path, os.path.getmtime(path))
    if key not in _URI_CACHE:
        ext = os.path.splitext(path)[1].lower()
        mime = "image/jpeg" if ext in (".jpg", ".jpeg") else "image/png"
        with open(path, "rb") as f:
            _URI_CACHE[key] = f"data:{mime};base64," + base64.b64encode(f.read()).decode()
    return _URI_CACHE[key]


def _png_px_per_mm(path: str, mm_w: float) -> float:
    try:
        from PIL import Image
        with Image.open(path) as im:
            return im.width / max(0.1, mm_w)
    except Exception:
        return 1654 / 210.0


def canon_title(text: str, key: str) -> str:
    """OCR'd heading → a properly spelled/spaced title ("PERSONALINFORMATION" → "Personal Information")."""
    from app.services.resume_builder import DEFAULT_TITLES
    t = re.sub(r"[^a-z]", "", (text or "").lower())
    if t:
        best, score = None, 0.0
        for cand in _TITLES:
            r = difflib.SequenceMatcher(None, t, re.sub(r"[^a-z]", "", cand.lower())).ratio()
            if r > score:
                best, score = cand, r
        if best and score >= 0.84:
            return best
    return DEFAULT_TITLES.get(key, key.replace("_", " ").title())


# ── styles ─────────────────────────────────────────────────────────────────────────────────────────

class Styles:
    def __init__(self, spec: dict, scale: float):
        self.st = spec.get("styles") or {}
        self.s = scale
        from .fonts import load_index
        idx = load_index()
        self.cat = {f: (idx.get(f) or {}).get("category", "") for f in {v["family"] for v in self.st.values()}}
        bodies = [k for k in self.st if k.startswith("body")] or list(self.st)
        self.default = max(bodies, key=lambda k: self.st[k].get("n", 0)) if bodies else None
        self.g = 1.0                     # whitespace factor (< 1 when fitting a page target)

    def pick(self, *keys) -> str | None:
        for k in keys:
            if k and k in self.st:
                return k
        return self.default

    def css(self) -> str:
        out = []
        for k, v in self.st.items():
            cat = (self.cat.get(v["family"]) or "").lower()
            generic = "serif" if "serif" in cat and "sans" not in cat else ("monospace" if "mono" in cat else
                                                                          ("cursive" if "hand" in cat else "sans-serif"))
            out.append(f".k-{k}{{font-family:'{v['family']}',{generic};font-weight:{v['weight']};"
                       f"font-size:{v['size'] * self.s:.3f}mm;line-height:{self.pitch(k):.3f}mm;"
                       f"letter-spacing:{v['ls']:.4f}em;color:{v['color']};"
                       f"text-transform:{'uppercase' if v['upper'] else 'none'}}}")
        return "\n".join(out)

    def fs(self, k) -> float:
        return (self.st.get(k) or {}).get("size", 3.4) * self.s

    def pitch(self, k) -> float:
        v = self.st.get(k) or {}
        fs = v.get("size", 3.4)
        p = v.get("pitch") or fs * 1.32
        if not (1.0 * fs <= p <= 1.75 * fs):
            p = fs * 1.32
        return p * self.s

    def lead(self, k) -> float:
        """Line box top → ink top (mm) for a line of style k (half-leading model, line-height = pitch)."""
        v = self.st.get(k) or {}
        fs = self.fs(k)
        L = self.pitch(k)
        asc, desc, ink = v.get("asc", 0.92), v.get("desc", 0.24), v.get("ink_asc", 0.72)
        return (L - (asc + desc) * fs) / 2 + (asc - ink) * fs

    def ink_h(self, k) -> float:
        v = self.st.get(k) or {}
        return v.get("ink_asc", 0.72) * self.fs(k)

    def lead1(self, k) -> float:
        """Same for line-height:1 (absolutely positioned header text)."""
        v = self.st.get(k) or {}
        fs = self.fs(k)
        asc, desc, ink = v.get("asc", 0.92), v.get("desc", 0.24), v.get("ink_asc", 0.72)
        return (fs - (asc + desc) * fs) / 2 + (asc - ink) * fs


def _m(v: float) -> str:
    return f"{v:.2f}mm"


# ── main ───────────────────────────────────────────────────────────────────────────────────────────

def render_replica_html(c: dict, d: dict, photo_uri: str, scale: float = 1.0) -> str:
    from app.services import resume_builder as rb
    rep = d.get("replica") or {}
    spec = load_spec(rep.get("sha1", ""))
    if not spec:
        # cache cleared or the analysis format changed: rebuild it from the reference file
        path = rep.get("path") or ""
        if not os.path.exists(path) and rep.get("source"):
            from .pipeline import _BASE
            path = os.path.join(_BASE, "data", "uploads", rep["source"])
        if os.path.exists(path):
            from .pipeline import analyse_reference
            spec = analyse_reference(path)
            if spec:
                _SPEC_CACHE[rep.get("sha1", "")] = spec
    if not spec:
        raise RuntimeError("replica spec missing (reference image not found)")
    if scale >= 0.85:
        f_scale, g_scale = 1.0, 1.0 - (1.0 - scale) / 0.15 * 0.6
    else:
        f_scale, g_scale = scale / 0.85, 0.4
    S = Styles(spec, f_scale)
    S.g = max(0.4, min(1.0, g_scale))
    ctx = {"S": S, "spec": spec, "c": c, "d": d, "rb": rb, "squeeze": scale < 0.999}
    plate1, plate2 = _uri(spec["page"]["plate"]), _uri(spec["page"]["plate2"])
    from .fonts import embed_css
    font_css = embed_css({f: w for f, w in (spec.get("fonts") or {}).items()})

    header = _header_html(ctx, photo_uri)
    placement = _place_sections(ctx)
    cols_html = []
    prev_right = 0.0
    page2_top = 12.0
    for ci, col in enumerate(spec["columns"]):
        secs = placement[ci]
        x0 = col["text_x"]
        w = max(20.0, col["x1"] - x0)
        inner = []
        prev = None                      # (last style key, ) of the previous block for gap conversion
        for i, (sec, key, title, ref) in enumerate(secs):
            html, last_key = _section_html(ctx, ci, col, sec, key, title, ref, prev, first=(i == 0))
            if html:
                inner.append(html)
                prev = (last_key, sec)
        first_top = (secs[0][0]["top"] if secs else col["top"])
        cols_html.append(f'<div class="col" style="margin-left:{_m(x0 - prev_right)};width:{_m(w)}">'
                         f'<div style="height:{_m(max(0.0, first_top))}"></div>{"".join(inner)}</div>')
        prev_right = x0 + w
    bottom_pad = max(8.0, min(40.0, 297.0 - max(c_["bottom"] for c_ in spec["columns"]) - 2.0))
    edit = rb._EDIT.get() is True
    css = _CSS.replace("%PAGE2TOP%", _m(page2_top)) + S.css()
    plate_css = (f".plate2{{background-image:url('{plate2}')}}.plate1{{background-image:url('{plate1}')}}")
    title = rb._e(c.get("name") or "Resume")
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{title} — Resume</title>'
            f'<style>{font_css}</style><style>{css}{plate_css}</style></head><body class="replica" data-ptop="{page2_top}" data-pbot="{bottom_pad:.2f}" style="--s:{scale}">'
            f'<div class="plate2"></div><div class="plate1"></div>{header}'
            f'<div class="cols">{"".join(cols_html)}</div>'
            f'{rb._free_html(d, edit)}'
            f'<script>window.__RBG__={json.dumps(_bg_grid(spec), separators=(",", ":"))};</script>'
            # layout scripts measure text, so they run once the embedded fonts are in (the PDF export waits for
            # data-ready): the editor and the PDF see the same metrics and make the same decisions
            f'<script>(document.fonts?document.fonts.ready:Promise.resolve()).then(function(){{'
            f'{_FIT_JS};window.__rbLayout=function(){{{_PAGINATE_JS};{_CONTRAST_JS};}};window.__rbLayout();'
            f'document.body.dataset.ready="1";var __t;document.addEventListener("input",function(){{'
            f'clearTimeout(__t);__t=setTimeout(window.__rbLayout,250);}});}});</script></body></html>')


_CSS = """
@page{size:A4;margin:0}
html,body{margin:0;padding:0}
body.replica{width:210mm}
@media print{html,body{width:210mm;overflow:hidden}}
body.replica{width:210mm;position:relative;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.plate2{position:absolute;left:0;top:297mm;bottom:0;width:210mm;background-size:210mm 297mm;background-repeat:repeat-y;z-index:0}
body.replica [data-f]{padding:0!important}
.pgsp{display:block;width:100%}
.plate1{position:absolute;left:0;top:0;width:210mm;height:297mm;background-size:210mm 297mm;background-repeat:no-repeat;z-index:1}
.hx{position:absolute;z-index:3;white-space:nowrap;line-height:1!important;margin:0}
.hx-ic{position:absolute;z-index:3}
.ph{position:absolute;z-index:3;overflow:hidden;background-size:cover;background-repeat:no-repeat}
.ph-empty{display:flex;align-items:center;justify-content:center;font:700 14mm/1 'Segoe UI',Arial,sans-serif}
.cols{position:relative;z-index:2;display:flex;align-items:flex-start}
.col{flex:none}
.col>div:first-child{margin-top:0}
section.sec{margin:0;padding:0;display:flow-root}
section.sec h2{margin:0;padding:0;font:inherit}
.hd{position:relative;display:flow-root;box-sizing:content-box}
.hd-hug{display:block;width:fit-content}
.hdw>h2{flex:none}
.hd .t{display:block;white-space:nowrap}
.blk{display:block;position:relative;margin:0;overflow-wrap:anywhere}
.row{display:flex;justify-content:space-between;align-items:baseline;gap:3mm;position:relative}
.row>.r{flex:none;text-align:right;white-space:nowrap}
.gl{position:absolute;display:block}
.item{position:relative}
.tl{position:absolute;display:block}
.chips{display:flex;flex-wrap:wrap}
.chip{display:inline-flex;align-items:center;box-sizing:border-box;white-space:nowrap}
.bar{position:relative;overflow:hidden}
.bar>i{position:absolute;left:0;top:0;bottom:0;display:block}
.dots{display:inline-flex;align-items:center}
.dots>i{display:block;border-radius:50%}
"""

# Contrast guard: text that flows onto a different background than in the reference (e.g. out of a dark
# sidebar onto white paper) switches to the most readable colour of the design's own palette.
_CONTRAST_JS = r"""(function(){const G=window.__RBG__;if(!G)return;const P=3.7795;
const lum=c=>{const f=v=>{v/=255;return v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4)};return 0.2126*f(c[0])+0.7152*f(c[1])+0.0722*f(c[2])};
const con=(a,b)=>{const x=lum(a),y=lum(b);return (Math.max(x,y)+0.05)/(Math.min(x,y)+0.05)};
const parse=s=>{const m=s.match(/[\d.]+/g);return m?m.slice(0,3).map(Number):[0,0,0]};
const body=document.body.getBoundingClientRect();
document.querySelectorAll('.cols [class^="k-"],.cols [class*=" k-"],.hx').forEach(e=>{
 if(e.closest('[data-nc]'))return;const r=e.getBoundingClientRect();if(!r.width||!r.height)return;
 const x0=(r.left-body.left)/P,y0=(r.top-body.top)/P,x1=x0+r.width/P,y1=y0+r.height/P;
 const page=Math.max(0,Math.floor((y0+y1)/2/297)),g=page?G.p2:G.p1,a=y0-page*297,b=y1-page*297;
 let acc=[0,0,0],n=0;
 for(let y=Math.max(0,Math.floor(a/G.c));y<=Math.min(G.h-1,Math.floor(b/G.c));y++)
  for(let x=Math.max(0,Math.floor(x0/G.c));x<=Math.min(G.w-1,Math.floor(x1/G.c));x++){const i=(y*G.w+x)*3;acc[0]+=g[i];acc[1]+=g[i+1];acc[2]+=g[i+2];n++;}
 if(!n)return;const bg=acc.map(v=>v/n),fg=parse(getComputedStyle(e).color);
 const km=(e.className.match(/k-([\w]+)/)||[])[1];const lim=Math.min(2.3,0.7*((G.rc&&G.rc[km])||4.5));
 if(con(fg,bg)>=lim)return;let best=null,bc=0;
 for(const c of G.pal){const cc=con(c,bg);if(cc>bc){bc=cc;best=c;}}
 if(best)e.style.color=`rgb(${best[0]},${best[1]},${best[2]})`;});})();"""

# Page breaks, decided once in the page itself (same code on screen and in print): a block that would cross the
# bottom margin moves to the next page behind an explicit spacer (a spacer's height survives a print break; a
# margin would not), headings and an item's first line stay with what follows. Print therefore never has to split
# anything itself, and the editor shows exactly what the PDF prints. The body ends on a whole page.
_PAGINATE_JS = r"""(function(){const P=3.7795,PH=297,b=document.body,TOP=parseFloat(b.dataset.ptop||'12'),
BOT=parseFloat(b.dataset.pbot||'10');const y=e=>(e.getBoundingClientRect().top-b.getBoundingClientRect().top)/P;
document.querySelectorAll('.pgsp').forEach(e=>e.remove());
const atoms=Array.from(document.querySelectorAll('.col .hdw,.col h2.hd,.col .blk,.col .row,.col .chips,.col .bargrid'))
 .filter(e=>!e.parentElement.closest('.hdw,.chips,.bargrid,.blk,.row'));
for(let i=0;i<atoms.length;i++){let e=atoms[i];const h=e.getBoundingClientRect().height/P;if(h<=0)continue;
 const t=y(e),k=Math.floor(t/PH),lim=(k+1)*PH-BOT;if(t+h<=lim+0.05||h>PH-TOP-BOT)continue;
 const p=atoms[i-1];
 if(p&&Math.floor(y(p)/PH)===k&&(p.matches('.hdw,h2.hd')||(p.parentElement===e.parentElement&&p===p.parentElement.firstElementChild&&p.parentElement.classList.contains('item'))))e=p;
 const need=(k+1)*PH+TOP-y(e);if(need<=0)continue;
 const sp=document.createElement('div');sp.className='pgsp';sp.style.height=need+'mm';e.parentNode.insertBefore(sp,e);}
const pages=Math.max(1,Math.ceil((b.scrollHeight/P-0.5)/PH));b.style.minHeight=(pages*PH-0.6)+'mm';
b.dataset.pages=pages;})();"""

_GRID_CACHE: dict = {}


def _bg_grid(spec: dict, cell: float = 3.0) -> dict:
    """Coarse RGB grid of both background plates (for the contrast guard)."""
    import cv2
    key = (spec["page"]["plate"], spec["page"]["plate2"], cell)
    if key in _GRID_CACHE:
        return _GRID_CACHE[key]
    w, h = int(210 / cell), int(297 / cell)
    out = {"c": cell, "w": w, "h": h}
    for name, path in (("p1", spec["page"]["plate"]), ("p2", spec["page"]["plate2"])):
        import numpy as np
        img = cv2.imdecode(np.fromfile(path, np.uint8), cv2.IMREAD_COLOR)
        small = cv2.resize(img, (w, h), interpolation=cv2.INTER_AREA)[:, :, ::-1]
        out[name] = small.reshape(-1).tolist()
    pal = {v.get("color") for v in (spec.get("styles") or {}).values() if v.get("color")} | {"#1d1d1f", "#ffffff"}
    out["pal"] = [[int(c[i:i + 2], 16) for i in (1, 3, 5)] for c in pal]
    out["rc"] = {k: v.get("ref_contrast", 4.5) for k, v in (spec.get("styles") or {}).items()}
    _GRID_CACHE[key] = out
    return out


_FIT_JS = r"""(function(){const P=3.7795;document.querySelectorAll('[data-fit]').forEach(e=>{const max=parseFloat(e.dataset.fit)*P;
const fs0=parseFloat(getComputedStyle(e).fontSize),mn=parseFloat(e.dataset.min||'0.3');let fs=fs0,i=0;
while(e.scrollWidth>max&&fs>fs0*mn&&i++<40){fs*=0.97;e.style.fontSize=fs+'px';}
if(e.scrollWidth>max){e.style.whiteSpace='normal';e.style.width=(max/P)+'mm';e.style.lineHeight='1.15';}});
const BR=document.body.getBoundingClientRect(),B=BR.top,G=window.__RBG__;
const at=(x,y)=>{if(!G)return null;const cx=Math.min(G.w-1,Math.max(0,Math.floor(x/G.c))),cy=Math.min(G.h-1,Math.max(0,Math.floor(y/G.c)));const i=(cy*G.w+cx)*3;return [G.p1[i],G.p1[i+1],G.p1[i+2]];};
const differ=(a,b)=>!a||!b||Math.abs(a[0]-b[0])+Math.abs(a[1]-b[1])+Math.abs(a[2]-b[2])>60;
document.querySelectorAll('section[data-mintop]').forEach(sc=>{const h=sc.firstElementChild;if(!h)return;
 const r=h.getBoundingClientRect(),top=(r.top-B)/P,min=parseFloat(sc.dataset.mintop),x=(r.left-BR.left)/P+2;
 // keep the flow unless it would put the section on another background (e.g. a dark sidebar's chevron)
 if(top<297&&top<min-0.3&&differ(at(x,top+2),at(x,min+2))){const m=parseFloat(getComputedStyle(h).marginTop)||0;h.style.marginTop=(m+(min-top)*P)+'px';}});})();"""


# ── header ─────────────────────────────────────────────────────────────────────────────────────────

def _abs_text(ctx, line: dict, align: str, text_html: str, max_w: float, key: str, bg: str | None = None,
              min_scale: float = 0.3) -> str:
    S = ctx["S"]
    top = line["y"] - S.lead1(key)
    patch = f";background:{bg};padding-right:1.5mm" if bg else ""
    if align == "center":
        cx = (line["x"] + line["x1"]) / 2
        pos = f"left:{_m(cx)};transform:translateX(-50%);text-align:center"
    elif align == "right":
        pos = f"right:{_m(210 - line['x1'])};text-align:right"
    else:
        pos = f"left:{_m(line['x'])}"
    return (f'<div class="hx k-{key}" data-fit="{max_w:.1f}" data-min="{min_scale}" style="top:{_m(top)};{pos}{patch}">'
            f'{text_html}</div>')


def _split_name(name: str, n: int) -> list[str]:
    words = name.split()
    if n <= 1 or len(words) < 2:
        return [name]
    if n == 2:
        return [" ".join(words[:-1]), words[-1]]
    return [" ".join(words[:-2]) or words[0], words[-2], words[-1]][-n:]


def _header_html(ctx, photo_uri: str) -> str:
    spec, c, rb = ctx["spec"], ctx["c"], ctx["rb"]
    out = []
    nm = spec.get("name")
    if nm and nm.get("lines"):
        name = c.get("name") or "Your Name"
        parts = _split_name(name, len(nm["lines"]))
        lines = nm["lines"][:len(parts)]
        for i, (ln, part) in enumerate(zip(lines, parts)):
            wref = ln["x1"] - ln["x"]
            grow = max(wref * 1.35, wref + 30)
            if ln.get("room_hard"):
                grow = min(grow, ln["room_hard"])      # the photo / a block on the same row stops it
            if nm["align"] == "left":
                maxw = min(205 - ln["x"], grow)
            elif nm["align"] == "right":
                maxw = min(ln["x1"] - 5, grow)
            else:
                cx = (ln["x"] + ln["x1"]) / 2
                maxw = min(grow, 2 * min(cx - 5, 205 - cx))
            # editor: the whole name is one field; split lines are separate spans of it on render
            txt = rb._f("name", name, "your name") if len(lines) == 1 else rb._e(part)
            out.append(_abs_text(ctx, ln, nm["align"], txt, maxw, ln.get("key") or "name"))
    tt = spec.get("title")
    if tt and tt.get("lines") and c.get("title"):
        ln0 = tt["lines"][0]
        if len(tt["lines"]) == 1:
            wref = ln0["x1"] - ln0["x"]
            # one line like the reference; a long title shrinks a little (≥ 75 %), covering a short decoration
            # beside it with its own background, and only then wraps
            al = tt["align"]
            cx = (ln0["x"] + ln0["x1"]) / 2
            maxw = (205 - ln0["x"]) if al == "left" else ((ln0["x1"] - 5) if al == "right" else 2 * min(cx - 5, 205 - cx))
            if ln0.get("room_hard") and al == "left":
                maxw = min(maxw, ln0["room_hard"])            # the photo / a block: fit before it
            patch = ln0.get("bg") if ln0.get("room_kind") == "rule" else None    # a thin rule may be covered
            out.append(_abs_text(ctx, ln0, al, rb._f("title", c["title"], "headline"), maxw, ln0.get("key") or "title",
                                 bg=patch, min_scale=0.75))
        else:
            S = ctx["S"]
            key = ln0.get("key") or "title"
            top = ln0["y"] - S.lead(key)
            x0 = min(l["x"] for l in tt["lines"])
            x1 = max(l["x1"] for l in tt["lines"])
            al = tt["align"]
            pos = (f"left:{_m((x0 + x1) / 2)};transform:translateX(-50%);text-align:center" if al == "center" else
                   (f"right:{_m(210 - x1)};text-align:right" if al == "right" else f"left:{_m(x0)}"))
            out.append(f'<div class="hx k-{key}" style="top:{_m(top)};{pos};white-space:normal;width:{_m((x1 - x0) * 1.06)};'
                       f'line-height:{_m(S.pitch(key))}!important">{rb._f("title", c["title"], "headline")}</div>')
    ph = spec.get("photo")
    if ph:
        x0, y0, x1, y1 = ph["box"]
        rad = "50%" if ph.get("circle") else _m(ph.get("radius") or 0)
        style = f"left:{_m(x0)};top:{_m(y0)};width:{_m(x1 - x0)};height:{_m(y1 - y0)};border-radius:{rad}"
        if photo_uri:
            out.append(f'<div class="ph hd-avatar" style="{style};background-image:url(\'{photo_uri}\');'
                       f'background-position:{_face_pos(photo_uri)}"></div>')
        else:
            col = (ctx["S"].st.get("name") or {}).get("color", "#334155")
            out.append(f'<div class="ph ph-empty hd-avatar" style="{style};background:{col}22;color:{col}">'
                       f'<span>{rb._e(rb._initials(c.get("name") or ""))}</span></div>')
    # header contact slots: same type → same place (with the reference's own icon)
    contact = c.get("contact") or {}
    used = set()
    for slot in spec.get("hcontact") or []:
        t = slot.get("type") or "website"
        val = contact.get(t) or ""
        if not val and t == "website":
            val = contact.get("linkedin") or ""
            t = "linkedin" if val else t
        if not val or t in used:
            continue
        used.add(t)
        key = slot.get("key") or "hcontact"
        out.append(_abs_text(ctx, slot, "left", rb._f(f"contact.{t}", val, t), 210 - slot["x"] - 4, key))
        ic = slot.get("icon")
        if ic:
            bx0, by0, bx1, by1 = ic["box"]
            out.append(f'<img class="hx-ic" src="{_uri(ic["file"])}" style="left:{_m(bx0)};top:{_m(by0)};'
                       f'width:{_m(bx1 - bx0)};height:{_m(by1 - by0)}">')
    ctx["hcontact_used"] = used
    return "".join(out)


_FACE_CACHE: dict = {}


def _face_pos(photo_uri: str) -> str:
    """background-position that keeps the user's face in the frame (centred, face in the upper third)."""
    import hashlib
    h = hashlib.sha1(photo_uri[-4000:].encode()).hexdigest()
    if h in _FACE_CACHE:
        return _FACE_CACHE[h]
    pos = "50% 30%"
    try:
        import cv2
        import numpy as np
        data = base64.b64decode(photo_uri.split(",", 1)[1])
        img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_GRAYSCALE)
        cas = cv2.CascadeClassifier(os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_default.xml"))
        f = cas.detectMultiScale(img, 1.1, 6, minSize=(40, 40))
        if len(f):
            x, y, w, hh = max(f, key=lambda r: r[2] * r[3])
            H, W = img.shape
            px = min(100, max(0, (x + w / 2) / W * 100))
            py = min(100, max(0, (y + hh / 2 - 0.12 * H) / H * 125))
            pos = f"{px:.0f}% {py:.0f}%"
    except Exception:
        pass
    _FACE_CACHE[h] = pos
    return pos


# ── placement of the user's sections into the reference's slots ───────────────────────────────────

def _has(c: dict, key: str) -> bool:
    if key == "contact":
        return any((c.get("contact") or {}).values())
    if key == "skills":
        return bool(c.get("skills") or c.get("additional_skills"))
    return bool(c.get(key))


def _place_sections(ctx) -> list[list]:
    """Per column: [(ref_section or template section, content key, title, is_ref_slot)]."""
    spec, c, d = ctx["spec"], ctx["c"], ctx["d"]
    hidden = set(d.get("hidden_sections") or [])
    titles = c.get("section_titles") or {}
    cols = spec["columns"]
    out = [[] for _ in cols]
    placed = set()
    has_exp_slot = any(s["key"] == "experience" for col in cols for s in col["sections"])
    has_proj_slot = any(s["key"] == "projects" for col in cols for s in col["sections"])
    for ci, col in enumerate(cols):
        for sec in col["sections"]:
            key = sec["key"]
            if key.startswith("x_"):
                out[ci].append((sec, None, None, True))          # unnamed slot: may host another section
                continue
            ckey = key
            if key == "experience" and not c.get("experience") and c.get("projects") and not has_proj_slot:
                ckey = "projects"                       # projects take the experience slot
            if key == "contact" and ctx.get("hcontact_used") and not set((c.get("contact") or {}).keys()) - ctx["hcontact_used"]:
                pass
            if ckey in placed or ckey in hidden or not _has(c, ckey):
                if ckey not in hidden and not _has(c, ckey):
                    out[ci].append((sec, None, None, True))      # vacant slot: may host another section
                continue
            title = titles.get(ckey) or (canon_title(sec["title"], ckey) if sec["title"] and ckey == key else None)
            from app.services.resume_builder import DEFAULT_TITLES
            title = title or DEFAULT_TITLES.get(ckey, ckey.title())
            out[ci].append((sec, ckey, title, True))
            placed.add(ckey)
    # user sections the reference has no slot for → the column that holds similar sections
    from app.services.resume_builder import SECTION_KEYS, DEFAULT_TITLES
    def home(key):
        want = _SIDE_KEYS if key in _SIDE_KEYS else _MAIN_KEYS
        best, bn = len(cols) - 1, -1
        for ci, col in enumerate(cols):
            n = sum(1 for s in col["sections"] if s["key"] in want)
            if n > bn:
                best, bn = ci, n
        return best
    # a user section without its own slot takes a vacant slot of the same kind (list ↔ list, items ↔ items),
    # with that slot's heading style and position — the way a designer would reuse the template
    def kind(k):
        return "items" if k in ("experience", "projects", "education") else ("para" if k == "profile" else "list")
    slot_limit = 297.0 - max(8.0, min(40.0, 297.0 - max(c_["bottom"] for c_ in cols) - 2.0))
    for key in SECTION_KEYS:
        if key in placed or key in hidden or not _has(c, key) or key == "contact":
            continue
        for ci in range(len(cols)):
            slot = next((j for j, e in enumerate(out[ci]) if e[1] is None and kind(e[0]["key"]) == kind(key)
                         and (e[0].get("top") or 0) + _est_height(ctx["S"], ci, cols[ci], e[0], key, c) <= slot_limit),
                        None)
            if slot is not None:
                out[ci][slot] = (out[ci][slot][0], key, titles.get(key) or DEFAULT_TITLES.get(key, key.title()), True)
                placed.add(key)
                break
    out = [[e for e in col_ if e[1] is not None] for col_ in out]
    # estimated filled height per column, so extra sections go where they fit
    S = ctx["S"]
    def bottom(ci):
        """Simulated bottom of a column: sections in order, a reference slot never above its reference top."""
        y = cols[ci]["sections"][0]["top"] if cols[ci]["sections"] else cols[ci]["top"]
        for sec, key, _, is_ref in out[ci]:
            if is_ref and sec.get("top"):
                y = max(y, sec["top"])
            y += _est_height(S, ci, cols[ci], sec, key, c)
        return y
    limit = 297.0 - max(8.0, min(40.0, 297.0 - max(c_["bottom"] for c_ in cols) - 2.0))
    used = [bottom(ci) for ci in range(len(cols))]
    avail = [limit] * len(cols)
    for key in SECTION_KEYS:
        if key in placed or key in hidden or not _has(c, key):
            continue
        if key == "contact" and ctx.get("hcontact_used"):
            continue                                    # contact is already in the header
        ci = home(key)
        h = _est_height(S, ci, cols[ci], _template_section(cols[ci], key), key, c)
        if used[ci] + h > avail[ci] and len(cols) > 1:
            alt = max(range(len(cols)), key=lambda j: avail[j] - used[j])
            if avail[alt] - used[alt] > avail[ci] - used[ci]:
                ci = alt
        tmpl = _template_section(cols[ci], key)
        out[ci].append((tmpl, key, titles.get(key) or DEFAULT_TITLES.get(key, key.title()), False))
        used[ci] = bottom(ci)
        placed.add(key)
    for cs in c.get("custom_sections") or []:
        if cs.get("id") in hidden:
            continue
        ci = home("certifications" if cs.get("style") in ("chips", "plain") else "profile")
        out[ci].append((_template_section(cols[ci], "custom"), cs["id"], cs.get("title") or "Section", False))
    return out


def _est_height(S, ci: int, col: dict, sec: dict, key: str, c: dict) -> float:
    """Rough height (mm) of a section in this column: heading + wrapped lines × the measured pitch."""
    K = _keys_for(S, ci)
    width = max(20.0, col["x1"] - col["text_x"])

    def lines(text: str, k: str) -> int:
        cpl = max(8, int(width / max(0.5, S.fs(k) * 0.52)))
        return max(1, -(-len(text or "") // cpl))
    deco = sec.get("deco")
    h = ((deco["box"][3] - deco["box"][1]) if deco else S.pitch(K["head"])) + 4.0
    kb, kl, kt = K["body"], K["list"], K["title"]
    if key == "profile":
        h += sum(lines(p, kb) for p in c.get("profile") or []) * S.pitch(kb)
    elif key in ("experience", "projects", "education"):
        for it in c.get(key) or []:
            h += S.pitch(kt) * 2.4
            for b in it.get("bullets") or []:
                h += lines(b, kb) * S.pitch(kb) + 0.8
            if it.get("description"):
                h += lines(it["description"], kb) * S.pitch(kb)
            h += 2.5
    elif key == "skills":
        g = sec.get("graphics") or {}
        n = len(c.get("skills") or [])
        h += n * (S.pitch(kl) * (2.0 if g.get("bars", {}).get("place") == "below" else 1.1))
        extra = c.get("additional_skills") or []
        if extra:
            h += (len(", ".join(extra)) / max(10, width / (S.fs(kl) * 0.6)) + 1) * S.pitch(kl) * 1.6
    elif key == "contact":
        h += sum(1 for v in (c.get("contact") or {}).values() if v) * S.pitch(K["contact"]) * 1.3
    else:
        items = c.get(key) or []
        for x in items:
            t = x if isinstance(x, str) else (x.get("name") or x.get("title") or "")
            h += lines(t, kl) * S.pitch(kl) + 1.0
    return h


def _template_section(col: dict, key: str) -> dict:
    """A section of this column to borrow heading decoration / styles / rhythm from."""
    secs = col["sections"]
    same = [s for s in secs if s["key"] == key]
    if same:
        return same[0]
    kind = "items" if key in ("experience", "projects", "education") else "list"
    pref = [s for s in secs if (s["key"] in ("experience", "projects", "education")) == (kind == "items")
            and not s.get("implicit")] or [s for s in secs if not s.get("implicit")]
    base = dict((pref or secs or [{}])[0])
    base = {k: v for k, v in base.items() if k not in ("graphics", "icons", "contact_labels")}
    base["graphics"] = {}
    return base


# ── sections ───────────────────────────────────────────────────────────────────────────────────────

def _tok(sec: dict, name: str, default: float | None = None):
    v = (sec.get("tokens") or {}).get(name)
    return v if isinstance(v, (int, float)) else default


def _role_x(sec: dict, role: str, col: dict) -> float:
    xs = [r["x"] for r in sec.get("roles") or [] if r["role"] == role and not r.get("lead")]
    if not xs:
        return 0.0
    xs.sort()
    v = max(-15.0, xs[len(xs) // 2] - col["text_x"])
    return 0.0 if v > 0.3 * max(20.0, col["x1"] - col["text_x"]) else v


def _keys_for(S: Styles, ci: int):
    o = 1 - ci if ci in (0, 1) else 0
    return {
        "head": S.pick(f"head{ci}", f"head{o}"),
        "title": S.pick(f"item_title{ci}", f"item_title{o}", f"sub{ci}", f"body{ci}"),
        "sub": S.pick(f"sub{ci}", f"sub{o}", f"body{ci}"),
        "meta": S.pick(f"meta{ci}", f"meta_right{ci}", f"meta{o}", f"meta_right{o}", f"body{ci}"),
        "meta_r": S.pick(f"meta_right{ci}", f"meta{ci}", f"meta_right{o}", f"body{ci}"),
        "body": S.pick(f"body{ci}", f"list{ci}", f"body{o}"),
        "list": S.pick(f"list{ci}", f"body{ci}", f"list{o}"),
        "contact": S.pick(f"contact{ci}", f"list{ci}", f"body{ci}", "hcontact"),
    }


def _margin(S: Styles, delta: float | None, prev_key: str | None, next_key: str, default_extra: float = 0.0) -> float:
    """Ink-top(prev last line) → ink-top(next first line) distance → CSS margin-top of the next block."""
    if prev_key is None:
        return 0.0
    if delta is None:
        delta = S.pitch(prev_key) + default_extra
    else:
        delta = delta * S.s
    return max(0.15, max(0.2, delta - S.pitch(prev_key) + S.lead(prev_key) - S.lead(next_key)) * S.g)


def _heading_html(ctx, ci: int, col: dict, sec: dict, key: str, title: str, margin_top: float) -> tuple[str, float]:
    """Returns (html, bottom offset → first-ink margin base). The heading box height = decoration height."""
    S, rb = ctx["S"], ctx["rb"]
    hk = sec.get("head_key") or _keys_for(S, ci)["head"]
    if hk not in S.st:
        hk = _keys_for(S, ci)["head"]
    deco = sec.get("deco")
    text = rb._f(f"section_titles.{key}", title, "section title")
    fs = S.fs(hk)
    st = S.st.get(hk) or {}
    if deco and os.path.exists(deco["file"]):
        bx0, by0, bx1, by1 = deco["box"]
        tx0, ty0, tx1, ty1 = deco["text"]
        Wc, Hc = (bx1 - bx0) * S.s, (by1 - by0) * S.s
        ppm = _png_px_per_mm(deco["file"], bx1 - bx0)
        L = max(0.0, tx0 * S.s - st.get("ls", 0) * 0.0)
        top_pad = ty0 * S.s - S.lead1(hk)
        x_off = bx0 - col["text_x"]
        if deco["kind"] == "full":
            R = max(0.6, min(4.0, (bx1 - bx0) * 0.03)) * S.s
            width = f"width:{_m(Wc - L - R)}"
        else:
            R = max(0.0, (bx1 - bx0 - tx1)) * S.s
            width = ""
        sl, sr = int(round(L / S.s * ppm)), int(round(R / S.s * ppm))
        style = (f"margin-top:{_m(margin_top)};margin-left:{_m(x_off)};border-style:solid;border-color:transparent;"
                 f"border-width:0 {_m(R)} 0 {_m(L)};border-image:url('{_uri(deco['file'])}') 0 {sr} 0 {sl} fill / 0 {_m(R)} 0 {_m(L)} stretch;"
                 f"height:{_m(Hc - max(0.0, top_pad))};padding-top:{_m(max(0.0, top_pad))};{width}")
        cls = "hd hd-full" if deco["kind"] == "full" else "hd hd-hug"
        nc = ' data-nc="1"' if deco.get("on_box") else ""
        h2 = f'<h2 class="{cls}"{nc} style="{style}"><span class="t k-{hk}" style="line-height:1">{text}</span></h2>'
        return _with_rule(S, sec, h2, ty0 * S.s, margin_top, x_off), 0.0
    # plain heading: no decoration in the reference → just the text, positioned by its ink
    hx = (sec.get("head_ink") or [col["text_x"]])[0] - col["text_x"]
    h2 = (f'<h2 class="hd" style="margin-top:{_m(margin_top)};margin-left:{_m(hx)}">'
          f'<span class="t k-{hk}" style="line-height:{_m(S.pitch(hk))}">{text}</span></h2>')
    return _with_rule(S, sec, h2, S.lead(hk), margin_top, hx), None


def _with_rule(S, sec: dict, h2: str, ink_top: float, margin_top: float, margin_left: float) -> str:
    """A rule trailing the heading text ("Contact Me ———"): drawn after the new text, either to the column
    edge (like the reference) or at the reference's fixed length — so a longer heading never runs over it."""
    r = sec.get("rule")
    if not r:
        return h2
    h2 = re.sub(r"margin-top:[^;]*;margin-left:[^;\"]*", "margin-top:0;margin-left:0", h2, count=1)
    rh = max(0.2, r["h"]) * S.s
    size = "flex:1;min-width:4mm" if r.get("to_edge") else f"width:{_m(r['len'] * S.s)};flex:none"
    rule = (f'<i class="hrule" style="display:block;{size};height:{_m(rh)};margin-left:{_m(max(1.0, r["gap"] * S.s))};'
            f'margin-top:{_m(ink_top + r["dy"] * S.s - rh / 2)};background:{r["color"]}"></i>')
    return (f'<div class="hdw" style="display:flex;align-items:flex-start;margin-top:{_m(margin_top)};'
            f'margin-left:{_m(margin_left)}">{h2}{rule}</div>')


def _section_html(ctx, ci, col, sec, key, title, is_ref, prev, first) -> tuple[str, str | None]:
    S, c, rb = ctx["S"], ctx["c"], ctx["rb"]
    K = _keys_for(S, ci)
    # gap above the heading: ink-top of the previous section's last line → heading decoration top
    hk = sec.get("head_key") or K["head"]
    if first:
        mt = 0.0
    else:
        prev_key = prev[0] if prev else None
        gap = _tok(sec, "sec_gap") if is_ref else None
        if gap is None:
            # an added section uses the design's plain section gap: the smallest measured one (bigger gaps are
            # usually shapes in between, e.g. a chevron)
            gaps = [_tok(s, "sec_gap") for s in col["sections"] if (_tok(s, "sec_gap") or 0) > 0]
            if not gaps:
                gaps = [_tok(s, "sec_gap") for c_ in ctx["spec"]["columns"] for s in c_["sections"]
                        if (_tok(s, "sec_gap") or 0) > 0]
            gap = min(gaps) if gaps else None
        if prev_key and gap is not None:
            # heading block top = deco top; previous block bottom = its last ink top − lead + pitch
            mt = max(0.2, gap * S.s - (S.pitch(prev_key) - S.lead(prev_key))) * S.g
        else:
            mt = 4.0 * S.s * S.g
    if sec.get("implicit") and is_ref and not (ctx["c"].get("section_titles") or {}).get(key):
        # the reference shows this text without a heading (e.g. a profile paragraph under the name)
        body, last = _content_html(ctx, ci, col, sec, key, _keys_for(S, ci), lambda nk: mt - S.lead(nk))
        return (f'<section class="sec sec-{key}">{body}</section>', last) if body else ("", None)
    head_html, _ = _heading_html(ctx, ci, col, sec, key, title, mt)
    has_deco = bool(sec.get("deco"))
    # first content block: deco bottom → first ink top
    hf = _tok(sec, "head_first")
    if hf is not None and hf < 0.3:
        hf = None                         # content beside/above its heading (strip layout): use the usual gap
    if hf is None:
        hfs = [_tok(s, "head_first") for s in col["sections"] if (_tok(s, "head_first") or 0) >= 0.3]
        hf = sorted(hfs)[len(hfs) // 2] if hfs else 3.0
    if not has_deco:
        # plain heading: the heading line box bottom → first ink
        hi_ = sec.get("head_ink")
        hspan = (sec.get("head_bottom", 0) - hi_[1]) if hi_ else 0.0          # heading ink height (0 if unknown)
        hfirst = lambda nk: _margin(S, (hf + hspan) if hf is not None else None, hk, nk)
    else:
        hfirst = lambda nk: max(0.15, (hf * S.s - S.lead(nk)) * (S.g if hf * S.s - S.lead(nk) > 0 else 1.0))
    body, last = _content_html(ctx, ci, col, sec, key, K, hfirst)
    if not body:
        return "", None
    mintop = f' data-mintop="{sec.get("top", 0):.2f}"' if is_ref and sec.get("top") and not ctx.get("squeeze") else ""
    return f'<section class="sec sec-{key}"{mintop}>{head_html}{body}</section>', last


def _glyph(lead: dict | None, S: Styles, key: str, x_text: float, x_glyph: float) -> str:
    if not lead or not os.path.exists(lead.get("file", "")):
        return ""
    top = S.lead(key) + lead.get("dy", 0) * S.s
    return (f'<img class="gl" src="{_uri(lead["file"])}" style="left:{_m(x_glyph - x_text)};top:{_m(top)};'
            f'width:{_m(lead["w"] * S.s)};height:{_m(lead["h"] * S.s)}">')


def _list_block(ctx, K, sec, col, path_items, key_style, hfirst, lead=None, x_text=0.0) -> tuple[str, str]:
    """Simple list: one block per item, the reference's bullet/icon on the left."""
    S, rb = ctx["S"], ctx["rb"]
    out = []
    ni = _tok(sec, "new_item")
    prev = None
    lead = lead if lead is not None else sec.get("lead")
    x_glyph = x_text - (lead["dx"] if lead else 0)
    for i, (path, val) in enumerate(path_items):
        mt = hfirst(key_style) if prev is None else _margin(S, ni, prev, key_style, 0.6)
        g = _glyph(lead, S, key_style, x_text, x_glyph) if lead else ""
        out.append(f'<div class="blk k-{key_style}"{rb._it(path)} style="margin-top:{_m(mt)};margin-left:{_m(x_text)}">'
                   f'{g}{rb._f(path, val)}</div>')
        prev = key_style
    return "".join(out), key_style


def _content_html(ctx, ci, col, sec, key, K, hfirst) -> tuple[str, str | None]:
    S, c, rb = ctx["S"], ctx["c"], ctx["rb"]
    g = sec.get("graphics") or {}
    lead = sec.get("lead")
    if key == "profile":
        k = K["body"]
        x = _role_x(sec, "body", col)
        paras = c.get("profile") or []
        out, prev = [], None
        for i, p in enumerate(paras):
            mt = hfirst(k) if prev is None else _margin(S, _tok(sec, "new_item"), prev, k, 1.2)
            out.append(f'<p class="blk k-{k}"{rb._it(f"profile.{i}")} style="margin-top:{_m(mt)};margin-left:{_m(x)}">'
                       f'{rb._f(f"profile.{i}", p, "profile paragraph")}</p>')
            prev = k
        return "".join(out), prev
    if key in ("experience", "projects", "education"):
        return _items_html(ctx, ci, col, sec, key, K, hfirst)
    if key == "contact":
        return _contact_html(ctx, ci, col, sec, K, hfirst)
    if key == "skills":
        return _skills_html(ctx, ci, col, sec, K, hfirst)
    if key == "languages":
        items = c.get("languages") or []
        if (g.get("dots") or g.get("bars")) and items:
            return _rated_html(ctx, col, sec, K, hfirst, [(f"languages.{i}", x["name"], x.get("level", 4) * 20)
                                                          for i, x in enumerate(items)], "languages")
        word = {5: "Native", 4: "Fluent", 3: "Intermediate", 2: "Basic", 1: "Beginner"}
        return _list_block(ctx, K, sec, col, [(f"languages.{i}.name", x["name"]) for i, x in enumerate(items)],
                           K["list"], hfirst, x_text=_role_x(sec, "list", col) if lead else _role_x(sec, "list", col))
    if key == "competencies":
        items = [(f"competencies.{i}.title", x["title"]) for i, x in enumerate(c.get("competencies") or [])]
        return _list_block(ctx, K, sec, col, items, K["list"], hfirst, x_text=_text_x(sec, col, "list"))
    if key in ("highlights", "achievements", "certifications", "references"):
        items = [(f"{key}.{i}", x) for i, x in enumerate(c.get(key) or [])]
        k = K["list"] if any(r["role"] == "list" for r in sec.get("roles") or []) else K["body"]
        return _list_block(ctx, K, sec, col, items, k, hfirst, x_text=_text_x(sec, col, None))
    if key == "interests":
        items = [(f"interests.{i}", x) for i, x in enumerate(c.get("interests") or [])]
        if g.get("chips"):
            return _chips_html(ctx, sec, col, K["list"], items, hfirst)
        return _list_block(ctx, K, sec, col, items, K["list"], hfirst, x_text=_text_x(sec, col, None))
    if key.startswith("custom_"):
        cs = next((x for x in c.get("custom_sections") or [] if x.get("id") == key), None)
        if not cs:
            return "", None
        items = [(f"custom_sections.{key}.items.{i}", x) for i, x in enumerate(cs.get("items") or [])]
        return _list_block(ctx, K, sec, col, items, K["body"], hfirst, x_text=_text_x(sec, col, None))
    return "", None


def _text_x(sec, col, role) -> float:
    rs = [r for r in sec.get("roles") or [] if (role is None or r["role"] == role)]
    if not rs:
        return 0.0
    xs = sorted(r["x"] for r in rs)
    v = max(-15.0, xs[len(xs) // 2] - col["text_x"])
    # an offset this large is a different layout (e.g. a contact strip beside its heading), not an indent
    return 0.0 if v > 0.3 * max(20.0, col["x1"] - col["text_x"]) else v


def _items_html(ctx, ci, col, sec, key, K, hfirst) -> tuple[str, str | None]:
    S, c, rb = ctx["S"], ctx["c"], ctx["rb"]
    roles = {r["role"] for r in sec.get("roles") or []}
    has_meta_r = "meta_right" in roles or (not roles and any(
        r["role"] == "meta_right" for s in col["sections"] for r in s.get("roles") or []))
    kt, ks, km, kmr, kb = K["title"], K["sub"], K["meta"], K["meta_r"], K["body"]
    xt, xs_, xm = _role_x(sec, "item_title", col), _role_x(sec, "sub", col), _role_x(sec, "meta", col)
    lead = sec.get("lead")
    own = sorted(r["x"] for r in sec.get("roles") or [] if r.get("lead") and r["role"] == "body")
    if lead and own:
        xb_text = own[len(own) // 2] - col["text_x"]                 # this section's own bullet indent
    elif lead:
        xb_text = (col.get("bullet_text_x") or col["text_x"]) - col["text_x"]
    else:
        xb_text = _role_x(sec, "body", col)
    if abs(xb_text) > 0.3 * max(20.0, col["x1"] - col["text_x"]):
        xb_text = 0.0                                                # implausible indent: not a bullet column
    xb_glyph = xb_text - (lead["dx"] if lead else 0)
    tl = (sec.get("graphics") or {}).get("timeline")
    items = c.get(key) or []
    out, prev = [], None
    for i, it in enumerate(items):
        p = f"{key}.{i}"
        if key == "experience":
            t, s_, per, bullets, desc = it.get("role", ""), it.get("company", ""), it.get("period", ""), it.get("bullets") or [], ""
            tf, sf, pf = "role", "company", "period"
            if it.get("location"):
                s_ = f"{s_}, {it['location']}" if s_ else it["location"]
        elif key == "projects":
            t, s_, per, bullets, desc = it.get("name", ""), it.get("tech", ""), it.get("period", ""), it.get("bullets") or [], it.get("description", "")
            tf, sf, pf = "name", "tech", "period"
        else:
            t, s_, per, bullets, desc = it.get("degree", ""), it.get("institution", ""), it.get("period", ""), [], ""
            tf, sf, pf = "degree", "institution", "period"
            det = (it.get("details") or "").strip()
            if det and per:                      # an older editor save glued the details into the period
                per = " · ".join(x for x in dict.fromkeys(per.split(" · ")) if x.strip() != det)
        # date (+ education details) as separate editable fields on one line, so editor saves stay separate
        parts = [rb._f(f"{p}.{pf}", per)] if per else []
        if key == "education" and it.get("details"):
            parts.append(rb._f(f"{p}.details", it["details"].strip()))
        per_html = " · ".join(parts)
        per = per or (it.get("details") if key == "education" else "")
        blocks = []
        mt = hfirst(kt) if prev is None else _margin(S, _tok(sec, "item_gap"), prev, kt, 2.2)
        node = ""
        if tl and tl.get("node") and os.path.exists(tl["node"]["file"]):
            nd = tl["node"]
            ny = S.lead(kt) + (nd.get("dy_mm") or 0) * S.s - nd["h_mm"] * S.s / 2
            node = (f'<img class="gl" src="{_uri(nd["file"])}" style="left:{_m(nd["cx_mm"] - nd["w_mm"] / 2 - col["text_x"] - xt)};'
                    f'top:{_m(ny)};width:{_m(nd["w_mm"] * S.s)};height:{_m(nd["h_mm"] * S.s)};z-index:2">')
        if has_meta_r and per:
            blocks.append(f'<div class="row" style="margin-top:{_m(mt)};margin-left:{_m(xt)}">{node}'
                          f'<span class="k-{kt}">{rb._f(f"{p}.{tf}", t)}</span>'
                          f'<span class="r k-{kmr}">{per_html}</span></div>')
            per_done = True
        else:
            blocks.append(f'<div class="blk k-{kt}" style="margin-top:{_m(mt)};margin-left:{_m(xt)}">{node}{rb._f(f"{p}.{tf}", t)}</div>')
            per_done = False
        last = kt
        if s_:
            blocks.append(f'<div class="blk k-{ks}" style="margin-top:{_m(_margin(S, _tok(sec, "title_sub"), last, ks))};'
                          f'margin-left:{_m(xs_)}">{rb._f(f"{p}.{sf}", s_)}</div>')
            last = ks
        if per and not per_done:
            d_ = _tok(sec, "sub_meta") if last == ks else _tok(sec, "title_sub")
            blocks.append(f'<div class="blk k-{km}" style="margin-top:{_m(_margin(S, d_, last, km))};margin-left:{_m(xm)}">'
                          f'{per_html}</div>')
            last = km
        if desc:
            fld = "description" if key == "projects" else "details"
            blocks.append(f'<div class="blk k-{kb}" style="margin-top:{_m(_margin(S, _tok(sec, "head_body"), last, kb))};'
                          f'margin-left:{_m(_role_x(sec, "body", col))}">{rb._f(f"{p}.{fld}", desc)}</div>')
            last = kb
        for j, b in enumerate(bullets):
            d_ = _tok(sec, "head_body") if j == 0 and last != kb else _tok(sec, "new_item")
            g = _glyph(lead, S, kb, xb_text, xb_glyph)
            blocks.append(f'<div class="blk k-{kb}"{rb._it(f"{p}.bullets.{j}")} style="margin-top:{_m(_margin(S, d_, last, kb))};'
                          f'margin-left:{_m(xb_text)}">{g}{rb._f(f"{p}.bullets.{j}", b)}</div>')
            last = kb
        out.append(f'<div class="item"{rb._it(p)}>{"".join(blocks)}</div>')
        prev = last
    html = "".join(out)
    if tl and html:
        lx = tl["x_mm"] - col["text_x"]
        first_off = S.lead(kt)
        html = (f'<div style="position:relative"><i class="tl" style="left:{_m(lx - tl["w_mm"] / 2)};width:{_m(max(0.2, tl["w_mm"]))};'
                f'top:{_m(hfirst(kt) + first_off)};bottom:{_m(1.0)};background:{tl["color"]}"></i>{html}</div>')
    return html, prev


def _contact_html(ctx, ci, col, sec, K, hfirst) -> tuple[str, str | None]:
    S, c, rb = ctx["S"], ctx["c"], ctx["rb"]
    contact = c.get("contact") or {}
    order = ["phone", "email", "location", "linkedin", "website"]
    canon = ["phone", "email", "website", "location", "linkedin"]
    icons: dict = {}
    last = -1
    for ic in sec.get("icons") or []:
        t = ic.get("ctype") or ""
        if t and t not in icons:
            icons[t] = ic
            last = canon.index(t) if t in canon else last
            continue
        cand = [x for x in canon[last + 1:] if x not in icons] or [x for x in canon if x not in icons]
        if cand:
            icons[cand[0]] = ic
            last = canon.index(cand[0])
    if "website" not in icons and "linkedin" in icons:
        icons["website"] = icons["linkedin"]
    if "linkedin" not in icons and "website" in icons:
        icons["linkedin"] = icons["website"]
    k = K["contact"]
    labels = sec.get("contact_labels")
    out, prev = [], None
    x_text = _text_x(sec, col, "contact")
    for t in order:
        v = contact.get(t)
        if not v or t in (ctx.get("hcontact_used") or set()):
            continue
        ic = icons.get(t)
        mt = hfirst(k) if prev is None else _margin(S, _tok(sec, "new_item"), prev, k, 0.8)
        if labels:
            lk = labels.get("key") or k
            lab = {"phone": "Phone", "email": "Email", "location": "Address", "linkedin": "LinkedIn", "website": "Website"}[t]
            out.append(f'<div class="blk k-{lk}" style="margin-top:{_m(mt)};margin-left:{_m(x_text)}">{lab}</div>')
            prev = lk
            mt = _margin(S, None, prev, k)
        g = ""
        if ic and os.path.exists(ic["file"]):
            g = (f'<img class="gl" src="{_uri(ic["file"])}" style="left:{_m(-ic["dx"] * S.s)};top:{_m(S.lead(k) + ic["dy"] * S.s)};'
                 f'width:{_m(ic["w"] * S.s)};height:{_m(ic["h"] * S.s)}">')
        out.append(f'<div class="blk k-{k}" style="margin-top:{_m(mt)};margin-left:{_m(x_text)}">{g}{rb._f(f"contact.{t}", v, t)}</div>')
        prev = k
    return "".join(out), prev


def _skills_html(ctx, ci, col, sec, K, hfirst) -> tuple[str, str | None]:
    S, c, rb = ctx["S"], ctx["c"], ctx["rb"]
    g = sec.get("graphics") or {}
    skills = c.get("skills") or []
    extra = c.get("additional_skills") or []
    k = K["list"]
    html, last = "", None
    if (g.get("bars") or g.get("dots")) and skills:
        html, last = _rated_html(ctx, col, sec, K, hfirst, [(f"skills.{i}", s["name"], s.get("level", 80))
                                                           for i, s in enumerate(skills)], "skills")
        rest = [(f"additional_skills.{i}", x) for i, x in enumerate(extra)]
    else:
        rest = [(f"skills.{i}.name", s["name"]) for i, s in enumerate(skills)] + \
               [(f"additional_skills.{i}", x) for i, x in enumerate(extra)]
    sh = sec.get("subhead")
    if rest and html and sh and sh.get("key") in S.st:
        shk = sh["key"]
        from app.services.resume_builder import _e
        title = (ctx["c"].get("section_titles") or {}).get("additional_skills") or "Other Technologies"
        html += (f'<div class="blk k-{shk}" style="margin-top:{_m(_margin(S, None, last, shk, 2.6))};'
                 f'margin-left:{_m(sh["x"] - col["text_x"])}">{_e(title)}</div>')
        last = shk
        after = sh.get("after")
    else:
        after = None
    if rest:
        first = (lambda nk: hfirst(nk)) if not html else (lambda nk: _margin(S, after, last, nk, 2.5))
        if g.get("chips"):
            h2, last = _chips_html(ctx, sec, col, k, rest, first)
        else:
            h2, last = _list_block(ctx, K, sec, col, rest, k, first, x_text=_text_x(sec, col, "list"))
        html += h2
    return html, last


def _rated_html(ctx, col, sec, K, hfirst, items, base) -> tuple[str, str]:
    """Skills/languages with the reference's bars or dots."""
    S, rb = ctx["S"], ctx["rb"]
    g = sec.get("graphics") or {}
    k = K["list"]
    x_text = _text_x(sec, col, "list")
    row_d = _tok(sec, "new_item") or _tok(sec, "wrap")
    if g.get("bars") and g["bars"].get("place") != "below":
        return _bar_grid_html(ctx, col, sec, k, hfirst, items, row_d), k
    out, prev = [], None
    for i, (path, name, level) in enumerate(items):
        mt = hfirst(k) if prev is None else _margin(S, row_d, prev, k, 2.0)
        name_f = rb._f(f"{path}.name", name)
        if g.get("bars"):
            b = g["bars"]
            lvl = max(5, min(100, level))
            radius = _m(b.get("radius_mm", 0) * S.s)
            track = b.get("track") or "transparent"
            bar = (f'<span class="bar" style="display:block;height:{_m(b["h_mm"] * S.s)};width:{_m(b["w_mm"] * S.s)};'
                   f'background:{track};border-radius:{radius};')
            if b.get("place") == "below":
                gap = b.get("gap_mm", 1.0) * S.s - (S.pitch(k) - S.lead(k) - S.ink_h(k))
                bx = b.get("x0_mm", col["text_x"]) - col["text_x"] - x_text
                out.append(f'<div class="blk"{rb._it(path)} style="margin-top:{_m(mt)};margin-left:{_m(x_text)}">'
                           f'<div class="k-{k}">{name_f}</div>{bar}margin-top:{_m(gap)};margin-left:{_m(bx)}">'
                           f'<i style="width:{lvl}%;background:{b["fill"]};border-radius:{radius}"></i></span></div>')
                prev = None
                # the next row starts after the bar: express the row distance relative to the label
                out[-1] = out[-1]
                prev = k
                ctx["_bar_extra"] = True
            else:
                bx = b.get("x0_mm", col["x1"] - b["w_mm"]) - col["text_x"]
                out.append(f'<div class="blk k-{k}"{rb._it(path)} style="margin-top:{_m(mt)};margin-left:{_m(x_text)}">{name_f}'
                           f'{bar}position:absolute;left:{_m(bx - x_text)};top:{_m(S.lead(k) + S.ink_h(k) / 2 - b["h_mm"] * S.s / 2)}">'
                           f'<i style="width:{lvl}%;background:{b["fill"]};border-radius:{radius}"></i></span></div>')
                prev = k
        else:
            dd = g["dots"]
            n = int(dd.get("n") or 5)
            on = max(0, min(n, round(level / 100 * n)))
            dots = "".join(f'<i style="width:{_m(dd["d_mm"] * S.s)};height:{_m(dd["d_mm"] * S.s)};'
                           f'margin-right:{_m((dd["pitch_mm"] - dd["d_mm"]) * S.s)};background:{dd["on"] if j < on else (dd.get("off") or "transparent")};'
                           f'{"" if j < on or dd.get("off") else "box-shadow:inset 0 0 0 0.25mm " + dd["on"]}"></i>' for j in range(n))
            dx = dd.get("x0_mm", col["x1"] - n * dd["pitch_mm"]) - col["text_x"] - x_text
            out.append(f'<div class="blk k-{k}"{rb._it(path)} style="margin-top:{_m(mt)};margin-left:{_m(x_text)}">{name_f}'
                       f'<span class="dots" style="position:absolute;left:{_m(dx)};top:{_m(S.lead(k) + S.ink_h(k) / 2 - dd["d_mm"] * S.s / 2)}">{dots}</span></div>')
            prev = k
    if g.get("bars") and g["bars"].get("place") == "below":
        # rows: label + bar; the measured label→label distance already contains the bar, so subtract its height
        return _fix_bar_rows("".join(out), S, k, row_d, g["bars"]), k
    return "".join(out), k


def _bar_grid_html(ctx, col, sec, k, hfirst, items, row_d) -> str:
    """Bars to the right of their labels, in the reference's number of columns (e.g. a 2-column skill grid):
    each cell = label + bar at the measured offset; rows at the measured row distance."""
    S, rb = ctx["S"], ctx["rb"]
    b = sec["graphics"]["bars"]
    ncol = max(1, int(b.get("columns") or 1))
    colx = b.get("col_x_mm") or [col["text_x"] + _text_x(sec, col, "list")]
    width = col["x1"] - colx[0]
    cell_w = (colx[1] - colx[0]) if ncol > 1 and len(colx) > 1 else width
    dx = b.get("label_dx_mm") or max(10.0, cell_w - b["w_mm"] - 1)
    bw = min(b["w_mm"], max(6.0, cell_w - dx - 2))
    pitch = S.pitch(k)
    gap = max(0.0, (row_d * S.s if row_d else pitch * 1.4) - pitch)
    radius = _m(b.get("radius_mm", 0) * S.s)
    track = b.get("track") or "transparent"
    top = S.lead(k) + S.ink_h(k) / 2 - b["h_mm"] * S.s / 2
    cells = []
    for path, name, level in items:
        lvl = max(5, min(100, level))
        cells.append(f'<div class="k-{k}"{rb._it(path)} style="position:relative;white-space:nowrap">'
                     f'<span style="display:inline-block;max-width:{_m(max(5.0, dx - 1.5))};overflow:hidden;'
                     f'text-overflow:ellipsis;vertical-align:top">{rb._f(f"{path}.name", name)}</span>'
                     f'<span class="bar" style="position:absolute;left:{_m(dx)};top:{_m(top)};width:{_m(bw)};'
                     f'height:{_m(b["h_mm"] * S.s)};background:{track};border-radius:{radius}">'
                     f'<i style="width:{lvl}%;background:{b["fill"]};border-radius:{radius}"></i></span></div>')
    return (f'<div class="bargrid" style="display:grid;grid-template-columns:repeat({ncol},{_m(cell_w)});row-gap:{_m(gap)};'
            f'margin-top:{_m(hfirst(k))};margin-left:{_m(colx[0] - col["text_x"])}">{"".join(cells)}</div>')


def _fix_bar_rows(html: str, S, k, row_d, b) -> str:
    """Below-label bars sit in the flow between labels: the measured label→label distance includes them,
    so the margin above each following row is reduced by the bar block (gap + height)."""
    if row_d is None:
        return html
    parts = html.split('<div class="blk"')
    if len(parts) <= 2:
        return html
    gap = b.get("gap_mm", 1.0) * S.s - (S.pitch(k) - S.lead(k) - S.ink_h(k))
    bar_block = gap + b["h_mm"] * S.s
    out = [parts[0], parts[1]]
    for p in parts[2:]:
        m = re.search(r"margin-top:(-?[\d.]+)mm", p)
        if m:
            v = max(0.4, float(m.group(1)) - bar_block)
            p = p[:m.start()] + f"margin-top:{v:.2f}mm" + p[m.end():]
        out.append(p)
    return '<div class="blk"'.join(out)


def _chips_html(ctx, sec, col, k, items, hfirst) -> tuple[str, str]:
    S, rb = ctx["S"], ctx["rb"]
    ch = (sec.get("graphics") or {}).get("chips") or {}
    h = ch.get("h_mm", 5.0) * S.s
    fs = S.fs(k)
    v = S.st.get(k) or {}
    # chip text vertically: centre the ink inside the chip
    pad_top = (h - v.get("ink_asc", 0.72) * fs) / 2 - ((fs - (v.get("asc", .92) + v.get("desc", .24)) * fs) / 2 +
                                                       (v.get("asc", .92) - v.get("ink_asc", .72)) * fs)
    chips = "".join(
        f'<span class="chip k-{k}" data-nc{rb._it(path)} style="height:{_m(h)};padding:0 {_m(ch.get("pad_x_mm", 2) * S.s)};'
        f'border:{_m(max(0.15, ch.get("border_w_mm", 0.2)))} solid {ch.get("border", "#999")};background:{ch.get("fill", "transparent")};'
        f'border-radius:{_m(ch.get("radius_mm", 2) * S.s)};margin:0 {_m(ch.get("gap_x_mm", 1.5) * S.s)} {_m(ch.get("gap_y_mm", 1.5) * S.s)} 0;'
        f'line-height:1;padding-top:{_m(max(0, pad_top))};align-items:flex-start;color:{ch.get("text_color") or v.get("color")}">'
        f'{rb._f(path, val)}</span>' for path, val in items)
    mt = hfirst(k) - S.lead(k) + S.lead(k)
    return f'<div class="chips" style="margin-top:{_m(mt - (h - v.get("ink_asc", 0.72) * fs) / 2)};margin-left:{_m(_text_x(sec, col, None))}">{chips}</div>', k
