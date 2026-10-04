"""
schema.py — Scene-graph node types, constants, and factory helpers.

A Replica Document is stored as:
{
  "id": str,
  "schema_version": int,
  "reference_hash": str,
  "created_at": float,
  "scene_graph": PAGE_NODE,
  "style_registry": {style_id: TEXT_STYLE},
  "component_registry": {component_id: NODE},
  "measurements": {...}
}
"""

import time
import uuid

# ---------------------------------------------------------------------------
# Version
# ---------------------------------------------------------------------------
SCHEMA_VERSION = 1

# ---------------------------------------------------------------------------
# Node types
# ---------------------------------------------------------------------------
NODE_PAGE    = "page"
NODE_GROUP   = "group"
NODE_FRAME   = "frame"
NODE_TEXT    = "text"
NODE_PATH    = "path"
NODE_IMAGE   = "image"
NODE_RULE    = "rule"
NODE_REPEAT  = "repeat"
NODE_CHART   = "chart"
NODE_MASTER  = "page_master"

# ---------------------------------------------------------------------------
# Fill types
# ---------------------------------------------------------------------------
FILL_SOLID   = "solid"
FILL_LINEAR  = "gradient_linear"
FILL_RADIAL  = "gradient_radial"
FILL_NONE    = "none"

# ---------------------------------------------------------------------------
# Layout modes
# ---------------------------------------------------------------------------
LAYOUT_FLOW      = "flow"
LAYOUT_ABSOLUTE  = "absolute"
LAYOUT_FLEX_ROW  = "flex_row"

# ---------------------------------------------------------------------------
# Chart types
# ---------------------------------------------------------------------------
CHART_RADAR     = "radar"
CHART_BARS      = "bars"
CHART_DOTS      = "dots"
CHART_RINGS     = "rings"
CHART_VENN      = "venn"
CHART_CHIPS     = "chips"
CHART_TAG_LEVEL = "tag_level"
CHART_LIST      = "list"

# ---------------------------------------------------------------------------
# Photo clip shapes
# ---------------------------------------------------------------------------
CLIP_CIRCLE   = "circle"
CLIP_ROUNDED  = "rounded"
CLIP_SQUARE   = "square"
CLIP_HEXAGON  = "hexagon"
CLIP_DIAMOND  = "diamond"
CLIP_SQUIRCLE = "squircle"
CLIP_NONE     = "none"

# ---------------------------------------------------------------------------
# Heading styles (for section headings)
# ---------------------------------------------------------------------------
HEAD_PLAIN               = "plain"
HEAD_UNDERLINE           = "underline"
HEAD_BAR_LEFT            = "bar_left"
HEAD_BAR_RIGHT           = "bar_right"
HEAD_FULL_BG             = "full_bg"
HEAD_ANGLED_BG           = "angled_bg"
HEAD_PILL                = "pill"
HEAD_GRADIENT_UNDERLINE  = "gradient_underline"
HEAD_ICON_BEFORE         = "icon_before"
HEAD_DOUBLE_LINE         = "double_line"

# ---------------------------------------------------------------------------
# Parametric path types
# ---------------------------------------------------------------------------
PARAM_ANGLED_RECT      = "angled_rect"
PARAM_PARALLELOGRAM    = "parallelogram"
PARAM_WAVE             = "wave"
PARAM_DIAGONAL_SPLIT   = "diagonal_split"
PARAM_RECT             = "rect"

# ---------------------------------------------------------------------------
# Section keys (used by bindings.py and others)
# ---------------------------------------------------------------------------
SECTION_KEYS = [
    "profile", "highlights", "contact", "skills", "competencies",
    "experience", "education", "achievements", "certifications",
    "languages", "interests", "projects", "references",
]

# ---------------------------------------------------------------------------
# Valid fill types set (for validation)
# ---------------------------------------------------------------------------
_VALID_FILL_TYPES = {FILL_SOLID, FILL_LINEAR, FILL_RADIAL, FILL_NONE}

# ---------------------------------------------------------------------------
# Factory: fills
# ---------------------------------------------------------------------------

def make_solid_fill(color: str) -> dict:
    """Returns {"type": "solid", "color": color}"""
    return {"type": FILL_SOLID, "color": color}


def make_linear_fill(angle_deg: float, stops: list) -> dict:
    """
    stops = [{"offset_pct": 0, "color": "#hex"}, {"offset_pct": 100, "color": "#hex"}]
    Returns {"type": "gradient_linear", "angle_deg": ..., "stops": [...]}
    """
    return {
        "type": FILL_LINEAR,
        "angle_deg": angle_deg,
        "stops": stops,
    }


