# repair

> 14 nodes · cohesion 0.19

## Key Concepts

- **repair.py** (18 connections) — `app/services/resume_replica/repair.py`
- **base64** (11 connections)
- **run_repair_loop()** (8 connections) — `app/services/resume_replica/repair.py`
- **compute_visual_diff()** (5 connections) — `app/services/resume_replica/repair.py`
- **_images_to_base64_pair()** (4 connections) — `app/services/resume_replica/repair.py`
- **_parse_diff_json()** (3 connections) — `app/services/resume_replica/repair.py`
- **_score_diff_list()** (3 connections) — `app/services/resume_replica/repair.py`
- **_load_and_scale()** (1 connections) — `app/services/resume_replica/repair.py`
- **repair.py — Visual diff and bounded repair loop. Runs after an initial render…** (1 connections) — `app/services/resume_replica/repair.py`
- **Sends both images to the VLM and asks it to describe differences. Returns a…** (1 connections) — `app/services/resume_replica/repair.py`
- **Runs the bounded repair loop: 1. Compare rendered PNG against reference image…** (1 connections) — `app/services/resume_replica/repair.py`
- **Loads two images, downscales if needed, and returns (b64_1, b64_2, mime). Uses…** (1 connections) — `app/services/resume_replica/repair.py`
- **Computes a quality score from a diff list. high severity = -3 points, medium =…** (1 connections) — `app/services/resume_replica/repair.py`
- **Robust JSON extractor for VLM responses.** (1 connections) — `app/services/resume_replica/repair.py`

## Relationships

- [repair](repair.md) (4 shared connections)
- [storage + orchestrator](storage_+_orchestrator.md) (4 shared connections)
- [benchmark + download_kokoro](benchmark_+_download_kokoro.md) (2 shared connections)
- [compiler](compiler.md) (2 shared connections)
- [screen_vision + screen_reader](screen_vision_+_screen_reader.md) (2 shared connections)
- [ppt_template](ppt_template.md) (1 shared connections)
- [schema](schema.md) (1 shared connections)
- [schema + bindings](schema_+_bindings.md) (1 shared connections)
- [assignment_answers](assignment_answers.md) (1 shared connections)
- [assignment_humanizer](assignment_humanizer.md) (1 shared connections)
- [assignment_tool + assignment_pipeline](assignment_tool_+_assignment_pipeline.md) (1 shared connections)
- [gmail_tool + memory_tool](gmail_tool_+_memory_tool.md) (1 shared connections)

## Source Files

- `app/services/resume_replica/repair.py`

## Audit Trail

- EXTRACTED: 42 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*