# ppt_designer

> 14 nodes · cohesion 0.18

## Key Concepts

- **place_image()** (26 connections) — `app/services/ppt_designer.py`
- **prepare_image()** (10 connections) — `app/services/ppt_designer.py`
- **_best_window()** (6 connections) — `app/services/ppt_designer.py`
- **._img()** (5 connections) — `app/services/ppt_designer.py`
- **_saliency_profile()** (5 connections) — `app/services/ppt_designer.py`
- **_replace_picture()** (5 connections) — `app/services/ppt_template.py`
- **Layout engine (`ppt_designer.py`)** (5 connections) — `docs/features/ppt.md`
- **._title_logo()** (4 connections) — `app/services/ppt_designer.py`
- **_soft_shadow()** (4 connections) — `app/services/ppt_designer.py`
- **_round_pic()** (2 connections) — `app/services/ppt_designer.py`
- **Return a PPTX-safe copy (EXIF-rotated, RGB, ≤2400px, png/jpg) and its aspect.** (1 connections) — `app/services/ppt_designer.py`
- **Edge-energy profile along an axis ('x' or 'y') for smart cropping.** (1 connections) — `app/services/ppt_designer.py`
- **Start fraction of the window (length=keep fraction) with most detail, biased to…** (1 connections) — `app/services/ppt_designer.py`
- **cover: fill box, crop with saliency. contain: fit inside box, centred.** (1 connections) — `app/services/ppt_designer.py`

## Relationships

- [ppt_designer](ppt_designer.md) (28 shared connections)
- [ppt_template](ppt_template.md) (7 shared connections)
- [ppt_composer + ppt_designer](ppt_composer_+_ppt_designer.md) (6 shared connections)
- [ppt_studio](ppt_studio.md) (2 shared connections)
- [ppt + KNOWN_ISSUES](ppt_+_KNOWN_ISSUES.md) (1 shared connections)

## Source Files

- `app/services/ppt_designer.py`
- `app/services/ppt_template.py`
- `docs/features/ppt.md`

## Audit Trail

- EXTRACTED: 56 (93%)
- INFERRED: 4 (7%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*