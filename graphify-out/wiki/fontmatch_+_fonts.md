# fontmatch + fonts

> 32 nodes · cohesion 0.10

## Key Concepts

- **fontmatch.py** (14 connections) — `app/services/resume_replica/fontmatch.py`
- **fonts.py** (13 connections) — `app/services/resume_replica/fonts.py`
- **load_index()** (12 connections) — `app/services/resume_replica/fonts.py`
- **FontMatcher** (11 connections) — `app/services/resume_replica/fontmatch.py`
- **identify()** (6 connections) — `app/services/resume_replica/fontmatch.py`
- **ensure_library()** (6 connections) — `app/services/resume_replica/fonts.py`
- **.__enter__()** (5 connections) — `app/services/resume_replica/fontmatch.py`
- **font_face_css()** (5 connections) — `app/services/resume_replica/fonts.py`
- **route_fonts()** (5 connections) — `app/services/resume_replica/fonts.py`
- **all_faces()** (4 connections) — `app/services/resume_replica/fontmatch.py`
- **run_jobs()** (4 connections) — `app/services/resume_replica/fontmatch.py`
- **_worker()** (4 connections) — `app/services/resume_replica/fontmatch.py`
- **.__init__()** (2 connections) — `app/services/resume_replica/exact_render.py`
- **._installed_system_fonts()** (2 connections) — `app/services/resume_replica/fontmatch.py`
- **.match()** (2 connections) — `app/services/resume_replica/fontmatch.py`
- **.metrics()** (2 connections) — `app/services/resume_replica/fontmatch.py`
- **_slug()** (2 connections) — `app/services/resume_replica/fonts.py`
- **.__exit__()** (1 connections) — `app/services/resume_replica/fontmatch.py`
- **.__init__()** (1 connections) — `app/services/resume_replica/fontmatch.py`
- **fontmatch.py — Font identification against the local library (fonts.py), all in…** (1 connections) — `app/services/resume_replica/fontmatch.py`
- **One warm Chromium page with the whole font library loaded. Use as a context…** (1 connections) — `app/services/resume_replica/fontmatch.py`
- **samples: [{text, ref, rw, rh, src_h}] (see ref_map). Returns per sample a…** (1 connections) — `app/services/resume_replica/fontmatch.py`
- **items: [{text, family, weight, ls}] → font/ink metrics in em (for the CSS half-…** (1 connections) — `app/services/resume_replica/fontmatch.py`
- **Runs in a separate process: jobs = [(sample, candidates, top_k)] → result lists.** (1 connections) — `app/services/resume_replica/fontmatch.py`
- **[(sample, candidates, top_k)] → results, spread over worker processes (one…** (1 connections) — `app/services/resume_replica/fontmatch.py`
- *... and 7 more nodes in this community*

## Relationships

- [pipeline](pipeline.md) (8 shared connections)
- [exact_render](exact_render.md) (4 shared connections)
- [acoustic_tripwire](acoustic_tripwire.md) (2 shared connections)
- [benchmark + download_kokoro](benchmark_+_download_kokoro.md) (2 shared connections)
- [assignment_assembler + smart_navigator](assignment_assembler_+_smart_navigator.md) (1 shared connections)
- [server + persistence](server_+_persistence.md) (1 shared connections)

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