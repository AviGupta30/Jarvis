"""
repair.py — Visual diff and bounded repair loop.

Runs after an initial render to detect and fix design mismatches by comparing
the rendered output against the reference image.

The repair loop is conservative: it only runs if a reference image is available,
has a hard limit on iterations, and always keeps the best result seen.
"""
from __future__ import annotations
import os
import json
import base64
import copy

MAX_REPAIR_ITERATIONS = 3
REPAIR_ENABLED = True  # Can be set to False to disable repair globally


def run_repair_loop(
    replica_doc: dict,
    content: dict,
    rendered_png_path: str,
    reference_image_path: str,
    photo_uri: str,
    scale: float,
    max_iterations: int = MAX_REPAIR_ITERATIONS,
) -> dict:
    """
    Runs the bounded repair loop:
    1. Compare rendered PNG against reference image using VLM diff
    2. For each high-severity diff, compute a patch
    3. Apply the patch to the replica_doc (modifying the scene graph)
    4. Re-compile and re-render
    5. Accept if improved, revert if worse
    6. Stop after max_iterations or when all diffs are resolved

    Returns the (possibly improved) replica_doc.
    Only modifies the in-memory replica_doc, does NOT save it.
    If reference_image_path is empty or rendering fails, returns replica_doc unchanged.
    """
    if not REPAIR_ENABLED:
        return replica_doc

    if not reference_image_path or not os.path.isfile(reference_image_path):
        return replica_doc

    if not rendered_png_path or not os.path.isfile(rendered_png_path):
        return replica_doc

    # Compute starting score
    initial_diffs = compute_visual_diff(rendered_png_path, reference_image_path)
    current_score = _score_diff_list(initial_diffs)
    best_doc = copy.deepcopy(replica_doc)
    best_score = current_score
    current_doc = copy.deepcopy(replica_doc)
    current_png = rendered_png_path

    print(f"[repair] Starting repair loop. Initial score={current_score:.2f}, diffs={len(initial_diffs)}")

    for iteration in range(max_iterations):
        diffs = compute_visual_diff(current_png, reference_image_path)
        # Filter to high and medium severity only
        actionable = [d for d in diffs if d.get("severity") in ("high", "medium")]
        if not actionable:
            print(f"[repair] Iteration {iteration + 1}: no actionable diffs — done")
            break

        patched_doc = apply_diff_patches(current_doc, actionable)
        if patched_doc is None:
            print(f"[repair] Iteration {iteration + 1}: no applicable patches — done")
            break

        # Re-compile
        try:
            from app.services.resume_replica.compiler import compile_replica_html as _compile
            new_html = _compile(patched_doc, content, photo_uri, scale)
        except Exception as e:
            print(f"[repair] Iteration {iteration + 1}: compile failed: {e}")
            break

        # Re-render to screenshot
        try:
            from app.services.resume_replica.renderer import render_to_screenshot
            new_png_bytes = render_to_screenshot(new_html)
        except Exception as e:
            print(f"[repair] Iteration {iteration + 1}: render failed: {e}")
            break

        if not new_png_bytes:
            print(f"[repair] Iteration {iteration + 1}: screenshot returned None — skipping")
            break

        # Save the new screenshot temporarily
        import tempfile
        tmp_png = os.path.join(
            tempfile.gettempdir(),
            f"replica_repair_{iteration}_{int(__import__('time').time()*1000)}.png"
        )
        try:
            with open(tmp_png, "wb") as fh:
                fh.write(new_png_bytes)

            new_diffs = compute_visual_diff(tmp_png, reference_image_path)
            new_score = _score_diff_list(new_diffs)
            print(f"[repair] Iteration {iteration + 1}: new_score={new_score:.2f} (was {current_score:.2f})")

            if new_score > current_score:
                # Improvement: accept
                current_score = new_score
                current_doc = copy.deepcopy(patched_doc)
                current_png = tmp_png
                if new_score > best_score:
                    best_score = new_score
                    best_doc = copy.deepcopy(patched_doc)
            else:
                # No improvement: revert current_doc but keep best_doc intact
                print(f"[repair] Iteration {iteration + 1}: no improvement — reverting")
                break
        except Exception as e:
            print(f"[repair] Iteration {iteration + 1}: scoring failed: {e}")
            break
        finally:
            try:
                if os.path.isfile(tmp_png) and tmp_png != rendered_png_path:
                    os.remove(tmp_png)
            except Exception:
                pass

    print(f"[repair] Loop complete. Best score={best_score:.2f}")
    return best_doc


