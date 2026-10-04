# schema + bindings

> 9 nodes · cohesion 0.22

## Key Concepts

- **walk_nodes()** (9 connections) — `app/services/resume_replica/schema.py`
- **build_editor_path_map()** (4 connections) — `app/services/resume_replica/bindings.py`
- **collect_bindings()** (4 connections) — `app/services/resume_replica/schema.py`
- **_walk()** (3 connections) — `app/services/resume_replica/schema.py`
- **_visitor()** (1 connections) — `app/services/resume_replica/bindings.py`
- **Walks the scene graph and builds a map from binding path -> list of node IDs…** (1 connections) — `app/services/resume_replica/bindings.py`
- **_visit()** (1 connections) — `app/services/resume_replica/schema.py`
- **Depth-first traversal of the scene graph. visitor(node, parent, depth) is…** (1 connections) — `app/services/resume_replica/schema.py`
- **Returns all unique binding paths referenced in the scene graph. E.g. ["name",…** (1 connections) — `app/services/resume_replica/schema.py`

## Relationships

- [bindings](bindings.md) (2 shared connections)
- [schema](schema.md) (2 shared connections)
- [repair](repair.md) (2 shared connections)
- [repair + renderer](repair_+_renderer.md) (1 shared connections)

## Source Files

- `app/services/resume_replica/bindings.py`
- `app/services/resume_replica/schema.py`

## Audit Trail

- EXTRACTED: 14 (88%)
- INFERRED: 2 (12%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*