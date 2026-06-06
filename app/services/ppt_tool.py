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

def _parse_bullet(b) -> tuple:
    """Safely parse any bullet item into (bold_text, body_text).
    Handles: proper dicts, single-quoted dict strings, plain strings."""
    if isinstance(b, dict):
        return b.get("bold", ""), b.get("text", b.get("description", ""))
    if isinstance(b, str):
        s = b.strip()
        # Handle Python-style single-quoted dicts: {'bold': '...', 'text': '...'}
        if s.startswith("{") and "'bold'" in s:
            try:
                # Convert single-quote dict repr to valid JSON
                import ast
                d = ast.literal_eval(s)
                if isinstance(d, dict):
                    return d.get("bold", ""), d.get("text", d.get("description", ""))
            except Exception:
                pass
        # Try JSON parse in case it has double quotes
        if s.startswith("{"):
            try:
                d = json.loads(s)
                if isinstance(d, dict):
                    return d.get("bold", ""), d.get("text", d.get("description", ""))
            except Exception:
                pass
        return "", s
    return "", str(b)

def _parse_card(c) -> dict:
    """Safely parse a card item into a dict with 'header' and 'bullets'."""
    if isinstance(c, dict):
        return c
    if isinstance(c, str):
        s = c.strip()
        if s.startswith("{"):
            try:
                import ast
                d = ast.literal_eval(s)
                if isinstance(d, dict): return d
            except Exception:
                pass
            try:
                d = json.loads(s)
                if isinstance(d, dict): return d
            except Exception:
                pass
        return {"header": "Note", "bullets": [s]}
    return {"header": "Note", "bullets": [str(c)]}

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
_SYS_OUTLINE = """\
You are an elite presentation generator. Create a structural outline.
Output ONLY valid JSON — no markdown fences, no explanation."""

_USR_OUTLINE = """\
Create a VISUAL-FIRST presentation outline for:
TOPIC/REQUEST: {prompt}

RULES:
- Outline 8 to 12 slides. First slide MUST use "aesthetic_title".
- Use a mix of layouts: "aesthetic_split", "aesthetic_grid", "aesthetic_flow", "aesthetic_timeline", "aesthetic_comparison", "aesthetic_metrics", "aesthetic_pitch".
- You MUST use AT LEAST 5 different layouts in the presentation.
- DO NOT use the exact same layout for two consecutive slides (e.g., do not put two 'aesthetic_grid' slides back-to-back).
- COLORS: If the user requests ANY specific color or theme (e.g. "cyan", "red", "maroon"), DO NOT rely on presets. You MUST output a "custom_theme" object with 6-character hex codes (NO hash) that PERFECTLY matches their request. Set "ac1", "ac2", "ac3", "border", "hdr_bg", and "bar" to the requested colors.
- Output ONLY valid JSON.

JSON SCHEMA:
{{
  "presentation_title": "...",
  "personality": "ocean_pro",
  "custom_theme": {{"bg": "400000", "bg2": "4A0000", "card": "550000", "card2": "600000", "text": "FFFFFF", "sub": "DDDDDD", "ac1": "FFD700", "ac2": "FFAA00", "ac3": "FFFF00", "border": "FFD700", "hdr_bg": "FFD700", "hdr_text": "400000", "bar": "FFD700"}},
  "slides": [
    {{
      "slide_number": 1,
      "layout": "aesthetic_title",
      "title": "Topic Name"
    }},
    {{
      "slide_number": 2,
      "layout": "aesthetic_split",
      "title": "Problem Statement"
    }}
  ]
}}"""

_SYS_CHUNK = """\
You are an elite presentation generator. Generate highly dense content for specific slides based on the provided outline.
Output ONLY valid JSON — no markdown fences, no explanation."""

