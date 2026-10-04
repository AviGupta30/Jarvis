"""
integrate.py — Glue between resume_builder.create_resume and the exact-replica engine.

create_resume calls, for a reference image/PDF:
    spec = yield from analyse_with_progress(path)      # progress lines stream to the chat
    design = replica_design(spec, previous_design)     # legacy-compatible design dict + {"replica": {...}}
The renderer is chosen in resume_builder._render_html by design["replica"].
Set RESUME_REPLICA=0 to fall back to the old describe-then-pick analysis.
"""
from __future__ import annotations

import os
import queue
import threading


def replica_enabled() -> bool:
    return os.environ.get("RESUME_REPLICA", "1") != "0"


def analyse_with_progress(image_path: str, force: bool = False):
    """Generator: yields progress lines, returns the spec (or None) — use with `yield from`."""
    from .pipeline import analyse_reference
    q: queue.Queue = queue.Queue()
    box: dict = {}

    def run():
        try:
            box["spec"] = analyse_reference(image_path, log=lambda m: q.put(m), force=force)
        except Exception as e:                      # surfaced to the caller, never swallowed silently
            import traceback
            traceback.print_exc()
            box["error"] = e
        finally:
            q.put(None)

    threading.Thread(target=run, daemon=True).start()
    while True:
        msg = q.get()
        if msg is None:
            break
        yield msg.strip() + "\n\n"
    if "error" in box:
        raise box["error"]
    return box.get("spec")


def replica_design(spec: dict, previous: dict | None = None) -> dict:
    """A legacy-compatible design dict carrying the replica reference. The legacy keys keep the rest of the
    builder (editor, fit loop, state) working; layout single_column means the fit loop never moves sections."""
    from app.services import resume_builder as rb
    d = rb._sanitize_design({**{k: v for k, v in rb.PRESETS["modern"].items()}, "source": "image"})
    order = []
    for col in spec.get("columns") or []:
        order += [s["key"] for s in col["sections"] if s["key"] in rb.SECTION_KEYS]
    order += [k for k in rb.SECTION_KEYS if k not in order]
    d.update({"layout": "single_column", "sidebar_sections": [], "main_sections": order, "bottom_sections": [],
              "photo": "circle" if spec.get("photo") else "none",
              "replica": {"sha1": spec["sha1"], "source": spec.get("source", ""), "v": spec.get("v"),
                          "path": spec.get("source_path", "")}})
    if previous and (previous.get("replica") or {}).get("sha1") == spec["sha1"]:
        for k in ("free", "hidden_sections"):            # the editor's custom styling of this same design
            if previous.get(k):
                d[k] = previous[k]
    return d


def replica_note(spec: dict) -> str:
    fams = ", ".join(sorted(spec.get("fonts") or {}))
    note = ("Copied your reference design exactly — its own background, heading boxes, icons and photo frame, "
            f"measured fonts ({fams}), sizes, colours and spacing.")
    dpi = (spec.get("page") or {}).get("src_dpi") or 200
    if dpi < 60:
        note += (f" ⚠️ The reference image is small (~{dpi:.0f} dpi), so thin lines and exact sizes are approximate — "
                 "send a larger screenshot or the PDF for a pixel-exact copy.")
    elif dpi < 100:
        note += f" (Reference resolution ~{dpi:.0f} dpi — a larger image or the PDF gives an even sharper copy.)"
    if (spec.get("page") or {}).get("partial"):
        note += " The picture showed only part of the page; the rest continues the same background."
    return note
