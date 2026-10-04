# compiler

> 21 nodes · cohesion 0.11

## Key Concepts

- **compiler.py** (48 connections) — `app/services/resume_replica/compiler.py`
- **_compile_path()** (7 connections) — `app/services/resume_replica/compiler.py`
- **_compile_frame()** (5 connections) — `app/services/resume_replica/compiler.py`
- **_fill_to_svg_fill()** (4 connections) — `app/services/resume_replica/compiler.py`
- **_commands_to_d()** (3 connections) — `app/services/resume_replica/compiler.py`
- **_compile_document_css()** (3 connections) — `app/services/resume_replica/compiler.py`
- **_fill_to_css_background()** (3 connections) — `app/services/resume_replica/compiler.py`
- **_parametric_to_commands()** (3 connections) — `app/services/resume_replica/compiler.py`
- **contextvars** (3 connections)
- **_mm_to_pt()** (2 connections) — `app/services/resume_replica/compiler.py`
- **_pt_to_mm()** (2 connections) — `app/services/resume_replica/compiler.py`
- **compiler.py — Scene graph → print-ready HTML/CSS. Entry point:…** (1 connections) — `app/services/resume_replica/compiler.py`
- **Converts a list of SVG path command lists to a path 'd' string. [["M", 0, 0],…** (1 connections) — `app/services/resume_replica/compiler.py`
- **Generates the complete CSS for the document.** (1 connections) — `app/services/resume_replica/compiler.py`
- **Converts mm to pt (1mm = 2.8346pt).** (1 connections) — `app/services/resume_replica/compiler.py`
- **Converts pt to mm (1pt = 0.3528mm).** (1 connections) — `app/services/resume_replica/compiler.py`
- **Converts a FILL dict to a CSS background property value string.** (1 connections) — `app/services/resume_replica/compiler.py`
- **Returns (fill_attr_value, gradient_defs_html). For solid: ('#hex', '') For…** (1 connections) — `app/services/resume_replica/compiler.py`
- **Compiles a FRAME node to a <div> element.** (1 connections) — `app/services/resume_replica/compiler.py`
- **Compiles a PATH node to an inline SVG element.** (1 connections) — `app/services/resume_replica/compiler.py`
- **Converts parametric geometry dict to (d_string, view_box).** (1 connections) — `app/services/resume_replica/compiler.py`

## Relationships

- [compiler](compiler.md) (37 shared connections)
- [voice_agent + download_kokoro](voice_agent_+_download_kokoro.md) (3 shared connections)
- [repair + assignment_humanizer](repair_+_assignment_humanizer.md) (2 shared connections)
- [ppt_chart_engine](ppt_chart_engine.md) (1 shared connections)
- [resume_builder](resume_builder.md) (1 shared connections)
- [exact_render](exact_render.md) (1 shared connections)

## Source Files

- `app/services/resume_replica/compiler.py`

## Audit Trail

- EXTRACTED: 69 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*