# repair

> 10 nodes · cohesion 0.20

## Key Concepts

- **apply_diff_patches()** (10 connections) — `app/services/resume_replica/repair.py`
- **_patch_fill()** (5 connections) — `app/services/resume_replica/repair.py`
- **make_linear_fill()** (4 connections) — `app/services/resume_replica/schema.py`
- **_patch_chart()** (1 connections) — `app/services/resume_replica/repair.py`
- **_patch_image()** (1 connections) — `app/services/resume_replica/repair.py`
- **_patch_opacity()** (1 connections) — `app/services/resume_replica/repair.py`
- **_visitor()** (1 connections) — `app/services/resume_replica/repair.py`
- **Converts VLM diffs into structured patches and applies them to the replica_doc.…** (1 connections) — `app/services/resume_replica/repair.py`
- **Finds the frame with the given ID in the scene graph and updates its fill.…** (1 connections) — `app/services/resume_replica/repair.py`
- **stops = [{"offset_pct": 0, "color": "#hex"}, {"offset_pct": 100, "color":…** (1 connections) — `app/services/resume_replica/schema.py`

## Relationships

- [repair](repair.md) (4 shared connections)
- [schema](schema.md) (2 shared connections)
- [schema + bindings](schema_+_bindings.md) (2 shared connections)

## Source Files

- `app/services/resume_replica/repair.py`
- `app/services/resume_replica/schema.py`

## Audit Trail

- EXTRACTED: 13 (76%)
- INFERRED: 4 (24%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*