# ppt_studio + ppt_content

> 45 nodes · cohesion 0.08

## Key Concepts

- **ppt_studio.py** (45 connections) — `app/services/ppt_studio.py`
- **create()** (34 connections) — `app/services/ppt_studio.py`
- **_create_format()** (12 connections) — `app/services/ppt_studio.py`
- **edit()** (12 connections) — `app/services/ppt_studio.py`
- **resolve_theme()** (9 connections) — `app/services/ppt_designer.py`
- **ppt_edit()** (9 connections) — `app/services/ppt_tool.py`
- **parse_instructions()** (7 connections) — `app/services/ppt_content.py`
- **_load_state()** (6 connections) — `app/services/ppt_studio.py`
- **_reference_theme()** (6 connections) — `app/services/ppt_studio.py`
- **_render_safely()** (6 connections) — `app/services/ppt_studio.py`
- **split_request()** (5 connections) — `app/services/ppt_content.py`
- **_with_progress()** (5 connections) — `app/services/ppt_studio.py`
- **_label()** (5 connections) — `app/services/ppt_template.py`
- **Fixed on 2026-09-30 (PPT v6)** (5 connections) — `docs/KNOWN_ISSUES.md`
- **_caption()** (4 connections) — `app/services/ppt_studio.py`
- **has_active_deck()** (4 connections) — `app/services/ppt_studio.py`
- **_out_path()** (4 connections) — `app/services/ppt_studio.py`
- **_push()** (4 connections) — `app/services/ppt_studio.py`
- **_render()** (4 connections) — `app/services/ppt_studio.py`
- **_save_state()** (4 connections) — `app/services/ppt_studio.py`
- **Flow — edit (`ppt_edit` → `ppt_studio.edit` → `ppt_content.apply_edit`)** (4 connections) — `docs/features/ppt.md`
- **detect_profile()** (3 connections) — `app/services/ppt_content.py`
- **slide_count()** (3 connections) — `app/services/ppt_content.py`
- **_collect_attachments()** (3 connections) — `app/services/ppt_studio.py`
- **_desktop()** (3 connections) — `app/services/ppt_studio.py`
- *... and 20 more nodes in this community*

## Relationships

- [ppt_content](ppt_content.md) (24 shared connections)
- [ppt_designer](ppt_designer.md) (12 shared connections)
- [ppt_template](ppt_template.md) (8 shared connections)
- [assignment_tool + safe_executor](assignment_tool_+_safe_executor.md) (5 shared connections)
- [ppt_tool + ppt_image_engine](ppt_tool_+_ppt_image_engine.md) (5 shared connections)
- [ppt_content + KNOWN_ISSUES](ppt_content_+_KNOWN_ISSUES.md) (4 shared connections)
- [ppt_studio](ppt_studio.md) (3 shared connections)
- [tools](tools.md) (3 shared connections)
- [voice_agent + acoustic_tripwire](voice_agent_+_acoustic_tripwire.md) (2 shared connections)
- [youtube_control](youtube_control.md) (2 shared connections)
- [persistence + server](persistence_+_server.md) (1 shared connections)
- [ui_inspector + lru](ui_inspector_+_lru.md) (1 shared connections)

## Source Files

- `app/services/ppt_content.py`
- `app/services/ppt_designer.py`
- `app/services/ppt_studio.py`
- `app/services/ppt_template.py`
- `app/services/ppt_tool.py`
- `app/services/tools.py`
- `docs/KNOWN_ISSUES.md`
- `docs/features/ppt.md`

## Audit Trail

- EXTRACTED: 136 (88%)
- INFERRED: 18 (12%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*