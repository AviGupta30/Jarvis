# ppt_composer + ppt_designer

> 30 nodes · cohesion 0.10

## Key Concepts

- **render_sections()** (22 connections) — `app/services/ppt_composer.py`
- **render_title_sections()** (17 connections) — `app/services/ppt_composer.py`
- **_section_h()** (12 connections) — `app/services/ppt_composer.py`
- **Composite slides (`ppt_composer.py`, kind `sections`)** (12 connections) — `docs/features/ppt.md`
- **_sizes()** (11 connections) — `app/services/ppt_designer.py`
- **evaluate()** (8 connections) — `app/services/ppt_composer.py`
- **justified_rows()** (7 connections) — `app/services/ppt_designer.py`
- **_fill()** (6 connections) — `app/services/ppt_composer.py`
- **_image_panel()** (6 connections) — `app/services/ppt_composer.py`
- **_norm_sections()** (6 connections) — `app/services/ppt_composer.py`
- **._list_fit()** (6 connections) — `app/services/ppt_designer.py`
- **image_block()** (5 connections) — `app/services/ppt_composer.py`
- **_masonry()** (5 connections) — `app/services/ppt_composer.py`
- **eval_images()** (5 connections) — `app/services/ppt_composer.py`
- **_stretch_cap()** (5 connections) — `app/services/ppt_composer.py`
- **_justified_fixed()** (5 connections) — `app/services/ppt_designer.py`
- **band_h()** (3 connections) — `app/services/ppt_composer.py`
- **search()** (3 connections) — `app/services/ppt_composer.py`
- **._s_sections()** (2 connections) — `app/services/ppt_designer.py`
- **._s_title_sections()** (2 connections) — `app/services/ppt_designer.py`
- **col_h()** (1 connections) — `app/services/ppt_composer.py`
- **Pill + optional section lead + body.** (1 connections) — `app/services/ppt_composer.py`
- **How much extra height a section can absorb before it looks inflated.** (1 connections) — `app/services/ppt_composer.py`
- **Framed images (no crop) + numbered captions under each. Returns used height.** (1 connections) — `app/services/ppt_composer.py`
- **Boxes for the images at full column width in exactly `rows` rows (scaled down…** (1 connections) — `app/services/ppt_composer.py`
- *... and 5 more nodes in this community*

## Relationships

- [ppt_composer + ppt_designer](ppt_composer_+_ppt_designer.md) (35 shared connections)
- [ppt_designer](ppt_designer.md) (27 shared connections)
- [ppt_designer + ppt_composer](ppt_designer_+_ppt_composer.md) (2 shared connections)
- [ppt_content](ppt_content.md) (1 shared connections)
- [ppt](ppt.md) (1 shared connections)

## Source Files

- `app/services/ppt_composer.py`
- `app/services/ppt_designer.py`
- `docs/features/ppt.md`

## Audit Trail

- EXTRACTED: 98 (88%)
- INFERRED: 14 (12%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*