_USR_CHUNK = """TOPIC: {prompt}
PRESENTATION OUTLINE: {outline}

Generate the FULL, EXTREMELY DENSE CONTENT for slides {start_idx} to {end_idx}.
Return a JSON object with a "slides" array containing ONLY those slides, fully populated.
The layout for each slide MUST exactly match what is in the outline.

ABSOLUTE RULES:
1. bullets/left_bullets/right_bullets/nodes/cards MUST be JSON arrays of OBJECTS with double-quote keys.
   NEVER output items as plain strings like {{'bold': 'x', 'text': 'y'}} -- always use double quotes.
2. Each bullet: "bold" = 2-5 word sub-header. "text" = 25-35 words of detailed, informative content.
3. Every slide MUST include "visual_suggestion" describing a specific chart, diagram, or infographic.

LAYOUT SCHEMAS:
- aesthetic_split/aesthetic_pitch/aesthetic_flow: "bullets": [{{"bold":"...", "text":"..."}}] (3-4 bullets)
- aesthetic_grid: "cards": [{{"header":"Card Title", "bullets":["detailed sentence 1", "detailed sentence 2"]}}] (4 cards)
- aesthetic_timeline: "nodes": [{{"header":"Phase Name", "text":"25-35 word description"}}] (4-5 nodes)
- aesthetic_metrics: "metrics": [{{"value":"94%", "label":"Satisfaction Rate"}}] (3-4 metrics)
- aesthetic_comparison: "left_header":"...", "right_header":"...", "left_bullets":[...], "right_bullets":[...]

EXAMPLE OUTPUT for aesthetic_split:
{{"slides": [{{"slide_number": 2, "layout": "aesthetic_split", "title": "Early Life",
  "visual_suggestion": "Timeline diagram with key early life milestones",
  "bullets": [
    {{"bold": "Born 1947 Varanasi", "text": "Pandit Jagdish Mohan was born in the ancient scholarly city of Varanasi in 1947, immersed from childhood in Sanskrit traditions and Vedic philosophy that shaped his entire career."}},
    {{"bold": "University Education", "text": "He studied Sanskrit literature at Banaras Hindu University, earning his degree with distinction and receiving the Chancellor Gold Medal for academic excellence."}},
    {{"bold": "Mentor Influence", "text": "Guided by the legendary Dr. Ramachandra Shukla, he developed rigorous analytical skills in classical Indian philosophy, blending traditional wisdom with modern interdisciplinary methods."}}
  ]
}}]}}"""



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
            # Apply ALL colors directly from the LLM's custom_theme.
            # Only fall back for fields the LLM did not provide.
            def _sh(val, fallback):
                """Safe hex: strip # and validate 6 chars, else return fallback."""
                if isinstance(val, str):
                    v = val.lstrip("#")
                    if len(v) == 6:
                        return v
                return fallback

            bg_hex = _sh(custom.get("bg"), "F5F0E8")
            try:
                rv, gv, bv = int(bg_hex[0:2],16), int(bg_hex[2:4],16), int(bg_hex[4:6],16)
                lum = (0.299*rv + 0.587*gv + 0.114*bv) / 255
            except:
                lum = 0.5
            is_light = lum > 0.5

            # Smart defaults based on light/dark detection
            def_text  = "222222" if is_light else "F5F5F5"
            def_sub   = "555555" if is_light else "B0B0C0"
            def_bg2   = "EDE8DC" if is_light else "121218"
            def_card  = "FAF6EE" if is_light else "1A1A22"
            def_card2 = "EDE8DC" if is_light else "22222C"
            def_hdrt  = "222222" if is_light else "FFFFFF"
            def_ac1   = "C8A96E" if is_light else "FFD700"
            def_ac2   = "A07840" if is_light else "FF8800"
            def_ac3   = "8B6530" if is_light else "00C8FF"

            self.P["bg"]       = bg_hex
            self.P["bg2"]      = _sh(custom.get("bg2"),      def_bg2)
            self.P["card"]     = _sh(custom.get("card"),     def_card)
            self.P["card2"]    = _sh(custom.get("card2"),    def_card2)
            self.P["text"]     = _sh(custom.get("text"),     def_text)
            self.P["sub"]      = _sh(custom.get("sub"),      def_sub)
            self.P["hdr_text"] = _sh(custom.get("hdr_text"), def_hdrt)

            ac1 = _sh(custom.get("ac1"), def_ac1)
            ac2 = _sh(custom.get("ac2"), def_ac2)
            ac3 = _sh(custom.get("ac3"), def_ac3)
            self.P["ac1"]    = ac1
            self.P["ac2"]    = ac2
            self.P["ac3"]    = ac3
            self.P["border"] = _sh(custom.get("border"), ac1)
            self.P["hdr_bg"] = _sh(custom.get("hdr_bg"), ac1)
            self.P["bar"]    = _sh(custom.get("bar"),    ac2)
            tc = custom.get("tag_colors", [])
            self.P["tag_colors"] = [
                _sh(tc[0] if len(tc)>0 else None, ac1),
                _sh(tc[1] if len(tc)>1 else None, ac2),
                _sh(tc[2] if len(tc)>2 else None, ac3),
                _sh(tc[3] if len(tc)>3 else None, "888888"),
            ]

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
        """Clean, minimalist centered pill title box."""
        tw, th = W * 0.65, Inches(0.65)
        tx, ty = (W - tw) / 2, Inches(0.15)
        
        # Single ultra-clean pill
        _round(slide, tx, ty, tw, th, fill=self.P["card"], line=self.P["border"], lw=1.5)
        
        # Text centered perfectly
        _tb(slide, title.upper(), tx, ty + Inches(0.08), tw, th - Inches(0.16),
            sz=22, bold=True, col=self.P["text"], align=PP_ALIGN.CENTER)

    def _premium_image_frame(self, slide, path: str, l, t, w, h, suggestion: str = ""):
        """Clean single-border rounded container for images."""
        # Main outer container
        _round(slide, l, t, w, h, fill=self.P["card"], line=self.P["border"], lw=1.5)

        # High-tech top-right dots
        for di in range(3):
            _oval(slide, l + w - Inches(0.6) + di * Inches(0.16), t + Inches(0.15),
                  Inches(0.08), Inches(0.08), fill=[self.P["ac1"], self.P["ac2"], self.P["ac3"]][di], line=None)

        # Embed image or placeholder
        pad = Inches(0.1)
        clean = _clean_image_path(path) if path else ""
        if clean and Path(clean).exists():
            try:
                pic = slide.shapes.add_picture(clean, l + pad, t + pad, w - 2*pad, h - 2*pad)
                pic.auto_shape_type = MSO_SHAPE.ROUNDED_RECTANGLE
                pic.line.fill.background()
                return
            except Exception as e:
                print(f"[ppt] image error: {e}")
                
        # Aesthetic placeholder
        _tb(slide, suggestion or "[ Detailed Visual ]",
            l + Inches(0.2), t + Inches(0.2), w - Inches(0.4), h - Inches(0.4),
            sz=14, italic=False, col=self.P["sub"], align=PP_ALIGN.CENTER)

    def _bullet_card(self, slide, l, t, w, h, bold_txt: str, body_txt: str,
                     tag_col: str, idx: int):
        """Clean minimalist bullet card."""
        # Main curved body
        _round(slide, l, t, w, h, fill=self.P["card"], line=tag_col, lw=1.5)

        # Number badge circle
        _oval(slide, l + Inches(0.15), t + Inches(0.12), Inches(0.25), Inches(0.25),
              fill=tag_col, line=None)
        _tb(slide, str(idx), l + Inches(0.15), t + Inches(0.12), Inches(0.25), Inches(0.23),
            sz=10, bold=True, col=self.P["bg"], align=PP_ALIGN.CENTER)

        # Bold sub-header
        if bold_txt:
            _tb(slide, bold_txt, l + Inches(0.5), t + Inches(0.1), w - Inches(0.6),
                Inches(0.3), sz=12, bold=True, col=tag_col)
                
        # Body text spacing
        body_top = t + Inches(0.35) if bold_txt else t + Inches(0.14)
        _tb(slide, body_txt, l + Inches(0.5), body_top, w - Inches(0.6),
            h - (Inches(0.4) if bold_txt else Inches(0.22)),
            sz=11, col=self.P["text"])

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
            bold_txt, body_txt = _parse_bullet(b)
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
                bold, text = _parse_bullet(b)
                header = bold if bold else (f"Section {i+1}")
                cards.append({"header": header, "bullets": [text] if text else ["(No content)"]})
        
        # Parse any string-cards into dicts
        cards = [_parse_card(c) for c in cards]
                
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
        """Clean full grid card without messy overlapping header bands."""
        # Card body — single clean border
        _round(slide, l, t, w, h, fill=self.P["card"], line=color, lw=1.5)

        # Header Text
        hh = Inches(0.4)
        _tb(slide, card.get("header", "Module").upper(), l + Inches(0.15), t + Inches(0.1),
            w - Inches(0.3), hh, sz=12, bold=True,
            col=color, align=PP_ALIGN.LEFT)
            
        # Accent rule under header
        _rect(slide, l + Inches(0.15), t + Inches(0.42), w - Inches(0.3), Inches(0.02), fill=color)

        # High-tech header accent dot
        _oval(slide, l + w - Inches(0.3), t + Inches(0.15), Inches(0.15), Inches(0.15),
              fill=color, line=None)

        # Bullet items with sleek badges
        bullets = card.get("bullets", [])
        if not bullets and "text" in card:
            bullets = [card["text"]]
        elif not bullets and "description" in card:
            bullets = [card["description"]]
        elif not bullets:
            bullets = ["(No detailed content provided)"]
            
        avail_h = h - hh - Inches(0.15)
        bsh = avail_h / max(len(bullets), 1)
        by = t + hh + Inches(0.1)
        
        for bi, b in enumerate(bullets[:5]):
            bold_part, text_part = _parse_bullet(b)
            display = text_part if text_part else (bold_part if bold_part else str(b))
            # Colored bullet number
            _oval(slide, l + Inches(0.15), by + Inches(0.06), Inches(0.2), Inches(0.2),
                  fill=color, line=None)
            _tb(slide, str(bi+1), l + Inches(0.15), by + Inches(0.07), Inches(0.2), Inches(0.18),
                sz=9, bold=True, col=self.P["bg"], align=PP_ALIGN.CENTER)
            _tb(slide, display, l + Inches(0.42), by + Inches(0.02), w - Inches(0.55),
                bsh - Inches(0.04), sz=11.5, col=self.P["text"])
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
            parts = []
            for b in d["bullets"]:
                _, txt = _parse_bullet(b)
                parts.append(txt)
            desc_text = " ".join(parts)
        if not desc_text and "nodes" in d:
            desc_text = " ".join([n.get("text", "") if isinstance(n, dict) else str(n) for n in d["nodes"]])
            
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

            # Clean Single Card
            _round(slide, ncx - cw2/2, cy2, cw2, ch2,
                   fill=self.P["card"], line=color, lw=1.5)
            
            # Text formatting
            _tb(slide, n.get("header", "Phase").upper(), ncx - cw2/2 + Inches(0.12),
                cy2 + Inches(0.08), cw2 - Inches(0.24), Inches(0.35),
                sz=12, bold=True, col=color, align=PP_ALIGN.CENTER)
            
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
            # Card — Clean single curve
            _round(slide, sx, top, cw2, avail, fill=self.P["card"], line=color, lw=1.5)
            
            # Header line
            _tb(slide, d.get(hk, "Column").upper(), sx + Inches(0.15), top + Inches(0.11),
                cw2 - Inches(0.3), Inches(0.4), sz=14, bold=True,
                col=color, align=PP_ALIGN.CENTER)
            
            # Divider
            _rect(slide, sx + Inches(0.3), top + Inches(0.48), cw2 - Inches(0.6), Inches(0.02), fill=color)

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
                bold, txt = _parse_bullet(b)
                
                # Accent bar
                _rect(slide, sx + Inches(0.15), by + Inches(0.1), Inches(0.05), bsh - Inches(0.2), fill=color)
                # Bold sub-header
                if bold:
                    _tb(slide, bold.upper(), sx + Inches(0.3), by + Inches(0.08),
                        cw2 - Inches(0.45), Inches(0.3), sz=10.5, bold=True, col=color)
                    _tb(slide, txt, sx + Inches(0.3), by + Inches(0.3),
                        cw2 - Inches(0.45), bsh - Inches(0.36), sz=11, col=self.P["text"])
                else:
                    _tb(slide, txt, sx + Inches(0.3), by + Inches(0.08),
                        cw2 - Inches(0.45), bsh - Inches(0.16), sz=11.5, col=self.P["text"])
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
            # Card - Clean Single Curve
            _round(slide, mx, top, mw, mh, fill=self.P["card"], line=color, lw=1.5)
            
            # Value
            _tb(slide, m.get("value", "—"), mx + Inches(0.1), top + Inches(0.15),
                mw - Inches(0.2), Inches(0.85), sz=34, bold=True,
                col=color, align=PP_ALIGN.CENTER)
            # Divider
            _rect(slide, mx + Inches(0.25), top + Inches(1.0), mw - Inches(0.5),
                  Inches(0.02), fill=color)
            # Label
            _tb(slide, m.get("label", ""), mx + Inches(0.12), top + Inches(1.2),
                mw - Inches(0.24), Inches(0.42), sz=9.5, col=self.P["sub"],
                align=PP_ALIGN.CENTER)

        # Dominant visual below (60%+ of slide)
        vt = top + mh + Inches(0.18)
        vh = H - vt - Inches(0.3)
        desc_fallback = d.get("description", d.get("text", ""))
        if not desc_fallback and "metrics" in d:
            desc_fallback = " ".join([m.get("label", "") if isinstance(m, dict) else str(m) for m in d["metrics"]])
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
                bold, text = _parse_bullet(b)
                header = bold if bold else f"Step {i+1}"
                cards.append({"header": header, "bullets": [text] if text else ["(No content)"]})
        
        # Parse any string-cards into dicts
        cards = [_parse_card(c) for c in cards]
        
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
        if not bullets and "description" in d: bullets = [{"bold": "", "text": d["description"]}]
        elif not bullets: bullets = [{"bold": "", "text": "(No detailed content provided)"}]
        
        # Internal bullets
        by = bot_t
        # Cap bullet height so 1 bullet doesn't stretch 3.5 inches tall
        bh = min(bot_h / max(len(bullets), 1), Inches(0.85))
        
        for i, b in enumerate(bullets[:6]):
            bold, txt = _parse_bullet(b)
            if not bold:
                bold = f"Point {i+1}"
            self._bullet_card(slide, rx, by, rw, bh - Inches(0.1), bold, txt, self.P["tag_colors"][i%4], i+1)
            by += bh

