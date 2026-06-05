"""
ppt_tool.py — Aesthetic High-Density PPT Engine
===============================================
Combines the Gamma-like vibrant aesthetics (colors, rounded corners)
with the SIH Hackathon extreme density (large visuals, dense bullets).
"""
from __future__ import annotations
import json, re, time
from pathlib import Path
from typing import Optional, Generator

try:
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE
except ImportError:
    import subprocess, sys
    subprocess.run([sys.executable, "-m", "pip", "install", "python-pptx", "-q"], check=False)
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE

try:
    from groq import Groq
    from app.core.config import settings
    _GROQ = Groq(api_key=settings.GROQ_API_KEY)
except Exception:
    _GROQ = None

_LAST_DECK_PATH: Optional[str] = None
_LAST_PLAN:      Optional[dict] = None

# 16:9 Standard
W = Inches(13.33)
H = Inches(7.5)

# Vibrant Palettes
PERSONALITIES = {
    "ocean_pro": {"name": "Ocean Pro", "desc": "Deep blue + cyan. Professional tech.", 
                  "bg": "0A1128", "card": "16203B", "text": "FFFFFF", "ac1": "00E5FF", "ac2": "3A86FF", "viz": "0D1B2A"},
    "neon_dark": {"name": "Neon Dark", "desc": "Black + vivid purple/pink.", 
                  "bg": "09090B", "card": "18181B", "text": "FAFAFA", "ac1": "D946EF", "ac2": "8B5CF6", "viz": "111113"},
    "emerald":   {"name": "Emerald", "desc": "Forest green + mint. Sustainability.", 
                  "bg": "064E3B", "card": "065F46", "text": "ECFDF5", "ac1": "34D399", "ac2": "10B981", "viz": "022C22"},
    "clean_light":{"name": "Clean Light", "desc": "White + corporate blue. Classic.", 
                  "bg": "F8FAFC", "card": "FFFFFF", "text": "0F172A", "ac1": "2563EB", "ac2": "3B82F6", "viz": "E2E8F0"},
    "synthwave": {"name": "Synthwave", "desc": "Neon pink + purple. Retro cyber.",
                  "bg": "120424", "card": "24083B", "text": "FDE0FF", "ac1": "FF2E93", "ac2": "00E5FF", "viz": "19052E"},
    "aurora":    {"name": "Aurora", "desc": "Deep teal + bright green. Nature tech.",
                  "bg": "021C1E", "card": "004445", "text": "E0F2F1", "ac1": "2C7873", "ac2": "6FB98F", "viz": "011214"},
    "hacker_terminal": {"name": "Hacker Terminal", "desc": "Pitch black + lime green. Matrix style.",
                  "bg": "000000", "card": "0A0A0A", "text": "39FF14", "ac1": "39FF14", "ac2": "008F11", "viz": "050505"}
}

def _c(h: str) -> RGBColor:
    h = h.lstrip("#")
    return RGBColor(int(h[:2],16), int(h[2:4],16), int(h[4:],16))

def _bg(slide, col: str):
    b = slide.background; b.fill.solid()
    b.fill.fore_color.rgb = _c(col)

def _shape(slide, shp_type, l, t, w, h, fill=None, line=None, lw=1.0):
    sh = slide.shapes.add_shape(shp_type, l, t, w, h)
    if fill:
        sh.fill.solid(); sh.fill.fore_color.rgb = _c(fill)
    else:
        sh.fill.background()
    if line:
        sh.line.color.rgb = _c(line); sh.line.width = Pt(lw)
    else:
        sh.line.fill.background()
    return sh

def _tb(slide, text: str, l, t, w, h, font="Calibri", sz=11, bold=False, italic=False, col="000000", align=PP_ALIGN.LEFT):
    if not text: return
    tb = slide.shapes.add_textbox(l, t, w, h)
    tb.word_wrap = True
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.alignment = align
    r = p.add_run()
    r.text = str(text)
    r.font.name = font; r.font.size = Pt(sz)
    r.font.bold = bold; r.font.italic = italic
    r.font.color.rgb = _c(col)


