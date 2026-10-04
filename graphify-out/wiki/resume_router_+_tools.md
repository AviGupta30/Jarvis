# resume_router + tools

> 14 nodes · cohesion 0.15

## Key Concepts

- **api/tools.py** (9 connections) — `app/api/tools.py`
- **resume_router.py** (8 connections) — `app/api/resume_router.py`
- **fastapi** (6 connections)
- **execute_tool()** (4 connections) — `app/api/tools.py`
- **pydantic** (4 connections)
- **resume_editor()** (3 connections) — `app/api/resume_router.py`
- **resume_save()** (3 connections) — `app/api/resume_router.py`
- **ToolExecuteRequest** (3 connections) — `app/api/tools.py`
- **fastapi_responses** (3 connections)
- **get** (1 connections)
- **post** (1 connections)
- **resume_router.py — FastAPI router for the visual resume editor…** (1 connections) — `app/api/resume_router.py`
- **BaseModel** (1 connections)
- **post** (1 connections)

## Relationships

- [memory + rag_memory](memory_+_rag_memory.md) (5 shared connections)
- [resume_builder + integrate](resume_builder_+_integrate.md) (4 shared connections)
- [main + screen_vision](main_+_screen_vision.md) (3 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (3 shared connections)
- [ppt_router + ppt_tool](ppt_router_+_ppt_tool.md) (3 shared connections)
- [style_profiler + reply_generator](style_profiler_+_reply_generator.md) (1 shared connections)
- [tools](tools.md) (1 shared connections)

## Source Files

- `app/api/resume_router.py`
- `app/api/tools.py`

## Audit Trail

- EXTRACTED: 34 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*