"""
compiler.py — Scene graph → print-ready HTML/CSS.

Entry point: compile_replica_html(content, replica_doc, photo_uri, scale, edit)
Returns a complete HTML document string.

Node types handled: frame, group, text, path, image, repeat, chart, rule
Chart types: radar, bars, dots, rings, venn, chips, tag_level, list
Photo clip shapes: circle, rounded, square, hexagon, diamond, squircle
"""
from __future__ import annotations

import html as _html
import math
import json
import re
import contextvars

# ── Editor mode context var (mirrors resume_builder.py's _EDIT) ─────────────
_REPLICA_EDIT = contextvars.ContextVar("replica_edit_mode", default=False)

# ── Google-font families we know how to request ──────────────────────────────
_GF_FAMILIES = {
    "roboto":               "Roboto:wght@300;400;500;700;900",
    "poppins":              "Poppins:wght@300;400;500;600;700",
    "montserrat":           "Montserrat:wght@400;600;700;800",
    "playfair display":     "Playfair+Display:wght@500;700",
    "cormorant garamond":   "Cormorant+Garamond:wght@500;600;700",
    "jetbrains mono":       "JetBrains+Mono:wght@500;700",
    "lora":                 "Lora:wght@400;600",
    "inter":                "Inter:wght@400;500;600",
    "open sans":            "Open+Sans:wght@400;600;700",
    "lato":                 "Lato:wght@400;700",
}

# ── Small inline icon set (same paths as resume_builder._ICONS) ─────────────
_ICONS: dict[str, str] = {
    "phone":    '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "mail":     '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
    "pin":      '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
    "linkedin": '<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-4 0v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/>',
    "link":     '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>',
    "trophy":   '<path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/>',
    "award":    '<circle cx="12" cy="8" r="7"/><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"/>',
    "star":     '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>',
    "globe":    '<circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>',
    "heart":    '<path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>',
    "cap":      '<path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/>',
    "briefcase":'<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>',
    "code":     '<polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/>',
    "clock":    '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    "compass":  '<circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/>',
    "gear":     '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 1 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>',
    "book":     '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>',
    "users":    '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "user":     '<path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
    "pie":      '<path d="M21.21 15.89A10 10 0 1 1 8 2.83"/><path d="M22 12A10 10 0 0 0 12 2v10z"/>',
    "bars":     '<line x1="12" y1="20" x2="12" y2="10"/><line x1="18" y1="20" x2="18" y2="4"/><line x1="6" y1="20" x2="6" y2="16"/>',
    "trending": '<polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/>',
    "money":    '<line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>',
    "shield":   '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
    "target":   '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    "lightbulb":'<path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/>',
    "megaphone":'<path d="m3 11 18-5v12L3 14v-3z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/>',
    "handshake":'<path d="m11 17 2 2a1 1 0 1 0 3-3"/><path d="m14 14 2.5 2.5a1 1 0 1 0 3-3l-3.88-3.88a3 3 0 0 0-4.24 0l-.88.88a1 1 0 1 1-3-3l2.81-2.81a5.79 5.79 0 0 1 7.06-.87l.47.28a2 2 0 0 0 1.42.25L21 4"/><path d="m21 3 1 11h-2"/><path d="M3 3 2 14l6.5 6.5a1 1 0 1 0 3-3"/><path d="M3 4h8"/>',
    "chat":     '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
    "refresh":  '<path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/><path d="M8 16H3v5"/>',
    "clipboard":'<rect x="8" y="2" width="8" height="4" rx="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/>',
    "presentation":'<path d="M2 3h20"/><path d="M21 3v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V3"/><path d="m7 21 5-5 5 5"/>',
}

# ── Section title defaults ────────────────────────────────────────────────────
_DEFAULT_TITLES = {
    "profile": "Profile", "highlights": "Career Highlights", "contact": "Contact",
    "skills": "Skills", "competencies": "Core Competencies", "experience": "Work Experience",
    "education": "Education", "achievements": "Achievements", "certifications": "Certifications",
    "languages": "Languages", "interests": "Interests", "projects": "Projects",
    "references": "References",
}


# ════════════════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ════════════════════════════════════════════════════════════════════════════

def compile_replica_html(
    content: dict,
    replica_doc: dict,
    photo_uri: str = "",
    scale: float = 1.0,
    edit: bool = False,
) -> str:
    """
    Main entry point. Returns a complete HTML document string.

    content      : normalised resume content dict (same format as resume_builder.py)
    replica_doc  : the stored replica document with 'scene_graph' inside
    photo_uri    : base64 data URI of the user's photo, or empty string
    scale        : 0.74-1.0 — same as legacy builder's --s CSS variable
    edit         : if True, add contenteditable spans with data-f attributes
    """
    token = _REPLICA_EDIT.set(edit)
    try:
        scene_graph: dict = replica_doc.get("scene_graph") or {}
        style_registry: dict = replica_doc.get("style_registry") or {}
        design: dict = replica_doc.get("design") or {}

        ctx: dict = {
            "photo_uri": photo_uri,
            "scale": scale,
            "edit": edit,
            "style_registry": style_registry,
            "design": design,
            "in_sidebar": False,
            "content": content,
        }

        font_link = _collect_google_fonts(scene_graph, style_registry)
        css = _compile_document_css(scene_graph, style_registry, scale, edit)

        # Render root page node children
        root_children = scene_graph.get("children") or []
        body_html = "".join(_compile_node(child, content, ctx) for child in root_children)

        title_name = _e(content.get("name") or "Resume")

        return (
            f'<!DOCTYPE html>\n<html lang="en">\n<head>\n'
            f'<meta charset="utf-8">\n'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">\n'
            f'<title>{title_name}</title>\n'
            f'{font_link}'
            f'<style>\n{css}\n</style>\n'
            f'</head>\n<body>\n'
            f'{body_html}\n'
            f'</body>\n</html>'
        )
    finally:
        _REPLICA_EDIT.reset(token)


# ════════════════════════════════════════════════════════════════════════════
#  CSS GENERATION
# ════════════════════════════════════════════════════════════════════════════

