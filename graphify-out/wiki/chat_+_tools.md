# chat + tools

> 23 nodes · cohesion 0.09

## Key Concepts

- **Fixed on 2026-09-28** (16 connections) — `docs/KNOWN_ISSUES.md`
- **ppt_create()** (15 connections) — `app/services/ppt_tool.py`
- **_media_compound()** (11 connections) — `app/api/chat.py`
- **_media_target()** (9 connections) — `app/api/chat.py`
- **Gotchas** (7 connections) — `docs/features/tool-registry.md`
- **research_topic()** (6 connections) — `app/services/research_pipeline.py`
- **_mail_tool()** (6 connections) — `app/services/tools.py`
- **create_folder()** (5 connections) — `app/services/file_ops.py`
- **_to_platform()** (4 connections) — `app/api/chat.py`
- **_research_and_create_ppt()** (4 connections) — `app/services/tools.py`
- **_ppt_create()** (3 connections) — `app/services/tools.py`
- **Email** (2 connections) — `docs/features/email-calendar.md`
- **_is_open()** (1 connections) — `app/api/chat.py`
- **_plat()** (1 connections) — `app/api/chat.py`
- **Which player an ambiguous media command ("pause it", "next song") is for: named…** (1 connections) — `app/api/chat.py`
- **Re-target an unspecific media intent (pause/next/play X) to the given platform.** (1 connections) — `app/api/chat.py`
- **"close this song and play shape of you", "pause the video then open mrbeast's…** (1 connections) — `app/api/chat.py`
- **Create a new folder. Supports path shortcuts (Desktop, Downloads, etc.).…** (1 connections) — `app/services/file_ops.py`
- **PPT v6 entry point → ppt_studio.create (adaptive layouts, strict user content,…** (1 connections) — `app/services/ppt_tool.py`
- **Scrapes the web for a topic and extracts verified facts and statistics. Yields…** (1 connections) — `app/services/research_pipeline.py`
- **Email tools: try the real Gmail API (gmail_tool) first, fall back to opening…** (1 connections) — `app/services/tools.py`
- **Generator wrapper — streams live progress to the frontend via chat.py's…** (1 connections) — `app/services/tools.py`
- **Phase 3: Autonomous Research Aggregator. Scrapes live facts from the web,…** (1 connections) — `app/services/tools.py`

## Relationships

- [tools](tools.md) (9 shared connections)
- [youtube_control](youtube_control.md) (7 shared connections)
- [chat + llm](chat_+_llm.md) (6 shared connections)
- [chat + chat-routing](chat_+_chat-routing.md) (3 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (3 shared connections)
- [memory + CLAUDE](memory_+_CLAUDE.md) (3 shared connections)
- [file_ops](file_ops.md) (2 shared connections)
- [ppt_router](ppt_router.md) (2 shared connections)
- [ppt_tool](ppt_tool.md) (2 shared connections)
- [nlp_extractor + download_kokoro](nlp_extractor_+_download_kokoro.md) (2 shared connections)
- [agentic_web](agentic_web.md) (2 shared connections)
- [assignment_pipeline + assignment_tool](assignment_pipeline_+_assignment_tool.md) (2 shared connections)

## Source Files

- `app/api/chat.py`
- `app/services/file_ops.py`
- `app/services/ppt_tool.py`
- `app/services/research_pipeline.py`
- `app/services/tools.py`
- `docs/KNOWN_ISSUES.md`
- `docs/features/email-calendar.md`
- `docs/features/tool-registry.md`

## Audit Trail

- EXTRACTED: 41 (54%)
- INFERRED: 35 (46%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*