# fontmatch + fonts

> 35 nodes · cohesion 0.08

## Key Concepts

- **fontmatch.py** (14 connections) — `app/services/resume_replica/fontmatch.py`
- **load_index()** (12 connections) — `app/services/resume_replica/fonts.py`
- **FontMatcher** (11 connections) — `app/services/resume_replica/fontmatch.py`
- **identify()** (6 connections) — `app/services/resume_replica/fontmatch.py`
- **ref_map()** (6 connections) — `app/services/resume_replica/fontmatch.py`
- **ensure_library()** (6 connections) — `app/services/resume_replica/fonts.py`
- **.__enter__()** (5 connections) — `app/services/resume_replica/fontmatch.py`
- **font_face_css()** (5 connections) — `app/services/resume_replica/fonts.py`
- **route_fonts()** (5 connections) — `app/services/resume_replica/fonts.py`
- **all_faces()** (4 connections) — `app/services/resume_replica/fontmatch.py`
- **_core_norm()** (4 connections) — `app/services/resume_replica/fontmatch.py`
- **run_jobs()** (4 connections) — `app/services/resume_replica/fontmatch.py`
- **_worker()** (4 connections) — `app/services/resume_replica/fontmatch.py`
- **.__init__()** (2 connections) — `app/services/resume_replica/exact_render.py`
- **._installed_system_fonts()** (2 connections) — `app/services/resume_replica/fontmatch.py`
- **.match()** (2 connections) — `app/services/resume_replica/fontmatch.py`
- **.metrics()** (2 connections) — `app/services/resume_replica/fontmatch.py`
- **ndarray** (2 connections)
- **_slug()** (2 connections) — `app/services/resume_replica/fonts.py`
- **.__exit__()** (1 connections) — `app/services/resume_replica/fontmatch.py`
- **.__init__()** (1 connections) — `app/services/resume_replica/fontmatch.py`
- **fontmatch.py — Font identification against the local library (fonts.py), all in…** (1 connections) — `app/services/resume_replica/fontmatch.py`
- **Scale so the stroke cores read 1.0 (same rule as the JS side: mean of values…** (1 connections) — `app/services/resume_replica/fontmatch.py`
- **Reference intensity map (0 = background, 1 = text colour) of a line's ink box…** (1 connections) — `app/services/resume_replica/fontmatch.py`
- **One warm Chromium page with the whole font library loaded. Use as a context…** (1 connections) — `app/services/resume_replica/fontmatch.py`
- *... and 10 more nodes in this community*

## Relationships

- [pipeline](pipeline.md) (8 shared connections)
- [voice_agent + download_kokoro](voice_agent_+_download_kokoro.md) (7 shared connections)
- [exact_render](exact_render.md) (3 shared connections)

## Source Files

- `app/services/resume_replica/exact_render.py`
- `app/services/resume_replica/fontmatch.py`
- `app/services/resume_replica/fonts.py`

## Audit Trail

- EXTRACTED: 65 (98%)
- INFERRED: 1 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*