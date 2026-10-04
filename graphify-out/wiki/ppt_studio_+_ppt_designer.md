# ppt_studio + ppt_designer

> 45 nodes · cohesion 0.09

## Key Concepts

- **ppt_studio.py** (45 connections) — `app/services/ppt_studio.py`
- **create()** (34 connections) — `app/services/ppt_studio.py`
- **_create_format()** (12 connections) — `app/services/ppt_studio.py`
- **edit()** (12 connections) — `app/services/ppt_studio.py`
- **_finish_theme()** (10 connections) — `app/services/ppt_designer.py`
- **ppt_edit()** (10 connections) — `app/services/ppt_tool.py`
- **resolve_theme()** (9 connections) — `app/services/ppt_designer.py`
- **theme_from_palette()** (8 connections) — `app/services/ppt_designer.py`
- **_load_state()** (6 connections) — `app/services/ppt_studio.py`
- **_reference_theme()** (6 connections) — `app/services/ppt_studio.py`
- **_render_safely()** (6 connections) — `app/services/ppt_studio.py`
- **split_request()** (5 connections) — `app/services/ppt_content.py`
- **_lum()** (5 connections) — `app/services/ppt_designer.py`
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
- **_collect_attachments()** (3 connections) — `app/services/ppt_studio.py`
- **_desktop()** (3 connections) — `app/services/ppt_studio.py`
- *... and 20 more nodes in this community*

## Relationships

- [ppt_content](ppt_content.md) (23 shared connections)
- [ppt_designer](ppt_designer.md) (10 shared connections)
- [ppt_composer + ppt_designer](ppt_composer_+_ppt_designer.md) (6 shared connections)
- [ppt_template](ppt_template.md) (6 shared connections)
- [ppt_tool](ppt_tool.md) (4 shared connections)
- [ppt_studio](ppt_studio.md) (3 shared connections)
- [tools](tools.md) (3 shared connections)
- [server + persistence](server_+_persistence.md) (2 shared connections)
- [chat-routing + chat](chat-routing_+_chat.md) (2 shared connections)
- [repair](repair.md) (1 shared connections)
- [benchmark + download_kokoro](benchmark_+_download_kokoro.md) (1 shared connections)
- [assignment_assembler + smart_navigator](assignment_assembler_+_smart_navigator.md) (1 shared connections)

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

- EXTRACTED: 142 (89%)
- INFERRED: 17 (11%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*