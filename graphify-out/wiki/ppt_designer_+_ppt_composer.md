# ppt_designer + ppt_composer

> 6 nodes · cohesion 0.33

## Key Concepts

- **justified_rows()** (7 connections) — `app/services/ppt_designer.py`
- **image_block()** (5 connections) — `app/services/ppt_composer.py`
- **_justified_fixed()** (5 connections) — `app/services/ppt_designer.py`
- **Boxes for the images at full column width in exactly `rows` rows (scaled down…** (1 connections) — `app/services/ppt_composer.py`
- **Google-Photos-style justified layout. Returns list of (x, y, w, h) relative to…** (1 connections) — `app/services/ppt_designer.py`
- **Justified layout with an exact number of rows (top-aligned). None if impossible.** (1 connections) — `app/services/ppt_designer.py`

## Relationships

- [ppt_composer + ppt_designer](ppt_composer_+_ppt_designer.md) (6 shared connections)
- [ppt_designer](ppt_designer.md) (4 shared connections)

## Source Files

- `app/services/ppt_composer.py`
- `app/services/ppt_designer.py`

## Audit Trail

- EXTRACTED: 14 (93%)
- INFERRED: 1 (7%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*