def compute_visual_diff(
    rendered_png_path: str,
    reference_image_path: str,
) -> list[dict]:
    """
    Sends both images to the VLM and asks it to describe differences.
    Returns a list of diff dicts:
    [
        {
            "element": "sidebar",
            "property": "fill",
            "severity": "high"|"medium"|"low",
            "reference_description": "dark navy gradient sidebar",
            "rendered_description": "solid dark sidebar",
            "suggested_fix": "Use linear gradient from #0b2a4a to #183943"
        },
        ...
    ]

    VLM prompt asks:
    'Left image is the reference resume design. Right image is my rendered replica.
    List visual differences you see. Focus on: colors (solid vs gradient), shapes (angles, curves),
    photo frame shape, section heading style, skill visualization type, spacing, fonts.
    Return JSON: {"diffs": [{"element": str, "property": str, "severity": "high|medium|low",
    "reference_description": str, "rendered_description": str, "suggested_fix": str}]}'

    Returns empty list if VLM call fails or no reference available.
    Limits to high+medium diffs only.
    """
    if not rendered_png_path or not reference_image_path:
        return []
    if not os.path.isfile(rendered_png_path) or not os.path.isfile(reference_image_path):
        return []

    combined_b64, _, mime = _images_to_base64_pair(reference_image_path, rendered_png_path)
    if not combined_b64:
        return []

    prompt = (
        "Left image is the reference resume design. Right image is my rendered replica. "
        "List visual differences you see. Focus on: colors (solid vs gradient), shapes (angles, curves), "
        "photo frame shape, section heading style, skill visualization type, spacing, fonts. "
        'Return JSON: {"diffs": [{"element": str, "property": str, "severity": "high|medium|low", '
        '"reference_description": str, "rendered_description": str, "suggested_fix": str}]}'
    )

    raw = ""
    try:
        # Try Groq vision first
        from app.core.config import settings
        from groq import Groq
        client = Groq(api_key=settings.GROQ_API_KEY)
        r = client.chat.completions.create(
            model=settings.GROQ_VISION_MODEL,
            messages=[{"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{combined_b64}"}},
            ]}],
            temperature=0.1,
            max_tokens=2000,
        )
        raw = r.choices[0].message.content or ""
    except Exception as e:
        print(f"[repair] Groq vision diff failed: {str(e)[:120]}")
        # Try Gemini
        try:
            import requests
            from app.core.config import settings
            key = getattr(settings, "GEMINI_API_KEY", "") or os.getenv("GEMINI_API_KEY", "")
            if key:
                parts = [
                    {"text": prompt},
                    {"inline_data": {"mime_type": mime, "data": combined_b64}},
                ]
                r = requests.post(
                    f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-lite-latest:generateContent?key={key}",
                    json={"contents": [{"parts": parts}], "generationConfig": {"temperature": 0.1, "maxOutputTokens": 2000, "responseMimeType": "application/json"}},
                    timeout=60,
                )
                if r.status_code == 200:
                    cand = (r.json().get("candidates") or [{}])[0]
                    raw = "".join(pt.get("text", "") for pt in (cand.get("content") or {}).get("parts", []))
        except Exception as e2:
            print(f"[repair] Gemini diff also failed: {str(e2)[:120]}")

    if not raw:
        return []

    # Parse JSON from raw
    data = _parse_diff_json(raw)
    diffs = data.get("diffs") or []
    if not isinstance(diffs, list):
        return []

    # Normalise and filter
    result = []
    for d in diffs:
        if not isinstance(d, dict):
            continue
        severity = str(d.get("severity") or "low").lower().strip()
        if severity not in ("high", "medium", "low"):
            severity = "low"
        result.append({
            "element": str(d.get("element") or ""),
            "property": str(d.get("property") or ""),
            "severity": severity,
            "reference_description": str(d.get("reference_description") or ""),
            "rendered_description": str(d.get("rendered_description") or ""),
            "suggested_fix": str(d.get("suggested_fix") or ""),
        })

    return result


