"""
orchestrator.py — Main pipeline for replica resume creation.

The public API:
    build_replica(image_path, reference_hash) -> replica_doc
    compile_replica_html(content, design, photo_uri, scale, edit) -> html_str

The full pipeline (called by create_resume in resume_builder.py):
    create_replica_resume(image_path, content, photo_path, target_pages, out_dir, stem) -> dict
"""
from __future__ import annotations
import os
import json
import time


def build_replica(
    image_path: str,
    reference_hash: str,
    legacy_spec: dict | None = None,
) -> dict | None:
    """
    Builds or retrieves a cached replica document for the given image.

    Steps:
    1. Check storage for existing doc with this reference_hash
    2. If found and schema_version matches, return cached doc
    3. If not found, call analyzer.analyze_reference(image_path, legacy_spec)
    4. Save the result to storage
    5. Return the replica_doc

    Returns None if analysis completely fails (caller falls back to legacy).
    """
    from app.services.resume_replica.storage import (
        load_replica_document,
        save_replica_document,
        has_replica_document,
    )
    from app.services.resume_replica.schema import SCHEMA_VERSION

    if not reference_hash:
        return None

    # 1. Check cache
    if has_replica_document(reference_hash):
        cached = load_replica_document(reference_hash)
        if cached and cached.get("schema_version") == SCHEMA_VERSION:
            print(f"[replica/orchestrator] Loaded cached replica doc: {reference_hash[:12]}…")
            return cached
        # Version mismatch — fall through to re-analyse

    # 2. Run the analyser
    if not image_path or not os.path.isfile(image_path):
        return None

    try:
        from app.services.resume_replica.analyzer import analyze_reference
        replica_doc = analyze_reference(image_path, legacy_spec)
    except Exception as e:
        print(f"[replica/orchestrator] analyze_reference failed: {e}")
        return None

    if not replica_doc:
        return None

    # 3. Persist
    try:
        save_replica_document(replica_doc)
        print(f"[replica/orchestrator] Saved replica doc: {replica_doc.get('id', '?')[:12]}…")
    except Exception as e:
        print(f"[replica/orchestrator] save failed (non-fatal): {e}")

    return replica_doc


def compile_replica_html(
    content: dict,
    design: dict,
    photo_uri: str = "",
    scale: float = 1.0,
    edit: bool = False,
) -> str:
    """
    Compiles a replica document to HTML.

    design must have replica.document_id set.
    Loads the replica_doc from storage.
    Calls compiler.compile_replica_html() with the loaded doc.

    Raises RuntimeError if:
    - design['replica']['document_id'] is missing
    - The replica document cannot be loaded
    - compiler.compile_replica_html raises an exception

    This is called by resume_builder._render_html_inner when the design has a replica field.
    """
    replica_meta = design.get("replica") or {}
    document_id = replica_meta.get("document_id")
    if not document_id:
        raise RuntimeError("[replica] design['replica']['document_id'] is missing")

    from app.services.resume_replica.storage import load_replica_document
    replica_doc = load_replica_document(document_id)
    if replica_doc is None:
        raise RuntimeError(f"[replica] Cannot load replica document '{document_id}'")

    from app.services.resume_replica.compiler import compile_replica_html as _compile
    try:
        html = _compile(content, replica_doc, photo_uri, scale, edit)
    except Exception as e:
        raise RuntimeError(f"[replica] compiler.compile_replica_html failed: {e}") from e

    return html


