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
import contextvars
import hashlib
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
    "wave": {
        "layout": "two_column", "sidebar_width": 50, "header": "full_band", "header_shape": "wave", "photo": "circle",
        "photo_position": "right", "photo_ring": True, "name_align": "center", "footer_shape": "wave", "decor": "none",
        "font": "modern", "name_case": "title", "heading_style": "square_icon", "skills_style": "bars",
        "language_style": "bars", "competency_style": "list", "timeline": False,
        "colors": {"primary": "#29abd4", "accent": "#1f9cc7", "heading": "#1f9cc7", "text": "#4b5563",
                   "sidebar_bg": "#ffffff", "page_bg": "#ffffff", "header_text": "#ffffff", "track": "#1f2937",
                   "skill_colors": ["#29abd4", "#1f9cc7", "#7dd3ea"]},
        "sidebar_sections": ["profile", "education", "experience", "projects"],
        "main_sections": ["skills", "languages", "competencies", "achievements", "certifications", "highlights", "interests", "references"],
        "bottom_sections": ["contact"],
    },
    "corporate": {
        "layout": "sidebar_left", "sidebar_width": 33, "header": "sidebar_photo", "photo": "circle",
        "font": "serif", "name_case": "upper", "heading_style": "underline", "skills_style": "bars",
        "language_style": "squares", "competency_style": "list", "timeline": False,
        "colors": {"primary": "#1e88d0", "accent": "#1565c0", "heading": "#0b2a4a", "text": "#333333",
                   "sidebar_bg": "#0b2d55", "page_bg": "#ffffff", "header_text": "#ffffff", "band": "#f1f1f1",
                   "skill_colors": ["#1e88d0", "#1565c0", "#90caf9"]},
        "sidebar_sections": ["contact", "skills", "languages", "interests", "certifications"],
        "main_sections": ["profile", "experience", "projects", "education", "achievements", "highlights", "competencies", "references"],
        "bottom_sections": [],
    },
}
PRESET_BLURBS = {
    "elegant": "gold diagonal banner + photo, light sidebar, Venn skills, icon competencies",
    "modern": "dark navy sidebar with photo & name, skill bars, clean timeline",
    "minimal": "single column, serif, centred name, ATS-friendly",
    "creative": "teal header band, coral accents, right sidebar, skill dots",
    "executive": "charcoal & gold, rounded photo, skill rings",
    "tech": "monospace headings, dark sidebar, skill bars",
    "wave": "wavy colour header & footer, round photo with ring, two equal columns, language bars",
    "corporate": "navy sidebar with round photo, name on a grey band, serif headings, skill bars, square language markers",
}

# Optional design keys (added 2026-10-02): every design gets these, so old saved designs keep working.
_STYLE_DEFAULTS = {"header_shape": "flat", "footer_shape": "none", "photo_position": "left", "photo_ring": False,
                   "name_align": "left", "language_style": "dots", "decor": "none", "bottom_sections": [],
                   "page_inset": [0, 0, 0, 0], "band_inset": [], "header_accent": "none", "column_divider": False,
                   "item_rules": False, "skills_columns": 1}

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


UNDO_PATH = os.path.join(_BASE_DIR, "app", "memory", "resume_undo.json")
_UNDO_KEYS = ("content", "design", "photo", "target_pages", "render_scale")


def _state_rev(st: dict) -> str:
    """Fingerprint of what the editor shows; its client-side undo history is only valid for this exact state."""
    blob = json.dumps([st.get(k) for k in ("content", "design", "photo")], sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha1(blob.encode("utf-8")).hexdigest()[:16]


def _undo_snap(st: dict) -> dict:
    return json.loads(json.dumps({k: st.get(k) for k in _UNDO_KEYS}, default=str))


def _undo_push(snap: dict) -> str:
    """Store a whole editor state (before a structural change); returns its id for the editor's history."""
    try:
        with open(UNDO_PATH, "r", encoding="utf-8") as f:
            snaps = json.load(f).get("snaps") or []
    except Exception:
        snaps = []
    sid = f"u{int(time.time() * 1000):x}{len(snaps) % 100}"
    snaps = (snaps + [{"id": sid, **snap}])[-40:]
    try:
        os.makedirs(os.path.dirname(UNDO_PATH), exist_ok=True)
        with open(UNDO_PATH, "w", encoding="utf-8") as f:
            json.dump({"snaps": snaps}, f, ensure_ascii=False)
    except Exception as e:
        print(f"[resume] could not save undo snapshot: {e}")
        return ""
    return sid


def _undo_get(sid: str) -> dict | None:
    try:
        with open(UNDO_PATH, "r", encoding="utf-8") as f:
            return next((x for x in json.load(f).get("snaps") or [] if x.get("id") == sid), None)
    except Exception:
        return None


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
 "layout": "sidebar_left|sidebar_right|two_column|single_column",
 "sidebar_width": <percent of page width taken by the left/narrow column, 25-50; 0 for single_column>,
 "header": "diagonal_banner|full_band|centered|left_plain|sidebar_name|sidebar_photo",
 "header_shape": "flat|wave|curve|diagonal" <shape of the coloured header's bottom edge>,
 "footer_shape": "none|wave|curve|bar" <decorative coloured shape along the page bottom>,
 "photo": "square|circle|rounded|none",
 "photo_position": "left|right|center",
 "photo_ring": true|false <coloured ring/border around the photo>,
 "name_align": "left|center",
 "decor": "none|circles|dots" <faint background decorations>,
 "header_accent": "none|left_bar" <a solid dark vertical bar at the left end of the header band>,
 "column_divider": true|false <thin vertical line between the two columns>,
 "item_rules": true|false <thin horizontal lines between contact/list rows>,
 "skills_columns": 1|2 <skills laid out in two columns>,
 "photo_bbox": [x0, y0, x1, y1] <photo position as fractions 0-1 of the WHOLE image, or null>,
 "font": "sans|geometric|modern|serif|elegant|mono",
 "name_case": "upper|title",
 "heading_style": "underline|bar_left|boxed|caps_line|plain|square_icon|dot",
 "skills_style": "venn|bars|dots|chips|circles|list",
 "language_style": "bars|dots|squares|text",
 "competency_style": "icon_grid|list",
 "timeline": true|false,
 "colors": {{"primary": "<header/banner colour>", "accent": "<secondary accent>", "heading": "<section heading text colour>",
             "text": "<body text>", "sidebar_bg": "<sidebar background>", "page_bg": "<main page background>",
             "header_text": "<text colour on the header>", "skill_colors": ["<up to 3 colours used in the skills graphic>"],
             "track": "<colour of empty progress-bar tracks, if any>",
             "band": "<background colour behind the name if it sits on its own light band, else empty>"}},
 "sidebar_sections": [<ordered section keys printed in the sidebar>],
 "main_sections": [<ordered section keys in the main column; for single_column, every section>],
 "section_titles": {{"<key>": "<heading text exactly as printed>"}},
 "notes": "<one sentence on distinctive design details>"
}}
Section keys: profile, highlights, contact, skills, competencies, experience, education, achievements, certifications, languages, interests, projects, references.
("highlights" = career highlights/summary bullets, "competencies" = core competencies/expertise blocks with icons.)
Layout: sidebar_* = one narrow column with its own background colour; two_column = two similar-width columns on the same background.
Header meanings: diagonal_banner = coloured banner with a slanted bottom edge next to/over a photo; full_band = coloured band across the top
(set header_shape: wave = wavy bottom edge, curve = one smooth arc, diagonal = straight slant, flat = straight);
centered = name centred on plain background; left_plain = name left-aligned on plain background; sidebar_name = name printed inside the sidebar;
sidebar_photo = PHOTO at the top of the sidebar while the NAME sits at the top of the main column (often on a light band).
Look carefully where the photo is: if it is inside the coloured sidebar, the header is sidebar_photo or sidebar_name, not left_plain.
heading_style: square_icon = small filled square before each heading; dot = filled circle before each heading.
skills_style: venn = overlapping circles; bars = progress bars; dots = rating dots; circles = ring charts; chips = tags; list = plain list.
Choose colours from the measured list whenever they match."""


# A focused second look: the small VLM gets columns/section placement right far more often
# when asked only this (the big style prompt alone tends to answer "single_column").
_LAYOUT_PROMPT = """Look at this resume page (ignore phone UI bars and viewer background). List every section heading in
reading order and say which column it is in.
Return ONLY JSON: {"columns": 1 or 2, "equal_columns": true|false, "narrow_column": "left|right|none",
"narrow_column_width_percent": <n>, "left_column_has_own_background": true|false,
"sections": [{"title": "<heading text>", "column": "left|right|full"}],   ("full" = spans the whole page width, e.g. a contact strip at the bottom)
"heading_text_color": "<hex of section heading text such as PROFILE>", "skill_graphic_colors": ["<hex>", "<hex>", "<hex>"],
"banner_color": "<hex of the header/banner background>", "name_color": "<hex of the person's name text>"}"""

_TITLE_KEYS = [
    (r"profile|summary|about|objective|introduction|overview", "profile"), (r"highlight|key\s+facts|at\s+a\s+glance", "highlights"),
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
    narrow = str(lay.get("narrow_column") or "").lower()
    cols2 = str(lay.get("columns")) == "2"
    equal = lay.get("equal_columns") is True or (cols2 and narrow not in ("left", "right")) or         (cols2 and lay.get("left_column_has_own_background") is False and narrow != "right")
    side_col = "left" if (equal or narrow not in ("left", "right")) else narrow
    side, main, bottom, titles = [], [], [], {}
    last_col_idx = max([i for i, s in enumerate(secs) if str(s.get("column")).lower() in ("left", "right")] or [-1])
    for i, s in enumerate(secs):
        key = _title_key(s.get("title", ""))
        if not key or key in side or key in main or key in bottom:
            continue
        titles[key] = str(s.get("title") or "").strip()[:40]
        col = str(s.get("column")).lower()
        if not cols2:
            main.append(key)
        elif col == "full":
            (bottom if i > last_col_idx >= 0 else main).append(key)
        else:
            (side if col == side_col else main).append(key)
    if secs:
        spec["section_titles"] = {**(spec.get("section_titles") or {}), **titles}
    if cols2 and side and main:
        spec["layout"] = "two_column" if equal else ("sidebar_left" if narrow == "left" else "sidebar_right")
        spec["sidebar_sections"], spec["main_sections"], spec["bottom_sections"] = side, main, bottom
        try:
            spec["sidebar_width"] = 50 if equal else int(float(lay.get("narrow_column_width_percent") or spec.get("sidebar_width") or 32))
        except Exception:
            pass
    elif secs and not cols2:
        spec["layout"], spec["sidebar_sections"], spec["main_sections"], spec["bottom_sections"] = "single_column", [], main, []
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


def _pixel_colors(image_path: str, colors: dict, spec: dict) -> dict:
    """Real colours of page / side column / header band from the reference pixels (vision hexes drift, and a
    side column printed on the page colour must not become a filled sidebar)."""
    try:
        import cv2
        import numpy as np
        img = cv2.imread(image_path)
        if img is None:
            return {}
        h, w = img.shape[:2]
        f = 500 / max(w, 1)
        if f < 1:
            img = cv2.resize(img, (int(w * f), int(h * f)), interpolation=cv2.INTER_AREA)
        rgb = img[:, :, ::-1].astype(np.int32)

        def mode(px):
            if px.size == 0:
                return None
            q = (px.reshape(-1, 3) // 4) * 4
            vals, counts = np.unique(q, axis=0, return_counts=True)
            r, g, b = (int(v) + 2 for v in vals[counts.argmax()])
            return "#%02x%02x%02x" % (r, g, b)

        # page box: rows/cols that are mostly light or mostly the vision page colour
        light = rgb.mean(-1) > 200
        rows = np.where(light.mean(1) >= 0.35)[0]
        cols = np.where(light.mean(0) >= 0.35)[0]
        if len(rows) < 20 or len(cols) < 20:
            return {}
        page = rgb[rows[0]:rows[-1] + 1, cols[0]:cols[-1] + 1]
        ph, pw = page.shape[:2]
        out = {"page_bg": mode(page[int(ph * .3):int(ph * .95), int(pw * .45):int(pw * .95)])}
        lay = spec.get("layout")
        sw = (spec.get("sidebar_width") or 32) / 100
        if lay in ("sidebar_left", "sidebar_right"):
            x0, x1 = (0, int(pw * sw * .9)) if lay == "sidebar_left" else (int(pw * (1 - sw * .9)), pw)
            side = mode(page[int(ph * .3):int(ph * .95), x0:x1])
            if side:
                out["sidebar_bg"] = out["page_bg"] if np.linalg.norm(np.array(_rgb(side)) - np.array(_rgb(out["page_bg"]))) < 14 else side
        # a thin dark vertical line in the body = column divider → its x gives the real column split
        body = page[int(ph * .3):int(ph * .95)]
        page_lum = float(np.median(body.mean(-1)))
        dark_cols = np.where((body.mean(-1) < page_lum - 35).mean(0) >= 0.5)[0]   # clearly darker than the page
        dark_cols = [x for x in dark_cols if pw * .18 <= x <= pw * .6]
        if dark_cols and (dark_cols[-1] - dark_cols[0]) < pw * .02:
            out["_divider_pct"] = round(100 * float(np.mean(dark_cols)) / pw, 1)
        if spec.get("header") == "full_band" and spec.get("header_shape", "flat") in ("flat", None, ""):
            band = mode(page[int(ph * .01):int(ph * .12), int(pw * .25):int(pw * .7)])
            if band and np.linalg.norm(np.array(_rgb(band)) - np.array(_rgb(out["page_bg"]))) >= 8:
                out["header_bg"] = band
        return {k: v for k, v in out.items() if v}
    except Exception as e:
        print(f"[resume] pixel colours failed: {e}")
        return {}


def _measure_frame(image_path: str, colors: dict) -> list:
    """White frame around the coloured blocks (sidebar / header band) in the reference, as [top, right, bottom, left] mm.
    Measured from pixels, not guessed: the page is the area dominated by the design's own colours (phone status
    bars, toolbars and the viewer background drop out); an inset only counts on a side a coloured block runs along."""
    try:
        import cv2
        import numpy as np
        img = cv2.imread(image_path)
        if img is None:
            return [0, 0, 0, 0]
        h, w = img.shape[:2]
        f = 700 / max(w, 1)
        if f < 1:
            img = cv2.resize(img, (int(w * f), int(h * f)), interpolation=cv2.INTER_AREA)
        rgb = img[:, :, ::-1].astype(np.int32)

        def near(hexc: str, tol: int = 42):
            r, g, b = _rgb(hexc)
            return np.sqrt(((rgb - np.array([r, g, b])) ** 2).sum(-1)) < tol

        page_c = _hex(colors.get("page_bg") or "#ffffff", "#ffffff")
        blocks = [c for c in (colors.get("sidebar_bg"), colors.get("primary")) if c and _contrast(_hex(c), page_c) > 1.25]
        if not blocks:
            return [0, 0, 0, 0]
        colored = np.zeros(rgb.shape[:2], bool)
        for c in blocks:
            colored |= near(_hex(c))
        design = near(page_c) | colored
        rows = np.where(design.mean(1) >= 0.45)[0]
        cols = np.where(design.mean(0) >= 0.45)[0]
        if len(rows) < 20 or len(cols) < 20:
            return [0, 0, 0, 0]
        py0, py1, px0, px1 = rows[0], rows[-1] + 1, cols[0], cols[-1] + 1
        pw = px1 - px0
        sub = colored[py0:py1, px0:px1]
        ccols = np.where(sub.mean(0) >= 0.25)[0]          # columns mostly covered by a coloured block
        crows = np.where(sub.mean(1) >= 0.15)[0]
        if not len(ccols) or not len(crows):
            return [0, 0, 0, 0]
        mm = 210.0 / pw
        raw = [crows[0] * mm, (pw - 1 - ccols[-1]) * mm, (sub.shape[0] - 1 - crows[-1]) * mm, ccols[0] * mm]
        # < 0.8 mm = touching the edge; > 14 mm = that side has no block running along it (just content margin)
        return [round(float(v), 1) if 0.8 <= v <= 14 else 0 for v in raw]
    except Exception as e:
        print(f"[resume] frame measure failed: {e}")
        return [0, 0, 0, 0]


def _measure_band(image_path: str, colors: dict, layout: str) -> list:
    """Gaps around a light name band (e.g. grey box behind the name next to a sidebar), as
    [top, right, gap-to-sidebar] mm from the page edges / sidebar edge. [] when there is no such band."""
    try:
        import cv2
        import numpy as np
        band_c, page_c = colors.get("band"), _hex(colors.get("page_bg") or "#ffffff", "#ffffff")
        side_c = colors.get("sidebar_bg")
        if not band_c or not side_c or layout not in ("sidebar_left", "sidebar_right") or _contrast(_hex(band_c), page_c) < 1.03:
            return []
        img = cv2.imread(image_path)
        if img is None:
            return []
        h, w = img.shape[:2]
        f = 700 / max(w, 1)
        if f < 1:
            img = cv2.resize(img, (int(w * f), int(h * f)), interpolation=cv2.INTER_AREA)
        rgb = img[:, :, ::-1].astype(np.int32)

        def near(hexc: str, tol: int):
            r, g, b = _rgb(_hex(hexc))
            return np.sqrt(((rgb - np.array([r, g, b])) ** 2).sum(-1)) < tol

        side = near(side_c, 42)
        design = near(page_c, 42) | side
        rows = np.where(design.mean(1) >= 0.45)[0]
        cols = np.where(design.mean(0) >= 0.45)[0]
        if len(rows) < 20 or len(cols) < 20:
            return []
        py0, py1, px0, px1 = rows[0], rows[-1] + 1, cols[0], cols[-1] + 1
        pw, ph = px1 - px0, py1 - py0
        side_cols = np.where(side[py0:py1, px0:px1].mean(0) >= 0.5)[0]
        if not len(side_cols):
            return []
        # band colour from the pixels (vision hexes for near-white tones are unreliable): the dominant light,
        # non-page tone in the top quarter of the main column
        region = rgb[py0:py0 + ph // 4, px0:px1].copy()
        outside = np.ones(region.shape[:2], bool)
        if layout == "sidebar_left":
            outside[:, :side_cols[-1] + 1] = False
        else:
            outside[:, side_cols[0]:] = False
        pr, pg, pb = _rgb(page_c)
        dist_page = np.sqrt(((region - np.array([pr, pg, pb])) ** 2).sum(-1))
        lum = region.mean(-1)
        cand = outside & (dist_page > 6) & (dist_page < 70) & (lum > 170)
        if cand.sum() < 200:
            return []
        q = (region[cand] // 4) * 4                       # quantise, take the most common tone
        vals, counts = np.unique(q.reshape(-1, 3), axis=0, return_counts=True)
        r0, g0, b0 = (int(v) + 2 for v in vals[counts.argmax()])
        band_c = "#%02x%02x%02x" % (r0, g0, b0)
        top = near(band_c, 9)[py0:py0 + ph // 4, px0:px1] & outside
        bcols = np.where(top.mean(0) >= 0.25)[0]
        brows = np.where(top.mean(1) >= 0.3)[0]
        if len(bcols) < 10 or len(brows) < 5:
            return []
        mm = 210.0 / pw
        if layout == "sidebar_left":
            gap, right = bcols[0] - side_cols[-1] - 1, pw - 1 - bcols[-1]
        else:
            gap, right = side_cols[0] - bcols[-1] - 1, bcols[0]     # "right" = outer edge
        vals = [brows[0] * mm, right * mm, gap * mm]
        return [round(float(v), 1) if 0.8 <= v <= 14 else 0 for v in vals] + [band_c]
    except Exception as e:
        print(f"[resume] band measure failed: {e}")
        return []


def _analyse_design(image_path: str) -> dict:
    from concurrent.futures import ThreadPoolExecutor
    key = "v3:" + _file_hash(image_path)       # bump on vocabulary changes; v3 entries get pixel measurements added lazily
    cache = _load_state().get("design_cache") or {}
    if key and key in cache:                      # same picture again → no vision tokens spent
        spec = cache[key]
        if "page_inset" not in spec or "band_inset" not in spec:   # older reading: add pixel measurements (no vision call)
            spec["page_inset"] = _measure_frame(image_path, spec.get("colors") or {})
            spec["band_inset"] = _measure_band(image_path, spec.get("colors") or {}, spec.get("layout", ""))
            if len(spec["band_inset"]) == 4:
                spec.setdefault("colors", {})["band"] = spec["band_inset"].pop()
            st = _load_state()
            st.setdefault("design_cache", {})[key] = spec
            _save_state(st)
        return spec
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
    px = _pixel_colors(image_path, spec.get("colors") or {}, spec)
    div = px.pop("_divider_pct", None)
    if div:                                          # measured split beats the model's "equal columns"
        spec["column_divider"] = True
        if 22 <= div <= 44:
            if spec.get("layout") == "two_column":
                spec["layout"], px["sidebar_bg"] = "sidebar_left", px.get("page_bg") or (spec.get("colors") or {}).get("page_bg")
            if spec.get("layout") in ("sidebar_left", "sidebar_right"):
                spec["sidebar_width"] = int(round(div if spec["layout"] == "sidebar_left" else 100 - div))
    spec.setdefault("colors", {}).update({k: v for k, v in px.items() if v})
    spec["page_inset"] = _measure_frame(image_path, spec.get("colors") or {})
    spec["band_inset"] = _measure_band(image_path, spec.get("colors") or {}, spec.get("layout", ""))
    if len(spec["band_inset"]) == 4:                 # measured band colour beats the vision guess for near-white tones
        spec.setdefault("colors", {})["band"] = spec["band_inset"].pop()
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
        if spec.get("header_shape") not in (None, "", "flat") and spec.get("header_shape") == p.get("header_shape"):
            score += 3
        if score > best_score:
            best, best_score = name, score
    return best


_DESIGN_CHOICES = {          # every enum key of the design vocabulary + its allowed values (also used by the editor)
    "layout": {"sidebar_left", "sidebar_right", "single_column", "two_column"},
    "header": {"diagonal_banner", "full_band", "centered", "left_plain", "sidebar_name", "sidebar_photo"},
    "photo": {"square", "circle", "rounded", "none"},
    "font": set(_FONTS), "name_case": {"upper", "title"},
    "heading_style": {"underline", "bar_left", "boxed", "caps_line", "plain", "square_icon", "dot"},
    "skills_style": {"venn", "bars", "dots", "chips", "circles", "list"},
    "competency_style": {"icon_grid", "list"},
    "header_shape": {"flat", "wave", "curve", "diagonal"},
    "footer_shape": {"none", "wave", "curve", "bar"},
    "photo_position": {"left", "right", "center"},
    "name_align": {"left", "center"},
    "language_style": {"bars", "dots", "squares", "text"},
    "decor": {"none", "circles", "dots"},
    "header_accent": {"none", "left_bar"},
}


def _merge_design(base: dict, over: dict) -> dict:
    d = json.loads(json.dumps(base))
    for k, ok in _DESIGN_CHOICES.items():
        v = str(over.get(k) or "").strip().lower()
        if v in ok:
            d[k] = v
    if isinstance(over.get("timeline"), bool):
        d["timeline"] = over["timeline"]
    for k in ("photo_ring", "column_divider", "item_rules"):
        if isinstance(over.get(k), bool):
            d[k] = over[k]
    if str(over.get("skills_columns")) in ("1", "2"):
        d["skills_columns"] = int(over["skills_columns"])
    band = over.get("band_inset")
    if isinstance(band, list) and len(band) in (0, 3):
        try:
            d["band_inset"] = [max(0.0, min(14.0, float(v))) for v in band]
        except (TypeError, ValueError):
            pass
    inset = over.get("page_inset")
    if isinstance(inset, list) and len(inset) == 4:
        try:
            d["page_inset"] = [max(0.0, min(14.0, float(v))) for v in inset]
        except (TypeError, ValueError):
            pass
    try:
        sw = int(float(over.get("sidebar_width") or 0))
        if 22 <= sw <= 56:
            d["sidebar_width"] = sw
    except Exception:
        pass
    cols = over.get("colors") or {}
    if isinstance(cols, dict):
        for k in ("primary", "accent", "heading", "text", "sidebar_bg", "page_bg", "header_text", "track", "band", "header_bg"):
            if cols.get(k):
                d["colors"][k] = _hex(cols[k], d["colors"].get(k) or "#888888")
        sc = [_hex(c, "") for c in (cols.get("skill_colors") or []) if _hex(c, "")]
        if sc:
            d["colors"]["skill_colors"] = (sc + d["colors"]["skill_colors"])[:3]
    for key in ("sidebar_sections", "main_sections", "bottom_sections"):
        lst = [s for s in (over.get(key) or []) if s in SECTION_KEYS]
        if lst or (key == "sidebar_sections" and over.get("layout") == "single_column") or                 (key == "bottom_sections" and "bottom_sections" in over):
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
    fvars = (design.get("free") or {}).get("vars")
    if isinstance(fvars, dict):                    # a new main colour beats the editor's palette overrides
        for v in ("--primary", "--on-primary", "--accent", "--heading", "--side", "--tint", "--track"):
            fvars.pop(v, None)
    return design


def _sanitize_design(design: dict) -> dict:
    """Make sure colours stay readable and every section has a home."""
    for k, v in _STYLE_DEFAULTS.items():
        design.setdefault(k, json.loads(json.dumps(v)))
    c = design["colors"]
    c["header_text"] = _readable_on(c["primary"], c.get("header_text"))
    if _contrast(c["text"], c["page_bg"]) < 4:
        c["text"] = _readable_on(c["page_bg"])
    # headings are large & bold, so a lighter brand colour (≈2:1, e.g. sky blue on white) still reads fine
    if _contrast(c["heading"], c["page_bg"]) < 2.0:
        c["heading"] = c["accent"] if _contrast(c["accent"], c["page_bg"]) >= 2.0 else _readable_on(c["page_bg"])
    if _contrast(c["accent"], c["page_bg"]) < 2.0:      # accent is used for company names / bullets
        c["accent"] = c["heading"]
    if _contrast(c["primary"], c["page_bg"]) < 1.6 and c.get("header_bg"):
        c["primary"] = c["heading"]
        c["accent"] = c["accent"] if _contrast(c["accent"], c["page_bg"]) >= 2.0 else c["heading"]
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
        if design["header"] in ("sidebar_name", "sidebar_photo"):
            design["header"] = "left_plain"
    elif not design.get("sidebar_sections"):
        design["sidebar_sections"] = ["contact", "skills", "education", "languages"]
    if design["layout"] == "two_column":                  # two equal white columns: no sidebar colour
        c["sidebar_bg"] = c["page_bg"]
        design["sidebar_width"] = max(44, min(56, int(design.get("sidebar_width") or 50)))
        if design["header"] in ("sidebar_name", "sidebar_photo"):
            design["header"] = "full_band"
    bottom = list(dict.fromkeys(design.get("bottom_sections") or []))
    design["bottom_sections"] = bottom
    design["sidebar_sections"] = [s for s in design.get("sidebar_sections", []) if s not in bottom]
    design["main_sections"] = [s for s in design["main_sections"] if s not in design.get("sidebar_sections", []) and s not in bottom]
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
- PROJECTS ARE NOT JOBS. Put projects in "projects" with their REAL names (e.g. "SmartFlex – AI-Powered Smart Classroom System"),
  the tech line in "tech" and their points in "bullets" — even if the user lists them under an "Experience" heading.
  "experience" is only for real jobs/internships the user states, with the role and organisation exactly as written.
  Never fill a role with a generic title like "Full Stack Software Developer" that the user didn't write for that entry.
- Say each fact ONCE. Don't repeat a project, award or bullet in highlights/achievements/competencies/profile bullets.
- Only produce sections the user gave or the design lists. Never create highlights, competencies, interests or references
  from nothing. Skip placeholder text without real values (e.g. "Links: LinkedIn / Portfolio / GitHub" with no URLs).
- If the user wrote section headings or said which column a section goes in (e.g. "LEFT COLUMN: Contact, Skills"), copy
  them into "section_titles" / "layout_hint" (keys from the shape below).
- Keep all of the user's real content; wording should be tight (bullets <= 22 words). Omit a field when there is nothing true for it.
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
 "projects": [{"name": "<real project name>", "tech": "<tech stack line, if given>", "period": "", "bullets": [""], "description": ""}],
 "references": [""],
 "section_titles": {"<section key>": "<heading the user explicitly wrote, e.g. 'Experience (Projects)'>"},
 "layout_hint": {"sidebar": ["<section keys the user put in the side column>"], "main": ["<section keys for the main column>"]}
}
Section keys: profile, highlights, contact, skills, competencies, experience, education, achievements, certifications,
languages, interests, projects, references.
Icon keys: target, users, user, pie, bars, trending, refresh, handshake, compass, presentation, lightbulb, gear, book, megaphone, shield, star, clipboard, code, globe, money, briefcase, award, chat, clock, heart, cap."""


