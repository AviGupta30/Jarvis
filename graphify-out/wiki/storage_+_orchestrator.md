# storage + orchestrator

> 36 nodes · cohesion 0.09

## Key Concepts

- **orchestrator.py** (20 connections) — `app/services/resume_replica/orchestrator.py`
- **storage.py** (12 connections) — `app/services/resume_replica/storage.py`
- **create_replica_resume()** (10 connections) — `app/services/resume_replica/orchestrator.py`
- **build_replica()** (8 connections) — `app/services/resume_replica/orchestrator.py`
- **compile_replica_html()** (6 connections) — `app/services/resume_replica/orchestrator.py`
- **get_document_path()** (6 connections) — `app/services/resume_replica/storage.py`
- **load_replica_document()** (6 connections) — `app/services/resume_replica/storage.py`
- **save_replica_document()** (6 connections) — `app/services/resume_replica/storage.py`
- **resume_replica/__init__.py** (5 connections) — `app/services/resume_replica/__init__.py`
- **_ensure_dir()** (5 connections) — `app/services/resume_replica/storage.py`
- **has_replica_document()** (5 connections) — `app/services/resume_replica/storage.py`
- **verify_render_basic()** (4 connections) — `app/services/resume_replica/renderer.py`
- **delete_replica_document()** (4 connections) — `app/services/resume_replica/storage.py`
- **prune_old_documents()** (4 connections) — `app/services/resume_replica/storage.py`
- **_compute_fit_scale()** (3 connections) — `app/services/resume_replica/orchestrator.py`
- **_data_uri()** (3 connections) — `app/services/resume_replica/orchestrator.py`
- **_design_with_replica()** (3 connections) — `app/services/resume_replica/orchestrator.py`
- **list_replica_documents()** (3 connections) — `app/services/resume_replica/storage.py`
- **resume_replica — Scene-graph-based resume replication engine. Import the public…** (1 connections) — `app/services/resume_replica/__init__.py`
- **orchestrator.py — Main pipeline for replica resume creation. The public API:…** (1 connections) — `app/services/resume_replica/orchestrator.py`
- **Full pipeline for creating a replica resume from a reference image. Called by…** (1 connections) — `app/services/resume_replica/orchestrator.py`
- **Builds or retrieves a cached replica document for the given image. Steps: 1.…** (1 connections) — `app/services/resume_replica/orchestrator.py`
- **Returns a design dict that has the 'replica' field set so that the renderer…** (1 connections) — `app/services/resume_replica/orchestrator.py`
- **Converts a file to a base64 data URI. Same as resume_builder._data_uri.** (1 connections) — `app/services/resume_replica/orchestrator.py`
- **Computes the next scale to try when over page target. Returns max(min_scale,…** (1 connections) — `app/services/resume_replica/orchestrator.py`
- *... and 11 more nodes in this community*

## Relationships

- [repair + renderer](repair_+_renderer.md) (8 shared connections)
- [benchmark + server](benchmark_+_server.md) (4 shared connections)
- [nlp_extractor + download_kokoro](nlp_extractor_+_download_kokoro.md) (2 shared connections)
- [analyzer](analyzer.md) (2 shared connections)
- [schema](schema.md) (1 shared connections)

## Source Files

- `app/services/resume_replica/__init__.py`
- `app/services/resume_replica/orchestrator.py`
- `app/services/resume_replica/renderer.py`
- `app/services/resume_replica/storage.py`

## Audit Trail

- EXTRACTED: 74 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*