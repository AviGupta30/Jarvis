# recolor + exact_render

> 19 nodes · cohesion 0.17

## Key Concepts

- **recolor.py** (10 connections) — `app/services/resume_replica/recolor.py`
- **recolor_rgb()** (9 connections) — `app/services/resume_replica/recolor.py`
- **_raster_palette()** (6 connections) — `app/services/resume_builder.py`
- **asset_files()** (6 connections) — `app/services/resume_replica/exact_render.py`
- **palette_of()** (6 connections) — `app/services/resume_replica/recolor.py`
- **dominant()** (5 connections) — `app/services/resume_replica/recolor.py`
- **ndarray** (5 connections)
- **recolor_file()** (5 connections) — `app/services/resume_replica/recolor.py`
- **clean_pairs()** (4 connections) — `app/services/resume_replica/recolor.py`
- **_unique()** (4 connections) — `app/services/resume_replica/recolor.py`
- **walk()** (3 connections) — `app/services/resume_replica/exact_render.py`
- **_hex()** (3 connections) — `app/services/resume_replica/recolor.py`
- **Dominant colours of an exact copy's images (background, heading boxes, icons)…** (1 connections) — `app/services/resume_builder.py`
- **Every image of the copy (background plates, heading boxes, icons, bars...),…** (1 connections) — `app/services/resume_replica/exact_render.py`
- **recolor.py — "change this colour everywhere" for the raster parts of an exact…** (1 connections) — `app/services/resume_replica/recolor.py`
- **PNG bytes of the recoloured image (alpha kept), or None when nothing applies /…** (1 connections) — `app/services/resume_replica/recolor.py`
- **The dominant colours over a set of images (weighted by pixels) as hex, most…** (1 connections) — `app/services/resume_replica/recolor.py`
- **Greedy merge of the most frequent colours → [(colour, pixel count)], most used…** (1 connections) — `app/services/resume_replica/recolor.py`
- **rgb: H×W×3 uint8 (RGB order). Returns a recoloured copy.** (1 connections) — `app/services/resume_replica/recolor.py`

## Relationships

- [exact_render](exact_render.md) (6 shared connections)
- [resume_builder](resume_builder.md) (3 shared connections)
- [resume_builder + integrate](resume_builder_+_integrate.md) (2 shared connections)
- [assignment_answers](assignment_answers.md) (1 shared connections)
- [fontmatch + fonts](fontmatch_+_fonts.md) (1 shared connections)

## Source Files

- `app/services/resume_builder.py`
- `app/services/resume_replica/exact_render.py`
- `app/services/resume_replica/recolor.py`

## Audit Trail

- EXTRACTED: 42 (98%)
- INFERRED: 1 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*