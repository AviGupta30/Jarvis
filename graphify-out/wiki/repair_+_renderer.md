# repair + renderer

> 28 nodes · cohesion 0.10

## Key Concepts

- **repair.py** (18 connections) — `app/services/resume_replica/repair.py`
- **base64** (11 connections)
- **compile_replica_html()** (10 connections) — `app/services/resume_replica/compiler.py`
- **renderer.py** (10 connections) — `app/services/resume_replica/renderer.py`
- **run_repair_loop()** (8 connections) — `app/services/resume_replica/repair.py`
- **render_replica()** (7 connections) — `app/services/resume_replica/renderer.py`
- **render_to_screenshot()** (6 connections) — `app/services/resume_replica/renderer.py`
- **compute_visual_diff()** (5 connections) — `app/services/resume_replica/repair.py`
- **_launch_browser()** (4 connections) — `app/services/resume_replica/renderer.py`
- **_images_to_base64_pair()** (4 connections) — `app/services/resume_replica/repair.py`
- **_count_pages_and_fill()** (3 connections) — `app/services/resume_replica/renderer.py`
- **_save_pngs()** (3 connections) — `app/services/resume_replica/renderer.py`
- **_parse_diff_json()** (3 connections) — `app/services/resume_replica/repair.py`
- **_score_diff_list()** (3 connections) — `app/services/resume_replica/repair.py`
- **Main entry point. Returns a complete HTML document string. content : normalised…** (1 connections) — `app/services/resume_replica/compiler.py`
- **renderer.py — Browser rendering and output verification for replica resumes.…** (1 connections) — `app/services/resume_replica/renderer.py`
- **Launches Chromium (or msedge fallback). Same as resume_builder._launch.** (1 connections) — `app/services/resume_replica/renderer.py`
- **Uses PyMuPDF (fitz) to count pages and measure fill of last page. Returns…** (1 connections) — `app/services/resume_replica/renderer.py`
- **Extracts PNG previews from the PDF using PyMuPDF. Returns list of PNG file…** (1 connections) — `app/services/resume_replica/renderer.py`
- **Renders the compiled HTML to PDF + PNG previews. Uses Playwright Chromium (or…** (1 connections) — `app/services/resume_replica/renderer.py`
- **Renders the HTML to a PNG screenshot (full page). Used by the repair loop to…** (1 connections) — `app/services/resume_replica/renderer.py`
- **_load_and_scale()** (1 connections) — `app/services/resume_replica/repair.py`
- **repair.py — Visual diff and bounded repair loop. Runs after an initial render…** (1 connections) — `app/services/resume_replica/repair.py`
- **Sends both images to the VLM and asks it to describe differences. Returns a…** (1 connections) — `app/services/resume_replica/repair.py`
- **Runs the bounded repair loop: 1. Compare rendered PNG against reference image…** (1 connections) — `app/services/resume_replica/repair.py`
- *... and 3 more nodes in this community*

## Relationships

- [storage + orchestrator](storage_+_orchestrator.md) (8 shared connections)
- [compiler](compiler.md) (5 shared connections)
- [repair](repair.md) (4 shared connections)
- [benchmark + server](benchmark_+_server.md) (3 shared connections)
- [nlp_extractor + download_kokoro](nlp_extractor_+_download_kokoro.md) (2 shared connections)
- [screen_vision + screen_reader](screen_vision_+_screen_reader.md) (2 shared connections)
- [ppt_template](ppt_template.md) (1 shared connections)
- [schema](schema.md) (1 shared connections)
- [schema + bindings](schema_+_bindings.md) (1 shared connections)
- [assignment_answers](assignment_answers.md) (1 shared connections)
- [assignment_humanizer](assignment_humanizer.md) (1 shared connections)
- [assignment_tool](assignment_tool.md) (1 shared connections)

## Source Files

- `app/services/resume_replica/compiler.py`
- `app/services/resume_replica/renderer.py`
- `app/services/resume_replica/repair.py`

## Audit Trail

- EXTRACTED: 72 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*