def make_radial_fill(cx_pct: float, cy_pct: float, stops: list) -> dict:
    """Returns {"type": "gradient_radial", "cx_pct": ..., "cy_pct": ..., "stops": [...]}"""
    return {
        "type": FILL_RADIAL,
        "cx_pct": cx_pct,
        "cy_pct": cy_pct,
        "stops": stops,
    }


def make_no_fill() -> dict:
    """Returns {"type": "none"}"""
    return {"type": FILL_NONE}


# ---------------------------------------------------------------------------
# Factory: text style
# ---------------------------------------------------------------------------

def make_text_style(
    font_family: str = "'Roboto', Arial, sans-serif",
    font_weight: int = 400,
    font_size_pt: float = 9.6,
    line_height_pt: float = None,
    letter_spacing_pt: float = 0.0,
    color: str = "#333333",
    text_align: str = "left",
    text_transform: str = "none",
) -> dict:
    """Returns a complete TEXT_STYLE dict."""
    style = {
        "font_family": font_family,
        "font_weight": font_weight,
        "font_size_pt": font_size_pt,
        "line_height_pt": line_height_pt if line_height_pt is not None else round(font_size_pt * 1.4, 4),
        "letter_spacing_pt": letter_spacing_pt,
        "color": color,
        "text_align": text_align,
        "text_transform": text_transform,
    }
    return style


# ---------------------------------------------------------------------------
# Factory: nodes
# ---------------------------------------------------------------------------

def make_page_node(
    width_mm: float = 210.0,
    height_mm: float = 297.0,
    background: dict = None,
    children: list = None,
) -> dict:
    """Returns a complete PAGE node."""
    return {
        "type": NODE_PAGE,
        "id": "page_root",
        "width_mm": width_mm,
        "height_mm": height_mm,
        "background": background if background is not None else make_solid_fill("#ffffff"),
        "children": children if children is not None else [],
    }


def make_frame_node(
    node_id: str,
    layout_mode: str = LAYOUT_FLOW,
    page_spanning: bool = False,
    position: dict = None,
    size: dict = None,
    fill: dict = None,
    padding: dict = None,
    children: list = None,
    z_index: int = 1,
) -> dict:
    """Returns a complete FRAME node."""
    return {
        "type": NODE_FRAME,
        "id": node_id,
        "layout_mode": layout_mode,
        "page_spanning": page_spanning,
        "position": position if position is not None else {},
        "size": size if size is not None else {},
        "fill": fill if fill is not None else make_no_fill(),
        "padding": padding if padding is not None else make_padding(),
        "children": children if children is not None else [],
        "z_index": z_index,
    }


def make_group_node(
    node_id: str,
    layout_mode: str = LAYOUT_FLOW,
    children: list = None,
    style: dict = None,
) -> dict:
    """Returns a complete GROUP node."""
    return {
        "type": NODE_GROUP,
        "id": node_id,
        "layout_mode": layout_mode,
        "children": children if children is not None else [],
        "style": style if style is not None else {},
    }


def make_text_node(
    node_id: str,
    binding: str = None,
    literal: str = None,
    style_ref: str = None,
    style: dict = None,
    placeholder: str = None,
) -> dict:
    """Returns a complete TEXT node."""
    node = {
        "type": NODE_TEXT,
        "id": node_id,
    }
    if binding is not None:
        node["binding"] = binding
    if literal is not None:
        node["literal"] = literal
    if style_ref is not None:
        node["style_ref"] = style_ref
    if style is not None:
        node["style"] = style
    if placeholder is not None:
        node["placeholder"] = placeholder
    return node


def make_path_node(
    node_id: str,
    geometry: dict,
    fill: dict = None,
    stroke: dict = None,
) -> dict:
    """Returns a complete PATH node."""
    node = {
        "type": NODE_PATH,
        "id": node_id,
        "geometry": geometry,
        "fill": fill if fill is not None else make_no_fill(),
    }
    if stroke is not None:
        node["stroke"] = stroke
    return node


def make_image_node(
    node_id: str,
    binding: str = "photo",
    size: dict = None,
    clip_shape: str = CLIP_CIRCLE,
    clip_radius_pct: float = 14.0,
    ring: dict = None,
) -> dict:
    """Returns a complete IMAGE node."""
    node = {
        "type": NODE_IMAGE,
        "id": node_id,
        "binding": binding,
        "size": size if size is not None else make_size(width_mm=30.0, height_mm=30.0),
        "clip_shape": clip_shape,
        "clip_radius_pct": clip_radius_pct,
    }
    if ring is not None:
        node["ring"] = ring
    return node