def _content_brief(design: dict) -> str:
    secs = design.get("sidebar_sections", []) + design.get("main_sections", [])
    lines = [f"Design sections (in order): {', '.join(secs)}."]
    if design.get("skills_style") == "venn":
        lines.append("The skills graphic is a 3-circle Venn: the FIRST 3 skills must be single words of <= 11 letters (e.g. SALES, LEADERSHIP); put the rest in additional_skills.")
    else:
        lines.append("List 5-8 skills with honest relative levels; extra ones go to additional_skills.")
    if "competencies" in secs:
        lines.append("The design has a competencies block: write 4-6 competencies from the user's real work (only if it doesn't just repeat other sections).")
    if "highlights" in secs:
        lines.append("The design has career highlights: 3-4, but only facts not already shown elsewhere.")
    if "experience" in secs and "projects" not in secs:
        lines.append("The design has an Experience slot but no Projects slot: still put projects in 'projects' (they are shown in that slot).")
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
            projs.append({"name": str(x["name"]).strip(), "tech": str(x.get("tech") or "").strip(),
                          "period": str(x.get("period") or "").strip(), "bullets": _str_list(x.get("bullets"), 8),
                          "description": str(x.get("description") or "").strip()})
    out["projects"] = projs[:8]
    out["references"] = _str_list(c.get("references"), 4)
    titles = c.get("section_titles") if isinstance(c.get("section_titles"), dict) else {}
    out["section_titles"] = {k: str(v).strip()[:40] for k, v in titles.items() if k in SECTION_KEYS and str(v or "").strip()}
    hint = c.get("layout_hint") if isinstance(c.get("layout_hint"), dict) else {}
    out["layout_hint"] = {side: [k for k in (hint.get(side) or []) if k in SECTION_KEYS] for side in ("sidebar", "main")}
    out["section_order"] = [k for k in (c.get("section_order") or []) if k in SECTION_KEYS]
    out["custom_sections"] = _custom_sections(c.get("custom_sections"))
    return out


_CUSTOM_STYLES = ("bullets", "text", "chips", "plain")


def _custom_sections(v) -> list[dict]:
    """User-made sections from the editor: {id: custom_N, title, style, items}. Kept even with no items."""
    out, used = [], set()
    for x in (v if isinstance(v, list) else [])[:12]:
        if not isinstance(x, dict):
            continue
        cid = str(x.get("id") or "")
        cid = cid if re.fullmatch(r"custom_\d{1,4}", cid) and cid not in used else ""
        out.append({"id": cid, "title": str(x.get("title") or "").strip()[:60] or "New Section",
                    "style": x.get("style") if x.get("style") in _CUSTOM_STYLES else "bullets",
                    "items": [str(i).strip() for i in (x.get("items") or []) if str(i or "").strip()][:30]
                    if isinstance(x.get("items"), list) else _str_list(x.get("items"), 30)})
        used.add(cid)
    n = 1
    for x in out:
        if not x["id"]:
            while f"custom_{n}" in used:
                n += 1
            x["id"] = f"custom_{n}"
            used.add(x["id"])
    return out


def _nums(text: str) -> set[str]:
    out = set()
    for n, k in re.findall(r"(\d[\d,]*(?:\.\d+)?)\s*([kKmM](?![a-zA-Z]))?", text or ""):
        n = n.replace(",", "")
        out.add(n)
        if k:            # "30K" is the same fact as "30,000"
            try:
                out.add(str(int(float(n) * (1000 if k.lower() == "k" else 1_000_000))))
            except ValueError:
                pass
    return out


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
        proj["bullets"] = [b for b in proj.get("bullets", []) if ok(b)]
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


_WORD_RX = re.compile(r"[a-z0-9+#]+")
_STOP = {"and", "the", "a", "an", "of", "to", "in", "for", "with", "on", "at", "by", "using", "via", "from", "as", "into"}


def _words(text: str) -> set[str]:
    return {w for w in _WORD_RX.findall((text or "").lower()) if w not in _STOP and len(w) > 1}


def _similar(a: str, b: str) -> float:
    wa, wb = _words(a), _words(b)
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / min(len(wa), len(wb))


# headings that show the user really gave a section (derived sections without these get dropped)
_EXPLICIT_RX = {
    "highlights": r"highlight|key\s+facts|at\s+a\s+glance", "competencies": r"competenc|expertise|strength|core\s+areas",
    "interests": r"interest|hobb|passion", "references": r"reference|referee", "achievements": r"achievement|award|honou?r|accomplish|rank|percentile|runner|winner|prize",
    "certifications": r"certif|course|licen|training", "languages": r"language|english|hindi|french|spanish|german|arabic",
}


def _finalize_content(content: dict, details: str, design: dict) -> dict:
    """Deterministic clean-up after the LLM: invented job entries, repeated facts, sections nobody asked for."""
    src = (details or "").lower()
    src_norm = re.sub(r"\s+", " ", src)
    # experience entries without an organisation whose role the user never wrote are projects in disguise
    kept = []
    for job in content["experience"]:
        role = re.sub(r"\s+", " ", job["role"].lower()).strip()
        if job["company"] or not role or role in src_norm:
            kept.append(job)
            continue
        text = " ".join(job["bullets"])
        if any(_similar(text, " ".join(pr.get("bullets", [])) + " " + pr.get("description", "")) > 0.5 for pr in content["projects"]):
            continue                                   # already captured as a project
        content["projects"].append({"name": job["role"], "tech": "", "period": job["period"], "bullets": job["bullets"], "description": ""})
    content["experience"] = kept
    # drop sections that neither the design nor the user's text has
    design_secs = set(design.get("sidebar_sections", [])) | set(design.get("main_sections", [])) | set(design.get("bottom_sections") or [])
    for key, rx in _EXPLICIT_RX.items():
        if content.get(key) and key not in design_secs and not re.search(rx, src):
            content[key] = []
    if not re.search(_EXPLICIT_RX["competencies"], src) and content["competencies"] and "competencies" not in design_secs:
        content["competencies"] = []
    # each fact once: weaker sections lose items already said by stronger ones
    strong = [b for j in content["experience"] for b in j["bullets"]] + \
             [x for pr in content["projects"] for x in pr.get("bullets", []) + [pr.get("description", ""), pr["name"]]] + \
             [e["degree"] + " " + e["details"] for e in content["education"]]
    for key in ("achievements", "certifications"):
        content[key] = [x for x in content[key] if not any(_similar(x, y) > 0.7 for y in strong)]
        strong += content[key]
    content["highlights"] = [x for x in content["highlights"] if not any(_similar(x, y) > 0.55 for y in strong)]
    strong += content["highlights"]
    content["competencies"] = [x for x in content["competencies"]
                               if not any(_similar(x["title"] + " " + x["description"], y) > 0.75 for y in strong)]
    for key in ("highlights", "achievements", "certifications", "additional_skills", "interests"):   # in-list repeats
        uniq = []
        for x in content[key]:
            if not any(_similar(x, u) > 0.8 for u in uniq):
                uniq.append(x)
        content[key] = uniq
    names = {s["name"].lower() for s in content["skills"]}
    content["additional_skills"] = [x for x in content["additional_skills"] if x.lower() not in names]
    # a heading the user wrote that covers two list sections ("Certifications & Achievements") → one list
    titles = content.get("section_titles") or {}
    for key in ("certifications", "achievements", "highlights", "interests"):
        title = titles.get(key, "")
        for other in ("certifications", "achievements", "highlights", "interests"):
            if other != key and content.get(other) and other not in titles and re.search(_EXPLICIT_RX[other], title, re.I):
                content[key] = content[key] + content[other]
                content[other] = []
    return content


# UPPERCASE headings the user typed ("EXPERIENCE (PROJECTS)", "CERTIFICATIONS & ACHIEVEMENTS") → exact titles + order.
# Pasted text often loses newlines ("CONTACTEmail:"), so only the known heading word (+ "(…)" / "& WORD") is taken.
_HEADING_WORDS = {
    "profile": r"PROFESSIONAL SUMMARY|SUMMARY|PROFILE|ABOUT ME|OBJECTIVE|OVERVIEW", "highlights": r"CAREER HIGHLIGHTS|HIGHLIGHTS",
    "contact": r"CONTACT(?: DETAILS| INFO)?", "competencies": r"CORE COMPETENCIES|COMPETENCIES|EXPERTISE",
    "skills": r"TECHNICAL SKILLS|SKILLS", "experience": r"WORK EXPERIENCE|PROFESSIONAL EXPERIENCE|EXPERIENCE|EMPLOYMENT",
    "education": r"EDUCATION", "achievements": r"ACHIEVEMENTS|AWARDS|HONOU?RS", "certifications": r"CERTIFICATIONS?|COURSES",
    "languages": r"LANGUAGES", "interests": r"INTERESTS|HOBBIES", "projects": r"PROJECTS", "references": r"REFERENCES",
}
_HEADING_RX = re.compile(r"(?<![A-Z])(" + "|".join(f"(?P<{k}>{v})" for k, v in _HEADING_WORDS.items()) +
                         r")(\s*\([A-Z][A-Z &/]{1,30}\)|\s*(?:&|AND)\s*(?:" + "|".join(_HEADING_WORDS.values()) + r"))?")


def _user_headings(details: str) -> tuple[dict, list]:
    titles, order, spans = {}, [], []
    for m in _HEADING_RX.finditer(details or ""):
        if any(a <= m.start() < b for a, b in spans):
            continue                                # "PROJECTS" inside "EXPERIENCE (PROJECTS)"
        key = next(k for k in _HEADING_WORDS if m.group(k))
        if key in titles:
            continue
        spans.append((m.start(), m.end()))
        titles[key] = re.sub(r"\s+", " ", m.group(0)).strip()
        order.append(key)
    return titles, order


def _restore_dropped(content: dict, details: str) -> dict:
    """Fallback models sometimes silently drop a project's/job's points. Re-add any full sentence from that
    entry's own block of the user's text that no bullet covers (verbatim — nothing invented)."""
    src = details or ""
    low = src.lower()
    entries = [(pr, pr["name"]) for pr in content["projects"]] + [(j, j["company"] or j["role"]) for j in content["experience"]]
    def where(n: str) -> int:              # exact case first: a lowercase mention in the summary isn't the entry
        i = src.find(n)
        return i if i >= 0 else low.find(n.lower())
    starts = sorted({where(n) for _, n in entries if n and where(n) >= 0} | {m.start() for m in _HEADING_RX.finditer(src)})
    for entry, name in entries:
        if not name or not entry.get("bullets"):
            continue
        a = where(name)
        if a < 0:
            continue
        b = next((x for x in starts if x > a), len(src))
        block = src[a + len(name):b]
        for sent in re.split(r"(?<=[.!?])\s+|\s{3,}|\n+", block):
            sent = sent.strip(" -•\t")
            if len(sent.split()) < 8 or not sent[:1].isupper() or not sent.endswith((".", "!")) or len(entry["bullets"]) >= 6:
                continue
            if not any(_similar(sent, x) > 0.5 for x in entry["bullets"]):
                entry["bullets"].append(sent)
    return content


def _apply_layout_hint(design: dict, content: dict) -> dict:
    """The user said which column a section goes in → that wins over the reference picture."""
    hint = content.get("layout_hint") or {}
    side, main = hint.get("sidebar") or [], hint.get("main") or []
    if design["layout"] in ("single_column",) or not (side or main):
        return design
    d = json.loads(json.dumps(design))
    for k in side:
        for lst in ("main_sections", "bottom_sections"):
            if k in (d.get(lst) or []):
                d[lst].remove(k)
    for k in main:
        for lst in ("sidebar_sections", "bottom_sections"):
            if k in (d.get(lst) or []):
                d[lst].remove(k)
    d["sidebar_sections"] = list(dict.fromkeys(side + [k for k in d["sidebar_sections"] if k not in side]))
    d["main_sections"] = list(dict.fromkeys(main + [k for k in d["main_sections"] if k not in main]))
    return d


def _build_content(details: str, design: dict) -> dict:
    user = f"{_content_brief(design)}\n\nUSER DETAILS:\n{details.strip()[:12000]}"
    content = _drop_invented(_normalise_content(_llm_json(_CONTENT_SYSTEM, user)), details)
    titles, order = _user_headings(details)
    if len(order) >= 2:                              # the user's own headings & order are authoritative
        content["section_titles"], content["section_order"] = titles, order
    content = _finalize_content(content, details, design)
    content = _restore_dropped(content, details)
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
    if "custom_sections" not in data and old.get("custom_sections"):     # model dropped the editor's own sections
        merged["custom_sections"] = old["custom_sections"]
    return merged if (merged.get("name") or merged.get("experience")) else old


# ── HTML rendering ──────────────────────────────────────────────────────────────────────────────
def _title(design: dict, key: str) -> str:
    return (design.get("section_titles") or {}).get(key) or DEFAULT_TITLES[key]


def _sec(design: dict, key: str, inner: str, cls: str = "") -> str:
    return f'<section class="sec sec-{key} {cls}"><h2>{_f("section_titles." + key, _title(design, key), "section title")}</h2>{inner}</section>'


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


# ── Editor mode: every text value can be tagged with its JSON path (contenteditable in /resume/editor) ──
# False = plain PDF render, True = editor, "mark" = PDF render of a design with per-element editor styles
# (keeps the data-f / data-item anchors those styles are keyed on, but no editor-only placeholders).
_EDIT = contextvars.ContextVar("resume_edit_mode", default=False)


def _f(path: str, value, ph: str = "") -> str:
    """Escaped text; in editor mode an editable span carrying the content JSON path it maps back to."""
    mode = _EDIT.get()
    if not mode:
        return _e(value)
    if mode == "mark":      # free-design PDF render: same DOM anchors as the editor, nothing editable
        return f'<span data-f="{path}">{_e(value)}</span>'
    return (f'<span data-f="{path}" data-ph="{_e(ph or path.split(".")[-1])}" contenteditable="true" '
            f'spellcheck="true">{_e(value)}</span>')


def _it(path: str) -> str:
    """Attribute marking a list item (editor shows + / up / x controls on hover)."""
    return f' data-item="{path}"' if _EDIT.get() else ""


def _skill_name(c: dict, i: int) -> str:
    return _f(f"skills.{i}.name", c["skills"][i]["name"], "skill")


def _skills_html(c: dict, d: dict, side: bool) -> str:
    skills, extra = c["skills"], c["additional_skills"]
    if not skills and not extra:
        return ""
    edit = _EDIT.get() is True
    style = d["skills_style"]
    cols = d["colors"]
    fg = "var(--side-accent)" if side else "var(--primary)"
    track = "var(--side-track)" if side else "var(--track)"
    parts = []
    extra_items = [(f"additional_skills.{j}", x, "skill", f"additional_skills.{j}") for j, x in enumerate(extra)]
    if style == "venn" and skills:
        parts.append(_venn(skills, cols["skill_colors"]))
        if edit:   # SVG labels can't be typed into: editable copies of the circle skills, editor-only
            parts.append('<div class="edit-only ed-venn"><small>Circle skills:</small> ' + "".join(
                f'<span class="ed-chip"{_it(f"skills.{i}")}>{_skill_name(c, i)}</span>' for i in range(min(3, len(skills)))) + "</div>")
        rest = [(f"skills.{i}.name", skills[i]["name"], "skill", f"skills.{i}") for i in range(3, len(skills))] + extra_items
        if rest:
            sep = " <span class=dot>•</span> "
            listing = sep.join(f'<span{_it(item)}>{_f(p, x, ph)}</span>' if edit else _f(p, x, ph) for p, x, ph, item in rest)
            parts.append(f'<div class="addl"><div class="addl-h">Additional Skills:</div><div class="addl-list">{listing}</div></div>')
        return "".join(parts)
    if style == "bars":
        parts.append('<div class="bars">' + "".join(
            f'<div class="bar-row"{_it(f"skills.{i}")}><div class="bar-l">{_skill_name(c, i)}</div><div class="bar-t" style="background:{track}">'
            f'<div class="bar-f" style="width:{s["level"]}%;background:{fg}"></div></div></div>' for i, s in enumerate(skills)) + "</div>")
    elif style == "dots":
        parts.append('<div class="dots">' + "".join(
            f'<div class="dot-row"{_it(f"skills.{i}")}><span>{_skill_name(c, i)}</span><span class="dot-set">' +
            "".join(f'<i style="background:{fg if k < round(s["level"] / 20) else track}"></i>' for k in range(5)) +
            "</span></div>" for i, s in enumerate(skills)) + "</div>")
    elif style == "circles":
        ring_col = cols["accent"]
        parts.append('<div class="rings">' + "".join(
            f'<div class="ring-cell"{_it(f"skills.{i}")}>{_ring(s["level"], ring_col, _mix(ring_col, "#ffffff", 0.75))}<div>{_skill_name(c, i)}</div></div>'
            for i, s in enumerate(skills[:9])) + "</div>")
    elif style == "list":
        parts.append('<ul class="plain">' + "".join(f'<li{_it(f"skills.{i}")}>{_skill_name(c, i)}</li>' for i in range(len(skills))) + "</ul>")
    else:  # chips (also used for leftovers)
        extra_items = [(f"skills.{i}.name", s["name"], "skill", f"skills.{i}") for i, s in enumerate(skills)] + extra_items
    if extra_items:
        if parts:                                    # don't let tags silently continue a bar list
            parts.append('<div class="sub-h">Other technologies</div>')
        parts.append('<div class="chips">' + "".join(
            f'<span{_it(item)}>{_f(p, x, ph)}</span>' for p, x, ph, item in extra_items) + "</div>")
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
    edit = _EDIT.get() is True
    if d["competency_style"] == "list" or side:
        out = []
        for i, x in enumerate(items):
            desc = (" — " + _f(f"competencies.{i}.description", x["description"], "description")) if (x["description"] or edit) else ""
            out.append(f'<li{_it(f"competencies.{i}")}><b>{_f(f"competencies.{i}.title", x["title"], "title")}</b>{desc}</li>')
        return '<ul class="comp-list">' + "".join(out) + "</ul>"
    return '<div class="comp-grid">' + "".join(
        f'<div class="comp"{_it(f"competencies.{i}")}><div class="comp-ic">{_icon(x["icon"] or _guess_icon(x["title"]), "var(--heading)")}</div>'
        f'<div><div class="comp-t">{_f(f"competencies.{i}.title", x["title"], "title")}</div>'
        f'<div class="comp-d">{_f(f"competencies.{i}.description", x["description"], "description")}</div></div></div>'
        for i, x in enumerate(items)) + "</div>"


def _experience_html(c: dict, d: dict, side: bool) -> str:
    if not c["experience"]:
        return ""
    edit = _EDIT.get() is True
    rows = []
    for i, x in enumerate(c["experience"]):
        p = f"experience.{i}"
        if edit:
            sub = _f(p + ".company", x["company"], "company") + " · " + _f(p + ".location", x["location"], "location")
            role = _f(p + ".role", x["role"], "role")
        else:
            sub = " · ".join(_e(v) for v in (x["company"], x["location"]) if v)
            role = _e(x["role"] or x["company"])
        bullets = "".join(f'<li{_it(f"{p}.bullets.{j}")}>{_f(f"{p}.bullets.{j}", b, "achievement")}</li>'
                          for j, b in enumerate(x["bullets"]))
        co = f"<div class=job-co>{sub}</div>" if sub and (x["role"] or edit) else ""
        ul = f"<ul>{bullets}</ul>" if bullets else ""
        rows.append(f'<div class="job"{_it(p)}><div class="job-top"><div class="job-role">{role}</div>'
                    f'<div class="job-period">{_f(p + ".period", x["period"], "period")}</div></div>{co}{ul}</div>')
    return f'<div class="{"timeline" if d.get("timeline") else "jobs"}">{"".join(rows)}</div>'


def _projects_html(c: dict, d: dict, side: bool) -> str:
    edit = _EDIT.get() is True
    rows, rich = [], any(x["bullets"] or x["tech"] for x in c["projects"])
    for i, x in enumerate(c["projects"]):
        p = f"projects.{i}"
        if not rich:
            desc = f'<div>{_f(p + ".description", x["description"], "description")}</div>' if (x["description"] or edit) else ""
            rows.append(f'<div class="proj"{_it(p)}><b>{_f(p + ".name", x["name"], "project")}</b>{desc}</div>')
            continue
        tech = f'<div class="job-co">{_f(p + ".tech", x["tech"], "tech stack")}</div>' if (x["tech"] or edit) else ""
        desc = f'<div class="proj-d">{_f(p + ".description", x["description"], "description")}</div>' if x["description"] else ""
        bullets = "".join(f'<li{_it(f"{p}.bullets.{j}")}>{_f(f"{p}.bullets.{j}", b, "point")}</li>' for j, b in enumerate(x["bullets"]))
        rows.append(f'<div class="job"{_it(p)}><div class="job-top"><div class="job-role">{_f(p + ".name", x["name"], "project")}</div>'
                    f'<div class="job-period">{_f(p + ".period", x["period"], "period")}</div></div>{tech}{desc}'
                    f'{f"<ul>{bullets}</ul>" if bullets else ""}</div>')
    if not rows:
        return ""
    return f'<div class="{"timeline" if (rich and d.get("timeline")) else "jobs"}">{"".join(rows)}</div>'


def _effective_design(c: dict, d: dict) -> dict:
    """Per-content tweaks: projects take an empty Experience slot; headings the user wrote win."""
    d = json.loads(json.dumps(d))
    lists = [d.setdefault("sidebar_sections", []), d.setdefault("main_sections", []), d.get("bottom_sections") or []]
    swapped = False
    # (only when the Experience slot comes first — not when it's just an empty placeholder appended after Projects)
    already_first = any("projects" in lst and "experience" in lst and lst.index("projects") < lst.index("experience") for lst in lists)
    if c.get("projects") and not c.get("experience") and any("experience" in lst for lst in lists) and not already_first:
        for lst in lists:                            # no real jobs: projects take the Experience slot
            if "projects" in lst:
                lst.remove("projects")
        for lst in lists:
            if "experience" in lst:
                lst[lst.index("experience")] = "projects"
                swapped = True
                break
    user_titles = dict(c.get("section_titles") or {})
    if swapped and "projects" not in user_titles and user_titles.get("experience"):
        user_titles["projects"] = user_titles.pop("experience")
    order = list(c.get("section_order") or [])
    if swapped and "experience" in order and "projects" not in order:
        order[order.index("experience")] = "projects"
    hint = c.get("layout_hint") or {}
    if order and (hint.get("sidebar") or hint.get("main")):   # user spelled out a layout → their order; else the design's
        for name in ("sidebar_sections", "main_sections"):
            lst = d[name]
            d[name] = sorted(lst, key=lambda k: (order.index(k), 0) if k in order else (len(order), lst.index(k)))
    if user_titles:
        d["section_titles"] = {**(d.get("section_titles") or {}), **user_titles}
    for cs in c.get("custom_sections") or []:          # editor-made sections without a slot go to the main column
        if not any(cs["id"] in lst for lst in lists):
            d["main_sections"].append(cs["id"])
    if c.get("layout_hint"):
        d["pinned"] = list(dict.fromkeys((d.get("pinned") or []) + (c["layout_hint"].get("sidebar") or []) + (c["layout_hint"].get("main") or [])))
        if swapped and "experience" in d["pinned"]:
            d["pinned"].append("projects")
    return d


def _education_html(c: dict, d: dict, side: bool) -> str:
    edit = _EDIT.get() is True
    out = []
    for i, x in enumerate(c["education"]):
        p = f"education.{i}"
        parts = [f'<div class="edu-deg">{_f(p + ".degree", x["degree"], "degree")}</div>']
        if x["institution"] or edit:
            parts.append(f'<div class="edu-inst">{_f(p + ".institution", x["institution"], "institution")}</div>')
        meta = [m for m in ((x["period"] or edit) and _f(p + ".period", x["period"], "period"),
                            (x["details"] or edit) and _f(p + ".details", x["details"], "details (grade, honours)")) if m]
        if meta:                                     # "2024 – 2028 · CGPA: 8.139" on one spaced line
            parts.append(f'<div class="edu-meta">{"<span class=sep>·</span>".join(meta)}</div>')
        out.append(f'<div class="edu"{_it(p)}>{"".join(parts)}</div>')
    return "".join(out)


def _contact_html(c: dict, d: dict, side: bool) -> str:
    ct = c["contact"]
    edit = _EDIT.get() is True
    col = "var(--side-heading)" if side else "var(--heading)"
    rows = [(k, ic) for k, ic in (("phone", "phone"), ("email", "mail"), ("location", "pin"),
                                  ("linkedin", "linkedin"), ("website", "link")) if ct.get(k) or edit]
    if not rows:
        return ""
    return '<div class="ct-wrap">' + "".join(f'<div class="ct"><span class="ct-ic">{_icon(ic, col, fill=col if ic == "phone" else "none")}</span>'
                                             f'<span class="ct-v">{_f("contact." + k, ct[k], k)}</span></div>' for k, ic in rows) + "</div>"


def _list_html(key: str, items: list[str], icon: str | None, side: bool) -> str:
    if not items:
        return ""
    if icon:
        col = "var(--side-heading)" if side else "var(--heading)"
        return '<ul class="ic-list">' + "".join(
            f'<li{_it(f"{key}.{i}")}><span class="li-ic">{_icon(icon, col, fill=col if icon == "trophy" else "none")}</span>{_f(f"{key}.{i}", x)}</li>'
            for i, x in enumerate(items)) + "</ul>"
    return '<ul class="bul">' + "".join(f'<li{_it(f"{key}.{i}")}>{_f(f"{key}.{i}", x)}</li>' for i, x in enumerate(items)) + "</ul>"


