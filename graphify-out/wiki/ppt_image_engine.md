# ppt_image_engine

> 17 nodes · cohesion 0.15

## Key Concepts

- **ppt_image_engine.py** (13 connections) — `app/services/ppt_image_engine.py`
- **build_image_descriptors()** (8 connections) — `app/services/ppt_image_engine.py`
- **_extract_keywords()** (5 connections) — `app/services/ppt_image_engine.py`
- **ImageDescriptor** (4 connections) — `app/services/ppt_image_engine.py`
- **_parse_slide_ref_by_title()** (4 connections) — `app/services/ppt_image_engine.py`
- **dataclasses** (4 connections)
- **get_aspect_ratio()** (3 connections) — `app/services/ppt_image_engine.py`
- **_parse_slide_ref()** (3 connections) — `app/services/ppt_image_engine.py`
- **_slide_score()** (3 connections) — `app/services/ppt_image_engine.py`
- **ppt_image_engine.py — Semantic Image-Slide Matcher for JARVIS PPT Engine…** (1 connections) — `app/services/ppt_image_engine.py`
- **Return (aspect_ratio, width_px, height_px) for an image. Falls back to (1.78,…** (1 connections) — `app/services/ppt_image_engine.py`
- **Build an ImageDescriptor for each uploaded image. Args: paths: Absolute file…** (1 connections) — `app/services/ppt_image_engine.py`
- **Score relevance of an image to a slide using keyword overlap. Returns a float…** (1 connections) — `app/services/ppt_image_engine.py`
- **All metadata about one uploaded image.** (1 connections) — `app/services/ppt_image_engine.py`
- **Extract meaningful 3+ character alpha tokens, filtering stop-words.** (1 connections) — `app/services/ppt_image_engine.py`
- **Detect explicit slide assignment in the user hint. Recognised patterns (case-…** (1 connections) — `app/services/ppt_image_engine.py`
- **Try to match vague slide references like "intro slide", "conclusion", "the…** (1 connections) — `app/services/ppt_image_engine.py`

## Relationships

- [ppt_tool + ppt_image_engine](ppt_tool_+_ppt_image_engine.md) (8 shared connections)
- [assignment_tool + safe_executor](assignment_tool_+_safe_executor.md) (2 shared connections)
- [ui_inspector + lru](ui_inspector_+_lru.md) (1 shared connections)
- [dag_executor + planner](dag_executor_+_planner.md) (1 shared connections)
- [voice](voice.md) (1 shared connections)

## Source Files

- `app/services/ppt_image_engine.py`

## Audit Trail

- EXTRACTED: 34 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*