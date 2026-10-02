# ppt_tool + ppt_image_engine

> 37 nodes · cohesion 0.08

## Key Concepts

- **ppt_tool.py** (51 connections) — `app/services/ppt_tool.py`
- **ppt_create()** (15 connections) — `app/services/ppt_tool.py`
- **_ppt_create_legacy()** (14 connections) — `app/services/ppt_tool.py`
- **extract_theme_from_image()** (13 connections) — `app/services/ppt_tool.py`
- **match_images_to_slides()** (8 connections) — `app/services/ppt_image_engine.py`
- **test_ppt.py** (8 connections) — `test_ppt.py`
- **_extract_theme_pil_local()** (7 connections) — `app/services/ppt_tool.py`
- **_c()** (5 connections) — `app/services/ppt_tool.py`
- **_normalize_and_recover()** (5 connections) — `app/services/ppt_tool.py`
- **_parse()** (5 connections) — `app/services/ppt_tool.py`
- **_shape()** (5 connections) — `app/services/ppt_tool.py`
- **_groq_call()** (4 connections) — `app/services/ppt_tool.py`
- **test_builder.py** (4 connections) — `test_builder.py`
- **main()** (4 connections) — `test_ppt.py`
- **_auto_select_image_layout()** (3 connections) — `app/services/ppt_tool.py`
- **_bg_fill()** (3 connections) — `app/services/ppt_tool.py`
- **_detect_purpose()** (3 connections) — `app/services/ppt_tool.py`
- **_ppt_create()** (3 connections) — `app/services/tools.py`
- **Gotchas** (3 connections) — `docs/features/ppt.md`
- **pptx_dml_color** (2 connections)
- **test_builder()** (2 connections) — `test_builder.py`
- **Assign images to slides intelligently. Assignment priority: 1. Explicit slide…** (1 connections) — `app/services/ppt_image_engine.py`
- **_validate()** (1 connections) — `app/services/ppt_tool.py`
- **_lum()** (1 connections) — `app/services/ppt_tool.py`
- **_rgb_to_hex()** (1 connections) — `app/services/ppt_tool.py`
- *... and 12 more nodes in this community*

## Relationships

- [ppt_tool](ppt_tool.md) (24 shared connections)
- [assignment_tool + safe_executor](assignment_tool_+_safe_executor.md) (10 shared connections)
- [ppt_image_engine](ppt_image_engine.md) (8 shared connections)
- [ppt_studio + ppt_content](ppt_studio_+_ppt_content.md) (5 shared connections)
- [ppt_router + resume_router](ppt_router_+_resume_router.md) (5 shared connections)
- [ppt_designer](ppt_designer.md) (4 shared connections)
- [tools](tools.md) (4 shared connections)
- [ppt_chart_engine](ppt_chart_engine.md) (2 shared connections)
- [ppt_content](ppt_content.md) (2 shared connections)
- [dag_executor + planner](dag_executor_+_planner.md) (2 shared connections)
- [message_reader + whatsapp](message_reader_+_whatsapp.md) (1 shared connections)
- [ui_inspector + lru](ui_inspector_+_lru.md) (1 shared connections)

## Source Files

- `app/services/ppt_image_engine.py`
- `app/services/ppt_tool.py`
- `app/services/tools.py`
- `docs/features/ppt.md`
- `test_builder.py`
- `test_ppt.py`

## Audit Trail

- EXTRACTED: 118 (91%)
- INFERRED: 11 (9%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*