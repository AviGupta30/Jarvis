# ppt_tool + ppt_router

> 3 nodes · cohesion 0.67

## Key Concepts

- **_pick()** (4 connections) — `app/services/ppt_tool.py`
- **generate()** (3 connections) — `app/api/ppt_router.py`
- **Intelligently pick a palette based on the presentation topic.** (1 connections) — `app/services/ppt_tool.py`

## Relationships

- [ppt_tool](ppt_tool.md) (2 shared connections)
- [ppt_router](ppt_router.md) (2 shared connections)

## Source Files

- `app/api/ppt_router.py`
- `app/services/ppt_tool.py`

## Audit Trail

- EXTRACTED: 6 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*