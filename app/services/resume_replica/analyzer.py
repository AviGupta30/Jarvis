"""
analyzer.py — Reference image → replica document (scene graph).

Pipeline:
1. Extract dominant palette (k-means, 8 colors)
2. Detect page geometry with pixel measurements
3. Run two VLM calls in parallel:
   - _REPLICA_DESIGN_PROMPT → rich design JSON
   - _REPLICA_LAYOUT_PROMPT → section list with columns
4. Run pixel color measurements (_pixel_measurements)
5. Build scene graph from VLM output + measurements
6. Return replica document
"""
from __future__ import annotations

import datetime
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

from app.core.config import settings
from app.services.resume_builder import (
    _file_hash,
    _gemini,
    _groq,
    _image_b64,
    _measure_band,
    _measure_frame,
    _palette,
    _parse_json,
    _pixel_colors,
    _rgb,
    _hex as _tohex,
    _lum,
    _readable_on,
)

# ---------------------------------------------------------------------------
# Vision prompts
# ---------------------------------------------------------------------------

_REPLICA_DESIGN_PROMPT = """\
You are a senior UI engineer analyzing a resume design to reconstruct it exactly.
Ignore phone status bars, app chrome, and viewer backgrounds.
Dominant colors from the image: {palette}

Return ONLY this JSON:
{{
  "layout": {{"type": "sidebar_left|sidebar_right|two_column|single_column", "sidebar_width_pct": 30}},
  "background": {{"color": "#hex"}},
  "sidebar": {{
    "fill": {{"type": "solid|gradient_linear", "color": "#hex", "gradient_start": "#hex", "gradient_end": "#hex", "gradient_angle_deg": 180}},
    "top_band": null
  }},
  "header": {{
    "type": "full_band|diagonal_split|sidebar_name|sidebar_photo|centered|left_plain",
    "fill": {{"type": "solid|gradient_linear", "color": "#hex", "gradient_start": "#hex", "gradient_end": "#hex", "angle_deg": 135}},
    "shape_bottom": "flat|wave|curve|diagonal",
    "accent_bar": null,
    "name_band": null,
    "photo": {{
      "present": true,
      "shape": "circle|rounded|square|hexagon|diamond|squircle|none",
      "position": "left|right|center|sidebar",
      "ring": null
    }}
  }},
  "section_heading": {{
    "style": "plain|underline|bar_left|bar_right|full_bg|angled_bg|pill|gradient_underline|icon_before|double_line",
    "bg_color": null,
    "text_color": "#hex",
    "slant_amount": 0,
    "underline_color": null,
    "icon_shape": null,
    "icon_color": null,
    "letter_spacing": "normal|wide|very_wide",
    "weight": "bold|black"
  }},
  "skills_section": {{
    "type": "bars|dots|rings|venn|chips|radar|tag_level|list",
    "fill_color": "#hex",
    "track_color": null,
    "columns": 1
  }},
  "experience": {{
    "timeline": true,
    "node_shape": "circle|diamond|square|none",
    "node_color": "#hex",
    "line_color": "#hex"
  }},
  "footer": {{"type": "none|wave|curve|bar", "color": null}},
  "column_divider": {{"present": false, "color": null}},
  "decor": {{"type": "none|circles|dots|lines|corner", "color": null}},
  "typography": {{
    "heading_font": "sans|serif|mono|geometric|modern|elegant",
    "body_font": "sans|serif|mono|geometric|modern|elegant",
    "name_case": "upper|title",
    "heading_case": "upper|title",
    "heading_color": "#hex",
    "body_color": "#hex",
    "accent_color": "#hex"
  }},
  "sections": [
    {{"title": "exact heading text", "column": "left|right|full", "key": "profile|experience|skills|contact|education|achievements|certifications|languages|interests|projects|highlights|competencies|references"}}
  ]
}}
"""

_REPLICA_LAYOUT_PROMPT = """\
Look at this resume page (ignore phone UI bars and viewer background). \
List every section heading in reading order and say which column it is in.
Return ONLY JSON: {{"columns": 1 or 2, "equal_columns": true|false, "narrow_column": "left|right|none",
"narrow_column_width_percent": <n>, "left_column_has_own_background": true|false,
"sections": [{{"title": "<heading text>", "column": "left|right|full"}}],
"heading_text_color": "<hex of section heading text such as PROFILE>",
"skill_graphic_colors": ["<hex>", "<hex>", "<hex>"],
"banner_color": "<hex of the header/banner background>",
"name_color": "<hex of the person's name text>"}}
"""

# ---------------------------------------------------------------------------
# Font stacks
# ---------------------------------------------------------------------------

_FONT_STACKS: dict[str, str] = {
    "sans":      "'Roboto', 'Segoe UI', Arial, sans-serif",
    "geometric": "'Montserrat', 'Segoe UI', Arial, sans-serif",
    "modern":    "'Poppins', 'Segoe UI', Arial, sans-serif",
    "serif":     "'Playfair Display', Georgia, serif",
    "elegant":   "'Cormorant Garamond', Georgia, serif",
    "mono":      "'JetBrains Mono', Consolas, monospace",
}

# Known section keys
_SECTION_KEYS = {
    "profile", "highlights", "contact", "skills", "competencies",
    "experience", "education", "achievements", "certifications",
    "languages", "interests", "projects", "references",
}

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _solid(color: str) -> dict:
    return {"type": "solid", "color": _tohex(color, "#ffffff")}


def _gradient_linear(angle_deg: float, start: str, end: str) -> dict:
    return {
        "type": "gradient_linear",
        "angle_deg": angle_deg,
        "stops": [
            {"offset_pct": 0, "color": _tohex(start, "#333333")},
            {"offset_pct": 100, "color": _tohex(end, "#111111")},
        ],
    }


def _no_fill() -> dict:
    return {"type": "none"}


def _text_node(
    node_id: str,
    binding: str | None = None,
    literal: str | None = None,
    style_ref: str | None = None,
    style: dict | None = None,
    placeholder: str | None = None,
) -> dict:
    return {
        "type": "text",
        "id": node_id,
        "binding": binding,
        "literal": literal,
        "style_ref": style_ref,
        "style": style,
        "placeholder": placeholder,
    }


def _group(node_id: str, children: list[dict], layout_mode: str = "flow", style: dict | None = None) -> dict:
    return {
        "type": "group",
        "id": node_id,
        "layout_mode": layout_mode,
        "children": children,
        "style": style or {},
    }


def _frame(
    node_id: str,
    children: list[dict],
    layout_mode: str = "flow",
    page_spanning: bool = False,
    position: dict | None = None,
    size: dict | None = None,
    fill: dict | None = None,
    padding: dict | None = None,
    z_index: int = 0,
) -> dict:
    return {
        "type": "frame",
        "id": node_id,
        "layout_mode": layout_mode,
        "page_spanning": page_spanning,
        "position": position,
        "size": size or {"width_mm": None, "width_pct": 100.0, "height_mm": None, "height_pct": None},
        "fill": fill or _no_fill(),
        "padding": padding or {"top_mm": 0.0, "right_mm": 0.0, "bottom_mm": 0.0, "left_mm": 0.0},
        "children": children,
        "z_index": z_index,
    }


def _chart_node(
    node_id: str,
    chart_type: str,
    binding: str,
    colors: list[str],
    track_color: str | None = None,
    columns: int = 1,
) -> dict:
    return {
        "type": "chart",
        "id": node_id,
        "chart_type": chart_type,
        "binding": binding,
        "label_field": "name",
        "value_field": "level",
        "colors": colors,
        "track_color": track_color,
        "columns": columns,
    }


def _repeat_node(
    node_id: str,
    binding: str,
    component: dict,
    gap_mm: float = 4.0,
    heading_node: dict | None = None,
) -> dict:
    return {
        "type": "repeat",
        "id": node_id,
        "binding": binding,
        "component": component,
        "gap_mm": gap_mm,
        "heading_node": heading_node,
    }


