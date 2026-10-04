# exact_render

> 18 nodes · cohesion 0.12

## Key Concepts

- **render_replica_html()** (16 connections) — `app/services/resume_replica/exact_render.py`
- **_place_sections()** (10 connections) — `app/services/resume_replica/exact_render.py`
- **_est_height()** (7 connections) — `app/services/resume_replica/exact_render.py`
- **embed_css()** (5 connections) — `app/services/resume_replica/fonts.py`
- **_bg_grid()** (4 connections) — `app/services/resume_replica/exact_render.py`
- **canon_title()** (3 connections) — `app/services/resume_replica/exact_render.py`
- **_template_section()** (3 connections) — `app/services/resume_replica/exact_render.py`
- **_has()** (2 connections) — `app/services/resume_replica/exact_render.py`
- **bottom()** (2 connections) — `app/services/resume_replica/exact_render.py`
- **lines()** (1 connections) — `app/services/resume_replica/exact_render.py`
- **home()** (1 connections) — `app/services/resume_replica/exact_render.py`
- **kind()** (1 connections) — `app/services/resume_replica/exact_render.py`
- **Coarse RGB grid of both background plates (for the contrast guard).** (1 connections) — `app/services/resume_replica/exact_render.py`
- **Per column: [(ref_section or template section, content key, title,…** (1 connections) — `app/services/resume_replica/exact_render.py`
- **Rough height (mm) of a section in this column: heading + wrapped lines × the…** (1 connections) — `app/services/resume_replica/exact_render.py`
- **A section of this column to borrow heading decoration / styles / rhythm from.** (1 connections) — `app/services/resume_replica/exact_render.py`
- **OCR'd heading → a properly spelled/spaced title ("PERSONALINFORMATION" →…** (1 connections) — `app/services/resume_replica/exact_render.py`
- **@font-face rules with the font files inlined (base64) — for the final resume…** (1 connections) — `app/services/resume_replica/fonts.py`

## Relationships

- [exact_render](exact_render.md) (14 shared connections)
- [resume_builder](resume_builder.md) (4 shared connections)
- [resume_builder + integrate](resume_builder_+_integrate.md) (3 shared connections)
- [pipeline](pipeline.md) (2 shared connections)
- [fontmatch + fonts](fontmatch_+_fonts.md) (1 shared connections)
- [benchmark + server](benchmark_+_server.md) (1 shared connections)

## Source Files

- `app/services/resume_replica/exact_render.py`
- `app/services/resume_replica/fonts.py`

## Audit Trail

- EXTRACTED: 40 (93%)
- INFERRED: 3 (7%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*