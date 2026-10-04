# repair + assignment_humanizer

> 26 nodes · cohesion 0.10

## Key Concepts

- **assignment_humanizer.py** (20 connections) — `app/services/assignment_humanizer.py`
- **repair.py** (18 connections) — `app/services/resume_replica/repair.py`
- **base64** (11 connections)
- **compile_replica_html()** (10 connections) — `app/services/resume_replica/compiler.py`
- **run_repair_loop()** (8 connections) — `app/services/resume_replica/repair.py`
- **_humanize_chunk_via_browser()** (6 connections) — `app/services/assignment_humanizer.py`
- **compute_visual_diff()** (5 connections) — `app/services/resume_replica/repair.py`
- **_images_to_base64_pair()** (4 connections) — `app/services/resume_replica/repair.py`
- **_extract_output_text()** (3 connections) — `app/services/assignment_humanizer.py`
- **_fill_input()** (3 connections) — `app/services/assignment_humanizer.py`
- **_find_element()** (3 connections) — `app/services/assignment_humanizer.py`
- **_parse_diff_json()** (3 connections) — `app/services/resume_replica/repair.py`
- **_score_diff_list()** (3 connections) — `app/services/resume_replica/repair.py`
- **Jarvis Assignment Tool — Phase 3: Answer Humanizer…** (1 connections) — `app/services/assignment_humanizer.py`
- **Try multiple CSS selectors to find a visible element.** (1 connections) — `app/services/assignment_humanizer.py`
- **Fill an input area with text using the most reliable method available.** (1 connections) — `app/services/assignment_humanizer.py`
- **Extract text from the output area of the humanizer.** (1 connections) — `app/services/assignment_humanizer.py`
- **Humanize a single text chunk on an already-open browser page. Returns humanized…** (1 connections) — `app/services/assignment_humanizer.py`
- **Main entry point. Returns a complete HTML document string. content : normalised…** (1 connections) — `app/services/resume_replica/compiler.py`
- **_load_and_scale()** (1 connections) — `app/services/resume_replica/repair.py`
- **repair.py — Visual diff and bounded repair loop. Runs after an initial render…** (1 connections) — `app/services/resume_replica/repair.py`
- **Sends both images to the VLM and asks it to describe differences. Returns a…** (1 connections) — `app/services/resume_replica/repair.py`
- **Runs the bounded repair loop: 1. Compare rendered PNG against reference image…** (1 connections) — `app/services/resume_replica/repair.py`
- **Loads two images, downscales if needed, and returns (b64_1, b64_2, mime). Uses…** (1 connections) — `app/services/resume_replica/repair.py`
- **Computes a quality score from a diff list. high severity = -3 points, medium =…** (1 connections) — `app/services/resume_replica/repair.py`
- *... and 1 more nodes in this community*

## Relationships

- [assignment_humanizer](assignment_humanizer.md) (9 shared connections)
- [storage + orchestrator](storage_+_orchestrator.md) (6 shared connections)
- [voice_agent + download_kokoro](voice_agent_+_download_kokoro.md) (5 shared connections)
- [compiler](compiler.md) (5 shared connections)
- [repair](repair.md) (4 shared connections)
- [message_reader + thread_extractor](message_reader_+_thread_extractor.md) (2 shared connections)
- [dynamic_skill + planner](dynamic_skill_+_planner.md) (2 shared connections)
- [ppt_template](ppt_template.md) (1 shared connections)
- [schema](schema.md) (1 shared connections)
- [schema + bindings](schema_+_bindings.md) (1 shared connections)
- [assignment_answers](assignment_answers.md) (1 shared connections)
- [assignment_tool](assignment_tool.md) (1 shared connections)

## Source Files

- `app/services/assignment_humanizer.py`
- `app/services/resume_replica/compiler.py`
- `app/services/resume_replica/repair.py`

## Audit Trail

- EXTRACTED: 77 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*