"""
ppt_tool.py — Premium Visual-First PPT Engine v5
=================================================
Design philosophy:
  • Visuals are DOMINANT — image gets 58%+ of the slide width/height
  • Background has depth — gradient strips, decorative geometry
  • Cards are content-dense — colored numbered tags, bold sub-headers, tight spacing
  • Image frame is premium — thick border + L-corner accents + subtle inner glow ring
  • Every slide has a polished header: brand chip + centered title box + accent line
  • Bottom: full-width bar + slide counter
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

W = Inches(13.33)
H = Inches(7.5)

# ─── Premium Palettes ──────────────────────────────────────────────────────────
PERSONALITIES = {
    "ocean_pro": {
        "name": "Ocean Pro", "desc": "Deep navy + electric cyan.",
        "bg": "050E1F", "bg2": "09162E", "card": "0D1F3C", "card2": "0A1830",
        "text": "D8EEFF", "sub": "7AACCC", "ac1": "00C8FF", "ac2": "0077CC", "ac3": "00FFB3",
        "border": "00C8FF", "hdr_bg": "00C8FF", "hdr_text": "050E1F", "bar": "0077CC",
        "tag_colors": ["00C8FF", "0077CC", "00FFB3", "4488FF"],
    },
    "neon_dark": {
        "name": "Neon Dark", "desc": "Black + vivid purple/pink.",
        "bg": "06020D", "bg2": "0E0520", "card": "140830", "card2": "1A0A3A",
        "text": "F5EEFF", "sub": "C4A8EE", "ac1": "BF5FFF", "ac2": "FF2D78", "ac3": "00F5FF",
        "border": "BF5FFF", "hdr_bg": "BF5FFF", "hdr_text": "06020D", "bar": "FF2D78",
        "tag_colors": ["BF5FFF", "FF2D78", "00F5FF", "FF8800"],
    },
    "emerald": {
        "name": "Emerald", "desc": "Dark forest green + gold.",
        "bg": "021A0C", "bg2": "042A14", "card": "083820", "card2": "0A4228",
        "text": "D8FFF0", "sub": "88CCAA", "ac1": "00E878", "ac2": "00AA55", "ac3": "FFD700",
        "border": "00E878", "hdr_bg": "00E878", "hdr_text": "021A0C", "bar": "00AA55",
        "tag_colors": ["00E878", "00AA55", "FFD700", "44DDBB"],
    },
    "clean_light": {
        "name": "Clean Light", "desc": "White + corporate blue.",
        "bg": "F0F5FF", "bg2": "E4EDFF", "card": "FFFFFF", "card2": "EBF2FF",
        "text": "0A1628", "sub": "3A5888", "ac1": "1A56DB", "ac2": "1040BB", "ac3": "F59E0B",
        "border": "1A56DB", "hdr_bg": "1A56DB", "hdr_text": "FFFFFF", "bar": "1040BB",
        "tag_colors": ["1A56DB", "F59E0B", "10B981", "EF4444"],
    },
    "synthwave": {
        "name": "Synthwave", "desc": "Neon pink + purple. Retro cyber.",
        "bg": "0A0118", "bg2": "130228", "card": "1C0535", "card2": "240645",
        "text": "FFE8FF", "sub": "D4A0D8", "ac1": "FF1493", "ac2": "9B30FF", "ac3": "00FFEE",
        "border": "FF1493", "hdr_bg": "FF1493", "hdr_text": "FFFFFF", "bar": "9B30FF",
        "tag_colors": ["FF1493", "9B30FF", "00FFEE", "FFAA00"],
    },
    "aurora": {
        "name": "Aurora", "desc": "Dark teal + bright green.",
        "bg": "011215", "bg2": "021C20", "card": "042C30", "card2": "05383D",
        "text": "D8FFF8", "sub": "80C8C0", "ac1": "00E8CC", "ac2": "00A898", "ac3": "80FF44",
        "border": "00E8CC", "hdr_bg": "00E8CC", "hdr_text": "011215", "bar": "00A898",
        "tag_colors": ["00E8CC", "00A898", "80FF44", "FFCC00"],
    },
    "hacker_terminal": {
        "name": "Hacker Terminal", "desc": "Pitch black + lime green.",
        "bg": "000000", "bg2": "040804", "card": "080D08", "card2": "0D140D",
        "text": "B8FFB8", "sub": "5EA85E", "ac1": "39FF14", "ac2": "20C000", "ac3": "FFFF00",
        "border": "39FF14", "hdr_bg": "39FF14", "hdr_text": "000000", "bar": "20C000",
        "tag_colors": ["39FF14", "20C000", "FFFF00", "FF8800"],
    },
    "solar_flare": {
        "name": "Solar Flare", "desc": "Charcoal + amber. Startup energy.",
        "bg": "0A0700", "bg2": "160E00", "card": "241500", "card2": "2E1A00",
        "text": "FFF8E8", "sub": "D4B870", "ac1": "FF8C00", "ac2": "FF5500", "ac3": "FFD700",
        "border": "FF8C00", "hdr_bg": "FF8C00", "hdr_text": "0A0700", "bar": "FF5500",
        "tag_colors": ["FF8C00", "FF5500", "FFD700", "FF2200"],
    },
    "midnight_exec": {
        "name": "Midnight Executive", "desc": "Deep indigo + platinum.",
        "bg": "05061A", "bg2": "090C28", "card": "101538", "card2": "161C44",
        "text": "E8EAF8", "sub": "8890C8", "ac1": "8080FF", "ac2": "5050DD", "ac3": "C0C0FF",
        "border": "8080FF", "hdr_bg": "8080FF", "hdr_text": "05061A", "bar": "5050DD",
        "tag_colors": ["8080FF", "5050DD", "C0C0FF", "FF8080"],
    },
    "cyber_dark": {
        "name": "Cyber Dark", "desc": "Dark navy + electric teal.",
        "bg": "030B18", "bg2": "060F25", "card": "091830", "card2": "0C1E3A",
        "text": "C8F0FF", "sub": "5AAABB", "ac1": "00F3FF", "ac2": "0088FF", "ac3": "00FF88",
        "border": "00F3FF", "hdr_bg": "00F3FF", "hdr_text": "030B18", "bar": "0088FF",
        "tag_colors": ["00F3FF", "0088FF", "00FF88", "FF8800"],
    },
    "arctic_clean": {
        "name": "Arctic Clean", "desc": "Ice white + deep teal.",
        "bg": "EDF8FA", "bg2": "D8EFF5", "card": "FFFFFF", "card2": "D0EBF5",
        "text": "001828", "sub": "005070", "ac1": "0088AA", "ac2": "006688", "ac3": "00CCAA",
        "border": "0088AA", "hdr_bg": "0088AA", "hdr_text": "FFFFFF", "bar": "006688",
        "tag_colors": ["0088AA", "006688", "00CCAA", "FF8800"],
    },
    "forest_calm": {
        "name": "Forest Calm", "desc": "Forest green + cream.",
        "bg": "041008", "bg2": "071A0C", "card": "0C2A12", "card2": "103416",
        "text": "D8F0DC", "sub": "80B888", "ac1": "44CC66", "ac2": "2EA050", "ac3": "CCFF44",
        "border": "44CC66", "hdr_bg": "44CC66", "hdr_text": "041008", "bar": "2EA050",
        "tag_colors": ["44CC66", "2EA050", "CCFF44", "FF8800"],
    },
    "ocean_gradient": {
        "name": "Ocean Gradient", "desc": "Deep ocean + cerulean.",
        "bg": "020B18", "bg2": "04102A", "card": "081830", "card2": "0B1E3A",
        "text": "C8E8FF", "sub": "6899BB", "ac1": "0099DD", "ac2": "0066BB", "ac3": "00DDCC",
        "border": "0099DD", "hdr_bg": "0099DD", "hdr_text": "020B18", "bar": "0066BB",
        "tag_colors": ["0099DD", "0066BB", "00DDCC", "FF8800"],
    },
    "velvet_noir": {
        "name": "Velvet Noir", "desc": "Deep plum + rose gold.",
        "bg": "0E0618", "bg2": "160828", "card": "1E0C3A", "card2": "280E48",
        "text": "F8E8FF", "sub": "C898D8", "ac1": "CC88FF", "ac2": "AA44CC", "ac3": "FFAA80",
        "border": "CC88FF", "hdr_bg": "CC88FF", "hdr_text": "0E0618", "bar": "AA44CC",
        "tag_colors": ["CC88FF", "AA44CC", "FFAA80", "FF2D78"],
    },
    "charcoal_minimal": {
        "name": "Charcoal Minimal", "desc": "True black + gold.",
        "bg": "0A0A0A", "bg2": "121212", "card": "1C1C1C", "card2": "242424",
        "text": "F0F0F0", "sub": "909090", "ac1": "CCA020", "ac2": "EEC040", "ac3": "FFFFFF",
        "border": "CCA020", "hdr_bg": "CCA020", "hdr_text": "0A0A0A", "bar": "EEC040",
        "tag_colors": ["CCA020", "EEC040", "FFFFFF", "FF5500"],
    },
}


def _c(h: str) -> RGBColor:
    h = h.lstrip("#")
    return RGBColor(int(h[:2], 16), int(h[2:4], 16), int(h[4:], 16))

def _bg_fill(slide, col: str):
    b = slide.background; b.fill.solid(); b.fill.fore_color.rgb = _c(col)

def _shape(slide, shp_type, l, t, w, h, fill=None, line=None, lw=1.0):
    sh = slide.shapes.add_shape(shp_type, l, t, w, h)
    if fill: sh.fill.solid(); sh.fill.fore_color.rgb = _c(fill)
    else: sh.fill.background()
    if line: sh.line.color.rgb = _c(line); sh.line.width = Pt(lw)
    else: sh.line.fill.background()
    return sh

def _rect(slide, l, t, w, h, fill=None, line=None, lw=1.0):
    return _shape(slide, MSO_SHAPE.RECTANGLE, l, t, w, h, fill=fill, line=line, lw=lw)

def _round(slide, l, t, w, h, fill=None, line=None, lw=1.0):
    return _shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, l, t, w, h, fill=fill, line=line, lw=lw)

def _oval(slide, l, t, w, h, fill=None, line=None, lw=1.0):
    return _shape(slide, MSO_SHAPE.OVAL, l, t, w, h, fill=fill, line=line, lw=lw)

def _tb(slide, text: str, l, t, w, h, font="Calibri", sz=11, bold=False, italic=False,
        col="FFFFFF", align=PP_ALIGN.LEFT):
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

def _clean_image_path(image_path: str) -> str:
    if not image_path: return ""
    s = str(image_path)
    m = re.search(r'\[ATTACHED_FILE:\s*(.+?)(?:\s*\|.*)?\]', s)
    if m: return m.group(1).strip()
    return s.split('|')[0].strip()

def _get_image_aspect_ratio(path: str) -> float:
    """Returns width / height of image using PIL if available, else 1.0"""
    try:
        from PIL import Image
        with Image.open(path) as img:
            return img.width / max(img.height, 1)
    except Exception:
        return 1.0

def _corner_L(slide, l, t, w, h, col, size=Inches(0.35), th=Inches(0.055)):
    """Draw 4 L-shaped corner brackets."""
    for lx, ly, bw, bh in [
        (l,         t,         size, th),  (l,         t,          th,   size),
        (l+w-size,  t,         size, th),  (l+w-th,    t,          th,   size),
        (l,         t+h-th,    size, th),  (l,         t+h-size,   th,   size),
        (l+w-size,  t+h-th,    size, th),  (l+w-th,    t+h-size,   th,   size),
    ]:
        _rect(slide, lx, ly, bw, bh, fill=col)


# ─── Groq Prompt ───────────────────────────────────────────────────────────────
_SYS = """\
You are an elite presentation generator. Create dense, visually rich slides.
Output ONLY valid JSON — no markdown fences, no explanation."""

_USR = """\
Create a VISUAL-FIRST, content-dense presentation for:
TOPIC/REQUEST: {prompt}