def make_rule_node(
    node_id: str,
    direction: str = "horizontal",
    color: str = "#e5e7eb",
    thickness_pt: float = 1.0,
    opacity: float = 1.0,
) -> dict:
    """Returns a complete RULE node."""
    return {
        "type": NODE_RULE,
        "id": node_id,
        "direction": direction,
        "color": color,
        "thickness_pt": thickness_pt,
        "opacity": opacity,
    }


def make_repeat_node(
    node_id: str,
    binding: str,
    component: dict,
    gap_mm: float = 4.0,
    heading_node: dict = None,
) -> dict:
    """Returns a complete REPEAT node."""
    node = {
        "type": NODE_REPEAT,
        "id": node_id,
        "binding": binding,
        "component": component,
        "gap_mm": gap_mm,
    }
    if heading_node is not None:
        node["heading_node"] = heading_node
    return node


def make_chart_node(
    node_id: str,
    chart_type: str,
    binding: str,
    colors: list,
    track_color: str = None,
    columns: int = 1,
) -> dict:
    """Returns a complete CHART node."""
    node = {
        "type": NODE_CHART,
        "id": node_id,
        "chart_type": chart_type,
        "binding": binding,
        "colors": colors,
        "columns": columns,
    }
    if track_color is not None:
        node["track_color"] = track_color
    return node


# ---------------------------------------------------------------------------
# Factory: geometry
# ---------------------------------------------------------------------------

def make_commands_geometry(commands: list, view_box: list) -> dict:
    """
    Returns a PATH_GEOMETRY with type='commands'.
    commands: list of ["M",x,y], ["L",x,y], ["Q",cx,cy,x,y], ["Z"] etc.
    view_box: [x, y, w, h]
    """
    return {
        "type": "commands",
        "commands": commands,
        "view_box": view_box,
    }


def make_parametric_geometry(parametric_type: str, params: dict) -> dict:
    """
    Returns a PATH_GEOMETRY with type='parametric'.
    parametric_type: one of PARAM_* constants
    params: dict of parameters specific to the shape
      For PARAM_ANGLED_RECT:    {"width": w, "height": h, "slant": s, "direction": "right"|"left"}
      For PARAM_PARALLELOGRAM:  {"width": w, "height": h, "slant": s}
      For PARAM_WAVE:           {"width": w, "height": h, "amplitude": a, "phase": p}
      For PARAM_DIAGONAL_SPLIT: {"width": w, "height": h, "split_x": x}
      For PARAM_RECT:           {"width": w, "height": h, "rx": r}  # rx = corner radius
    """
    return {
        "type": "parametric",
        "parametric_type": parametric_type,
        "params": params,
    }


# ---------------------------------------------------------------------------
# Factory: misc helpers
# ---------------------------------------------------------------------------

def make_ring_spec(color: str, width_mm: float = 2.0, gap_mm: float = 1.0) -> dict:
    """Returns {"color": ..., "width_mm": ..., "gap_mm": ...}"""
    return {"color": color, "width_mm": width_mm, "gap_mm": gap_mm}


def make_padding(
    top_mm: float = 0.0,
    right_mm: float = 0.0,
    bottom_mm: float = 0.0,
    left_mm: float = 0.0,
) -> dict:
    """Returns {"top_mm": ..., "right_mm": ..., "bottom_mm": ..., "left_mm": ...}"""
    return {
        "top_mm": top_mm,
        "right_mm": right_mm,
        "bottom_mm": bottom_mm,
        "left_mm": left_mm,
    }