def _compile_document_css(
    scene_graph: dict,
    style_registry: dict,
    scale: float,
    edit: bool = False,
) -> str:
    """Generates the complete CSS for the document."""
    colors: dict = scene_graph.get("colors") or {}
    primary     = colors.get("primary", "#2563eb")
    sidebar_bg  = colors.get("sidebar_bg", "#1f2a44")
    page_bg     = colors.get("page_bg", "#ffffff")
    heading_col = colors.get("heading", "#1e293b")
    text_col    = colors.get("text", "#334155")
    accent      = colors.get("accent", primary)
    header_text = colors.get("header_text", "#ffffff")
    track_col   = colors.get("track", "#e2e8f0")

    # heading style from style_registry
    hs = style_registry.get("heading_style", "underline")

    heading_css = ""
    if hs == "underline":
        heading_css = (
            ".rr-section-heading{border-bottom:1.5px solid var(--heading);padding-bottom:1.2mm;margin-bottom:2mm}"
        )
    elif hs == "bar_left":
        heading_css = (
            ".rr-section-heading{border-left:3px solid var(--primary);padding-left:2.5mm;margin-bottom:2mm}"
        )
    elif hs == "boxed":
        heading_css = (
            ".rr-section-heading{background:var(--primary);color:var(--on-primary);"
            "padding:1mm 3mm;border-radius:2px;margin-bottom:2mm}"
        )
    elif hs == "caps_line":
        heading_css = (
            ".rr-section-heading{text-transform:uppercase;letter-spacing:.08em;"
            "border-bottom:1px solid var(--heading);padding-bottom:.8mm;margin-bottom:2mm}"
        )
    elif hs == "square_icon":
        heading_css = (
            '.rr-section-heading::before{content:"";display:inline-block;width:.72em;height:.72em;'
            "background:var(--primary);border-radius:1px;margin-right:2mm;vertical-align:-.05em}"
            ".rr-section-heading{margin-bottom:2mm}"
        )
    elif hs == "dot":
        heading_css = (
            '.rr-section-heading::before{content:"";display:inline-block;width:.65em;height:.65em;'
            "background:var(--primary);border-radius:50%;margin-right:2mm;vertical-align:-.05em}"
            ".rr-section-heading{margin-bottom:2mm}"
        )
    else:  # plain
        heading_css = ".rr-section-heading{margin-bottom:2mm}"

    editor_css = ""
    if edit:
        editor_css = (
            "[data-f]{outline:none;border-radius:2px;cursor:text}"
            "[data-f]:hover{background:rgba(59,130,246,.10)}"
            "[data-f]:focus{background:rgba(59,130,246,.15);box-shadow:0 0 0 2px rgba(59,130,246,.8)}"
        )

    s = f"{scale:.4f}"

    return f"""
@page{{size:A4;margin:0}}
*{{box-sizing:border-box}}
html,body{{margin:0;padding:0}}
body{{width:210mm;-webkit-print-color-adjust:exact;print-color-adjust:exact;
  --s:{s};--primary:{primary};--accent:{accent};--heading:{heading_col};
  --text:{text_col};--sidebar-bg:{sidebar_bg};--page-bg:{page_bg};
  --on-primary:{header_text};--track:{track_col};
  background:{page_bg};color:{text_col};font-size:calc(9.6pt * {s})}}
.rr-page-bg{{position:fixed;inset:0;z-index:0}}
.rr-sidebar-bg{{position:fixed;top:0;bottom:0;z-index:0}}
.rr-layout{{position:relative;z-index:1;display:flex;align-items:flex-start}}
.rr-sidebar{{flex:none;-webkit-box-decoration-break:clone;box-decoration-break:clone}}
.rr-main{{flex:1;min-width:0;-webkit-box-decoration-break:clone;box-decoration-break:clone}}
.rr-section{{margin-bottom:calc(4mm * {s})}}
.rr-section-heading{{color:var(--heading);font-weight:700;font-size:calc(9pt * {s});
  text-transform:uppercase;letter-spacing:.05em}}
{heading_css}
.rr-path{{position:absolute;inset:0;width:100%;height:100%}}
.rr-heading-group{{position:relative}}
.rr-photo-circle{{border-radius:50%}}
.rr-photo-hexagon{{clip-path:polygon(50% 0%,100% 25%,100% 75%,50% 100%,0% 75%,0% 25%)}}
.rr-photo-diamond{{clip-path:polygon(50% 0%,100% 50%,50% 100%,0% 50%)}}
.rr-photo-squircle{{border-radius:30% / 35%}}
.rr-photo-rounded{{border-radius:14%}}
.rr-photo-square{{border-radius:0}}
.rr-photo{{background-size:cover;background-position:center top;background-repeat:no-repeat}}
.rr-photo-empty{{display:flex;align-items:center;justify-content:center;
  background:var(--primary);color:var(--on-primary);font-weight:700}}
.rr-bars{{width:100%}}
.rr-bar-row{{display:flex;align-items:center;gap:2mm;margin-bottom:1.2mm;font-size:calc(8pt * {s})}}
.rr-bar-label{{flex:0 0 30%;font-size:calc(7.8pt * {s})}}
.rr-bar-track{{flex:1;height:2.5mm;background:var(--track);border-radius:1.5mm;overflow:hidden}}
.rr-bar-fill{{height:100%;border-radius:1.5mm;background:var(--primary)}}
.rr-dots{{width:100%}}
.rr-dot-row{{display:flex;align-items:center;justify-content:space-between;
  margin-bottom:1.4mm;font-size:calc(8pt * {s})}}
.rr-dot-set{{display:flex;gap:1.2mm}}
.rr-dot-set i{{display:inline-block;width:2.4mm;height:2.4mm;border-radius:50%}}
.rr-rings{{display:flex;flex-wrap:wrap;gap:3mm;justify-content:center}}
.rr-ring-cell{{display:flex;flex-direction:column;align-items:center;gap:.8mm;
  font-size:calc(7pt * {s});text-align:center;width:calc(30% - 2mm)}}
.rr-ring-cell svg{{width:calc(14mm * {s});height:calc(14mm * {s})}}
.rr-chips{{display:flex;flex-wrap:wrap;gap:1.5mm 2mm}}
.rr-chip{{padding:.6mm 2.5mm;border-radius:20px;font-size:calc(7.5pt * {s});
  background:var(--primary);color:var(--on-primary)}}
.rr-radar{{display:block;margin:0 auto}}
.rr-tag-level span{{display:inline-block;margin:.5mm;border-radius:3px;
  padding:.4mm 2mm;background:var(--primary);color:var(--on-primary)}}
.rr-list-skills{{padding-left:4mm;margin:0}}
.rr-list-skills li{{margin-bottom:.8mm;font-size:calc(8pt * {s})}}
.rr-timeline{{border-left:2px solid var(--timeline-line,{primary});
  padding-left:4.5mm;margin-left:1mm}}
.rr-job{{position:relative;margin-bottom:calc(3mm * {s})}}
.rr-job-top{{display:flex;justify-content:space-between;align-items:baseline;gap:2mm}}
.rr-job-role{{font-weight:700;font-size:calc(9pt * {s});color:var(--heading)}}
.rr-job-period{{font-size:calc(7.5pt * {s});color:var(--accent);white-space:nowrap;flex-shrink:0}}
.rr-job-company{{font-size:calc(8pt * {s});color:var(--accent);margin:.5mm 0}}
.rr-job ul{{margin:.8mm 0 0;padding-left:4mm}}
.rr-job li{{font-size:calc(8pt * {s});margin-bottom:.5mm;line-height:1.35}}
.rr-timeline .rr-job::before{{content:"";position:absolute;left:-6.5mm;top:1.2mm;
  width:2.6mm;height:2.6mm;border-radius:50%;background:var(--page-bg);
  border:2px solid var(--primary)}}
.rr-edu{{margin-bottom:calc(2.5mm * {s})}}
.rr-edu-deg{{font-weight:700;font-size:calc(8.5pt * {s});color:var(--heading)}}
.rr-edu-inst{{font-size:calc(8pt * {s});color:var(--accent)}}
.rr-edu-meta{{font-size:calc(7.5pt * {s});color:var(--text);opacity:.8}}
.rr-ct-wrap{{display:flex;flex-direction:column;gap:1.5mm}}
.rr-ct{{display:flex;align-items:center;gap:2mm;font-size:calc(8pt * {s})}}
.rr-ct-ic svg{{flex-shrink:0;width:1em;height:1em}}
.rr-ct-v{{word-break:break-all}}
.rr-bul{{padding-left:4mm;margin:0}}
.rr-bul li{{margin-bottom:.8mm;font-size:calc(8pt * {s})}}
.rr-comp-grid{{display:grid;grid-template-columns:1fr 1fr;gap:2mm 3mm}}
.rr-comp{{display:flex;align-items:flex-start;gap:1.5mm}}
.rr-comp-ic{{flex-shrink:0;width:1.2em;height:1.2em;color:var(--heading)}}
.rr-comp-ic svg{{width:100%;height:100%}}
.rr-comp-t{{font-weight:700;font-size:calc(8pt * {s})}}
.rr-comp-d{{font-size:calc(7.5pt * {s});opacity:.85}}
.rr-hr{{border:none;border-top:1px solid currentColor;margin:2mm 0}}
.rr-vline{{display:inline-block;height:100%;width:1px;background:currentColor}}
ic{{display:inline-block;vertical-align:middle;line-height:0}}
{editor_css}
"""


def _fill_to_css_background(fill: dict | None) -> str:
    """Converts a FILL dict to a CSS background property value string."""
    if not fill or fill.get("type") == "none":
        return "transparent"
    t = fill.get("type", "solid")
    if t == "solid":
        return fill.get("color", "transparent")
    if t == "gradient_linear":
        angle = fill.get("angle_deg", 135)
        stops = fill.get("stops") or []
        stops_css = ", ".join(
            f'{s.get("color","#000")} {s.get("offset_pct",0)}%' for s in stops
        )
        return f"linear-gradient({angle}deg, {stops_css})"
    if t == "gradient_radial":
        cx = fill.get("cx_pct", 50)
        cy = fill.get("cy_pct", 50)
        stops = fill.get("stops") or []
        stops_css = ", ".join(
            f'{s.get("color","#000")} {s.get("offset_pct",0)}%' for s in stops
        )
        return f"radial-gradient(circle at {cx}% {cy}%, {stops_css})"
    return "transparent"