# ─────────────────────────────────────────────────────────────────────────────
#  GROQ PLANNER PROMPT
# ─────────────────────────────────────────────────────────────────────────────
_SYS = """\
You are an elite aesthetic presentation generator.
You create hyper-dense, visually stunning presentations with dedicated space for architecture diagrams.
Output ONLY valid JSON — no markdown fences, no explanation."""

_USR = """\
Create a highly technical, content-dense, aesthetic presentation for:
TOPIC: {prompt}

RULES:
- Create 8 to 12 slides depending on topic complexity.
- First slide MUST use "aesthetic_title".
- Use a diverse mix of: "aesthetic_split", "aesthetic_grid", "aesthetic_flow", "aesthetic_timeline", "aesthetic_comparison", "aesthetic_metrics".
- TEXT MUST BE EXTREMELY DENSE. Every bullet array must have 3-4 items, and each text property MUST be 25-30 words of deep technical/strategic detail. No short bullets. We want to fill the slides with rich text.
- Every layout requires a "visual_suggestion" detailing exactly what flowchart/diagram goes in the massive placeholder. If the user provided images via [ATTACHED_FILE: <path>], you MUST use the exact path in an "image_path" field instead of "visual_suggestion".
- Output ONLY valid JSON.

JSON SCHEMA:
{{
  "presentation_title": "...",
  "personality": "ocean_pro",
  "slides": [
    {{
      "slide_number": 1,
      "layout": "aesthetic_title",
      "title": "Project/Topic Name",
      "subtitle": "A robust 3-sentence technical abstract explaining the core innovation, stack, and impact."
    }},
    {{
      "slide_number": 2,
      "layout": "aesthetic_split",
      "title": "Problem Statement",
      "bullets": [
        {{"bold": "Key Point 1", "text": "25-30 words of extremely detailed context ensuring vertical space is filled completely."}}
      ],
      "visual_suggestion": "[ Diagram: User pain-point flowchart or current system architecture ]",
      "image_path": "c:/path/to/image.png"
    }},
    {{
      "slide_number": 3,
      "layout": "aesthetic_grid",
      "title": "Technical Approach",
      "cards": [
        {{
          "header": "Data Ingestion",
          "bullets": ["20 words detailing the pipeline", "20 words on scaling", "20 words on security"]
        }}
      ]
    }},
    {{
      "slide_number": 4,
      "layout": "aesthetic_flow",
      "title": "System Architecture",
      "description": "A dense 50-word paragraph explaining the exact end-to-end data flow.",
      "visual_suggestion": "[ Massive Flowchart: User -> API -> DB -> LLM ]"
    }},
    {{
      "slide_number": 5,
      "layout": "aesthetic_timeline",
      "title": "Deployment Roadmap",
      "nodes": [
        {{"header": "Phase 1: Alpha", "text": "30 words detailing the foundational steps and rollout."}}
      ]
    }},
    {{
      "slide_number": 6,
      "layout": "aesthetic_comparison",
      "title": "Old vs New Architecture",
      "left_header": "Legacy System",
      "right_header": "Modern Stack",
      "left_bullets": ["25 words..."],
      "right_bullets": ["25 words..."]
    }},
    {{
      "slide_number": 7,
      "layout": "aesthetic_metrics",
      "title": "Performance Impact",
      "metrics": [
        {{"value": "99.9%", "label": "Uptime SLAs guaranteed under high load..."}}
      ],
      "visual_suggestion": "[ Diagram: Load testing graphs ]"
    }}
  ]
}}"""

