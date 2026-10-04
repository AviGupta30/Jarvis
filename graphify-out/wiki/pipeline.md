# pipeline

> 29 nodes · cohesion 0.11

## Key Concepts

- **pipeline.py** (28 connections) — `app/services/resume_replica/pipeline.py`
- **analyse_reference()** (23 connections) — `app/services/resume_replica/pipeline.py`
- **_font_styles()** (10 connections) — `app/services/resume_replica/pipeline.py`
- **_choose_families()** (7 connections) — `app/services/resume_replica/pipeline.py`
- **load_spec()** (5 connections) — `app/services/resume_replica/pipeline.py`
- **_section_tokens()** (5 connections) — `app/services/resume_replica/pipeline.py`
- **_ink_top()** (4 connections) — `app/services/resume_replica/pipeline.py`
- **_pitch_of()** (4 connections) — `app/services/resume_replica/pipeline.py`
- **load_spec()** (3 connections) — `app/services/resume_replica/exact_render.py`
- **_align()** (3 connections) — `app/services/resume_replica/pipeline.py`
- **_mm()** (3 connections) — `app/services/resume_replica/pipeline.py`
- **spec_path()** (3 connections) — `app/services/resume_replica/pipeline.py`
- **run()** (2 connections) — `app/services/resume_replica/integrate.py`
- **line_box()** (2 connections) — `app/services/resume_replica/pipeline.py`
- **best_in()** (2 connections) — `app/services/resume_replica/pipeline.py`
- **total()** (2 connections) — `app/services/resume_replica/pipeline.py`
- **_file_hash()** (2 connections) — `app/services/resume_replica/pipeline.py`
- **_mostly_lower()** (2 connections) — `app/services/resume_replica/pipeline.py`
- **_style_key()** (2 connections) — `app/services/resume_replica/pipeline.py`
- **_lum()** (1 connections) — `app/services/resume_replica/pipeline.py`
- **pipeline.py — Reference resume (image/PDF) → exact template spec (cached per…** (1 connections) — `app/services/resume_replica/pipeline.py`
- **Designs use 1–3 families: pick the family set that best explains every text…** (1 connections) — `app/services/resume_replica/pipeline.py`
- **Line pitch (mm) of wrapped lines of one style: consecutive same-key lines…** (1 connections) — `app/services/resume_replica/pipeline.py`
- **Ink-top → ink-top gaps between line roles inside one section (mm).** (1 connections) — `app/services/resume_replica/pipeline.py`
- **left / center / right for a stacked group (name + title) from their ink boxes.** (1 connections) — `app/services/resume_replica/pipeline.py`
- *... and 4 more nodes in this community*

## Relationships

- [fontmatch + fonts](fontmatch_+_fonts.md) (8 shared connections)
- [exact_render](exact_render.md) (5 shared connections)
- [resume_builder + integrate](resume_builder_+_integrate.md) (4 shared connections)
- [benchmark + server](benchmark_+_server.md) (3 shared connections)
- [ingest](ingest.md) (3 shared connections)
- [plate](plate.md) (3 shared connections)
- [measure](measure.md) (2 shared connections)
- [nlp_extractor + download_kokoro](nlp_extractor_+_download_kokoro.md) (1 shared connections)
- [assignment_assembler + smart_navigator](assignment_assembler_+_smart_navigator.md) (1 shared connections)
- [dark_enhancement + dark_video_enhancement](dark_enhancement_+_dark_video_enhancement.md) (1 shared connections)
- [resume_builder](resume_builder.md) (1 shared connections)

## Source Files

- `app/services/resume_replica/exact_render.py`
- `app/services/resume_replica/integrate.py`
- `app/services/resume_replica/pipeline.py`

## Audit Trail

- EXTRACTED: 75 (97%)
- INFERRED: 2 (3%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*