def apply_diff_patches(
    replica_doc: dict,
    diffs: list[dict],
) -> dict | None:
    """
    Converts VLM diffs into structured patches and applies them to the replica_doc.
    Returns a modified copy of replica_doc, or None if no applicable patches found.

    Patch categories handled:
    - fill/color: update fill in sidebar frame, header frame, or section heading paths
    - gradient: convert solid fill to gradient_linear fill
    - photo_shape: update IMAGE node clip_shape
    - heading_style: rebuild section heading GROUP nodes with new style
    - skill_type: update CHART node chart_type
    - opacity: adjust fill opacity

    Patches are applied to in-memory replica_doc only.
    Returns None if no patches could be applied.
    """
    if not diffs:
        return None

    doc = copy.deepcopy(replica_doc)
    applied = 0

    for diff in diffs:
        element = diff.get("element", "").lower()
        prop = diff.get("property", "").lower()
        fix = diff.get("suggested_fix", "")
        ref_desc = diff.get("reference_description", "").lower()

        # ── fill / color patches ────────────────────────────────────────────
        if prop in ("fill", "color", "background", "gradient"):
            # Determine target frame ID from element name
            target_id = None
            if "sidebar" in element:
                target_id = "sidebar_frame"
            elif "header" in element or "banner" in element:
                target_id = "header_frame"
            elif "heading" in element or "section" in element:
                target_id = "heading_path"

            if target_id:
                # Decide on fill type
                if "gradient" in ref_desc or "gradient" in fix.lower():
                    # Parse gradient from fix description
                    import re
                    hex_colors = re.findall(r"#[0-9a-fA-F]{6}", fix)
                    if len(hex_colors) >= 2:
                        from app.services.resume_replica.schema import make_linear_fill
                        new_fill = make_linear_fill(
                            angle_deg=180.0,
                            stops=[
                                {"offset_pct": 0, "color": hex_colors[0]},
                                {"offset_pct": 100, "color": hex_colors[1]},
                            ],
                        )
                        if _patch_fill(doc, target_id, new_fill):
                            applied += 1
                    elif len(hex_colors) == 1:
                        from app.services.resume_replica.schema import make_solid_fill
                        if _patch_fill(doc, target_id, make_solid_fill(hex_colors[0])):
                            applied += 1
                else:
                    import re
                    hex_colors = re.findall(r"#[0-9a-fA-F]{6}", fix)
                    if hex_colors:
                        from app.services.resume_replica.schema import make_solid_fill
                        if _patch_fill(doc, target_id, make_solid_fill(hex_colors[0])):
                            applied += 1

        # ── photo shape patch ───────────────────────────────────────────────
        elif prop in ("photo_shape", "photo", "clip", "clip_shape", "frame_shape") and "photo" in element:
            shape = "circle"
            ref_lower = ref_desc.lower()
            if "circle" in ref_lower:
                shape = "circle"
            elif "square" in ref_lower:
                shape = "square"
            elif "round" in ref_lower:
                shape = "rounded"
            elif "hexagon" in ref_lower:
                shape = "hexagon"
            # Walk tree and update IMAGE nodes
            from app.services.resume_replica.schema import walk_nodes, NODE_IMAGE
            def _patch_image(node, parent, depth):
                if node.get("type") == NODE_IMAGE:
                    node["clip_shape"] = shape
            walk_nodes(doc.get("scene_graph", {}), _patch_image)
            applied += 1

        # ── skill chart type patch ──────────────────────────────────────────
        elif prop in ("skill_type", "chart_type", "skill_visualization") and "skill" in element:
            chart_type = "bars"
            ref_lower = ref_desc.lower()
            if "dot" in ref_lower:
                chart_type = "dots"
            elif "bar" in ref_lower:
                chart_type = "bars"
            elif "ring" in ref_lower or "circle" in ref_lower:
                chart_type = "rings"
            elif "venn" in ref_lower:
                chart_type = "venn"
            elif "chip" in ref_lower or "tag" in ref_lower:
                chart_type = "chips"
            from app.services.resume_replica.schema import walk_nodes, NODE_CHART
            def _patch_chart(node, parent, depth):
                if node.get("type") == NODE_CHART:
                    node["chart_type"] = chart_type
            walk_nodes(doc.get("scene_graph", {}), _patch_chart)
            applied += 1

        # ── opacity patch ───────────────────────────────────────────────────
        elif prop in ("opacity", "transparency") and "sidebar" in element:
            import re
            pct = re.search(r"(\d+)\s*%", fix)
            alpha = float(pct.group(1)) / 100.0 if pct else 0.85
            from app.services.resume_replica.schema import walk_nodes, NODE_FRAME
            def _patch_opacity(node, parent, depth):
                if node.get("type") == NODE_FRAME and node.get("id") == "sidebar_frame":
                    fill = node.get("fill") or {}
                    if fill.get("type") == "solid":
                        fill["opacity"] = alpha
                        node["fill"] = fill
            walk_nodes(doc.get("scene_graph", {}), _patch_opacity)
            applied += 1

    if applied == 0:
        return None
    return doc