def _custom_section_html(key: str, c: dict) -> str:
    edit = _EDIT.get() is True
    idx = next((i for i, x in enumerate(c.get("custom_sections") or []) if x.get("id") == key), None)
    if idx is None:
        return ""
    cs, p = c["custom_sections"][idx], f"custom_sections.{idx}"
    items = cs["items"] or ([""] if edit else [])      # editor: one empty line to type into
    if not items:
        return ""
    paths = [(f"{p}.items.{i}", x) for i, x in enumerate(items)]
    if cs["style"] == "text":
        inner = "".join(f'<p{_it(q)}>{_f(q, x, "text")}</p>' for q, x in paths)
    elif cs["style"] == "chips":
        inner = '<div class="chips">' + "".join(f'<span{_it(q)}>{_f(q, x, "item")}</span>' for q, x in paths) + "</div>"
    else:
        plain = ' style="list-style:none;padding-left:0"' if cs["style"] == "plain" else ""
        inner = f'<ul class="bul"{plain}>' + "".join(f'<li{_it(q)}>{_f(q, x, "item")}</li>' for q, x in paths) + "</ul>"
    return f'<section class="sec sec-{key} sec-custom"><h2>{_f(p + ".title", cs["title"], "section title")}</h2>{inner}</section>'


def _section_html(key: str, c: dict, d: dict, side: bool) -> str:
    edit = _EDIT.get() is True
    if key in (d.get("hidden_sections") or []):
        return ""
    if key.startswith("custom_"):
        return _custom_section_html(key, c)
    if key not in SECTION_KEYS:
        return ""
    if key == "profile":
        inner = "".join(f'<p{_it(f"profile.{i}")}>{_f(f"profile.{i}", p, "profile paragraph")}</p>' for i, p in enumerate(c["profile"]))
    elif key == "highlights":
        inner = _list_html("highlights", c["highlights"], None, side)
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
        inner = _list_html("achievements", c["achievements"], "trophy", side)
    elif key == "certifications":
        inner = _list_html("certifications", c["certifications"], "award", side)
    elif key == "languages":
        inner = _languages_html(c, d, side)
    elif key == "interests":
        inner = ('<div class="chips">' + "".join(f'<span{_it(f"interests.{i}")}>{_f(f"interests.{i}", x, "interest")}</span>'
                                                 for i, x in enumerate(c["interests"])) + "</div>") if c["interests"] else ""
    elif key == "projects":
        inner = _projects_html(c, d, side)
    elif key == "references":
        inner = _list_html("references", c["references"], None, side)
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
    edit = _EDIT.get() is True
    up = " up" if d["name_case"] == "upper" else ""          # CSS uppercase: the stored text keeps its real case
    name = c["name"] or ("" if edit else "Your Name")
    title = c["title"]
    title_html = _f("title", title, "headline / job title")
    if not edit and len(title) > 30 and " & " in title:      # "CHIEF BRANCH MANAGER &<br>MARKETING PROFESSIONAL"
        title_html = title_html.replace(" &amp; ", " &amp;<br>", 1)
    title_div = f'<div class="ttl{up}">{title_html}</div>' if (title or edit) else ""
    return f'<div class="nm{up}" style="font-size:{size_pt:.1f}pt">{_f("name", name, "Your Name")}</div>{title_div}'


def _name_size(name: str, avail_mm: float, max_pt: float) -> float:
    # bold caps ≈ 0.68em per glyph; 1pt = 0.3528mm
    return max(16.0, min(max_pt, avail_mm / (0.68 * 0.3528 * max(len(name), 6))))


# ── Shapes & decorations (wave / curve / diagonal header band, footer, corner decor) ─────────────
# Paths live in a 1000×300 box stretched over the element (preserveAspectRatio="none").
_SHAPES = {
    "wave": ("M0,0 H1000 V182 C860,262 700,92 500,152 C330,206 175,256 0,200 Z",
             "M0,0 H1000 V212 C850,296 690,128 500,184 C320,238 170,284 0,230 Z"),
    "curve": ("M0,0 H1000 V185 Q500,300 0,185 Z", "M0,0 H1000 V212 Q500,322 0,212 Z"),
    "diagonal": ("M0,0 H1000 V115 L0,228 Z", "M0,0 H1000 V146 L0,258 Z"),
}
_FOOT_H = {"wave": 26, "curve": 20, "bar": 7}


def _shape_svg(shape: str, cls: str, flip: bool = False) -> str:
    main, back = _SHAPES.get(shape, _SHAPES["wave"])
    tf = ' transform="translate(0,300) scale(1,-1)"' if flip else ""
    return (f'<svg class="{cls}" viewBox="0 0 1000 300" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">'
            f'<g{tf}><path d="{back}" fill="var(--primary)" fill-opacity="0.32"/><path d="{main}" fill="var(--primary)"/></g></svg>')


def _shaped_header_html(c: dict, d: dict, photo_uri: str) -> str:
    name = c["name"] or "Your Name"
    ph = _photo_html(photo_uri, name, d["photo"], "hd-avatar hd-avatar-lg")
    pos = d.get("photo_position", "right") if ph else "none"
    avail = 210 - 26 - (48 if ph and pos != "center" else 0)
    return (f'<header class="hd-shape pos-{pos} al-{d.get("name_align", "center")}">{_shape_svg(d["header_shape"], "hd-svg")}'
            f'<div class="hd-inner"><div class="hd-txt">{_name_block(c, d, _name_size(name, avail, 32))}</div>{ph}</div></header>')


def _svg_bg(svg: str) -> str:
    """CSS background for an SVG. Chromium repeats position:fixed elements on every printed page, but not
    when they contain an inline <svg>, so footer/decor shapes must be background images (hex colours, no CSS vars)."""
    from urllib.parse import quote
    return f"background:url(\"data:image/svg+xml;charset=utf-8,{quote(svg)}\") no-repeat;background-size:100% 100%"


def _footer_html(d: dict) -> str:
    shape = d.get("footer_shape", "none")
    if shape == "none":
        return ""
    if shape == "bar":
        return '<div class="rb-foot rb-foot-bar"></div>'
    col = d["colors"]["primary"]
    main, back = _SHAPES.get(shape, _SHAPES["wave"])
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 300" preserveAspectRatio="none">'
           f'<g transform="translate(0,300) scale(1,-1)"><path d="{back}" fill="{col}" fill-opacity="0.32"/>'
           f'<path d="{main}" fill="{col}"/></g></svg>')
    return f"<div class=\"rb-foot\" style='{_svg_bg(svg)}'></div>"


def _decor_html(d: dict) -> str:
    decor = d.get("decor", "none")
    p, a = d["colors"]["primary"], d["colors"]["accent"]
    if decor == "circles":
        body = (f'<circle cx="205" cy="120" r="34" fill="{p}" fill-opacity="0.07"/>'
                f'<circle cx="2" cy="230" r="46" fill="{p}" fill-opacity="0.06"/>'
                f'<circle cx="190" cy="270" r="14" fill="{a}" fill-opacity="0.08"/>')
    elif decor == "dots":
        body = "".join(f'<circle cx="{180 + (i % 6) * 4.2:.1f}" cy="{96 + (i // 6) * 4.2:.1f}" r="0.8" fill="{p}" fill-opacity="0.35"/>'
                       for i in range(36))
    else:
        return ""
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 210 297" preserveAspectRatio="none">{body}</svg>'
    return f"<div class=\"rb-decor\" style='{_svg_bg(svg)}'></div>"


def _languages_html(c: dict, d: dict, side: bool) -> str:
    style = d.get("language_style", "dots")
    langs = c["languages"]
    if not langs:
        return ""
    if style == "bars":
        fg = "var(--side-accent)" if side else "var(--primary)"
        return '<div class="bars lang-bars">' + "".join(
            f'<div class="lang-row"{_it(f"languages.{i}")}><span class="lang-n">{_f(f"languages.{i}.name", x["name"], "language")}</span>'
            f'<div class="bar-t lang-t"><div class="bar-f" style="width:{x["level"] * 20}%;background:{fg}"></div></div></div>'
            for i, x in enumerate(langs)) + "</div>"
    if style == "text":
        words = {5: "Native / Fluent", 4: "Professional", 3: "Intermediate", 2: "Basic", 1: "Beginner"}
        return "".join(f'<div class="lang-txt"{_it(f"languages.{i}")}><b>{_f(f"languages.{i}.name", x["name"], "language")}</b>'
                       f' — {words.get(x["level"], "")}</div>' for i, x in enumerate(langs))
    sq = " sq" if style == "squares" else ""
    return "".join(
        f'<div class="dot-row"{_it(f"languages.{i}")}><span>{_f(f"languages.{i}.name", x["name"], "language")}</span><span class="dot-set{sq}">' +
        "".join(f'<i class="{"on" if k < x["level"] else ""}"></i>' for k in range(5)) + "</span></div>"
        for i, x in enumerate(langs))


def _css_extra(d: dict, scale: float) -> str:
    """CSS for the newer design vocabulary (kept apart from _css so older designs render identically)."""
    c = d["colors"]
    foot = d.get("footer_shape", "none")
    foot_h = _FOOT_H.get(foot, 0)
    track = c.get("track") or ""
    hs = d["heading_style"]
    marker = ""
    if hs in ("square_icon", "dot"):
        radius = "50%" if hs == "dot" else "1px"
        marker = (f'.sec h2::before{{content:"";display:inline-block;width:.74em;height:.74em;background:var(--primary);'
                  f'border-radius:{radius};margin-right:2.6mm;vertical-align:-.06em}}'
                  f'aside .sec h2::before{{background:var(--side-accent)}}')
    ring = ("box-shadow:0 0 0 1.6mm var(--page),0 0 0 2.5mm var(--primary);" if d.get("photo_ring") else "")
    band = c.get("band") or _mix(c["page_bg"], "#000000", 0.05)
    out = [marker]
    out.append(f"""
.hd-shape{{position:relative;height:calc(70mm*(0.45 + 0.55*var(--s)))}}
.hd-svg{{position:absolute;inset:0;width:100%;height:100%;display:block}}
.hd-inner{{position:relative;display:flex;align-items:flex-start;justify-content:space-between;gap:6mm;padding:8mm 13mm 0}}
.hd-shape .hd-txt{{flex:1;color:var(--on-primary);padding-top:1mm}}
.hd-shape.al-center .hd-txt{{text-align:center}}
.hd-shape.pos-left .hd-inner{{flex-direction:row-reverse}}
.hd-shape.pos-center .hd-inner{{flex-direction:column;align-items:center}}
.hd-shape .ttl{{opacity:.95}}
.hd-avatar-lg{{width:calc(40mm*(0.6 + 0.4*var(--s)));height:calc(40mm*(0.6 + 0.4*var(--s)));border:0!important;{ring}margin-top:1mm}}
.hd-band.pos-right{{flex-direction:row-reverse;justify-content:space-between}}
.hd-avatar{{{ring}}}
.rb-foot{{position:fixed;left:0;right:0;bottom:0;height:{foot_h}mm;z-index:0}}
.rb-foot-bar{{background:var(--primary)}}
.rb-decor{{position:fixed;inset:0;z-index:0;pointer-events:none}}
.lay-two_column aside{{padding:7mm 6mm 10mm 13mm}} .lay-two_column main{{padding:7mm 13mm 10mm 6mm}}
.lay-sidebar_right .main-top{{margin:-7mm -8mm 5.5mm -12mm}}
.lay-two_column .side-bg{{display:none}}
.bottom{{position:relative;z-index:1;padding:2mm 13mm 6mm}}
.bottom .sec{{margin-bottom:3mm}}
.bottom .sec-contact{{display:flex;align-items:center;gap:10mm;flex-wrap:wrap}}
.bottom .sec-contact h2{{margin:0}}
.bottom .ct-wrap{{display:grid;grid-template-columns:auto auto;gap:2mm 12mm}}
.lang-row{{display:flex;align-items:center;gap:4mm;margin-bottom:2.4mm}}
.lang-n{{width:22mm;flex:none;color:var(--accent);font-weight:500}}
.lang-bars .lang-t{{flex:1;height:1.6mm;{f"background:{track}!important;" if track else ""}}}
.lang-txt{{margin-bottom:1.6mm}}
.dot-set.sq i{{border-radius:1px}}
.proj-d{{margin-bottom:1mm}}
.main-top{{margin:-7mm -12mm 5.5mm -8mm;padding:6.5mm 10mm 5.5mm;background:{band};text-align:center}}
.main-top .nm{{color:var(--heading)}}
.main-top .ttl{{color:var(--text);letter-spacing:2px;font-weight:500;margin-top:1.8mm;font-size:calc(10pt*var(--s))}}
.side-top.photo-only{{margin-bottom:5.5mm}}
.side-top.photo-only .hd-avatar{{width:29mm;height:29mm;border:1.6mm solid #ffffff;margin:0 auto}}
""".replace("{band}", band))
    if foot_h:   # keep text clear of the footer shape on every page
        # columns always keep footer clearance (cloned at every page break); a bottom strip is pulled up into it
        out.append(f"aside,main{{padding-bottom:calc({foot_h}mm + 8mm)!important}}"
                   f".bottom{{margin-top:calc(-{foot_h}mm - 4mm);padding-bottom:calc({foot_h}mm + 6mm)}}")
    if track:
        out.append(f".bars .bar-t{{background:{_mix(track, c['page_bg'], 0.82)}!important}}")
    if c.get("header_bg"):                       # measured band colour (light band → dark text)
        out.append(f".hd-band{{background:{c['header_bg']};color:{_readable_on(c['header_bg'], c['heading'])}}}"
                   f".hd-band .ttl{{color:{_readable_on(c['header_bg'], c['text'])};letter-spacing:2.5px}}")
    if d.get("header_accent") == "left_bar":
        out.append(".hd-band.acc-left_bar{position:relative;padding-left:24mm}"
                   ".hd-band.acc-left_bar::before{content:'';position:absolute;left:0;top:0;bottom:0;width:8mm;background:var(--heading)}")
    if d.get("column_divider"):
        side = "left" if d["layout"] != "sidebar_right" else "right"
        out.append(f"main{{border-{side}:1px solid {_mix(c['heading'], c['page_bg'], 0.25)}}}")
    if d.get("item_rules"):
        out.append(f".ct,.ic-list li,.edu{{border-bottom:1px solid {_mix(c['heading'], c['page_bg'], 0.55)};padding-bottom:1.6mm;margin-bottom:1.8mm}}")
    if d.get("skills_columns") == 2:
        out.append("main .bars{display:grid;grid-template-columns:1fr 1fr;column-gap:9mm}")
    t, r, b, l = (d.get("page_inset") or [0, 0, 0, 0]) + [0, 0, 0, 0][len(d.get("page_inset") or []):]
    band_in = d.get("band_inset") or []
    if len(band_in) == 3 and any(band_in):
        bt, br, bg = max(0.0, band_in[0] - t), max(0.0, band_in[1] - r), band_in[2]
        if d["layout"] == "sidebar_right":
            out.append(f".lay-sidebar_right .main-top{{margin:calc(-7mm + {bt}mm) {bg - 8}mm 5.5mm calc(-12mm + {br}mm)}}")
        else:
            out.append(f".main-top{{margin:calc(-7mm + {bt}mm) calc(-12mm + {br}mm) 5.5mm calc(-8mm + {bg}mm)}}")
    if any((t, r, b, l)):
        swf = (d.get("sidebar_width", 32) or 32) / 100
        out.append(
            f".side-bg{{top:{t}mm!important;bottom:{b}mm!important;left:{l}mm!important;"
            f"width:calc((210mm - {l + r}mm) * {swf:.4f})!important}}"
            f".lay-sidebar_right .side-bg{{left:auto!important;right:{r}mm!important}}"
            f"header{{margin:{t}mm {r}mm 0 {l}mm}}"
            f".cols,.bottom{{margin-left:{l}mm;margin-right:{r}mm}}"
            f"body:not(:has(header)) .cols{{margin-top:{t}mm}}"
            f".rb-foot{{left:{l}mm;right:{r}mm;bottom:{b}mm}}"
            # later pages: keep text inside the framed sidebar block
            f"aside,main{{padding-bottom:calc(10mm + {b}mm)}}")
    return "".join(out)


def _header_html(c: dict, d: dict, photo_uri: str) -> str:
    h, sw = d["header"], d.get("sidebar_width", 32) if d["layout"] != "single_column" else 0
    name = c["name"] or "Your Name"
    if h in ("sidebar_name", "sidebar_photo"):
        return ""
    if h == "full_band" and d.get("header_shape", "flat") != "flat":
        return _shaped_header_html(c, d, photo_uri)
    if h == "diagonal_banner":
        ph = _photo_html(photo_uri, name, "square" if d["photo"] != "none" else "none", "hd-photo")
        width_pct = sw if (ph and sw) else (30 if ph else 0)
        avail = 210 * (100 - width_pct) / 100 - 20
        return (f'<header class="hd-diag" style="--pw:{width_pct}%">{ph}'
                f'<div class="hd-banner">{_name_block(c, d, _name_size(name, avail, 34))}</div></header>')
    if h == "full_band":
        ph = _photo_html(photo_uri, name, d["photo"], "hd-avatar")
        avail = 210 - 24 - (40 if ph else 0)
        return f'<header class="hd-band pos-{d.get("photo_position", "left")} acc-{d.get("header_accent", "none")}">{ph}<div class="hd-txt">{_name_block(c, d, _name_size(name, avail, 32))}</div></header>'
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
    }.get(hs, "")      # square_icon / dot markers come from _css_extra
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
aside{{width:var(--sw);flex:none;padding:7mm 6mm 10mm 8mm;color:var(--side-text);-webkit-box-decoration-break:clone;box-decoration-break:clone}}
.lay-sidebar_right aside{{padding:7mm 8mm 10mm 6mm}}
main{{flex:1;min-width:0;padding:7mm 12mm 10mm 8mm;-webkit-box-decoration-break:clone;box-decoration-break:clone}}
.lay-sidebar_right main{{padding:7mm 8mm 10mm 12mm}}
.lay-single_column main{{padding:8mm 15mm 12mm}}
h2,.nm,.ttl,.comp-t,.job-role{{font-family:{head_font}}}
.sec{{margin-bottom:calc(6.5mm*var(--s))}}
.sec h2{{color:var(--heading);font-size:calc(15pt*var(--s));font-weight:700;text-transform:uppercase;margin:0 0 3.2mm;line-height:1.08;
letter-spacing:.3px;break-after:avoid;{h2}}}
aside .sec h2{{color:var(--side-heading)}}
{side_h2_fix}
.sec p{{margin:0 0 2.4mm;line-height:1.6}}
aside .sec{{font-size:calc(9.2pt*var(--s))}}
ul{{margin:0;padding-left:4.2mm}}
li{{margin-bottom:1.2mm;line-height:1.5}}
.bul li::marker{{color:var(--accent)}}
aside .bul{{font-size:calc(8.6pt*var(--s))}}
.ic-list{{list-style:none;padding:0}}
.ic-list li{{display:flex;gap:2.4mm;align-items:flex-start}}
.li-ic{{flex:none;height:1.5em;display:flex;align-items:center}} .li-ic svg{{display:block}}
.ct{{display:flex;gap:2.6mm;align-items:flex-start;margin-bottom:2.2mm;font-size:calc(8.8pt*var(--s));line-height:1.45}}
.ct-ic{{flex:none;display:flex;align-items:center;justify-content:center;width:1.2em;height:1.45em}} .ct-ic svg{{display:block;width:1.05em;height:1.05em}} .ct-v{{word-break:break-word;min-width:0}}
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
.sub-h{{font-family:{head_font};font-weight:700;font-size:calc(9pt*var(--s));letter-spacing:.6px;text-transform:uppercase;color:var(--heading);margin:3.2mm 0 .5mm;opacity:.9}} aside .sub-h{{color:var(--side-heading)}}
.chips>span{{border:1px solid var(--rule);background:var(--tint);color:var(--text);padding:.7mm 2.4mm;border-radius:3mm;font-size:calc(8.4pt*var(--s))}}
aside .chips>span{{background:transparent;border-color:var(--side-rule);color:var(--side-text)}}
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
.edu{{margin-bottom:3.6mm;break-inside:avoid;line-height:1.4}} .edu-deg{{font-weight:700;margin-bottom:.6mm}} .edu-inst{{font-weight:500;margin-bottom:.9mm}} .edu-meta{{color:var(--muted);font-size:.92em}} .edu-meta .sep{{padding:0 1.6mm;opacity:.7}}
aside .edu-meta{{color:var(--side-text);opacity:.8}}
.proj{{margin-bottom:2.4mm}} .proj b{{color:var(--heading)}}
.nm{{font-weight:800;line-height:1.02;letter-spacing:.4px}} .up{{text-transform:uppercase}}
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
.side-top{{text-align:center;margin-bottom:5.5mm}}
.side-top .hd-avatar{{margin:0 auto 4mm;width:31mm;height:31mm;border-color:var(--side-accent)}}
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
    placed = set(side_secs) | set(main_secs) | set(d.get("bottom_sections") or [])
    for key in SECTION_KEYS:      # anything with content but no slot in the design still gets printed
        if key not in placed:
            (side_secs if (lay != "single_column" and key in _SIDEBAR_FRIENDLY - {"skills", "profile"}) else main_secs).append(key)
    return side_secs, main_secs


# ── Free design layer (editor "Design" mode) ──────────────────────────────────────────────────────
# design["free"] = {styles: {element key: {css prop: value}}, groups: {css selector: {...}}, vars: {--primary: …},
#                   fonts: {head, body}, text_scale, shapes: [line / box / text / image / icon …]}
# Element keys ("f:experience.0.role", "s:skills/h2:0", "l:photo") are resolved in the page by _FREE_RT_JS, which
# also draws the shapes (mm coordinates on the page), so the editor and the PDF share one renderer.
# Designs without "free" render exactly as before.
_FREE_FONTS = [   # (name, category, Google Fonts spec or "" for a system font)
    ("Roboto", "sans", "Roboto:wght@300;400;500;700;900"), ("Open Sans", "sans", "Open+Sans:wght@400;600;700"),
    ("Lato", "sans", "Lato:wght@400;700;900"), ("Montserrat", "sans", "Montserrat:wght@400;600;700;800"),
    ("Poppins", "sans", "Poppins:wght@300;400;500;600;700"), ("Inter", "sans", "Inter:wght@400;500;600;700"),
    ("Raleway", "sans", "Raleway:wght@400;600;700"), ("Nunito", "sans", "Nunito:wght@400;600;700"),
    ("Work Sans", "sans", "Work+Sans:wght@400;500;700"), ("Source Sans 3", "sans", "Source+Sans+3:wght@400;600;700"),
    ("Rubik", "sans", "Rubik:wght@400;500;700"), ("Manrope", "sans", "Manrope:wght@400;600;800"),
    ("DM Sans", "sans", "DM+Sans:wght@400;500;700"), ("Josefin Sans", "sans", "Josefin+Sans:wght@400;600;700"),
    ("Quicksand", "sans", "Quicksand:wght@400;600;700"), ("Ubuntu", "sans", "Ubuntu:wght@400;500;700"),
    ("Oswald", "sans", "Oswald:wght@400;500;700"), ("Bebas Neue", "sans", "Bebas+Neue"),
    ("Merriweather", "serif", "Merriweather:wght@400;700"), ("Playfair Display", "serif", "Playfair+Display:wght@400;700"),
    ("Lora", "serif", "Lora:wght@400;600;700"), ("Cormorant Garamond", "serif", "Cormorant+Garamond:wght@400;600;700"),
    ("EB Garamond", "serif", "EB+Garamond:wght@400;600;700"), ("PT Serif", "serif", "PT+Serif:wght@400;700"),
    ("Libre Baskerville", "serif", "Libre+Baskerville:wght@400;700"), ("Crimson Text", "serif", "Crimson+Text:wght@400;600;700"),
    ("JetBrains Mono", "mono", "JetBrains+Mono:wght@400;700"), ("Dancing Script", "script", "Dancing+Script:wght@400;700"),
    ("Great Vibes", "script", "Great+Vibes"), ("Pacifico", "script", "Pacifico"),
    ("Segoe UI", "sans", ""), ("Arial", "sans", ""), ("Calibri", "sans", ""), ("Verdana", "sans", ""),
    ("Tahoma", "sans", ""), ("Trebuchet MS", "sans", ""), ("Georgia", "serif", ""), ("Cambria", "serif", ""),
    ("Times New Roman", "serif", ""), ("Garamond", "serif", ""), ("Courier New", "mono", ""),
]
_FREE_PROPS = {
    "color", "background-color", "font-family", "font-size", "font-weight", "font-style", "text-decoration",
    "text-align", "text-transform", "letter-spacing", "line-height", "opacity", "border-radius", "border",
    "border-width", "border-style", "border-color", "translate", "rotate", "scale", "width", "height", "display",
    "clip-path", "padding", "margin-top", "margin-bottom", "z-index", "box-shadow", "background-size",
    "background-position", "filter", "visibility", "max-width", "min-height", "text-shadow",
}
_SHAPE_TYPES = {"line", "rect", "ellipse", "triangle", "diamond", "hexagon", "pentagon", "star", "wave", "curve",
                "text", "image", "icon"}
_SHAPE_NUM = {"x", "y", "w", "h", "x1", "y1", "x2", "y2", "mx", "my", "rot", "sw", "opacity", "radius", "size", "lh",
              "pad", "zoom", "px", "py", "ls", "weight"}
_SHAPE_STR = {"id", "type", "fill", "stroke", "dash", "arrow", "z", "text", "font", "ff", "color", "align", "shape", "icon",
              "path"}
_SHAPE_BOOL = {"bold", "italic", "underline", "upper", "fx", "fy"}


def _css_val(v) -> str:
    v = str(v if v is not None else "").strip()[:240]
    if not v or re.search(r"[{}<>;\\]|url\s*\(|expression|@import|javascript:", v, re.I):
        return ""
    return v


