# resume_builder

> 22 nodes · cohesion 0.11

## Key Concepts

- **Flow** (16 connections) — `docs/features/resume-creator.md`
- **_analyse_design()** (13 connections) — `app/services/resume_builder.py`
- **_resolve_design()** (9 connections) — `app/services/resume_builder.py`
- **_crop_photo()** (6 connections) — `app/services/resume_builder.py`
- **_pixel_colors()** (6 connections) — `app/services/resume_builder.py`
- **_apply_layout_answer()** (5 connections) — `app/services/resume_builder.py`
- **_grow_photo_box()** (5 connections) — `app/services/resume_builder.py`
- **_save_state()** (5 connections) — `app/services/resume_builder.py`
- **_merge_design()** (4 connections) — `app/services/resume_builder.py`
- **_palette()** (4 connections) — `app/services/resume_builder.py`
- **_face_ratio()** (3 connections) — `app/services/resume_builder.py`
- **_faces()** (3 connections) — `app/services/resume_builder.py`
- **_closest_preset()** (2 connections) — `app/services/resume_builder.py`
- **_file_hash()** (2 connections) — `app/services/resume_builder.py`
- **_title_key()** (2 connections) — `app/services/resume_builder.py`
- **flat()** (1 connections) — `app/services/resume_builder.py`
- **mode()** (1 connections) — `app/services/resume_builder.py`
- **Returns (design, note) — note is a human line about where the design came from.** (1 connections) — `app/services/resume_builder.py`
- **Dominant colours (hex, share) — gives the VLM exact values to pick from.** (1 connections) — `app/services/resume_builder.py`
- **Grow from the face outwards until each edge hits a flat (uniform) line = the…** (1 connections) — `app/services/resume_builder.py`
- **Cut the portrait out of the reference resume: face-anchored edge growth → VLM…** (1 connections) — `app/services/resume_builder.py`
- **Real colours of page / side column / header band from the reference pixels…** (1 connections) — `app/services/resume_builder.py`

## Relationships

- [resume_builder](resume_builder.md) (37 shared connections)
- [resume-creator](resume-creator.md) (2 shared connections)
- [chat + llm](chat_+_llm.md) (1 shared connections)

## Source Files

- `app/services/resume_builder.py`
- `docs/features/resume-creator.md`

## Audit Trail

- EXTRACTED: 48 (73%)
- INFERRED: 18 (27%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*