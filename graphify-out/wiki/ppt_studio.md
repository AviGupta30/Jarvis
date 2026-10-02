# ppt_studio

> 6 nodes · cohesion 0.33

## Key Concepts

- **_assign_images()** (6 connections) — `app/services/ppt_studio.py`
- **_rebalance()** (4 connections) — `app/services/ppt_studio.py`
- **eligible()** (1 connections) — `app/services/ppt_studio.py`
- **score()** (1 connections) — `app/services/ppt_studio.py`
- **Put each image on its best slide. Explicit instructions win. Mutates deck;…** (1 connections) — `app/services/ppt_studio.py`
- **Move images off slides whose layout can't show them (or has too many) onto…** (1 connections) — `app/services/ppt_studio.py`

## Relationships

- [ppt_studio + ppt_content](ppt_studio_+_ppt_content.md) (3 shared connections)
- [ppt_content](ppt_content.md) (1 shared connections)

## Source Files

- `app/services/ppt_studio.py`

## Audit Trail

- EXTRACTED: 7 (78%)
- INFERRED: 2 (22%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*