def _clean_free(f) -> dict:
    """Whitelist the editor's free-design JSON (it ends up in CSS and in the page script)."""
    if not isinstance(f, dict):
        return {}
    out: dict = {}
    for name, key_ok in (("styles", r"[\w\-.:/ ]{1,300}"), ("groups", r"[\w\-.\[\]=\"'^$*>:#() ,]{1,300}")):
        got = {}
        for k, props in list((f.get(name) or {}).items())[:500]:
            if not isinstance(props, dict) or not re.fullmatch(key_ok, str(k)):
                continue
            p = {n: v for n, v in ((str(n), _css_val(v)) for n, v in props.items()) if n in _FREE_PROPS and v}
            if p:
                got[str(k)] = p
        if got:
            out[name] = got
    fv = {k: _css_val(v) for k, v in (f.get("vars") or {}).items() if re.fullmatch(r"--[a-z][a-z0-9-]{0,30}", str(k))}
    if any(fv.values()):
        out["vars"] = {k: v for k, v in fv.items() if v}
    names = {n for n, _, _ in _FREE_FONTS}
    fonts = {k: v for k, v in (f.get("fonts") or {}).items() if k in ("head", "body") and v in names}
    if fonts:
        out["fonts"] = fonts
    try:
        ts = round(max(0.6, min(1.6, float(f.get("text_scale") or 1))), 3)
    except Exception:
        ts = 1.0
    if ts != 1.0:
        out["text_scale"] = ts
    shapes = []
    for s in (f.get("shapes") or [])[:200]:
        if not isinstance(s, dict) or s.get("type") not in _SHAPE_TYPES:
            continue
        t = {}
        for k, v in s.items():
            if k in _SHAPE_NUM:
                try:
                    t[k] = round(max(-2000.0, min(5000.0, float(v))), 4)
                except Exception:
                    pass
            elif k in _SHAPE_BOOL:
                t[k] = bool(v)
            elif k in _SHAPE_STR and v is not None:
                t[k] = str(v)[:4000] if k == "text" else (str(v)[:400] if k == "path" else _css_val(v)[:200 if k == "ff" else 80])
        if t.get("type") == "image" and not (t.get("path") and os.path.isfile(t["path"])
                                             and t["path"].lower().endswith(_IMG_EXTS)):
            continue
        if t.get("font") not in names:
            t.pop("font", None)
        t["id"] = re.sub(r"[^\w-]", "", t.get("id") or "") or f"s{len(shapes) + 1}"
        shapes.append(t)
    if shapes:
        out["shapes"] = shapes
    return out


def _free_of(d: dict) -> dict:
    f = d.get("free")
    return f if isinstance(f, dict) else {}


def _free_html(d: dict, edit: bool) -> str:
    """The free-design layer: font links, a style element, the shapes layer and the runtime script."""
    f = _free_of(d)
    if not edit and not f:
        return ""
    shapes = []
    for s in f.get("shapes") or []:
        s = dict(s)
        if s.get("type") == "image":
            s["src"] = _data_uri(s.get("path") or "") if os.path.isfile(s.get("path") or "") else ""
        shapes.append(s)
    used = {f.get("fonts", {}).get("head"), f.get("fonts", {}).get("body")} | {s.get("font") for s in shapes}
    for props in list((f.get("styles") or {}).values()) + list((f.get("groups") or {}).values()):
        used.add(props.get("font-family"))
    specs = [g for n, _, g in _FREE_FONTS if g and n in used]
    links = "".join(f'<link href="https://fonts.googleapis.com/css2?family={g}&display=swap" rel="stylesheet">' for g in specs)
    icon_names = list(_ICONS) if edit else sorted({s.get("icon") or "star" for s in shapes if s.get("type") == "icon"})
    data = {"styles": f.get("styles") or {}, "groups": f.get("groups") or {}, "vars": f.get("vars") or {},
            "fonts": f.get("fonts") or {}, "text_scale": f.get("text_scale") or 1, "shapes": shapes,
            "fontcat": {n: cat for n, cat, _ in _FREE_FONTS},
            "icons": {n: _icon(n, "currentColor", "100%") for n in icon_names},
            "waves": {k: list(v) for k, v in _SHAPES.items()}}
    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    return (f'{links}<style id="rb-free-css"></style><div id="rb-free"></div>'
            f'<script>window.__RBF__ = {blob};</script><script>{_FREE_RT_JS}</script>')


_FREE_RT_JS = r"""
(function(){
const D = window.__RBF__ = window.__RBF__ || {};
const MM = 96 / 25.4;
const FALL = {serif: 'Georgia, serif', mono: 'Consolas, monospace', script: 'cursive', sans: "'Segoe UI', Arial, sans-serif"};
function stack(n){ return n ? "'" + String(n).replace(/'/g, '') + "', " + (FALL[(D.fontcat || {})[n]] || FALL.sans) : ''; }
const LANDMARKS = [['photo', '.hd-avatar,.hd-photo'], ['name', '.nm'], ['headline', '.ttl'], ['sidetop', '.side-top'],
  ['maintop', '.main-top'], ['header', 'header'], ['sidebg', '.side-bg'], ['footer', '.rb-foot'], ['decor', '.rb-decor'],
  ['aside', 'aside'], ['main', 'main'], ['bottom', '.bottom'], ['cols', '.cols']];
function skip(el){
  return !el || el.nodeType !== 1 || (el.id && el.id.indexOf('rb-') === 0) || el.classList.contains('edit-only') ||
    el.classList.contains('rbs') || /^(SCRIPT|STYLE|LINK|BR)$/.test(el.tagName);
}
function sig(el){
  const cls = Array.from(el.classList).filter(c => c.indexOf('rb') !== 0 && c !== 'up').sort();
  return el.tagName.toLowerCase() + (cls.length ? '.' + cls.join('.') : '');
}
function anchorOf(el){
  if (el.hasAttribute('data-f')) return 'f:' + el.getAttribute('data-f');
  if (el.hasAttribute('data-item')) return 'i:' + el.getAttribute('data-item');
  if (el.tagName === 'SECTION') { const m = el.className.match(/\bsec-(\w+)/); if (m) return 's:' + m[1]; }
  for (const [n, sel] of LANDMARKS) if (el.matches(sel)) return 'l:' + n;
  if (el === document.body) return 'l:body';
  return null;
}
function keyOf(el){
  const steps = [];
  let cur = el;
  while (cur && cur.nodeType === 1) {
    const a = anchorOf(cur);
    if (a) return steps.length ? a + '/' + steps.reverse().join('/') : a;
    const p = cur.parentElement;
    if (!p) return null;
    const s = sig(cur);
    let n = 0;
    for (const sib of p.children) { if (sib === cur) break; if (!skip(sib) && sig(sib) === s) n++; }
    steps.push(s + ':' + n);
    cur = p;
  }
  return null;
}
function anchorFind(a){
  const t = a.slice(0, 1), v = a.slice(2);
  const q = s => { try { return document.querySelector(s); } catch (e) { return null; } };
  if (t === 'f') return q('[data-f="' + CSS.escape(v) + '"]');
  if (t === 'i') return q('[data-item="' + CSS.escape(v) + '"]');
  if (t === 's') return q('section.sec-' + CSS.escape(v));
  if (v === 'body') return document.body;
  const lm = LANDMARKS.find(x => x[0] === v);
  return lm ? q(lm[1]) : null;
}
function find(key){
  const parts = String(key).split('/');
  let el = anchorFind(parts[0]);
  for (let i = 1; el && i < parts.length; i++) {
    const j = parts[i].lastIndexOf(':'), s = parts[i].slice(0, j), n = +parts[i].slice(j + 1);
    let k = 0, hit = null;
    for (const ch of el.children) { if (skip(ch) || sig(ch) !== s) continue; if (k++ === n) { hit = ch; break; } }
    el = hit;
  }
  return el;
}
function val(p, v){ return p === 'font-family' ? stack(v) : v; }
const BOXY = ['translate', 'rotate', 'scale', 'width', 'height'];
let touched = [];
function applyStyles(){
  touched.forEach(el => { if (el.__rbo === null) el.removeAttribute('style'); else el.setAttribute('style', el.__rbo); });
  touched = [];
  for (const [k, props] of Object.entries(D.styles || {})) {
    const el = find(k);
    if (!el) continue;
    if (!('__rbo' in el)) el.__rbo = el.getAttribute('style');
    touched.push(el);
    for (const [p, v] of Object.entries(props)) if (v !== '' && v != null) el.style.setProperty(p, val(p, v), 'important');
    if (!props.display && BOXY.some(p => props[p]) && getComputedStyle(el).display === 'inline')
      el.style.setProperty('display', 'inline-block', 'important');   // transforms don't apply to inline boxes
  }
}
function buildCss(){
  let out = '';
  const vars = Object.entries(D.vars || {}).filter(x => x[1]);
  if (vars.length) out += ':root{' + vars.map(([k, v]) => k + ':' + v + ' !important').join(';') + '}';
  const f = D.fonts || {};
  if (f.body) out += 'html body{font-family:' + stack(f.body) + '}';
  if (f.head) out += 'html body h2,html body .nm,html body .ttl,html body .comp-t,html body .job-role,html body .addl-h,html body .sub-h,html body .venn{font-family:' + stack(f.head) + '}';
  for (const [sel, props] of Object.entries(D.groups || {})) {
    const decl = Object.entries(props).filter(x => x[1] !== '' && x[1] != null).map(([p, v]) => p + ':' + val(p, v) + ' !important');
    if (BOXY.some(p => props[p]) && !props.display) decl.push('display:inline-block');
    if (decl.length) out += sel + '{' + decl.join(';') + '}';
  }
  if (D.shapes && D.shapes.length) out += 'body{position:relative}';
  out += '#rb-free{position:absolute;left:0;top:0;width:210mm;height:0;pointer-events:none}' +
         '.rbs{position:absolute;box-sizing:border-box}.rbs-in{width:100%;height:100%;box-sizing:border-box;overflow:hidden}' +
         '.rbs-txt{white-space:pre-wrap;overflow-wrap:break-word;box-sizing:border-box}';
  const st = document.getElementById('rb-free-css');
  if (st) st.textContent = out;
}
const POLY = {triangle: '50,0 100,100 0,100', diamond: '50,0 100,50 50,100 0,50',
  hexagon: '25,0 75,0 100,50 75,100 25,100 0,50', pentagon: '50,0 100,38 82,100 18,100 0,38',
  star: '50,0 61,35 98,35 68,57 79,91 50,70 21,91 32,57 2,35 39,35'};
const CLIP = {circle: 'circle(50% at 50% 50%)', ellipse: 'ellipse(50% 50% at 50% 50%)'};
for (const [k, v] of Object.entries(POLY)) CLIP[k] = 'polygon(' + v.split(' ').map(p => p.split(',').map(n => n + '%').join(' ')).join(',') + ')';
function a(v){ return String(v == null ? '' : v).replace(/[<>"&]/g, ''); }
function dashOf(s, w){ return s.dash === 'dashed' ? (w * 4) + ' ' + (w * 2.5) : s.dash === 'dotted' ? '0.01 ' + (w * 2.2) : ''; }
function build(s){
  const w = document.createElement('div');
  w.className = 'rbs rbs-' + s.type;
  w.dataset.sid = s.id;
  const st = w.style;
  st.zIndex = s.z === 'back' ? 0 : 5;
  st.opacity = s.opacity == null ? 1 : s.opacity;
  const stroke = s.stroke || 'none', fill = s.fill || 'none';
  if (s.type === 'line') {
    const sw = Math.max(0.05, (s.sw == null ? 1.5 : s.sw) * 0.3528);
    const mx = s.mx == null ? (s.x1 + s.x2) / 2 : s.mx, my = s.my == null ? (s.y1 + s.y2) / 2 : s.my;
    const qx = 2 * mx - (s.x1 + s.x2) / 2, qy = 2 * my - (s.y1 + s.y2) / 2, pad = sw * 5 + 2;
    const x0 = Math.min(s.x1, s.x2, qx) - pad, y0 = Math.min(s.y1, s.y2, qy) - pad;
    const W = Math.max(s.x1, s.x2, qx) + pad - x0, H = Math.max(s.y1, s.y2, qy) + pad - y0;
    Object.assign(st, {left: x0 + 'mm', top: y0 + 'mm', width: W + 'mm', height: H + 'mm'});
    const d = 'M' + s.x1 + ' ' + s.y1 + ' Q' + qx + ' ' + qy + ' ' + s.x2 + ' ' + s.y2;
    const col = a(s.stroke || '#111827'), id = 'ah-' + a(s.id), ar = s.arrow || 'none';
    const mk = ar === 'none' ? '' : '<defs><marker id="' + id + '" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="' + col + '"/></marker></defs>';
    const ends = (ar === 'end' || ar === 'both' ? ' marker-end="url(#' + id + ')"' : '') + (ar === 'start' || ar === 'both' ? ' marker-start="url(#' + id + ')"' : '');
    w.innerHTML = '<svg viewBox="' + x0 + ' ' + y0 + ' ' + W + ' ' + H + '" width="100%" height="100%" style="display:block;overflow:visible">' + mk +
      '<path class="rbs-hit" d="' + d + '" fill="none" stroke="transparent" stroke-width="' + Math.max(sw, 3.5) + '"/>' +
      '<path d="' + d + '" fill="none" stroke="' + col + '" stroke-width="' + sw + '" stroke-linecap="round" stroke-dasharray="' + dashOf(s, sw) + '"' + ends + '/></svg>';
    return w;
  }
  Object.assign(st, {left: (s.x || 0) + 'mm', top: (s.y || 0) + 'mm', width: (s.w || 30) + 'mm'});
  if (s.type !== 'text') st.height = (s.h || 20) + 'mm';
  if (s.rot) st.rotate = s.rot + 'deg';
  if ((s.fx || s.fy) && s.type !== 'text') st.scale = (s.fx ? -1 : 1) + ' ' + (s.fy ? -1 : 1);
  const swpt = s.sw == null ? 0 : s.sw;
  const border = swpt > 0 && stroke !== 'none' ? swpt + 'pt ' + (s.dash === 'dashed' ? 'dashed' : s.dash === 'dotted' ? 'dotted' : 'solid') + ' ' + a(stroke) : 'none';
  const inner = document.createElement('div');
  inner.className = 'rbs-in';
  if (s.type === 'rect' || s.type === 'ellipse') {
    Object.assign(inner.style, {background: fill === 'none' ? 'transparent' : fill, border: border,
      borderRadius: s.type === 'ellipse' ? '50%' : (s.radius || 0) + 'mm'});
  } else if (POLY[s.type] || s.type === 'wave' || s.type === 'curve') {
    inner.style.overflow = 'visible';
    const f = fill === 'none' ? 'none' : a(fill), k = a(stroke), px = swpt * 1.333;
    const common = ' stroke="' + (swpt > 0 ? k : 'none') + '" stroke-width="' + px + '" vector-effect="non-scaling-stroke" stroke-linejoin="round" stroke-dasharray="' + dashOf(s, px) + '"';
    if (POLY[s.type]) {
      inner.innerHTML = '<svg viewBox="0 0 100 100" preserveAspectRatio="none" width="100%" height="100%" style="display:block;overflow:visible"><polygon points="' + POLY[s.type] + '" fill="' + f + '"' + common + '/></svg>';
    } else {
      const p = (D.waves || {})[s.type === 'wave' ? 'wave' : 'curve'] || ['', ''];
      inner.innerHTML = '<svg viewBox="0 0 1000 300" preserveAspectRatio="none" width="100%" height="100%" style="display:block;overflow:visible"><path d="' + p[1] + '" fill="' + f + '" fill-opacity="0.32"/><path d="' + p[0] + '" fill="' + f + '"' + common + '/></svg>';
    }
  } else if (s.type === 'text') {
    inner.className = 'rbs-in rbs-txt';
    inner.textContent = s.text == null ? 'Your text' : s.text;
    const wt = +s.weight || 0;
    Object.assign(inner.style, {height: 'auto', overflow: 'visible', fontFamily: stack(s.font) || s.ff || 'inherit', fontSize: (s.size || 11) + 'pt',
      color: s.color || '#111827', fontWeight: s.bold ? String(wt >= 600 ? wt : 700) : String(wt && wt < 600 ? wt : 400),
      fontStyle: s.italic ? 'italic' : 'normal',
      textDecoration: s.underline ? 'underline' : 'none', textTransform: s.upper ? 'uppercase' : 'none',
      textAlign: s.align || 'left', lineHeight: String(s.lh || 1.3), letterSpacing: (s.ls || 0) + 'px',
      background: fill === 'none' ? 'transparent' : fill, padding: (s.pad == null ? 1 : s.pad) + 'mm', border: border,
      borderRadius: (s.radius || 0) + 'mm'});
  } else if (s.type === 'image') {
    const shp = s.shape || 'square';
    Object.assign(inner.style, {border: border, borderRadius: shp === 'circle' ? '50%' : shp === 'rounded' ? (s.radius || 4) + 'mm' : '0',
      clipPath: (shp !== 'circle' && CLIP[shp]) || 'none', backgroundImage: s.src ? 'url("' + s.src + '")' : 'none',
      backgroundColor: s.src ? 'transparent' : '#e5e7eb', backgroundRepeat: 'no-repeat',
      backgroundSize: (s.zoom && s.zoom !== 100) ? s.zoom + '%' : 'cover',
      backgroundPosition: (s.px == null ? 50 : s.px) + '% ' + (s.py == null ? 50 : s.py) + '%'});
  } else if (s.type === 'icon') {
    inner.innerHTML = (D.icons || {})[s.icon || 'star'] || (D.icons || {}).star || '';
    Object.assign(inner.style, {color: s.color || s.stroke || '#111827', overflow: 'visible'});
  }
  w.appendChild(inner);
  return w;
}
function renderShapes(){
  const layer = document.getElementById('rb-free');
  if (!layer) return;
  layer.innerHTML = '';
  for (const s of D.shapes || []) { try { layer.appendChild(build(s)); } catch (e) {} }
}
function refresh(){ buildCss(); applyStyles(); renderShapes(); }
window.RBF = {D, MM, stack, keyOf, find, sig, skip, refresh, buildCss, applyStyles, renderShapes, CLIP, POLY};
refresh();
})();
"""


def _render_html(c: dict, d: dict, photo_uri: str, scale: float = 1.0, edit: bool = False) -> str:
    free = _free_of(d)
    token = _EDIT.set(True if edit else ("mark" if (free.get("styles") or free.get("groups")) else False))
    try:
        if d.get("replica"):                 # exact copy of an uploaded design (app/services/resume_replica)
            from app.services.resume_replica.exact_render import render_replica_html
            return render_replica_html(c, d, photo_uri, scale)
        return _render_html_inner(c, d, photo_uri, scale)
    finally:
        _EDIT.reset(token)


def _render_html_inner(c: dict, d: dict, photo_uri: str, scale: float) -> str:
    d = _effective_design(c, d)
    scale *= float(_free_of(d).get("text_scale") or 1)       # editor's global text size
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
    elif d["header"] == "sidebar_photo" and lay != "single_column":
        name = c["name"] or "Your Name"
        ph = _photo_html(photo_uri, name, d["photo"], "hd-avatar")
        top = f'<div class="side-top photo-only">{ph}</div>' if ph else ""
        avail = 210 * (100 - d.get("sidebar_width", 32)) / 100 - 24
        main_html = f'<div class="main-top">{_name_block(c, d, _name_size(name, avail, 24))}</div>' + main_html
    body = (f'<div class="cols"><main>{main_html}</main></div>' if lay == "single_column" else
            f'<div class="side-bg"></div><div class="cols"><aside>{top}{side_html}</aside><main>{main_html}</main></div>')
    bottom_html = "".join(_section_html(k, c, d, False) for k in d.get("bottom_sections") or [])
    if bottom_html:
        body += f'<div class="bottom">{bottom_html}</div>'
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{_e(c["name"] or "Resume")} — Resume</title>'
            f'<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family={gfont}&display=swap" rel="stylesheet">'
            f'<style>{_css(d, scale)}{_css_extra(d, scale)}</style></head><body class="lay-{lay}">'
            f'{_decor_html(d)}{_footer_html(d)}{_header_html(c, d, photo_uri)}{body}{_free_html(d, _EDIT.get() is True)}</body></html>')


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


_SECTION_HEIGHTS_JS = r"""Array.from(document.querySelectorAll('aside > .sec, main > .sec')).map(e => {
  const m = e.className.match(/sec-(\w+)/);
  return [m ? m[1] : '', e.getBoundingClientRect().height + parseFloat(getComputedStyle(e).marginBottom || 0)];
})"""


def _balance_columns(wd: dict, measured: list) -> bool:
    """Greedy: move the section that most reduces the taller column, until no move helps. Profile stays put."""
    h = {k: float(v) for k, v in measured if k}
    left = [k for k in wd["sidebar_sections"] if k in h]
    right = [k for k in wd["main_sections"] if k in h]
    changed = False
    for _ in range(10):
        hl, hr = sum(h[k] for k in left), sum(h[k] for k in right)
        src, dst = (left, right) if hl > hr else (right, left)
        best_k, best_max = None, max(hl, hr) - 15
        for k in src:
            if k == "profile" or k in (wd.get("pinned") or []):
                continue
            new_max = max(hl - h[k], hr + h[k]) if src is left else max(hl + h[k], hr - h[k])
            if new_max < best_max:
                best_k, best_max = k, new_max
        if not best_k:
            break
        src.remove(best_k)
        dst.append(best_k)
        changed = True
    if changed:
        rest_l = [k for k in wd["sidebar_sections"] if k not in h]
        rest_r = [k for k in wd["main_sections"] if k not in h]
        wd["sidebar_sections"], wd["main_sections"] = left + rest_l, right + rest_r
    return changed


