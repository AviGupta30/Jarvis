"""
resume_builder.py — Resume Creator

Upload a picture of any resume → Jarvis reads its DESIGN (layout, colours, header shape, photo, heading
style, skill graphic, section order) with the Groq vision model, structures the user's own details with
the LLM, and renders a print-ready A4 resume (PDF + PNG preview + editable HTML) in that design.
Without an image it uses one of the fixed preset formats (elegant, modern, minimal, creative, executive, tech).

Flow: detect_resume_request(prompt) → create_resume(...) generator
  design  = preset  ←  vision spec of the reference image  ←  template / colour overrides
  content = LLM(details) → normalised JSON   (edit mode: LLM(old JSON + instruction))
  HTML (fixed CSS formats) → Playwright Chromium page.pdf → PyMuPDF PNG previews
State (last design/content, "waiting for details") lives in app/memory/resume_state.json.
"""
from __future__ import annotations

import base64
import html as _html
import json
import os
import re
import time

from app.core.config import settings

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_DIR = os.path.join(_BASE_DIR, "data", "uploads", "resumes")          # served at /media/resumes/
STATE_PATH = os.path.join(_BASE_DIR, "app", "memory", "resume_state.json")
MEDIA_URL = "http://127.0.0.1:8000/media/resumes"
_TEXT_MODEL = "openai/gpt-oss-120b"
_TEXT_MODEL_FALLBACK = "openai/gpt-oss-20b"
_IMG_EXTS = (".png", ".jpg", ".jpeg", ".webp", ".bmp")
_AWAIT_TTL = 30 * 60   # seconds a "send me your details" prompt stays open

SECTION_KEYS = ["profile", "highlights", "contact", "skills", "competencies", "experience", "education",
                "achievements", "certifications", "languages", "interests", "projects", "references"]
DEFAULT_TITLES = {
    "profile": "Profile", "highlights": "Career Highlights", "contact": "Contact", "skills": "Skills",
    "competencies": "Core Competencies", "experience": "Work Experience", "education": "Education",
    "achievements": "Achievements", "certifications": "Certifications", "languages": "Languages",
    "interests": "Interests", "projects": "Projects", "references": "References",
}
_SIDEBAR_FRIENDLY = {"profile", "highlights", "contact", "education", "achievements", "certifications",
                     "languages", "interests", "references", "skills"}

# ── Fixed formats ───────────────────────────────────────────────────────────────────────────────
PRESETS: dict[str, dict] = {
    "elegant": {
        "layout": "sidebar_left", "sidebar_width": 32, "header": "diagonal_banner", "photo": "square",
        "font": "sans", "name_case": "upper", "heading_style": "underline", "skills_style": "venn",
        "competency_style": "icon_grid", "timeline": True,
        "colors": {"primary": "#c4a574", "accent": "#8b6c47", "heading": "#8b6c47", "text": "#3d3d3d",
                   "sidebar_bg": "#f3f1ec", "page_bg": "#ffffff", "header_text": "#ffffff",
                   "skill_colors": ["#d9a7a7", "#9c7b5e", "#a3bfe3"]},
        "sidebar_sections": ["profile", "highlights", "contact", "achievements", "education", "languages", "interests"],
        "main_sections": ["skills", "competencies", "experience", "projects", "certifications", "references"],
    },
    "modern": {
        "layout": "sidebar_left", "sidebar_width": 33, "header": "sidebar_name", "photo": "circle",
        "font": "modern", "name_case": "upper", "heading_style": "bar_left", "skills_style": "bars",
        "competency_style": "icon_grid", "timeline": True,
        "colors": {"primary": "#2563eb", "accent": "#2563eb", "heading": "#1e293b", "text": "#334155",
                   "sidebar_bg": "#1f2a44", "page_bg": "#ffffff", "header_text": "#ffffff",
                   "skill_colors": ["#60a5fa", "#2563eb", "#93c5fd"]},
        "sidebar_sections": ["contact", "skills", "languages", "education", "interests"],
        "main_sections": ["profile", "experience", "competencies", "projects", "achievements", "certifications", "highlights", "references"],
    },
    "minimal": {
        "layout": "single_column", "sidebar_width": 0, "header": "centered", "photo": "none",
        "font": "serif", "name_case": "title", "heading_style": "caps_line", "skills_style": "chips",
        "competency_style": "list", "timeline": False,
        "colors": {"primary": "#111827", "accent": "#6b7280", "heading": "#111827", "text": "#374151",
                   "sidebar_bg": "#ffffff", "page_bg": "#ffffff", "header_text": "#111827",
                   "skill_colors": ["#9ca3af", "#4b5563", "#d1d5db"]},
        "sidebar_sections": [],
        "main_sections": ["profile", "experience", "skills", "competencies", "education", "projects", "achievements",
                          "certifications", "highlights", "languages", "interests", "references", "contact"],
    },
    "creative": {
        "layout": "sidebar_right", "sidebar_width": 33, "header": "full_band", "photo": "circle",
        "font": "geometric", "name_case": "upper", "heading_style": "boxed", "skills_style": "dots",
        "competency_style": "icon_grid", "timeline": True,
        "colors": {"primary": "#0f766e", "accent": "#f97316", "heading": "#0f766e", "text": "#334155",
                   "sidebar_bg": "#f0fdfa", "page_bg": "#ffffff", "header_text": "#ffffff",
                   "skill_colors": ["#f97316", "#0f766e", "#5eead4"]},
        "sidebar_sections": ["contact", "skills", "languages", "achievements", "certifications", "interests"],
        "main_sections": ["profile", "experience", "competencies", "projects", "education", "highlights", "references"],
    },
    "executive": {
        "layout": "sidebar_right", "sidebar_width": 31, "header": "full_band", "photo": "rounded",
        "font": "elegant", "name_case": "upper", "heading_style": "underline", "skills_style": "circles",
        "competency_style": "icon_grid", "timeline": True,
        "colors": {"primary": "#1f2937", "accent": "#b8913a", "heading": "#1f2937", "text": "#374151",
                   "sidebar_bg": "#f7f4ec", "page_bg": "#ffffff", "header_text": "#f5e6b8",
                   "skill_colors": ["#b8913a", "#1f2937", "#d6c08a"]},
        "sidebar_sections": ["contact", "skills", "education", "achievements", "certifications", "languages"],
        "main_sections": ["profile", "highlights", "experience", "competencies", "projects", "interests", "references"],
    },
    "tech": {
        "layout": "sidebar_left", "sidebar_width": 31, "header": "left_plain", "photo": "none",
        "font": "mono", "name_case": "title", "heading_style": "caps_line", "skills_style": "bars",
        "competency_style": "list", "timeline": True,
        "colors": {"primary": "#0891b2", "accent": "#0891b2", "heading": "#0f172a", "text": "#334155",
                   "sidebar_bg": "#0f172a", "page_bg": "#ffffff", "header_text": "#0f172a",
                   "skill_colors": ["#22d3ee", "#0891b2", "#67e8f9"]},
        "sidebar_sections": ["contact", "skills", "languages", "certifications", "interests", "education"],
        "main_sections": ["profile", "experience", "projects", "competencies", "achievements", "highlights", "references"],
    },
}
PRESET_BLURBS = {
    "elegant": "gold diagonal banner + photo, light sidebar, Venn skills, icon competencies",
    "modern": "dark navy sidebar with photo & name, skill bars, clean timeline",
    "minimal": "single column, serif, centred name, ATS-friendly",
    "creative": "teal header band, coral accents, right sidebar, skill dots",
    "executive": "charcoal & gold, rounded photo, skill rings",
    "tech": "monospace headings, dark sidebar, skill bars",
}

_FONTS = {
    "sans":      ("'Roboto', 'Segoe UI', Arial, sans-serif", "'Roboto', 'Segoe UI', Arial, sans-serif", "Roboto:wght@300;400;500;700;900"),
    "geometric": ("'Montserrat', 'Segoe UI', Arial, sans-serif", "'Open Sans', 'Segoe UI', Arial, sans-serif", "Montserrat:wght@400;600;700;800&family=Open+Sans:wght@400;600;700"),
    "modern":    ("'Poppins', 'Segoe UI', Arial, sans-serif", "'Poppins', 'Segoe UI', Arial, sans-serif", "Poppins:wght@300;400;500;600;700"),
    "serif":     ("'Playfair Display', Georgia, serif", "'Lora', Georgia, serif", "Playfair+Display:wght@500;700&family=Lora:wght@400;600"),
    "elegant":   ("'Cormorant Garamond', Georgia, serif", "'Lato', 'Segoe UI', Arial, sans-serif", "Cormorant+Garamond:wght@500;600;700&family=Lato:wght@400;700"),
    "mono":      ("'JetBrains Mono', Consolas, monospace", "'Inter', 'Segoe UI', Arial, sans-serif", "JetBrains+Mono:wght@500;700&family=Inter:wght@400;500;600"),
}

_NAMED_COLORS = {
    "navy": "#1f3a68", "blue": "#2563eb", "sky": "#0ea5e9", "teal": "#0f766e", "green": "#15803d",
    "emerald": "#059669", "olive": "#6b7a2e", "maroon": "#7f1d1d", "red": "#b91c1c", "wine": "#722f37",
    "purple": "#6d28d9", "violet": "#7c3aed", "lavender": "#8b7fc7", "pink": "#db2777", "rose": "#be7a7a",
    "orange": "#ea580c", "gold": "#c4a574", "golden": "#c4a574", "yellow": "#ca8a04", "mustard": "#c49a1a",
    "brown": "#8b5e3c", "beige": "#c8b49a", "black": "#111827", "charcoal": "#1f2937", "grey": "#4b5563",
    "gray": "#4b5563", "silver": "#9ca3af", "cyan": "#0891b2", "indigo": "#4338ca", "coral": "#f97362",
}

# ── Icons (24×24 stroke paths) ──────────────────────────────────────────────────────────────────
_ICONS = {
    "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "user": '<path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
    "pie": '<path d="M21.21 15.89A10 10 0 1 1 8 2.83"/><path d="M22 12A10 10 0 0 0 12 2v10z"/>',
    "bars": '<line x1="12" y1="20" x2="12" y2="10"/><line x1="18" y1="20" x2="18" y2="4"/><line x1="6" y1="20" x2="6" y2="16"/>',
    "trending": '<polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/>',
    "refresh": '<path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/><path d="M8 16H3v5"/>',
    "handshake": '<path d="m11 17 2 2a1 1 0 1 0 3-3"/><path d="m14 14 2.5 2.5a1 1 0 1 0 3-3l-3.88-3.88a3 3 0 0 0-4.24 0l-.88.88a1 1 0 1 1-3-3l2.81-2.81a5.79 5.79 0 0 1 7.06-.87l.47.28a2 2 0 0 0 1.42.25L21 4"/><path d="m21 3 1 11h-2"/><path d="M3 3 2 14l6.5 6.5a1 1 0 1 0 3-3"/><path d="M3 4h8"/>',
    "compass": '<circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/>',
    "presentation": '<path d="M2 3h20"/><path d="M21 3v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V3"/><path d="m7 21 5-5 5 5"/>',
    "lightbulb": '<path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/>',
    "gear": '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 1 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>',
    "book": '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>',
    "megaphone": '<path d="m3 11 18-5v12L3 14v-3z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
    "star": '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>',
    "clipboard": '<rect x="8" y="2" width="8" height="4" rx="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/>',
    "code": '<polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/>',
    "globe": '<circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>',
    "money": '<line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>',
    "briefcase": '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>',
    "award": '<circle cx="12" cy="8" r="7"/><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"/>',
    "chat": '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    "heart": '<path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>',
    "cap": '<path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/>',
    "trophy": '<path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/>',
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
    "pin": '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
    "linkedin": '<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-4 0v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/>',
    "link": '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>',
}


