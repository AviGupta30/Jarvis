# ingest

> 13 nodes · cohesion 0.26

## Key Concepts

- **ingest.py** (12 connections) — `app/services/resume_replica/ingest.py`
- **load_reference()** (9 connections) — `app/services/resume_replica/ingest.py`
- **_trim()** (6 connections) — `app/services/resume_replica/ingest.py`
- **ndarray** (4 connections)
- **_remove_viewer_overlays()** (4 connections) — `app/services/resume_replica/ingest.py`
- **_viewerish()** (4 connections) — `app/services/resume_replica/ingest.py`
- **_uniform()** (3 connections) — `app/services/resume_replica/ingest.py`
- **_imread()** (2 connections) — `app/services/resume_replica/ingest.py`
- **ingest.py — Reference file → clean page image at a fixed working resolution. *…** (1 connections) — `app/services/resume_replica/ingest.py`
- **Returns {img (BGR, page width = 210 mm at PX_PER_MM), page_h_mm, src_dpi,…** (1 connections) — `app/services/resume_replica/ingest.py`
- **Grey/dark colours typical of a viewer background (a white or tinted border is…** (1 connections) — `app/services/resume_replica/ingest.py`
- **Trims uniform viewer-coloured borders. Returns x0, y0, x1, y1.** (1 connections) — `app/services/resume_replica/ingest.py`
- **Phone screenshots carry app overlays on top of the page: Google Lens' dark…** (1 connections) — `app/services/resume_replica/ingest.py`

## Relationships

- [pipeline](pipeline.md) (3 shared connections)
- [resume_campus + measure](resume_campus_+_measure.md) (2 shared connections)
- [benchmark + download_kokoro](benchmark_+_download_kokoro.md) (1 shared connections)
- [acoustic_tripwire](acoustic_tripwire.md) (1 shared connections)
- [measure](measure.md) (1 shared connections)
- [plate](plate.md) (1 shared connections)

## Source Files

- `app/services/resume_replica/ingest.py`

## Audit Trail

- EXTRACTED: 29 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*