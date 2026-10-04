# resume_builder

> 23 nodes · cohesion 0.15

## Key Concepts

- **_sanitize_design()** (12 connections) — `app/services/resume_builder.py`
- **_measure_frame()** (11 connections) — `app/services/resume_builder.py`
- **_rgb()** (11 connections) — `app/services/resume_builder.py`
- **_apply_color()** (10 connections) — `app/services/resume_builder.py`
- **_measure_band()** (10 connections) — `app/services/resume_builder.py`
- **_readable_on()** (10 connections) — `app/services/resume_builder.py`
- **_contrast()** (8 connections) — `app/services/resume_builder.py`
- **_pixel_measurements()** (8 connections) — `app/services/resume_replica/analyzer.py`
- **_css_extra()** (7 connections) — `app/services/resume_builder.py`
- **_lum()** (7 connections) — `app/services/resume_builder.py`
- **_mix()** (7 connections) — `app/services/resume_builder.py`
- **Design vocabulary (what a reference image can map to)** (7 connections) — `docs/features/resume-creator.md`
- **_css()** (5 connections) — `app/services/resume_builder.py`
- **near()** (3 connections) — `app/services/resume_builder.py`
- **near()** (2 connections) — `app/services/resume_builder.py`
- **_is_sidebar()** (2 connections) — `app/services/resume_replica/analyzer.py`
- **ch()** (1 connections) — `app/services/resume_builder.py`
- **Make sure colours stay readable and every section has a home.** (1 connections) — `app/services/resume_builder.py`
- **CSS for the newer design vocabulary (kept apart from _css so older designs…** (1 connections) — `app/services/resume_builder.py`
- **White frame around the coloured blocks (sidebar / header band) in the…** (1 connections) — `app/services/resume_builder.py`
- **Gaps around a light name band (e.g. grey box behind the name next to a…** (1 connections) — `app/services/resume_builder.py`
- **_dominant_color()** (1 connections) — `app/services/resume_replica/analyzer.py`
- **Runs pixel-level measurements on the image. Returns dict with keys: -…** (1 connections) — `app/services/resume_replica/analyzer.py`

## Relationships

- [resume_builder](resume_builder.md) (21 shared connections)
- [analyzer](analyzer.md) (15 shared connections)
- [resume_builder + resume-exact-replica](resume_builder_+_resume-exact-replica.md) (12 shared connections)
- [resume_builder + exact_render](resume_builder_+_exact_render.md) (3 shared connections)
- [resume_builder + integrate](resume_builder_+_integrate.md) (2 shared connections)

## Source Files

- `app/services/resume_builder.py`
- `app/services/resume_replica/analyzer.py`
- `docs/features/resume-creator.md`

## Audit Trail

- EXTRACTED: 76 (84%)
- INFERRED: 14 (16%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*