def _icon(name: str, color: str = "currentColor", size: str = "1em", fill: str = "none") -> str:
    body = _ICONS.get(name) or _ICONS["star"]
    return (f'<svg class="ic" viewBox="0 0 24 24" width="{size}" height="{size}" fill="{fill}" stroke="{color}" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{body}</svg>')


# ── Small helpers ───────────────────────────────────────────────────────────────────────────────
def _e(s) -> str:
    return _html.escape(str(s or ""), quote=True)


def _hex(c, default: str = "#888888") -> str:
    c = str(c or "").strip().lower()
    if c in _NAMED_COLORS:
        return _NAMED_COLORS[c]
    m = re.fullmatch(r"#?([0-9a-f]{6}|[0-9a-f]{3})", c)
    if not m:
        return default
    h = m.group(1)
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    return "#" + h


def _rgb(h: str) -> tuple[int, int, int]:
    h = _hex(h).lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def _mix(a: str, b: str, t: float) -> str:
    ra, ga, ba = _rgb(a)
    rb, gb, bb = _rgb(b)
    return "#%02x%02x%02x" % (round(ra + (rb - ra) * t), round(ga + (gb - ga) * t), round(ba + (bb - ba) * t))


def _lum(h: str) -> float:
    def ch(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = _rgb(h)
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def _contrast(a: str, b: str) -> float:
    la, lb = sorted([_lum(a), _lum(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


def _readable_on(bg: str, preferred: str | None = None) -> str:
    if preferred and _contrast(preferred, bg) >= 3.0:
        return preferred
    return "#ffffff" if _lum(bg) < 0.45 else "#2b2b2b"


def _load_state() -> dict:
    try:
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save_state(state: dict) -> None:
    if "design_cache" not in state:                 # callers hold an older copy; keep the on-disk cache
        cached = _load_state().get("design_cache")
        if cached:
            state["design_cache"] = cached
    try:
        os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
        with open(STATE_PATH, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[resume] could not save state: {e}")


def _parse_json(raw: str) -> dict:
    raw = re.sub(r"<think>.*?</think>", "", raw or "", flags=re.S)
    raw = re.sub(r"```(?:json)?|```", "", raw).strip()
    try:
        return json.loads(raw)
    except Exception:
        pass
    start = raw.find("{")
    if start < 0:
        return {}
    depth = 0
    for i in range(start, len(raw)):
        if raw[i] == "{":
            depth += 1
        elif raw[i] == "}":
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(raw[start:i + 1])
                except Exception:
                    return {}
    return {}


def _groq():
    from groq import Groq
    return Groq(api_key=settings.GROQ_API_KEY)


_GEMINI_MODELS = ("gemini-flash-lite-latest", "gemini-3.5-flash-lite", "gemini-3.1-flash-lite", "gemini-flash-latest")


def _gemini(parts: list, json_mode: bool = True, max_tokens: int = 6000) -> str:
    """Fallback when Groq is rate-limited (its vision model has a 200k tokens/DAY cap)."""
    import requests
    key = getattr(settings, "GEMINI_API_KEY", "") or os.getenv("GEMINI_API_KEY", "")
    if not key:
        return ""
    cfg = {"temperature": 0.3, "maxOutputTokens": max_tokens}
    if json_mode:
        cfg["responseMimeType"] = "application/json"
    for model in _GEMINI_MODELS:
        try:
            r = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}",
                              json={"contents": [{"parts": parts}], "generationConfig": cfg}, timeout=90)
            if r.status_code != 200:
                print(f"[resume] gemini {model} -> {r.status_code}")
                continue
            cand = (r.json().get("candidates") or [{}])[0]
            text = "".join(pt.get("text", "") for pt in (cand.get("content") or {}).get("parts", []))
            if text.strip():
                return text
        except Exception as e:
            print(f"[resume] gemini {model} failed: {str(e)[:120]}")
    return ""


def _llm_json(system: str, user: str, max_tokens: int = 6000) -> dict:
    last_err = None
    for model in (_TEXT_MODEL, _TEXT_MODEL_FALLBACK):
        for attempt in range(2):
            try:
                r = _groq().chat.completions.create(
                    model=model,
                    messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
                    max_tokens=max_tokens, temperature=0.4, response_format={"type": "json_object"})
                data = _parse_json(r.choices[0].message.content or "")
                if data:
                    return data
            except Exception as e:
                last_err = e
                msg = str(e).lower()
                print(f"[resume] {model} failed: {str(e)[:160]}")
                if "per day" in msg or "tpd" in msg:
                    break                      # daily cap: retrying the same model is pointless
                if "rate" in msg or "429" in msg:
                    time.sleep(3 + attempt * 3)
    data = _parse_json(_gemini([{"text": f"{system}\n\n{user}"}], True, max_tokens))
    if data:
        return data
    raise RuntimeError(f"LLM unavailable (Groq and Gemini): {last_err}")


# ── Image analysis ──────────────────────────────────────────────────────────────────────────────
def _palette(path: str, k: int = 8) -> list[tuple[str, float]]:
    """Dominant colours (hex, share) — gives the VLM exact values to pick from."""
    try:
        import cv2
        import numpy as np
        img = cv2.imread(path)
        if img is None:
            return []
        h, w = img.shape[:2]
        scale = 220 / max(w, 1)
        img = cv2.resize(img, (max(1, int(w * scale)), max(1, int(h * scale))), interpolation=cv2.INTER_AREA)
        px = img.reshape(-1, 3).astype(np.float32)
        crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
        _, labels, centers = cv2.kmeans(px, k, None, crit, 3, cv2.KMEANS_PP_CENTERS)
        counts = np.bincount(labels.flatten(), minlength=k)
        out = []
        for idx in counts.argsort()[::-1]:
            b, g, r = [int(v) for v in centers[idx]]
            out.append(("#%02x%02x%02x" % (r, g, b), round(float(counts[idx]) / len(labels), 3)))
        return out
    except Exception as e:
        print(f"[resume] palette failed: {e}")
        return []


def _faces(path: str) -> list[tuple[int, int, int, int]]:
    try:
        import cv2
        img = cv2.imread(path)
        if img is None:
            return []
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cascade = cv2.CascadeClassifier(os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_default.xml"))
        found = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=6, minSize=(30, 30))
        return sorted([tuple(int(v) for v in f) for f in found], key=lambda f: -f[2] * f[3])
    except Exception:
        return []


def _face_ratio(path: str) -> float:
    try:
        import cv2
        img = cv2.imread(path)
        faces = _faces(path)
        if img is None or not faces:
            return 0.0
        x, y, w, h = faces[0]
        return (w * h) / float(img.shape[0] * img.shape[1])
    except Exception:
        return 0.0


def _grow_photo_box(gray, face) -> tuple[int, int, int, int]:
    """Grow from the face outwards until each edge hits a flat (uniform) line = the photo's border."""
    H, W = gray.shape[:2]
    fx, fy, fw, fh = face
    x0, y0, x1, y1 = fx, fy, fx + fw, fy + fh

    def flat(seg) -> bool:
        return seg.size == 0 or float(seg.std()) < 7.0

    # probe only through the face's own band, so a slanted photo edge/banner doesn't look like "photo"
    by0, by1 = max(0, fy - fh // 2), min(H, fy + fh + fh // 2)
    bx0, bx1 = max(0, fx - fw // 2), min(W, fx + fw + fw // 2)
    while x0 > 0 and (x1 - x0) < 5 * fw and not flat(gray[by0:by1, x0 - 1]):
        x0 -= 1
    while x1 < W and (x1 - x0) < 5 * fw and not flat(gray[by0:by1, x1]):
        x1 += 1
    while y0 > 0 and (y1 - y0) < 6 * fh and not flat(gray[y0 - 1, bx0:bx1]):
        y0 -= 1
    while y1 < H and (y1 - y0) < 6 * fh and not flat(gray[y1, bx0:bx1]):
        y1 += 1
    return x0, y0, x1, y1


def _crop_photo(path: str, bbox: list | None = None) -> str:
    """Cut the portrait out of the reference resume: face-anchored edge growth → VLM bbox → face-expanded."""
    try:
        import cv2
        img = cv2.imread(path)
        if img is None:
            return ""
        H, W = img.shape[:2]
        faces = _faces(path)
        crop = None
        if faces:
            gx0, gy0, gx1, gy1 = _grow_photo_box(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), faces[0])
            fw, fh = faces[0][2], faces[0][3]
            if (gx1 - gx0) * (gy1 - gy0) >= 3 * fw * fh:
                crop = (gx0, gy0, gx1, gy1)
        if crop is None and bbox and len(bbox) == 4:
            x0, y0, x1, y1 = [float(v) for v in bbox]
            if max(x0, y0, x1, y1) <= 1.0:
                x0, x1, y0, y1 = x0 * W, x1 * W, y0 * H, y1 * H
            x0, y0, x1, y1 = int(max(0, x0)), int(max(0, y0)), int(min(W, x1)), int(min(H, y1))
            if x1 - x0 > 40 and y1 - y0 > 40:
                inside = any(x0 <= fx + fw / 2 <= x1 and y0 <= fy + fh / 2 <= y1 for fx, fy, fw, fh in faces)
                if inside or not faces:
                    crop = (x0, y0, x1, y1)
        if crop is None and faces:
            fx, fy, fw, fh = faces[0]
            cx, cy = fx + fw / 2, fy + fh * 0.75
            cw, chh = fw * 2.6, fh * 3.2
            crop = (int(max(0, cx - cw / 2)), int(max(0, cy - chh / 2)), int(min(W, cx + cw / 2)), int(min(H, cy + chh / 2)))
        if crop is None:
            return ""
        x0, y0, x1, y1 = crop
        os.makedirs(OUT_DIR, exist_ok=True)
        out = os.path.join(OUT_DIR, f"photo_{int(time.time())}.png")
        cv2.imwrite(out, img[y0:y1, x0:x1])
        return out
    except Exception as e:
        print(f"[resume] photo crop failed: {e}")
        return ""


_VISION_PROMPT = """You are a senior graphic designer. Analyse this RESUME DESIGN so it can be rebuilt exactly.
It may be a phone screenshot: IGNORE phone status bars, app toolbars/buttons and the viewer background around the page.
Dominant colours measured from the image (hex, share of pixels): {palette}

Return ONLY one JSON object, no prose:
{{
 "layout": "sidebar_left|sidebar_right|single_column",
 "sidebar_width": <percent of page width taken by the sidebar, 25-40; 0 for single_column>,
 "header": "diagonal_banner|full_band|centered|left_plain|sidebar_name",
 "photo": "square|circle|rounded|none",
 "photo_bbox": [x0, y0, x1, y1] <photo position as fractions 0-1 of the WHOLE image, or null>,
 "font": "sans|geometric|modern|serif|elegant|mono",
 "name_case": "upper|title",
 "heading_style": "underline|bar_left|boxed|caps_line|plain",
 "skills_style": "venn|bars|dots|chips|circles|list",
 "competency_style": "icon_grid|list",
 "timeline": true|false,
 "colors": {{"primary": "<header/banner colour>", "accent": "<secondary accent>", "heading": "<section heading text colour>",
             "text": "<body text>", "sidebar_bg": "<sidebar background>", "page_bg": "<main page background>",
             "header_text": "<text colour on the header>", "skill_colors": ["<up to 3 colours used in the skills graphic>"]}},
 "sidebar_sections": [<ordered section keys printed in the sidebar>],
 "main_sections": [<ordered section keys in the main column; for single_column, every section>],
 "section_titles": {{"<key>": "<heading text exactly as printed>"}},
 "notes": "<one sentence on distinctive design details>"
}}
Section keys: profile, highlights, contact, skills, competencies, experience, education, achievements, certifications, languages, interests, projects, references.
("highlights" = career highlights/summary bullets, "competencies" = core competencies/expertise blocks with icons.)
Header meanings: diagonal_banner = coloured banner with a slanted bottom edge next to/over a photo; full_band = solid coloured band across the top;
centered = name centred on plain background; left_plain = name left-aligned on plain background; sidebar_name = name printed inside the sidebar.
skills_style: venn = overlapping circles; bars = progress bars; dots = rating dots; circles = ring charts; chips = tags; list = plain list.
Choose colours from the measured list whenever they match."""


# A focused second look: the small VLM gets columns/section placement right far more often
# when asked only this (the big style prompt alone tends to answer "single_column").
_LAYOUT_PROMPT = """Look at this resume page (ignore phone UI bars and viewer background). List every section heading in
reading order and say which column it is in.
Return ONLY JSON: {"columns": 1 or 2, "narrow_column": "left|right|none", "narrow_column_width_percent": <n>,
"sections": [{"title": "<heading text>", "column": "left|right|full"}],
"heading_text_color": "<hex of section heading text such as PROFILE>", "skill_graphic_colors": ["<hex>", "<hex>", "<hex>"],
"banner_color": "<hex of the header/banner background>", "name_color": "<hex of the person's name text>"}"""

_TITLE_KEYS = [
    (r"profile|summary|about|objective|introduction", "profile"), (r"highlight|key\s+facts|at\s+a\s+glance", "highlights"),
    (r"contact|personal\s+(?:info|details)|reach", "contact"), (r"competenc|expertise|strength|core\s+areas", "competencies"),
    (r"skill|abilit", "skills"), (r"experience|employment|work\s+history|career\s+history|professional\s+history", "experience"),
    (r"education|academic|qualification|study", "education"), (r"achievement|award|honou?r|accomplish", "achievements"),
    (r"certif|training|course|licen", "certifications"), (r"language", "languages"),
    (r"interest|hobb|passion", "interests"), (r"project|portfolio", "projects"), (r"reference|referee", "references"),
]


def _title_key(title: str) -> str:
    t = (title or "").lower()
    for rx, key in _TITLE_KEYS:
        if re.search(rx, t):
            return key
    return ""


def _vision(b64: str, mime: str, prompt: str, max_tokens: int) -> dict:
    try:
        r = _groq().chat.completions.create(
            model=settings.GROQ_VISION_MODEL,
            messages=[{"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}}]}],
            temperature=0.1, max_tokens=max_tokens)
        data = _parse_json(r.choices[0].message.content or "")
        if data:
            return data
    except Exception as e:
        print(f"[resume] groq vision failed: {str(e)[:160]}")
    return _parse_json(_gemini([{"text": prompt}, {"inline_data": {"mime_type": mime, "data": b64}}], True, max_tokens + 1500))


def _image_b64(path: str, max_side: int = 1400) -> tuple[str, str]:
    """Downscaled JPEG (a 1080x2400 phone screenshot costs far fewer vision tokens at 1400px)."""
    try:
        import cv2
        img = cv2.imread(path)
        if img is not None:
            h, w = img.shape[:2]
            if max(h, w) > max_side:
                f = max_side / max(h, w)
                img = cv2.resize(img, (int(w * f), int(h * f)), interpolation=cv2.INTER_AREA)
            ok, buf = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 88])
            if ok:
                return base64.b64encode(buf.tobytes()).decode(), "image/jpeg"
    except Exception:
        pass
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode(), ("image/png" if path.lower().endswith(".png") else "image/jpeg")


def _file_hash(path: str) -> str:
    import hashlib
    try:
        with open(path, "rb") as f:
            return hashlib.sha1(f.read()).hexdigest()
    except Exception:
        return ""


def _apply_layout_answer(spec: dict, lay: dict) -> dict:
    secs = [s for s in (lay.get("sections") or []) if isinstance(s, dict)]
    side, main, titles = [], [], {}
    narrow = str(lay.get("narrow_column") or "").lower()
    two_cols = str(lay.get("columns")) == "2" and narrow in ("left", "right")
    for s in secs:
        key = _title_key(s.get("title", ""))
        if not key or key in side or key in main:
            continue
        titles[key] = str(s.get("title") or "").strip()[:40]
        (side if two_cols and str(s.get("column")).lower() == narrow else main).append(key)
    if secs:
        spec["section_titles"] = {**(spec.get("section_titles") or {}), **titles}
    if two_cols and side and main:
        spec["layout"] = "sidebar_left" if narrow == "left" else "sidebar_right"
        spec["sidebar_sections"], spec["main_sections"] = side, main
        try:
            spec["sidebar_width"] = int(float(lay.get("narrow_column_width_percent") or spec.get("sidebar_width") or 32))
        except Exception:
            pass
    elif secs and str(lay.get("columns")) == "1":
        spec["layout"], spec["sidebar_sections"], spec["main_sections"] = "single_column", [], main
    if not isinstance(spec.get("colors"), dict):
        spec["colors"] = {}
    cols = spec["colors"]
    if lay.get("heading_text_color"):
        cols["heading"] = lay["heading_text_color"]
    if lay.get("banner_color"):
        cols["primary"] = lay["banner_color"]
    if lay.get("name_color"):
        cols["header_text"] = lay["name_color"]
    if lay.get("skill_graphic_colors"):
        cols["skill_colors"] = lay["skill_graphic_colors"]
    return spec


def _analyse_design(image_path: str) -> dict:
    from concurrent.futures import ThreadPoolExecutor
    key = _file_hash(image_path)
    cache = _load_state().get("design_cache") or {}
    if key and key in cache:                      # same picture again → no vision tokens spent
        return cache[key]
    pal = _palette(image_path)
    pal_txt = ", ".join(f"{c} ({s:.0%})" for c, s in pal) or "unavailable"
    try:
        b64, mime = _image_b64(image_path)
    except Exception as e:
        print(f"[resume] cannot read image: {e}")
        return {"_palette": pal, "_vision_failed": True}
    with ThreadPoolExecutor(max_workers=2) as ex:
        f_style = ex.submit(_vision, b64, mime, _VISION_PROMPT.format(palette=pal_txt), 2500)
        f_layout = ex.submit(_vision, b64, mime, _LAYOUT_PROMPT, 1500)
        spec, lay = f_style.result(), f_layout.result()
    if not spec and not lay:
        return {"_palette": pal, "_vision_failed": True}
    spec = _apply_layout_answer(spec or {}, lay or {})
    spec["_palette"] = pal
    if key:
        st = _load_state()
        cache = st.get("design_cache") or {}
        cache[key] = spec
        st["design_cache"] = dict(list(cache.items())[-10:])
        _save_state(st)
    return spec


def _closest_preset(spec: dict) -> str:
    best, best_score = "elegant", -1
    for name, p in PRESETS.items():
        score = sum(2 if spec.get(k) == p.get(k) else 0 for k in ("layout", "header"))
        score += sum(1 for k in ("skills_style", "heading_style", "font", "photo") if spec.get(k) == p.get(k))
        if score > best_score:
            best, best_score = name, score
    return best


def _merge_design(base: dict, over: dict) -> dict:
    d = json.loads(json.dumps(base))
    allowed = {
        "layout": {"sidebar_left", "sidebar_right", "single_column"},
        "header": {"diagonal_banner", "full_band", "centered", "left_plain", "sidebar_name"},
        "photo": {"square", "circle", "rounded", "none"},
        "font": set(_FONTS), "name_case": {"upper", "title"},
        "heading_style": {"underline", "bar_left", "boxed", "caps_line", "plain"},
        "skills_style": {"venn", "bars", "dots", "chips", "circles", "list"},
        "competency_style": {"icon_grid", "list"},
    }
    for k, ok in allowed.items():
        v = str(over.get(k) or "").strip().lower()
        if v in ok:
            d[k] = v
    if isinstance(over.get("timeline"), bool):
        d["timeline"] = over["timeline"]
    try:
        sw = int(float(over.get("sidebar_width") or 0))
        if 22 <= sw <= 42:
            d["sidebar_width"] = sw
    except Exception:
        pass
    cols = over.get("colors") or {}
    if isinstance(cols, dict):
        for k in ("primary", "accent", "heading", "text", "sidebar_bg", "page_bg", "header_text"):
            if cols.get(k):
                d["colors"][k] = _hex(cols[k], d["colors"][k])
        sc = [_hex(c, "") for c in (cols.get("skill_colors") or []) if _hex(c, "")]
        if sc:
            d["colors"]["skill_colors"] = (sc + d["colors"]["skill_colors"])[:3]
    for key in ("sidebar_sections", "main_sections"):
        lst = [s for s in (over.get(key) or []) if s in SECTION_KEYS]
        if lst or (key == "sidebar_sections" and over.get("layout") == "single_column"):
            d[key] = list(dict.fromkeys(lst))
    titles = over.get("section_titles") or {}
    if isinstance(titles, dict):
        d.setdefault("section_titles", {}).update({k: str(v)[:40] for k, v in titles.items() if k in SECTION_KEYS and v})
    if over.get("photo_bbox"):
        d["photo_bbox"] = over["photo_bbox"]
    if over.get("notes"):
        d["notes"] = str(over["notes"])[:300]
    return d


def _apply_color(design: dict, color: str) -> dict:
    c = _hex(color, "")
    if not c:
        return design
    cols = design["colors"]
    cols["primary"] = c
    dark = _mix(c, "#000000", 0.35) if _lum(c) > 0.2 else c
    cols["accent"] = dark
    cols["heading"] = dark if _contrast(dark, cols.get("page_bg", "#ffffff")) >= 3 else "#222222"
    if _lum(cols.get("sidebar_bg", "#ffffff")) > 0.6:
        cols["sidebar_bg"] = _mix(c, "#ffffff", 0.9)
    else:
        cols["sidebar_bg"] = _mix(c, "#000000", 0.55)
    cols["skill_colors"] = [_mix(c, "#ffffff", 0.35), dark, _mix(c, "#ffffff", 0.6)]
    cols["header_text"] = _readable_on(c)
    return design


def _sanitize_design(design: dict) -> dict:
    """Make sure colours stay readable and every section has a home."""
    c = design["colors"]
    c["header_text"] = _readable_on(c["primary"], c.get("header_text"))
    if _contrast(c["text"], c["page_bg"]) < 4:
        c["text"] = _readable_on(c["page_bg"])
    if _contrast(c["heading"], c["page_bg"]) < 2.5:
        c["heading"] = c["accent"] if _contrast(c["accent"], c["page_bg"]) >= 2.5 else _readable_on(c["page_bg"])
    if _contrast(c["accent"], c["page_bg"]) < 2.5:      # accent is used for company names / bullets
        c["accent"] = c["heading"]
    venn = []
    for col in c.get("skill_colors") or []:              # white labels sit on these circles
        for _ in range(8):
            if _contrast(col, "#ffffff") >= 1.8:
                break
            col = _mix(col, "#000000", 0.08)
        venn.append(col)
    c["skill_colors"] = (venn + [c["primary"], c["accent"], c["heading"]])[:3]
    if design["layout"] == "single_column":
        design["main_sections"] = list(dict.fromkeys(design.get("sidebar_sections", []) + design["main_sections"]))
        design["sidebar_sections"] = []
        if design["header"] == "sidebar_name":
            design["header"] = "left_plain"
    elif not design.get("sidebar_sections"):
        design["sidebar_sections"] = ["contact", "skills", "education", "languages"]
    design["main_sections"] = [s for s in design["main_sections"] if s not in design.get("sidebar_sections", [])]
    return design


def _resolve_design(image_path: str, template: str, color: str, previous: dict | None):
    """Returns (design, note) — note is a human line about where the design came from."""
    tpl = (template or "").strip().lower()
    if image_path:
        spec = _analyse_design(image_path)
        base = PRESETS[tpl] if tpl in PRESETS else PRESETS[_closest_preset(spec)]
        design = _merge_design(base, spec)
        design["source"] = "image"
        note = ("I couldn't read the reference clearly, so I matched it to the closest built-in format."
                if spec.get("_vision_failed") else f"Design read from your image ({design['layout'].replace('_', ' ')}, "
                f"{design['header'].replace('_', ' ')} header, {design['skills_style']} skills).")
    elif tpl in PRESETS:
        design = json.loads(json.dumps(PRESETS[tpl]))
        design["source"] = tpl
        note = f"Using the **{tpl}** format."
    elif previous:
        design = json.loads(json.dumps(previous))
        note = ("Design copied from your reference image." if previous.get("source") == "image"
                else "Using the same design as last time.")
    else:
        design = json.loads(json.dumps(PRESETS["elegant"]))
        design["source"] = "elegant"
        note = "Using the **elegant** format (send a picture of any resume to copy its design)."
    if color:
        design = _apply_color(design, color)
    return _sanitize_design(design), note


# ── Content ─────────────────────────────────────────────────────────────────────────────────────
_CONTENT_SYSTEM = """You are an expert resume writer and typesetter. Turn the user's raw details into polished resume content as JSON.
RULES
- Use ONLY facts the user gave. Never invent employers, job titles, dates, degrees, numbers, awards, phone, email or links.
- NEVER add metrics, percentages or figures the user did not write (no "increased revenue by 30%").
- Write in standard resume voice with NO pronouns (no I/he/she/they/his/her) and don't start the profile with the person's name.
  e.g. "B.Tech CSE student at DTU building AI assistants..." — never guess gender.
- You MAY polish wording, fix grammar, make bullets punchy and action-led, and write short descriptions that restate the user's facts.
- Fill the design's sections when the user's facts support them (e.g. derive core competencies and key skills from their experience).
- Keep it tight so it fits 1-2 A4 pages. Omit a field (empty string/list) when there is nothing true to put in it.
Return exactly this JSON shape:
{
 "name": "", "title": "<headline, e.g. 'Chief Branch Manager & Marketing Professional'>",
 "profile": ["<paragraph 1, 35-55 words>", "<optional paragraph 2>"],
 "contact": {"phone": "", "email": "", "location": "", "linkedin": "", "website": ""},
 "highlights": ["<career highlight, max 12 words>"],
 "skills": [{"name": "<skill, 1-2 words>", "level": <50-100>}],
 "additional_skills": ["<short skill>"],
 "competencies": [{"title": "<1-3 words>", "description": "<10-16 words>", "icon": "<icon key>"}],
 "experience": [{"role": "", "company": "", "period": "", "location": "", "bullets": [""]}],
 "education": [{"degree": "", "institution": "", "period": "", "details": ""}],
 "achievements": [""], "certifications": [""],
 "languages": [{"name": "", "level": <1-5>}], "interests": [""],
 "projects": [{"name": "", "description": ""}], "references": [""]
}
Icon keys: target, users, user, pie, bars, trending, refresh, handshake, compass, presentation, lightbulb, gear, book, megaphone, shield, star, clipboard, code, globe, money, briefcase, award, chat, clock, heart, cap."""


def _content_brief(design: dict) -> str:
    secs = design.get("sidebar_sections", []) + design.get("main_sections", [])
    lines = [f"Design sections (in order): {', '.join(secs)}."]
    if design.get("skills_style") == "venn":
        lines.append("The skills graphic is a 3-circle Venn: the FIRST 3 skills must be single words of <= 11 letters (e.g. SALES, LEADERSHIP); put the rest in additional_skills.")
    else:
        lines.append("List 5-8 skills with honest relative levels; extra ones go to additional_skills.")
    if "competencies" in secs:
        lines.append("Write 6-8 competencies (even number) derived from the user's real work.")
    if "highlights" in secs:
        lines.append("Write 3-5 career highlights.")
    return " ".join(lines)


def _str_list(v, limit: int = 20) -> list[str]:
    if isinstance(v, str):
        v = [x for x in re.split(r"\n|;|•", v)]
    if not isinstance(v, list):
        return []
    out = []
    for x in v:
        if isinstance(x, dict):
            x = x.get("name") or x.get("title") or x.get("text") or ""
        x = str(x).strip(" -•\t")
        if x:
            out.append(x)
    return out[:limit]


def _normalise_content(c: dict) -> dict:
    c = c if isinstance(c, dict) else {}
    out = {"name": str(c.get("name") or "").strip(), "title": str(c.get("title") or "").strip()}
    out["profile"] = _str_list(c.get("profile"), 3)
    contact = c.get("contact") if isinstance(c.get("contact"), dict) else {}
    out["contact"] = {k: str(contact.get(k) or "").strip() for k in ("phone", "email", "location", "linkedin", "website")}
    out["highlights"] = _str_list(c.get("highlights"), 8)
    skills = []
    for s in (c.get("skills") or []):
        if isinstance(s, str):
            s = {"name": s}
        if isinstance(s, dict) and str(s.get("name") or "").strip():
            try:
                lvl = int(float(s.get("level") or 80))
            except Exception:
                lvl = 80
            skills.append({"name": str(s["name"]).strip(), "level": max(20, min(100, lvl))})
    out["skills"] = skills[:12]
    out["additional_skills"] = _str_list(c.get("additional_skills"), 14)
    comps = []
    for x in (c.get("competencies") or []):
        if isinstance(x, str):
            x = {"title": x}
        if isinstance(x, dict) and x.get("title"):
            icon = str(x.get("icon") or "").strip().lower()
            comps.append({"title": str(x["title"]).strip(), "description": str(x.get("description") or "").strip(),
                          "icon": icon if icon in _ICONS else ""})
    out["competencies"] = comps[:10]
    exp = []
    for x in (c.get("experience") or []):
        if isinstance(x, dict) and (x.get("role") or x.get("company")):
            exp.append({k: str(x.get(k) or "").strip() for k in ("role", "company", "period", "location")}
                       | {"bullets": _str_list(x.get("bullets"), 8)})
    out["experience"] = exp[:10]
    edu = []
    for x in (c.get("education") or []):
        if isinstance(x, str):
            x = {"degree": x}
        if isinstance(x, dict) and (x.get("degree") or x.get("institution")):
            edu.append({k: str(x.get(k) or "").strip() for k in ("degree", "institution", "period", "details")})
    out["education"] = edu[:6]
    out["achievements"] = _str_list(c.get("achievements"), 12)
    out["certifications"] = _str_list(c.get("certifications"), 10)
    langs = []
    for x in (c.get("languages") or []):
        if isinstance(x, str):
            x = {"name": x}
        if isinstance(x, dict) and not x.get("name"):
            x = {**x, "name": x.get("language") or x.get("title") or ""}
        if isinstance(x, dict) and x.get("name"):
            try:
                lvl = int(float(x.get("level") or 4))
            except Exception:
                word = str(x.get("level")).lower()
                lvl = next((v for k, v in (("native", 5), ("mother", 5), ("fluent", 5), ("profic", 4), ("advanced", 4),
                                           ("professional", 4), ("intermediate", 3), ("conversational", 3),
                                           ("basic", 2), ("beginner", 1)) if k in word), 4)
            langs.append({"name": str(x["name"]).strip(), "level": max(1, min(5, lvl))})
    out["languages"] = langs[:6]
    out["interests"] = _str_list(c.get("interests"), 10)
    projs = []
    for x in (c.get("projects") or []):
        if isinstance(x, str):
            x = {"name": x}
        if isinstance(x, dict) and x.get("name"):
            projs.append({"name": str(x["name"]).strip(), "description": str(x.get("description") or "").strip()})
    out["projects"] = projs[:6]
    out["references"] = _str_list(c.get("references"), 4)
    return out


def _nums(text: str) -> set[str]:
    return {n.replace(",", "") for n in re.findall(r"\d[\d,]*(?:\.\d+)?", text or "")}


def _drop_invented(content: dict, source: str) -> dict:
    """The LLM likes to 'improve' bullets with made-up metrics. Drop any sentence/bullet whose numbers
    the user never wrote, and blank contact values that aren't in the source."""
    known = _nums(source)
    src_low = (source or "").lower()

    def ok(s: str) -> bool:
        return _nums(s) <= known

    def clean_text(s: str) -> str:
        return " ".join(p for p in re.split(r"(?<=[.!?])\s+", s) if ok(p)).strip()

    content["profile"] = [t for t in (clean_text(p) for p in content["profile"]) if t]
    for key in ("highlights", "achievements", "certifications", "references"):
        content[key] = [x for x in content[key] if ok(x)]
    for job in content["experience"]:
        job["bullets"] = [b for b in job["bullets"] if ok(b)]
        if not ok(job["period"]):
            job["period"] = ""
    for comp in content["competencies"]:
        comp["description"] = clean_text(comp["description"])
    for proj in content["projects"]:
        proj["description"] = clean_text(proj["description"])
    for edu in content["education"]:
        if not ok(edu["period"]):
            edu["period"] = ""
    ct = content["contact"]
    if ct["phone"] and not (re.sub(r"\D", "", ct["phone"])[-8:] in re.sub(r"\D", "", source or "")):
        ct["phone"] = ""
    for k in ("email", "linkedin", "website"):
        if ct[k] and ct[k].lower().split("//")[-1].strip("/") not in src_low:
            ct[k] = ""
    return content


_NAME_STOP = re.compile(r"\b(?:student|engineer|developer|manager|b\.?\s?tech|resume|cv|email|phone|skills?|university|college)\b", re.I)


def _guess_name(details: str) -> str:
    """Smaller fallback models sometimes drop the name; recover it from the user's own text."""
    m = re.search(r"\bname\s*(?:is|:|-)\s*([A-Z][\w.'-]+(?:\s+[A-Z][\w.'-]+){0,3})", details)
    if m:
        return m.group(1).strip()
    m = re.search(r"\b(?:i\s+am|i'm|this\s+is|for)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,2})\b", details)
    if m and not _NAME_STOP.search(m.group(1)):
        return m.group(1)
    for line in details.strip().splitlines()[:3]:
        head = re.split(r"[,|•\-–:(]", line.strip(), 1)[0].strip()
        if re.fullmatch(r"[A-Z][a-zA-Z.'-]+(?:\s+[A-Z][a-zA-Z.'-]+){1,3}", head) and not _NAME_STOP.search(head):
            return head
    return ""


def _guess_title(details: str) -> str:
    m = re.search(r"\b(?:title|headline|role|position)\s*[:\-]\s*([^\n.,;]{3,60})", details, re.I)
    if m:
        return m.group(1).strip()
    m = re.search(r"\b((?:B\.?\s?Tech|M\.?\s?Tech|BCA|MCA|MBA|B\.?Sc|M\.?Sc|BBA|B\.?Com)[^,\n.]{0,30}?student)\b", details, re.I)
    if m:
        return m.group(1).strip()
    m = re.search(r"\b((?:(?:senior|junior|lead|chief|principal|associate)\s+)?(?:(?!(?:a|an|the|as|at|of)\b)[a-z]+\s+){0,2}?"
                  r"(?:engineer|developer|manager|designer|analyst|consultant|scientist|architect))\b", details, re.I)
    return m.group(1).strip().title() if m else ""


def _build_content(details: str, design: dict) -> dict:
    user = f"{_content_brief(design)}\n\nUSER DETAILS:\n{details.strip()[:12000]}"
    content = _drop_invented(_normalise_content(_llm_json(_CONTENT_SYSTEM, user)), details)
    if not content["name"]:
        content["name"] = _guess_name(details)
    if not content["title"]:
        content["title"] = _guess_title(details)
    return content


_EDIT_SYSTEM = """You edit an existing resume. Apply the user's instruction to the resume JSON and return the FULL updated JSON
in the same shape. Change only what the instruction asks; never invent facts. If the instruction asks for a design change
(colour, template, font, layout), leave the content unchanged and also return "design_request": "<short description>".
Shape reference (use these exact keys for any list you add to):
""" + _CONTENT_SYSTEM.split("Return exactly this JSON shape:", 1)[1]


def _edit_content(old: dict, instruction: str) -> dict:
    user = f"INSTRUCTION: {instruction}\n\nCURRENT RESUME JSON:\n{json.dumps(old, ensure_ascii=False)}"
    data = _llm_json(_EDIT_SYSTEM, user)
    data.pop("design_request", None)
    merged = _drop_invented(_normalise_content(data), json.dumps(old, ensure_ascii=False) + "\n" + instruction)
    return merged if (merged.get("name") or merged.get("experience")) else old


# ── HTML rendering ──────────────────────────────────────────────────────────────────────────────
def _title(design: dict, key: str) -> str:
    return (design.get("section_titles") or {}).get(key) or DEFAULT_TITLES[key]


def _sec(design: dict, key: str, inner: str, cls: str = "") -> str:
    return f'<section class="sec sec-{key} {cls}"><h2>{_e(_title(design, key))}</h2>{inner}</section>'


def _venn(skills: list[dict], colors: list[str]) -> str:
    top = [s["name"] for s in skills[:3]]
    n = len(top)
    if not n:
        return ""
    r, cy = 78, 88
    centers = {1: [180], 2: [135, 225], 3: [100, 180, 260]}[n]
    offsets = {1: [0], 2: [-22, 22], 3: [-26, 0, 26]}[n]
    circles, labels = [], []
    for i, (cx, label) in enumerate(zip(centers, top)):
        col = colors[i % len(colors)]
        circles.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}" fill-opacity="0.82"/>')
        txt = label.upper()
        width = 92 if n == 3 else 120
        fs = max(8.5, min(15.0, width / (0.66 * max(len(txt), 1))))
        labels.append(f'<text x="{cx + offsets[i]}" y="{cy + fs * 0.35:.1f}" text-anchor="middle" font-size="{fs:.1f}" '
                      f'font-weight="700" fill="#ffffff" letter-spacing="0.4">{_e(txt)}</text>')
    return f'<svg class="venn" viewBox="0 0 360 176" xmlns="http://www.w3.org/2000/svg">{"".join(circles)}{"".join(labels)}</svg>'


def _ring(level: int, color: str, track: str) -> str:
    circ = 2 * 3.14159 * 15
    dash = circ * level / 100
    return (f'<svg viewBox="0 0 36 36" class="ring"><circle cx="18" cy="18" r="15" fill="none" stroke="{track}" stroke-width="3.2"/>'
            f'<circle cx="18" cy="18" r="15" fill="none" stroke="{color}" stroke-width="3.2" stroke-linecap="round" '
            f'stroke-dasharray="{dash:.1f} {circ:.1f}" transform="rotate(-90 18 18)"/>'
            f'<text x="18" y="21" text-anchor="middle" font-size="8.5" font-weight="700" fill="{color}">{level}%</text></svg>')


def _skills_html(c: dict, d: dict, side: bool) -> str:
    skills, extra = c["skills"], c["additional_skills"]
    if not skills and not extra:
        return ""
    style = d["skills_style"]
    cols = d["colors"]
    fg = "var(--side-accent)" if side else "var(--primary)"
    track = "var(--side-track)" if side else "var(--track)"
    parts = []
    if style == "venn" and skills:
        parts.append(_venn(skills, cols["skill_colors"]))
        rest = [s["name"] for s in skills[3:]] + extra
        if rest:
            parts.append(f'<div class="addl"><div class="addl-h">Additional Skills:</div>'
                         f'<div class="addl-list">{" <span class=dot>•</span> ".join(_e(x) for x in rest)}</div></div>')
        return "".join(parts)
    if style == "bars":
        parts.append('<div class="bars">' + "".join(
            f'<div class="bar-row"><div class="bar-l">{_e(s["name"])}</div><div class="bar-t" style="background:{track}">'
            f'<div class="bar-f" style="width:{s["level"]}%;background:{fg}"></div></div></div>' for s in skills) + "</div>")
    elif style == "dots":
        parts.append('<div class="dots">' + "".join(
            f'<div class="dot-row"><span>{_e(s["name"])}</span><span class="dot-set">' +
            "".join(f'<i style="background:{fg if k < round(s["level"] / 20) else track}"></i>' for k in range(5)) +
            "</span></div>" for s in skills) + "</div>")
    elif style == "circles":
        ring_col = cols["accent"]
        parts.append('<div class="rings">' + "".join(
            f'<div class="ring-cell">{_ring(s["level"], ring_col, _mix(ring_col, "#ffffff", 0.75))}<div>{_e(s["name"])}</div></div>'
            for s in skills[:9]) + "</div>")
    elif style == "list":
        parts.append('<ul class="plain">' + "".join(f"<li>{_e(s['name'])}</li>" for s in skills) + "</ul>")
    else:  # chips (also used for leftovers)
        extra = [s["name"] for s in skills] + extra
    if extra:
        parts.append('<div class="chips">' + "".join(f"<span>{_e(x)}</span>" for x in extra) + "</div>")
    return "".join(parts)


_ICON_GUESS = [("strateg", "compass"), ("plan", "clipboard"), ("team", "users"), ("develop", "trending"),
               ("manage", "user"), ("lead", "users"), ("coach", "presentation"), ("mentor", "presentation"),
               ("train", "presentation"), ("target", "target"), ("execut", "target"), ("goal", "target"),
               ("analy", "pie"), ("data", "bars"), ("persist", "refresh"), ("renew", "refresh"), ("retention", "refresh"),
               ("relation", "handshake"), ("client", "handshake"), ("customer", "handshake"), ("negotia", "handshake"),
               ("sales", "money"), ("revenue", "money"), ("finance", "money"), ("market", "megaphone"),
               ("brand", "megaphone"), ("communic", "chat"), ("creativ", "lightbulb"), ("innov", "lightbulb"),
               ("operat", "gear"), ("process", "gear"), ("tech", "code"), ("software", "code"), ("research", "book"),
               ("compliance", "shield"), ("risk", "shield"), ("time", "clock"), ("global", "globe")]


def _guess_icon(title: str) -> str:
    t = title.lower()
    for kw, ic in _ICON_GUESS:
        if kw in t:
            return ic
    return "star"


def _competencies_html(c: dict, d: dict, side: bool) -> str:
    items = c["competencies"]
    if not items:
        return ""
    if d["competency_style"] == "list" or side:
        return '<ul class="comp-list">' + "".join(
            f'<li><b>{_e(x["title"])}</b>{" — " + _e(x["description"]) if x["description"] else ""}</li>' for x in items) + "</ul>"
    return '<div class="comp-grid">' + "".join(
        f'<div class="comp"><div class="comp-ic">{_icon(x["icon"] or _guess_icon(x["title"]), "var(--heading)")}</div>'
        f'<div><div class="comp-t">{_e(x["title"])}</div><div class="comp-d">{_e(x["description"])}</div></div></div>'
        for x in items) + "</div>"


def _experience_html(c: dict, d: dict, side: bool) -> str:
    if not c["experience"]:
        return ""
    rows = []
    for x in c["experience"]:
        sub = " · ".join(_e(v) for v in (x["company"], x["location"]) if v)
        bullets = "".join(f"<li>{_e(b)}</li>" for b in x["bullets"])
        rows.append(f'<div class="job"><div class="job-top"><div class="job-role">{_e(x["role"] or x["company"])}</div>'
                    f'<div class="job-period">{_e(x["period"])}</div></div>'
                    f'{f"<div class=job-co>{sub}</div>" if sub and x["role"] else ""}'
                    f'{f"<ul>{bullets}</ul>" if bullets else ""}</div>')
    return f'<div class="{"timeline" if d.get("timeline") else "jobs"}">{"".join(rows)}</div>'


def _education_html(c: dict, d: dict, side: bool) -> str:
    return "".join(
        f'<div class="edu"><div class="edu-deg">{_e(x["degree"])}</div>'
        f'{f"<div class=edu-inst>{_e(x["institution"])}</div>" if x["institution"] else ""}'
        f'{f"<div class=edu-meta>{_e(x["period"])}</div>" if x["period"] else ""}'
        f'{f"<div class=edu-meta>{_e(x["details"])}</div>" if x["details"] else ""}</div>' for x in c["education"])


def _contact_html(c: dict, d: dict, side: bool) -> str:
    ct = c["contact"]
    col = "var(--side-heading)" if side else "var(--heading)"
    rows = [(k, ic) for k, ic in (("phone", "phone"), ("email", "mail"), ("location", "pin"),
                                  ("linkedin", "linkedin"), ("website", "link")) if ct.get(k)]
    return "".join(f'<div class="ct"><span class="ct-ic">{_icon(ic, col, fill=col if ic == "phone" else "none")}</span>'
                   f'<span class="ct-v">{_e(ct[k])}</span></div>' for k, ic in rows)


def _list_html(items: list[str], icon: str | None, side: bool) -> str:
    if not items:
        return ""
    if icon:
        col = "var(--side-heading)" if side else "var(--heading)"
        return '<ul class="ic-list">' + "".join(
            f'<li><span class="li-ic">{_icon(icon, col, fill=col if icon == "trophy" else "none")}</span>{_e(x)}</li>'
            for x in items) + "</ul>"
    return '<ul class="bul">' + "".join(f"<li>{_e(x)}</li>" for x in items) + "</ul>"


def _section_html(key: str, c: dict, d: dict, side: bool) -> str:
    if key == "profile":
        inner = "".join(f"<p>{_e(p)}</p>" for p in c["profile"])
    elif key == "highlights":
        inner = _list_html(c["highlights"], None, side)
    elif key == "contact":
        inner = _contact_html(c, d, side)
    elif key == "skills":
        inner = _skills_html(c, d, side)
    elif key == "competencies":
        inner = _competencies_html(c, d, side)
    elif key == "experience":
        inner = _experience_html(c, d, side)
    elif key == "education":
        inner = _education_html(c, d, side)
    elif key == "achievements":
        inner = _list_html(c["achievements"], "trophy", side)
    elif key == "certifications":
        inner = _list_html(c["certifications"], "award", side)
    elif key == "languages":
        inner = "".join(
            f'<div class="dot-row"><span>{_e(x["name"])}</span><span class="dot-set">' +
            "".join(f'<i class="{"on" if k < x["level"] else ""}"></i>' for k in range(5)) + "</span></div>"
            for x in c["languages"])
    elif key == "interests":
        inner = ('<div class="chips">' + "".join(f"<span>{_e(x)}</span>" for x in c["interests"]) + "</div>") if c["interests"] else ""
    elif key == "projects":
        inner = "".join(f'<div class="proj"><b>{_e(x["name"])}</b>{f"<div>{_e(x["description"])}</div>" if x["description"] else ""}</div>'
                        for x in c["projects"])
    elif key == "references":
        inner = _list_html(c["references"], None, side)
    else:
        inner = ""
    return _sec(d, key, inner) if inner else ""


def _initials(name: str) -> str:
    parts = [p for p in re.split(r"\s+", name.strip()) if p]
    return "".join(p[0] for p in parts[:2]).upper() or "CV"


def _photo_html(photo_uri: str, name: str, shape: str, cls: str) -> str:
    if shape == "none":
        return ""
    if photo_uri:
        return f'<div class="{cls} ph-{shape}" style="background-image:url(\'{photo_uri}\')"></div>'
    return f'<div class="{cls} ph-{shape} ph-empty"><span>{_e(_initials(name))}</span></div>'


def _name_block(c: dict, d: dict, size_pt: float) -> str:
    name = c["name"] or "Your Name"
    name = name.upper() if d["name_case"] == "upper" else name
    title = c["title"].upper() if d["name_case"] == "upper" else c["title"]
    title_html = _e(title)
    if len(title) > 30 and " & " in title:          # "CHIEF BRANCH MANAGER &<br>MARKETING PROFESSIONAL"
        title_html = _e(title).replace(" &amp; ", " &amp;<br>", 1)
    return (f'<div class="nm" style="font-size:{size_pt:.1f}pt">{_e(name)}</div>'
            f'{f"<div class=ttl>{title_html}</div>" if title else ""}')


def _name_size(name: str, avail_mm: float, max_pt: float) -> float:
    # bold caps ≈ 0.68em per glyph; 1pt = 0.3528mm
    return max(16.0, min(max_pt, avail_mm / (0.68 * 0.3528 * max(len(name), 6))))


def _header_html(c: dict, d: dict, photo_uri: str) -> str:
    h, sw = d["header"], d.get("sidebar_width", 32) if d["layout"] != "single_column" else 0
    name = c["name"] or "Your Name"
    if h == "sidebar_name":
        return ""
    if h == "diagonal_banner":
        ph = _photo_html(photo_uri, name, "square" if d["photo"] != "none" else "none", "hd-photo")
        width_pct = sw if (ph and sw) else (30 if ph else 0)
        avail = 210 * (100 - width_pct) / 100 - 20
        return (f'<header class="hd-diag" style="--pw:{width_pct}%">{ph}'
                f'<div class="hd-banner">{_name_block(c, d, _name_size(name, avail, 34))}</div></header>')
    if h == "full_band":
        ph = _photo_html(photo_uri, name, d["photo"], "hd-avatar")
        avail = 210 - 24 - (40 if ph else 0)
        return f'<header class="hd-band">{ph}<div class="hd-txt">{_name_block(c, d, _name_size(name, avail, 32))}</div></header>'
    if h == "centered":
        ph = _photo_html(photo_uri, name, d["photo"], "hd-avatar")
        return f'<header class="hd-center">{ph}{_name_block(c, d, _name_size(name, 170, 30))}</header>'
    ph = _photo_html(photo_uri, name, d["photo"], "hd-avatar")
    return f'<header class="hd-left"><div class="hd-txt">{_name_block(c, d, _name_size(name, 150, 30))}</div>{ph}</header>'


def _css(d: dict, scale: float) -> str:
    c = d["colors"]
    head_font, body_font, _ = _FONTS.get(d["font"], _FONTS["sans"])
    side_bg = c["sidebar_bg"]
    side_text = _readable_on(side_bg, c["text"])
    side_heading = _readable_on(side_bg, c["heading"])
    side_accent = c["accent"] if _contrast(c["accent"], side_bg) >= 2.2 else (c["primary"] if _contrast(c["primary"], side_bg) >= 2.2 else side_text)
    sw = d.get("sidebar_width", 32)
    hs = d["heading_style"]
    h2 = {
        "underline": "display:inline-block;padding-bottom:1.2mm;border-bottom:2.6px solid currentColor;min-width:36mm;",
        "bar_left": "border-left:4px solid var(--primary);padding-left:2.6mm;",
        "boxed": "display:inline-block;background:var(--primary);color:var(--on-primary)!important;padding:1.2mm 3.2mm;border-radius:2px;",
        "caps_line": "letter-spacing:2.2px;border-bottom:1px solid var(--rule);padding-bottom:1.2mm;display:block;",
        "plain": "",
    }[hs]
    side_h2_fix = "aside .sec h2{border-left-color:var(--side-accent)}" if hs == "bar_left" else ""
    if hs == "boxed":
        side_h2_fix = "aside .sec h2{background:var(--side-accent);color:%s!important}" % _readable_on(side_accent)
    if hs == "caps_line":
        side_h2_fix = "aside .sec h2{border-bottom-color:var(--side-rule)}"
    photo_radius = {"circle": "50%", "rounded": "14%", "square": "0"}.get(d["photo"], "50%")
    return f"""
:root{{--primary:{c['primary']};--on-primary:{c['header_text']};--accent:{c['accent']};--heading:{c['heading']};--text:{c['text']};
--muted:{_mix(c['text'], c['page_bg'], 0.3)};--page:{c['page_bg']};--side:{side_bg};--side-text:{side_text};--side-heading:{side_heading};
--side-accent:{side_accent};--track:{_mix(c['primary'], c['page_bg'], 0.8)};--side-track:{_mix(side_text, side_bg, 0.8)};
--rule:{_mix(c['heading'], c['page_bg'], 0.65)};--side-rule:{_mix(side_heading, side_bg, 0.6)};--tint:{_mix(c['primary'], '#ffffff', 0.86)};
--sw:{sw}%;--s:{scale:.3f}}}
@page{{size:A4;margin:0}}
*{{box-sizing:border-box}}
html,body{{margin:0;padding:0;background:var(--page)}}
body{{width:210mm;font-family:{body_font};color:var(--text);font-size:calc(9.6pt*var(--s));line-height:1.42;
-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.side-bg{{position:fixed;top:0;bottom:0;left:0;width:var(--sw);background:var(--side);z-index:0}}
.lay-sidebar_right .side-bg{{left:auto;right:0}}
header,.cols{{position:relative;z-index:1}}
.cols{{display:flex;align-items:flex-start}}
.lay-sidebar_right .cols{{flex-direction:row-reverse}}
aside{{width:var(--sw);flex:none;padding:8mm 5.5mm 10mm 8mm;color:var(--side-text);-webkit-box-decoration-break:clone;box-decoration-break:clone}}
.lay-sidebar_right aside{{padding:8mm 8mm 10mm 6mm}}
main{{flex:1;min-width:0;padding:8mm 9mm 10mm 9mm;-webkit-box-decoration-break:clone;box-decoration-break:clone}}
.lay-single_column main{{padding:8mm 15mm 12mm}}
h2,.nm,.ttl,.comp-t,.job-role{{font-family:{head_font}}}
.sec{{margin-bottom:calc(6.5mm*var(--s))}}
.sec h2{{color:var(--heading);font-size:calc(15pt*var(--s));font-weight:700;text-transform:uppercase;margin:0 0 3.2mm;line-height:1.08;
letter-spacing:.3px;break-after:avoid;{h2}}}
aside .sec h2{{color:var(--side-heading)}}
{side_h2_fix}
.sec p{{margin:0 0 2.4mm}}
aside .sec{{font-size:calc(9.2pt*var(--s))}}
ul{{margin:0;padding-left:4.2mm}}
li{{margin-bottom:1mm}}
.bul li::marker{{color:var(--accent)}}
aside .bul{{font-size:calc(8.6pt*var(--s))}}
.ic-list{{list-style:none;padding:0}}
.ic-list li{{display:flex;gap:2.4mm;align-items:flex-start}}
.li-ic{{flex:none;padding-top:.5mm}}
.ct{{display:flex;gap:3mm;align-items:center;margin-bottom:2.2mm;font-size:calc(8.8pt*var(--s))}}
.ct-ic{{flex:none;display:flex}} .ct-v{{word-break:break-word}}
.venn{{width:100%;max-width:calc(95mm*var(--s));display:block;margin:0 auto 1mm;font-family:{head_font}}}
.addl{{text-align:center;margin-top:1mm}}
.addl-h{{font-family:{head_font};font-weight:700;color:var(--heading);font-size:calc(12.5pt*var(--s));margin-bottom:1mm}}
aside .addl-h{{color:var(--side-heading)}}
.addl-list{{font-size:calc(8.8pt*var(--s))}} .dot{{color:var(--heading);padding:0 .6mm}}
.bars .bar-row{{margin-bottom:2.3mm}} .bar-l{{font-size:calc(8.8pt*var(--s));margin-bottom:.8mm;font-weight:500}}
.bar-t{{height:2mm;border-radius:2mm;overflow:hidden}} .bar-f{{height:100%;border-radius:2mm}}
.dot-row{{display:flex;justify-content:space-between;align-items:center;margin-bottom:1.8mm;gap:2mm}}
.dot-set{{display:flex;gap:1.1mm}} .dot-set i{{width:2.4mm;height:2.4mm;border-radius:50%;display:block;background:var(--track)}}
.dot-set i.on{{background:var(--primary)}} aside .dot-set i.on{{background:var(--side-accent)}} aside .dot-set i:not(.on):not([style]){{background:var(--side-track)}}
.rings{{display:grid;grid-template-columns:repeat(3,1fr);gap:2mm;text-align:center;font-size:calc(8pt*var(--s))}}
.lay-single_column .rings{{grid-template-columns:repeat(6,1fr)}}
.ring{{width:13mm;height:13mm;display:block;margin:0 auto .8mm}}
.chips{{display:flex;flex-wrap:wrap;gap:1.6mm;margin-top:1.5mm}}
.chips span{{border:1px solid var(--rule);background:var(--tint);color:var(--text);padding:.7mm 2.4mm;border-radius:3mm;font-size:calc(8.4pt*var(--s))}}
aside .chips span{{background:transparent;border-color:var(--side-rule);color:var(--side-text)}}
.comp-grid{{display:grid;grid-template-columns:1fr 1fr;column-gap:6mm;row-gap:3.6mm}}
.comp{{display:flex;gap:2.6mm;break-inside:avoid}}
.comp-ic{{flex:none;width:9.5mm;height:9.5mm;border-radius:50%;border:1.6px solid var(--heading);background:var(--tint);display:flex;
align-items:center;justify-content:center}} .comp-ic svg{{width:4.8mm;height:4.8mm}}
.comp-t{{font-weight:700;color:var(--heading);font-size:calc(11pt*var(--s));line-height:1.15;margin-bottom:.6mm}}
.comp-d{{font-size:calc(8.3pt*var(--s));text-align:left;color:var(--muted);line-height:1.38}}
.comp-list li{{margin-bottom:1.6mm}}
.timeline{{border-left:2px solid var(--heading);padding-left:4.5mm;margin-left:1mm}}
.job{{margin-bottom:4mm;position:relative}} .job li{{break-inside:avoid}} .job-top,.job-co{{break-after:avoid}}
.timeline .job::before{{content:"";position:absolute;left:-6.5mm;top:1.2mm;width:2.6mm;height:2.6mm;border-radius:50%;background:var(--page);
border:2px solid var(--heading)}}
.job-top{{display:flex;justify-content:space-between;gap:3mm;align-items:baseline}}
.job-role{{font-weight:700;color:var(--heading);font-size:calc(11pt*var(--s))}}
.job-period{{font-weight:700;font-size:calc(8.8pt*var(--s));white-space:nowrap}}
.job-co{{color:var(--accent);font-weight:600;font-size:calc(9.2pt*var(--s));margin-bottom:1mm}}
.job ul{{font-size:calc(9pt*var(--s))}}
.edu{{margin-bottom:2.6mm;break-inside:avoid}} .edu-deg{{font-weight:700}} .edu-inst{{font-weight:500}} .edu-meta{{color:var(--muted);font-size:.92em}}
aside .edu-meta{{color:var(--side-text);opacity:.8}}
.proj{{margin-bottom:2.4mm}} .proj b{{color:var(--heading)}}
.nm{{font-weight:800;line-height:1.02;letter-spacing:.4px}}
.ttl{{font-weight:600;font-size:calc(12.5pt*var(--s));line-height:1.18;margin-top:2.2mm;letter-spacing:.3px}}
.hd-diag{{display:flex;height:calc(84mm*(0.4 + 0.6*var(--s)));clip-path:polygon(0 0,100% 0,100% 62%,0 100%)}}
.hd-photo{{width:var(--pw);flex:none;height:100%;background-size:cover;background-position:center 20%}}
.hd-banner{{flex:1;background:var(--primary);color:var(--on-primary);text-align:center;padding:13mm 8mm 0;display:flex;flex-direction:column;align-items:center}}
.hd-banner .ttl{{font-size:calc(14pt*var(--s))}}
.hd-band{{background:var(--primary);color:var(--on-primary);display:flex;align-items:center;gap:7mm;padding:11mm 12mm}}
.hd-center{{text-align:center;padding:13mm 15mm 4mm;color:var(--heading)}}
.hd-center .ttl{{color:var(--accent);letter-spacing:2px}}
.hd-center::after{{content:"";display:block;width:24mm;height:2px;background:var(--primary);margin:5mm auto 0}}
.hd-left{{display:flex;align-items:center;justify-content:space-between;padding:12mm 9mm 6mm calc(var(--sw) + 9mm);color:var(--heading)}}
.lay-single_column .hd-left{{padding:12mm 15mm 4mm}}
.hd-left .ttl{{color:var(--primary)}}
.hd-avatar{{flex:none;width:32mm;height:32mm;background-size:cover;background-position:center 20%;border-radius:{photo_radius};
border:2.5px solid var(--on-primary)}}
.hd-center .hd-avatar{{margin:0 auto 4mm;border-color:var(--primary)}} .hd-left .hd-avatar{{border-color:var(--primary)}}
.side-top{{text-align:center;margin-bottom:7mm}}
.side-top .hd-avatar{{margin:0 auto 5mm;width:38mm;height:38mm;border-color:var(--side-accent)}}
.side-top .nm{{color:var(--side-heading)}} .side-top .ttl{{color:var(--side-accent)}}
.ph-empty{{display:flex;align-items:center;justify-content:center;background:{_mix(c['primary'], '#000000', 0.25)};color:#fff;
font-family:{head_font};font-weight:700;font-size:26pt}}
.hd-photo.ph-empty{{background:{_mix(c['primary'], '#000000', 0.3)};font-size:40pt}}
"""


def _placement(d: dict) -> tuple[list[str], list[str]]:
    """Design's column lists + every other section (content or not) appended where it fits best."""
    lay = d["layout"]
    side_secs = list(d.get("sidebar_sections", [])) if lay != "single_column" else []
    main_secs = list(d.get("main_sections", []))
    placed = set(side_secs) | set(main_secs)
    for key in SECTION_KEYS:      # anything with content but no slot in the design still gets printed
        if key not in placed:
            (side_secs if (lay != "single_column" and key in _SIDEBAR_FRIENDLY - {"skills", "profile"}) else main_secs).append(key)
    return side_secs, main_secs


def _render_html(c: dict, d: dict, photo_uri: str, scale: float = 1.0) -> str:
    _, _, gfont = _FONTS.get(d["font"], _FONTS["sans"])
    lay = d["layout"]
    side_secs, main_secs = _placement(d)
    side_html = "".join(_section_html(k, c, d, True) for k in side_secs)
    main_html = "".join(_section_html(k, c, d, False) for k in main_secs)
    top = ""
    if d["header"] == "sidebar_name" and lay != "single_column":
        name = c["name"] or "Your Name"
        avail = 210 * d.get("sidebar_width", 32) / 100 - 14
        top = f'<div class="side-top">{_photo_html(photo_uri, name, d["photo"], "hd-avatar")}{_name_block(c, d, _name_size(name, avail * 1.5, 22))}</div>'
    body = (f'<div class="cols"><main>{main_html}</main></div>' if lay == "single_column" else
            f'<div class="side-bg"></div><div class="cols"><aside>{top}{side_html}</aside><main>{main_html}</main></div>')
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{_e(c["name"] or "Resume")} — Resume</title>'
            f'<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family={gfont}&display=swap" rel="stylesheet">'
            f'<style>{_css(d, scale)}</style></head><body class="lay-{lay}">{_header_html(c, d, photo_uri)}{body}</body></html>')


def _data_uri(path: str) -> str:
    try:
        ext = os.path.splitext(path)[1].lower().lstrip(".") or "png"
        mime = "image/jpeg" if ext in ("jpg", "jpeg") else f"image/{ext}"
        with open(path, "rb") as f:
            return f"data:{mime};base64," + base64.b64encode(f.read()).decode()
    except Exception:
        return ""


def _launch(pw):
    try:
        return pw.chromium.launch(headless=True)
    except Exception:
        return pw.chromium.launch(headless=True, channel="msedge")


def _render_files(c: dict, d: dict, photo_path: str, stem: str) -> dict:
    """HTML → PDF (auto-shrinks to avoid a nearly-empty last page) → PNG previews."""
    from playwright.sync_api import sync_playwright
    os.makedirs(OUT_DIR, exist_ok=True)
    photo_uri = _data_uri(photo_path) if photo_path else ""
    pdf_path = os.path.join(OUT_DIR, stem + ".pdf")
    html_path = os.path.join(OUT_DIR, stem + ".html")
    import fitz
    wd = json.loads(json.dumps(d))       # working copy: sections may be moved between columns to fit
    if wd["layout"] != "single_column":
        wd["sidebar_sections"], wd["main_sections"] = _placement(wd)
    moved: set[str] = set()              # never move a section back (stops ping-pong)
    pdf_opts = dict(format="A4", print_background=True, margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
    with sync_playwright() as pw:
        browser = _launch(pw)
        try:
            page = browser.new_page(viewport={"width": 794, "height": 1123})
            page.emulate_media(media="print")
            scale, html, pdf_bytes, moves = 1.0, "", b"", 0
            for _ in range(8):
                html = _render_html(c, wd, photo_uri, scale)
                page.set_content(html, wait_until="domcontentloaded")
                try:
                    page.wait_for_load_state("networkidle", timeout=8000)
                except Exception:
                    pass
                try:
                    page.evaluate("document.fonts.ready.then(() => true)")
                except Exception:
                    pass
                pdf_bytes = page.pdf(**pdf_opts)
                doc = fitz.open(stream=pdf_bytes, filetype="pdf")
                pages = len(doc)
                last = doc[-1]
                fill = max([b[3] for b in last.get_text("blocks")] or [0]) / last.rect.height
                doc.close()
                if os.environ.get("RESUME_DEBUG"):
                    print(f"[resume] fit: pages={pages} fill={fill:.2f} scale={scale:.2f} side={wd.get('sidebar_sections')} main={wd.get('main_sections')}")
                if pages == 1 or (pages == 2 and fill > 0.45):
                    break
                # 1) move a section from the end of the longer column to the shorter one
                if wd["layout"] != "single_column" and moves < 4:
                    side_h, main_h = page.evaluate("[document.querySelector('aside')?.scrollHeight||0, document.querySelector('main')?.scrollHeight||0]")
                    if side_h + 60 < main_h:
                        movable = [k for k in reversed(wd["main_sections"]) if k in _SIDEBAR_FRIENDLY - {"skills", "profile"}
                                   and k not in moved and _section_html(k, c, wd, True)]
                        src, dst = "main_sections", "sidebar_sections"
                    elif main_h + 60 < side_h:
                        movable = [k for k in reversed(wd["sidebar_sections"]) if k not in ("contact", "profile")
                                   and k not in moved and _section_html(k, c, wd, False)]
                        src, dst = "sidebar_sections", "main_sections"
                    else:
                        movable = []
                    if movable:
                        wd[src].remove(movable[0])
                        wd[dst].append(movable[0])
                        moved.add(movable[0])
                        moves += 1
                        continue
                # 2) otherwise shrink the type a little
                if scale - 0.04 < 0.8:
                    break
                scale -= 0.04
        finally:
            browser.close()
    with open(pdf_path, "wb") as f:
        f.write(pdf_bytes)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    pngs = []
    try:
        import fitz
        doc = fitz.open(pdf_path)
        for i, pg in enumerate(doc):
            if i >= 3:
                break
            out = os.path.join(OUT_DIR, f"{stem}_p{i + 1}.png")
            pg.get_pixmap(matrix=fitz.Matrix(1.6, 1.6)).save(out)
            pngs.append(out)
        n_pages = len(doc)
        doc.close()
    except Exception as e:
        print(f"[resume] preview failed: {e}")
        n_pages = 0
    return {"pdf": pdf_path, "html": html_path, "pngs": pngs, "pages": n_pages}


# ── Routing helpers (used by chat.py) ───────────────────────────────────────────────────────────
_NOUN = r"(?:r[eé]sum[eé]s?|\bcv\b|curriculum\s+vitae|bio-?data)"
_CREATE_RX = re.compile(r"\b(?:create|make|build|generate|design|prepare|write|draft|craft|recreate|replicate|copy|redo|"
                        r"format|banao|bana\s*do|bana)\b[^.\n]{0,70}?" + _NOUN, re.I)
_LIKE_RX = re.compile(_NOUN + r"\s+(?:like|same|similar|exactly|based\s+on|from\s+(?:this|the)|using\s+(?:this|the|my)|"
                      r"with\s+(?:these|this|my|the\s+following|following)|in\s+(?:this|the\s+same|same)|for\s+me)", re.I)
_TOOL_RX = re.compile(_NOUN + r"\s+(?:template|format|design|maker|builder|creator|generator)s?\b|"
                      r"\b(?:need|want|get\s+me|give\s+me)\s+(?:a|an|my|new|a\s+new)\s+(?:professional\s+|creative\s+)?" + _NOUN + "|"
                      + _NOUN + r"[^.\n]{0,40}?\b(?:bana\s*do|banado|banao|bana\s+de|bana\s+dijiye|taiyar\s+karo)\b", re.I)
# Another artifact named BEFORE the resume noun means the resume is only the topic ("make a ppt on resumes").
# Order matters: resume details routinely contain "email", "presentation skills", "LinkedIn"...
_OTHER_ARTIFACT_RX = re.compile(r"\b(?:ppt|presentation|slides?|deck|powerpoint|essay|cover\s+letter|e-?mail\s+(?:to|for)|linkedin\s+post)\b", re.I)
_EDIT_RX = re.compile(r"\b(?:change|update|edit|modify|add|remove|delete|replace|fix|switch|make|put|shorten|improve|redo|regenerate)\b"
                      r"[^.\n]{0,80}?\b(?:my|the|this|that)\s+" + _NOUN, re.I)
_MEDIA_RX = re.compile(r"\bresume\s+(?:the\s+|my\s+)?(?:music|song|video|playback|playing|track|spotify|youtube|task|work|"
                       r"download|it|that|this|where|from\s+where|reading|game)\b", re.I)
_TEMPLATE_RX = re.compile(r"\b(" + "|".join(PRESETS) + r")\b(?:\s+(?:template|format|style|design|layout|theme))?", re.I)
_COLOR_RX = re.compile(r"\b(" + "|".join(sorted(_NAMED_COLORS, key=len, reverse=True)) + r"|#[0-9a-f]{6})\b"
                       r"(?:\s+(?:colou?r|theme|tone|accent|shade))?", re.I)


def _attachments(prompt: str) -> list[tuple[str, str]]:
    out = []
    for raw in re.findall(r"\[ATTACHED_FILE:\s*(.+?)\]", prompt, re.I):
        parts = raw.split("|")
        path = parts[0].strip()
        desc = ""
        for p in parts[1:]:
            if p.strip().upper().startswith("DESCRIPTION:"):
                desc = p.split(":", 1)[1].strip()
        out.append((path, desc))
    return out


def _split_images(prompt: str) -> tuple[str, str]:
    """→ (reference_image, photo). A photo is labelled as such or is a close-up face."""
    imgs = [(p, d) for p, d in _attachments(prompt) if p.lower().endswith(_IMG_EXTS) and os.path.exists(p)]
    ref, photo = "", ""
    for p, d in imgs:
        label = f"{d} {os.path.basename(p)}".lower()
        is_photo = bool(re.search(r"\b(photo|pic|picture|headshot|selfie|profile\s*pic|dp|my\s+image)\b", label))
        if not is_photo and not re.search(r"\b(resume|cv|template|format|design|reference|sample)\b", label):
            is_photo = _face_ratio(p) > 0.12
        if is_photo and not photo:
            photo = p
        elif not ref:
            ref = p
        elif not photo:
            photo = p
    return ref, photo


def _strip_tags(prompt: str) -> str:
    text = re.sub(r"\[ATTACHED_FILE:.*?\]", "", prompt, flags=re.I)
    return text.strip()


def _has_details(text: str) -> bool:
    t = text.lower()
    signals = sum([
        bool(re.search(r"[\w.+-]+@[\w-]+\.\w+", t)),
        bool(re.search(r"\+?\d[\d\s-]{8,}\d", t)),
        bool(re.search(r"\b(experience|worked|working|years?|education|degree|b\.?tech|mba|graduat|college|university|"
                       r"school|skills?|manager|engineer|developer|intern|company|achievement|certific|name\s*(?:is|:))\b", t)),
        len(t) > 220,
        t.count("\n") >= 3,
    ])
    return signals >= 2


def resume_awaiting_details() -> bool:
    st = _load_state()
    return bool(st.get("awaiting_details")) and time.time() - float(st.get("awaiting_since") or 0) < _AWAIT_TTL


def detect_resume_request(prompt: str) -> dict | None:
    """Fast regex router → create_resume kwargs (or {"_list": True}), else None."""
    try:
        text = _strip_tags(prompt)
        lower = text.lower()
        if re.search(r"\b(?:list|show|what|which)\b[^.\n]{0,30}" + _NOUN + r"\s+(?:templates?|formats?|styles?|designs?)", lower):
            return {"_list": True}
        noun_m = re.search(_NOUN, lower)
        other_m = _OTHER_ARTIFACT_RX.search(lower)
        if other_m and (not noun_m or other_m.start() < noun_m.start()):
            return None
        # the UI's "Resume Design Image" / "Resume Photo" uploads are labelled → always a resume request
        labelled = any(re.search(r"r[eé]sum[eé]|\bcv\b", d.lower()) for _, d in _attachments(prompt))
        if _MEDIA_RX.search(lower) and not re.search(r"\bcv\b|curriculum|bio-?data|\b(?:a|my|the|this)\s+r[eé]sum[eé]\b", lower):
            return None
        state = _load_state()
        ref, photo = _split_images(prompt)
        tpl_m = _TEMPLATE_RX.search(lower)
        template = tpl_m.group(1).lower() if tpl_m and (tpl_m.group(0) != tpl_m.group(1) or
                                                         re.search(r"\b(template|format|style)\b", lower)) else ""
        col_m = _COLOR_RX.search(lower)
        color = ""
        if col_m and re.search(r"\b(colou?r|theme|tone|shade|accent)\b", lower):
            color = col_m.group(1).lower()
        args = {"details": "", "image_path": ref, "photo_path": photo, "template": template, "color": color,
                "instruction": "", "reuse_photo": bool(re.search(r"\b(same|that|this|existing|original)\s+(photo|pic|picture|image of me)\b|"
                                                                r"\b(keep|use)\s+(the\s+)?(photo|pic|picture)\b", lower))}
        create = bool(labelled or _CREATE_RX.search(lower) or _LIKE_RX.search(lower) or _TOOL_RX.search(lower)
                      or ((template or color) and re.search(_NOUN, lower)))
        edit = bool(_EDIT_RX.search(lower)) and bool(state.get("content"))
        if create and not (edit and not ref and not _has_details(text) and re.search(r"\b(my|the|this)\s+" + _NOUN, lower)
                           and not re.search(r"\b(new|another|fresh)\b", lower)):
            args["details"] = text
            return args
        if edit:
            args["instruction"] = text
            return args
        if resume_awaiting_details() and (_has_details(text) or ref or photo):
            args["details"] = text
            return args
        return None
    except Exception as e:
        print(f"[resume] detect failed: {e}")
        return None


def list_resume_templates() -> str:
    rows = "\n".join(f"- **{k}** — {v}" for k, v in PRESET_BLURBS.items())
    return ("Resume formats I can build, Sir:\n" + rows +
            "\n\nOr upload a picture of ANY resume and say *\"make my resume like this\"* with your details — I'll copy its design.")


# ── Tool entry point ────────────────────────────────────────────────────────────────────────────
def create_resume(details: str = "", image_path: str = "", photo_path: str = "", template: str = "", color: str = "",
                  instruction: str = "", reuse_photo: bool = False, open_file: bool = False):
    """Generator: progress lines, then markdown with PNG preview(s) + PDF/HTML links."""
    try:
        state = _load_state()
        tags_img, tags_photo = _split_images(details or instruction or "")
        image_path = image_path or tags_img
        photo_path = photo_path or tags_photo
        details = _strip_tags(details or "")
        instruction = _strip_tags(instruction or "")
        if image_path and not os.path.exists(image_path):
            yield f"I couldn't find the image at {image_path}, Sir."
            return

        if (template or "").lower() not in ("",) and template.lower() not in PRESETS:
            template = ""

        # 1) Design
        if image_path:
            yield "🎨 Studying the design of your reference resume (layout, colours, header, sections)…\n\n"
        design, design_note = _resolve_design(image_path, template, color, state.get("design"))

        # 2) Content
        content = None
        clean_details = re.sub(r"(?i)^.*?\b(?:create|make|build|generate|design|prepare|write|recreate)\b[^.\n:]{0,80}?" + _NOUN +
                               r"[^.\n:]{0,60}[:.\-]?\s*", "", details, count=1).strip() if details else ""
        has_new_details = _has_details(clean_details) or len(clean_details) > 120
        if instruction and state.get("content") and not has_new_details:
            if image_path or template or color:
                content = state["content"]
                if not re.fullmatch(r"[^.\n]{0,40}\b(colou?r|template|format|style|design|theme)\b[^.\n]{0,60}", instruction.lower()):
                    yield "✍️ Applying your changes…\n\n"
                    content = _edit_content(state["content"], instruction)
            else:
                yield "✍️ Applying your changes…\n\n"
                content = _edit_content(state["content"], instruction)
        elif has_new_details:
            yield "✍️ Structuring your details into resume sections…\n\n"
            content = _build_content(clean_details or details, design)
        elif state.get("content") and (image_path or template or color or re.search(r"\b(again|same|my)\b", details.lower())):
            content = state["content"]
        if not content or not (content.get("name") or content.get("experience") or content.get("profile")):
            state.update({"design": design, "awaiting_details": True, "awaiting_since": time.time(),
                          "ref_image": image_path or state.get("ref_image", ""), "photo": photo_path or state.get("photo", ""),
                          "reuse_photo": reuse_photo or state.get("reuse_photo", False)})
            _save_state(state)
            yield (f"{design_note}\n\nNow send me your details, Sir — name, headline/title, phone, email, profile summary, "
                   "skills, work experience (role, company, years, key points), education, achievements. "
                   "Paste them as plain text or attach a PDF/DOCX; attach a photo too if you want one on the resume.")
            return

        # 3) Photo
        photo = photo_path or ""
        ref_for_photo = image_path or state.get("ref_image", "")
        if not photo and (reuse_photo or state.get("reuse_photo")) and ref_for_photo:
            photo = _crop_photo(ref_for_photo, design.get("photo_bbox"))
        if not photo and not (image_path or photo_path) and state.get("photo") and os.path.exists(state["photo"]):
            photo = state["photo"]

        # 4) Render
        yield "🖨️ Typesetting and rendering the PDF…\n\n"
        slug = re.sub(r"[^a-z0-9]+", "_", (content.get("name") or "resume").lower()).strip("_")[:30] or "resume"
        stem = f"resume_{slug}_{int(time.time())}"
        files = _render_files(content, design, photo, stem)

        state.update({"design": design, "content": content, "awaiting_details": False, "photo": photo,
                      "ref_image": ref_for_photo, "reuse_photo": False, "last_pdf": files["pdf"], "updated": time.time()})
        _save_state(state)
        if open_file:
            try:
                os.startfile(files["pdf"])
            except Exception:
                pass

        name = os.path.basename
        previews = "\n\n".join(f"![Resume page {i + 1}]({MEDIA_URL}/{name(p)})" for i, p in enumerate(files["pngs"]))
        missing = []
        if design["photo"] != "none" and not photo:
            missing.append("attach a photo (or say *\"use the same photo\"*) to replace the initials block")
        tips = ("\n\n_" + "; ".join(missing) + "._") if missing else ""
        yield (f"Your resume is ready, Sir. {design_note} {files['pages']} page(s).\n\n{previews}\n\n"
               f"📄 [Download PDF]({MEDIA_URL}/{name(files['pdf'])}) · 🌐 [Editable HTML]({MEDIA_URL}/{name(files['html'])})\n\n"
               f"Saved to `{files['pdf']}`. Say things like *\"change the resume colour to navy\"*, *\"use the modern template\"* "
               f"or *\"add AWS certification to my resume\"* to tweak it.{tips}")
    except Exception as e:
        import traceback
        traceback.print_exc()
        yield f"Sorry Sir, the resume builder hit a problem: {e}"


def resume_tool(details: str = "", image_path: str = "", photo_path: str = "", template: str = "", color: str = "",
                instruction: str = "", reuse_photo: bool = False):
    """Registry entry: also handles a bare 'list templates' request."""
    if not any([details, image_path, photo_path, template, color, instruction]) and not _load_state().get("content"):
        yield list_resume_templates()
        return
    yield from create_resume(details=details, image_path=image_path, photo_path=photo_path, template=template,
                             color=color, instruction=instruction, reuse_photo=reuse_photo)