def _fill_to_svg_fill(fill: dict | None) -> tuple[str, str]:
    """
    Returns (fill_attr_value, gradient_defs_html).
    For solid: ('#hex', '')
    For gradient: ('url(#grad_X)', '<defs>...</defs>')
    For none: ('none', '')
    """
    if not fill or fill.get("type") == "none":
        return "none", ""
    t = fill.get("type", "solid")
    if t == "solid":
        return fill.get("color", "#888"), ""
    import hashlib
    gid = "rg_" + hashlib.md5(json.dumps(fill, sort_keys=True).encode()).hexdigest()[:8]
    stops = fill.get("stops") or []
    stop_tags = "".join(
        f'<stop offset="{s.get("offset_pct",0)}%" stop-color="{_e(s.get("color","#000"))}"/>'
        for s in stops
    )
    if t == "gradient_linear":
        angle = fill.get("angle_deg", 135)
        rad = math.radians(angle)
        x1 = 50 - 50 * math.sin(rad)
        y1 = 50 + 50 * math.cos(rad)
        x2 = 50 + 50 * math.sin(rad)
        y2 = 50 - 50 * math.cos(rad)
        defs = (f'<defs><linearGradient id="{gid}" x1="{x1:.1f}%" y1="{y1:.1f}%"'
                f' x2="{x2:.1f}%" y2="{y2:.1f}%">{stop_tags}</linearGradient></defs>')
        return f"url(#{gid})", defs
    if t == "gradient_radial":
        cx = fill.get("cx_pct", 50)
        cy = fill.get("cy_pct", 50)
        defs = (f'<defs><radialGradient id="{gid}" cx="{cx}%" cy="{cy}%" r="50%"'
                f' gradientUnits="userSpaceOnUse">{stop_tags}</radialGradient></defs>')
        return f"url(#{gid})", defs
    return fill.get("color", "#888"), ""


def _text_style_to_css(style: dict) -> str:
    """Converts a TEXT_STYLE dict to a CSS properties string."""
    parts = []
    if style.get("font_family"):
        parts.append(f'font-family:{style["font_family"]}')
    if style.get("font_weight"):
        parts.append(f'font-weight:{style["font_weight"]}')
    if style.get("font_size_pt"):
        parts.append(f'font-size:{style["font_size_pt"]:.2f}pt')
    if style.get("line_height_pt"):
        parts.append(f'line-height:{style["line_height_pt"]:.2f}pt')
    if style.get("letter_spacing_pt") is not None and style["letter_spacing_pt"] != 0:
        parts.append(f'letter-spacing:{style["letter_spacing_pt"]:.3f}pt')
    if style.get("color"):
        parts.append(f'color:{style["color"]}')
    if style.get("text_align"):
        parts.append(f'text-align:{style["text_align"]}')
    tt = style.get("text_transform", "none")
    if tt and tt != "none":
        parts.append(f'text-transform:{tt}')
    return ";".join(parts)


# ════════════════════════════════════════════════════════════════════════════
#  NODE COMPILATION
# ════════════════════════════════════════════════════════════════════════════

def _compile_node(node: dict, content: dict, ctx: dict) -> str:
    """Dispatches to the appropriate node compiler based on node['type']."""
    ntype = (node.get("type") or "").lower()
    if ntype == "frame":
        return _compile_frame(node, content, ctx)
    if ntype == "group":
        return _compile_group(node, content, ctx)
    if ntype == "text":
        return _compile_text(node, content, ctx)
    if ntype == "path":
        return _compile_path(node, ctx)
    if ntype == "image":
        return _compile_image(node, content, ctx)
    if ntype == "repeat":
        return _compile_repeat(node, content, ctx)
    if ntype == "chart":
        return _compile_chart(node, content, ctx)
    if ntype == "rule":
        return _compile_rule(node, ctx)
    # unknown — render children if any
    children = node.get("children") or []
    return "".join(_compile_node(c, content, ctx) for c in children)


def _compile_frame(node: dict, content: dict, ctx: dict) -> str:
    """Compiles a FRAME node to a <div> element."""
    layout_mode  = node.get("layout_mode", "flow")
    page_spanning= node.get("page_spanning", False)
    fill         = node.get("fill")
    padding      = node.get("padding") or {}
    width_mm     = node.get("width_mm")
    width_pct    = node.get("width_pct")
    height_mm    = node.get("height_mm")
    height_pct   = node.get("height_pct")
    classes      = node.get("classes") or []
    node_id      = node.get("id", "")
    extra_css    = node.get("css") or ""

    style_parts = []

    # Position / layout
    if page_spanning:
        style_parts.append("position:fixed;inset:0;z-index:0")
    elif layout_mode == "absolute":
        style_parts.append("position:absolute")
        if node.get("top_mm") is not None:
            style_parts.append(f'top:{node["top_mm"]}mm')
        if node.get("left_mm") is not None:
            style_parts.append(f'left:{node["left_mm"]}mm')
        if node.get("right_mm") is not None:
            style_parts.append(f'right:{node["right_mm"]}mm')
        if node.get("bottom_mm") is not None:
            style_parts.append(f'bottom:{node["bottom_mm"]}mm')
    elif layout_mode == "flex_row":
        style_parts.append("display:flex;flex-direction:row")
        gap = node.get("gap_mm")
        if gap is not None:
            style_parts.append(f"gap:{gap}mm")
        align = node.get("align_items")
        if align:
            style_parts.append(f"align-items:{align}")
        justify = node.get("justify_content")
        if justify:
            style_parts.append(f"justify-content:{justify}")
    elif layout_mode == "flex_col":
        style_parts.append("display:flex;flex-direction:column")
        gap = node.get("gap_mm")
        if gap is not None:
            style_parts.append(f"gap:{gap}mm")
    else:
        style_parts.append("display:block")

    # Size
    if width_mm is not None:
        style_parts.append(f"width:{width_mm}mm")
    elif width_pct is not None:
        style_parts.append(f"width:{width_pct}%")
    if height_mm is not None:
        style_parts.append(f"height:{height_mm}mm")
    elif height_pct is not None:
        style_parts.append(f"height:{height_pct}%")
    if node.get("min_height_mm") is not None:
        style_parts.append(f'min-height:{node["min_height_mm"]}mm')
    if node.get("flex"):
        style_parts.append(f'flex:{node["flex"]}')

    # Padding
    if padding:
        pt = padding.get("top", 0)
        pr = padding.get("right", 0)
        pb = padding.get("bottom", 0)
        pl = padding.get("left", 0)
        style_parts.append(f"padding:{pt}mm {pr}mm {pb}mm {pl}mm")

    # Fill → background
    if fill:
        bg = _fill_to_css_background(fill)
        if bg and bg != "transparent":
            style_parts.append(f"background:{bg}")

    if node.get("overflow_hidden"):
        style_parts.append("overflow:hidden")
    if node.get("position_relative"):
        style_parts.append("position:relative")
    if extra_css:
        style_parts.append(extra_css)

    cls_str = " ".join(classes)
    style_str = ";".join(style_parts)
    id_attr = f' id="{_e(node_id)}"' if node_id else ""
    children_html = "".join(_compile_node(c, content, ctx) for c in (node.get("children") or []))

    return (f'<div{id_attr} class="{_e(cls_str)}"'
            f'{" style=\"" + style_str + "\"" if style_str else ""}>'
            f'{children_html}</div>')


def _compile_group(node: dict, content: dict, ctx: dict) -> str:
    """Compiles a GROUP node to a <div>. Used for section headings and composites."""
    classes = list(node.get("classes") or [])
    is_heading_group = node.get("is_heading_group", False)
    if is_heading_group:
        classes.append("rr-heading-group")

    style_parts = []
    if node.get("position_relative") or is_heading_group:
        style_parts.append("position:relative")
    padding = node.get("padding") or {}
    if padding:
        pt = padding.get("top", 0)
        pr = padding.get("right", 0)
        pb = padding.get("bottom", 0)
        pl = padding.get("left", 0)
        style_parts.append(f"padding:{pt}mm {pr}mm {pb}mm {pl}mm")
    if node.get("margin_bottom_mm") is not None:
        style_parts.append(f'margin-bottom:{node["margin_bottom_mm"]}mm')
    extra = node.get("css") or ""
    if extra:
        style_parts.append(extra)

    cls_str = " ".join(classes)
    style_str = ";".join(style_parts)
    children_html = "".join(_compile_node(c, content, ctx) for c in (node.get("children") or []))
    return (f'<div class="{_e(cls_str)}"'
            f'{" style=\"" + style_str + "\"" if style_str else ""}>'
            f'{children_html}</div>')


