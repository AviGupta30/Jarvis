# pipeline

> 33 nodes · cohesion 0.10

## Key Concepts

- **pipeline.py** (28 connections) — `app/services/resume_replica/pipeline.py`
- **analyse_reference()** (24 connections) — `app/services/resume_replica/pipeline.py`
- **_font_styles()** (10 connections) — `app/services/resume_replica/pipeline.py`
- **_choose_families()** (7 connections) — `app/services/resume_replica/pipeline.py`
- **ref_map()** (6 connections) — `app/services/resume_replica/fontmatch.py`
- **load_spec()** (6 connections) — `app/services/resume_replica/pipeline.py`
- **_file_hash()** (5 connections) — `app/services/resume_replica/pipeline.py`
- **_section_tokens()** (5 connections) — `app/services/resume_replica/pipeline.py`
- **_core_norm()** (4 connections) — `app/services/resume_replica/fontmatch.py`
- **_ink_top()** (4 connections) — `app/services/resume_replica/pipeline.py`
- **_pitch_of()** (4 connections) — `app/services/resume_replica/pipeline.py`
- **_align()** (3 connections) — `app/services/resume_replica/pipeline.py`
- **_mm()** (3 connections) — `app/services/resume_replica/pipeline.py`
- **spec_path()** (3 connections) — `app/services/resume_replica/pipeline.py`
- **ndarray** (2 connections)
- **run()** (2 connections) — `app/services/resume_replica/integrate.py`
- **line_box()** (2 connections) — `app/services/resume_replica/pipeline.py`
- **best_in()** (2 connections) — `app/services/resume_replica/pipeline.py`
- **total()** (2 connections) — `app/services/resume_replica/pipeline.py`
- **_mostly_lower()** (2 connections) — `app/services/resume_replica/pipeline.py`
- **_style_key()** (2 connections) — `app/services/resume_replica/pipeline.py`
- **Scale so the stroke cores read 1.0 (same rule as the JS side: mean of values…** (1 connections) — `app/services/resume_replica/fontmatch.py`
- **Reference intensity map (0 = background, 1 = text colour) of a line's ink box…** (1 connections) — `app/services/resume_replica/fontmatch.py`
- **_lum()** (1 connections) — `app/services/resume_replica/pipeline.py`
- **pipeline.py — Reference resume (image/PDF) → exact template spec (cached per…** (1 connections) — `app/services/resume_replica/pipeline.py`
- *... and 8 more nodes in this community*

## Relationships

- [fontmatch + fonts](fontmatch_+_fonts.md) (8 shared connections)
- [resume_builder](resume_builder.md) (8 shared connections)
- [exact_render](exact_render.md) (5 shared connections)
- [benchmark + download_kokoro](benchmark_+_download_kokoro.md) (3 shared connections)
- [ingest](ingest.md) (3 shared connections)
- [plate](plate.md) (3 shared connections)
- [measure](measure.md) (2 shared connections)
- [assignment_assembler + smart_navigator](assignment_assembler_+_smart_navigator.md) (1 shared connections)
- [dump_wa_ui + test_wa](dump_wa_ui_+_test_wa.md) (1 shared connections)
- [acoustic_tripwire](acoustic_tripwire.md) (1 shared connections)
- [resume_builder + resume-exact-replica](resume_builder_+_resume-exact-replica.md) (1 shared connections)

## Source Files

- `app/services/resume_replica/fontmatch.py`
- `app/services/resume_replica/integrate.py`
- `app/services/resume_replica/pipeline.py`

## Audit Trail

- EXTRACTED: 85 (98%)
- INFERRED: 2 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*