def _path_parametric(
    node_id: str,
    parametric_type: str,
    params: dict,
    fill: dict | None = None,
    stroke: dict | None = None,
) -> dict:
    return {
        "type": "path",
        "id": node_id,
        "geometry": {
            "type": "parametric",
            "parametric_type": parametric_type,
            "params": params,
        },
        "fill": fill or _no_fill(),
        "stroke": stroke,
    }


def _path_commands(
    node_id: str,
    commands: list,
    viewbox: list,
    fill: dict | None = None,
    stroke: dict | None = None,
) -> dict:
    return {
        "type": "path",
        "id": node_id,
        "geometry": {
            "type": "commands",
            "commands": commands,
            "viewBox": viewbox,
        },
        "fill": fill or _no_fill(),
        "stroke": stroke,
    }


def _image_node(
    node_id: str,
    width_mm: float,
    height_mm: float,
    clip_shape: str = "circle",
    clip_radius_pct: float = 50.0,
    ring: dict | None = None,
    binding: str = "photo",
) -> dict:
    return {
        "type": "image",
        "id": node_id,
        "binding": binding,
        "size": {"width_mm": width_mm, "height_mm": height_mm},
        "clip_shape": clip_shape,
        "clip_radius_pct": clip_radius_pct,
        "ring": ring,
    }


def _rule_path(node_id: str, color: str, width_mm: float = 0.3) -> dict:
    """Horizontal rule using a parametric line."""
    return _path_parametric(
        node_id,
        "hrule",
        {"width_pct": 100, "height_pt": width_mm * 2.835},
        fill=_solid(color),
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def analyze_reference(image_path: str, legacy_spec: dict | None = None) -> dict:
    """
    Main entry point. Returns a complete replica document dict:
    {
      "id": sha1_of_image,
      "schema_version": 1,
      "reference_hash": sha1,
      "created_at": timestamp,
      "scene_graph": PAGE_NODE,
      "style_registry": {style_id: TEXT_STYLE},
      "component_registry": {},
      "measurements": {pixel measurement results},
      "raw_vision": {the raw VLM response, for debugging}
    }

    Falls back gracefully: if VLM fails, uses legacy_spec to build
    a basic scene graph from the vocabulary-based design.
    """
    sha1 = _file_hash(image_path)

    # 1. Extract dominant palette
    pal = _palette(image_path, k=8)
    palette_txt = ", ".join(f"{h} ({round(s*100)}%)" for h, s in pal) if pal else "unknown"

    # 2. Encode image for vision calls
    b64, mime = _image_b64(image_path, max_side=1400)

    # 3. Run two VLM calls in parallel
    design_json: dict = {}
    layout_json: dict = {}
    try:
        design_json, layout_json = _run_vision_calls(b64, mime, palette_txt)
    except Exception as exc:
        print(f"[replica] vision calls failed: {exc}")

    # 4. Fallback to legacy spec if VLM returned nothing useful
    if not design_json and legacy_spec:
        try:
            page_node = _build_from_legacy(legacy_spec, image_path)
            style_registry = _build_style_registry({}, {})
            return {
                "id": sha1,
                "schema_version": 1,
                "reference_hash": sha1,
                "created_at": datetime.datetime.utcnow().isoformat() + "Z",
                "scene_graph": page_node,
                "style_registry": style_registry,
                "component_registry": {},
                "measurements": {},
                "raw_vision": {"design": {}, "layout": {}},
            }
        except Exception as exc2:
            print(f"[replica] legacy fallback failed: {exc2}")

    # 5. Pixel measurements (override VLM color guesses with real pixel values)
    measurements: dict = {}
    try:
        measurements = _pixel_measurements(image_path, design_json)
    except Exception as exc:
        print(f"[replica] pixel measurements failed: {exc}")

    # 6. Merge layout sections into design_json
    if layout_json.get("sections"):
        existing_keys = {s.get("key") for s in (design_json.get("sections") or [])}
        for ls in layout_json["sections"]:
            title = ls.get("title", "")
            col = ls.get("column", "right")
            # Infer key from title
            key = _infer_key(title)
            if key and key not in existing_keys:
                design_json.setdefault("sections", []).append({
                    "title": title, "column": col, "key": key
                })
                existing_keys.add(key)
        # Merge color hints from layout_json
        if layout_json.get("heading_text_color"):
            design_json.setdefault("section_heading", {})["text_color"] = layout_json["heading_text_color"]
        if layout_json.get("banner_color"):
            design_json.setdefault("header", {}).setdefault("fill", {})["color"] = layout_json["banner_color"]
        if layout_json.get("name_color"):
            design_json.setdefault("typography", {})["name_color"] = layout_json["name_color"]

    # 7. Build scene graph
    scene_graph: dict = {}
    try:
        scene_graph = _build_scene_graph(design_json, layout_json, measurements, image_path)
    except Exception as exc:
        print(f"[replica] scene graph build failed: {exc}")
        # Minimal fallback page
        scene_graph = {
            "type": "page",
            "id": "page",
            "width_mm": 210.0,
            "height_mm": 297.0,
            "background": _solid("#ffffff"),
            "children": [],
        }

    # 8. Build style registry
    style_registry = _build_style_registry(design_json, measurements)

    return {
        "id": sha1,
        "schema_version": 1,
        "reference_hash": sha1,
        "created_at": datetime.datetime.utcnow().isoformat() + "Z",
        "scene_graph": scene_graph,
        "style_registry": style_registry,
        "component_registry": {},
        "measurements": measurements,
        "raw_vision": {"design": design_json, "layout": layout_json},
    }


# ---------------------------------------------------------------------------
# Vision calls
# ---------------------------------------------------------------------------

def _vision_call(b64: str, mime: str, prompt: str, max_tokens: int = 2500) -> dict:
    """Single vision call: tries Groq first, falls back to Gemini."""
    try:
        r = _groq().chat.completions.create(
            model=settings.GROQ_VISION_MODEL,
            messages=[{"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}}
            ]}],
            temperature=0.1,
            max_tokens=max_tokens,
        )
        result = _parse_json(r.choices[0].message.content or "")
        if result:
            return result
    except Exception as exc:
        print(f"[replica] groq vision failed: {exc}")
    # Gemini fallback
    raw = _gemini(
        [{"text": prompt}, {"inline_data": {"mime_type": mime, "data": b64}}],
        True,
        max_tokens + 1500,
    )
    return _parse_json(raw) if raw else {}


def _run_vision_calls(b64: str, mime: str, palette_txt: str) -> tuple[dict, dict]:
    """
    Runs the two vision calls in parallel using ThreadPoolExecutor.
    Returns (design_json, layout_json).
    """
    design_prompt = _REPLICA_DESIGN_PROMPT.format(palette=palette_txt)
    layout_prompt = _REPLICA_LAYOUT_PROMPT

    design_json: dict = {}
    layout_json: dict = {}

    with ThreadPoolExecutor(max_workers=2) as pool:
        fut_design = pool.submit(_vision_call, b64, mime, design_prompt, 2500)
        fut_layout = pool.submit(_vision_call, b64, mime, layout_prompt, 1200)
        for fut in as_completed([fut_design, fut_layout]):
            if fut is fut_design:
                try:
                    design_json = fut.result() or {}
                except Exception as exc:
                    print(f"[replica] design prompt failed: {exc}")
            else:
                try:
                    layout_json = fut.result() or {}
                except Exception as exc:
                    print(f"[replica] layout prompt failed: {exc}")

    return design_json, layout_json


# ---------------------------------------------------------------------------
# Pixel measurements
# ---------------------------------------------------------------------------