def _compile_text(node: dict, content: dict, ctx: dict) -> str:
    """Compiles a TEXT node, optionally binding to content and supporting edit mode."""
    binding    = node.get("binding") or ""
    style_ref  = node.get("style_ref") or ""
    inline_style = node.get("style") or {}
    tag        = node.get("tag", "span")       # span | div | p | h1 | h2 | h3
    static_val = node.get("value") or ""
    classes    = node.get("classes") or []

    # Resolve text style
    text_style: dict = {}
    sr = ctx.get("style_registry") or {}
    if style_ref and style_ref in sr:
        text_style = sr[style_ref]
    if inline_style:
        text_style = {**text_style, **inline_style}

    # Resolve value from binding
    if binding:
        value = _resolve_binding(binding, content)
        if isinstance(value, list):
            value = " ".join(str(v) for v in value)
        value = str(value or "")
    else:
        value = static_val

    # text_transform
    tt = text_style.get("text_transform", "none")
    if tt == "uppercase":
        display_value = value.upper()
    elif tt == "capitalize":
        display_value = value.title()
    else:
        display_value = value

    # Edit mode wrapping
    if binding and ctx.get("edit"):
        inner = _ef(binding, value, value, ctx)
    else:
        inner = _e(display_value)

    css = _text_style_to_css(text_style)
    cls_str = " ".join(classes)
    style_attr = f' style="{css}"' if css else ""
    class_attr = f' class="{_e(cls_str)}"' if cls_str else ""
    return f"<{tag}{class_attr}{style_attr}>{inner}</{tag}>"


def _resolve_binding(binding: str, content: dict):
    """Walks a dot-path binding into content dict. Returns '' if not found."""
    parts = binding.split(".")
    cur = content
    for part in parts:
        if isinstance(cur, dict):
            cur = cur.get(part)
        elif isinstance(cur, list):
            try:
                cur = cur[int(part)]
            except (ValueError, IndexError):
                return ""
        else:
            return ""
        if cur is None:
            return ""
    return cur


def _compile_path(node: dict, ctx: dict) -> str:
    """Compiles a PATH node to an inline SVG element."""
    geom    = node.get("geometry") or {}
    fill    = node.get("fill")
    stroke  = node.get("stroke") or {}
    classes = list(node.get("classes") or [])
    classes.append("rr-path")
    width_mm  = node.get("width_mm")
    height_mm = node.get("height_mm")

    # Resolve d-string and viewBox
    if geom.get("type") == "commands":
        d_str = _commands_to_d(geom.get("commands") or [])
        vb = geom.get("viewBox") or [0, 0, 100, 100]
    elif geom.get("type") == "parametric":
        d_str, vb = _parametric_to_commands(geom)
    else:
        d_str, vb = "", [0, 0, 100, 100]

    vb_str = " ".join(str(v) for v in vb)
    fill_val, grad_defs = _fill_to_svg_fill(fill)

    stroke_attr = ""
    if stroke.get("color"):
        sw = stroke.get("width_pt", 1)
        stroke_attr = f' stroke="{_e(stroke["color"])}" stroke-width="{sw}"'
    else:
        stroke_attr = ' stroke="none"'

    style_parts = []
    if width_mm:
        style_parts.append(f"width:{width_mm}mm")
    if height_mm:
        style_parts.append(f"height:{height_mm}mm")
    style_str = ";".join(style_parts)
    style_attr = f' style="{style_str}"' if style_str else ""

    cls_str = " ".join(classes)
    path_tag = (f'<path d="{_e(d_str)}" fill="{_e(fill_val)}"{stroke_attr}/>'
                if d_str else "")

    return (f'<svg class="{_e(cls_str)}" viewBox="{vb_str}" xmlns="http://www.w3.org/2000/svg"'
            f' preserveAspectRatio="none"{style_attr}>'
            f'{grad_defs}{path_tag}</svg>')


def _parametric_to_commands(geom: dict) -> tuple[str, list]:
    """Converts parametric geometry dict to (d_string, view_box)."""
    pt    = geom.get("parametric_type", "rect")
    p     = geom.get("params") or {}
    w     = float(p.get("width", 100))
    h     = float(p.get("height", 100))

    if pt == "angled_rect":
        slant = float(p.get("slant", 20))
        direction = p.get("direction", "right")
        if direction == "right":
            # right edge slants: top-right to bottom-right goes left by slant
            d = f"M0,0 L{w},0 L{w - slant},{h} L0,{h} Z"
        else:
            # left edge: bottom-left is offset right by slant
            d = f"M0,0 L{w},0 L{w},{h} L{slant},{h} Z"
        return d, [0, 0, w, h]

    if pt == "parallelogram":
        slant = float(p.get("slant", 20))
        d = f"M{slant},0 L{w},0 L{w - slant},{h} L0,{h} Z"
        return d, [0, 0, w, h]

    if pt == "wave":
        amplitude = float(p.get("amplitude", h * 0.25))
        # Generate a wave as cubic bezier bottom edge
        c1x = w * 0.3
        c1y = h + amplitude
        c2x = w * 0.7
        c2y = h - amplitude
        d = f"M0,0 L{w},0 L{w},{h} C{c2x},{c2y} {c1x},{c1y} 0,{h} Z"
        return d, [0, 0, w, h]

    if pt == "diagonal_split":
        split_x = float(p.get("split_x", w * 0.6))
        d = f"M0,0 L{w},0 L{split_x},{h} L0,{h} Z"
        return d, [0, 0, w, h]

    if pt == "rect":
        rx = float(p.get("rx", 0))
        if rx:
            d = (f"M{rx},0 L{w - rx},0 Q{w},0 {w},{rx} "
                 f"L{w},{h - rx} Q{w},{h} {w - rx},{h} "
                 f"L{rx},{h} Q0,{h} 0,{h - rx} "
                 f"L0,{rx} Q0,0 {rx},0 Z")
        else:
            d = f"M0,0 L{w},0 L{w},{h} L0,{h} Z"
        return d, [0, 0, w, h]

    # fallback: full rect
    d = f"M0,0 L{w},0 L{w},{h} L0,{h} Z"
    return d, [0, 0, w, h]


def _compile_image(node: dict, content: dict, ctx: dict) -> str:
    """Compiles an IMAGE node to a div with background-image (or initials block)."""
    binding    = node.get("binding") or ""
    clip_shape = node.get("clip_shape", "circle")
    width_mm   = node.get("width_mm", 30)
    height_mm  = node.get("height_mm", 30)
    ring       = node.get("ring", False)
    ring_color = node.get("ring_color") or "var(--primary)"
    classes    = list(node.get("classes") or [])

    photo_uri = ctx.get("photo_uri") or ""

    # Determine which image source to use
    if binding == "photo":
        src = photo_uri
    else:
        resolved = _resolve_binding(binding, content) if binding else ""
        src = str(resolved) if resolved else ""

    # Clip shape CSS class
    shape_cls = f"rr-photo-{clip_shape}" if clip_shape != "none" else ""
    classes.append("rr-photo")
    if shape_cls:
        classes.append(shape_cls)

    style_parts = [
        f"width:{width_mm}mm",
        f"height:{height_mm}mm",
        "flex-shrink:0",
    ]
    if ring:
        style_parts.append(
            f"box-shadow:0 0 0 1.6mm var(--page-bg,#fff),0 0 0 3mm {ring_color}"
        )

    if src:
        style_parts.append(f"background-image:url('{src}')")
        cls_str = " ".join(classes)
        style_str = ";".join(style_parts)
        return f'<div class="{_e(cls_str)}" style="{style_str}"></div>'
    else:
        # Render initials block
        name = content.get("name") or ""
        color = node.get("initials_color") or "var(--primary)"
        classes.append("rr-photo-empty")
        cls_str = " ".join(classes)
        style_parts.append(f"background:{color};color:#fff;font-weight:700;font-size:{width_mm * 0.3:.1f}mm")
        style_str = ";".join(style_parts)
        initials = _initials_block(name, color, width_mm)
        return f'<div class="{_e(cls_str)}" style="{style_str}">{initials}</div>'


def _compile_rule(node: dict, ctx: dict) -> str:
    """Compiles a RULE node to an <hr> or vertical div."""
    direction = node.get("direction", "horizontal")
    color     = node.get("color") or "currentColor"
    thickness = node.get("thickness_pt", 1)
    length    = node.get("length_pct", 100)
    margin    = node.get("margin_mm", 2)

    if direction == "vertical":
        return (f'<div style="display:inline-block;width:{thickness}pt;height:100%;'
                f'background:{_e(color)};margin:0 {margin}mm;vertical-align:middle"></div>')
    # horizontal
    return (f'<hr class="rr-hr" style="border-top:{thickness}pt solid {_e(color)};'
            f'width:{length}%;margin:{margin}mm auto">')