def _normalize_and_recover(chunk_data, outline_chunk):
    """Silently maps hallucinated content arrays to the expected keys and supplies fallbacks so no slide is ever blank."""
    if not isinstance(chunk_data, dict): return
    slides = chunk_data.get("slides", [])
        
    for i, s in enumerate(slides):
        expected_lay = outline_chunk[i].get("layout", "aesthetic_split") if i < len(outline_chunk) else "aesthetic_split"
        lay = s.get("layout", expected_lay)
        
        # 1. Force valid layout (handles Phase 1 Outline hallucinating layout names)
        if lay not in ["aesthetic_split", "aesthetic_pitch", "aesthetic_flow", "aesthetic_grid", "aesthetic_timeline", "aesthetic_metrics", "aesthetic_comparison", "aesthetic_title"]:
            lay = "aesthetic_split"
        s["layout"] = lay
            
        # 2. Aggressive Data Recovery
        alt = s.get("bullets") or s.get("cards") or s.get("nodes") or s.get("points") or s.get("items") or s.get("content") or s.get("metrics") or []
        if isinstance(alt, str): alt = [{"bold": "Note", "text": alt}]
        
        if lay in ["aesthetic_split", "aesthetic_pitch", "aesthetic_flow"]:
            if not s.get("bullets"): s["bullets"] = alt if alt else [{"bold": "Auto-Recovered", "text": "The generation failed to produce detailed content for this section."}]
        elif lay == "aesthetic_grid":
            if not s.get("cards"): s["cards"] = alt if alt else [{"header": "Auto-Recovered", "bullets": ["Content missing"]}]
        elif lay == "aesthetic_timeline":
            if not s.get("nodes"): s["nodes"] = alt if alt else [{"header": "Auto-Recovered", "text": "Content missing"}]
        elif lay == "aesthetic_metrics":
            if not s.get("metrics"): s["metrics"] = alt if alt else [{"value": "-", "label": "Auto-Recovered"}]
        elif lay == "aesthetic_comparison":
            if not s.get("left_bullets"): s["left_bullets"] = alt if alt else [{"bold": "Left", "text": "Auto-Recovered"}]
            if not s.get("right_bullets"): s["right_bullets"] = [{"bold": "Right", "text": "Auto-Recovered"}]

