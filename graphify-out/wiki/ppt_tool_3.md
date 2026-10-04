# ppt_tool

> 24 nodes · cohesion 0.14

## Key Concepts

- **ppt_tool.py** (51 connections) — `app/services/ppt_tool.py`
- **_ppt_create_legacy()** (14 connections) — `app/services/ppt_tool.py`
- **extract_theme_from_image()** (13 connections) — `app/services/ppt_tool.py`
- **test_ppt.py** (8 connections) — `test_ppt.py`
- **_oval()** (7 connections) — `app/services/ppt_tool.py`
- **_c()** (5 connections) — `app/services/ppt_tool.py`
- **_normalize_and_recover()** (5 connections) — `app/services/ppt_tool.py`
- **_parse()** (5 connections) — `app/services/ppt_tool.py`
- **_shape()** (5 connections) — `app/services/ppt_tool.py`
- **_groq_call()** (4 connections) — `app/services/ppt_tool.py`
- **main()** (4 connections) — `test_ppt.py`
- **_auto_select_image_layout()** (3 connections) — `app/services/ppt_tool.py`
- **_bg_fill()** (3 connections) — `app/services/ppt_tool.py`
- **_detect_purpose()** (3 connections) — `app/services/ppt_tool.py`
- **Gotchas** (3 connections) — `docs/features/ppt.md`
- **pptx_dml_color** (2 connections)
- **_validate()** (1 connections) — `app/services/ppt_tool.py`
- **RGBColor** (1 connections)
- **ppt_tool.py — Premium Visual-First PPT Engine v5…** (1 connections) — `app/services/ppt_tool.py`
- **After an image is assigned to a slide, pick the most aesthetically appropriate…** (1 connections) — `app/services/ppt_tool.py`
- **Maps hallucinated content arrays to expected keys and supplies fallbacks so no…** (1 connections) — `app/services/ppt_tool.py`
- **Legacy v5 generation pipeline (fixed aesthetic_* layouts). Used only as a…** (1 connections) — `app/services/ppt_tool.py`
- **Auto-detect presentation purpose from the user prompt.** (1 connections) — `app/services/ppt_tool.py`
- **Analyze a PPT screenshot and extract the exact color palette as a custom_theme…** (1 connections) — `app/services/ppt_tool.py`

## Relationships

- [ppt_tool](ppt_tool.md) (28 shared connections)
- [ppt_image_engine](ppt_image_engine.md) (5 shared connections)
- [ppt_designer](ppt_designer.md) (4 shared connections)
- [benchmark + server](benchmark_+_server.md) (3 shared connections)
- [ppt_studio + ppt_designer](ppt_studio_+_ppt_designer.md) (3 shared connections)
- [ppt_chart_engine](ppt_chart_engine.md) (2 shared connections)
- [nlp_extractor + download_kokoro](nlp_extractor_+_download_kokoro.md) (2 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (2 shared connections)
- [chat + tools](chat_+_tools.md) (2 shared connections)
- [ppt + KNOWN_ISSUES](ppt_+_KNOWN_ISSUES.md) (2 shared connections)
- [ppt_router](ppt_router.md) (2 shared connections)
- [safe_executor](safe_executor.md) (1 shared connections)

## Source Files

- `app/services/ppt_tool.py`
- `docs/features/ppt.md`
- `test_ppt.py`

## Audit Trail

- EXTRACTED: 100 (96%)
- INFERRED: 4 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*