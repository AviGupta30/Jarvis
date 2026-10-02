# ppt_composer + ppt_designer

> 27 nodes · cohesion 0.11

## Key Concepts

- **render_sections()** (22 connections) — `app/services/ppt_composer.py`
- **Composite slides (`ppt_composer.py`, kind `sections`)** (12 connections) — `docs/features/ppt.md`
- **_sizes()** (11 connections) — `app/services/ppt_designer.py`
- **evaluate()** (8 connections) — `app/services/ppt_composer.py`
- **justified_rows()** (7 connections) — `app/services/ppt_designer.py`
- **_fill()** (6 connections) — `app/services/ppt_composer.py`
- **_image_panel()** (6 connections) — `app/services/ppt_composer.py`
- **_balanced_rows()** (5 connections) — `app/services/ppt_composer.py`
- **image_block()** (5 connections) — `app/services/ppt_composer.py`
- **_masonry()** (5 connections) — `app/services/ppt_composer.py`
- **eval_images()** (5 connections) — `app/services/ppt_composer.py`
- **_stretch_cap()** (5 connections) — `app/services/ppt_composer.py`
- **_justified_fixed()** (5 connections) — `app/services/ppt_designer.py`
- **icon_for()** (4 connections) — `app/services/ppt_designer.py`
- **icon_png()** (4 connections) — `app/services/ppt_designer.py`
- **band_h()** (3 connections) — `app/services/ppt_composer.py`
- **search()** (3 connections) — `app/services/ppt_composer.py`
- **._s_sections()** (2 connections) — `app/services/ppt_designer.py`
- **col_h()** (1 connections) — `app/services/ppt_composer.py`
- **Split items into rows with at most one item difference (5 in 3 cols → 3+2, 7 →…** (1 connections) — `app/services/ppt_composer.py`
- **How much extra height a section can absorb before it looks inflated.** (1 connections) — `app/services/ppt_composer.py`
- **Framed images (no crop) + numbered captions under each. Returns used height.** (1 connections) — `app/services/ppt_composer.py`
- **Boxes for the images at full column width in exactly `rows` rows (scaled down…** (1 connections) — `app/services/ppt_composer.py`
- **Balanced split of sections into columns (reading order kept inside each…** (1 connections) — `app/services/ppt_composer.py`
- **Share the free height of a column between its sections (each up to its stretch…** (1 connections) — `app/services/ppt_composer.py`
- *... and 2 more nodes in this community*

## Relationships

- [ppt_composer + ppt_designer](ppt_composer_+_ppt_designer.md) (32 shared connections)
- [ppt_designer](ppt_designer.md) (19 shared connections)
- [ppt_content + ppt_designer](ppt_content_+_ppt_designer.md) (1 shared connections)
- [ppt + KNOWN_ISSUES](ppt_+_KNOWN_ISSUES.md) (1 shared connections)

## Source Files

- `app/services/ppt_composer.py`
- `app/services/ppt_designer.py`
- `docs/features/ppt.md`

## Audit Trail

- EXTRACTED: 78 (87%)
- INFERRED: 12 (13%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*