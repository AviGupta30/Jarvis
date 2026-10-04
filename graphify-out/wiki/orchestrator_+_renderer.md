# orchestrator + renderer

> 47 nodes · cohesion 0.07

## Key Concepts

- **orchestrator.py** (20 connections) — `app/services/resume_replica/orchestrator.py`
- **repair.py** (18 connections) — `app/services/resume_replica/repair.py`
- **compile_replica_html()** (10 connections) — `app/services/resume_replica/compiler.py`
- **create_replica_resume()** (10 connections) — `app/services/resume_replica/orchestrator.py`
- **renderer.py** (10 connections) — `app/services/resume_replica/renderer.py`
- **build_replica()** (8 connections) — `app/services/resume_replica/orchestrator.py`
- **run_repair_loop()** (8 connections) — `app/services/resume_replica/repair.py`
- **render_replica()** (7 connections) — `app/services/resume_replica/renderer.py`
- **compile_replica_html()** (6 connections) — `app/services/resume_replica/orchestrator.py`
- **render_to_screenshot()** (6 connections) — `app/services/resume_replica/renderer.py`
- **load_replica_document()** (6 connections) — `app/services/resume_replica/storage.py`
- **resume_replica/__init__.py** (5 connections) — `app/services/resume_replica/__init__.py`
- **compute_visual_diff()** (5 connections) — `app/services/resume_replica/repair.py`
- **_launch_browser()** (4 connections) — `app/services/resume_replica/renderer.py`
- **verify_render_basic()** (4 connections) — `app/services/resume_replica/renderer.py`
- **_images_to_base64_pair()** (4 connections) — `app/services/resume_replica/repair.py`
- **_compute_fit_scale()** (3 connections) — `app/services/resume_replica/orchestrator.py`
- **_data_uri()** (3 connections) — `app/services/resume_replica/orchestrator.py`
- **_design_with_replica()** (3 connections) — `app/services/resume_replica/orchestrator.py`
- **_count_pages_and_fill()** (3 connections) — `app/services/resume_replica/renderer.py`
- **_save_pngs()** (3 connections) — `app/services/resume_replica/renderer.py`
- **_parse_diff_json()** (3 connections) — `app/services/resume_replica/repair.py`
- **_score_diff_list()** (3 connections) — `app/services/resume_replica/repair.py`
- **Main entry point. Returns a complete HTML document string. content : normalised…** (1 connections) — `app/services/resume_replica/compiler.py`
- **resume_replica — Scene-graph-based resume replication engine. Import the public…** (1 connections) — `app/services/resume_replica/__init__.py`
- *... and 22 more nodes in this community*

## Relationships

- [jarvis_overlay + prompt_overlay](jarvis_overlay_+_prompt_overlay.md) (6 shared connections)
- [storage](storage.md) (6 shared connections)
- [compiler](compiler.md) (5 shared connections)
- [repair](repair.md) (4 shared connections)
- [schema](schema.md) (2 shared connections)
- [server + persistence](server_+_persistence.md) (2 shared connections)
- [analyzer](analyzer.md) (2 shared connections)
- [assignment_humanizer](assignment_humanizer.md) (1 shared connections)
- [ppt_template](ppt_template.md) (1 shared connections)
- [schema + bindings](schema_+_bindings.md) (1 shared connections)

## Source Files

- `app/services/resume_replica/__init__.py`
- `app/services/resume_replica/compiler.py`
- `app/services/resume_replica/orchestrator.py`
- `app/services/resume_replica/renderer.py`
- `app/services/resume_replica/repair.py`
- `app/services/resume_replica/storage.py`

## Audit Trail

- EXTRACTED: 103 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*