def create_replica_resume(
    image_path: str,
    content: dict,
    photo_path: str,
    target_pages: int | None,
    out_dir: str,
    stem: str,
    reference_hash: str,
    legacy_spec: dict | None = None,
    legacy_design: dict | None = None,
) -> dict | None:
    """
    Full pipeline for creating a replica resume from a reference image.
    Called by resume_builder.create_resume when image_path is provided.

    Steps:
    1. build_replica(image_path, reference_hash, legacy_spec) -> replica_doc
    2. If replica_doc is None: return None (caller falls back to legacy)
    3. Photo handling: if photo_path, convert to data URI
    4. Compile at scale=1.0: compile_replica_html(content, design_with_replica, photo_uri)
    5. Verify basic render validity
    6. renderer.render_replica(html, stem, out_dir, target_pages) -> files
    7. If target_pages and over page count: re-compile at lower scale
    8. If repair enabled and image_path available:
       a. render_to_screenshot(html) -> rendered_png
       b. repair.run_repair_loop(replica_doc, content, rendered_png, image_path, ...)
       c. If improved: recompile + re-render
    9. Return files dict: {pdf, html, pngs, pages}

    Returns None if any critical step fails (caller falls back to legacy).
    """
    # ── Step 1: Build / retrieve replica doc ────────────────────────────────
    replica_doc = build_replica(image_path, reference_hash, legacy_spec)
    if replica_doc is None:
        print("[replica/orchestrator] build_replica returned None — falling back")
        return None

    # ── Step 2: Photo URI ────────────────────────────────────────────────────
    photo_uri = ""
    if photo_path and os.path.isfile(photo_path):
        photo_uri = _data_uri(photo_path)

    # ── Step 3: Design dict ──────────────────────────────────────────────────
    design = _design_with_replica(replica_doc, legacy_design or {})

    # ── Step 4: Compile at scale 1.0 ────────────────────────────────────────
    scale = 1.0
    try:
        html = compile_replica_html(content, design, photo_uri, scale, edit=False)
    except Exception as e:
        print(f"[replica/orchestrator] Initial compile failed: {e}")
        return None

    # ── Step 5: Basic HTML sanity check ─────────────────────────────────────
    from app.services.resume_replica.renderer import verify_render_basic, render_replica, render_to_screenshot
    valid, reason = verify_render_basic(html)
    if not valid:
        print(f"[replica/orchestrator] HTML verification failed: {reason}")
        return None

    # ── Step 6: Render to PDF ────────────────────────────────────────────────
    os.makedirs(out_dir, exist_ok=True)
    files = render_replica(html, stem, out_dir, target_pages)
    if not files.get("pdf"):
        print("[replica/orchestrator] render_replica returned no PDF")
        return None

    # ── Step 7: Fit loop — re-compile at lower scale if over page target ────
    if target_pages and files.get("pages", 1) > target_pages:
        scale = _compute_fit_scale(files["pages"], target_pages, scale)
        for _attempt in range(5):
            try:
                html = compile_replica_html(content, design, photo_uri, scale, edit=False)
                files = render_replica(html, stem, out_dir, target_pages)
                files["fit_scale"] = scale
            except Exception as e:
                print(f"[replica/orchestrator] fit compile failed at scale={scale:.2f}: {e}")
                break
            if files.get("pages", 1) <= target_pages:
                break
            new_scale = _compute_fit_scale(files["pages"], target_pages, scale)
            if new_scale == scale:
                break
            scale = new_scale

    # ── Step 8: Repair loop ──────────────────────────────────────────────────
    from app.services.resume_replica import repair as _repair_mod
    if _repair_mod.REPAIR_ENABLED and image_path and os.path.isfile(image_path):
        pngs = files.get("pngs") or []
        rendered_png = pngs[0] if pngs else ""

        if rendered_png and os.path.isfile(rendered_png):
            try:
                improved_doc = _repair_mod.run_repair_loop(
                    replica_doc=replica_doc,
                    content=content,
                    rendered_png_path=rendered_png,
                    reference_image_path=image_path,
                    photo_uri=photo_uri,
                    scale=scale,
                )
                # If the doc changed, recompile + re-render
                if improved_doc is not replica_doc:
                    try:
                        repaired_html = compile_replica_html(content, design, photo_uri, scale, edit=False)
                        repaired_files = render_replica(repaired_html, f"{stem}_repaired", out_dir, target_pages)
                        if repaired_files.get("pdf"):
                            # Accept the repaired version: overwrite paths
                            files = repaired_files
                            files["fit_scale"] = scale
                            replica_doc = improved_doc
                    except Exception as e:
                        print(f"[replica/orchestrator] repaired compile/render failed: {e}")
            except Exception as e:
                print(f"[replica/orchestrator] repair loop failed (non-fatal): {e}")

    files["fit_scale"] = scale
    return files


def _design_with_replica(replica_doc: dict, legacy_design: dict) -> dict:
    """
    Returns a design dict that has the 'replica' field set so that
    the renderer dispatch in resume_builder._render_html_inner knows
    to use the replica system.

    Copies legacy_design and adds:
    design['replica'] = {
        'schema_version': 1,
        'enabled': True,
        'document_id': replica_doc['id'],
        'fallback_policy': 'legacy'
    }
    """
    import copy
    design = copy.deepcopy(legacy_design) if legacy_design else {}
    design["replica"] = {
        "schema_version": 1,
        "enabled": True,
        "document_id": replica_doc["id"],
        "fallback_policy": "legacy",
    }
    return design


def _data_uri(path: str) -> str:
    """
    Converts a file to a base64 data URI.
    Same as resume_builder._data_uri.
    """
    import base64
    try:
        ext = os.path.splitext(path)[1].lower().lstrip(".") or "png"
        mime = "image/jpeg" if ext in ("jpg", "jpeg") else f"image/{ext}"
        with open(path, "rb") as fh:
            return f"data:{mime};base64," + base64.b64encode(fh.read()).decode()
    except Exception:
        return ""


def _compute_fit_scale(
    pages: int,
    target_pages: int,
    current_scale: float,
    min_scale: float = 0.74,
) -> float:
    """
    Computes the next scale to try when over page target.
    Returns max(min_scale, current_scale - 0.05).
    Returns current_scale if already at target.
    """
    if pages <= target_pages:
        return current_scale
    next_scale = round(current_scale - 0.05, 4)
    return max(min_scale, next_scale)
