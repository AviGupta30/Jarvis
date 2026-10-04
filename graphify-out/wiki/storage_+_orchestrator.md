# storage + orchestrator

> 48 nodes · cohesion 0.07

## Key Concepts

- **orchestrator.py** (20 connections) — `app/services/resume_replica/orchestrator.py`
- **storage.py** (12 connections) — `app/services/resume_replica/storage.py`
- **create_replica_resume()** (10 connections) — `app/services/resume_replica/orchestrator.py`
- **renderer.py** (10 connections) — `app/services/resume_replica/renderer.py`
- **build_replica()** (8 connections) — `app/services/resume_replica/orchestrator.py`
- **render_replica()** (7 connections) — `app/services/resume_replica/renderer.py`
- **compile_replica_html()** (6 connections) — `app/services/resume_replica/orchestrator.py`
- **render_to_screenshot()** (6 connections) — `app/services/resume_replica/renderer.py`
- **get_document_path()** (6 connections) — `app/services/resume_replica/storage.py`
- **load_replica_document()** (6 connections) — `app/services/resume_replica/storage.py`
- **save_replica_document()** (6 connections) — `app/services/resume_replica/storage.py`
- **resume_replica/__init__.py** (5 connections) — `app/services/resume_replica/__init__.py`
- **_ensure_dir()** (5 connections) — `app/services/resume_replica/storage.py`
- **has_replica_document()** (5 connections) — `app/services/resume_replica/storage.py`
- **_launch_browser()** (4 connections) — `app/services/resume_replica/renderer.py`
- **verify_render_basic()** (4 connections) — `app/services/resume_replica/renderer.py`
- **delete_replica_document()** (4 connections) — `app/services/resume_replica/storage.py`
- **prune_old_documents()** (4 connections) — `app/services/resume_replica/storage.py`
- **_compute_fit_scale()** (3 connections) — `app/services/resume_replica/orchestrator.py`
- **_data_uri()** (3 connections) — `app/services/resume_replica/orchestrator.py`
- **_design_with_replica()** (3 connections) — `app/services/resume_replica/orchestrator.py`
- **_count_pages_and_fill()** (3 connections) — `app/services/resume_replica/renderer.py`
- **_save_pngs()** (3 connections) — `app/services/resume_replica/renderer.py`
- **list_replica_documents()** (3 connections) — `app/services/resume_replica/storage.py`
- **resume_replica — Scene-graph-based resume replication engine. Import the public…** (1 connections) — `app/services/resume_replica/__init__.py`
- *... and 23 more nodes in this community*

## Relationships

- [benchmark + download_kokoro](benchmark_+_download_kokoro.md) (6 shared connections)
- [repair](repair.md) (4 shared connections)
- [dump_wa_ui + test_wa](dump_wa_ui_+_test_wa.md) (3 shared connections)
- [compiler](compiler.md) (2 shared connections)
- [analyzer](analyzer.md) (2 shared connections)
- [schema](schema.md) (1 shared connections)

## Source Files

- `app/services/resume_replica/__init__.py`
- `app/services/resume_replica/orchestrator.py`
- `app/services/resume_replica/renderer.py`
- `app/services/resume_replica/storage.py`

## Audit Trail

- EXTRACTED: 94 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*