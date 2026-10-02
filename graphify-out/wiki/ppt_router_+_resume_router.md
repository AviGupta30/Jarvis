# ppt_router + resume_router

> 30 nodes · cohesion 0.09

## Key Concepts

- **ppt_router.py** (20 connections) — `app/api/ppt_router.py`
- **resume_router.py** (8 connections) — `app/api/resume_router.py`
- **build_ppt()** (6 connections) — `app/api/ppt_router.py`
- **fastapi** (6 connections)
- **create_ppt_backend()** (5 connections) — `app/api/ppt_router.py`
- **extract_theme()** (5 connections) — `app/api/ppt_router.py`
- **get_styles()** (4 connections) — `app/api/ppt_router.py`
- **BaseModel** (4 connections)
- **_pick()** (4 connections) — `app/services/ppt_tool.py`
- **pydantic** (4 connections)
- **generate()** (3 connections) — `app/api/ppt_router.py`
- **PPTBuildRequest** (3 connections) — `app/api/ppt_router.py`
- **PPTCreateRequest** (3 connections) — `app/api/ppt_router.py`
- **PPTExtractThemeRequest** (3 connections) — `app/api/ppt_router.py`
- **post** (3 connections)
- **resume_editor()** (3 connections) — `app/api/resume_router.py`
- **resume_save()** (3 connections) — `app/api/resume_router.py`
- **fastapi_responses** (3 connections)
- **generate()** (2 connections) — `app/api/ppt_router.py`
- **PPTStylesResponse** (2 connections) — `app/api/ppt_router.py`
- **get** (1 connections)
- **ppt_router.py — FastAPI router for the PPT AI build endpoint…** (1 connections) — `app/api/ppt_router.py`
- **End-to-end PPT generation using Groq on the backend. Optionally accepts a…** (1 connections) — `app/api/ppt_router.py`
- **Extract color theme from a PPT screenshot image. Returns the custom_theme dict…** (1 connections) — `app/api/ppt_router.py`
- **Return all available design personalities.** (1 connections) — `app/api/ppt_router.py`
- *... and 5 more nodes in this community*

## Relationships

- [ppt_tool + ppt_image_engine](ppt_tool_+_ppt_image_engine.md) (5 shared connections)
- [resume_builder](resume_builder.md) (4 shared connections)
- [ppt_tool](ppt_tool.md) (3 shared connections)
- [main + screen_vision](main_+_screen_vision.md) (3 shared connections)
- [chat](chat.md) (3 shared connections)
- [tools](tools.md) (2 shared connections)
- [rag_memory + memory](rag_memory_+_memory.md) (2 shared connections)
- [agents + tool_runner](agents_+_tool_runner.md) (2 shared connections)
- [assignment_tool + safe_executor](assignment_tool_+_safe_executor.md) (1 shared connections)
- [ui_inspector + lru](ui_inspector_+_lru.md) (1 shared connections)

## Source Files

- `app/api/ppt_router.py`
- `app/api/resume_router.py`
- `app/services/ppt_tool.py`

## Audit Trail

- EXTRACTED: 64 (98%)
- INFERRED: 1 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*