def _render_files(c: dict, d: dict, photo_path: str, stem: str, target_pages: int | None = None,
                  start_scale: float = 1.0) -> dict:
    """HTML → PDF (auto-shrinks to avoid a nearly-empty last page) → PNG previews."""
    from playwright.sync_api import sync_playwright
    os.makedirs(OUT_DIR, exist_ok=True)
    photo_uri = _data_uri(photo_path) if photo_path else ""
    pdf_path = os.path.join(OUT_DIR, stem + ".pdf")
    html_path = os.path.join(OUT_DIR, stem + ".html")
    import fitz
    wd = _effective_design(c, d)         # working copy: sections may be moved between columns to fit
    if wd["layout"] != "single_column":
        wd["sidebar_sections"], wd["main_sections"] = _placement(wd)
    if _free_of(wd).get("shapes"):       # shapes sit at fixed page positions: keep the columns as the editor shows them
        wd["pinned"] = list(dict.fromkeys(wd["sidebar_sections"] + wd["main_sections"]))
    if wd.get("replica"):                # exact copy: the reference decides the columns and the type sizes
        wd["pinned"] = list(dict.fromkeys(wd["sidebar_sections"] + wd["main_sections"]))
    moved: set[str] = set()              # never move a section back (stops ping-pong)
    pdf_opts = dict(format="A4", print_background=True, margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
    with sync_playwright() as pw:
        browser = _launch(pw)
        try:
            page = browser.new_page(viewport={"width": 794, "height": 1123})
            page.emulate_media(media="print")
            scale, html, pdf_bytes, moves = start_scale, "", b"", 0
            min_scale = 0.74 if target_pages else 0.79   # a page target allows slightly smaller type
            if wd.get("replica"):                         # exact copy: sizes stay as measured (a page target: ≤ 15 %)
                min_scale = 0.70 if target_pages else 1.0
            best = None                          # (score, pdf_bytes, html) — a later attempt can be worse
            balanced = False
            for _ in range(14):
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
                try:                                       # exact copies lay out (fit, page breaks) after fonts load
                    page.wait_for_function("!document.body.classList.contains('replica') || "
                                           "document.body.dataset.ready === '1'", timeout=10000)
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
                # one readable page beats everything; otherwise prefer a well-filled second page
                # on two pages: a non-trivial page 2 first, then columns that end at similar heights
                cols_h = page.evaluate("[document.querySelector('aside')?.scrollHeight||0, document.querySelector('main')?.scrollHeight||0]")
                imbalance = round(abs(cols_h[0] - cols_h[1]) / 60) if wd["layout"] != "single_column" else 0
                if target_pages and pages <= target_pages:
                    score = (3, scale, fill)               # meets the user's page target: biggest type wins
                else:
                    score = (2, scale) if pages == 1 else ((1, fill >= 0.2, -imbalance, fill) if pages == 2 else (0, -pages))
                if best is None or score > best[0]:
                    best = (score, pdf_bytes, html, scale)
                if pages == 1 or (target_pages and pages <= target_pages):
                    break
                # 0) equal columns: measure every section once and even the columns out in one pass
                if wd["layout"] == "two_column" and not balanced:
                    balanced = True
                    if _balance_columns(wd, page.evaluate(_SECTION_HEIGHTS_JS)):
                        continue
                # a bottom strip (e.g. contact row) alone on page 2 → fold it into the shorter column
                if pages == 2 and fill < 0.1 and wd.get("bottom_sections") and wd["layout"] != "single_column":
                    side_h, main_h = page.evaluate("[document.querySelector('aside')?.scrollHeight||0, document.querySelector('main')?.scrollHeight||0]")
                    wd["sidebar_sections" if side_h <= main_h else "main_sections"].extend(wd["bottom_sections"])
                    wd["bottom_sections"] = []
                    continue
                good_two = pages == 2 and fill > 0.45 and not target_pages   # acceptable, but still even out the columns
                # 1) move a section from the end of the longer column to the shorter one
                if wd["layout"] != "single_column" and moves < 4:
                    side_h, main_h = page.evaluate("[document.querySelector('aside')?.scrollHeight||0, document.querySelector('main')?.scrollHeight||0]")
                    thr = 150 if good_two else 60
                    pinned = set(wd.get("pinned") or [])
                    to_side = (lambda k: k not in pinned) if wd["layout"] == "two_column" else \
                        (lambda k: k in _SIDEBAR_FRIENDLY - {"skills", "profile"} and k not in pinned)
                    if side_h + thr < main_h:
                        movable = [k for k in reversed(wd["main_sections"]) if to_side(k)
                                   and k not in moved and _section_html(k, c, wd, True)]
                        src, dst = "main_sections", "sidebar_sections"
                    elif main_h + thr < side_h:
                        movable = [k for k in reversed(wd["sidebar_sections"]) if k not in ("contact", "profile")
                                   and k not in moved and k not in pinned and _section_html(k, c, wd, False)]
                        src, dst = "sidebar_sections", "main_sections"
                    else:
                        movable = []
                    if movable:
                        wd[src].remove(movable[0])
                        wd[dst].append(movable[0])
                        moved.add(movable[0])
                        moves += 1
                        continue
                if good_two:
                    break
                # 2) otherwise shrink the type a little
                if scale - 0.04 < min_scale:
                    break
                scale -= 0.04
            try:
                cols_h = page.evaluate("[document.querySelector('aside')?.scrollHeight||0, document.querySelector('main')?.scrollHeight||0]")
            except Exception:
                cols_h = [0, 0]
        finally:
            browser.close()
    if wd["layout"] == "single_column":
        long_col = list(wd["main_sections"])
    else:
        long_col = list(wd["main_sections"] if cols_h[1] >= cols_h[0] else wd["sidebar_sections"])
    if best:
        pdf_bytes, html, scale = best[1], best[2], best[3]
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
    return {"pdf": pdf_path, "html": html_path, "pngs": pngs, "pages": n_pages, "long_column": long_col,
            "scale": round(float(scale), 4)}


# ── Strict page target ("single page resume", "2 pages") ─────────────────────────────────────────
_PAGES_RX = re.compile(r"\b(one|single|1|two|2|three|3)[\s-]*pages?\b|\bpages?\s*(?:limit|count)?\s*[:=]?\s*(1|2|3)\b|\bone[\s-]?pager\b", re.I)


def _parse_pages(text: str) -> int | None:
    m = _PAGES_RX.search(text or "")
    if not m:
        return None
    if "pager" in m.group(0).lower():
        return 1
    word = (m.group(1) or m.group(2) or "").lower()
    return {"one": 1, "single": 1, "1": 1, "two": 2, "2": 2, "three": 3, "3": 3}.get(word)


_CONDENSE_SYSTEM = """You shorten resumes to fit a page limit. Return the FULL resume JSON in the same shape.
- Keep every real section, job, project, degree and award — shorten wording instead of deleting facts where possible.
- Only shorten the sections listed as TOO LONG; return the others exactly as they are.
- When a bullet must go, drop the most generic one; keep bullets with results, numbers or awards.
- Copy every number exactly as written (30,000+, 99.05, 5%) — never abbreviate or round them.
- Bullets: at most 3 per entry, each <= 14 words. Profile: one paragraph <= 40 words. Descriptions <= 18 words.
- If it still can't fit, drop the least important items first (extra skills, minor bullets, duplicate points).
- NEVER invent anything or add numbers that aren't already in the JSON. Keep section_titles and layout_hint unchanged."""


def _condense_content(content: dict, target: int, pages: int, long_keys: list | None = None) -> dict:
    keys = [k for k in (long_keys or SECTION_KEYS) if k != "contact"]
    user = (f"The resume currently prints on {pages} A4 page(s); it MUST fit on {target}. "
            f"TOO LONG sections: {', '.join(keys)}. Cut roughly {max(15, int(100 * (pages - target) / max(pages, 1)))}% "
            f"of their text.\n\nRESUME JSON:\n" + json.dumps(content, ensure_ascii=False))
    try:
        data = _llm_json(_CONDENSE_SYSTEM, user)
    except Exception as e:
        print(f"[resume] condense failed: {e}")
        return content
    out = _drop_invented(_normalise_content(data), json.dumps(content, ensure_ascii=False))
    for k in ("section_titles", "layout_hint", "custom_sections"):
        out[k] = content.get(k) or out.get(k)
    for k in SECTION_KEYS:                       # columns that weren't overflowing stay untouched
        if k not in keys and k in content:
            out[k] = content[k]
    if "skills" not in keys:
        out["additional_skills"] = content["additional_skills"]
    if not out["name"]:
        out["name"], out["title"], out["contact"] = content["name"], content["title"], content["contact"]
    return out if (out["experience"] or out["projects"] or out["profile"]) else content


def _cap_bullets(c: dict, n: int) -> bool:
    changed = False
    for e in c["experience"] + c["projects"]:
        if len(e.get("bullets", [])) > n:
            e["bullets"] = e["bullets"][:n]
            changed = True
    return changed


def _cap(c: dict, key: str, n: int) -> bool:
    if len(c.get(key) or []) > n:
        c[key] = c[key][:n]
        return True
    return False


def _short_profile(c: dict, words: int) -> bool:
    text = " ".join(c["profile"])
    if len(text.split()) <= words and len(c["profile"]) <= 1:
        return False
    sentences, out = re.split(r"(?<=[.!?])\s+", text), []
    for snt in sentences:
        if out and len(" ".join(out + [snt]).split()) > words:
            break
        out.append(snt)
    c["profile"] = [" ".join(out)]
    return True


# least important first; each step returns True if it changed something
_TRIM_STEPS = [
    lambda c: _cap(c, "references", 0), lambda c: _cap(c, "interests", 0), lambda c: _short_profile(c, 60),
    lambda c: _cap_bullets(c, 3), lambda c: _cap(c, "highlights", 2), lambda c: _cap(c, "competencies", 4),
    lambda c: _cap(c, "additional_skills", 8), lambda c: _cap(c, "skills", 7), lambda c: _short_profile(c, 40),
    lambda c: _cap_bullets(c, 2), lambda c: _cap(c, "certifications", 3), lambda c: _cap(c, "achievements", 3),
    lambda c: _cap(c, "highlights", 0), lambda c: _cap(c, "competencies", 0), lambda c: _cap(c, "additional_skills", 4),
    lambda c: _cap(c, "education", 2), lambda c: _short_profile(c, 25), lambda c: _cap_bullets(c, 1),
]


def _fit_render(content: dict, design: dict, photo: str, stem: str, target: int | None):
    """Render; with a page target, shrink → AI-condense → trim until it fits. Returns (files, content, note)."""
    files = _render_files(content, design, photo, stem, target)
    if not target or files["pages"] <= target:
        return files, content, ""
    content = _condense_content(json.loads(json.dumps(content)), target, files["pages"], files.get("long_column"))
    files = _render_files(content, design, photo, stem, target, start_scale=0.92)
    note = "condensed the wording"
    trimmed = 0
    for step in _TRIM_STEPS:
        if files["pages"] <= target:
            break
        before = json.loads(json.dumps(content))
        if step(content):
            changed = [k for k in SECTION_KEYS if content.get(k) != before.get(k)] + \
                      (["skills"] if content["additional_skills"] != before["additional_skills"] else [])
            if not set(changed) & set(files.get("long_column") or SECTION_KEYS):
                content = before                     # that section isn't in the overflowing column
                continue
            trimmed += 1
            files = _render_files(content, design, photo, stem, target, start_scale=0.86)
    if trimmed:
        note += " and trimmed the least important items"
    if files["pages"] > target:
        note += f" — still {files['pages']} pages, the content is too long for {target}"
    return files, content, note


# ── Visual editor (/resume/editor) ───────────────────────────────────────────────────────────────
# The resume is rendered with every text value as a contenteditable span tagged with its JSON path
# (_f / _it above). The page posts the edited content back to /resume/save (editor_save), which also
# handles list operations, template/colour/photo changes, AI rewrites and PDF export.
EDITOR_URL = "http://127.0.0.1:8000/resume/editor"

_ITEM_TEMPLATES = {
    "bullets": "New point: what you did and the result",
    "profile": "Write a short profile paragraph here.",
    "highlights": "New highlight", "achievements": "New achievement", "certifications": "New certification",
    "references": "Available on request", "interests": "New interest", "additional_skills": "New skill",
    "skills": {"name": "New skill", "level": 80},
    "competencies": {"title": "New competency", "description": "Describe this strength in one line.", "icon": ""},
    "experience": {"role": "Job title", "company": "Company", "period": "Start – End", "location": "",
                   "bullets": ["What you achieved there"]},
    "education": {"degree": "Degree / course", "institution": "Institution", "period": "", "details": ""},
    "languages": {"name": "Language", "level": 4},
    "projects": {"name": "Project name", "tech": "Tech stack", "period": "", "bullets": ["What you built and the result"],
                 "description": ""},
}
_ADDABLE = ["profile", "highlights", "skills", "competencies", "experience", "education", "projects",
            "achievements", "certifications", "languages", "interests", "references"]

_EDITOR_CSS = """
<style id="rb-editor-css">
html{background:#2f333b!important}
html.rb-pan{padding-right:322px}
body{position:relative;margin:76px auto 60px!important;box-shadow:0 8px 44px rgba(0,0,0,.5);min-height:297mm}
.side-bg,.rb-foot,.rb-decor{position:absolute!important}
body::after{content:"";position:absolute;inset:0;pointer-events:none;z-index:40;
 background:repeating-linear-gradient(to bottom,transparent 0,transparent calc(297mm - 2px),rgba(239,68,68,.8) calc(297mm - 2px),rgba(239,68,68,.8) 297mm)}
[data-f]{outline:none;border-radius:2px;cursor:text;transition:background .12s,box-shadow .12s;display:inline;padding:0 1px}
[data-f]:hover{background:rgba(59,130,246,.10);box-shadow:0 0 0 1px rgba(59,130,246,.45)}
[data-f]:focus{background:rgba(59,130,246,.15);box-shadow:0 0 0 2px rgba(59,130,246,.8)}
[data-f]:empty::before{content:attr(data-ph);color:#9ca3af;font-style:italic;font-weight:400;text-transform:none;letter-spacing:0}
[data-item]{position:relative}
[data-item].rb-hot{box-shadow:0 0 0 1px dashed rgba(16,185,129,.6);outline:1px dashed rgba(16,185,129,.7);outline-offset:1px}
.ed-venn{text-align:center;font-size:8pt;margin:-1mm 0 2.5mm;color:#6b7280}
.ed-chip{display:inline-block;border:1px dashed #9ca3af;border-radius:3mm;padding:.4mm 2.2mm;margin:0 .8mm;color:#374151}
#rb-bar{position:fixed;top:0;left:0;right:0;z-index:1000;display:flex;flex-wrap:wrap;gap:8px;align-items:center;
 padding:10px 14px;background:#0b1220;color:#e5e7eb;font:13px 'Segoe UI',Arial,sans-serif;box-shadow:0 2px 14px rgba(0,0,0,.5)}
#rb-bar b{color:#67e8f9;margin-right:4px}
#rb-bar select,#rb-bar input[type=text]{background:#111a2e;color:#e5e7eb;border:1px solid #334155;border-radius:6px;padding:6px 8px;font:inherit}
#rb-bar input[type=text]{width:230px}
#rb-bar input[type=color]{width:34px;height:30px;border:1px solid #334155;border-radius:6px;background:#111a2e;padding:2px;cursor:pointer}
#rb-bar button,#rb-bar label.btn{background:#1e293b;color:#e5e7eb;border:1px solid #334155;border-radius:6px;padding:6px 10px;font:inherit;cursor:pointer}
#rb-bar button:hover,#rb-bar label.btn:hover{background:#334155}
#rb-bar button.primary{background:#0891b2;border-color:#06b6d4;color:#fff;font-weight:600}
#rb-bar button.primary:hover{background:#06b6d4}
#rb-bar .seg{display:inline-flex;border:1px solid #334155;border-radius:6px;overflow:hidden}
#rb-bar .seg button{border:0;border-radius:0}
#rb-bar .seg button.on,#rb-bar button.on{background:#0891b2;color:#fff}
#rb-status{margin-left:auto;color:#a5f3fc;max-width:420px}
#rb-status a{color:#fde68a}
#rb-hint{position:fixed;bottom:12px;left:50%;transform:translateX(-50%);z-index:1000;background:#0b1220e6;color:#cbd5e1;
 font:12px 'Segoe UI',Arial;padding:6px 12px;border-radius:20px}
#rb-ctl,#rb-sctl{position:absolute;display:none;z-index:1001;gap:3px;background:#0b1220;border-radius:6px;padding:3px;box-shadow:0 2px 8px rgba(0,0,0,.4)}
#rb-sctl{flex-direction:column}
#rb-ctl button,#rb-sctl button{background:#1e293b;color:#fff;border:0;border-radius:4px;width:24px;height:22px;cursor:pointer;font:13px Arial;line-height:22px;padding:0}
#rb-ctl button:hover,#rb-sctl button:hover{background:#0891b2} #rb-ctl button[data-a=del]:hover,#rb-sctl button[data-a=hide]:hover{background:#dc2626}
#rb-panel{position:fixed;right:0;bottom:0;width:312px;z-index:1001;background:#0f172a;color:#e2e8f0;font:12px 'Segoe UI',Arial,sans-serif;
 overflow:auto;box-shadow:-4px 0 18px rgba(0,0,0,.45);display:none}
html.rb-pan #rb-panel{display:block}
#rb-panel .tabs{display:flex;position:sticky;top:0;background:#0b1220;z-index:2;border-bottom:1px solid #1e293b}
#rb-panel .tabs button{flex:1;background:none;border:0;border-bottom:2px solid transparent;border-radius:0;color:#94a3b8;padding:9px 4px;font-weight:600}
#rb-panel .tabs button.on{border-bottom-color:#06b6d4;color:#fff;background:none}
#rb-panel .grp{padding:8px 12px;border-bottom:1px solid #1e293b}
#rb-panel h4{margin:2px 0 8px;font-size:10.5px;letter-spacing:.8px;text-transform:uppercase;color:#67e8f9}
#rb-panel .pr{display:flex;align-items:center;gap:8px;margin:5px 0}
#rb-panel .pr>label{width:82px;flex:none;color:#94a3b8}
#rb-panel .pr>div{flex:1;display:flex;gap:4px;align-items:center;flex-wrap:wrap;min-width:0}
#rb-panel input[type=number],#rb-panel select,#rb-panel input[type=text],#rb-panel textarea{background:#111a2e;color:#e5e7eb;border:1px solid #334155;border-radius:5px;padding:4px 6px;font:inherit;min-width:0}
#rb-panel input[type=number]{width:62px}
#rb-panel select{max-width:178px}
#rb-panel textarea{width:100%;min-height:54px;resize:vertical}
#rb-panel input[type=color]{width:30px;height:24px;padding:1px;border:1px solid #334155;border-radius:4px;background:#111a2e;cursor:pointer}
#rb-panel input[type=range]{flex:1;min-width:70px;accent-color:#06b6d4}
#rb-panel button{background:#1e293b;color:#e5e7eb;border:1px solid #334155;border-radius:5px;padding:4px 8px;font:inherit;cursor:pointer}
#rb-panel button:hover{background:#334155}
#rb-panel button.on{background:#0891b2;border-color:#06b6d4;color:#fff}
#rb-panel button.danger:hover{background:#dc2626}
#rb-panel .muted{color:#64748b;font-size:11px;line-height:1.5;margin:4px 0}
#rb-panel .sec-row{display:flex;align-items:center;gap:3px;padding:2px 0}
#rb-panel .sec-row span{flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
#rb-panel .sec-row button{padding:2px 6px}
#rb-panel .val{min-width:34px;color:#94a3b8;text-align:right}
body.rb-design{user-select:none;-webkit-user-select:none}
body.rb-design [data-f]{cursor:default}
body.rb-design [data-f]:hover,body.rb-design [data-f]:focus{background:none;box-shadow:none}
.rb-hov{outline:1px dashed rgba(6,182,212,.95)!important;outline-offset:1px}
#rb-selbox{position:absolute;z-index:1500;border:1.5px solid #06b6d4;pointer-events:none;box-shadow:0 0 0 1px rgba(255,255,255,.7);display:none}
#rb-selbox .rb-h{position:absolute;width:10px;height:10px;background:#fff;border:1.5px solid #0891b2;border-radius:2px;pointer-events:auto}
#rb-selbox .rb-h[data-h=se]{right:-6px;bottom:-6px;cursor:nwse-resize}
#rb-selbox .rb-h[data-h=e]{right:-6px;top:calc(50% - 5px);cursor:ew-resize}
#rb-selbox .rb-h[data-h=s]{bottom:-6px;left:calc(50% - 5px);cursor:ns-resize}
#rb-selbox .rb-h[data-h=rot]{top:-28px;left:calc(50% - 6px);width:12px;height:12px;border-radius:50%;cursor:grab}
#rb-selbox .rb-h[data-h=move]{left:-7px;top:-7px;width:12px;height:12px;cursor:move;background:#0891b2;border-color:#fff}
#rb-selbox .rb-tag{position:absolute;left:10px;top:-21px;background:#0891b2;color:#fff;font:10px 'Segoe UI',Arial;padding:1px 6px;border-radius:3px;white-space:nowrap}
.rb-pt{position:absolute;z-index:1501;width:12px;height:12px;margin:-6px 0 0 -6px;border-radius:50%;background:#fff;border:2px solid #0891b2;cursor:move;display:none}
.rb-pt.mid{background:#fde68a;border-color:#d97706}
body:not(.rb-design) #rb-free .rbs{pointer-events:none}
body.rb-design #rb-free .rbs:not(.rbs-line){pointer-events:auto;cursor:move}
body.rb-design #rb-free .rbs-line path{pointer-events:stroke;cursor:move}
body.rb-design #rb-free .rbs-txt[contenteditable=true]{cursor:text;user-select:text;-webkit-user-select:text;outline:2px solid #06b6d4}
@media print{#rb-bar,#rb-ctl,#rb-sctl,#rb-hint,#rb-panel,#rb-selbox,.rb-pt,.edit-only{display:none!important}}
</style>
"""

# The page always starts below the toolbar, whatever height the toolbar wraps to (narrow windows).
_EDITOR_FIT_JS = r"""<script>(function(){function fit(){const bar=document.getElementById('rb-bar');if(!bar)return;
const h=bar.getBoundingClientRect().height;document.body.style.setProperty('margin-top',(h+18)+'px','important');}
fit();window.addEventListener('resize',fit);setTimeout(fit,400);})();</script>"""

_EDITOR_JS = r"""
<script>
(function(){
  const RB = window.__RB__, F = window.RBF, FD = F.D, MM = F.MM;
  ['styles', 'groups', 'vars', 'fonts'].forEach(k => { if (!FD[k] || typeof FD[k] !== 'object' || Array.isArray(FD[k])) FD[k] = {}; });
  if (!Array.isArray(FD.shapes)) FD.shapes = [];
  let dirty = false, hot = null, mode = 'text', sel = null, scope = 'one', tab = 'sel', drag = null, editingShape = false;
  let rev = RB.rev || '', busy = false;
  const hist = [], fut = [], srcOf = {}, typing = {el: null, t: 0};
  const $ = s => document.querySelector(s);
  const status = (h) => { $('#rb-status').innerHTML = h; };
  const ss = {get(k){ try { return sessionStorage.getItem(k); } catch(e) { return null; } },
              set(k, v){ try { sessionStorage.setItem(k, v); } catch(e) {} },
              del(k){ try { sessionStorage.removeItem(k); } catch(e) {} }};
  const orig = new Map();
  document.querySelectorAll('[data-f]').forEach(el => orig.set(el, el.textContent));

  // ── text content ────────────────────────────────────────────────────────────────────────────
  function collect(){
    const c = JSON.parse(JSON.stringify(RB.content));
    document.querySelectorAll('[data-f]').forEach(el => {
      if (el.dataset.f.indexOf('section_titles.') === 0 && el.textContent === orig.get(el)) return;   // untouched heading
      const path = el.dataset.f.split('.');
      let o = c;
      for (let i = 0; i < path.length - 1; i++) {
        const k = /^\d+$/.test(path[i]) ? +path[i] : path[i];
        if (o[k] === undefined || o[k] === null) return;
        o = o[k];
      }
      const last = path[path.length - 1];
      o[/^\d+$/.test(last) ? +last : last] = el.textContent.replace(/\s+/g, ' ').trim();
    });
    return c;
  }
  function freeOut(){
    return {styles: FD.styles, groups: FD.groups, vars: FD.vars, fonts: FD.fonts, text_scale: FD.text_scale || 1,
            shapes: FD.shapes.map(s => { const t = Object.assign({}, s); delete t.src; return t; })};
  }
  function keepView(){
    ss.set('rbScroll', String(window.scrollY)); ss.set('rbMode', mode); ss.set('rbTab', tab);
    ss.set('rbPan', document.documentElement.classList.contains('rb-pan') ? '1' : '');
    if (sel) ss.set('rbSel', JSON.stringify({kind: sel.kind, key: sel.key, id: sel.id}));
    persistHist();
  }
  async function send(extra, reload){
    status('⏳ Working…');
    try {
      const r = await fetch('/resume/save', {method:'POST', headers:{'Content-Type':'application/json'},
                                             body: JSON.stringify(Object.assign({content: collect(), free: freeOut()}, extra))});
      const j = await r.json();
      if (!j.ok) { status('⚠️ ' + (j.message || 'Failed')); return j; }
      dirty = false;
      if (j.rev) rev = j.rev;
      if (j.snap && !extra.restore_snap) { hist.push({srv: j.snap}); fut.length = 0; }   // one Ctrl+Z step
      if (reload) { keepView(); location.reload(); return j; }
      status(j.message_html || j.message || 'Saved');
      return j;
    } catch (e) { status('⚠️ ' + e); }
  }
  let saveT = null;
  function saveFree(){
    clearTimeout(saveT);
    status('✏️ Design changed…');
    saveT = setTimeout(() => send({}, false).then(j => {
      if (j && j.ok) status('✅ Design saved — press <b>Save &amp; export PDF</b> to update the PDF');
    }), 700);
  }

  document.querySelectorAll('[data-f]').forEach(el => {
    el.addEventListener('beforeinput', e => {
      if (e.inputType === 'historyUndo' || e.inputType === 'historyRedo') { e.preventDefault(); e.inputType === 'historyUndo' ? undo() : redo(); return; }
      const now = Date.now();
      if (el !== typing.el || now - typing.t > 1200) snap();
      typing.el = el; typing.t = now;
    });
    el.addEventListener('focusout', () => { typing.el = null; });
    el.addEventListener('input', () => { dirty = true; status('✏️ Unsaved changes — press <b>Save &amp; export PDF</b> (Ctrl+S)'); });
    el.addEventListener('keydown', e => { if (e.key === 'Enter') { e.preventDefault(); el.blur(); } });
    el.addEventListener('paste', e => { e.preventDefault(); document.execCommand('insertText', false, (e.clipboardData || window.clipboardData).getData('text/plain')); });
  });

  // positions relative to <body> (it is position:relative, so absolute children use its box)
  function brect(el){ const r = el.getBoundingClientRect(), b = document.body.getBoundingClientRect();
                      return {x: r.left - b.left, y: r.top - b.top, w: r.width, h: r.height}; }
  function pmm(e){ const b = document.body.getBoundingClientRect(); return {x: (e.clientX - b.left) / MM, y: (e.clientY - b.top) / MM}; }
  const editorUi = t => t && t.closest && t.closest('#rb-bar,#rb-panel,#rb-hint,#rb-ctl,#rb-sctl,#rb-selbox,.rb-pt');

  // text mode: hover controls for list items (add after / move up / delete) and whole sections
  const ctl = $('#rb-ctl'), sctl = $('#rb-sctl');
  let hotSec = null;
  document.addEventListener('mouseover', e => {
    if (mode !== 'text' || ctl.contains(e.target) || sctl.contains(e.target)) return;
    const sec = e.target.closest('section.sec');
    if (sec) {
      hotSec = sec;
      const r = brect(sec);
      sctl.style.display = 'flex';
      sctl.style.top = r.y + 'px';
      sctl.style.left = (r.x - 34) + 'px';
    }
    const it = e.target.closest('[data-item]');
    if (!it) return;
    if (hot) hot.classList.remove('rb-hot');
    hot = it; it.classList.add('rb-hot');
    const r = brect(it);
    ctl.style.display = 'flex';
    ctl.style.top = (r.y - 26) + 'px';
    ctl.style.left = (r.x + r.w - ctl.offsetWidth) + 'px';
  });
  ctl.addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b || !hot) return;
    send({op: {action: b.dataset.a, path: hot.dataset.item}}, true);
  });
  sctl.addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b || !hotSec) return;
    const m = hotSec.className.match(/\bsec-(\w+)/);
    if (m) send({sec_op: {action: b.dataset.a, key: m[1]}}, true);
  });

  // ── toolbar ─────────────────────────────────────────────────────────────────────────────────
  $('#rb-save').onclick = async () => { const j = await send({export: true}, false);
    if (j && j.reload) { keepView(); setTimeout(() => location.reload(), 1500); } };
  $('#rb-pages').onchange = e => send({target_pages: e.target.value}, false);
  $('#rb-tpl').onchange = e => { if (e.target.value) send({template: e.target.value}, true); };
  $('#rb-color').onchange = e => {
    ['--primary', '--on-primary', '--accent', '--heading', '--side', '--tint', '--track'].forEach(v => delete FD.vars[v]);
    send({color: e.target.value}, true);
  };
  $('#rb-add').onchange = e => {
    const v = e.target.value;
    if (!v) return;
    if (v === '__custom') {
      const t = prompt('Title of the new section (e.g. Volunteering, Publications, Hobbies):', '');
      e.target.value = '';
      if (t && t.trim()) send({add_custom: {title: t.trim(), style: 'bullets', column: 'main'}}, true);
      return;
    }
    send({add_section: v}, true);
  };
  $('#rb-nophoto').onclick = () => send({remove_photo: true}, true);
  async function upload(f){
    const fd = new FormData(); fd.append('file', f);
    const j = await (await fetch('/upload', {method:'POST', body: fd})).json();
    return j.status === 'success' ? j.path : null;
  }
  $('#rb-photo').onchange = async e => {
    const f = e.target.files[0]; if (!f) return;
    status('⏳ Uploading photo…');
    const p = await upload(f);
    if (!p) { status('⚠️ Upload failed'); return; }
    send({photo: p}, true);
  };
  const ai = () => { const v = $('#rb-ai').value.trim(); if (v) send({instruction: v}, true); };
  $('#rb-ai-go').onclick = ai;
  $('#rb-ai').addEventListener('keydown', e => { if (e.key === 'Enter') ai(); });
  window.addEventListener('beforeunload', e => { if (dirty) { e.preventDefault(); e.returnValue = ''; } });

  // ── undo / redo: one history for typing, design changes and structural changes ──────────────
  // A local step is a snapshot of every text field + the free design; a structural step ({srv: id}) is a
  // whole-state snapshot kept by the server (item / section ops, template, colour, photo, AI edit, page fit).
  const fdOf = () => ({styles: FD.styles, groups: FD.groups, vars: FD.vars, fonts: FD.fonts, text_scale: FD.text_scale || 1, shapes: FD.shapes});
  const texts = () => Array.from(document.querySelectorAll('[data-f]'), el => [el.dataset.f, el.textContent]);
  const snapshot = () => JSON.stringify({t: texts(), f: fdOf()});
  function snap(){ hist.push(snapshot()); if (hist.length > 80) hist.shift(); fut.length = 0; }
  function setTexts(t){
    const els = Array.from(document.querySelectorAll('[data-f]'));
    const same = els.length === t.length && els.every((el, i) => el.dataset.f === t[i][0]);
    const byKey = same ? null : new Map(t);
    let changed = false;
    els.forEach((el, i) => {
      const v = same ? t[i][1] : byKey.get(el.dataset.f);
      if (v == null || el.textContent === v) return;
      el.textContent = v; changed = true;
    });
    if (!changed) return;
    dirty = true;
    const a = document.activeElement;
    if (a && a.closest && a.closest('[data-f]')) {           // keep the caret in the field being typed in
      const r = document.createRange(); r.selectNodeContents(a); r.collapse(false);
      const g = document.getSelection(); g.removeAllRanges(); g.addRange(r);
    }
    if (window.__rbLayout) window.__rbLayout();
  }
  function restore(js){
    const o = JSON.parse(js), f = o.f || o;
    (f.shapes || []).forEach(x => { if (x.type === 'image' && !x.src && x.path && srcOf[x.path]) x.src = srcOf[x.path]; });
    const fdChanged = JSON.stringify(f) !== JSON.stringify(fdOf());
    Object.assign(FD, f);
    document.documentElement.style.setProperty('--s', String(FD.text_scale || 1));
    F.refresh();
    if (o.t) setTexts(o.t);
    if (sel && sel.kind === 'shape' && !shapeById(sel.id)) sel = null;
    if (sel && sel.kind === 'el') sel.el = F.find(sel.key) || sel.el;
    updateSel(); renderPanel();
    if (fdChanged) saveFree();
    else if (dirty) status('✏️ Unsaved changes — press <b>Save &amp; export PDF</b> (Ctrl+S)');
  }
  async function step(from, to, undoing){
    if (busy) return;
    if (drag) return;
    const h = from.pop();
    typing.el = null;
    if (h === undefined) return status(undoing ? 'Nothing to undo' : 'Nothing to redo');
    if (typeof h === 'string') { to.push(snapshot()); restore(h); return; }
    busy = true;
    status(undoing ? '⏳ Undoing…' : '⏳ Redoing…');
    const j = await send({restore_snap: h.srv}, false);
    busy = false;
    if (j && j.ok && j.snap) { to.push({srv: j.snap}); keepView(); location.reload(); }
  }
  function undo(){ return step(hist, fut, true); }
  function redo(){ return step(fut, hist, false); }
  function persistHist(){
    const strip = h => {
      if (typeof h !== 'string') return h;
      const o = JSON.parse(h);
      ((o.f || {}).shapes || []).forEach(x => { if (x.src && x.path) srcOf[x.path] = x.src; delete x.src; });
      return JSON.stringify(o);
    };
    try { ss.set('rbHist', JSON.stringify({rev: rev, hist: hist.slice(-60).map(strip), fut: fut.slice(-60).map(strip)})); } catch (e) {}
  }
  try {                                                       // the history survives the editor's own reloads
    const o = JSON.parse(ss.get('rbHist') || 'null');
    ss.del('rbHist');
    if (o && o.rev && o.rev === RB.rev) { hist.push(...(o.hist || [])); fut.push(...(o.fut || [])); }
  } catch (e) {}
  FD.shapes.forEach(x => { if (x.src && x.path) srcOf[x.path] = x.src; });
  window.addEventListener('pagehide', persistHist);
  $('#rb-undo').onclick = undo;
  $('#rb-redo').onclick = redo;

  // ── modes & panel ───────────────────────────────────────────────────────────────────────────
  const panel = $('#rb-panel'), selbox = $('#rb-selbox');
  function layoutChrome(){
    const h = $('#rb-bar').offsetHeight;
    document.body.style.setProperty('margin-top', (h + 18) + 'px', 'important');
    panel.style.top = h + 'px';
  }
  function setPanel(open){
    document.documentElement.classList.toggle('rb-pan', open);
    $('#rb-panel-btn').classList.toggle('on', open);
    if (open) renderPanel();
    setTimeout(updateSel, 0);
  }
  function setMode(m){
    mode = m;
    document.body.classList.toggle('rb-design', m === 'design');
    $('#rb-mode-text').classList.toggle('on', m === 'text');
    $('#rb-mode-design').classList.toggle('on', m === 'design');
    document.querySelectorAll('[data-f]').forEach(el => el.setAttribute('contenteditable', m === 'text' ? 'true' : 'false'));
    ctl.style.display = 'none'; sctl.style.display = 'none';
    if (hot) hot.classList.remove('rb-hot');
    if (m === 'text') select(null);
    else setPanel(true);
    $('#rb-hint').innerHTML = m === 'text'
      ? 'Click text to type · hover an item for ＋ ⧉ ↑ ✕ · hover a section for ↑ ↓ ⇄ ✕ · Ctrl+Z undo · Ctrl+D duplicates the item · red line = page break · Ctrl+S saves'
      : 'Click anything to select · drag to move · handles resize / rotate · Del hides · arrows nudge · Ctrl+Z undo · Ctrl+D duplicate · double-click text to edit';
  }
  $('#rb-mode-text').onclick = () => setMode('text');
  $('#rb-mode-design').onclick = () => setMode('design');
  $('#rb-panel-btn').onclick = () => setPanel(!document.documentElement.classList.contains('rb-pan'));

  // ── selection ───────────────────────────────────────────────────────────────────────────────
  const shapeById = id => FD.shapes.find(s => s.id === id);
  const curShape = () => sel && sel.kind === 'shape' ? shapeById(sel.id) : null;
  const shapeEl = id => document.querySelector('#rb-free .rbs[data-sid="' + id + '"]');
  function select(target, keepTab){
    if (!target) sel = null;
    else if (target.kind === 'shape') sel = {kind: 'shape', id: target.id};
    else {
      const key = F.keyOf(target);
      sel = key ? {kind: 'el', el: target, key: key} : null;
    }
    scope = 'one';
    updateSel();
    if (tab !== 'sel' && sel && !keepTab) tab = 'sel';
    renderPanel();
  }
  const pts = {p1: $('#rb-pt-p1'), p2: $('#rb-pt-p2'), mid: $('#rb-pt-mid')};
  function updateSel(){
    Object.values(pts).forEach(p => p.style.display = 'none');
    if (!sel) { selbox.style.display = 'none'; return; }
    let el = sel.kind === 'shape' ? shapeEl(sel.id) : sel.el;
    if (sel.kind === 'el' && (!el || !el.isConnected)) { el = sel.el = F.find(sel.key); }
    if (!el) { selbox.style.display = 'none'; return; }
    const s = curShape();
    if (s && s.type === 'line') {
      selbox.style.display = 'none';
      const mx = s.mx == null ? (s.x1 + s.x2) / 2 : s.mx, my = s.my == null ? (s.y1 + s.y2) / 2 : s.my;
      [['p1', s.x1, s.y1], ['p2', s.x2, s.y2], ['mid', mx, my]].forEach(([k, x, y]) => {
        Object.assign(pts[k].style, {display: 'block', left: (x * MM) + 'px', top: (y * MM) + 'px'});
      });
      return;
    }
    const r = brect(el);
    Object.assign(selbox.style, {display: 'block', left: (r.x - 2) + 'px', top: (r.y - 2) + 'px', width: (r.w + 4) + 'px', height: (r.h + 4) + 'px'});
    selbox.querySelector('.rb-tag').textContent = s ? s.type : friendly(sel.key);
  }
  function friendly(k){
    return String(k).replace(/^l:/, '').replace(/^s:(\w+)/, '$1 section').replace(/^[fi]:/, '').replace(/section_titles\.(\w+)/, '$1 heading')
      .replace(/\.(\d+)/g, (m, n) => ' #' + (+n + 1)).replace(/\//g, ' › ').replace(/:\d+/g, '').replace(/\./g, ' ');
  }
  window.addEventListener('resize', () => { layoutChrome(); updateSel(); });

  function newId(){ return 's' + Date.now().toString(36) + Math.random().toString(36).slice(2, 5); }
  function cssColor(v, fb){
    const c = document.createElement('canvas').getContext('2d');
    c.fillStyle = fb || '#000000';
    try { c.fillStyle = String(v || '').trim() || fb || '#000000'; } catch (e) {}
    const out = c.fillStyle;
    if (out[0] === '#') return out;
    const m = out.match(/[\d.]+/g);
    if (!m) return fb || '#000000';
    if (m.length > 3 && +m[3] === 0) return fb || '#ffffff';
    return '#' + m.slice(0, 3).map(x => (Math.round(+x)).toString(16).padStart(2, '0')).join('');
  }
  const rootVar = v => getComputedStyle(document.documentElement).getPropertyValue(v).trim();

  // ── element style buckets ─────────────────────────────────────────────────────────────────
  const NOCLS = /^(rb|sec-|pos-|acc-|al-|ph-|lay-)/;
  function groupSel(el){
    const f = el.getAttribute('data-f');
    if (f !== null) {
      if (/^section_titles\.|^custom_sections\.\d+\.title$/.test(f)) return '[data-f^="section_titles."],[data-f^="custom_sections."][data-f$=".title"]';
      const segs = f.split('.'), words = segs.filter(s => !/^\d+$/.test(s));
      if (words.length === 1 && segs.length === 1) return '[data-f="' + f + '"]';
      let q = '[data-f^="' + words[0] + '."]';
      const lastNum = /^\d+$/.test(segs[segs.length - 1]);
      for (let i = 1; i < words.length; i++)
        q += (i === words.length - 1 && !lastNum) ? '[data-f$=".' + words[i] + '"]' : '[data-f*=".' + words[i] + '."]';
      return q;
    }
    const pick = e => Array.from(e.classList).filter(c => !NOCLS.test(c) && c !== 'up').map(c => '.' + CSS.escape(c)).join('');
    const tag = el.tagName.toLowerCase(), own = pick(el);
    if (own) return tag + own;
    const p = el.parentElement;
    if (!p || p === document.body) return tag;
    return p.tagName.toLowerCase() + pick(p) + ' > ' + tag;
  }
  function bucket(own){
    if (!sel || sel.kind !== 'el') return null;
    if (scope === 'all' && !own) { const g = groupSel(sel.el); return FD.groups[g] = FD.groups[g] || {}; }
    return FD.styles[sel.key] = FD.styles[sel.key] || {};
  }
  function getProp(p, own){
    if (!sel || sel.kind !== 'el') return undefined;
    const b = (scope === 'all' && !own) ? FD.groups[groupSel(sel.el)] : FD.styles[sel.key];
    return b ? b[p] : undefined;
  }
  function tidy(){ for (const m of [FD.styles, FD.groups]) for (const k in m) if (!Object.keys(m[k]).length) delete m[k]; }
  function setProp(p, v, own){
    const b = bucket(own); if (!b) return;
    if (v === '' || v == null) delete b[p]; else b[p] = v;
    tidy(); F.buildCss(); F.applyStyles(); updateSel();
  }
  function trOf(){ const m = String(getProp('translate', true) || '').match(/(-?[\d.]+)mm\s+(-?[\d.]+)mm/); return m ? [+m[1], +m[2]] : [0, 0]; }
  function setTr(x, y){ setProp('translate', (Math.abs(x) > 0.01 || Math.abs(y) > 0.01) ? x.toFixed(2) + 'mm ' + y.toFixed(2) + 'mm' : '', true); }

  // ── insert shapes ───────────────────────────────────────────────────────────────────────────
  function viewCenter(){
    const b = document.body.getBoundingClientRect();
    const x = (Math.min(window.innerWidth - (document.documentElement.classList.contains('rb-pan') ? 322 : 0), b.right) + Math.max(0, b.left)) / 2;
    return {x: Math.max(20, Math.min(190, (x - b.left) / MM)), y: Math.max(15, (window.innerHeight / 2 - b.top) / MM)};
  }
  function addShape(kind, extra, edit){
    const c = viewCenter(), pri = cssColor(rootVar('--primary'), '#1f3a68'), txt = cssColor(rootVar('--text'), '#111827');
    let s;
    if (kind === 'line' || kind === 'bend' || kind === 'arrow') {
      s = {type: 'line', x1: c.x - 30, y1: c.y, x2: c.x + 30, y2: c.y, stroke: pri, sw: 1.5};
      if (kind === 'bend') { s.mx = c.x; s.my = c.y - 14; }
      if (kind === 'arrow') s.arrow = 'end';
    } else if (kind === 'text') {
      s = {type: 'text', x: c.x - 30, y: c.y - 5, w: 60, text: 'Your text', size: 11, color: txt};
    } else if (kind === 'wave' || kind === 'curve') {
      s = {type: kind, x: 0, y: c.y - 15, w: 210, h: 30, fill: pri};
    } else if (kind === 'icon') {
      s = {type: 'icon', x: c.x - 5, y: c.y - 5, w: 10, h: 10, icon: 'star', color: pri};
    } else if (kind === 'image') {
      s = {type: 'image', x: c.x - 18, y: c.y - 18, w: 36, h: 36, shape: 'circle'};
    } else {
      const sq = {ellipse: 1, triangle: 1, diamond: 1, hexagon: 1, pentagon: 1, star: 1}[kind];
      s = {type: kind === 'rounded' ? 'rect' : kind, x: c.x - (sq ? 13 : 25), y: c.y - 13, w: sq ? 26 : 50, h: 26,
           fill: cssColor(rootVar('--tint'), '#e0f2fe'), stroke: pri, sw: kind === 'rect' || kind === 'rounded' ? 1 : 0};
      if (kind === 'rounded') s.radius = 4;
      if (sq && kind !== 'ellipse') { s.fill = pri; s.sw = 0; }
    }
    if (extra) {
      Object.assign(s, extra);
      if (extra.x == null && s.type !== 'line' && s.w) s.x = Math.max(0, c.x - s.w / 2);
    }
    s.id = newId();
    if (s.src && s.path) srcOf[s.path] = s.src;
    snap();
    FD.shapes.push(s);
    F.buildCss(); F.renderShapes();
    if (mode !== 'design') setMode('design');
    select({kind: 'shape', id: s.id});
    saveFree();
    if (edit && s.type === 'text') editShapeText(s.id);
    return s;
  }
  // the exact look of a piece of resume text (family, size, weight, colour, leading, tracking, case)
  function textStyle(el){
    const cs = getComputedStyle(el), fs = parseFloat(cs.fontSize) || 14.67, wt = parseInt(cs.fontWeight, 10) || 400;
    const lh = cs.lineHeight === 'normal' ? 1.2 : (parseFloat(cs.lineHeight) || fs * 1.2) / fs;
    const al = {start: 'left', end: 'right', left: 'left', right: 'right', center: 'center', justify: 'justify'}[cs.textAlign] || 'left';
    return {ff: cs.fontFamily, size: Math.round(fs * 7500) / 10000, color: cssColor(cs.color, '#111827'), weight: wt, bold: wt >= 600,
            italic: cs.fontStyle === 'italic', upper: cs.textTransform === 'uppercase', align: al, pad: 0,
            lh: Math.round(lh * 10000) / 10000, ls: cs.letterSpacing === 'normal' ? 0 : Math.round(parseFloat(cs.letterSpacing) * 10000) / 10000};
  }
  // the resume's body text = the style that carries the most characters (headings and the name excluded)
  function bodyText(){
    const votes = new Map();
    document.querySelectorAll('[data-f]').forEach(el => {
      const f = el.dataset.f, n = el.textContent.trim().length;
      if (!n || el.closest('#rb-free') || /^(section_titles\.|name$|title$)/.test(f) || /^custom_sections\.\d+\.title$/.test(f)) return;
      const cs = getComputedStyle(el);
      if (cs.display === 'none' || cs.visibility === 'hidden') return;
      const key = [cs.fontFamily, cs.fontSize, cs.fontWeight, cs.fontStyle, cs.color, cs.textTransform, cs.letterSpacing].join('|');
      const v = votes.get(key) || {n: 0, el: el};
      v.n += n; votes.set(key, v);
    });
    let best = null;
    votes.forEach(v => { if (!best || v.n > best.n) best = v; });
    return best ? best.el : null;
  }
  function addTextBox(){
    const el = bodyText(), st = el ? textStyle(el) : {};
    let w = 60;
    if (el) {
      const box = el.closest('[data-item]') || el.parentElement;
      const bw = box ? brect(box).w / MM : 0;
      if (bw > 20) w = Math.round(Math.min(bw, 120) * 10) / 10;
    }
    addShape('text', Object.assign(st, {text: 'Your text', w: w}), true);
  }
  // Ctrl+D: a shape → its copy; a resume item (bullet, entry, skill…) → a real duplicate item in the content;
  // any other text / the photo / a coloured box → an identical free copy placed 4 mm lower-right
  function duplicate(field){
    if (mode === 'design' && curShape()) { dupShape(); return; }
    const el = field || (mode === 'design' && sel && sel.kind === 'el' ? sel.el : null) || (mode === 'text' ? hot : null);
    if (!el || !el.isConnected) return status('Select something first (🎨 Design: click it · ✍️ Text: click into an item), then Ctrl+D');
    const it = el.closest('[data-item]');
    if (it) { status('⏳ Duplicating…'); send({op: {action: 'dup', path: it.dataset.item}}, true); return; }
    copyAsShape(el);
  }
  function copyAsShape(el){
    if (el.querySelector('[data-item],section') || el.matches('section,main,aside,header,body,html'))
      return status('That holds whole sections — select one item, text line, the photo or a shape to duplicate');
    const r = brect(el), cs = getComputedStyle(el), x = r.x / MM + 4, y = r.y / MM + 4, w = r.w / MM, h = r.h / MM;
    const photo = el.closest('.hd-avatar,.hd-photo') || (sel && sel.kind === 'el' && sel.key === 'l:photo' ? el : null);
    if (photo && RB.photo) {
      const img = photo.tagName === 'IMG' ? photo : photo.querySelector('img');
      const bgm = getComputedStyle(photo).backgroundImage.match(/url\(["']?(.*?)["']?\)/);
      const src = img ? img.src : bgm ? bgm[1] : '';
      const pr = brect(photo), round = parseFloat(getComputedStyle(photo).borderTopLeftRadius) >= Math.min(pr.w, pr.h) * 0.4;
      if (src) { addShape('image', {path: RB.photo, src: src, x: pr.x / MM + 4, y: pr.y / MM + 4, w: pr.w / MM, h: pr.h / MM, shape: round ? 'circle' : 'square'}); return; }
    }
    const txt = (el.innerText || '').trim();
    if (txt && txt.length <= 800) {
      const s = addShape('text', Object.assign(textStyle(el), {text: txt, x: x, y: y, w: Math.round((w + 0.6) * 100) / 100}));
      // line boxes differ (inline run vs block): measure both texts and put the copy's glyphs exactly 4 mm off
      const inner = shapeEl(s.id) && shapeEl(s.id).querySelector('.rbs-txt');
      const g = n => { const rg = document.createRange(); rg.selectNodeContents(n); return rg.getBoundingClientRect(); };
      if (inner) {
        const a = g(el), c = g(inner);
        s.x = Math.round((x + (a.left - c.left) / MM + 4) * 100) / 100;
        s.y = Math.round((y + (a.top - c.top) / MM + 4) * 100) / 100;
        F.renderShapes(); updateSel(); renderPanel();
      }
      return;
    }
    const bg = cs.backgroundColor, hasBg = bg && bg !== 'transparent' && !/rgba\([^)]*,\s*0\)$/.test(bg), bw = parseFloat(cs.borderTopWidth) || 0;
    if (hasBg || bw > 0) {
      addShape('rect', {x: x, y: y, w: w, h: h, fill: hasBg ? cssColor(bg) : 'none', stroke: bw ? cssColor(cs.borderTopColor) : 'none',
                        sw: Math.round(bw * 75) / 100, radius: Math.round((parseFloat(cs.borderTopLeftRadius) || 0) / MM * 100) / 100});
      return;
    }
    status('Nothing to copy here — select a text line, an item, the photo or a shape, then Ctrl+D');
  }
  $('#rb-insert').onchange = e => {
    const v = e.target.value; e.target.value = '';
    if (v === 'image') $('#rb-img-file').click();
    else if (v === 'text') addTextBox();
    else if (v) addShape(v);
  };
  $('#rb-addtext').onclick = addTextBox;
  async function imageFile(f, replace){
    status('⏳ Uploading image…');
    const p = await upload(f);
    if (!p) return status('⚠️ Upload failed');
    const src = await new Promise(res => { const r = new FileReader(); r.onload = () => res(r.result); r.readAsDataURL(f); });
    if (replace) { snap(); Object.assign(replace, {path: p, src: src}); F.renderShapes(); updateSel(); saveFree(); }
    else addShape('image', {path: p, src: src});
  }
  $('#rb-img-file').onchange = e => { const f = e.target.files[0]; e.target.value = ''; if (f) imageFile(f, null); };
  $('#rb-img-repl').onchange = e => { const f = e.target.files[0]; e.target.value = ''; const s = curShape(); if (f && s) imageFile(f, s); };

  // ── pointer: select, move, resize, rotate, bend ────────────────────────────────────────────
  document.addEventListener('click', e => {
    if (mode === 'design' && !editorUi(e.target) && !editingShape) { e.preventDefault(); }
  }, true);
  document.addEventListener('pointerdown', e => {
    if (mode !== 'design' || e.button !== 0 || editingShape && e.target.closest('[contenteditable=true]')) return;
    const h = e.target.closest('.rb-h, .rb-pt');
    if (h) { startDrag(e, h.dataset.h); return; }
    if (editorUi(e.target)) return;
    const sh = e.target.closest('#rb-free .rbs');
    if (sh) { select({kind: 'shape', id: sh.dataset.sid}); startDrag(e, 'move'); return; }
    let el = e.target;
    if (el === document.documentElement) { select(null); return; }
    if (el.closest && el.closest('svg') && el.tagName.toLowerCase() !== 'svg') el = el.closest('svg');
    if (!sel || sel.kind !== 'el' || sel.el !== el) select(el);
    if (sel) startDrag(e, 'move');
  });
  function startDrag(e, how){
    if (!sel) return;
    const d = {how: how, sx: e.clientX, sy: e.clientY, moved: false, shift: e.shiftKey};
    const s = curShape();
    if (s) { d.s0 = Object.assign({}, s); delete d.s0.src; }
    else {
      d.t0 = trOf();
      const r = sel.el.getBoundingClientRect();
      d.w0 = r.width / MM; d.h0 = r.height / MM;
      d.photo = sel.key === 'l:photo';
    }
    const el = s ? shapeEl(s.id) : sel.el;
    if (el) { const r = el.getBoundingClientRect(); d.cx = r.left + r.width / 2; d.cy = r.top + r.height / 2; }
    drag = d;
    e.preventDefault();
  }
  let hov = null;
  window.addEventListener('pointermove', e => {
    if (!drag) {
      if (mode !== 'design') return;
      const t = editorUi(e.target) ? null : (e.target.closest('#rb-free .rbs') || e.target);
      if (hov && hov !== t) hov.classList.remove('rb-hov');
      hov = (t && t !== document.documentElement && t !== document.body && t.classList) ? t : null;
      if (hov) hov.classList.add('rb-hov');
      return;
    }
    if (!drag.moved) {
      if (Math.abs(e.clientX - drag.sx) + Math.abs(e.clientY - drag.sy) < 3) return;
      drag.moved = true; snap();
    }
    const dx = (e.clientX - drag.sx) / MM, dy = (e.clientY - drag.sy) / MM, d = drag, s = curShape();
    const ang = () => { let a = Math.atan2(e.clientY - d.cy, e.clientX - d.cx) * 180 / Math.PI + 90;
                        if (e.shiftKey) a = Math.round(a / 15) * 15; return Math.round(((a + 540) % 360 - 180) * 10) / 10; };
    if (s) {
      const o = d.s0;
      if (d.how === 'move') {
        if (s.type === 'line') {
          Object.assign(s, {x1: o.x1 + dx, y1: o.y1 + dy, x2: o.x2 + dx, y2: o.y2 + dy});
          if (o.mx != null) { s.mx = o.mx + dx; s.my = o.my + dy; }
        } else { s.x = o.x + dx; s.y = o.y + dy; }
      } else if (d.how === 'p1' || d.how === 'p2') {
        const n = d.how === 'p1' ? '1' : '2';
        s['x' + n] = o['x' + n] + dx; s['y' + n] = o['y' + n] + dy;
        if (e.shiftKey) {               // snap to horizontal / vertical
          const m = n === '1' ? '2' : '1';
          if (Math.abs(s['x' + n] - s['x' + m]) < Math.abs(s['y' + n] - s['y' + m])) s['x' + n] = s['x' + m]; else s['y' + n] = s['y' + m];
        }
        if (o.mx != null) { s.mx = o.mx + dx / 2; s.my = o.my + dy / 2; }
      } else if (d.how === 'mid') {
        s.mx = (o.mx == null ? (o.x1 + o.x2) / 2 : o.mx) + dx;
        s.my = (o.my == null ? (o.y1 + o.y2) / 2 : o.my) + dy;
      } else if (d.how === 'rot') {
        s.rot = ang();
      } else {
        let w = o.w || 30, h = o.h || 20;
        if (d.how !== 's') w = Math.max(2, (o.w || 30) + dx);
        if (d.how !== 'e') h = Math.max(2, (o.h || 20) + dy);
        if (e.shiftKey && d.how === 'se') h = w * (o.h || 20) / (o.w || 30);
        s.w = w; if (s.type !== 'text') s.h = h;
      }
      F.renderShapes();
    } else {
      if (d.how === 'move') setTr(d.t0[0] + dx, d.t0[1] + dy);
      else if (d.how === 'rot') setProp('rotate', ang() ? ang() + 'deg' : '', true);
      else {
        let w = d.w0, h = d.h0;
        if (d.how !== 's') w = Math.max(2, d.w0 + dx);
        if (d.how !== 'e') h = Math.max(2, d.h0 + dy);
        if ((d.photo !== e.shiftKey) && d.how === 'se') h = w * d.h0 / d.w0;     // photo keeps its ratio (Shift frees it)
        const b = bucket(true);
        if (d.how !== 's') b.width = w.toFixed(2) + 'mm';
        if (d.how !== 'e') b.height = h.toFixed(2) + 'mm';
        if (d.photo && d.how === 'se') b['max-width'] = 'none';
        F.applyStyles();
      }
    }
    updateSel();
  });
  window.addEventListener('pointerup', () => {
    if (drag && drag.moved) { saveFree(); renderPanel(); }
    drag = null;
  });

  // double-click: edit a text box, or jump to typing in resume text
  document.addEventListener('dblclick', e => {
    if (mode !== 'design' || editorUi(e.target)) return;
    const sh = e.target.closest('#rb-free .rbs-text');
    if (sh) { editShapeText(sh.dataset.sid); return; }
    const f = e.target.closest('[data-f]');
    if (f) { setMode('text'); f.focus(); }
  });

  function editShapeText(sid){
    const s = shapeById(sid), sh = shapeEl(sid), inner = sh && sh.querySelector('.rbs-txt');
    if (!s || !inner) return;
    const before = snapshot();
    editingShape = true;
    inner.setAttribute('contenteditable', 'true');
    inner.focus();
    document.getSelection().selectAllChildren(inner);
    inner.addEventListener('blur', () => {
      editingShape = false;
      const t = inner.innerText.replace(/\n$/, '');
      if (t !== s.text) { hist.push(before); fut.length = 0; s.text = t; }
      F.renderShapes(); updateSel(); renderPanel(); saveFree();
    }, {once: true});
  }

  // keyboard
  document.addEventListener('keydown', e => {
    const k = e.key.toLowerCase(), ctrl = e.ctrlKey || e.metaKey;
    if (ctrl && k === 's') { e.preventDefault(); send({export: true}, false); return; }
    const t = e.target, field = t && t.closest ? t.closest('[data-f]') : null;
    const ui = t && (t.isContentEditable || /^(INPUT|SELECT|TEXTAREA)$/.test(t.tagName));
    if (ctrl && !e.altKey && (field || !ui)) {               // resume text fields share the editor's history
      if (k === 'z') { e.preventDefault(); e.shiftKey ? redo() : undo(); return; }
      if (k === 'y') { e.preventDefault(); redo(); return; }
      if (k === 'd') { e.preventDefault(); duplicate(field); return; }
    }
    if (ui) return;
    if (mode !== 'design' || !sel) return;
    const s = curShape();
    if (k === 'escape') { select(null); return; }
    if (k === 'delete' || k === 'backspace') { e.preventDefault(); removeSel(); return; }
    const step = e.shiftKey ? 5 : 0.5;
    const mv = {arrowleft: [-step, 0], arrowright: [step, 0], arrowup: [0, -step], arrowdown: [0, step]}[k];
    if (!mv) return;
    e.preventDefault();
    snap();
    if (s) {
      if (s.type === 'line') { s.x1 += mv[0]; s.x2 += mv[0]; s.y1 += mv[1]; s.y2 += mv[1]; if (s.mx != null) { s.mx += mv[0]; s.my += mv[1]; } }
      else { s.x += mv[0]; s.y += mv[1]; }
      F.renderShapes(); updateSel();
    } else { const t0 = trOf(); setTr(t0[0] + mv[0], t0[1] + mv[1]); }
    saveFree(); renderPanel();
  });
  function removeSel(){
    if (!sel) return;
    snap();
    if (sel.kind === 'shape') FD.shapes = FD.shapes.filter(x => x.id !== sel.id), F.renderShapes();
    else setProp('display', 'none', true);
    select(null); saveFree();
  }
  function dupShape(){
    const s = curShape(); if (!s) return;
    snap();
    const c = JSON.parse(JSON.stringify(s));
    c.id = newId();
    if (c.type === 'line') { ['x1', 'x2', 'mx'].forEach(k => { if (c[k] != null) c[k] += 5; }); ['y1', 'y2', 'my'].forEach(k => { if (c[k] != null) c[k] += 5; }); }
    else { c.x += 5; c.y += 5; }
    FD.shapes.push(c); F.renderShapes(); select({kind: 'shape', id: c.id}); saveFree();
  }

  // ── panel ───────────────────────────────────────────────────────────────────────────────────
  const esc = v => String(v == null ? '' : v).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;');
  const row = (label, html) => '<div class="pr"><label>' + label + '</label><div>' + html + '</div></div>';
  const grp = (title, html) => '<div class="grp">' + (title ? '<h4>' + title + '</h4>' : '') + html + '</div>';
  const opt = (v, label, cur) => '<option value="' + esc(v) + '"' + (String(cur) === String(v) ? ' selected' : '') + '>' + esc(label) + '</option>';
  const nice = v => String(v).replace(/_/g, ' ').replace(/^./, c => c.toUpperCase());
  const num = (attr, v, step, min, max) => '<input type="number" ' + attr + ' value="' + esc(v) + '" step="' + (step || 1) + '"' + (min != null ? ' min="' + min + '"' : '') + (max != null ? ' max="' + max + '"' : '') + '>';
  const rng = (attr, v, min, max, step) => '<input type="range" ' + attr + ' value="' + esc(v) + '" min="' + min + '" max="' + max + '" step="' + step + '">';
  const col = (attr, v) => '<input type="color" ' + attr + ' value="' + esc(cssColor(v, '#000000')) + '">';
  const btn = (attr, label, on, title) => '<button ' + attr + (on ? ' class="on"' : '') + (title ? ' title="' + esc(title) + '"' : '') + '>' + label + '</button>';
  const fontSel = (attr, cur) => '<select ' + attr + '>' + opt('', 'Default', cur || '') + RB.fonts.map(f => opt(f[0], f[0], cur || '')).join('') + '</select>';
  const r1 = v => Math.round(v * 10) / 10;
  function loadFont(n){
    const f = RB.fonts.find(x => x[0] === n);
    if (!f || !f[2] || document.querySelector('link[data-font="' + CSS.escape(n) + '"]')) return;
    const l = document.createElement('link');
    l.rel = 'stylesheet'; l.dataset.font = n;
    l.href = 'https://fonts.googleapis.com/css2?family=' + f[2] + '&display=swap';
    document.head.appendChild(l);
  }

  function renderPanel(){
    if (!document.documentElement.classList.contains('rb-pan')) return;
    const tabs = '<div class="tabs">' + [['sel', 'Selected'], ['page', 'Page & colours'], ['secs', 'Sections']]
      .map(([k, l]) => btn('data-tab="' + k + '"', l, tab === k)).join('') + '</div>';
    let body = '';
    try { body = tab === 'page' ? pagePanel() : tab === 'secs' ? secPanel() : (sel ? (sel.kind === 'shape' ? shapePanel() : elPanel()) : emptyPanel()); }
    catch (err) { body = grp('', '<p class="muted">Panel error: ' + esc(err) + '</p>'); }
    panel.innerHTML = tabs + body;
  }
  function emptyPanel(){
    return grp('Design mode', '<p class="muted">Switch to <b>🎨 Design</b>, then click anything on the resume: a heading, a line of text, the photo, ' +
      'the header band, a column, an icon. Drag it to move it, pull the handles to resize or rotate, and style it here ' +
      '(font, size, colour, background, border, shape…).<br><br>Use <b>＋ Insert</b> to add lines, curved lines, arrows, shapes, text boxes, icons or images. ' +
      'Drag a line\'s yellow dot to bend it.<br><br><b>Page &amp; colours</b> changes the whole palette, fonts, text size and layout. ' +
      '<b>Sections</b> lets you reorder, move, hide, rename or add sections.</p>');
  }
  function elPanel(){
    const el = sel.el, cs = getComputedStyle(el), n = document.querySelectorAll(groupSel(el)).length;
    const g = p => getProp(p);
    const fs = parseFloat(g('font-size')) || r1(parseFloat(cs.fontSize) * 0.75);
    const fw = g('font-weight') || cs.fontWeight, it = g('font-style') || cs.fontStyle, td = g('text-decoration') || cs.textDecorationLine, tt = g('text-transform') || cs.textTransform;
    const al = g('text-align') || cs.textAlign;
    const tr = trOf(), rot = parseFloat(getProp('rotate', true)) || 0;
    const isPhoto = sel.key === 'l:photo';
    let h = grp('Selected: ' + esc(friendly(sel.key)),
      row('Apply to', btn('data-act="scope" data-v="one"', 'This one', scope === 'one') + btn('data-act="scope" data-v="all"', 'All like this (' + n + ')', scope === 'all')) +
      '<div class="pr"><div>' + btn('data-act="parent"', '⬆ Parent', 0, 'Select the box around this') + btn('data-act="dupel"', '⧉ Duplicate', 0, 'Duplicate (Ctrl+D)') +
      btn('data-act="hide" class="danger"', '🙈 Hide', 0, 'Hide (Del)') +
      btn('data-act="reset"', '↺ Reset', 0, 'Remove all custom styling of this') + '</div></div>');
    h += grp('Text',
      row('Font', fontSel('data-prop="font-family"', g('font-family'))) +
      row('Size (pt)', num('data-prop="font-size" data-unit="pt"', fs, 0.5, 3, 120)) +
      row('Colour', col('data-prop="color"', g('color') || cs.color) + btn('data-act="clr" data-p="color"', '↺', 0, 'Back to the design colour')) +
      row('Style', btn('data-act="tog" data-p="font-weight" data-on="700" data-off="400"', '<b>B</b>', +fw >= 600) +
        btn('data-act="tog" data-p="font-style" data-on="italic" data-off="normal"', '<i>I</i>', it === 'italic') +
        btn('data-act="tog" data-p="text-decoration" data-on="underline" data-off="none"', '<u>U</u>', /underline/.test(td)) +
        btn('data-act="tog" data-p="text-transform" data-on="uppercase" data-off="none"', 'AA', tt === 'uppercase')) +
      row('Align', ['left', 'center', 'right', 'justify'].map(a => btn('data-act="set" data-p="text-align" data-v="' + a + '"', {left: '⯇', center: '≡', right: '⯈', justify: '☰'}[a], al === a || (a === 'left' && al === 'start'), a)).join('')) +
      row('Spacing', rng('data-prop="letter-spacing" data-unit="px"', parseFloat(g('letter-spacing')) || 0, -1, 10, 0.1)) +
      row('Line height', rng('data-prop="line-height"', parseFloat(g('line-height')) || 1.4, 0.8, 2.6, 0.05)));
    h += grp('Box',
      row('Background', col('data-prop="background-color"', g('background-color') || cs.backgroundColor) + btn('data-act="clr" data-p="background-color"', '↺')) +
      row('Border', num('data-prop="border-width" data-unit="px"', parseFloat(g('border-width')) || 0, 0.5, 0, 30) +
        '<select data-prop="border-style">' + ['solid', 'dashed', 'dotted', 'double'].map(v => opt(v, v, g('border-style') || 'solid')).join('') + '</select>' +
        col('data-prop="border-color"', g('border-color') || cs.borderTopColor)) +
      row('Corners (mm)', num('data-prop="border-radius" data-unit="mm"', parseFloat(g('border-radius')) || 0, 0.5, 0, 200)) +
      row('Padding (mm)', num('data-prop="padding" data-unit="mm"', g('padding') == null ? '' : parseFloat(g('padding')), 0.5, 0, 60)) +
      row('Opacity', rng('data-prop="opacity"', g('opacity') == null ? 1 : g('opacity'), 0, 1, 0.05)) +
      row('Shadow', btn('data-act="tog" data-p="box-shadow" data-on="0 1.5mm 4mm rgba(0,0,0,.28)" data-off=""', 'Drop shadow', !!g('box-shadow'))));
    const W = getProp('width', true), H = getProp('height', true);
    h += grp('Position & size',
      row('Move (mm)', 'X ' + num('data-tr="x"', r1(tr[0]), 0.5) + ' Y ' + num('data-tr="y"', r1(tr[1]), 0.5)) +
      row('Rotate (°)', num('data-own="rotate" data-unit="deg"', rot, 1, -360, 360)) +
      row('Size (mm)', 'W ' + num('data-own="width" data-unit="mm"', W ? parseFloat(W) : '', 0.5, 1, 400) + ' H ' + num('data-own="height" data-unit="mm"', H ? parseFloat(H) : '', 0.5, 1, 600)) +
      row('Layer', btn('data-act="front"', 'Bring to front', getProp('z-index', true) === '30') + btn('data-act="moveReset"', 'Reset position')));
    if (isPhoto || /url\(/.test(cs.backgroundImage)) {
      const bs = parseFloat(getProp('background-size', true)) || 100;
      const bp = String(getProp('background-position', true) || '50% 20%').match(/-?[\d.]+/g) || [50, 20];
      h += grp('Picture',
        row('Shape', '<select data-photo="shape">' + ['circle', 'square', 'rounded', 'ellipse', 'hexagon', 'diamond', 'pentagon', 'triangle', 'star']
          .map(v => opt(v, nice(v), photoShape())).join('') + '</select>') +
        row('Size (mm)', num('data-photo="size"', r1(el.getBoundingClientRect().width / MM), 1, 8, 200)) +
        row('Zoom', rng('data-own="background-size" data-unit="%"', bs, 100, 300, 5)) +
        row('Pan', 'X ' + rng('data-bp="x"', bp[0], 0, 100, 1) + ' Y ' + rng('data-bp="y"', bp[1], 0, 100, 1)) +
        row('Black & white', btn('data-act="tog" data-p="filter" data-on="grayscale(1)" data-off="" data-own="1"', 'B/W', getProp('filter', true) === 'grayscale(1)')));
    }
    return h;
  }
  function photoShape(){
    const cp = String(getProp('clip-path', true) || ''), r = String(getProp('border-radius', true) || '');
    for (const k of ['hexagon', 'diamond', 'pentagon', 'triangle', 'star']) if (cp && cp === F.CLIP[k]) return k;
    if (r === '0' || r === '0mm') return 'square';
    if (r === '14%') return 'rounded';
    if (r === '50%' && getProp('width', true) && getProp('height', true) && getProp('width', true) !== getProp('height', true)) return 'ellipse';
    return r === '50%' ? 'circle' : (RB.design.photo || 'circle');
  }
  function shapePanel(){
    const s = curShape(), t = s.type, line = t === 'line', box = !line;
    const sp = (k, v, step, min, max) => num('data-sp="' + k + '"', v == null ? '' : r1(v), step, min, max);
    let h = grp('Shape: ' + nice(t === 'curve' ? 'curve band' : t),
      '<div class="pr"><div>' + btn('data-act="dup"', '⧉ Duplicate') + btn('data-act="del" class="danger"', '🗑 Delete') +
      btn('data-act="z"', s.z === 'back' ? 'Behind text' : 'In front', s.z === 'back', 'Toggle in front of / behind the resume text') + '</div></div>');
    let st = '';
    if (t !== 'icon' && t !== 'line') st += row('Fill', col('data-sp="fill"', s.fill && s.fill !== 'none' ? s.fill : '#ffffff') + btn('data-act="none" data-p="fill"', 'None', !s.fill || s.fill === 'none'));
    if (t !== 'icon') st += row(line ? 'Colour' : 'Outline', col('data-sp="stroke"', s.stroke && s.stroke !== 'none' ? s.stroke : '#111827')) +
      row('Thickness (pt)', sp('sw', s.sw == null ? (line ? 1.5 : 0) : s.sw, 0.25, 0, 40) +
        '<select data-sp="dash">' + ['solid', 'dashed', 'dotted'].map(v => opt(v, v, s.dash || 'solid')).join('') + '</select>');
    if (t === 'icon') st += row('Icon', '<select data-sp="icon">' + Object.keys(F.D.icons || {}).map(k => opt(k, k, s.icon || 'star')).join('') + '</select>') +
      row('Colour', col('data-sp="color"', s.color || '#111827'));
    if (line) st += row('Arrows', '<select data-sp="arrow">' + [['none', 'None'], ['end', 'End'], ['start', 'Start'], ['both', 'Both']].map(v => opt(v[0], v[1], s.arrow || 'none')).join('') + '</select>') +
      row('Bend', btn('data-act="straight"', 'Straighten', s.mx == null) + '<span class="muted">drag the yellow dot</span>');
    if (t === 'rect' || t === 'text' || (t === 'image' && s.shape === 'rounded')) st += row('Corners (mm)', sp('radius', s.radius || 0, 0.5, 0, 100));
    st += row('Opacity', rng('data-sp="opacity"', s.opacity == null ? 1 : s.opacity, 0, 1, 0.05));
    let h2 = grp('Style', st);
    if (t === 'text') h2 += grp('Text', '<textarea data-sp="text">' + esc(s.text == null ? 'Your text' : s.text) + '</textarea>' +
      row('Font', fontSel('data-sp="font"', s.font)) + row('Size (pt)', sp('size', s.size || 11, 0.5, 3, 160)) +
      row('Colour', col('data-sp="color"', s.color || '#111827')) +
      row('Style', ['bold', 'italic', 'underline', 'upper'].map(k => btn('data-act="stog" data-p="' + k + '"', {bold: '<b>B</b>', italic: '<i>I</i>', underline: '<u>U</u>', upper: 'AA'}[k], !!s[k])).join('')) +
      row('Align', ['left', 'center', 'right', 'justify'].map(a => btn('data-act="sset" data-p="align" data-v="' + a + '"', {left: '⯇', center: '≡', right: '⯈', justify: '☰'}[a], (s.align || 'left') === a)).join('')) +
      row('Line height', rng('data-sp="lh"', s.lh || 1.3, 0.8, 3, 0.05)) + row('Spacing', rng('data-sp="ls"', s.ls || 0, -1, 12, 0.1)) +
      row('Padding (mm)', sp('pad', s.pad == null ? 1 : s.pad, 0.5, 0, 30)));
    if (t === 'image') h2 += grp('Picture', row('Shape', '<select data-sp="shape">' + ['square', 'rounded', 'circle', 'ellipse', 'hexagon', 'diamond', 'pentagon', 'triangle', 'star']
        .map(v => opt(v, nice(v), s.shape || 'square')).join('') + '</select>') +
      row('Zoom', rng('data-sp="zoom"', s.zoom || 100, 100, 300, 5)) +
      row('Pan', 'X ' + rng('data-sp="px"', s.px == null ? 50 : s.px, 0, 100, 1) + ' Y ' + rng('data-sp="py"', s.py == null ? 50 : s.py, 0, 100, 1)) +
      row('', '<label class="btn" style="cursor:pointer;border:1px solid #334155;border-radius:5px;padding:4px 8px" for="rb-img-repl">🖼 Replace image</label>'));
    let pos;
    if (line) pos = row('Start (mm)', 'X ' + sp('x1', s.x1, 0.5) + ' Y ' + sp('y1', s.y1, 0.5)) + row('End (mm)', 'X ' + sp('x2', s.x2, 0.5) + ' Y ' + sp('y2', s.y2, 0.5));
    else pos = row('Position (mm)', 'X ' + sp('x', s.x, 0.5) + ' Y ' + sp('y', s.y, 0.5)) +
      row('Size (mm)', 'W ' + sp('w', s.w, 0.5, 1) + (t === 'text' ? '' : ' H ' + sp('h', s.h, 0.5, 1))) +
      row('Rotate (°)', sp('rot', s.rot || 0, 1, -360, 360)) +
      (t !== 'text' ? row('Flip', btn('data-act="stog" data-p="fx"', '⇋ Horizontal', !!s.fx) + btn('data-act="stog" data-p="fy"', '⇵ Vertical', !!s.fy)) : '');
    return h + h2 + grp('Position', pos);
  }
  const PALETTE = [['--primary', 'Main / bands'], ['--on-primary', 'Text on bands'], ['--accent', 'Accent'], ['--heading', 'Headings'],
    ['--text', 'Body text'], ['--muted', 'Muted text'], ['--page', 'Page background'], ['--side', 'Sidebar background'],
    ['--side-text', 'Sidebar text'], ['--side-heading', 'Sidebar headings'], ['--side-accent', 'Sidebar accent'],
    ['--rule', 'Lines & rules'], ['--tint', 'Chips / tint'], ['--track', 'Bar track']];
  function pagePanel(){
    const D = RB.design, C = RB.choices;
    let h = grp('Colours', PALETTE.map(([v, l]) => row(l, col('data-var="' + v + '"', rootVar(v)) + (FD.vars[v] ? btn('data-act="unvar" data-v="' + v + '"', '↺', 0, 'Back to the design colour') : ''))).join('') +
      '<p class="muted">Header waves, footer and the Venn circles follow the main colour picker in the top bar.</p>');
    h += grp('Fonts & text size', row('Headings', fontSel('data-font="head"', FD.fonts.head)) + row('Body text', fontSel('data-font="body"', FD.fonts.body)) +
      row('Font pairing', dsel('font')) +
      row('Text size', rng('data-ts="1"', Math.round((FD.text_scale || 1) * 100), 60, 160, 1) + '<span class="val" id="rb-ts-v">' + Math.round((FD.text_scale || 1) * 100) + '%</span>'));
    h += grp('Layout', row('Layout', dsel('layout')) +
      (D.layout !== 'single_column' ? row('Column width', rng('data-dset="sidebar_width"', D.sidebar_width || 32, 18, 60, 1)) : '') +
      row('Header', dsel('header')) + row('Header shape', dsel('header_shape')) + row('Footer', dsel('footer_shape')) +
      row('Decoration', dsel('decor')) + row('Headings', dsel('heading_style')) + row('Skills', dsel('skills_style')) +
      row('Languages', dsel('language_style')) + row('Competencies', dsel('competency_style')) +
      row('Photo', dsel('photo')) + row('Photo place', dsel('photo_position')) + row('Name case', dsel('name_case')) +
      row('Name align', dsel('name_align')) +
      row('Extras', ['timeline', 'photo_ring', 'column_divider', 'item_rules'].map(k =>
        '<label style="display:inline-flex;gap:3px;align-items:center;margin-right:6px"><input type="checkbox" data-dset="' + k + '"' + (D[k] ? ' checked' : '') + '>' + nice(k) + '</label>').join('')));
    const hidden = Object.entries(FD.styles).filter(([k, p]) => p.display === 'none');
    h += grp('Hidden elements', hidden.length ? hidden.map(([k]) => '<div class="sec-row"><span title="' + esc(k) + '">' + esc(friendly(k)) + '</span>' + btn('data-act="unhide" data-k="' + esc(k) + '"', 'Show') + '</div>').join('')
      : '<p class="muted">Nothing hidden. Select something in Design mode and press 🙈 Hide (or Del).</p>');
    h += grp('', btn('data-act="resetall" class="danger"', '↺ Reset all free design', 0, 'Removes every custom style, colour, font and shape'));
    return h;
    function dsel(k){ return '<select data-dset="' + k + '">' + (C[k] || []).map(v => opt(v, nice(v), D[k])).join('') + '</select>'; }
  }
  function secPanel(){
    const S = RB.sections, single = RB.design.layout === 'single_column';
    const cols = [['sidebar', single ? '' : 'Side column'], ['main', single ? 'Sections' : 'Main column'], ['bottom', 'Bottom strip']];
    let h = '';
    for (const [c, label] of cols) {
      if (!S[c] || !S[c].length || !label) continue;
      h += grp(label, S[c].map(([k, t]) => '<div class="sec-row"><span title="' + esc(k) + '">' + esc(t) + '</span>' +
        btn('data-sec="up" data-k="' + k + '"', '↑', 0, 'Move up') + btn('data-sec="down" data-k="' + k + '"', '↓', 0, 'Move down') +
        (single ? '' : btn('data-sec="move" data-k="' + k + '"', '⇄', 0, 'Move to the other column')) +
        btn('data-sec="hide" data-k="' + k + '"', '🙈', 0, 'Hide this section') +
        (k.indexOf('custom_') === 0 ? btn('data-sec="delete_custom" data-k="' + k + '" class="danger"', '🗑', 0, 'Delete this section') : '') + '</div>').join(''));
    }
    if (S.hidden && S.hidden.length) h += grp('Hidden sections', S.hidden.map(([k, t]) => '<div class="sec-row"><span>' + esc(t) + '</span>' + btn('data-sec="show" data-k="' + k + '"', 'Show') + '</div>').join(''));
    h += grp('Add your own section', row('Title', '<input type="text" id="rb-cs-title" placeholder="e.g. Volunteering">') +
      row('Style', '<select id="rb-cs-style">' + [['bullets', 'Bullet list'], ['text', 'Paragraphs'], ['chips', 'Tags'], ['plain', 'Plain list']].map(v => opt(v[0], v[1], 'bullets')).join('') + '</select>') +
      (single ? '' : row('Column', '<select id="rb-cs-col">' + opt('main', 'Main', 'main') + opt('sidebar', 'Side', 'main') + '</select>')) +
      '<div class="pr"><div>' + btn('data-act="addcustom"', '＋ Add section') + '</div></div>' +
      (RB.addable.length ? row('Built-in', '<select id="rb-bi">' + RB.addable.map(v => opt(v[0], v[1], '')).join('') + '</select>' + btn('data-act="addbuiltin"', 'Add')) : '') +
      '<p class="muted">Rename any section by clicking its heading in ✍️ Text mode.</p>');
    return h;
  }

  // panel events
  let tx = false;
  const begin = () => { if (!tx) { snap(); tx = true; } };
  const end = () => { if (tx) { tx = false; saveFree(); } };
  function ctlValue(t){
    if (t.type === 'checkbox') return t.checked;
    if (t.type === 'number' || t.type === 'range') return t.value === '' ? null : +t.value;
    return t.value;
  }
  function applyCtl(t){
    const k = t.dataset;
    if (k.prop || k.own) {
      const p = k.prop || k.own, v = t.value === '' ? '' : t.value + (k.unit || '');
      if (p === 'font-family') loadFont(t.value);
      setProp(p, v, !!k.own);
    } else if (k.tr) {
      const c = trOf(), v = +t.value || 0;
      setTr(k.tr === 'x' ? v : c[0], k.tr === 'y' ? v : c[1]);
    } else if (k.bp) {
      const cur = String(getProp('background-position', true) || '50% 20%').match(/-?[\d.]+/g) || [50, 20];
      cur[k.bp === 'x' ? 0 : 1] = t.value;
      setProp('background-position', cur[0] + '% ' + cur[1] + '%', true);
    } else if (k.photo) {
      if (k.photo === 'size') { const v = (+t.value || 30).toFixed(1) + 'mm'; const b = bucket(true); b.width = v; b.height = v; b['max-width'] = 'none'; F.applyStyles(); updateSel(); return; }
      const sh = t.value, b = bucket(true);
      b['border-radius'] = {square: '0', rounded: '14%'}[sh] || (sh === 'circle' || sh === 'ellipse' ? '50%' : '0');
      if (F.CLIP[sh] && sh !== 'circle' && sh !== 'ellipse') b['clip-path'] = F.CLIP[sh]; else delete b['clip-path'];
      if (sh === 'ellipse') { const r = sel.el.getBoundingClientRect(); b.width = r1(r.width / MM) + 'mm'; b.height = r1(r.width / MM * 1.3) + 'mm'; b['max-width'] = 'none'; }
      F.applyStyles(); updateSel();
    } else if (k.sp) {
      const s = curShape(); if (!s) return;
      const v = ctlValue(t);
      if (v === null || v === '') delete s[k.sp]; else s[k.sp] = v;
      if (k.sp === 'font') loadFont(v);
      F.renderShapes(); updateSel();
    } else if (k.var) {
      FD.vars[k.var] = t.value; F.buildCss();
    } else if (k.font) {
      if (t.value) { FD.fonts[k.font] = t.value; loadFont(t.value); } else delete FD.fonts[k.font];
      F.buildCss(); updateSel();
    } else if (k.ts) {
      FD.text_scale = (+t.value || 100) / 100;
      document.documentElement.style.setProperty('--s', FD.text_scale.toFixed(3));
      const lab = $('#rb-ts-v'); if (lab) lab.textContent = t.value + '%';
      updateSel();
    }
  }
  panel.addEventListener('input', e => {
    const t = e.target;
    if (!t.dataset) return;
    if (t.dataset.dset) { if (t.dataset.dset === 'sidebar_width') document.documentElement.style.setProperty('--sw', t.value + '%'); return; }
    if (t.type === 'text' || t.tagName === 'TEXTAREA' && !t.dataset.sp) return;
    begin(); applyCtl(t);
  });
  panel.addEventListener('change', e => {
    const t = e.target;
    if (!t.dataset) return;
    if (t.dataset.dset) {
      const v = t.type === 'checkbox' ? t.checked : t.dataset.dset === 'sidebar_width' ? +t.value : t.value;
      send({design_set: {[t.dataset.dset]: v}}, true);
      return;
    }
    if (!(t.dataset.prop || t.dataset.own || t.dataset.tr || t.dataset.bp || t.dataset.photo || t.dataset.sp || t.dataset.var || t.dataset.font || t.dataset.ts)) return;
    begin(); applyCtl(t); end();
    if (t.tagName === 'SELECT' || t.dataset.photo) renderPanel();
  });
  panel.addEventListener('click', e => {
    const b = e.target.closest('button');
    if (!b) return;
    const d = b.dataset;
    if (d.tab) { tab = d.tab; renderPanel(); return; }
    if (d.sec) {
      if (d.sec === 'delete_custom' && !confirm('Delete this section and its text?')) return;
      send({sec_op: {action: d.sec, key: d.k}}, true); return;
    }
    const a = d.act, s = curShape();
    if (!a) return;
    if (a === 'addcustom') {
      const t = ($('#rb-cs-title') || {}).value || '';
      if (!t.trim()) { status('⚠️ Type a title for the new section'); return; }
      send({add_custom: {title: t.trim(), style: ($('#rb-cs-style') || {}).value || 'bullets', column: ($('#rb-cs-col') || {}).value || 'main'}}, true);
      return;
    }
    if (a === 'addbuiltin') { const v = ($('#rb-bi') || {}).value; if (v) send({add_section: v}, true); return; }
    if (a === 'scope') { scope = d.v; renderPanel(); return; }
    if (a === 'parent') { const p = sel && sel.el && sel.el.parentElement; if (p && p !== document.documentElement) select(p); return; }
    if (a === 'dupel') { duplicate(null); return; }
    snap();
    if (a === 'hide') removeSel();
    else if (a === 'reset') { if (scope === 'all') delete FD.groups[groupSel(sel.el)]; else delete FD.styles[sel.key]; F.buildCss(); F.applyStyles(); }
    else if (a === 'clr') setProp(d.p, '');
    else if (a === 'tog') { const own = !!d.own, on = getProp(d.p, own) === d.on || (!getProp(d.p, own) && b.classList.contains('on')); setProp(d.p, on ? d.off : d.on, own); }
    else if (a === 'set') setProp(d.p, d.v);
    else if (a === 'front') { const on = getProp('z-index', true) === '30'; setProp('z-index', on ? '' : '30', true); setProp('position', '', true); if (!on) { const b2 = bucket(true); if (getComputedStyle(sel.el).position === 'static') b2.position = 'relative'; F.applyStyles(); } }
    else if (a === 'moveReset') { ['translate', 'rotate', 'width', 'height', 'max-width'].forEach(p => setProp(p, '', true)); }
    else if (a === 'unhide') { if (FD.styles[d.k]) { delete FD.styles[d.k].display; tidy(); F.applyStyles(); } }
    else if (a === 'resetall') { if (!confirm('Remove every custom style, colour, font and shape?')) return;
      Object.assign(FD, {styles: {}, groups: {}, vars: {}, fonts: {}, text_scale: 1, shapes: []});
      document.documentElement.style.removeProperty('--s'); F.refresh(); select(null); }
    else if (a === 'unvar') { delete FD.vars[d.v]; F.buildCss(); }
    else if (a === 'dup') { hist.pop(); dupShape(); return; }
    else if (a === 'del') { hist.pop(); removeSel(); return; }
    else if (a === 'z' && s) { if (s.z === 'back') delete s.z; else s.z = 'back'; F.renderShapes(); }
    else if (a === 'none' && s) { s[d.p] = 'none'; F.renderShapes(); }
    else if (a === 'straight' && s) { delete s.mx; delete s.my; F.renderShapes(); }
    else if (a === 'stog' && s) { s[d.p] = !s[d.p]; F.renderShapes(); }
    else if (a === 'sset' && s) { s[d.p] = d.v; F.renderShapes(); }
    updateSel(); renderPanel(); saveFree();
  });

  // ── start ───────────────────────────────────────────────────────────────────────────────────
  layoutChrome();
  const y = ss.get('rbScroll');
  if (y) { window.scrollTo(0, +y); ss.del('rbScroll'); }
  tab = ss.get('rbTab') || 'sel';
  const m0 = ss.get('rbMode'), pan0 = ss.get('rbPan'), sel0 = ss.get('rbSel');
  ['rbMode', 'rbTab', 'rbPan', 'rbSel'].forEach(k => ss.del(k));
  setMode(m0 === 'design' ? 'design' : 'text');
  if (pan0) setPanel(true);
  if (sel0 && mode === 'design') {
    try { const o = JSON.parse(sel0);
      if (o.kind === 'shape' && shapeById(o.id)) select({kind: 'shape', id: o.id}, true);
      else if (o.kind === 'el') { const el = F.find(o.key); if (el) select(el, true); }
    } catch (e) {}
  }
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => { layoutChrome(); updateSel(); });
})();
</script>
"""


def _editor_toolbar(content: dict, design: dict, state: dict) -> str:
    tpl = "".join(f'<option value="{k}" title="{_e(v)}">{k.title()}</option>' for k, v in PRESET_BLURBS.items())
    hidden = set(design.get("hidden_sections") or [])
    empty = [k for k in _ADDABLE if not content.get(k) or k in hidden]
    add = "".join(f'<option value="{k}">{_e(DEFAULT_TITLES[k])}</option>' for k in empty)
    tp = state.get("target_pages")
    pages_opts = "".join(f'<option value="{v}"{" selected" if str(tp or "") == v else ""}>{lbl}</option>'
                         for v, lbl in (("", "Pages: auto"), ("1", "Fit 1 page"), ("2", "Fit 2 pages")))
    pdf = state.get("last_pdf") or ""
    last = (f'Last PDF: <a href="{MEDIA_URL}/{_e(os.path.basename(pdf))}" target="_blank">open</a>'
            if pdf and os.path.exists(pdf) else "Click any text to edit it")
    shapes = [("line", "／ Line"), ("bend", "⌒ Curved line"), ("arrow", "→ Arrow"), ("rect", "▭ Rectangle"),
              ("rounded", "▢ Rounded box"), ("ellipse", "◯ Circle / ellipse"), ("triangle", "△ Triangle"),
              ("diamond", "◇ Diamond"), ("hexagon", "⬡ Hexagon"), ("pentagon", "⬠ Pentagon"), ("star", "☆ Star"),
              ("wave", "〰 Wave band"), ("curve", "◠ Curve band"), ("text", "T  Text box"), ("icon", "★ Icon"),
              ("image", "🖼 Image…")]
    ins = "".join(f'<option value="{k}">{_e(v)}</option>' for k, v in shapes)
    return (f'<div id="rb-bar"><b>✏️ Resume editor</b>'
            f'<span class="seg"><button id="rb-mode-text" class="on" title="Type into the resume">✍️ Text</button>'
            f'<button id="rb-mode-design" title="Select, move, resize, rotate and restyle anything">🎨 Design</button></span>'
            f'<select id="rb-insert" title="Add a line, shape, text box, icon or image"><option value="">＋ Insert…</option>{ins}</select>'
            f'<button id="rb-addtext" title="Add a text box in the same font, size and colour as the resume text">＋ Text box</button>'
            f'<button id="rb-undo" title="Undo (Ctrl+Z)">↶</button><button id="rb-redo" title="Redo (Ctrl+Y / Ctrl+Shift+Z)">↷</button>'
            f'<button id="rb-panel-btn" title="Style panel: selection, colours, fonts, layout, sections">🎛 Panel</button>'
            f'<select id="rb-tpl" title="Switch format"><option value="">Template…</option>{tpl}</select>'
            f'<input type="color" id="rb-color" value="{_e(design["colors"]["primary"])}" title="Main colour">'
            f'<select id="rb-add" title="Add a section"><option value="">＋ Add section…</option>{add}'
            f'<option value="__custom">✚ Your own section…</option></select>'
            f'<label class="btn" title="Upload a photo">📷 Photo<input type="file" id="rb-photo" accept="image/*" hidden></label>'
            f'<button id="rb-nophoto" title="Remove the photo block">No photo</button>'
            f'<input type="text" id="rb-ai" placeholder="Ask AI, e.g. make bullets punchier">'
            f'<button id="rb-ai-go">✨ Apply</button>'
            f'<select id="rb-pages" title="Strict page limit for the PDF">{pages_opts}</select>'
            f'<button id="rb-save" class="primary">💾 Save &amp; export PDF</button>'
            f'<span id="rb-status">{last}</span></div>'
            f'<input type="file" id="rb-img-file" accept="image/*" hidden><input type="file" id="rb-img-repl" accept="image/*" hidden>'
            f'<div id="rb-ctl"><button data-a="add" title="Add an item below">＋</button>'
            f'<button data-a="dup" title="Duplicate this item (Ctrl+D)">⧉</button>'
            f'<button data-a="up" title="Move up">↑</button><button data-a="del" title="Delete">✕</button></div>'
            f'<div id="rb-sctl"><button data-a="up" title="Move section up">↑</button><button data-a="down" title="Move section down">↓</button>'
            f'<button data-a="move" title="Move to the other column">⇄</button><button data-a="hide" title="Hide section">✕</button></div>'
            f'<div id="rb-selbox"><span class="rb-tag"></span><i class="rb-h" data-h="move" title="Drag to move"></i>'
            f'<i class="rb-h" data-h="rot" title="Drag to rotate (Shift snaps)"></i><i class="rb-h" data-h="e"></i>'
            f'<i class="rb-h" data-h="s"></i><i class="rb-h" data-h="se" title="Resize (Shift keeps/frees the ratio)"></i></div>'
            f'<i class="rb-pt" id="rb-pt-p1" data-h="p1"></i><i class="rb-pt" id="rb-pt-p2" data-h="p2"></i>'
            f'<i class="rb-pt mid" id="rb-pt-mid" data-h="mid" title="Drag to bend"></i>'
            f'<div id="rb-panel"></div>'
            f'<div id="rb-hint">Click text to type · hover an item for ＋ ⧉ ↑ ✕ · Ctrl+Z undo · Ctrl+D duplicate · Ctrl+S saves</div>')


def _editor_meta(content: dict, design: dict) -> dict:
    """What the editor's panel needs: design choices, the section columns as rendered, fonts."""
    wd = _effective_design(content, design)
    side, main = _placement(wd)
    hidden = list(design.get("hidden_sections") or [])
    custom = {x["id"]: x["title"] for x in content.get("custom_sections") or []}
    token = _EDIT.set(True)
    try:
        def shown(keys, is_side):
            return [[k, custom.get(k) or _title(wd, k)] for k in keys
                    if k not in hidden and (k in custom or (k in SECTION_KEYS and _section_html(k, content, wd, is_side)))]
        sections = {"sidebar": shown(side, True), "main": shown(main, False),
                    "bottom": shown(wd.get("bottom_sections") or [], False),
                    "hidden": [[k, custom.get(k) or (_title(wd, k) if k in SECTION_KEYS else k)] for k in hidden]}
    finally:
        _EDIT.reset(token)
    keys = ("layout", "header", "header_shape", "footer_shape", "decor", "heading_style", "skills_style", "language_style",
            "competency_style", "photo", "photo_position", "name_case", "name_align", "font", "sidebar_width", "timeline",
            "photo_ring", "column_divider", "item_rules")
    return {"design": {k: design.get(k) for k in keys}, "sections": sections,
            "choices": {k: sorted(v) for k, v in _DESIGN_CHOICES.items()},
            "fonts": [[n, cat, g] for n, cat, g in _FREE_FONTS],
            "addable": [[k, DEFAULT_TITLES[k]] for k in _ADDABLE if not content.get(k) or k in hidden]}


def editor_page() -> str:
    """Full HTML page of the current resume in edit mode."""
    try:
        st = _load_state()
        content, design = st.get("content"), st.get("design")
        if not content or not design:
            return ("<!doctype html><meta charset=utf-8><title>Resume editor</title><body style='font:16px Segoe UI;"
                    "background:#0b1220;color:#e5e7eb;padding:60px;text-align:center'><h2>No resume yet</h2>"
                    "<p>Ask Jarvis to create one first, e.g. <i>“make my resume like this”</i> with a design image and your details.</p>")
        photo = st.get("photo") or ""
        photo_uri = _data_uri(photo) if photo and os.path.exists(photo) else ""
        html = _render_html(content, design, photo_uri, float(st.get("render_scale") or 1.0), edit=True)
        data = json.dumps({"content": content, "rev": _state_rev(st), "photo": photo if photo_uri else "",
                           **_editor_meta(content, design)}, ensure_ascii=False).replace("</", "<\\/")
        html = html.replace("</head>", _EDITOR_CSS + "</head>", 1)
        html = html.replace("</body>", _editor_toolbar(content, design, st) +
                            f"<script>window.__RB__ = {data};</script>" + _EDITOR_JS + _EDITOR_FIT_JS + "</body>", 1)
        return html
    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"<!doctype html><meta charset=utf-8><body style='font:15px Segoe UI;padding:40px'>Editor error: {_e(e)}"


def _apply_op(content: dict, action: str, path: str) -> None:
    parts = [p for p in str(path or "").split(".") if p]
    if len(parts) < 2 or not parts[-1].isdigit():
        return
    idx, key = int(parts[-1]), parts[-2]
    lst = content
    for k in parts[:-1]:
        lst = lst[int(k)] if (k.isdigit() and isinstance(lst, list)) else (lst.get(k) if isinstance(lst, dict) else None)
        if lst is None:
            return
    if not isinstance(lst, list) or not 0 <= idx < len(lst):
        return
    if action == "del":
        lst.pop(idx)
    elif action == "add":
        lst.insert(idx + 1, json.loads(json.dumps(_ITEM_TEMPLATES.get(key, "New item"))))
    elif action == "dup" and key != "custom_sections":       # a whole custom section carries an id; items don't
        lst.insert(idx + 1, json.loads(json.dumps(lst[idx])))
    elif action == "up" and idx > 0:
        lst[idx - 1], lst[idx] = lst[idx], lst[idx - 1]
    elif action == "down" and idx < len(lst) - 1:
        lst[idx + 1], lst[idx] = lst[idx], lst[idx + 1]


def _section_op(c: dict, d: dict, action: str, key: str) -> str:
    """Editor section controls: up / down / move (other column) / hide / show / delete_custom."""
    key = str(key or "")
    if not (key in SECTION_KEYS or re.fullmatch(r"custom_\d{1,4}", key)):
        return "Unknown section."
    wd = _effective_design(c, d)
    side, main = _placement(wd)
    if wd["layout"] == "single_column":
        side, main = [], side + main
    lists = {"side": side, "main": main, "bottom": list(wd.get("bottom_sections") or [])}
    hidden = [k for k in (d.get("hidden_sections") or []) if k != key]
    note = "Section updated."
    if action == "hide":
        hidden.append(key)
        note = "Section hidden (Sections tab → Show brings it back)."
    elif action == "show":
        note = "Section shown."
    elif action == "delete_custom":
        c["custom_sections"] = [x for x in c.get("custom_sections") or [] if x["id"] != key]
        for lst in lists.values():
            if key in lst:
                lst.remove(key)
        note = "Section deleted."
    else:
        name = next((n for n, lst in lists.items() if key in lst), None)
        if not name:
            return "Section not found."
        lst = lists[name]
        if action in ("up", "down"):
            vis = [k for k in lst if k not in hidden and (k.startswith("custom_") or _section_html(k, c, wd, name == "side"))]
            i = vis.index(key) if key in vis else -1
            j = i - 1 if action == "up" else i + 1
            if i < 0 or not 0 <= j < len(vis):
                return "Already at the " + ("top." if action == "up" else "bottom.")
            a, b = lst.index(key), lst.index(vis[j])
            lst[a], lst[b] = lst[b], lst[a]
        elif action == "move":
            if wd["layout"] == "single_column":
                return "This layout has one column — switch the layout in Page & colours first."
            dst = "main" if name in ("side", "bottom") else "side"
            lst.remove(key)
            lists[dst].append(key)
            note = "Moved to the " + ("main" if dst == "main" else "side") + " column."
    d["sidebar_sections"], d["main_sections"], d["bottom_sections"] = lists["side"], lists["main"], lists["bottom"]
    d["hidden_sections"] = hidden
    d["pinned"] = list(dict.fromkeys(lists["side"] + lists["main"]))      # the user arranged it: the fit loop keeps it
    return note


def _design_set(d: dict, changes: dict) -> dict:
    """Editor 'Page & colours' layout controls → validated design keys."""
    for k, v in (changes or {}).items():
        if k in _DESIGN_CHOICES and str(v) in _DESIGN_CHOICES[k]:
            d[k] = str(v)
        elif k in ("timeline", "photo_ring", "column_divider", "item_rules"):
            d[k] = bool(v)
        elif k == "sidebar_width":
            try:
                d[k] = max(18, min(60, int(float(v))))
            except Exception:
                pass
    if d.get("layout") != "single_column" and not d.get("sidebar_sections"):
        d["sidebar_sections"] = [k for k in ("contact", "skills", "education", "languages")]
    return _sanitize_design(d)


def editor_save(payload: dict) -> dict:
    """Backend of the editor: apply text edits + one optional action, persist, optionally export the PDF."""
    try:
        st = _load_state()
        if not st.get("content") or not st.get("design"):
            return {"ok": False, "message": "No resume yet — create one in Jarvis first."}
        raw = payload.get("content") if isinstance(payload.get("content"), dict) else st["content"]
        content = _normalise_content(json.loads(json.dumps(raw)))
        design = st["design"]
        note = "Saved."
        if "free" in payload:                         # Design mode: styles, shapes, palette, fonts (always sent)
            free = _clean_free(payload.get("free"))
            if free:
                design["free"] = free
            else:
                design.pop("free", None)

        if payload.get("restore_snap"):               # editor undo / redo of a structural change
            snap = _undo_get(str(payload["restore_snap"]))
            if not snap:
                return {"ok": False, "message": "That step is too old to undo."}
            st.update({"content": content, "design": design})
            here = _undo_push(_undo_snap(st))
            st.update({k: snap.get(k) for k in _UNDO_KEYS})
            st["updated"] = time.time()
            _save_state(st)
            return {"ok": True, "reload": True, "snap": here, "rev": _state_rev(st), "message": "Restored."}
        before = _undo_snap({**st, "content": content, "design": design})

        op = payload.get("op") or {}
        if isinstance(op, dict) and op.get("action") in ("add", "del", "up", "down", "dup"):
            _apply_op(content, op["action"], op.get("path", ""))
            content = _normalise_content(content)
        sec = str(payload.get("add_section") or "")
        if sec in _ITEM_TEMPLATES:
            design["hidden_sections"] = [k for k in design.get("hidden_sections") or [] if k != sec]
            if not content.get(sec):
                content[sec] = [json.loads(json.dumps(_ITEM_TEMPLATES[sec]))]
                content = _normalise_content(content)
        custom = payload.get("add_custom")
        if isinstance(custom, dict) and str(custom.get("title") or "").strip():
            content["custom_sections"] = _custom_sections((content.get("custom_sections") or []) + [
                {"title": str(custom["title"]), "style": custom.get("style"), "items": []}])
            new_id = content["custom_sections"][-1]["id"]
            col = "sidebar_sections" if custom.get("column") == "sidebar" and design.get("layout") != "single_column" else "main_sections"
            design.setdefault(col, []).append(new_id)
            note = "Section added — click its first line to type."
        if isinstance(payload.get("sec_op"), dict):
            note = _section_op(content, design, str(payload["sec_op"].get("action") or ""), payload["sec_op"].get("key"))
        tpl = str(payload.get("template") or "").lower()
        if tpl in PRESETS:
            keep = {k: design[k] for k in ("free", "hidden_sections") if design.get(k)}
            design = _sanitize_design(json.loads(json.dumps(PRESETS[tpl])) | {"source": tpl}) | keep
            note = f"Switched to the {tpl} format."
        if isinstance(payload.get("design_set"), dict):
            design = _design_set(design, payload["design_set"])
            note = "Layout updated."
        if payload.get("color"):
            design = _sanitize_design(_apply_color(design, str(payload["color"])))
        if payload.get("photo") and os.path.exists(str(payload["photo"])):
            st["photo"] = str(payload["photo"])
            if design.get("photo") == "none":
                design["photo"] = "square" if design.get("header") == "diagonal_banner" else "circle"
        if payload.get("remove_photo"):
            st["photo"] = ""
            design["photo"] = "none"
        if payload.get("instruction"):
            content = _edit_content(content, str(payload["instruction"]))
            note = "AI edit applied."
        if "target_pages" in payload:
            tp = str(payload.get("target_pages") or "")
            st["target_pages"] = int(tp) if tp in ("1", "2", "3") else None
            note = f"Page target: {st['target_pages'] or 'auto'}."

        st.update({"content": content, "design": design, "awaiting_details": False, "updated": time.time()})
        _save_state(st)

        def undo_id() -> str:                      # a structural change becomes one step of the editor's Ctrl+Z
            return _undo_push(before) if _undo_snap(st) != before else ""
        if "target_pages" in payload:
            payload["export"] = True               # fit to the new target now, so the editor shows the result
        if not payload.get("export"):
            return {"ok": True, "reload": True, "message": note, "snap": undo_id(), "rev": _state_rev(st)}

        slug = re.sub(r"[^a-z0-9]+", "_", (content.get("name") or "resume").lower()).strip("_")[:30] or "resume"
        photo = st.get("photo") if st.get("photo") and os.path.exists(st["photo"]) else ""
        target = st.get("target_pages")
        old_scale = float(st.get("render_scale") or 1.0)
        files, fitted, fit_note = _fit_render(content, design, photo, f"resume_{slug}_{int(time.time())}", target)
        if fitted is not content:
            st["content"] = fitted
        st["last_pdf"] = files["pdf"]
        st["render_scale"] = files.get("scale", 1.0)
        _save_state(st)
        pdf_url = f"{MEDIA_URL}/{os.path.basename(files['pdf'])}"
        return {"ok": True, "reload": False, "pdf_url": pdf_url, "snap": undo_id(), "rev": _state_rev(st),
                "png_urls": [f"{MEDIA_URL}/{os.path.basename(p)}" for p in files["pngs"]],
                # fitting changed the text or the type size -> reload so the editor shows exactly the PDF
                "reload": bool(fit_note) or "target_pages" in payload or abs(files.get("scale", 1.0) - old_scale) > 1e-3,
                "message": f"PDF exported ({files['pages']} page(s)).",
                "message_html": f'✅ PDF exported ({files["pages"]} page(s)){" — " + _e(fit_note) if fit_note else ""} — <a href="{pdf_url}" target="_blank">open PDF</a>'}
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"ok": False, "message": f"Save failed: {e}"}