def _patch_fill(
    replica_doc: dict,
    target_frame_id: str,
    new_fill: dict,
) -> bool:
    """
    Finds the frame with the given ID in the scene graph and updates its fill.
    Returns True if the frame was found and updated.
    """
    found = [False]
    from app.services.resume_replica.schema import walk_nodes, NODE_FRAME, NODE_PATH

    def _visitor(node, parent, depth):
        if found[0]:
            return
        node_id = node.get("id", "")
        # Match exact ID or partial (e.g. "sidebar_frame" in "main_sidebar_frame")
        if target_frame_id in node_id or node_id == target_frame_id:
            if node.get("type") in (NODE_FRAME, NODE_PATH):
                node["fill"] = new_fill
                found[0] = True

    walk_nodes(replica_doc.get("scene_graph", {}), _visitor)
    return found[0]


def _images_to_base64_pair(path1: str, path2: str) -> tuple[str, str, str]:
    """
    Loads two images, downscales if needed, and returns (b64_1, b64_2, mime).
    Uses the same _image_b64 function from resume_builder.
    For a side-by-side comparison: combines both images side by side into one image.
    Returns (combined_b64, "", "image/jpeg").
    If either image doesn't exist, returns ("", "", "").
    """
    if not os.path.isfile(path1) or not os.path.isfile(path2):
        return "", "", ""

    try:
        import cv2
        import numpy as np

        def _load_and_scale(path: str, max_h: int = 900) -> "np.ndarray | None":
            img = cv2.imread(path)
            if img is None:
                return None
            h, w = img.shape[:2]
            if h > max_h:
                f = max_h / h
                img = cv2.resize(img, (int(w * f), int(h * f)), interpolation=cv2.INTER_AREA)
            return img

        img1 = _load_and_scale(path1)
        img2 = _load_and_scale(path2)
        if img1 is None or img2 is None:
            return "", "", ""

        # Normalise heights
        h1, w1 = img1.shape[:2]
        h2, w2 = img2.shape[:2]
        target_h = max(h1, h2)
        if h1 < target_h:
            pad = np.full((target_h - h1, w1, 3), 255, dtype=np.uint8)
            img1 = np.vstack([img1, pad])
        if h2 < target_h:
            pad = np.full((target_h - h2, w2, 3), 255, dtype=np.uint8)
            img2 = np.vstack([img2, pad])

        # Side-by-side with a 4-px divider
        divider = np.full((target_h, 4, 3), 180, dtype=np.uint8)
        combined = np.hstack([img1, divider, img2])

        ok, buf = cv2.imencode(".jpg", combined, [cv2.IMWRITE_JPEG_QUALITY, 82])
        if not ok:
            return "", "", ""

        b64 = base64.b64encode(buf.tobytes()).decode()
        return b64, "", "image/jpeg"

    except Exception as e:
        print(f"[repair] image pair encoding failed: {e}")
        # Fallback: just encode path1
        try:
            with open(path1, "rb") as fh:
                b64 = base64.b64encode(fh.read()).decode()
            mime = "image/png" if path1.lower().endswith(".png") else "image/jpeg"
            return b64, "", mime
        except Exception:
            return "", "", ""


def _score_diff_list(diffs: list[dict]) -> float:
    """
    Computes a quality score from a diff list.
    high severity = -3 points, medium = -1, low = -0.2.
    Perfect score = 0. Worse = more negative.
    """
    score = 0.0
    weights = {"high": -3.0, "medium": -1.0, "low": -0.2}
    for d in diffs:
        severity = str(d.get("severity") or "low").lower().strip()
        score += weights.get(severity, -0.2)
    return score


# ---------------------------------------------------------------------------
# Internal JSON parser
# ---------------------------------------------------------------------------

def _parse_diff_json(raw: str) -> dict:
    """Robust JSON extractor for VLM responses."""
    import re
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
                    return json.loads(raw[start: i + 1])
                except Exception:
                    return {}
    return {}
