# compiler

> 21 nodes · cohesion 0.13

## Key Concepts

- **_e()** (21 connections) — `app/services/resume_replica/compiler.py`
- **_compile_node()** (13 connections) — `app/services/resume_replica/compiler.py`
- **compile_replica_html()** (10 connections) — `app/services/resume_replica/compiler.py`
- **_compile_text()** (7 connections) — `app/services/resume_replica/compiler.py`
- **_compile_image()** (6 connections) — `app/services/resume_replica/compiler.py`
- **_compile_frame()** (5 connections) — `app/services/resume_replica/compiler.py`
- **_compile_group()** (4 connections) — `app/services/resume_replica/compiler.py`
- **_compile_rule()** (4 connections) — `app/services/resume_replica/compiler.py`
- **_initials_block()** (4 connections) — `app/services/resume_replica/compiler.py`
- **_resolve_binding()** (4 connections) — `app/services/resume_replica/compiler.py`
- **_text_style_to_css()** (3 connections) — `app/services/resume_replica/compiler.py`
- **Returns the initials text for the photo placeholder.** (1 connections) — `app/services/resume_replica/compiler.py`
- **Converts a TEXT_STYLE dict to a CSS properties string.** (1 connections) — `app/services/resume_replica/compiler.py`
- **Dispatches to the appropriate node compiler based on node['type'].** (1 connections) — `app/services/resume_replica/compiler.py`
- **Compiles a FRAME node to a <div> element.** (1 connections) — `app/services/resume_replica/compiler.py`
- **Compiles a GROUP node to a <div>. Used for section headings and composites.** (1 connections) — `app/services/resume_replica/compiler.py`
- **Compiles a TEXT node, optionally binding to content and supporting edit mode.** (1 connections) — `app/services/resume_replica/compiler.py`
- **Walks a dot-path binding into content dict. Returns '' if not found.** (1 connections) — `app/services/resume_replica/compiler.py`
- **Compiles an IMAGE node to a div with background-image (or initials block).** (1 connections) — `app/services/resume_replica/compiler.py`
- **Compiles a RULE node to an <hr> or vertical div.** (1 connections) — `app/services/resume_replica/compiler.py`
- **Main entry point. Returns a complete HTML document string. content : normalised…** (1 connections) — `app/services/resume_replica/compiler.py`

## Relationships

- [compiler](compiler.md) (31 shared connections)
- [storage + orchestrator](storage_+_orchestrator.md) (2 shared connections)
- [repair](repair.md) (2 shared connections)

## Source Files

- `app/services/resume_replica/compiler.py`

## Audit Trail

- EXTRACTED: 63 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*