def open_resume_editor() -> str:
    if not _load_state().get("content"):
        return "There's no resume to edit yet, Sir. Ask me to create one first."
    try:
        import webbrowser
        webbrowser.open(EDITOR_URL)
    except Exception:
        pass
    return (f"Opening the resume editor, Sir: ✏️ [Edit your resume]({EDITOR_URL})\n\n"
            "Click any text on the resume to change it. Hover an item for ＋ / ↑ / ✕. Use the toolbar to switch "
            "template, colour or photo, add a section, or ask the AI to rewrite something. Then press "
            "**Save & export PDF**.")


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
_TEMPLATE_RX = re.compile(r"\b(" + "|".join(PRESETS) + r")\s+(?:template|format|style|design|layout|theme)\b|"
                          r"\b(?:template|format|style|theme)\s*[:=-]?\s*(" + "|".join(PRESETS) + r")\b", re.I)
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
        # bare "edit my resume" / "open the resume editor" (no concrete change) → visual editor
        if re.fullmatch(r"(?:(?:please|jarvis|hey jarvis|ok)[,\s]+)?(?:i\s+(?:want|need)\s+to\s+|let\s+me\s+|can\s+i\s+|"
                        r"how\s+(?:do|can)\s+i\s+)?(?:open\s+(?:the\s+|my\s+)?)?(?:edit|modify|change|tweak|fix|update)?\s*"
                        r"(?:my\s+|the\s+|this\s+)?" + _NOUN + r"(?:\s+(?:editor|manually|myself|content|text|details))?"
                        r"(?:\s+(?:please|now|myself|manually))?\s*[.!?]*", lower.strip()) and \
                re.search(r"\b(edit|modify|change|tweak|fix|update|editor)\b", lower):
            return {"_editor": True}
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
        head = lower[:220]                           # "tech stack" deep in pasted details must not pick a template
        tpl_m = _TEMPLATE_RX.search(head)
        template = (tpl_m.group(1) or tpl_m.group(2)).lower() if tpl_m else ""
        col_m = _COLOR_RX.search(head)
        color = ""
        if col_m and re.search(r"\b(colou?r|theme|tone|shade|accent)\b", head):
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
                  instruction: str = "", reuse_photo: bool = False, open_file: bool = False, pages: int | None = None):
    """Generator: progress lines, then markdown with PNG preview(s) + PDF/HTML links."""
    try:
        state = _load_state()
        # "single page resume" / "fit it in 2 pages" -> strict page target (looked for in the request part only)
        pages = pages or _parse_pages((details or instruction or "")[:300])
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

        # 1) Design — an uploaded design is copied exactly (resume_replica); the old analysis is only a fallback
        design, design_note, replica_err = None, "", ""
        tpl_req = (template or "").lower() in PRESETS
        if image_path and not tpl_req:
            from app.services.resume_replica.integrate import (analyse_with_progress, replica_design, replica_enabled,
                                                               replica_note)
            if replica_enabled():
                yield "🎨 Measuring your reference design so I can copy it exactly (first time ~1–2 min)…\n\n"
                try:
                    spec = yield from analyse_with_progress(image_path)
                    if spec:
                        design, design_note = replica_design(spec, state.get("design")), replica_note(spec)
                    else:
                        replica_err = "it didn't look like a resume page"
                except Exception as e:
                    replica_err = str(e)[:160]
        if design is None:
            if image_path:
                yield "🎨 Studying the design of your reference resume (layout, colours, header, sections)…\n\n"
            design, design_note = _resolve_design(image_path, template, color, state.get("design"))
            if replica_err:
                design_note = (f"⚠️ I couldn't make an exact copy of this design ({replica_err}), so I matched it as "
                               f"closely as the built-in formats allow. {design_note}")
        if design.get("replica") and color:
            design_note += (" (Colour requests don't apply to an exact copy — it keeps the reference's colours. "
                            "Say *use the modern template* for a format I can recolour.)")

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
            design = _apply_layout_hint(design, content)        # "LEFT COLUMN: Contact, Skills" beats the picture
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
        if not photo and state.get("photo") and os.path.exists(state["photo"]) and design.get("photo") != "none":
            photo = state["photo"]                       # the user's own photo carries over to new designs

        # 4) Render
        target = pages or (None if has_new_details else state.get("target_pages"))
        yield ("🖨️ Typesetting and rendering the PDF" + (f" (strictly {target} page{'s' if target > 1 else ''})" if target else "") + "…\n\n")
        slug = re.sub(r"[^a-z0-9]+", "_", (content.get("name") or "resume").lower()).strip("_")[:30] or "resume"
        stem = f"resume_{slug}_{int(time.time())}"
        files, content, fit_note = _fit_render(content, design, photo, stem, target)

        state.update({"design": design, "content": content, "awaiting_details": False, "photo": photo, "target_pages": target,
                      "ref_image": ref_for_photo, "reuse_photo": False, "last_pdf": files["pdf"], "updated": time.time(),
                      "render_scale": files.get("scale", 1.0)})
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
        fit_txt = f" To fit {target} page{'s' if target > 1 else ''} I {fit_note}." if fit_note else ""
        yield (f"Your resume is ready, Sir. {design_note} {files['pages']} page(s).{fit_txt}\n\n{previews}\n\n"
               f"✏️ [Edit text, sections & layout]({EDITOR_URL}) · 📄 [Download PDF]({MEDIA_URL}/{name(files['pdf'])}) · "
               f"🌐 [HTML]({MEDIA_URL}/{name(files['html'])})\n\n"
               f"Saved to `{files['pdf']}`. Say things like *\"change the resume colour to navy\"*, *\"use the modern template\"* "
               f"or *\"add AWS certification to my resume\"* to tweak it.{tips}")
    except Exception as e:
        import traceback
        traceback.print_exc()
        yield f"Sorry Sir, the resume builder hit a problem: {e}"


def resume_tool(details: str = "", image_path: str = "", photo_path: str = "", template: str = "", color: str = "",
                instruction: str = "", reuse_photo: bool = False, pages: int | None = None):
    """Registry entry: also handles a bare 'list templates' request."""
    if not any([details, image_path, photo_path, template, color, instruction]) and not _load_state().get("content"):
        yield list_resume_templates()
        return
    yield from create_resume(details=details, image_path=image_path, photo_path=photo_path, template=template,
                             color=color, instruction=instruction, reuse_photo=reuse_photo, pages=pages)
