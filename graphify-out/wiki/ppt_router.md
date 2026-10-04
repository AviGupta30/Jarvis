# ppt_router

> 19 nodes · cohesion 0.15

## Key Concepts

- **ppt_router.py** (20 connections) — `app/api/ppt_router.py`
- **build_ppt()** (6 connections) — `app/api/ppt_router.py`
- **create_ppt_backend()** (5 connections) — `app/api/ppt_router.py`
- **extract_theme()** (5 connections) — `app/api/ppt_router.py`
- **get_styles()** (4 connections) — `app/api/ppt_router.py`
- **BaseModel** (4 connections)
- **pydantic** (4 connections)
- **PPTBuildRequest** (3 connections) — `app/api/ppt_router.py`
- **PPTCreateRequest** (3 connections) — `app/api/ppt_router.py`
- **PPTExtractThemeRequest** (3 connections) — `app/api/ppt_router.py`
- **post** (3 connections)
- **generate()** (2 connections) — `app/api/ppt_router.py`
- **PPTStylesResponse** (2 connections) — `app/api/ppt_router.py`
- **get** (1 connections)
- **ppt_router.py — FastAPI router for the PPT AI build endpoint…** (1 connections) — `app/api/ppt_router.py`
- **End-to-end PPT generation using Groq on the backend. Optionally accepts a…** (1 connections) — `app/api/ppt_router.py`
- **Extract color theme from a PPT screenshot image. Returns the custom_theme dict…** (1 connections) — `app/api/ppt_router.py`
- **Return all available design personalities.** (1 connections) — `app/api/ppt_router.py`
- **Build a PPTX from a pre-generated slide plan (JSON). Streams live per-slide…** (1 connections) — `app/api/ppt_router.py`

## Relationships

- [ppt_tool](ppt_tool.md) (4 shared connections)
- [chat + tools](chat_+_tools.md) (2 shared connections)
- [tools](tools.md) (2 shared connections)
- [ppt_tool + ppt_router](ppt_tool_+_ppt_router.md) (2 shared connections)
- [resume_router](resume_router.md) (2 shared connections)
- [social_content_manager + tools](social_content_manager_+_tools.md) (2 shared connections)
- [nlp_extractor + download_kokoro](nlp_extractor_+_download_kokoro.md) (1 shared connections)
- [main + screen_vision](main_+_screen_vision.md) (1 shared connections)
- [chat + llm](chat_+_llm.md) (1 shared connections)
- [memory + CLAUDE](memory_+_CLAUDE.md) (1 shared connections)

## Source Files

- `app/api/ppt_router.py`

## Audit Trail

- EXTRACTED: 43 (98%)
- INFERRED: 1 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*