def _compile_repeat(node: dict, content: dict, ctx: dict) -> str:
    """Compiles a REPEAT node by iterating content[binding] and rendering items."""
    binding       = node.get("binding") or ""
    template      = node.get("component_template") or {}
    style_registry= ctx.get("style_registry") or {}
    design        = ctx.get("design") or {}
    has_timeline  = design.get("timeline", False)
    parts         = []

    items = content.get(binding) if binding else []
    if not items:
        return ""

    if binding == "experience":
        for i, item in enumerate(items):
            parts.append(_render_experience_item(item, i, style_registry, has_timeline, ctx))
    elif binding == "education":
        for i, item in enumerate(items):
            parts.append(_render_education_item(item, i, style_registry, ctx))
    elif binding == "projects":
        for i, item in enumerate(items):
            parts.append(_render_project_item(item, i, style_registry, has_timeline, ctx))
    elif binding == "competencies":
        for i, item in enumerate(items):
            parts.append(_render_competency_item(item, i, ctx))
    elif binding == "contact":
        ct = content.get("contact") or {}
        parts.append(_render_contact_section(ct, ctx))
    elif binding == "languages":
        for i, item in enumerate(items):
            name_val = _ef(f"languages.{i}.name", item.get("name",""), "language", ctx)
            lvl = item.get("level", 3)
            dots_html = "".join(
                f'<i style="background:var(--{"primary" if k < lvl else "track"});'
                f'display:inline-block;width:2.4mm;height:2.4mm;border-radius:50%;margin-right:.5mm"></i>'
                for k in range(5)
            )
            parts.append(
                f'<div class="rr-dot-row"{_it(f"languages.{i}")}>'
                f'<span>{name_val}</span>'
                f'<span class="rr-dot-set">{dots_html}</span></div>'
            )
    else:
        # Generic list rendering
        for i, item in enumerate(items):
            if isinstance(item, dict):
                text = item.get("name") or item.get("title") or item.get("text") or str(item)
            else:
                text = str(item)
            parts.append(
                f'<li{_it(f"{binding}.{i}")}>{_ef(f"{binding}.{i}", text, "item", ctx)}</li>'
            )
        if parts:
            return '<ul class="rr-bul">' + "".join(parts) + "</ul>"
        return ""

    container_cls = "rr-timeline" if (has_timeline and binding in ("experience", "projects")) else "rr-jobs"
    return f'<div class="{container_cls}">' + "".join(parts) + "</div>"


def _compile_chart(node: dict, content: dict, ctx: dict) -> str:
    """Compiles a CHART node to the appropriate skill/language visualisation."""
    chart_type  = node.get("chart_type", "bars")
    data_binding= node.get("data_binding") or "skills"
    colors_node = node.get("colors") or []
    track_color = node.get("track_color") or "var(--track)"
    columns     = node.get("columns", 1)
    size_mm     = node.get("size_mm", 50.0)

    # Resolve data
    items = content.get(data_binding) or []
    if not items and data_binding == "additional_skills":
        items = content.get("additional_skills") or []

    # Normalise colors
    design  = ctx.get("design") or {}
    c_colors= (design.get("colors") or {}).get("skill_colors") or ["#2563eb","#1e40af","#93c5fd"]
    colors  = colors_node if colors_node else c_colors

    if chart_type == "bars":
        return _render_bars(items, colors, track_color, columns, ctx)
    if chart_type == "dots":
        return _render_dots(items, colors, track_color, ctx)
    if chart_type == "rings":
        return _render_rings(items, colors, track_color, ctx)
    if chart_type == "venn":
        return _render_venn(items, colors, ctx)
    if chart_type == "chips":
        return _render_chips(items, ctx)
    if chart_type == "radar":
        return _render_radar(items, colors, size_mm)
    if chart_type == "tag_level":
        return _render_tag_level(items, colors, ctx)
    if chart_type == "list":
        return _render_list_skills(items, ctx)
    return _render_chips(items, ctx)


# ════════════════════════════════════════════════════════════════════════════
#  CHART RENDERERS
# ════════════════════════════════════════════════════════════════════════════

def _render_bars(skills: list, colors: list, track_color: str, columns: int, ctx: dict) -> str:
    """Progress bar skills. Supports 2-column CSS grid."""
    if not skills:
        return ""
    fg = colors[0] if colors else "var(--primary)"
    rows = []
    for i, s in enumerate(skills):
        if isinstance(s, dict):
            name = s.get("name", "")
            level = s.get("level", 80)
        else:
            name = str(s)
            level = 80
        name_html = _ef(f"skills.{i}.name", name, "skill", ctx)
        rows.append(
            f'<div class="rr-bar-row"{_it(f"skills.{i}")}>'
            f'<div class="rr-bar-label">{name_html}</div>'
            f'<div class="rr-bar-track" style="background:{_e(track_color)}">'
            f'<div class="rr-bar-fill" style="width:{level}%;background:{_e(fg)}"></div>'
            f'</div></div>'
        )
    grid_style = f'display:grid;grid-template-columns:1fr 1fr;gap:0 3mm' if columns >= 2 else ""
    style_attr = f' style="{grid_style}"' if grid_style else ""
    return f'<div class="rr-bars"{style_attr}>{"".join(rows)}</div>'


def _render_dots(skills: list, colors: list, track_color: str, ctx: dict) -> str:
    """5-dot rating skills."""
    if not skills:
        return ""
    fg = colors[0] if colors else "var(--primary)"
    rows = []
    for i, s in enumerate(skills):
        if isinstance(s, dict):
            name = s.get("name", "")
            level = s.get("level", 80)
        else:
            name = str(s)
            level = 80
        filled = round(level / 20)
        name_html = _ef(f"skills.{i}.name", name, "skill", ctx)
        dot_html = "".join(
            f'<i style="display:inline-block;width:2.4mm;height:2.4mm;border-radius:50%;'
            f'background:{_e(fg) if k < filled else _e(track_color)};margin-right:.5mm"></i>'
            for k in range(5)
        )
        rows.append(
            f'<div class="rr-dot-row"{_it(f"skills.{i}")}>'
            f'<span>{name_html}</span>'
            f'<span class="rr-dot-set">{dot_html}</span>'
            f'</div>'
        )
    return f'<div class="rr-dots">{"".join(rows)}</div>'


def _render_rings(skills: list, colors: list, track_color: str, ctx: dict) -> str:
    """Ring/donut chart skills (up to 9, max 3 per row)."""
    if not skills:
        return ""
    col = colors[0] if colors else "var(--primary)"
    track = track_color if track_color else "var(--track)"
    cells = []
    for i, s in enumerate(skills[:9]):
        if isinstance(s, dict):
            name = s.get("name", "")
            level = s.get("level", 80)
        else:
            name = str(s)
            level = 80
        ring_svg = _ring_svg(level, col, track)
        name_html = _ef(f"skills.{i}.name", name, "skill", ctx)
        cells.append(
            f'<div class="rr-ring-cell"{_it(f"skills.{i}")}>'
            f'{ring_svg}<div>{name_html}</div></div>'
        )
    return f'<div class="rr-rings">{"".join(cells)}</div>'


def _render_venn(skills: list, colors: list, ctx: dict) -> str:
    """3-circle Venn diagram using the first 3 skills."""
    top = []
    for s in skills[:3]:
        top.append(s.get("name", str(s)) if isinstance(s, dict) else str(s))
    n = len(top)
    if not n:
        return ""
    r, cy = 78, 88
    centers_map = {1: [180], 2: [135, 225], 3: [100, 180, 260]}
    offsets_map  = {1: [0],  2: [-22, 22],  3: [-26, 0, 26]}
    centers = centers_map[n]
    offsets = offsets_map[n]
    all_colors = (colors + ["#2563eb", "#0f766e", "#ea580c"])[:3]
    circles, labels = [], []
    for i, (cx, label) in enumerate(zip(centers, top)):
        col = all_colors[i % len(all_colors)]
        circles.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{_e(col)}" fill-opacity="0.82"/>')
        txt = label.upper()
        width = 92 if n == 3 else 120
        fs = max(8.5, min(15.0, width / (0.66 * max(len(txt), 1))))
        labels.append(
            f'<text x="{cx + offsets[i]}" y="{cy + fs * 0.35:.1f}" text-anchor="middle" '
            f'font-size="{fs:.1f}" font-weight="700" fill="#ffffff" letter-spacing="0.4">'
            f'{_e(txt)}</text>'
        )
    return (
        f'<svg class="rr-venn" viewBox="0 0 360 176" xmlns="http://www.w3.org/2000/svg">'
        f'{"".join(circles)}{"".join(labels)}</svg>'
    )