def ppt_create(prompt: str, style: str = None, output_path: str = None):
    yield "🤖 Generating Presentation Outline...\n"
    raw_outline = _groq_call(_SYS_OUTLINE, _USR_OUTLINE.format(prompt=prompt))
    plan = _parse(raw_outline)
    
    if style and style in PERSONALITIES:
        plan["personality"] = style
        
    slides_outline = plan.get("slides", [])
    total_slides = len(slides_outline)
    yield f"📋 Outline created: {total_slides} slides planned.\n"
    
    full_slides = []
    
    # Chunk generation (2 slides at a time to prevent hallucination)
    chunk_size = 2
    outline_str = json.dumps([{"slide_number": s.get("slide_number"), "title": s.get("title"), "layout": s.get("layout")} for s in slides_outline])

    for i in range(0, total_slides, chunk_size):
        chunk = slides_outline[i:i+chunk_size]
        start_idx = chunk[0].get('slide_number', i+1)
        end_idx = chunk[-1].get('slide_number', i+len(chunk))
        
        yield f"✍️ Generating extremely dense content for Slides {start_idx}-{end_idx}...\n"
        
        chunk_slides = []
        last_err = None
        for attempt in range(2):  # Try up to 2 times silently
            try:
                raw_chunk = _groq_call(
                    _SYS_CHUNK,
                    _USR_CHUNK.format(prompt=prompt, outline=outline_str, start_idx=start_idx, end_idx=end_idx)
                )
                chunk_data = _parse(raw_chunk)
                _normalize_and_recover(chunk_data, chunk)
                chunk_slides = chunk_data.get("slides", [])
                if chunk_slides:
                    break  # Success — stop retrying
                last_err = ValueError("No slides in response.")
            except Exception as e:
                last_err = e
                # Brief pause before retry to avoid rate-limit cascade
                import time as _t; _t.sleep(1.5)

        if chunk_slides:
            full_slides.extend(chunk_slides)
        else:
            yield f"⚠️ Chunk {start_idx}-{end_idx} failed after 2 attempts ({last_err}). Using fallback.\n"
            for c in chunk:
                full_slides.append({
                    "title": c.get("title", "Slide"),
                    "layout": "aesthetic_split",
                    "bullets": [{"bold": c.get("title", "Note"), "text": "Content could not be generated for this slide. Please try regenerating the presentation."}]
                })
    yield "🎨 Content generated! Building PPTX with precision curves...\n"
    
    # ── CRITICAL: Write the fully-populated slides back into the plan ──
    plan["slides"] = full_slides
    
    out = output_path or str(Path.home()/"Desktop"/f"Aesthetic_Deck_{int(time.time())}.pptx")
    b = PresentationBuilder(plan, out)
    for s in b.build_with_progress(): yield s + "\n"
    yield f"✅ Saved to: `{out}`\n"

def ppt_styles():
    return {"styles": {k: {"name": v["name"], "desc": v["desc"]} for k, v in PERSONALITIES.items()},
            "count": len(PERSONALITIES)}

def _pick(p): return "ocean_pro"
