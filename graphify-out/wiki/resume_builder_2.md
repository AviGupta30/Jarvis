# resume_builder

> 26 nodes · cohesion 0.10

## Key Concepts

- **editor_save()** (14 connections) — `app/services/resume_builder.py`
- **_render_files()** (13 connections) — `app/services/resume_builder.py`
- **editor_page()** (10 connections) — `app/services/resume_builder.py`
- **resume_router.py** (8 connections) — `app/api/resume_router.py`
- **_normalise_content()** (8 connections) — `app/services/resume_builder.py`
- **Visual editor (/resume/editor)** (8 connections) — `docs/features/resume-creator.md`
- **_edit_content()** (6 connections) — `app/services/resume_builder.py`
- **_effective_design()** (5 connections) — `app/services/resume_builder.py`
- **_render_html()** (5 connections) — `app/services/resume_builder.py`
- **_balance_columns()** (4 connections) — `app/services/resume_builder.py`
- **resume_editor()** (3 connections) — `app/api/resume_router.py`
- **resume_save()** (3 connections) — `app/api/resume_router.py`
- **_apply_op()** (3 connections) — `app/services/resume_builder.py`
- **_data_uri()** (3 connections) — `app/services/resume_builder.py`
- **_editor_toolbar()** (3 connections) — `app/services/resume_builder.py`
- **fastapi_responses** (3 connections)
- **_launch()** (2 connections) — `app/services/resume_builder.py`
- **_str_list()** (2 connections) — `app/services/resume_builder.py`
- **get** (1 connections)
- **post** (1 connections)
- **resume_router.py — FastAPI router for the visual resume editor…** (1 connections) — `app/api/resume_router.py`
- **Per-content tweaks: projects take an empty Experience slot; headings the user…** (1 connections) — `app/services/resume_builder.py`
- **Greedy: move the section that most reduces the taller column, until no move…** (1 connections) — `app/services/resume_builder.py`
- **HTML → PDF (auto-shrinks to avoid a nearly-empty last page) → PNG previews.** (1 connections) — `app/services/resume_builder.py`
- **Full HTML page of the current resume in edit mode.** (1 connections) — `app/services/resume_builder.py`
- *... and 1 more nodes in this community*

## Relationships

- [resume_builder](resume_builder.md) (40 shared connections)
- [agents + tool_runner](agents_+_tool_runner.md) (1 shared connections)
- [main](main.md) (1 shared connections)
- [resume-creator](resume-creator.md) (1 shared connections)
- [chat + llm](chat_+_llm.md) (1 shared connections)
- [ppt_router](ppt_router.md) (1 shared connections)

## Source Files

- `app/api/resume_router.py`
- `app/services/resume_builder.py`
- `docs/features/resume-creator.md`

## Audit Trail

- EXTRACTED: 65 (83%)
- INFERRED: 13 (17%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*