CRITICAL INSTRUCTION FOR MODIFICATIONS: If the REQUEST asks to change the theme, style, or colors of a previous presentation, you MUST preserve the EXACT SAME TOPIC AND CONTENT from the previous context. Do NOT make a new presentation about the color/theme itself!


CRITICAL RULES:
- Create 8 to 12 slides based on topic complexity.
- First slide MUST use "aesthetic_title".
- Use a mix of layouts: "aesthetic_split", "aesthetic_grid", "aesthetic_flow", "aesthetic_timeline", "aesthetic_comparison", "aesthetic_metrics", "aesthetic_pitch".
- Prefer "aesthetic_split", "aesthetic_flow", and "aesthetic_pitch" — they have LARGE dedicated visual areas.
- EVERY SLIDE that has a visual zone (aesthetic_split, aesthetic_flow, aesthetic_metrics, aesthetic_pitch) MUST include EITHER an "image_path" (if user provided [ATTACHED_FILE: <path>]) OR a "visual_suggestion" describing a specific, detailed diagram/infographic for that slide.
- BULLETS/CONTENT: You MUST make the presentation CONTENT HEAVY. Do not output single-line sentences. Each bullet/card MUST contain a bold label (2-5 words) AND highly detailed, multi-sentence text (40-60 words). Fill the cards so they look dense and professional. For timeline layouts, the "text" field MUST be massive and highly descriptive (50-80 words).
- VISUALS: Every aesthetic_split, aesthetic_flow, aesthetic_metrics, aesthetic_pitch slide MUST include "visual_suggestion" with a specific diagram/chart description. If [ATTACHED_FILE: <path>] tags exist, set "image_path" to that exact path.
- COLORS: If the user requests ANY specific color or theme (e.g. "cyan", "red", "maroon and golden"), DO NOT rely on presets. You MUST output a "custom_theme" object with 6-character hex codes (NO hash) that PERFECTLY matches their request. Set "ac1", "ac2", "ac3", "border", "hdr_bg", and "bar" to the requested colors.
- BOLD FIELD must always be set and act as a mini sub-header (2-4 word label).
- Output ONLY valid JSON. No trailing commas.