def _groq_call(sys_p: str, usr_p: str, tokens: int = 4000) -> str:
    if _GROQ is None: raise RuntimeError("GROQ_API_KEY not configured")
    # Free tier TPM limit is 6000. Total requested = prompt_tokens + max_tokens.
    # By setting max_tokens to 4500, we ensure total stays below 6000.
    safe_tokens = min(tokens, 4500)
    try:
        r = _GROQ.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role":"system","content":sys_p}, {"role":"user","content":usr_p}],
            max_tokens=safe_tokens, temperature=0.7, response_format={"type":"json_object"},
        )
        return r.choices[0].message.content or ""
    except Exception as e:
        err_str = str(e).lower()
        if "429" in err_str or "413" in err_str or "rate limit" in err_str or "rate_limit" in err_str or "too large" in err_str:
            # Fallback to a smaller model with a higher rate limit
            r = _GROQ.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role":"system","content":sys_p}, {"role":"user","content":usr_p}],
                max_tokens=safe_tokens, temperature=0.7, response_format={"type":"json_object"},
            )
            return r.choices[0].message.content or ""
        raise e

def _parse(raw: str) -> dict:
    raw = re.sub(r"```(?:json)?|```", "", raw).strip()
    return json.loads(raw[raw.find("{"):raw.rfind("}")+1])


