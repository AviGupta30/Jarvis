# ppt_router + ppt_tool

> 25 nodes · cohesion 0.11

## Key Concepts

- **ppt_router.py** (20 connections) — `app/api/ppt_router.py`
- **ppt_create()** (15 connections) — `app/services/ppt_tool.py`
- **build_ppt()** (6 connections) — `app/api/ppt_router.py`
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
- **_ppt_create()** (3 connections) — `app/services/tools.py`
- **generate()** (2 connections) — `app/api/ppt_router.py`
- **PPTStylesResponse** (2 connections) — `app/api/ppt_router.py`
- **get** (1 connections)
- **ppt_router.py — FastAPI router for the PPT AI build endpoint…** (1 connections) — `app/api/ppt_router.py`
- **End-to-end PPT generation using Groq on the backend. Optionally accepts a…** (1 connections) — `app/api/ppt_router.py`
- **Extract color theme from a PPT screenshot image. Returns the custom_theme dict…** (1 connections) — `app/api/ppt_router.py`
- **Return all available design personalities.** (1 connections) — `app/api/ppt_router.py`
- **Build a PPTX from a pre-generated slide plan (JSON). Streams live per-slide…** (1 connections) — `app/api/ppt_router.py`
- **PPT v6 entry point → ppt_studio.create (adaptive layouts, strict user content,…** (1 connections) — `app/services/ppt_tool.py`
- **Intelligently pick a palette based on the presentation topic.** (1 connections) — `app/services/ppt_tool.py`
- **Generator wrapper — streams live progress to the frontend via chat.py's…** (1 connections) — `app/services/tools.py`

## Relationships

- [ppt_tool](ppt_tool.md) (8 shared connections)
- [tools](tools.md) (5 shared connections)
- [resume_router](resume_router.md) (2 shared connections)
- [assignment_tool + assignment_humanizer](assignment_tool_+_assignment_humanizer.md) (1 shared connections)
- [memory + memory](memory_+_memory.md) (1 shared connections)
- [persistence + server](persistence_+_server.md) (1 shared connections)
- [main + screen_vision](main_+_screen_vision.md) (1 shared connections)
- [ppt_studio + ppt_content](ppt_studio_+_ppt_content.md) (1 shared connections)
- [research_scraper + nlp_extractor](research_scraper_+_nlp_extractor.md) (1 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (1 shared connections)
- [ppt_research](ppt_research.md) (1 shared connections)
- [agentic_web + email-calendar](agentic_web_+_email-calendar.md) (1 shared connections)

## Source Files

- `app/api/ppt_router.py`
- `app/services/ppt_tool.py`
- `app/services/tools.py`

## Audit Trail

- EXTRACTED: 52 (87%)
- INFERRED: 8 (13%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*