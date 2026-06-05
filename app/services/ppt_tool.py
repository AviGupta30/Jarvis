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
                  "bg": "F8FAFC", "card": "FFFFFF", "text": "0F172A", "ac1": "2563EB", "ac2": "3B82F6", "viz": "E2E8F0"}
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
- Exactly 10 slides.
- First slide MUST use "aesthetic_title".
- Use a mix of "aesthetic_split", "aesthetic_grid", and "aesthetic_flow" for the rest.
- TEXT MUST BE EXTREMELY DENSE. Every bullet array must have 3-4 items, and each text property MUST be 25-30 words of deep technical/strategic detail. No short bullets. We want to fill the slides with rich text.
- Every layout requires a "visual_suggestion" detailing exactly what flowchart/diagram goes in the massive placeholder.
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
        {{"bold": "Key Point 1", "text": "25-30 words of extremely detailed context ensuring vertical space is filled completely."}},
        {{"bold": "Key Point 2", "text": "25-30 words explaining consequences, metrics, or current system failures in depth."}},
        {{"bold": "Key Point 3", "text": "25-30 words on why previous approaches fall short and what needs to change."}}
      ],
      "visual_suggestion": "[ Diagram: User pain-point flowchart or current system architecture ]"
    }},
    {{
      "slide_number": 3,
      "layout": "aesthetic_grid",
      "title": "Technical Approach",
      "cards": [
        {{
          "header": "Data Ingestion",
          "bullets": ["20 words detailing the pipeline", "20 words on scaling", "20 words on security"]
        }},
        // EXACTLY 4 cards total, each fully fleshed out to look dense.
        {{"header":"...","bullets":["...","...","..."]}},
        {{"header":"...","bullets":["...","...","..."]}},
        {{"header":"...","bullets":["...","...","..."]}}
      ]
    }},
    {{
      "slide_number": 4,
      "layout": "aesthetic_flow",
      "title": "System Architecture",
      "description": "A dense 50-word paragraph explaining the exact end-to-end data flow and logical architecture before displaying the huge diagram below.",
      "visual_suggestion": "[ Massive Flowchart: User -> API -> DB -> LLM ]"
    }}
  ]
}}"""

def _groq_call(sys_p: str, usr_p: str, tokens: int = 6000) -> str:
    if _GROQ is None: raise RuntimeError("GROQ_API_KEY not configured")
    r = _GROQ.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role":"system","content":sys_p}, {"role":"user","content":usr_p}],
        max_tokens=tokens, temperature=0.7, response_format={"type":"json_object"},
    )
    return r.choices[0].message.content or ""

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

    def _header(self, slide, title: str):
        # Aesthetic header with rounded colored accent
        _shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(0.4), W-Inches(1.0), Inches(0.8), fill=self.P["card"])
        _shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(0.4), Inches(0.2), Inches(0.8), fill=self.P["ac1"])
        _tb(slide, title.upper(), Inches(0.9), Inches(0.5), W-Inches(2.0), Inches(0.6), sz=24, bold=True, col=self.P["text"], font="Inter")

    def _viz(self, slide, l, t, w, h, text):
        # Massive rounded visual placeholder box
        _shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, l, t, w, h, fill=self.P["viz"], line=self.P["ac2"], lw=1.5)
        _tb(slide, text, l+Inches(0.2), t+h/2-Inches(0.5), w-Inches(0.4), Inches(1.0), sz=14, italic=True, col=self.P["ac1"], align=PP_ALIGN.CENTER)

    def build_with_progress(self) -> Generator[str,None,None]:
        slides = self.plan.get("slides",[])
        for i, sd in enumerate(slides):
            lay = sd.get("layout","aesthetic_split")
            yield f"🔨 Slide {i+1} — {sd.get('title','')} ({lay})"
            fn = getattr(self, f"_lay_{lay}", self._lay_aesthetic_split)
            fn(sd)
        yield "💾 Saving…"
        self.prs.save(self.out)

    # ── LAYOUT 1: TITLE ───────────────────────────────────────────────────────
    def _lay_aesthetic_title(self, d: dict):
        slide = self._blank()
        
        # Center card
        cw, ch = Inches(10.0), Inches(4.0)
        cx, cy = (W-cw)/2, (H-ch)/2
        _shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, cx, cy, cw, ch, fill=self.P["card"])
        
        # Accents
        _shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, cx, cy, cw, Inches(0.15), fill=self.P["ac1"])
        
        _tb(slide, d.get("title", "Title"), cx+Inches(0.5), cy+Inches(0.8), cw-Inches(1.0), Inches(1.2), sz=44, bold=True, col=self.P["text"], align=PP_ALIGN.CENTER)
        _tb(slide, d.get("subtitle", ""), cx+Inches(1.0), cy+Inches(2.0), cw-Inches(2.0), Inches(1.5), sz=14, col=self.P["text"], align=PP_ALIGN.CENTER)

    # ── LAYOUT 2: AESTHETIC SPLIT (LEFT TEXT, RIGHT VISUAL) ───────────────────
    def _lay_aesthetic_split(self, d: dict):
        slide = self._blank()
        self._header(slide, d.get("title", ""))
        
        bt = Inches(1.5)
        bh = H - bt - Inches(0.5)
        lw = (W - Inches(1.5)) * 0.45
        
        # Left Text Panel (Dense Bullets)
        _shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), bt, lw, bh, fill=self.P["card"])
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
        self._viz(slide, rx, bt, rw, bh, d.get("visual_suggestion", "[ Suggested Visual ]"))

    # ── LAYOUT 3: AESTHETIC GRID (2x2 CARDS + SMALL VIZ) ──────────────────────
    def _lay_aesthetic_grid(self, d: dict):
        slide = self._blank()
        self._header(slide, d.get("title", ""))
        
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
            
            _shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, cx, cy, cw, ch, fill=self.P["card"])
            _shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, cx, cy, cw, Inches(0.1), fill=self.P["ac2"])
            
            _tb(slide, c.get("header",""), cx+Inches(0.3), cy+Inches(0.2), cw-Inches(0.6), Inches(0.4), sz=16, bold=True, col=self.P["text"])
            
            sy = cy + Inches(0.7)
            bsh = (ch - Inches(0.8)) / max(len(c.get("bullets",[])), 1)
            for b in c.get("bullets",[])[:3]:
                _tb(slide, "• " + b, cx+Inches(0.3), sy, cw-Inches(0.6), bsh, sz=11, col=self.P["text"])
                sy += bsh

    # ── LAYOUT 4: AESTHETIC FLOW (TOP TEXT, BOTTOM MASSIVE VISUAL) ────────────
    def _lay_aesthetic_flow(self, d: dict):
        slide = self._blank()
        self._header(slide, d.get("title", ""))
        
        bt = Inches(1.5)
        
        # Top Description
        _shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), bt, W-Inches(1.0), Inches(1.2), fill=self.P["card"])
        _tb(slide, d.get("description",""), Inches(0.8), bt+Inches(0.2), W-Inches(1.6), Inches(0.8), sz=13, col=self.P["text"])
        
        # Bottom Visual
        vt = bt + Inches(1.5)
        vh = H - vt - Inches(0.5)
        self._viz(slide, Inches(0.5), vt, W-Inches(1.0), vh, d.get("visual_suggestion", "[ Architecture Flowchart ]"))


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