# ─────────────────────────────────────────────────────────────────────────────
#  BUILDER
# ─────────────────────────────────────────────────────────────────────────────
class PresentationBuilder:
    def __init__(self, plan: dict, out: str):
        self.plan = plan
        self.out  = out
        self.prs = Presentation()
        self.prs.slide_width  = W
        self.prs.slide_height = H
        
        pk = plan.get("personality", "ocean_pro")
        self.P = PERSONALITIES.get(pk, PERSONALITIES["ocean_pro"])

    def _blank(self):
        s = self.prs.slides.add_slide(self.prs.slide_layouts[6])
        _bg(s, self.P["bg"])
        return s

    def _card(self, slide, l, t, w, h):
        # Drop shadow effect
        _shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, l+Inches(0.06), t+Inches(0.06), w, h, fill=self.P["viz"], line=self.P["ac1"], lw=0.5)
        # Main card
        _shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, l, t, w, h, fill=self.P["card"])

    def _footer(self, slide, cur, total):
        if total <= 0: return
        pw = (W / total) * cur
        # Progress bar
        _shape(slide, MSO_SHAPE.RECTANGLE, 0, H-Inches(0.05), W, Inches(0.05), fill=self.P["viz"])
        _shape(slide, MSO_SHAPE.RECTANGLE, 0, H-Inches(0.05), pw, Inches(0.05), fill=self.P["ac1"])
        # Slide number
        _tb(slide, f"{cur:02d} // {total:02d}", W-Inches(1.0), H-Inches(0.3), Inches(0.8), Inches(0.2), sz=9, bold=True, col=self.P["ac1"], align=PP_ALIGN.RIGHT)

    def _header(self, slide, title: str):
        # Aesthetic header with rounded colored accent
        self._card(slide, Inches(0.5), Inches(0.4), W-Inches(1.0), Inches(0.8))
        _shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(0.4), Inches(0.2), Inches(0.8), fill=self.P["ac1"])
        _tb(slide, title.upper(), Inches(0.9), Inches(0.5), W-Inches(2.0), Inches(0.6), sz=24, bold=True, col=self.P["text"], font="Inter")

    def _viz(self, slide, l, t, w, h, text, image_path=None):
        if image_path:
            import re
            m = re.search(r'\[ATTACHED_FILE:\s*(.+?)\]', str(image_path))
            clean_path = m.group(1) if m else str(image_path)
            
            if Path(clean_path).exists():
                try:
                    slide.shapes.add_picture(clean_path, l, t, w, h)
                    return
                except Exception as e:
                    print(f"Error adding picture {clean_path}: {e}")
                
        # Massive rounded visual placeholder box with subtle depth
        _shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, l+Inches(0.04), t+Inches(0.04), w, h, fill=self.P["bg"], line=self.P["ac2"], lw=1.5)
        _shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, l, t, w, h, fill=self.P["viz"], line=self.P["ac1"], lw=1.0)
        _tb(slide, text, l+Inches(0.2), t+h/2-Inches(0.5), w-Inches(0.4), Inches(1.0), sz=14, italic=True, col=self.P["ac1"], align=PP_ALIGN.CENTER)

    def build_with_progress(self) -> Generator[str,None,None]:
        slides = self.plan.get("slides",[])
        total = len(slides)
        for i, sd in enumerate(slides):
            lay = sd.get("layout","aesthetic_split")
            yield f"🔨 Slide {i+1} — {sd.get('title','')} ({lay})"
            fn = getattr(self, f"_lay_{lay}", self._lay_aesthetic_split)
            try:
                fn(sd, i+1, total)
            except Exception as e:
                # Provide a fallback if signature doesn't match or errors out
                yield f"⚠️ Error in {lay}: {str(e)} — generating fallback split"
                self._lay_aesthetic_split(sd, i+1, total)
        yield "💾 Saving…"
        self.prs.save(self.out)

    # ── LAYOUT 1: TITLE ───────────────────────────────────────────────────────
    def _lay_aesthetic_title(self, d: dict, cur: int, total: int):
        slide = self._blank()
        self._footer(slide, cur, total)
        
        # Center card
        cw, ch = Inches(10.0), Inches(4.5)
        cx, cy = (W-cw)/2, (H-ch)/2
        self._card(slide, cx, cy, cw, ch)
        
        # Accents
        _shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, cx, cy, cw, Inches(0.15), fill=self.P["ac1"])
        
        # Title given more vertical space to wrap safely without overlapping
        _tb(slide, d.get("title", "Title"), cx+Inches(0.5), cy+Inches(0.5), cw-Inches(1.0), Inches(2.0), sz=44, bold=True, col=self.P["text"], align=PP_ALIGN.CENTER)
        
        # Subtitle shifted down
        _tb(slide, d.get("subtitle", ""), cx+Inches(1.0), cy+Inches(2.7), cw-Inches(2.0), Inches(1.5), sz=14, col=self.P["text"], align=PP_ALIGN.CENTER)

    # ── LAYOUT 2: AESTHETIC SPLIT (LEFT TEXT, RIGHT VISUAL) ───────────────────
    def _lay_aesthetic_split(self, d: dict, cur: int, total: int):
        slide = self._blank()
        self._header(slide, d.get("title", ""))
        self._footer(slide, cur, total)
        
        bt = Inches(1.5)
        bh = H - bt - Inches(0.5)
        lw = (W - Inches(1.5)) * 0.45
        
        # Left Text Panel (Dense Bullets)
        self._card(slide, Inches(0.5), bt, lw, bh)
        sy = bt + Inches(0.3)
        bullets = d.get("bullets", [])
        sh = (bh - Inches(0.6)) / max(len(bullets), 1)
        
        for b in bullets[:4]:
            bold = b.get("bold", "")
            txt = b.get("text", "")
            if bold: txt = f"{bold}: {txt}"
            _tb(slide, "• " + txt, Inches(0.8), sy, lw-Inches(0.6), sh, sz=12, col=self.P["text"])
            sy += sh
            
        # Right Visual Panel
        rx = Inches(0.5) + lw + Inches(0.5)
        rw = W - rx - Inches(0.5)
        self._viz(slide, rx, bt, rw, bh, d.get("visual_suggestion", "[ Suggested Visual ]"), d.get("image_path"))

    # ── LAYOUT 3: AESTHETIC GRID (2x2 CARDS + SMALL VIZ) ──────────────────────
    def _lay_aesthetic_grid(self, d: dict, cur: int, total: int):
        slide = self._blank()
        self._header(slide, d.get("title", ""))
        self._footer(slide, cur, total)
        
        bt = Inches(1.5)
        bh = H - bt - Inches(0.5)
        
        cw = (W - Inches(1.5)) / 2
        ch = (bh - Inches(0.3)) / 2
        
        cards = d.get("cards", [])
        for i, c in enumerate(cards[:4]):
            col = i % 2
            row = i // 2
            cx = Inches(0.5) + col*(cw + Inches(0.5))
            cy = bt + row*(ch + Inches(0.3))
            
            self._card(slide, cx, cy, cw, ch)
            _shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, cx, cy, cw, Inches(0.1), fill=self.P["ac2"])
            
            _tb(slide, c.get("header",""), cx+Inches(0.3), cy+Inches(0.2), cw-Inches(0.6), Inches(0.4), sz=16, bold=True, col=self.P["text"])
            
            sy = cy + Inches(0.7)
            bsh = (ch - Inches(0.8)) / max(len(c.get("bullets",[])), 1)
            for b in c.get("bullets",[])[:3]:
                _tb(slide, "• " + b, cx+Inches(0.3), sy, cw-Inches(0.6), bsh, sz=11, col=self.P["text"])
                sy += bsh

    # ── LAYOUT 4: AESTHETIC FLOW (TOP TEXT, BOTTOM MASSIVE VISUAL) ────────────
    def _lay_aesthetic_flow(self, d: dict, cur: int, total: int):
        slide = self._blank()
        self._header(slide, d.get("title", ""))
        self._footer(slide, cur, total)
        
        bt = Inches(1.5)
        
        # Top Description
        self._card(slide, Inches(0.5), bt, W-Inches(1.0), Inches(1.2))
        _tb(slide, d.get("description",""), Inches(0.8), bt+Inches(0.2), W-Inches(1.6), Inches(0.8), sz=13, col=self.P["text"])
        
        # Bottom Visual
        vt = bt + Inches(1.5)
        vh = H - vt - Inches(0.5)
        self._viz(slide, Inches(0.5), vt, W-Inches(1.0), vh, d.get("visual_suggestion", "[ Architecture Flowchart ]"), d.get("image_path"))

    # ── LAYOUT 5: AESTHETIC TIMELINE ──────────────────────────────────────────
    def _lay_aesthetic_timeline(self, d: dict, cur: int, total: int):
        slide = self._blank()
        self._header(slide, d.get("title", ""))
        self._footer(slide, cur, total)
        
        bt = Inches(2.5)
        nodes = d.get("nodes", [])
        if not nodes: return
        
        # Central track
        _shape(slide, MSO_SHAPE.RECTANGLE, Inches(1.0), bt + Inches(1.5), W-Inches(2.0), Inches(0.1), fill=self.P["viz"])
        
        nw = (W - Inches(2.0)) / max(len(nodes), 1)
        
        for i, n in enumerate(nodes[:5]):
            nx = Inches(1.0) + i*nw
            # Node dot
            _shape(slide, MSO_SHAPE.OVAL, nx + nw/2 - Inches(0.15), bt + Inches(1.5) - Inches(0.1), Inches(0.3), Inches(0.3), fill=self.P["ac1"])
            
            # Alternating top/bottom cards
            cy = bt if i % 2 == 0 else bt + Inches(2.0)
            self._card(slide, nx + Inches(0.1), cy, nw - Inches(0.2), Inches(1.3))
            _shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, nx + Inches(0.1), cy, nw - Inches(0.2), Inches(0.1), fill=self.P["ac2"])
            
            _tb(slide, n.get("header","Phase"), nx + Inches(0.2), cy + Inches(0.15), nw - Inches(0.4), Inches(0.3), sz=14, bold=True, col=self.P["text"], align=PP_ALIGN.CENTER)
            _tb(slide, n.get("text",""), nx + Inches(0.2), cy + Inches(0.45), nw - Inches(0.4), Inches(0.8), sz=10, col=self.P["text"], align=PP_ALIGN.CENTER)

    # ── LAYOUT 6: AESTHETIC COMPARISON ────────────────────────────────────────
    def _lay_aesthetic_comparison(self, d: dict, cur: int, total: int):
        slide = self._blank()
        self._header(slide, d.get("title", ""))
        self._footer(slide, cur, total)
        
        bt = Inches(1.5)
        bh = H - bt - Inches(0.5)
        cw = (W - Inches(1.5)) / 2
        
        # Left Side
        self._card(slide, Inches(0.5), bt, cw, bh)
        _shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), bt, cw, Inches(0.15), fill=self.P["ac1"])
        _tb(slide, d.get("left_header","Left"), Inches(0.8), bt+Inches(0.3), cw-Inches(0.6), Inches(0.5), sz=18, bold=True, col=self.P["ac1"], align=PP_ALIGN.CENTER)
        
        sy = bt + Inches(1.0)
        lblts = d.get("left_bullets", [])
        lsh = (bh - Inches(1.2)) / max(len(lblts), 1)
        for b in lblts[:4]:
            _tb(slide, "• " + b, Inches(0.8), sy, cw-Inches(0.6), lsh, sz=12, col=self.P["text"])
            sy += lsh
            
        # Right Side
        rx = Inches(1.0) + cw
        self._card(slide, rx, bt, cw, bh)
        _shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, rx, bt, cw, Inches(0.15), fill=self.P["ac2"])
        _tb(slide, d.get("right_header","Right"), rx+Inches(0.3), bt+Inches(0.3), cw-Inches(0.6), Inches(0.5), sz=18, bold=True, col=self.P["ac2"], align=PP_ALIGN.CENTER)
        
        sy = bt + Inches(1.0)
        rblts = d.get("right_bullets", [])
        rsh = (bh - Inches(1.2)) / max(len(rblts), 1)
        for b in rblts[:4]:
            _tb(slide, "• " + b, rx+Inches(0.3), sy, cw-Inches(0.6), rsh, sz=12, col=self.P["text"])
            sy += rsh

    # ── LAYOUT 7: AESTHETIC METRICS ───────────────────────────────────────────
    def _lay_aesthetic_metrics(self, d: dict, cur: int, total: int):
        slide = self._blank()
        self._header(slide, d.get("title", ""))
        self._footer(slide, cur, total)
        
        bt = Inches(1.5)
        metrics = d.get("metrics", [])
        mw = (W - Inches(1.0) - Inches(0.5)*max(len(metrics)-1, 0)) / max(len(metrics), 1)
        
        # Top Metrics
        for i, m in enumerate(metrics[:3]):
            mx = Inches(0.5) + i*(mw + Inches(0.5))
            self._card(slide, mx, bt, mw, Inches(1.5))
            _shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, mx, bt, mw, Inches(0.1), fill=self.P["ac1"])
            
            _tb(slide, m.get("value","0%"), mx+Inches(0.1), bt+Inches(0.2), mw-Inches(0.2), Inches(0.8), sz=36, bold=True, col=self.P["ac1"], align=PP_ALIGN.CENTER)
            _tb(slide, m.get("label","Metric"), mx+Inches(0.1), bt+Inches(1.0), mw-Inches(0.2), Inches(0.4), sz=11, col=self.P["text"], align=PP_ALIGN.CENTER)
            
        # Bottom Visual
        vt = bt + Inches(1.8)
        vh = H - vt - Inches(0.5)
        self._viz(slide, Inches(0.5), vt, W-Inches(1.0), vh, d.get("visual_suggestion", "[ Metric Graph ]"), d.get("image_path"))


# API Aliases for backend route compatibility
def ppt_create(prompt: str, style: str=None, output_path: str=None):
    yield "🤖 Groq (LLaMA 3.3-70B) generating AESTHETIC high-density presentation...\n"
    raw = _groq_call(_SYS, _USR.format(prompt=prompt))
    plan = _parse(raw)
    if style and style in PERSONALITIES:
        plan["personality"] = style
    out = output_path or str(Path.home()/"Desktop"/f"Aesthetic_Deck_{int(time.time())}.pptx")
    b = PresentationBuilder(plan, out)
    for s in b.build_with_progress(): yield s + "\n"
    yield f"📂 Saved to: `{out}`\n"

def ppt_styles():
    return {"styles": {k: {"name": v["name"], "desc": v["desc"]} for k,v in PERSONALITIES.items()}, "count": len(PERSONALITIES)}

def _pick(p):
    return "ocean_pro"
