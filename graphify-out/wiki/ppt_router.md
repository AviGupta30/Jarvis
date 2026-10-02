# ppt_router

> 24 nodes · cohesion 0.12

## Key Concepts

- **ppt_router.py** (20 connections) — `app/api/ppt_router.py`
- **build_ppt()** (6 connections) — `app/api/ppt_router.py`
- **ppt_styles()** (6 connections) — `app/services/ppt_tool.py`
- **create_ppt_backend()** (5 connections) — `app/api/ppt_router.py`
- **extract_theme()** (5 connections) — `app/api/ppt_router.py`
- **get_styles()** (4 connections) — `app/api/ppt_router.py`
- **BaseModel** (4 connections)
- **_pick()** (4 connections) — `app/services/ppt_tool.py`
- **generate()** (3 connections) — `app/api/ppt_router.py`
- **PPTBuildRequest** (3 connections) — `app/api/ppt_router.py`
- **PPTCreateRequest** (3 connections) — `app/api/ppt_router.py`
- **PPTExtractThemeRequest** (3 connections) — `app/api/ppt_router.py`
- **post** (3 connections)
- **_ppt_styles()** (3 connections) — `app/services/tools.py`
- **generate()** (2 connections) — `app/api/ppt_router.py`
- **PPTStylesResponse** (2 connections) — `app/api/ppt_router.py`
- **get** (1 connections)
- **ppt_router.py — FastAPI router for the PPT AI build endpoint…** (1 connections) — `app/api/ppt_router.py`
- **End-to-end PPT generation using Groq on the backend. Optionally accepts a…** (1 connections) — `app/api/ppt_router.py`
- **Extract color theme from a PPT screenshot image. Returns the custom_theme dict…** (1 connections) — `app/api/ppt_router.py`
- **Return all available design personalities.** (1 connections) — `app/api/ppt_router.py`
- **Build a PPTX from a pre-generated slide plan (JSON). Streams live per-slide…** (1 connections) — `app/api/ppt_router.py`
- **Intelligently pick a palette based on the presentation topic.** (1 connections) — `app/services/ppt_tool.py`
- **List all available presentation design personalities.** (1 connections) — `app/services/tools.py`

## Relationships

- [ppt_tool](ppt_tool.md) (7 shared connections)
- [ppt_content](ppt_content.md) (2 shared connections)
- [smart_navigator + rag_memory](smart_navigator_+_rag_memory.md) (2 shared connections)
- [agents + tool_runner](agents_+_tool_runner.md) (2 shared connections)
- [tools](tools.md) (2 shared connections)
- [resume_builder](resume_builder.md) (1 shared connections)
- [main](main.md) (1 shared connections)
- [tools + whatsapp_smart](tools_+_whatsapp_smart.md) (1 shared connections)

## Source Files

- `app/api/ppt_router.py`
- `app/services/ppt_tool.py`
- `app/services/tools.py`

## Audit Trail

- EXTRACTED: 48 (94%)
- INFERRED: 3 (6%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*