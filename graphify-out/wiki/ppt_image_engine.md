# ppt_image_engine

> 19 nodes · cohesion 0.16

## Key Concepts

- **ppt_image_engine.py** (13 connections) — `app/services/ppt_image_engine.py`
- **build_image_descriptors()** (8 connections) — `app/services/ppt_image_engine.py`
- **match_images_to_slides()** (8 connections) — `app/services/ppt_image_engine.py`
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
- **Assign images to slides intelligently. Assignment priority: 1. Explicit slide…** (1 connections) — `app/services/ppt_image_engine.py`
- **All metadata about one uploaded image.** (1 connections) — `app/services/ppt_image_engine.py`
- **Extract meaningful 3+ character alpha tokens, filtering stop-words.** (1 connections) — `app/services/ppt_image_engine.py`
- **Detect explicit slide assignment in the user hint. Recognised patterns (case-…** (1 connections) — `app/services/ppt_image_engine.py`
- **Try to match vague slide references like "intro slide", "conclusion", "the…** (1 connections) — `app/services/ppt_image_engine.py`

## Relationships

- [ppt_tool](ppt_tool.md) (5 shared connections)
- [assignment_assembler + smart_navigator](assignment_assembler_+_smart_navigator.md) (1 shared connections)
- [test_lru](test_lru.md) (1 shared connections)
- [style_profiler + reply_generator](style_profiler_+_reply_generator.md) (1 shared connections)
- [dag_executor](dag_executor.md) (1 shared connections)
- [voice](voice.md) (1 shared connections)

## Source Files

- `app/services/ppt_image_engine.py`

## Audit Trail

- EXTRACTED: 37 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*