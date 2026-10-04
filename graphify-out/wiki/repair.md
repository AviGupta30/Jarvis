# repair

> 27 nodes · cohesion 0.10

## Key Concepts

- **repair.py** (18 connections) — `app/services/resume_replica/repair.py`
- **compile_replica_html()** (10 connections) — `app/services/resume_replica/compiler.py`
- **apply_diff_patches()** (10 connections) — `app/services/resume_replica/repair.py`
- **run_repair_loop()** (8 connections) — `app/services/resume_replica/repair.py`
- **compute_visual_diff()** (5 connections) — `app/services/resume_replica/repair.py`
- **_patch_fill()** (5 connections) — `app/services/resume_replica/repair.py`
- **make_solid_fill()** (5 connections) — `app/services/resume_replica/schema.py`
- **_images_to_base64_pair()** (4 connections) — `app/services/resume_replica/repair.py`
- **make_linear_fill()** (4 connections) — `app/services/resume_replica/schema.py`
- **_parse_diff_json()** (3 connections) — `app/services/resume_replica/repair.py`
- **_score_diff_list()** (3 connections) — `app/services/resume_replica/repair.py`
- **Main entry point. Returns a complete HTML document string. content : normalised…** (1 connections) — `app/services/resume_replica/compiler.py`
- **_patch_chart()** (1 connections) — `app/services/resume_replica/repair.py`
- **_patch_image()** (1 connections) — `app/services/resume_replica/repair.py`
- **_patch_opacity()** (1 connections) — `app/services/resume_replica/repair.py`
- **_load_and_scale()** (1 connections) — `app/services/resume_replica/repair.py`
- **_visitor()** (1 connections) — `app/services/resume_replica/repair.py`
- **repair.py — Visual diff and bounded repair loop. Runs after an initial render…** (1 connections) — `app/services/resume_replica/repair.py`
- **Sends both images to the VLM and asks it to describe differences. Returns a…** (1 connections) — `app/services/resume_replica/repair.py`
- **Converts VLM diffs into structured patches and applies them to the replica_doc.…** (1 connections) — `app/services/resume_replica/repair.py`
- **Runs the bounded repair loop: 1. Compare rendered PNG against reference image…** (1 connections) — `app/services/resume_replica/repair.py`
- **Finds the frame with the given ID in the scene graph and updates its fill.…** (1 connections) — `app/services/resume_replica/repair.py`
- **Loads two images, downscales if needed, and returns (b64_1, b64_2, mime). Uses…** (1 connections) — `app/services/resume_replica/repair.py`
- **Computes a quality score from a diff list. high severity = -3 points, medium =…** (1 connections) — `app/services/resume_replica/repair.py`
- **Robust JSON extractor for VLM responses.** (1 connections) — `app/services/resume_replica/repair.py`
- *... and 2 more nodes in this community*

## Relationships

- [compiler](compiler.md) (5 shared connections)
- [storage + orchestrator](storage_+_orchestrator.md) (4 shared connections)
- [schema + bindings](schema_+_bindings.md) (3 shared connections)
- [schema](schema.md) (3 shared connections)
- [renderer](renderer.md) (2 shared connections)
- [social_content_manager + content-tools](social_content_manager_+_content-tools.md) (1 shared connections)
- [assignment_humanizer + task_ledger](assignment_humanizer_+_task_ledger.md) (1 shared connections)
- [screen_vision + screen_reader](screen_vision_+_screen_reader.md) (1 shared connections)
- [ppt_template](ppt_template.md) (1 shared connections)

## Source Files

- `app/services/resume_replica/compiler.py`
- `app/services/resume_replica/repair.py`
- `app/services/resume_replica/schema.py`

## Audit Trail

- EXTRACTED: 52 (93%)
- INFERRED: 4 (7%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*