def _pixel_measurements(image_path: str, design_json: dict) -> dict:
    """
    Runs pixel-level measurements on the image.

    Returns dict with keys:
    - page_bg_color
    - sidebar_bg_color
    - sidebar_gradient
    - sidebar_gradient_top
    - sidebar_gradient_bottom
    - header_color
    - heading_color
    - sidebar_width_pct
    - divider_x_pct
    - page_inset
    """
    try:
        import cv2
        import numpy as np
    except ImportError:
        return {}

    result: dict = {}

    try:
        img = cv2.imread(image_path)
        if img is None:
            return {}
        h, w = img.shape[:2]
        scale = 500 / max(w, 1)
        if scale < 1:
            img = cv2.resize(img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)
        h, w = img.shape[:2]
        rgb = img[:, :, ::-1].astype(np.int32)

        def _dominant_color(region: Any) -> str:
            """Return hex of the most common quantised color in region."""
            if region.size == 0:
                return "#ffffff"
            flat = (region.reshape(-1, 3) // 4) * 4
            vals, counts = np.unique(flat, axis=0, return_counts=True)
            r, g, b = (int(v) + 2 for v in vals[counts.argmax()])
            return "#%02x%02x%02x" % (r, g, b)

        # --- page background: central content area -------------------------
        page_bg = _dominant_color(rgb[int(h * 0.30):int(h * 0.95), int(w * 0.45):int(w * 0.95)])
        result["page_bg_color"] = page_bg

        # --- detect layout from design_json --------------------------------
        layout_type = ""
        sidebar_w_pct = 33.0
        lout = design_json.get("layout") or {}
        if isinstance(lout, dict):
            layout_type = lout.get("type", "")
            sidebar_w_pct = float(lout.get("sidebar_width_pct") or 33)
        elif isinstance(lout, str):
            layout_type = lout

        # --- sidebar measurements -------------------------------------------
        if layout_type in ("sidebar_left", "sidebar_right"):
            sw = sidebar_w_pct / 100.0
            if layout_type == "sidebar_left":
                x0, x1 = 0, int(w * sw * 0.92)
            else:
                x0, x1 = int(w * (1 - sw * 0.92)), w
            side_region = rgb[int(h * 0.20):int(h * 0.90), x0:x1]
            sidebar_color = _dominant_color(side_region)
            result["sidebar_bg_color"] = sidebar_color

            # Check gradient: compare top 20% vs bottom 20% of sidebar
            top_region = rgb[int(h * 0.05):int(h * 0.25), x0:x1]
            bot_region = rgb[int(h * 0.75):int(h * 0.95), x0:x1]
            top_color = _dominant_color(top_region)
            bot_color = _dominant_color(bot_region)
            top_rgb = np.array(_rgb(top_color), dtype=float)
            bot_rgb = np.array(_rgb(bot_color), dtype=float)
            color_diff = float(np.linalg.norm(top_rgb - bot_rgb))
            result["sidebar_gradient"] = color_diff > 30.0
            result["sidebar_gradient_top"] = top_color
            result["sidebar_gradient_bottom"] = bot_color

            # Measure actual sidebar width by finding the edge
            # (column of pixels where sidebar color dominates)
            def _is_sidebar(col_idx: int) -> bool:
                col = rgb[:, col_idx, :]
                sr, sg, sb = _rgb(sidebar_color)
                dist = np.sqrt(((col - np.array([sr, sg, sb])) ** 2).sum(-1))
                return float((dist < 40).mean()) > 0.5

            if layout_type == "sidebar_left":
                edge = x1
                for xi in range(x1, 0, -4):
                    if not _is_sidebar(xi):
                        edge = xi
                        break
                result["sidebar_width_pct"] = round(100.0 * edge / max(w, 1), 1)
            else:
                edge = x0
                for xi in range(x0, w, 4):
                    if not _is_sidebar(xi):
                        edge = xi
                        break
                result["sidebar_width_pct"] = round(100.0 * (w - edge) / max(w, 1), 1)

            # Divider line
            body = rgb[int(h * 0.30):int(h * 0.95)]
            page_lum = float(np.median(body.mean(-1)))
            dark_cols = np.where((body.mean(-1) < page_lum - 35).mean(0) >= 0.5)[0]
            dark_cols = [x for x in dark_cols if w * 0.18 <= x <= w * 0.6]
            if dark_cols and (dark_cols[-1] - dark_cols[0]) < w * 0.02:
                result["divider_x_pct"] = round(100.0 * float(np.mean(dark_cols)) / w, 1)
            else:
                result["divider_x_pct"] = None
        else:
            result["sidebar_bg_color"] = page_bg
            result["sidebar_gradient"] = False
            result["sidebar_gradient_top"] = page_bg
            result["sidebar_gradient_bottom"] = page_bg
            result["sidebar_width_pct"] = sidebar_w_pct
            result["divider_x_pct"] = None

        # --- header color: top 20% of page ----------------------------------
        header_region = rgb[int(h * 0.01):int(h * 0.20), int(w * 0.25):int(w * 0.80)]
        result["header_color"] = _dominant_color(header_region)

        # --- heading text color (use VLM value if available) ----------------
        heading_color = (design_json.get("section_heading") or {}).get("text_color") or "#333333"
        result["heading_color"] = _tohex(heading_color, "#333333")

        # --- page inset: measure from _measure_frame -----------------------
        legacy_colors = {
            "page_bg": result["page_bg_color"],
            "sidebar_bg": result.get("sidebar_bg_color", "#ffffff"),
            "primary": result.get("header_color", "#333333"),
        }
        legacy_spec_mock = {
            "layout": layout_type or "single_column",
            "sidebar_width": int(result.get("sidebar_width_pct", 33)),
            "header": "full_band",
            "header_shape": "flat",
        }
        inset = _measure_frame(image_path, legacy_colors)
        result["page_inset"] = inset if inset else [0, 0, 0, 0]

    except Exception as exc:
        print(f"[replica] _pixel_measurements failed: {exc}")

    return result


# ---------------------------------------------------------------------------
# Scene graph builder
# ---------------------------------------------------------------------------

def _build_scene_graph(
    design_json: dict,
    layout_json: dict,
    measurements: dict,
    image_path: str,
) -> dict:
    """
    Builds the scene graph from VLM output + pixel measurements.
    Returns a PAGE node.
    """
    # ── Layout meta ────────────────────────────────────────────────────────
    lout = design_json.get("layout") or {}
    if isinstance(lout, dict):
        layout_type = lout.get("type", "single_column")
        sidebar_w_pct = float(lout.get("sidebar_width_pct") or 33)
    else:
        layout_type = str(lout) or "single_column"
        sidebar_w_pct = 33.0

    # Override with measured sidebar width
    measured_sw = measurements.get("sidebar_width_pct")
    if measured_sw and 15.0 < measured_sw < 65.0:
        sidebar_w_pct = measured_sw

    # ── Colors ─────────────────────────────────────────────────────────────
    bg_color = (design_json.get("background") or {}).get("color") or "#ffffff"
    measured_page_bg = measurements.get("page_bg_color")
    if measured_page_bg:
        bg_color = measured_page_bg

    # ── Page node ──────────────────────────────────────────────────────────
    page_children: list[dict] = []

    # ── Sidebar background frame (page_spanning) ───────────────────────────
    if layout_type in ("sidebar_left", "sidebar_right"):
        sidebar_fill_cfg = (design_json.get("sidebar") or {}).get("fill") or {}
        measured_sb = measurements.get("sidebar_bg_color")
        is_gradient = measurements.get("sidebar_gradient", False)

        if is_gradient:
            top_c = measurements.get("sidebar_gradient_top", "#333333")
            bot_c = measurements.get("sidebar_gradient_bottom", "#111111")
            sidebar_fill = _gradient_linear(180, top_c, bot_c)
        elif measured_sb:
            sidebar_fill = _solid(measured_sb)
        else:
            fill_type = sidebar_fill_cfg.get("type", "solid")
            if fill_type == "gradient_linear":
                sidebar_fill = _gradient_linear(
                    float(sidebar_fill_cfg.get("gradient_angle_deg", 180)),
                    sidebar_fill_cfg.get("gradient_start", "#333333"),
                    sidebar_fill_cfg.get("gradient_end", "#111111"),
                )
            else:
                sidebar_fill = _solid(sidebar_fill_cfg.get("color", "#2d3748"))

        if layout_type == "sidebar_left":
            sb_pos = {"x_mm": 0.0, "y_mm": 0.0}
            sb_size = {"width_mm": None, "width_pct": sidebar_w_pct, "height_mm": 297.0, "height_pct": None}
        else:
            sb_size_w = 210.0 * (sidebar_w_pct / 100.0)
            sb_pos = {"x_mm": 210.0 - sb_size_w, "y_mm": 0.0}
            sb_size = {"width_mm": sb_size_w, "width_pct": None, "height_mm": 297.0, "height_pct": None}

        sidebar_bg_frame = _frame(
            "sidebar_master",
            children=[],
            layout_mode="absolute",
            page_spanning=True,
            position=sb_pos,
            size=sb_size,
            fill=sidebar_fill,
            padding={"top_mm": 0, "right_mm": 0, "bottom_mm": 0, "left_mm": 0},
            z_index=0,
        )
        page_children.append(sidebar_bg_frame)

    # ── Decorative background elements ─────────────────────────────────────
    decor_cfg = design_json.get("decor") or {}
    decor_type = decor_cfg.get("type", "none")
    decor_color = decor_cfg.get("color")
    if decor_type != "none" and decor_color:
        decor_nodes = _build_decor_nodes(decor_type, decor_color)
        if decor_nodes:
            page_children.append(_frame(
                "decor_layer",
                children=decor_nodes,
                layout_mode="absolute",
                page_spanning=True,
                position={"x_mm": 0.0, "y_mm": 0.0},
                size={"width_mm": 210.0, "width_pct": None, "height_mm": 297.0, "height_pct": None},
                fill=_no_fill(),
                z_index=0,
            ))

    # ── Header frame ───────────────────────────────────────────────────────
    header_cfg = design_json.get("header") or {}
    header_type = header_cfg.get("header_type") or header_cfg.get("type", "full_band")
    header_fill_cfg = header_cfg.get("fill") or {}

    measured_hdr = measurements.get("header_color")
    if measured_hdr:
        header_fill = _solid(measured_hdr)
    else:
        h_fill_type = header_fill_cfg.get("type", "solid")
        if h_fill_type == "gradient_linear":
            header_fill = _gradient_linear(
                float(header_fill_cfg.get("angle_deg", 135)),
                header_fill_cfg.get("gradient_start") or header_fill_cfg.get("color", "#2d3748"),
                header_fill_cfg.get("gradient_end", "#1a202c"),
            )
        else:
            header_fill = _solid(header_fill_cfg.get("color", "#2d3748"))

    header_nodes = _build_header_nodes(design_json, measurements)
    header_height_mm = 55.0 if header_type in ("full_band", "diagonal_split") else 40.0
    if header_type in ("sidebar_name", "sidebar_photo", "left_plain"):
        header_height_mm = 0.0  # name is placed in sidebar/column content

    page_inset = measurements.get("page_inset") or [0, 0, 0, 0]
    inset_top = float(page_inset[0]) if page_inset else 0.0

    if header_height_mm > 0:
        header_frame = _frame(
            "header",
            children=header_nodes,
            layout_mode="flow",
            page_spanning=False,
            position=None,
            size={"width_mm": None, "width_pct": 100.0, "height_mm": header_height_mm, "height_pct": None},
            fill=header_fill,
            padding={"top_mm": inset_top + 8.0, "right_mm": 10.0, "bottom_mm": 6.0, "left_mm": 10.0},
            z_index=1,
        )
        page_children.append(header_frame)

    # ── Footer ─────────────────────────────────────────────────────────────
    footer_cfg = design_json.get("footer") or {}
    footer_type = footer_cfg.get("type", "none")
    footer_color = footer_cfg.get("color")

    # ── Sections ───────────────────────────────────────────────────────────
    sections_cfg = design_json.get("sections") or []
    sidebar_sections: list[dict] = []
    main_sections: list[dict] = []

    for sec in sections_cfg:
        col = sec.get("column", "right")
        if layout_type == "sidebar_left" and col == "left":
            sidebar_sections.append(sec)
        elif layout_type == "sidebar_right" and col == "right":
            sidebar_sections.append(sec)
        else:
            main_sections.append(sec)

    # If no sections from VLM, fall back to defaults
    if not sidebar_sections and not main_sections:
        if layout_type in ("sidebar_left", "sidebar_right"):
            sidebar_sections = [
                {"key": "contact", "title": "Contact", "column": "left"},
                {"key": "skills", "title": "Skills", "column": "left"},
                {"key": "languages", "title": "Languages", "column": "left"},
                {"key": "education", "title": "Education", "column": "left"},
            ]
            main_sections = [
                {"key": "profile", "title": "Profile", "column": "right"},
                {"key": "experience", "title": "Experience", "column": "right"},
                {"key": "projects", "title": "Projects", "column": "right"},
            ]
        else:
            main_sections = [
                {"key": k, "title": k.capitalize(), "column": "right"}
                for k in ["profile", "experience", "skills", "education"]
            ]

    # Build sidebar column children
    sidebar_col_children: list[dict] = []
    for i, sec in enumerate(sidebar_sections):
        sec_node = _build_section_group(sec, design_json, measurements, i, is_sidebar=True)
        sidebar_col_children.append(sec_node)

    # Build main column children
    main_col_children: list[dict] = []
    for i, sec in enumerate(main_sections):
        sec_node = _build_section_group(sec, design_json, measurements, i, is_sidebar=False)
        main_col_children.append(sec_node)

    # ── Columns frame ──────────────────────────────────────────────────────
    col_padding = {"top_mm": 5.0, "right_mm": 6.0, "bottom_mm": 5.0, "left_mm": 6.0}

    if layout_type in ("sidebar_left", "sidebar_right"):
        main_w_pct = 100.0 - sidebar_w_pct

        sidebar_frame = _frame(
            "sidebar",
            children=sidebar_col_children,
            layout_mode="flow",
            page_spanning=False,
            position=None,
            size={"width_mm": None, "width_pct": sidebar_w_pct, "height_mm": None, "height_pct": None},
            fill=_no_fill(),  # background handled by page_spanning master frame
            padding=col_padding,
            z_index=1,
        )

        # Column divider line
        col_divider_cfg = design_json.get("column_divider") or {}
        divider_nodes: list[dict] = []
        if col_divider_cfg.get("present"):
            div_color = col_divider_cfg.get("color") or "#cccccc"
            divider_nodes = [_path_commands(
                "col_divider_line",
                [["M", 0, 0], ["L", 0, 297]],
                [0, 0, 1, 297],
                fill=_no_fill(),
                stroke={"color": _tohex(div_color, "#cccccc"), "width_pt": 0.5},
            )]

        main_frame = _frame(
            "main",
            children=main_col_children,
            layout_mode="flow",
            page_spanning=False,
            position=None,
            size={"width_mm": None, "width_pct": main_w_pct, "height_mm": None, "height_pct": None},
            fill=_no_fill(),
            padding=col_padding,
            z_index=1,
        )

        columns_children: list[dict] = (
            [sidebar_frame] + divider_nodes + [main_frame]
            if layout_type == "sidebar_left"
            else [main_frame] + divider_nodes + [sidebar_frame]
        )
        columns_frame = _frame(
            "columns",
            children=columns_children,
            layout_mode="flex_row",
            page_spanning=False,
            position=None,
            size={"width_mm": None, "width_pct": 100.0, "height_mm": None, "height_pct": None},
            fill=_no_fill(),
            padding={"top_mm": 0, "right_mm": 0, "bottom_mm": 0, "left_mm": 0},
            z_index=1,
        )
        page_children.append(columns_frame)

    elif layout_type == "two_column":
        col_a = _frame(
            "col_a",
            children=sidebar_col_children if sidebar_col_children else main_col_children[:len(main_col_children)//2],
            layout_mode="flow",
            size={"width_mm": None, "width_pct": 50.0, "height_mm": None, "height_pct": None},
            fill=_no_fill(),
            padding=col_padding,
            z_index=1,
        )
        col_b = _frame(
            "col_b",
            children=main_col_children if sidebar_col_children else main_col_children[len(main_col_children)//2:],
            layout_mode="flow",
            size={"width_mm": None, "width_pct": 50.0, "height_mm": None, "height_pct": None},
            fill=_no_fill(),
            padding=col_padding,
            z_index=1,
        )
        columns_frame = _frame(
            "columns",
            children=[col_a, col_b],
            layout_mode="flex_row",
            size={"width_mm": None, "width_pct": 100.0, "height_mm": None, "height_pct": None},
            fill=_no_fill(),
            padding={"top_mm": 0, "right_mm": 0, "bottom_mm": 0, "left_mm": 0},
            z_index=1,
        )
        page_children.append(columns_frame)

    else:
        # single_column
        all_sections = sidebar_col_children + main_col_children
        single_frame = _frame(
            "main",
            children=all_sections,
            layout_mode="flow",
            size={"width_mm": None, "width_pct": 100.0, "height_mm": None, "height_pct": None},
            fill=_no_fill(),
            padding=col_padding,
            z_index=1,
        )
        page_children.append(single_frame)

    # ── Footer frame ───────────────────────────────────────────────────────
    if footer_type != "none" and footer_color:
        footer_shape_node = _path_parametric(
            "footer_shape",
            footer_type,  # wave | curve | bar
            {"width_pct": 100, "height_mm": 12},
            fill=_solid(footer_color),
        )
        footer_frame = _frame(
            "footer",
            children=[footer_shape_node],
            layout_mode="absolute",
            page_spanning=False,
            position=None,
            size={"width_mm": None, "width_pct": 100.0, "height_mm": 12.0, "height_pct": None},
            fill=_no_fill(),
            padding={"top_mm": 0, "right_mm": 0, "bottom_mm": 0, "left_mm": 0},
            z_index=1,
        )
        page_children.append(footer_frame)

    return {
        "type": "page",
        "id": "page",
        "width_mm": 210.0,
        "height_mm": 297.0,
        "background": _solid(bg_color),
        "children": page_children,
    }


# ---------------------------------------------------------------------------
# Header builders
# ---------------------------------------------------------------------------

def _build_header_nodes(design_json: dict, measurements: dict) -> list[dict]:
    """
    Builds the header group nodes based on header type.
    Handles: full_band, diagonal_split, sidebar_name, sidebar_photo, centered, left_plain.
    For angled/shaped headers, uses PATH nodes for the geometry.
    Returns list of nodes to put in the header frame.
    """
    header_cfg = design_json.get("header") or {}
    header_type = header_cfg.get("header_type") or header_cfg.get("type", "full_band")
    photo_cfg = header_cfg.get("photo") or {}
    shape_bottom = header_cfg.get("shape_bottom", "flat")
    typo = design_json.get("typography") or {}
    name_case = typo.get("name_case", "upper")
    body_color_raw = typo.get("body_color", "#ffffff")
    header_text_color = _tohex(body_color_raw, "#ffffff")
    header_bg_color = (header_cfg.get("fill") or {}).get("color") or (measurements.get("header_color") or "#2d3748")
    header_text_color = _readable_on(header_bg_color)

    nodes: list[dict] = []

    # ── Non-banded headers: name lives inside column content ───────────────
    if header_type in ("sidebar_name", "sidebar_photo", "left_plain", "centered"):
        # These header types don't produce a large colored band across the top.
        # The name TEXT is placed in the sidebar or main column content.
        # We just return an empty list; the column builder will place name + title.
        return []

    # ── Shape-bottom overlay path (wave / curve / diagonal) ────────────────
    if shape_bottom != "flat":
        shape_node = _path_parametric(
            "header_shape_bottom",
            shape_bottom,
            {"width_pct": 100, "height_mm": 10, "direction": "down"},
            fill=_solid(header_bg_color),
        )
        nodes.append(shape_node)

    # ── Photo ──────────────────────────────────────────────────────────────
    if photo_cfg.get("present"):
        photo_position = photo_cfg.get("position", "left")
        photo_shape = photo_cfg.get("shape", "circle")
        ring_cfg = photo_cfg.get("ring")
        ring = None
        if ring_cfg:
            ring_color = ring_cfg.get("color", "#ffffff") if isinstance(ring_cfg, dict) else "#ffffff"
            ring = {"color": _tohex(ring_color, "#ffffff"), "width_mm": 1.5, "gap_mm": 0.5}
        clip_radius = 50.0 if photo_shape == "circle" else 15.0
        photo_node = _image_node(
            "photo",
            width_mm=28.0,
            height_mm=28.0,
            clip_shape=photo_shape if photo_shape != "none" else "circle",
            clip_radius_pct=clip_radius,
            ring=ring,
        )
        nodes.append(photo_node)

    # ── Name + Job Title text ───────────────────────────────────────────────
    name_node = _text_node(
        "header_name",
        binding="name",
        style_ref="name",
    )
    job_title_node = _text_node(
        "header_job_title",
        binding="job_title",
        style_ref="title",
    )
    nodes.append(name_node)
    nodes.append(job_title_node)

    # ── Diagonal split path ─────────────────────────────────────────────────
    if header_type == "diagonal_split":
        slant_node = _path_parametric(
            "header_diagonal",
            "diagonal_split",
            {"width_pct": 100, "height_mm": 55, "slant_mm": 20, "direction": "right"},
            fill=_solid(header_bg_color),
        )
        nodes.insert(0, slant_node)

    # ── Accent bar ─────────────────────────────────────────────────────────
    accent_bar = header_cfg.get("accent_bar")
    if accent_bar and isinstance(accent_bar, dict):
        bar_color = accent_bar.get("color", "#000000")
        bar_w = float(accent_bar.get("width_mm", 8))
        bar_side = accent_bar.get("side", "left")
        bar_x = 0.0 if bar_side == "left" else (210.0 - bar_w)
        bar_node = _path_commands(
            "header_accent_bar",
            [["M", bar_x, 0], ["L", bar_x + bar_w, 0], ["L", bar_x + bar_w, 55], ["L", bar_x, 55], ["Z"]],
            [0, 0, 210, 55],
            fill=_solid(bar_color),
        )
        nodes.insert(0, bar_node)

    return nodes


def _build_decor_nodes(decor_type: str, color: str) -> list[dict]:
    """Build decorative background path nodes (circles, dots, lines, corner)."""
    nodes: list[dict] = []
    c = _tohex(color, "#eeeeee")
    if decor_type == "circles":
        for i, (cx, cy, r) in enumerate([(190, 20, 40), (10, 270, 30), (195, 270, 25)]):
            nodes.append(_path_parametric(
                f"decor_circle_{i}",
                "circle",
                {"cx_mm": cx, "cy_mm": cy, "r_mm": r},
                fill=_solid(c),
            ))
    elif decor_type == "dots":
        nodes.append(_path_parametric(
            "decor_dots",
            "dot_grid",
            {"spacing_mm": 8, "dot_r_mm": 0.8, "color": c},
            fill=_solid(c),
        ))
    elif decor_type == "lines":
        for i in range(3):
            nodes.append(_path_commands(
                f"decor_line_{i}",
                [["M", 0, 80 + i * 30], ["L", 210, 80 + i * 30]],
                [0, 0, 210, 297],
                fill=_no_fill(),
                stroke={"color": c, "width_pt": 0.5},
            ))
    elif decor_type == "corner":
        nodes.append(_path_parametric(
            "decor_corner",
            "corner_arc",
            {"corner": "top_right", "r_mm": 60, "color": c},
            fill=_solid(c),
        ))
    return nodes


# ---------------------------------------------------------------------------
# Section group builders
# ---------------------------------------------------------------------------

def _build_section_group(
    section: dict,
    design_json: dict,
    measurements: dict,
    index: int,
    is_sidebar: bool = False,
) -> dict:
    """Build the GROUP node for a single section (heading + content)."""
    key = section.get("key", "")
    sec_id = f"section_{key}_{index}"
    heading_node = _build_section_heading_node(design_json, key, measurements)

    content_nodes: list[dict] = []

    if key == "profile":
        content_nodes.append(_text_node(f"{sec_id}_text", binding="profile", style_ref="body"))

    elif key == "skills":
        content_nodes.append(_build_skills_node(design_json, measurements))

    elif key == "competencies":
        comp_type = (design_json.get("skills_section") or {}).get("type", "list")
        chart_type = "chips" if comp_type == "chips" else "list"
        content_nodes.append(_chart_node(
            f"{sec_id}_chart", chart_type, "competencies",
            [(design_json.get("typography") or {}).get("accent_color", "#2563eb")],
        ))

    elif key == "experience":
        exp_component = _build_experience_component(design_json)
        content_nodes.append(_repeat_node(f"{sec_id}_repeat", "experience", exp_component, gap_mm=6.0))

    elif key == "education":
        edu_component = _group(
            "edu_entry",
            children=[
                _text_node("edu_degree", binding="education.{i}.degree", style_ref="job_role"),
                _text_node("edu_institution", binding="education.{i}.institution", style_ref="job_company"),
                _text_node("edu_year", binding="education.{i}.year", style_ref="job_period"),
            ],
        )
        content_nodes.append(_repeat_node(f"{sec_id}_repeat", "education", edu_component, gap_mm=4.0))

    elif key == "projects":
        proj_component = _group(
            "proj_entry",
            children=[
                _text_node("proj_name", binding="projects.{i}.name", style_ref="job_role"),
                _text_node("proj_desc", binding="projects.{i}.description", style_ref="body"),
            ],
        )
        content_nodes.append(_repeat_node(f"{sec_id}_repeat", "projects", proj_component, gap_mm=4.0))

    elif key == "contact":
        contact_group = _group(
            f"{sec_id}_contact",
            children=[
                _text_node("contact_phone", binding="contact.phone", style_ref="label"),
                _text_node("contact_email", binding="contact.email", style_ref="label"),
                _text_node("contact_location", binding="contact.location", style_ref="label"),
                _text_node("contact_linkedin", binding="contact.linkedin", style_ref="label"),
                _text_node("contact_website", binding="contact.website", style_ref="label"),
            ],
        )
        content_nodes.append(contact_group)

    elif key == "languages":
        lang_type = (design_json.get("skills_section") or {}).get("type", "dots")
        chart_type = lang_type if lang_type in ("bars", "dots", "chips", "list") else "dots"
        typo = design_json.get("typography") or {}
        fill_color = typo.get("accent_color", "#2563eb")
        content_nodes.append(_chart_node(
            f"{sec_id}_chart", chart_type, "languages", [fill_color],
            track_color=(design_json.get("skills_section") or {}).get("track_color"),
        ))

    elif key == "highlights":
        hl_component = _group(
            "hl_entry",
            children=[_text_node("hl_text", binding="highlights.{i}", style_ref="body")],
        )
        content_nodes.append(_repeat_node(f"{sec_id}_repeat", "highlights", hl_component, gap_mm=2.0))

    elif key in ("achievements", "certifications", "interests", "references"):
        item_component = _group(
            f"{key}_entry",
            children=[_text_node(f"{key}_item", binding=f"{key}.{{i}}", style_ref="body")],
        )
        content_nodes.append(_repeat_node(f"{sec_id}_repeat", key, item_component, gap_mm=2.0))

    else:
        # Generic fallback
        gen_component = _group(
            f"{key}_entry",
            children=[_text_node(f"{key}_item", binding=f"{key}.{{i}}", style_ref="body")],
        )
        content_nodes.append(_repeat_node(f"{sec_id}_repeat", key, gen_component, gap_mm=2.0))

    return _group(sec_id, children=[heading_node] + content_nodes)


def _build_section_heading_node(design_json: dict, section_key: str, measurements: dict) -> dict:
    """
    Builds a section heading GROUP node based on the heading style.
    - plain: just a TEXT node
    - underline: TEXT + RULE below
    - bar_left: PATH (vertical bar) + TEXT
    - bar_right: PATH (vertical bar on right) + TEXT
    - full_bg: FRAME with fill + TEXT
    - angled_bg: PATH (angled rect) + TEXT
    - pill: FRAME with rounded fill + TEXT
    - gradient_underline: TEXT + PATH (gradient line)
    - icon_before: PATH (square/circle/diamond) + TEXT
    - double_line: RULE + TEXT + RULE
    Returns a GROUP node.
    """
    heading_cfg = design_json.get("section_heading") or {}
    style = heading_cfg.get("style", "plain")
    text_color = _tohex(
        measurements.get("heading_color") or heading_cfg.get("text_color", "#2d3748"),
        "#2d3748"
    )
    bg_color = _tohex(heading_cfg.get("bg_color") or "#2d3748", "#2d3748")
    underline_color = _tohex(heading_cfg.get("underline_color") or text_color, text_color)
    icon_shape = heading_cfg.get("icon_shape") or "square"
    icon_color = _tohex(heading_cfg.get("icon_color") or text_color, text_color)

    node_id = f"heading_{section_key}"
    text_node = _text_node(
        f"{node_id}_text",
        binding=f"section_titles.{section_key}",
        style_ref="section_heading",
    )

    if style == "plain":
        return _group(node_id, children=[text_node])

    elif style == "underline":
        rule = _rule_path(f"{node_id}_rule", underline_color, 0.4)
        return _group(node_id, children=[text_node, rule])

    elif style == "bar_left":
        bar = _path_commands(
            f"{node_id}_bar",
            [["M", 0, 0], ["L", 3, 0], ["L", 3, 14], ["L", 0, 14], ["Z"]],
            [0, 0, 3, 14],
            fill=_solid(icon_color),
        )
        return _group(node_id, children=[bar, text_node], layout_mode="flow")

    elif style == "bar_right":
        bar = _path_commands(
            f"{node_id}_bar",
            [["M", 0, 0], ["L", 3, 0], ["L", 3, 14], ["L", 0, 14], ["Z"]],
            [0, 0, 3, 14],
            fill=_solid(icon_color),
        )
        return _group(node_id, children=[text_node, bar], layout_mode="flow")

    elif style == "full_bg":
        bg_frame = _frame(
            f"{node_id}_bg",
            children=[text_node],
            layout_mode="flow",
            size={"width_mm": None, "width_pct": 100.0, "height_mm": None, "height_pct": None},
            fill=_solid(bg_color),
            padding={"top_mm": 2.0, "right_mm": 4.0, "bottom_mm": 2.0, "left_mm": 4.0},
        )
        return _group(node_id, children=[bg_frame])

    elif style == "angled_bg":
        slant = float(heading_cfg.get("slant_amount", 12) or 12)
        angled = _path_parametric(
            f"{node_id}_angled",
            "angled_rect",
            {"width": 200, "height": 20, "slant": slant, "direction": "right"},
            fill=_solid(bg_color),
        )
        return _group(node_id, children=[angled, text_node])

    elif style == "pill":
        pill_frame = _frame(
            f"{node_id}_pill",
            children=[text_node],
            layout_mode="flow",
            size={"width_mm": None, "width_pct": None, "height_mm": None, "height_pct": None},
            fill=_solid(bg_color),
            padding={"top_mm": 1.5, "right_mm": 6.0, "bottom_mm": 1.5, "left_mm": 6.0},
        )
        return _group(node_id, children=[pill_frame])

    elif style == "gradient_underline":
        grad_rule = _path_parametric(
            f"{node_id}_grad_rule",
            "gradient_hrule",
            {"width_pct": 100, "height_pt": 1.5, "start_color": text_color, "end_color": "transparent"},
            fill=_gradient_linear(90, text_color, "#ffffff"),
        )
        return _group(node_id, children=[text_node, grad_rule])

    elif style == "icon_before":
        if icon_shape == "circle":
            icon_cmds = [["M", 6, 7], ["A", 5, 5, 0, 1, 0, 6.01, 7], ["Z"]]
            vb = [0, 0, 12, 14]
        elif icon_shape == "diamond":
            icon_cmds = [["M", 6, 0], ["L", 12, 7], ["L", 6, 14], ["L", 0, 7], ["Z"]]
            vb = [0, 0, 12, 14]
        else:  # square
            icon_cmds = [["M", 0, 0], ["L", 10, 0], ["L", 10, 10], ["L", 0, 10], ["Z"]]
            vb = [0, 0, 10, 10]
        icon_path = _path_commands(
            f"{node_id}_icon",
            icon_cmds,
            vb,
            fill=_solid(icon_color),
        )
        return _group(node_id, children=[icon_path, text_node], layout_mode="flow")

    elif style == "double_line":
        rule_top = _rule_path(f"{node_id}_rule_top", underline_color, 0.4)
        rule_bot = _rule_path(f"{node_id}_rule_bot", underline_color, 0.4)
        return _group(node_id, children=[rule_top, text_node, rule_bot])

    # fallback
    return _group(node_id, children=[text_node])


# ---------------------------------------------------------------------------
# Skills / Experience / Style builders
# ---------------------------------------------------------------------------

def _build_skills_node(design_json: dict, measurements: dict) -> dict:
    """Builds the CHART node for the skills section."""
    skills_cfg = design_json.get("skills_section") or {}
    chart_type = skills_cfg.get("type", "bars")
    # Map to valid chart_type values
    valid_chart_types = {"radar", "bars", "dots", "rings", "venn", "chips", "tag_level", "list"}
    if chart_type not in valid_chart_types:
        chart_type = "bars"

    fill_color = _tohex(skills_cfg.get("fill_color", "#2563eb"), "#2563eb")
    track_color = skills_cfg.get("track_color")
    if track_color:
        track_color = _tohex(track_color, "#e2e8f0")
    columns = int(skills_cfg.get("columns") or 1)

    typo = design_json.get("typography") or {}
    accent = _tohex(typo.get("accent_color", fill_color), fill_color)

    return _chart_node(
        "skills_chart",
        chart_type,
        "skills",
        [fill_color, accent],
        track_color=track_color,
        columns=columns,
    )


def _build_experience_component(design_json: dict) -> dict:
    """
    Builds the component template for a single experience entry.
    Returns a GROUP node with role, period, company, and bullets sub-nodes.
    """
    exp_cfg = design_json.get("experience") or {}
    timeline = exp_cfg.get("timeline", False)
    node_shape = exp_cfg.get("node_shape", "none")
    node_color = _tohex(exp_cfg.get("node_color", "#2d3748"), "#2d3748")
    line_color = _tohex(exp_cfg.get("line_color", "#cbd5e0"), "#cbd5e0")

    children: list[dict] = []

    # Timeline dot/node
    if timeline and node_shape != "none":
        if node_shape == "circle":
            cmds = [["M", 6, 5], ["A", 5, 5, 0, 1, 0, 6.01, 5], ["Z"]]
            vb = [0, 0, 12, 12]
        elif node_shape == "diamond":
            cmds = [["M", 6, 0], ["L", 12, 6], ["L", 6, 12], ["L", 0, 6], ["Z"]]
            vb = [0, 0, 12, 12]
        else:  # square
            cmds = [["M", 0, 0], ["L", 10, 0], ["L", 10, 10], ["L", 0, 10], ["Z"]]
            vb = [0, 0, 10, 10]
        timeline_node = _path_commands(
            "exp_timeline_node",
            cmds,
            vb,
            fill=_solid(node_color),
        )
        children.append(timeline_node)

    children.extend([
        _text_node("exp_role", binding="experience.{i}.role", style_ref="job_role"),
        _text_node("exp_period", binding="experience.{i}.period", style_ref="job_period"),
        _text_node("exp_company", binding="experience.{i}.company", style_ref="job_company"),
        _text_node("exp_bullets", binding="experience.{i}.bullets", style_ref="body"),
    ])

    return _group("exp_entry", children=children)


def _build_style_registry(design_json: dict, measurements: dict) -> dict:
    """
    Builds the style_registry for the document.
    Returns dict with style IDs as keys and TEXT_STYLE dicts as values.
    Standard styles: 'name', 'title', 'section_heading', 'body', 'muted',
                     'job_role', 'job_company', 'job_period', 'label'
    """
    typo = design_json.get("typography") or {}
    heading_font = typo.get("heading_font", "sans")
    body_font = typo.get("body_font", "sans")
    name_case = typo.get("name_case", "upper")
    heading_case = typo.get("heading_case", "upper")
    heading_color = _tohex(
        measurements.get("heading_color") or typo.get("heading_color", "#2d3748"),
        "#2d3748",
    )
    body_color = _tohex(typo.get("body_color", "#374151"), "#374151")
    accent_color = _tohex(typo.get("accent_color", "#2563eb"), "#2563eb")
    muted_color = _tohex(typo.get("accent_color", "#6b7280"), "#6b7280")

    heading_font_family = _font_stack(heading_font)
    body_font_family = _font_stack(body_font)

    heading_ls = {"normal": 0.0, "wide": 1.0, "very_wide": 2.5}.get(
        (design_json.get("section_heading") or {}).get("letter_spacing", "normal"), 0.0
    )
    heading_weight = 900 if (design_json.get("section_heading") or {}).get("weight") == "black" else 700

    # Header text color
    header_fill = (design_json.get("header") or {}).get("fill") or {}
    header_bg = _tohex(
        measurements.get("header_color") or header_fill.get("color", "#2d3748"),
        "#2d3748",
    )
    name_color = _readable_on(header_bg)
    # Override with typography name_color if present
    if typo.get("name_color"):
        name_color = _tohex(typo["name_color"], name_color)

    sidebar_bg = _tohex(measurements.get("sidebar_bg_color", "#2d3748"), "#2d3748")

    def _text_style(
        font_family: str,
        font_weight: int,
        font_size_pt: float,
        color: str,
        text_align: str = "left",
        text_transform: str = "none",
        letter_spacing_pt: float = 0.0,
        line_height_pt: float | None = None,
    ) -> dict:
        return {
            "font_family": font_family,
            "font_weight": font_weight,
            "font_size_pt": font_size_pt,
            "line_height_pt": line_height_pt,
            "letter_spacing_pt": letter_spacing_pt,
            "color": color,
            "text_align": text_align,
            "text_transform": text_transform,
        }

    return {
        "name": _text_style(
            heading_font_family, 900, 22.0, name_color,
            text_align="left",
            text_transform=name_case,
            letter_spacing_pt=1.0,
        ),
        "title": _text_style(
            body_font_family, 400, 11.0, name_color,
            text_align="left",
            text_transform="none",
            letter_spacing_pt=0.3,
        ),
        "section_heading": _text_style(
            heading_font_family, heading_weight, 9.5, heading_color,
            text_align="left",
            text_transform=heading_case,
            letter_spacing_pt=heading_ls,
        ),
        "body": _text_style(
            body_font_family, 400, 9.0, body_color,
            text_align="left",
            line_height_pt=13.0,
        ),
        "muted": _text_style(
            body_font_family, 400, 8.5, muted_color,
            text_align="left",
        ),
        "job_role": _text_style(
            heading_font_family, 600, 10.0, heading_color,
            text_align="left",
        ),
        "job_company": _text_style(
            body_font_family, 500, 9.0, accent_color,
            text_align="left",
        ),
        "job_period": _text_style(
            body_font_family, 400, 8.5, muted_color,
            text_align="left",
            text_transform="none",
        ),
        "label": _text_style(
            body_font_family, 400, 9.0, _readable_on(sidebar_bg),
            text_align="left",
        ),
    }


# ---------------------------------------------------------------------------
# Font stack utility
# ---------------------------------------------------------------------------

def _font_stack(font_type: str) -> str:
    """
    Converts a font type name to a CSS font family stack.
    font_type: 'sans', 'serif', 'mono', 'geometric', 'modern', 'elegant'
    Returns CSS font-family string.
    """
    return _FONT_STACKS.get(str(font_type).lower(), _FONT_STACKS["sans"])


# ---------------------------------------------------------------------------
# Legacy fallback
# ---------------------------------------------------------------------------

def _build_from_legacy(legacy_spec: dict, image_path: str) -> dict:
    """
    Fallback: builds a basic scene graph from a legacy vocabulary-based design dict.
    Used when VLM analysis fails.
    Maps legacy design keys to scene graph nodes.
    Returns a PAGE node.
    """
    colors = legacy_spec.get("colors") or {}
    page_bg = _tohex(colors.get("page_bg", "#ffffff"), "#ffffff")
    sidebar_bg = _tohex(colors.get("sidebar_bg", "#2d3748"), "#2d3748")
    primary = _tohex(colors.get("primary", "#2563eb"), "#2563eb")
    accent = _tohex(colors.get("accent", "#2563eb"), "#2563eb")
    heading_color = _tohex(colors.get("heading", "#1e293b"), "#1e293b")
    text_color = _tohex(colors.get("text", "#374151"), "#374151")
    header_text = _tohex(colors.get("header_text", "#ffffff"), "#ffffff")
    skill_colors = [_tohex(c, primary) for c in (colors.get("skill_colors") or [primary])]

    layout = legacy_spec.get("layout", "sidebar_left")
    sidebar_w = float(legacy_spec.get("sidebar_width") or 33)
    header_style = legacy_spec.get("header", "full_band")
    photo_shape = legacy_spec.get("photo", "circle")
    font_type = legacy_spec.get("font", "sans")
    heading_style = legacy_spec.get("heading_style", "plain")
    skills_style = legacy_spec.get("skills_style", "bars")

    font_family = _font_stack(font_type)
    page_children: list[dict] = []

    # Sidebar background
    if layout in ("sidebar_left", "sidebar_right"):
        if layout == "sidebar_left":
            sb_pos = {"x_mm": 0.0, "y_mm": 0.0}
            sb_size = {"width_mm": None, "width_pct": sidebar_w, "height_mm": 297.0, "height_pct": None}
        else:
            sb_x = 210.0 * (1 - sidebar_w / 100.0)
            sb_pos = {"x_mm": sb_x, "y_mm": 0.0}
            sb_size = {"width_mm": 210.0 - sb_x, "width_pct": None, "height_mm": 297.0, "height_pct": None}

        page_children.append(_frame(
            "sidebar_master",
            children=[],
            layout_mode="absolute",
            page_spanning=True,
            position=sb_pos,
            size=sb_size,
            fill=_solid(sidebar_bg),
            z_index=0,
        ))

    # Header
    if header_style in ("full_band", "diagonal_banner"):
        header_nodes: list[dict] = []
        if photo_shape != "none":
            header_nodes.append(_image_node("photo", 28.0, 28.0, clip_shape=photo_shape))
        header_nodes.append(_text_node("header_name", binding="name", style_ref="name"))
        header_nodes.append(_text_node("header_job_title", binding="job_title", style_ref="title"))
        page_children.append(_frame(
            "header",
            children=header_nodes,
            layout_mode="flow",
            size={"width_mm": None, "width_pct": 100.0, "height_mm": 50.0, "height_pct": None},
            fill=_solid(primary),
            padding={"top_mm": 8.0, "right_mm": 10.0, "bottom_mm": 6.0, "left_mm": 10.0},
            z_index=1,
        ))

    # Columns
    sidebar_sections = legacy_spec.get("sidebar_sections") or []
    main_sections = legacy_spec.get("main_sections") or []

    def _make_section_nodes(keys: list[str], prefix: str) -> list[dict]:
        nodes: list[dict] = []
        for i, key in enumerate(keys):
            heading_text_node = _text_node(
                f"{prefix}_{key}_heading_text",
                binding=f"section_titles.{key}",
                style_ref="section_heading",
            )
            heading = _group(f"{prefix}_{key}_heading", children=[heading_text_node])
            if key == "skills":
                chart_type = skills_style if skills_style in {"bars", "dots", "rings", "venn", "chips", "radar", "tag_level", "list"} else "bars"
                content: list[dict] = [_chart_node(f"{prefix}_{key}_chart", chart_type, "skills", skill_colors)]
            elif key == "experience":
                exp_comp = _build_experience_component({})
                content = [_repeat_node(f"{prefix}_{key}_repeat", "experience", exp_comp)]
            elif key == "education":
                edu_comp = _group("edu_entry", children=[
                    _text_node("edu_degree", binding="education.{i}.degree", style_ref="job_role"),
                    _text_node("edu_institution", binding="education.{i}.institution", style_ref="job_company"),
                    _text_node("edu_year", binding="education.{i}.year", style_ref="job_period"),
                ])
                content = [_repeat_node(f"{prefix}_{key}_repeat", "education", edu_comp)]
            elif key == "contact":
                content = [_group(f"{prefix}_contact_group", children=[
                    _text_node("contact_phone", binding="contact.phone", style_ref="label"),
                    _text_node("contact_email", binding="contact.email", style_ref="label"),
                    _text_node("contact_location", binding="contact.location", style_ref="label"),
                ])]
            else:
                generic_comp = _group(f"{key}_entry", children=[
                    _text_node(f"{key}_item", binding=f"{key}.{{i}}", style_ref="body"),
                ])
                content = [_repeat_node(f"{prefix}_{key}_repeat", key, generic_comp)]
            nodes.append(_group(f"{prefix}_section_{key}", children=[heading] + content))
        return nodes

    sidebar_children = _make_section_nodes(sidebar_sections, "sb")
    main_children = _make_section_nodes(main_sections, "main")
    col_pad = {"top_mm": 5.0, "right_mm": 6.0, "bottom_mm": 5.0, "left_mm": 6.0}

    if layout in ("sidebar_left", "sidebar_right"):
        main_w = 100.0 - sidebar_w
        sb_frame = _frame("sidebar", children=sidebar_children, layout_mode="flow",
                          size={"width_mm": None, "width_pct": sidebar_w, "height_mm": None, "height_pct": None},
                          fill=_no_fill(), padding=col_pad, z_index=1)
        main_frame = _frame("main", children=main_children, layout_mode="flow",
                            size={"width_mm": None, "width_pct": main_w, "height_mm": None, "height_pct": None},
                            fill=_no_fill(), padding=col_pad, z_index=1)
        col_children = [sb_frame, main_frame] if layout == "sidebar_left" else [main_frame, sb_frame]
        page_children.append(_frame("columns", children=col_children, layout_mode="flex_row",
                                    size={"width_mm": None, "width_pct": 100.0, "height_mm": None, "height_pct": None},
                                    fill=_no_fill(), padding={"top_mm": 0, "right_mm": 0, "bottom_mm": 0, "left_mm": 0},
                                    z_index=1))
    else:
        all_children = sidebar_children + main_children
        page_children.append(_frame("main", children=all_children, layout_mode="flow",
                                    size={"width_mm": None, "width_pct": 100.0, "height_mm": None, "height_pct": None},
                                    fill=_no_fill(), padding=col_pad, z_index=1))

    return {
        "type": "page",
        "id": "page",
        "width_mm": 210.0,
        "height_mm": 297.0,
        "background": _solid(page_bg),
        "children": page_children,
    }


# ---------------------------------------------------------------------------
# Key inference helper
# ---------------------------------------------------------------------------

_KEY_PATTERNS = [
    (r"profile|summary|about|objective|introduction|overview", "profile"),
    (r"highlight|key\s+facts|at\s+a\s+glance", "highlights"),
    (r"contact|personal\s+(?:info|details)|reach", "contact"),
    (r"competenc|expertise|strength|core\s+areas", "competencies"),
    (r"skill|abilit", "skills"),
    (r"experience|employment|work\s+history|career\s+history|professional\s+history", "experience"),
    (r"education|academic|qualification|study", "education"),
    (r"achievement|award|honou?r|accomplish", "achievements"),
    (r"certif|training|course|licen", "certifications"),
    (r"language", "languages"),
    (r"interest|hobb|passion", "interests"),
    (r"project|portfolio", "projects"),
    (r"reference|referee", "references"),
]


def _infer_key(title: str) -> str:
    """Infer section key from heading title text."""
    t = (title or "").lower()
    for pattern, key in _KEY_PATTERNS:
        if re.search(pattern, t):
            return key
    return ""