def _render_chips(items: list, ctx: dict) -> str:
    """Chip/tag style. Items can be skill dicts or strings."""
    if not items:
        return ""
    chips = []
    for i, item in enumerate(items):
        if isinstance(item, dict):
            name = item.get("name") or item.get("title") or str(item)
            path = f"skills.{i}.name"
        else:
            name = str(item)
            path = f"skills.{i}"
        chips.append(
            f'<span class="rr-chip"{_it(path)}>{_ef(path, name, "skill", ctx)}</span>'
        )
    return f'<div class="rr-chips">{"".join(chips)}</div>'


def _render_radar(skills: list, colors: list, size_mm: float = 50.0) -> str:
    """
    Radar/spider chart as inline SVG.
    100x100 viewBox, center (50,50), max radius 38.
    Grid: 4 concentric polygons. Axis lines. Filled data polygon. Labels outside.
    """
    if not skills:
        return ""
    n = len(skills)
    if n < 3:
        # Pad to 3 for a valid polygon
        skills = list(skills) + [{"name": "", "level": 0}] * (3 - n)
        n = 3

    cx, cy, max_r = 50.0, 50.0, 38.0
    fill_color = colors[0] if colors else "#2563eb"
    stroke_color = colors[1] if len(colors) > 1 else fill_color

    def vertex(i: int, r: float):
        angle = math.radians(90 + 360 * i / n)
        return cx + r * math.cos(angle), cy - r * math.sin(angle)

    # Grid polygons (25%, 50%, 75%, 100%)
    grid_polys = []
    for pct in (0.25, 0.50, 0.75, 1.0):
        pts = " ".join(f"{vertex(i, max_r * pct)[0]:.2f},{vertex(i, max_r * pct)[1]:.2f}"
                       for i in range(n))
        grid_polys.append(
            f'<polygon points="{pts}" fill="none" stroke="#ccc" stroke-width="0.5"/>'
        )

    # Axis lines
    axes = []
    for i in range(n):
        x, y = vertex(i, max_r)
        axes.append(f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{x:.2f}" y2="{y:.2f}" stroke="#ccc" stroke-width="0.5"/>')

    # Data polygon
    def _safe_level(s):
        if isinstance(s, dict):
            return max(0, min(100, int(s.get("level", 80))))
        return 80

    data_pts = " ".join(
        f"{vertex(i, max_r * _safe_level(s) / 100)[0]:.2f},{vertex(i, max_r * _safe_level(s) / 100)[1]:.2f}"
        for i, s in enumerate(skills)
    )
    data_poly = (
        f'<polygon points="{data_pts}" fill="{_e(fill_color)}" fill-opacity="0.35" '
        f'stroke="{_e(stroke_color)}" stroke-width="1.5"/>'
    )

    # Labels
    label_tags = []
    for i, s in enumerate(skills):
        name = s.get("name", "") if isinstance(s, dict) else str(s)
        if not name:
            continue
        lx, ly = vertex(i, max_r + 8)
        anchor = "middle"
        if lx < cx - 2:
            anchor = "end"
        elif lx > cx + 2:
            anchor = "start"
        label_tags.append(
            f'<text x="{lx:.2f}" y="{ly:.2f}" text-anchor="{anchor}" '
            f'font-size="5.5" fill="#555">{_e(name)}</text>'
        )

    size_style = f'width:{size_mm}mm;height:{size_mm}mm'
    return (
        f'<svg class="rr-radar" viewBox="0 0 100 100" '
        f'xmlns="http://www.w3.org/2000/svg" style="{size_style}">'
        f'{"".join(grid_polys)}{"".join(axes)}{data_poly}{"".join(label_tags)}'
        f'</svg>'
    )


def _render_tag_level(skills: list, colors: list, ctx: dict) -> str:
    """Tags where size/opacity indicates level (higher → larger/more saturated)."""
    if not skills:
        return ""
    base_col = colors[0] if colors else "#2563eb"
    tags = []
    for i, s in enumerate(skills):
        if isinstance(s, dict):
            name = s.get("name", "")
            level = s.get("level", 80)
        else:
            name = str(s)
            level = 80
        # Scale font 7pt–10pt based on level
        fs = 7.0 + (level / 100) * 3.0
        opacity = 0.55 + (level / 100) * 0.45
        path = f"skills.{i}.name"
        tags.append(
            f'<span style="font-size:{fs:.1f}pt;background:{_e(base_col)};'
            f'opacity:{opacity:.2f};color:#fff;padding:.5mm 2.5mm;border-radius:3px;'
            f'margin:.5mm;display:inline-block"{_it(path)}>'
            f'{_ef(path, name, "skill", ctx)}</span>'
        )
    return f'<div class="rr-tag-level">{"".join(tags)}</div>'


def _render_list_skills(skills: list, ctx: dict) -> str:
    """Simple <ul><li> list of skill names."""
    if not skills:
        return ""
    items = []
    for i, s in enumerate(skills):
        name = s.get("name", "") if isinstance(s, dict) else str(s)
        path = f"skills.{i}.name" if isinstance(s, dict) else f"skills.{i}"
        items.append(f'<li{_it(f"skills.{i}")}>{_ef(path, name, "skill", ctx)}</li>')
    return f'<ul class="rr-list-skills">{"".join(items)}</ul>'


# ════════════════════════════════════════════════════════════════════════════
#  CONTENT SECTION RENDERERS
# ════════════════════════════════════════════════════════════════════════════

def _render_experience_item(
    item: dict, idx: int, style_registry: dict, has_timeline: bool, ctx: dict
) -> str:
    """Renders a single experience entry (same format as legacy builder's _experience_html)."""
    p = f"experience.{idx}"
    edit = ctx.get("edit", False)

    role    = item.get("role", "")
    company = item.get("company", "")
    period  = item.get("period", "")
    location= item.get("location", "")
    bullets = item.get("bullets") or []

    role_html   = _ef(f"{p}.role", role, "role", ctx)
    period_html = _ef(f"{p}.period", period, "period", ctx)

    if edit:
        sub = (_ef(f"{p}.company", company, "company", ctx) +
               " · " + _ef(f"{p}.location", location, "location", ctx))
    else:
        sub_parts = [v for v in (company, location) if v]
        sub = " · ".join(_e(v) for v in sub_parts)

    co_html = f'<div class="rr-job-company">{sub}</div>' if (sub and (role or edit)) else ""
    bullet_items = "".join(
        f'<li{_it(f"{p}.bullets.{j}")}>{_ef(f"{p}.bullets.{j}", b, "achievement", ctx)}</li>'
        for j, b in enumerate(bullets)
    )
    ul_html = f"<ul>{bullet_items}</ul>" if bullet_items else ""

    return (
        f'<div class="rr-job"{_it(p)}>'
        f'<div class="rr-job-top">'
        f'<div class="rr-job-role">{role_html}</div>'
        f'<div class="rr-job-period">{period_html}</div>'
        f'</div>'
        f'{co_html}{ul_html}'
        f'</div>'
    )


def _render_education_item(
    item: dict, idx: int, style_registry: dict, ctx: dict
) -> str:
    """Renders a single education entry."""
    p      = f"education.{idx}"
    edit   = ctx.get("edit", False)
    degree = item.get("degree", "")
    inst   = item.get("institution", "")
    period = item.get("period", "")
    details= item.get("details", "")

    parts = [f'<div class="rr-edu-deg">{_ef(f"{p}.degree", degree, "degree", ctx)}</div>']
    if inst or edit:
        parts.append(f'<div class="rr-edu-inst">{_ef(f"{p}.institution", inst, "institution", ctx)}</div>')
    meta_parts = []
    if period or edit:
        meta_parts.append(_ef(f"{p}.period", period, "period", ctx))
    if details or edit:
        meta_parts.append(_ef(f"{p}.details", details, "details", ctx))
    if meta_parts:
        parts.append(f'<div class="rr-edu-meta">{"<span>·</span>".join(meta_parts)}</div>')

    return f'<div class="rr-edu"{_it(p)}>{"".join(parts)}</div>'


def _render_project_item(
    item: dict, idx: int, style_registry: dict, has_timeline: bool, ctx: dict
) -> str:
    """Renders a single project entry (same format as legacy builder's _projects_html)."""
    p = f"projects.{idx}"
    edit = ctx.get("edit", False)

    name    = item.get("name", "")
    tech    = item.get("tech", "")
    period  = item.get("period", "")
    bullets = item.get("bullets") or []
    description = item.get("description", "")

    rich = bool(bullets or tech)
    if not rich:
        desc_html = (f'<div>{_ef(f"{p}.description", description, "description", ctx)}</div>'
                     if (description or edit) else "")
        return (f'<div class="rr-job"{_it(p)}>'
                f'<b>{_ef(f"{p}.name", name, "project", ctx)}</b>{desc_html}</div>')

    tech_html = (f'<div class="rr-job-company">{_ef(f"{p}.tech", tech, "tech stack", ctx)}</div>'
                 if (tech or edit) else "")
    desc_html = (f'<div style="font-style:italic;font-size:.9em">'
                 f'{_ef(f"{p}.description", description, "description", ctx)}</div>'
                 if description else "")
    bullet_items = "".join(
        f'<li{_it(f"{p}.bullets.{j}")}>{_ef(f"{p}.bullets.{j}", b, "point", ctx)}</li>'
        for j, b in enumerate(bullets)
    )
    ul_html = f"<ul>{bullet_items}</ul>" if bullet_items else ""

    return (
        f'<div class="rr-job"{_it(p)}>'
        f'<div class="rr-job-top">'
        f'<div class="rr-job-role">{_ef(f"{p}.name", name, "project", ctx)}</div>'
        f'<div class="rr-job-period">{_ef(f"{p}.period", period, "period", ctx)}</div>'
        f'</div>'
        f'{tech_html}{desc_html}{ul_html}'
        f'</div>'
    )


def _render_competency_item(item: dict, idx: int, ctx: dict) -> str:
    """Renders a single competency as an icon+title+description card."""
    p    = f"competencies.{idx}"
    title= item.get("title", "")
    desc = item.get("description", "")
    icon = item.get("icon") or _guess_icon(title)

    icon_svg = _icon_svg(icon, "var(--heading)")
    return (
        f'<div class="rr-comp"{_it(p)}>'
        f'<div class="rr-comp-ic">{icon_svg}</div>'
        f'<div>'
        f'<div class="rr-comp-t">{_ef(f"{p}.title", title, "title", ctx)}</div>'
        f'<div class="rr-comp-d">{_ef(f"{p}.description", desc, "description", ctx)}</div>'
        f'</div></div>'
    )


def _render_contact_section(contact: dict, ctx: dict) -> str:
    """Renders the contact section with icons."""
    fields = [
        ("phone",    "phone"),
        ("email",    "mail"),
        ("location", "pin"),
        ("linkedin", "linkedin"),
        ("website",  "link"),
    ]
    edit = ctx.get("edit", False)
    rows = []
    for key, icon in fields:
        val = contact.get(key, "")
        if not val and not edit:
            continue
        ic_html = _icon_svg(icon, "var(--heading)", "1em")
        rows.append(
            f'<div class="rr-ct">'
            f'<span class="rr-ct-ic">{ic_html}</span>'
            f'<span class="rr-ct-v">{_ef(f"contact.{key}", val, key, ctx)}</span>'
            f'</div>'
        )
    if not rows:
        return ""
    return f'<div class="rr-ct-wrap">{"".join(rows)}</div>'


# ════════════════════════════════════════════════════════════════════════════
#  SECTION COMPILER (high-level)
# ════════════════════════════════════════════════════════════════════════════

def _compile_section(
    key: str,
    content: dict,
    heading_node: dict | None,
    chart_type: str | None,
    style_registry: dict,
    design: dict,
    ctx: dict,
) -> str:
    """
    High-level section renderer.
    Returns complete HTML for the section (heading + content), or '' if no data.
    """
    # Resolve section title
    title_text = (
        (design.get("section_titles") or {}).get(key)
        or _DEFAULT_TITLES.get(key, key.title())
    )

    # Generate content HTML
    has_timeline = design.get("timeline", False)

    if key == "profile":
        paras = content.get("profile") or []
        if not paras and not ctx.get("edit"):
            return ""
        inner = "".join(
            f'<p{_it(f"profile.{i}")}>{_ef(f"profile.{i}", p, "profile paragraph", ctx)}</p>'
            for i, p in enumerate(paras)
        )
    elif key == "contact":
        inner = _render_contact_section(content.get("contact") or {}, ctx)
    elif key == "skills":
        skills = content.get("skills") or []
        extra  = content.get("additional_skills") or []
        if not skills and not extra:
            return ""
        cols = design.get("skills_columns", 1)
        sty  = chart_type or design.get("skills_style", "bars")
        if sty == "bars":
            inner = _render_bars(skills, _skill_colors(design), "var(--track)", cols, ctx)
        elif sty == "dots":
            inner = _render_dots(skills, _skill_colors(design), "var(--track)", ctx)
        elif sty in ("circles", "rings"):
            inner = _render_rings(skills, _skill_colors(design), "var(--track)", ctx)
        elif sty == "venn":
            inner = _render_venn(skills, _skill_colors(design), ctx)
        elif sty == "list":
            inner = _render_list_skills(skills, ctx)
        else:
            inner = _render_chips(skills, ctx)
        if extra:
            chips = _render_chips([{"name": x} for x in extra], ctx)
            inner += f'<div style="margin-top:1.5mm">{chips}</div>'
    elif key == "languages":
        langs = content.get("languages") or []
        if not langs:
            return ""
        lang_style = design.get("language_style", "dots")
        if lang_style == "bars":
            inner = _render_bars(
                [{"name": l["name"], "level": l.get("level", 4) * 20} for l in langs],
                _skill_colors(design), "var(--track)", 1, ctx
            )
        elif lang_style == "text":
            words = {5:"Native / Fluent", 4:"Professional", 3:"Intermediate", 2:"Basic", 1:"Beginner"}
            inner = "".join(
                f'<div{_it(f"languages.{i}")}>'
                f'<b>{_ef(f"languages.{i}.name", l["name"], "language", ctx)}</b>'
                f' — {words.get(l.get("level",4),"")}</div>'
                for i, l in enumerate(langs)
            )
        else:
            inner = _render_dots(
                [{"name": l["name"], "level": l.get("level", 4) * 20} for l in langs],
                _skill_colors(design), "var(--track)", ctx
            )
    elif key == "competencies":
        items = content.get("competencies") or []
        if not items:
            return ""
        cells = [_render_competency_item(it, i, ctx) for i, it in enumerate(items)]
        comp_style = design.get("competency_style", "icon_grid")
        if comp_style == "list":
            rows = []
            for i, x in enumerate(items):
                desc = (f' — {_ef(f"competencies.{i}.description", x.get("description",""), "description", ctx)}'
                        if x.get("description") or ctx.get("edit") else "")
                rows.append(
                    f'<li{_it(f"competencies.{i}")}>'
                    f'<b>{_ef(f"competencies.{i}.title", x.get("title",""), "title", ctx)}</b>{desc}</li>'
                )
            inner = f'<ul class="rr-bul">{"".join(rows)}</ul>'
        else:
            inner = f'<div class="rr-comp-grid">{"".join(cells)}</div>'
    elif key == "experience":
        items = content.get("experience") or []
        if not items:
            return ""
        rendered = [_render_experience_item(it, i, style_registry, has_timeline, ctx) for i, it in enumerate(items)]
        cls = "rr-timeline" if has_timeline else "rr-jobs"
        inner = f'<div class="{cls}">{"".join(rendered)}</div>'
    elif key == "projects":
        items = content.get("projects") or []
        if not items:
            return ""
        rendered = [_render_project_item(it, i, style_registry, has_timeline, ctx) for i, it in enumerate(items)]
        cls = "rr-timeline" if has_timeline else "rr-jobs"
        inner = f'<div class="{cls}">{"".join(rendered)}</div>'
    elif key == "education":
        items = content.get("education") or []
        if not items:
            return ""
        inner = "".join(_render_education_item(it, i, style_registry, ctx) for i, it in enumerate(items))
    elif key == "highlights":
        items = content.get("highlights") or []
        if not items:
            return ""
        inner = ('<ul class="rr-bul">' +
                 "".join(f'<li{_it(f"highlights.{i}")}>{_ef(f"highlights.{i}", x, "highlight", ctx)}</li>'
                         for i, x in enumerate(items)) + "</ul>")
    elif key == "achievements":
        items = content.get("achievements") or []
        if not items:
            return ""
        inner = ('<ul class="rr-bul">' +
                 "".join(f'<li{_it(f"achievements.{i}")}>{_ef(f"achievements.{i}", x, "achievement", ctx)}</li>'
                         for i, x in enumerate(items)) + "</ul>")
    elif key == "certifications":
        items = content.get("certifications") or []
        if not items:
            return ""
        inner = ('<ul class="rr-bul">' +
                 "".join(f'<li{_it(f"certifications.{i}")}>{_ef(f"certifications.{i}", x, "certification", ctx)}</li>'
                         for i, x in enumerate(items)) + "</ul>")
    elif key == "interests":
        items = content.get("interests") or []
        if not items:
            return ""
        inner = _render_chips([{"name": x} for x in items], ctx)
    elif key == "references":
        items = content.get("references") or []
        if not items:
            return ""
        inner = ('<ul class="rr-bul">' +
                 "".join(f'<li{_it(f"references.{i}")}>{_ef(f"references.{i}", x, "reference", ctx)}</li>'
                         for i, x in enumerate(items)) + "</ul>")
    else:
        return ""

    if not inner:
        return ""

    heading_html = f'<div class="rr-section-heading">{_e(title_text)}</div>'
    return (
        f'<div class="rr-section rr-section-{key}">'
        f'{heading_html}'
        f'{inner}'
        f'</div>'
    )


def _skill_colors(design: dict) -> list:
    return (design.get("colors") or {}).get("skill_colors") or ["#2563eb", "#1e40af", "#93c5fd"]


# ════════════════════════════════════════════════════════════════════════════
#  HELPER FUNCTIONS
# ════════════════════════════════════════════════════════════════════════════

def _e(s) -> str:
    """HTML-escape a value."""
    return _html.escape(str(s or ""), quote=True)


def _ef(path: str, value, placeholder: str = "", ctx: dict | None = None) -> str:
    """
    Returns escaped text in normal mode, or a contenteditable span in edit mode.
    Mirrors resume_builder._f() / _EDIT pattern but uses _REPLICA_EDIT.
    """
    edit = (ctx.get("edit") if ctx else False) or _REPLICA_EDIT.get()
    if not edit:
        return _e(value)
    ph = _e(placeholder or (path.split(".")[-1]))
    return (
        f'<span data-f="{_e(path)}" data-ph="{ph}" '
        f'contenteditable="true" spellcheck="true">{_e(value)}</span>'
    )


def _it(path: str) -> str:
    """Returns data-item attribute string in edit mode, else empty string."""
    if _REPLICA_EDIT.get():
        return f' data-item="{_e(path)}"'
    return ""


def _commands_to_d(commands: list) -> str:
    """
    Converts a list of SVG path command lists to a path 'd' string.
    [["M", 0, 0], ["L", 100, 0], ["Z"]] -> "M 0 0 L 100 0 Z"
    """
    parts = []
    for cmd in commands:
        if not cmd:
            continue
        op = str(cmd[0])
        coords = " ".join(f"{v:.4g}" for v in cmd[1:]) if len(cmd) > 1 else ""
        parts.append(f"{op} {coords}".strip())
    return " ".join(parts)


def _ring_svg(level_pct: int, color: str, track: str) -> str:
    """Renders a single ring/donut chart SVG for a skill."""
    circ = 2 * math.pi * 15
    dash = circ * level_pct / 100
    return (
        f'<svg viewBox="0 0 36 36" xmlns="http://www.w3.org/2000/svg">'
        f'<circle cx="18" cy="18" r="15" fill="none" stroke="{_e(track)}" stroke-width="3.2"/>'
        f'<circle cx="18" cy="18" r="15" fill="none" stroke="{_e(color)}" stroke-width="3.2" '
        f'stroke-linecap="round" stroke-dasharray="{dash:.1f} {circ:.1f}" '
        f'transform="rotate(-90 18 18)"/>'
        f'<text x="18" y="21" text-anchor="middle" font-size="8.5" font-weight="700" '
        f'fill="{_e(color)}">{level_pct}%</text>'
        f'</svg>'
    )


def _initials_block(name: str, color: str, size_mm: float) -> str:
    """Returns the initials text for the photo placeholder."""
    parts = [p for p in re.split(r"\s+", name.strip()) if p]
    initials = "".join(p[0] for p in parts[:2]).upper() or "CV"
    return f'<span style="font-size:{size_mm * 0.32:.1f}mm;line-height:1">{_e(initials)}</span>'


def _icon_svg(name: str, color: str = "currentColor", size: str = "1em") -> str:
    """Returns an inline SVG icon using the _ICONS dict."""
    # First try local _ICONS, then fall back to resume_builder._ICONS
    body = _ICONS.get(name)
    if not body:
        try:
            from app.services.resume_builder import _ICONS as _RB_ICONS
            body = _RB_ICONS.get(name) or _RB_ICONS.get("star", "")
        except Exception:
            body = _ICONS.get("star", "")
    if not body:
        body = _ICONS.get("star", "")
    return (
        f'<svg viewBox="0 0 24 24" width="{_e(size)}" height="{_e(size)}" '
        f'fill="none" stroke="{_e(color)}" stroke-width="2" '
        f'stroke-linecap="round" stroke-linejoin="round">{body}</svg>'
    )


def _guess_icon(title: str) -> str:
    """Guesses an icon name from a competency title string."""
    _ICON_GUESS = [
        ("strateg", "compass"), ("plan", "clipboard"), ("team", "users"),
        ("develop", "trending"), ("manage", "user"), ("lead", "users"),
        ("coach", "presentation"), ("mentor", "presentation"), ("train", "presentation"),
        ("target", "target"), ("execut", "target"), ("goal", "target"),
        ("analy", "pie"), ("data", "bars"), ("persist", "refresh"),
        ("relation", "handshake"), ("client", "handshake"), ("customer", "handshake"),
        ("sales", "money"), ("revenue", "money"), ("finance", "money"),
        ("market", "megaphone"), ("brand", "megaphone"), ("communic", "chat"),
        ("creativ", "lightbulb"), ("innov", "lightbulb"), ("operat", "gear"),
        ("process", "gear"), ("tech", "code"), ("software", "code"),
        ("research", "book"), ("compliance", "shield"), ("risk", "shield"),
        ("time", "clock"), ("global", "globe"),
    ]
    t = title.lower()
    for kw, ic in _ICON_GUESS:
        if kw in t:
            return ic
    return "star"


def _collect_google_fonts(scene_graph: dict, style_registry: dict) -> str:
    """
    Scans the scene graph and style registry for font families.
    Returns a Google Fonts <link> tag for any fonts we can request.
    """
    families_needed: set[str] = set()

    # Scan style_registry for font families
    for key, style in (style_registry or {}).items():
        if isinstance(style, dict):
            ff = str(style.get("font_family") or "").strip()
            if ff:
                families_needed.add(ff.lower().split(",")[0].strip().strip("'\""))

    # Scan scene_graph nodes recursively
    def _walk(node):
        if not isinstance(node, dict):
            return
        ff = (node.get("style") or {}).get("font_family") or ""
        if ff:
            families_needed.add(ff.lower().split(",")[0].strip().strip("'\""))
        ff2 = node.get("font_family") or ""
        if ff2:
            families_needed.add(ff2.lower().split(",")[0].strip().strip("'\""))
        for child in (node.get("children") or []):
            _walk(child)

    _walk(scene_graph)

    queries = []
    for fam in families_needed:
        gf_query = _GF_FAMILIES.get(fam)
        if gf_query:
            queries.append(gf_query)

    if not queries:
        return ""
    combined = "&family=".join(queries)
    href = f"https://fonts.googleapis.com/css2?family={combined}&display=swap"
    return (
        f'<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        f'<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        f'<link href="{href}" rel="stylesheet">\n'
    )


def _mm_to_pt(mm: float) -> float:
    """Converts mm to pt (1mm = 2.8346pt)."""
    return mm * 2.8346


def _pt_to_mm(pt: float) -> float:
    """Converts pt to mm (1pt = 0.3528mm)."""
    return pt * 0.3528
