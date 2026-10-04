# resume_builder + resume-creator

> 28 nodes · cohesion 0.10

## Key Concepts

- **_analyse_design()** (16 connections) — `app/services/resume_builder.py`
- **Flow** (16 connections) — `docs/features/resume-creator.md`
- **Resume creator** (16 connections) — `docs/features/resume-creator.md`
- **_resolve_design()** (12 connections) — `app/services/resume_builder.py`
- **1. Why the current creator can't do it (evidence)** (9 connections) — `docs/plans/resume-exact-replica.md`
- **_palette()** (8 connections) — `app/services/resume_builder.py`
- **_grow_photo_box()** (7 connections) — `app/services/resume_builder.py`
- **_image_b64()** (7 connections) — `app/services/resume_builder.py`
- **_crop_photo()** (6 connections) — `app/services/resume_builder.py`
- **_apply_layout_answer()** (5 connections) — `app/services/resume_builder.py`
- **_merge_design()** (5 connections) — `app/services/resume_builder.py`
- **_file_hash()** (5 connections) — `app/services/resume_replica/pipeline.py`
- **_closest_preset()** (3 connections) — `app/services/resume_builder.py`
- **Purpose** (3 connections) — `docs/features/resume-creator.md`
- **_title_key()** (2 connections) — `app/services/resume_builder.py`
- **Data/config** (2 connections) — `docs/features/resume-creator.md`
- **UI** (2 connections) — `docs/features/resume-creator.md`
- **Step 1: Measure (local CV, no LLM)** (2 connections) — `docs/plans/resume-exact-replica.md`
- **flat()** (1 connections) — `app/services/resume_builder.py`
- **Returns (design, note) — note is a human line about where the design came from.** (1 connections) — `app/services/resume_builder.py`
- **Dominant colours (hex, share) — gives the VLM exact values to pick from.** (1 connections) — `app/services/resume_builder.py`
- **Grow from the face outwards until each edge hits a flat (uniform) line = the…** (1 connections) — `app/services/resume_builder.py`
- **Cut the portrait out of the reference resume: face-anchored edge growth → VLM…** (1 connections) — `app/services/resume_builder.py`
- **Downscaled JPEG (a 1080x2400 phone screenshot costs far fewer vision tokens at…** (1 connections) — `app/services/resume_builder.py`
- **resume-creator.md** (1 connections) — `docs/features/resume-creator.md`
- *... and 3 more nodes in this community*

## Relationships

- [resume_builder](resume_builder.md) (24 shared connections)
- [resume_builder + resume-exact-replica](resume_builder_+_resume-exact-replica.md) (13 shared connections)
- [resume_builder + integrate](resume_builder_+_integrate.md) (8 shared connections)
- [analyzer](analyzer.md) (7 shared connections)
- [plate](plate.md) (2 shared connections)
- [pipeline](pipeline.md) (2 shared connections)
- [chat](chat.md) (1 shared connections)
- [measure](measure.md) (1 shared connections)

## Source Files

- `app/services/resume_builder.py`
- `app/services/resume_replica/pipeline.py`
- `docs/features/resume-creator.md`
- `docs/plans/resume-exact-replica.md`

## Audit Trail

- EXTRACTED: 65 (67%)
- INFERRED: 32 (33%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*