JSON SCHEMA:
{{
  "presentation_title": "...",
  "personality": "ocean_pro",
  "custom_theme": {{"bg": "400000", "bg2": "4A0000", "card": "550000", "card2": "600000", "text": "FFFFFF", "sub": "DDDDDD", "ac1": "FFD700", "ac2": "FFAA00", "ac3": "FFFF00", "border": "FFD700", "hdr_bg": "FFD700", "hdr_text": "400000", "bar": "FFD700"}},
  "slides": [
    {{
      "slide_number": 1,
      "layout": "aesthetic_title",
      "title": "Topic Name",
      "subtitle": "Three concise technical sentences covering the core innovation, implementation stack, and measurable business impact."
    }},
    {{
      "slide_number": 2,
      "layout": "aesthetic_split",
      "title": "Problem Statement",
      "bullets": [
        {{"bold": "Integration Gap", "text": "Existing infrastructure lacks native AI connectors, requiring costly custom middleware that breaks during major platform upgrades and creates vendor lock-in."}},
        {{"bold": "Data Silos", "text": "Fragmented data across 15+ systems with incompatible schemas prevents unified analytics, forcing analysts to manually reconcile reports for every stakeholder meeting."}},
        {{"bold": "Scalability", "text": "Legacy batch processing handles only 10K events/hour vs the 2M events/hour required for real-time monitoring of modern distributed microservice architectures."}},
        {{"bold": "Cost Overrun", "text": "Manual operations consume 40% of engineering bandwidth on toil, driving OpEx 3x above industry benchmarks and delaying feature delivery by an average of 6 weeks."}}
      ],
      "visual_suggestion": "[ Detailed flowchart: Current fragmented system with pain-point annotations at each bottleneck ]",
      "image_path": ""
    }},
    {{
      "slide_number": 3,
      "layout": "aesthetic_timeline",
      "title": "Phased Deployment Roadmap",
      "nodes": [
        {{"header": "Phase 1", "text": "Extensive text here describing exactly what happens in phase 1 in extreme detail spanning 50-80 words..."}},
        {{"header": "Phase 2", "text": "Extensive text here describing exactly what happens in phase 2 in extreme detail spanning 50-80 words..."}}
      ]
    }}
  ]
}}"""


def _groq_call(sys_p: str, usr_p: str, tokens: int = 4000) -> str:
    if _GROQ is None: raise RuntimeError("GROQ_API_KEY not configured")
    safe_tokens = min(tokens, 4500)
    try:
        r = _GROQ.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": sys_p}, {"role": "user", "content": usr_p}],
            max_tokens=safe_tokens, temperature=0.7, response_format={"type": "json_object"},
        )
        return r.choices[0].message.content or ""
    except Exception as e:
        err_str = str(e).lower()
        if "429" in err_str or "413" in err_str or "rate" in err_str or "too large" in err_str:
            r = _GROQ.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "system", "content": sys_p}, {"role": "user", "content": usr_p}],
                max_tokens=safe_tokens, temperature=0.7, response_format={"type": "json_object"},
            )
            return r.choices[0].message.content or ""
        raise e

def _parse(raw: str) -> dict:
    raw = re.sub(r"```(?:json)?|```", "", raw).strip()
    return json.loads(raw[raw.find("{"):raw.rfind("}") + 1])


# ─────────────────────────────────────────────────────────────────────────────
class PresentationBuilder:
    def __init__(self, plan: dict, out: str):
        self.plan = plan
        self.out = out
        self.prs = Presentation()
        self.prs.slide_width = W
        self.prs.slide_height = H
        
        pk = plan.get("personality", "ocean_pro")
        base_p = PERSONALITIES.get(pk, PERSONALITIES["ocean_pro"])
        
        # Deep copy to allow overrides
        self.P = dict(base_p)
        
        # Dynamic custom theme overrides! If user specified explicit colors not matching presets
        custom = plan.get("custom_theme", {})
        if isinstance(custom, dict) and custom:
            # ENFORCE PREMIUM DARK MODE AESTHETICS FOR CUSTOM THEMES
            # Users often get ugly colors if LLM picks them blindly.
            # We force background to near-black and text to white.
            # We only adopt the LLM's colors for the accents.
            
            # Extract accents from whatever the LLM gave
            accents = []
            for k in ["ac1", "ac2", "ac3", "hdr_bg", "border", "bg", "card"]:
                if k in custom and isinstance(custom[k], str) and len(custom[k]) == 6:
                    accents.append(custom[k])
                    
            if not accents:
                accents = ["FFD700", "FF5500", "00C8FF"] # Fallback accents
                
            primary = accents[0]
            secondary = accents[1] if len(accents) > 1 else primary
            tertiary = accents[2] if len(accents) > 2 else secondary

            bg_hex = custom.get("bg", "0A0A0E")
            try:
                r, g, b = int(bg_hex[0:2], 16), int(bg_hex[2:4], 16), int(bg_hex[4:6], 16)
                lum = (0.299*r + 0.587*g + 0.114*b) / 255
            except:
                lum = 0
                
            is_light = lum > 0.6

            if is_light:
                self.P["bg"] = "FFFFFF"
                self.P["bg2"] = "F0F0F0"
                self.P["card"] = "F8F8F8"
                self.P["card2"] = "EAEAEA"
                self.P["text"] = "111111"
                self.P["sub"] = "333333"
                self.P["hdr_text"] = "FFFFFF"
            else:
                self.P["bg"] = "0A0A0E"
                self.P["bg2"] = "121218"
                self.P["card"] = "1A1A22"
                self.P["card2"] = "22222C"
                self.P["text"] = "F5F5F5"
                self.P["sub"] = "B0B0C0"
                self.P["hdr_text"] = "000000"
            
            self.P["ac1"] = primary
            self.P["ac2"] = secondary
            self.P["ac3"] = tertiary
            self.P["border"] = primary
            self.P["hdr_bg"] = primary
            self.P["bar"] = secondary
            
            self.P["tag_colors"] = [primary, secondary, tertiary, "FFFFFF"]

    def _blank(self):
        s = self.prs.slides.add_slide(self.prs.slide_layouts[6])
        _bg_fill(s, self.P["bg"])
        # Subtle secondary tone strips top and bottom
        _rect(s, 0, 0, W, Inches(0.06), fill=self.P["ac1"])
        _rect(s, 0, H - Inches(0.28), W, Inches(0.28), fill=self.P["bar"])
        # Decorative dark panel on right edge — adds depth
        _rect(s, W - Inches(0.18), Inches(0.06), Inches(0.18), H - Inches(0.34), fill=self.P["bg2"])
        return s

    def _progress(self, slide, cur, total):
        _tb(slide, f"{cur:02d} / {total:02d}", W - Inches(1.35), H - Inches(0.24),
            Inches(1.1), Inches(0.2), sz=9, bold=True, col=self.P["text"], align=PP_ALIGN.RIGHT)

    def _header(self, slide, title: str):
        """Centered ROUNDED bordered title box + thin accent rule."""
        # Center title box — ROUNDED rectangle with thick colored border
        tx, ty, tw, th = Inches(0.25), Inches(0.08), W - Inches(0.5), Inches(0.64)
        _round(slide, tx + Inches(0.07), ty + Inches(0.07), tw, th,
               fill=self.P["bg2"], line=None)  # shadow
        _round(slide, tx, ty, tw, th, fill=self.P["card"], line=self.P["border"], lw=2.5)
        # Left accent stripe inside title box
        _rect(slide, tx, ty + Inches(0.06), Inches(0.1), th - Inches(0.12), fill=self.P["ac1"])
        _tb(slide, title.upper(), tx + Inches(0.22), ty + Inches(0.08),
            tw - Inches(0.32), th - Inches(0.12),
            sz=22, bold=True, col=self.P["text"], align=PP_ALIGN.CENTER)

        # Accent rule under header
        _rect(slide, Inches(0.25), Inches(0.76), W - Inches(0.5), Inches(0.04), fill=self.P["ac1"])

    def _premium_image_frame(self, slide, path: str, l, t, w, h, suggestion: str = ""):
        """Multi-layer premium image frame with ROUNDED corners and L-corner accents."""
        # Layer 1: dark glow shadow behind
        _round(slide, l + Inches(0.12), t + Inches(0.12), w, h, fill=self.P["bg2"], line=None)
        # Layer 2: outer ROUNDED border frame
        _round(slide, l, t, w, h, fill=self.P["card"], line=self.P["border"], lw=3.0)
        # Layer 3: thin inner accent ring
        pad1 = Inches(0.07)
        _round(slide, l + pad1, t + pad1, w - 2*pad1, h - 2*pad1,
               fill=None, line=self.P["ac2"], lw=0.9)

        # Corner L-brackets (sharp, they're decorative on top of the rounded card)
        # REMOVED: User explicitly disliked sharp corners falling out of the rounded radius.

        # Small status dots in top-right
        for di in range(3):
            _rect(slide, l + w - Inches(0.5) + di * Inches(0.14), t + Inches(0.12),
                  Inches(0.09), Inches(0.09), fill=[self.P["ac1"], self.P["ac2"], self.P["ac3"]][di])

        # Embed image or placeholder
        pad = Inches(0.13)
        clean = _clean_image_path(path) if path else ""
        if clean and Path(clean).exists():
            try:
                pic = slide.shapes.add_picture(clean, l + pad, t + pad, w - 2*pad, h - 2*pad)
                # Force the picture geometry to match the rounded frame
                pic.auto_shape_type = MSO_SHAPE.ROUNDED_RECTANGLE
                # Remove the sharp line border
                pic.line.fill.background()
                return
            except Exception as e:
                print(f"[ppt] image error: {e}")
                
        # If no image, render the text largely inside the beautiful frame
        _tb(slide, suggestion or "[ Detailed Content Block ]",
            l + Inches(0.5), t + Inches(0.5), w - Inches(1.0), h - Inches(1.0),
            sz=14.5, italic=False, col=self.P["sub"], align=PP_ALIGN.CENTER)

    def _bullet_card(self, slide, l, t, w, h, bold_txt: str, body_txt: str,
                     tag_col: str, idx: int):
        """Single dense bullet card with ROUNDED corners: number badge + bold header + body."""
        # Shadow
        _round(slide, l + Inches(0.06), t + Inches(0.06), w, h, fill=self.P["bg2"], line=None)
        # Card background — ROUNDED
        _round(slide, l, t, w, h, fill=self.P["card"], line=tag_col, lw=1.4)
        # Colored left stripe (rect clips to rounded card edge acceptably)
        _rect(slide, l, t + Inches(0.02), Inches(0.1), h - Inches(0.04), fill=tag_col)
        # Number badge circle
        _oval(slide, l + Inches(0.15), t + Inches(0.1), Inches(0.3), Inches(0.3),
              fill=tag_col, line=None)
        _tb(slide, str(idx), l + Inches(0.14), t + Inches(0.11), Inches(0.32), Inches(0.27),
            sz=10, bold=True, col=self.P["bg"], align=PP_ALIGN.CENTER)

        # Bold sub-header
        if bold_txt:
            _tb(slide, bold_txt, l + Inches(0.54), t + Inches(0.1), w - Inches(0.68),
                Inches(0.3), sz=12, bold=True, col=tag_col)
        # Body text
        body_top = t + Inches(0.35) if bold_txt else t + Inches(0.14)
        _tb(slide, body_txt, l + Inches(0.54), body_top, w - Inches(0.67),
            h - (Inches(0.38) if bold_txt else Inches(0.22)),
            sz=11.5, col=self.P["text"])

    def build_with_progress(self) -> Generator[str, None, None]:
        slides = self.plan.get("slides", [])
        total = len(slides)

        # ── Render each slide ──────────────────────────────────────────────────
        for i, sd in enumerate(slides):
            lay = sd.get("layout", "aesthetic_split")
            yield f"Slide {i+1} - {sd.get('title', '')}"

            fn = getattr(self, f"_lay_{lay}", self._lay_aesthetic_split)
            try:
                fn(sd, i+1, total)
            except Exception as e:
                yield f"Error {lay}: {e}"
                try: self._lay_aesthetic_split(sd, i+1, total)
                except: pass
        yield "Saving..."
        self.prs.save(self.out)

    # ── LAYOUT 1: TITLE SLIDE ─────────────────────────────────────────────────
    def _lay_aesthetic_title(self, d: dict, cur: int, total: int):
        slide = self._blank()
        self._progress(slide, cur, total)

        # Decorative large circle behind card (depth element)
        _oval(slide, W*0.55, H*0.1, Inches(5.5), Inches(5.5),
              fill=self.P["bg2"], line=self.P["border"], lw=0.5)
        _oval(slide, W*0.58, H*0.18, Inches(4.0), Inches(4.0),
              fill=self.P["bg"], line=self.P["ac2"], lw=0.4)

        # Center hero card
        cw, ch = Inches(11.0), Inches(5.4)
        cx, cy = (W - cw)/2, (H - ch)/2 - Inches(0.1)

        # Drop shadow
        _round(slide, cx + Inches(0.15), cy + Inches(0.15), cw, ch,
               fill=self.P["bg2"], line=None)
        # Main card
        _round(slide, cx, cy, cw, ch, fill=self.P["card"], line=self.P["border"], lw=2.0)
        # Top accent bar
        _round(slide, cx, cy, cw, Inches(0.2), fill=self.P["ac1"])
        # Bottom accent bar
        _rect(slide, cx, cy + ch - Inches(0.08), cw, Inches(0.08), fill=self.P["ac2"])

        # Corner L-brackets
        _corner_L(slide, cx, cy, cw, ch, col=self.P["ac1"], size=Inches(0.5), th=Inches(0.07))

        # Title
        _tb(slide, d.get("title", "Presentation"), cx + Inches(0.5), cy + Inches(0.4),
            cw - Inches(1.0), Inches(2.4), sz=48, bold=True, col=self.P["text"],
            align=PP_ALIGN.CENTER, font="Calibri")

        # Divider
        _rect(slide, cx + Inches(2.2), cy + Inches(2.95), cw - Inches(4.4), Inches(0.05),
              fill=self.P["ac1"])

        # Subtitle
        _tb(slide, d.get("subtitle", ""), cx + Inches(0.7), cy + Inches(3.1),
            cw - Inches(1.4), Inches(1.95), sz=13.5, col=self.P["sub"],
            align=PP_ALIGN.CENTER)

        # Bottom decoration dots
        for di in range(3):
            _rect(slide, cx + cw - Inches(0.8) + di * Inches(0.22),
                  cy + ch - Inches(0.38), Inches(0.12), Inches(0.12), fill=self.P["ac1"])

    # ── LAYOUT 2: SPLIT — LEFT DENSE BULLETS + RIGHT DOMINANT IMAGE ──────────
    def _lay_aesthetic_split(self, d: dict, cur: int, total: int):
        slide = self._blank()
        self._header(slide, d.get("title", ""))
        self._progress(slide, cur, total)

        top   = Inches(0.86)
        avail = H - top - Inches(0.3)
        gap   = Inches(0.2)

        # Image gets 57% of slide width — DOMINANT
        lw = (W - Inches(0.55)) * 0.41
        rw = (W - Inches(0.55)) * 0.57
        lx = Inches(0.25)
        rx = lx + lw + gap

        # ── RIGHT: Premium image frame ────────────────────────────────────
        self._premium_image_frame(slide, d.get("image_path", ""), rx, top, rw, avail,
                                   d.get("visual_suggestion", "[ Visual ]"))

        # ── LEFT: Dense bullet cards ──────────────────────────────────────
        bullets = d.get("bullets", [])
        tag_colors = self.P["tag_colors"]
        n = max(len(bullets[:4]), 1)
        card_gap = Inches(0.1)
        ch2 = (avail - card_gap * (n-1)) / n
        by = top

        for i, b in enumerate(bullets[:4]):
            bold_txt = b.get("bold", "")
            body_txt = b.get("text", "")
            self._bullet_card(slide, lx, by, lw, ch2, bold_txt, body_txt,
                              tag_colors[i % len(tag_colors)], i+1)
            by += ch2 + card_gap

    # ── LAYOUT 3: GRID — 2×2 COLORED CARDS (+ optional side image) ───────────
    def _lay_aesthetic_grid(self, d: dict, cur: int, total: int):
        slide = self._blank()
        self._header(slide, d.get("title", ""))
        self._progress(slide, cur, total)

        top   = Inches(0.86)
        avail = H - top - Inches(0.3)
        gap   = Inches(0.18)
        cards = d.get("cards", [])
        
        # Fallback if LLM generated "bullets" instead of "cards"
        if not cards and "bullets" in d:
            for i, b in enumerate(d["bullets"]):
                header = b.get("bold", b.get("header", f"Section {i+1}")) if isinstance(b, dict) else f"Section {i+1}"
                text = b.get("text", b.get("description", str(b))) if isinstance(b, dict) else str(b)
                cards.append({"header": header, "bullets": [text]})
                
        # Fix missing headers dynamically
        for i, c in enumerate(cards):
            if not c.get("header", ""):
                c["header"] = f"Module {i+1}"

        # Check if we have an image to show alongside
        img_path = _clean_image_path(d.get("image_path", ""))
        has_img = bool(img_path and Path(img_path).exists())

        if has_img:
            # 3 cards left + image right
            grid_w = (W - Inches(0.5)) * 0.55
            img_w  = (W - Inches(0.5)) * 0.42
            img_x  = Inches(0.25) + grid_w + gap
            self._premium_image_frame(slide, img_path, img_x, top, img_w, avail)
            n_cols, n_rows = 1, min(len(cards), 3)
            col_w = grid_w - Inches(0.04)
            row_h = (avail - gap*(n_rows-1)) / max(n_rows, 1)
            for i, c in enumerate(cards[:n_rows]):
                cy2 = top + i*(row_h + gap)
                cx2 = Inches(0.25)
                self._colored_card_full(slide, cx2, cy2, col_w, row_h, c,
                                        self.P["tag_colors"][i % 4])
        else:
            # Standard 2×2 grid
            n_cols, n_rows = 2, 2
            col_w = (W - Inches(0.5) - gap) / 2
            row_h = (avail - gap) / 2
            for i, c in enumerate(cards[:4]):
                ci, ri = i % n_cols, i // n_cols
                cx2 = Inches(0.25) + ci*(col_w + gap)
                cy2 = top + ri*(row_h + gap)
                self._colored_card_full(slide, cx2, cy2, col_w, row_h, c,
                                        self.P["tag_colors"][i % 4])

    def _colored_card_full(self, slide, l, t, w, h, card: dict, color: str):
        """Full grid card with ROUNDED corners: colored header band + numbered bullet list."""
        # Drop shadow
        _round(slide, l + Inches(0.08), t + Inches(0.08), w, h, fill=self.P["bg2"], line=None)
        # Card body — ROUNDED
        _round(slide, l, t, w, h, fill=self.P["card"], line=color, lw=1.8)
        # Header band
        hh = Inches(0.46)
        _round(slide, l, t, w, hh, fill=color, line=None)
        # Small white dot accent on header right
        _oval(slide, l + w - Inches(0.45), t + Inches(0.12), Inches(0.22), Inches(0.22),
              fill=self.P["card"], line=None)
        _tb(slide, card.get("header", "Module"), l + Inches(0.15), t + Inches(0.1),
            w - Inches(0.55), hh - Inches(0.14), sz=13, bold=True,
            col=self.P["bg"], align=PP_ALIGN.LEFT)

        # Bullet items with numbered tags
        bullets = card.get("bullets", [])
        if not bullets and "text" in card:
            bullets = [card["text"]]
        elif not bullets and "description" in card:
            bullets = [card["description"]]
        elif not bullets:
            bullets = ["(No detailed content provided)"]
        avail_h = h - hh - Inches(0.12)
        bsh = avail_h / max(len(bullets), 1)
        by = t + hh + Inches(0.08)
        for bi, b in enumerate(bullets[:4]):
            # Colored bullet number
            _oval(slide, l + Inches(0.12), by + Inches(0.08), Inches(0.22), Inches(0.22),
                  fill=color, line=None)
            _tb(slide, str(bi+1), l + Inches(0.12), by + Inches(0.09), Inches(0.22), Inches(0.2),
                sz=10, bold=True, col=self.P["bg"], align=PP_ALIGN.CENTER)
            _tb(slide, str(b), l + Inches(0.42), by + Inches(0.04), w - Inches(0.56),
                bsh - Inches(0.06), sz=12.5, col=self.P["text"])
            by += bsh

    # ── LAYOUT 4: FLOW — TOP CALLOUT + DOMINANT FULL-WIDTH IMAGE ─────────────
    def _lay_aesthetic_flow(self, d: dict, cur: int, total: int):
        slide = self._blank()
        self._header(slide, d.get("title", ""))
        self._progress(slide, cur, total)

        top   = Inches(0.86)
        avail = H - top - Inches(0.3)

        # Description callout card — ROUNDED with inner accent
        desc_h = Inches(1.5)
        _round(slide, Inches(0.25) + Inches(0.07), top + Inches(0.07), W - Inches(0.43), desc_h,
               fill=self.P["bg2"], line=None)  # shadow
        _round(slide, Inches(0.25), top, W - Inches(0.43), desc_h,
               fill=self.P["card"], line=self.P["border"], lw=1.8)
        # Left colored accent stripe
        _rect(slide, Inches(0.25), top + Inches(0.06), Inches(0.1), desc_h - Inches(0.12),
              fill=self.P["ac2"])
        # Quote icon
        _round(slide, Inches(0.44), top + Inches(0.1), Inches(0.35), Inches(0.35),
               fill=self.P["ac2"], line=None)
        _tb(slide, '"', Inches(0.46), top + Inches(0.09), Inches(0.33), Inches(0.33),
            sz=18, bold=True, col=self.P["bg"], align=PP_ALIGN.CENTER)
        desc_text = d.get("description", "")
        # Fallback if LLM generated "text" or "bullets" instead of "description"
        if not desc_text:
            desc_text = d.get("text", "")
        if not desc_text and "bullets" in d:
            desc_text = " ".join([b.get("text", str(b)) if isinstance(b, dict) else str(b) for b in d["bullets"]])
        if not desc_text and "nodes" in d:
            desc_text = " ".join([n.get("text", "") for n in d["nodes"]])
            
        _tb(slide, desc_text, Inches(0.94), top + Inches(0.12),
            W - Inches(1.3), desc_h - Inches(0.2), sz=14, col=self.P["text"])

        # DOMINANT visual — takes up 70% of slide height
        vt = top + desc_h + Inches(0.15)
        vh = H - vt - Inches(0.3)
        self._premium_image_frame(slide, d.get("image_path", ""), Inches(0.25), vt,
                                   W - Inches(0.43), vh, d.get("visual_suggestion", "[ Architecture ]"))

    # ── LAYOUT 5: TIMELINE ────────────────────────────────────────────────────
    def _lay_aesthetic_timeline(self, d: dict, cur: int, total: int):
        slide = self._blank()
        self._header(slide, d.get("title", ""))
        self._progress(slide, cur, total)

        nodes = d.get("nodes", [])
        if not nodes: return

        top   = Inches(0.9)
        avail = H - top - Inches(0.35)
        track_y = top + avail * 0.50

        # Track line
        _rect(slide, Inches(0.3), track_y - Inches(0.04),
              W - Inches(0.6), Inches(0.08), fill=self.P["border"])
        _rect(slide, Inches(0.3), track_y - Inches(0.02),
              W - Inches(0.6), Inches(0.04), fill=self.P["ac1"])

        nw = (W - Inches(0.6)) / max(len(nodes), 1)
        tag_cols = self.P["tag_colors"]

        for i, n in enumerate(nodes[:5]):
            ncx = Inches(0.3) + i * nw + nw / 2
            color = tag_cols[i % len(tag_cols)]

            # Node dot
            dot_r = Inches(0.22)
            _oval(slide, ncx - dot_r, track_y - dot_r, dot_r*2, dot_r*2,
                  fill=color, line=self.P["bg2"], lw=3.0)
            _oval(slide, ncx - dot_r*0.4, track_y - dot_r*0.4,
                  dot_r*0.8, dot_r*0.8, fill=self.P["bg"])

            # Card
            cw2 = nw - Inches(0.25)
            ch2 = avail * 0.42
            above = (i % 2 == 0)
            cy2 = track_y - ch2 - Inches(0.35) if above else track_y + Inches(0.38)

            # Connector line
            line_t = cy2 + ch2 if above else track_y + dot_r
            line_b = track_y - dot_r if above else cy2
            _rect(slide, ncx - Inches(0.03), min(line_t, line_b),
                  Inches(0.06), abs(line_b - line_t), fill=color)

            _round(slide, ncx - cw2/2 + Inches(0.07), cy2 + Inches(0.07), cw2, ch2,
                   fill=self.P["bg2"], line=None)
            _round(slide, ncx - cw2/2, cy2, cw2, ch2,
                   fill=self.P["card"], line=color, lw=1.8)
            _round(slide, ncx - cw2/2, cy2, cw2, Inches(0.14), fill=color)
            _tb(slide, n.get("header", "Phase"), ncx - cw2/2 + Inches(0.12),
                cy2 + Inches(0.16), cw2 - Inches(0.24), Inches(0.35),
                sz=12, bold=True, col=self.P["text"], align=PP_ALIGN.CENTER)
            
            # Use a slightly larger font and top align it to fill out the timeline card better
            _tb(slide, n.get("text", ""), ncx - cw2/2 + Inches(0.12),
                cy2 + Inches(0.45), cw2 - Inches(0.24), ch2 - Inches(0.55),
                sz=12.5, col=self.P["sub"], align=PP_ALIGN.LEFT)

    # ── LAYOUT 6: COMPARISON ──────────────────────────────────────────────────
    def _lay_aesthetic_comparison(self, d: dict, cur: int, total: int):
        slide = self._blank()
        self._header(slide, d.get("title", ""))
        self._progress(slide, cur, total)

        top   = Inches(0.86)
        avail = H - top - Inches(0.3)
        cw2   = (W - Inches(0.7)) / 2

        for si, (hk, bk, color) in enumerate([
            ("left_header",  "left_bullets",  self.P["ac1"]),
            ("right_header", "right_bullets", self.P["ac2"]),
        ]):
            sx = Inches(0.25) + si * (cw2 + Inches(0.2))
            # Shadow
            _round(slide, sx + Inches(0.08), top + Inches(0.08), cw2, avail,
                   fill=self.P["bg2"], line=None)
            # Card — ROUNDED
            _round(slide, sx, top, cw2, avail, fill=self.P["card"], line=color, lw=2.4)
            # Inner premium ring
            pad1 = Inches(0.06)
            _round(slide, sx + pad1, top + pad1, cw2 - 2*pad1, avail - 2*pad1, fill=None, line=self.P["border"], lw=0.8)
            
            # Header band — ROUNDED top only (simulate with overlapping round)
            _round(slide, sx, top, cw2, Inches(0.56), fill=color)
            # Ensure bottom of header is square
            _rect(slide, sx, top + Inches(0.28), cw2, Inches(0.28), fill=color)
            _tb(slide, d.get(hk, "Column"), sx + Inches(0.15), top + Inches(0.11),
                cw2 - Inches(0.3), Inches(0.4), sz=16, bold=True,
                col=self.P["bg"], align=PP_ALIGN.CENTER)

            # Bullets
            blist = d.get(bk, [])
            if not blist:
                prefix = "left_" if "left" in bk else "right_"
                alt = d.get(f"{prefix}text", d.get(f"{prefix}description", ""))
                if alt:
                    blist = [alt]
                else:
                    blist = ["(No detailed content provided)"]
                    
            bsh = (avail - Inches(0.65)) / max(len(blist), 1)
            by = top + Inches(0.58)
            for bi, b in enumerate(blist[:5]):
                # Subtle row stripe alternating
                if bi % 2 == 0:
                    _rect(slide, sx + Inches(0.1), by, cw2 - Inches(0.2), bsh,
                          fill=self.P["card2"], line=None)
                _rect(slide, sx + Inches(0.1), by, Inches(0.06), bsh, fill=color)
                _tb(slide, str(b), sx + Inches(0.25), by + Inches(0.06),
                    cw2 - Inches(0.4), bsh - Inches(0.1), sz=12.5, col=self.P["text"])
                by += bsh

        # VS badge centre
        vx = Inches(0.25) + cw2 + Inches(0.05)
        _round(slide, vx, top + avail/2 - Inches(0.5), Inches(0.1), Inches(1.0),
               fill=self.P["border"], line=None)
        _tb(slide, "VS", vx - Inches(0.06), top + avail/2 - Inches(0.22),
            Inches(0.22), Inches(0.45), sz=9, bold=True,
            col=self.P["text"], align=PP_ALIGN.CENTER)

    # ── LAYOUT 7: METRICS — KPI ROW + DOMINANT VISUAL ────────────────────────
    def _lay_aesthetic_metrics(self, d: dict, cur: int, total: int):
        slide = self._blank()
        self._header(slide, d.get("title", ""))
        self._progress(slide, cur, total)

        top     = Inches(0.86)
        metrics = d.get("metrics", [])
        n       = max(len(metrics[:4]), 1)
        gap     = Inches(0.18)
        mw      = (W - Inches(0.5) - gap*(n-1)) / n
        mh      = Inches(1.65)

        # KPI cards row — ROUNDED
        for i, m in enumerate(metrics[:4]):
            mx = Inches(0.25) + i*(mw + gap)
            color = self.P["tag_colors"][i % 4]
            # Shadow
            _round(slide, mx + Inches(0.07), top + Inches(0.07), mw, mh,
                   fill=self.P["bg2"], line=None)
            # Card
            _round(slide, mx, top, mw, mh, fill=self.P["card"], line=color, lw=2.2)
            # Top accent bar (rounded on top)
            _round(slide, mx, top, mw, Inches(0.14), fill=color)
            _rect(slide, mx, top + Inches(0.07), mw, Inches(0.07), fill=color)
            # Value
            _tb(slide, m.get("value", "—"), mx + Inches(0.1), top + Inches(0.22),
                mw - Inches(0.2), Inches(0.85), sz=38, bold=True,
                col=color, align=PP_ALIGN.CENTER)
            # Divider
            _rect(slide, mx + Inches(0.25), top + Inches(1.12), mw - Inches(0.5),
                  Inches(0.04), fill=color)
            # Label
            _tb(slide, m.get("label", ""), mx + Inches(0.12), top + Inches(1.2),
                mw - Inches(0.24), Inches(0.42), sz=9.5, col=self.P["sub"],
                align=PP_ALIGN.CENTER)

        # Dominant visual below (60%+ of slide)
        vt = top + mh + Inches(0.18)
        vh = H - vt - Inches(0.3)
        desc_fallback = d.get("description", d.get("text", ""))
        fallback_text = desc_fallback if desc_fallback else d.get("visual_suggestion", "[ Detailed Metric Analysis ]")
        self._premium_image_frame(slide, d.get("image_path", ""), Inches(0.25), vt,
                                   W - Inches(0.43), vh, fallback_text)

    # ── LAYOUT 8: PITCH (DENSE GRID + VISUAL) ───────────────────────────────
    def _lay_aesthetic_pitch(self, d: dict, cur: int, total: int):
        slide = self._blank()
        self._header(slide, d.get("title", ""))
        self._progress(slide, cur, total)

        top = Inches(0.86)
        avail = H - top - Inches(0.3)
        
        # Top half: 4 dense grid cards
        top_h = Inches(2.3) # Increased from 1.3 to fit 40-60 words!
        cards = d.get("cards", [])
        if not cards and "bullets" in d:
            for i, b in enumerate(d["bullets"]):
                header = b.get("bold", b.get("header", f"Step {i+1}")) if isinstance(b, dict) else f"Step {i+1}"
                text = b.get("text", b.get("description", str(b))) if isinstance(b, dict) else str(b)
                cards.append({"header": header, "bullets": [text]})
        
        # Fix missing headers dynamically
        for i, c in enumerate(cards):
            if not c.get("header", ""):
                c["header"] = f"Module {i+1}"
                
        num_cards = max(len(cards[:4]), 1)
        total_gap = Inches(0.15) * (num_cards - 1)
        cw = (W - Inches(0.5) - total_gap) / num_cards
        
        for i, c in enumerate(cards[:4]):
            cx = Inches(0.25) + i*(cw + Inches(0.15))
            self._colored_card_full(slide, cx, top, cw, top_h, c, self.P["tag_colors"][i % 4])

        # Bottom half: Left image, Right bullets
        bot_t = top + top_h + Inches(0.2)
        bot_h = avail - top_h - Inches(0.2)
        
        # Left image (55% width)
        lw = (W - Inches(0.7)) * 0.55
        desc_fallback = d.get("description", d.get("text", ""))
        fallback_text = desc_fallback if desc_fallback else d.get("visual_suggestion", "[ Flowchart / Architecture ]")
        self._premium_image_frame(slide, d.get("image_path", ""), Inches(0.25), bot_t, lw, bot_h, fallback_text)
        
        # Right bullets (45% width)
        rx = Inches(0.25) + lw + Inches(0.2)
        rw = (W - Inches(0.7)) * 0.45
        
        bullets = d.get("right_bullets", d.get("bottom_bullets", []))
        if not bullets and "description" in d: bullets = [{"text": d["description"]}]
        elif not bullets: bullets = [{"text": "(No detailed content provided)"}]
        
        # Internal bullets
        by = bot_t
        # Cap bullet height so 1 bullet doesn't stretch 3.5 inches tall
        bh = min(bot_h / max(len(bullets), 1), Inches(0.85))
        
        for i, b in enumerate(bullets[:6]):
            bold = b.get("bold", b.get("header", f"Point {i+1}")) if isinstance(b, dict) else f"Point {i+1}"
            txt = b.get("text", b.get("description", str(b))) if isinstance(b, dict) else str(b)
            self._bullet_card(slide, rx, by, rw, bh - Inches(0.1), bold, txt, self.P["tag_colors"][i%4], i+1)
            by += bh

# ─── API ───────────────────────────────────────────────────────────────────────
def ppt_create(prompt: str, style: str = None, output_path: str = None):
    yield "Groq generating presentation...\n"
    raw = _groq_call(_SYS, _USR.format(prompt=prompt))
    plan = _parse(raw)
    if style and style in PERSONALITIES:
        plan["personality"] = style
    out = output_path or str(Path.home()/"Desktop"/f"Aesthetic_Deck_{int(time.time())}.pptx")
    b = PresentationBuilder(plan, out)
    for s in b.build_with_progress(): yield s + "\n"
    yield f"Saved to: `{out}`\n"

def ppt_styles():
    return {"styles": {k: {"name": v["name"], "desc": v["desc"]} for k, v in PERSONALITIES.items()},
            "count": len(PERSONALITIES)}

def _pick(p): return "ocean_pro"
