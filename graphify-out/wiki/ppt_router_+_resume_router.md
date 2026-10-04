# ppt_router + resume_router

> 32 nodes · cohesion 0.08

## Key Concepts

- **ppt_router.py** (20 connections) — `app/api/ppt_router.py`
- **resume_router.py** (8 connections) — `app/api/resume_router.py`
- **build_ppt()** (6 connections) — `app/api/ppt_router.py`
- **ppt_styles()** (6 connections) — `app/services/ppt_tool.py`
- **fastapi** (6 connections)
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
- **resume_editor()** (3 connections) — `app/api/resume_router.py`
- **resume_save()** (3 connections) — `app/api/resume_router.py`
- **_ppt_styles()** (3 connections) — `app/services/tools.py`
- **fastapi_responses** (3 connections)
- **generate()** (2 connections) — `app/api/ppt_router.py`
- **PPTStylesResponse** (2 connections) — `app/api/ppt_router.py`
- **get** (1 connections)
- **ppt_router.py — FastAPI router for the PPT AI build endpoint…** (1 connections) — `app/api/ppt_router.py`
- **End-to-end PPT generation using Groq on the backend. Optionally accepts a…** (1 connections) — `app/api/ppt_router.py`
- **Extract color theme from a PPT screenshot image. Returns the custom_theme dict…** (1 connections) — `app/api/ppt_router.py`
- *... and 7 more nodes in this community*

## Relationships

- [ppt_tool](ppt_tool.md) (7 shared connections)
- [resume_builder](resume_builder.md) (4 shared connections)
- [memory + tool_runner](memory_+_tool_runner.md) (3 shared connections)
- [main](main.md) (3 shared connections)
- [tools + window_layout](tools_+_window_layout.md) (3 shared connections)
- [ppt_content](ppt_content.md) (2 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (2 shared connections)
- [jarvis_overlay + prompt_overlay](jarvis_overlay_+_prompt_overlay.md) (1 shared connections)
- [server + persistence](server_+_persistence.md) (1 shared connections)

## Source Files

- `app/api/ppt_router.py`
- `app/api/resume_router.py`
- `app/services/ppt_tool.py`
- `app/services/tools.py`

## Audit Trail

- EXTRACTED: 65 (96%)
- INFERRED: 3 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*