def make_size(
    width_mm: float = None,
    width_pct: float = None,
    height_mm: float = None,
    height_pct: float = None,
) -> dict:
    """Returns size dict, only including non-None values."""
    size = {}
    if width_mm is not None:
        size["width_mm"] = width_mm
    if width_pct is not None:
        size["width_pct"] = width_pct
    if height_mm is not None:
        size["height_mm"] = height_mm
    if height_pct is not None:
        size["height_pct"] = height_pct
    return size


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_node(node: dict) -> tuple:
    """
    Validates that a node dict has the required fields for its type.
    Returns (is_valid, error_message). error_message is empty string if valid.
    """
    if not isinstance(node, dict):
        return False, "node must be a dict"

    if "type" not in node:
        return False, "node missing required field 'type'"
    if "id" not in node:
        return False, f"node of type '{node['type']}' missing required field 'id'"

    ntype = node["type"]

    if ntype == NODE_PAGE:
        if not isinstance(node.get("children"), list):
            return False, "PAGE node must have a 'children' list"

    elif ntype == NODE_FRAME:
        if "layout_mode" not in node:
            return False, f"FRAME '{node['id']}' missing 'layout_mode'"
        if "size" not in node:
            return False, f"FRAME '{node['id']}' missing 'size'"
        if not isinstance(node.get("children"), list):
            return False, f"FRAME '{node['id']}' must have a 'children' list"

    elif ntype == NODE_TEXT:
        if "binding" not in node and "literal" not in node:
            return False, f"TEXT '{node['id']}' must have at least one of 'binding' or 'literal'"

    elif ntype == NODE_PATH:
        if "geometry" not in node:
            return False, f"PATH '{node['id']}' missing 'geometry'"

    elif ntype == NODE_IMAGE:
        if "size" not in node:
            return False, f"IMAGE '{node['id']}' missing 'size'"
        if "clip_shape" not in node:
            return False, f"IMAGE '{node['id']}' missing 'clip_shape'"

    elif ntype == NODE_REPEAT:
        if "binding" not in node:
            return False, f"REPEAT '{node['id']}' missing 'binding'"
        if "component" not in node:
            return False, f"REPEAT '{node['id']}' missing 'component'"

    elif ntype == NODE_CHART:
        if "chart_type" not in node:
            return False, f"CHART '{node['id']}' missing 'chart_type'"
        if "binding" not in node:
            return False, f"CHART '{node['id']}' missing 'binding'"
        if "colors" not in node:
            return False, f"CHART '{node['id']}' missing 'colors'"

    # Validate fills where present
    for fill_key in ("fill", "background"):
        if fill_key in node:
            fill = node[fill_key]
            if not isinstance(fill, dict):
                return False, f"'{fill_key}' in node '{node['id']}' must be a dict"
            if fill.get("type") not in _VALID_FILL_TYPES:
                return False, (
                    f"'{fill_key}' in node '{node['id']}' has invalid type '{fill.get('type')}'; "
                    f"must be one of {sorted(_VALID_FILL_TYPES)}"
                )

    return True, ""


# ---------------------------------------------------------------------------
# Graph traversal
# ---------------------------------------------------------------------------

def walk_nodes(root: dict, visitor):
    """
    Depth-first traversal of the scene graph.
    visitor(node, parent, depth) is called for each node.
    """
    def _walk(node, parent, depth):
        visitor(node, parent, depth)
        # Walk children list (used by PAGE, FRAME, GROUP)
        for child in node.get("children", []):
            _walk(child, node, depth + 1)
        # Walk heading_node (REPEAT)
        if "heading_node" in node and node["heading_node"] is not None:
            _walk(node["heading_node"], node, depth + 1)
        # Walk component (REPEAT)
        if "component" in node and node["component"] is not None:
            _walk(node["component"], node, depth + 1)

    _walk(root, None, 0)


def collect_bindings(root: dict) -> list:
    """
    Returns all unique binding paths referenced in the scene graph.
    E.g. ["name", "title", "experience", "section_titles.experience", ...]
    """
    seen = set()
    result = []

    def _visit(node, parent, depth):
        binding = node.get("binding")
        if binding and binding not in seen:
            seen.add(binding)
            result.append(binding)

    walk_nodes(root, _visit)
    return result


# ---------------------------------------------------------------------------
# Binding resolution
# ---------------------------------------------------------------------------

def resolve_binding(content: dict, path: str):
    """
    Resolves a dot-separated binding path against the content dict.
    'name'                      -> content['name']
    'section_titles.experience' -> content.get('section_titles', {}).get('experience', '')
    'experience'                -> content['experience'] (list)
    'experience.0.role'         -> content['experience'][0]['role']
    Returns None if path not found.
    """
    if not path:
        return None

    parts = path.split(".")
    current = content

    for part in parts:
        if current is None:
            return None
        if isinstance(current, list):
            # Try to interpret part as an integer index
            try:
                idx = int(part)
                if 0 <= idx < len(current):
                    current = current[idx]
                else:
                    return None
            except ValueError:
                return None
        elif isinstance(current, dict):
            current = current.get(part)
        else:
            return None

    return current


# ---------------------------------------------------------------------------
# Replica document skeleton
# ---------------------------------------------------------------------------

def make_default_replica_document(reference_hash: str) -> dict:
    """
    Returns a skeleton replica document with an empty scene graph.
    The caller is expected to populate 'scene_graph', 'style_registry',
    'component_registry', and 'measurements' before saving.
    """
    return {
        "id": reference_hash,
        "schema_version": SCHEMA_VERSION,
        "reference_hash": reference_hash,
        "created_at": time.time(),
        "scene_graph": make_page_node(),
        "style_registry": {},
        "component_registry": {},
        "measurements": {},
    }
