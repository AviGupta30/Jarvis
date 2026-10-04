# ppt_studio + ppt_designer

> 43 nodes · cohesion 0.09

## Key Concepts

- **ppt_studio.py** (45 connections) — `app/services/ppt_studio.py`
- **create()** (34 connections) — `app/services/ppt_studio.py`
- **_create_format()** (12 connections) — `app/services/ppt_studio.py`
- **edit()** (12 connections) — `app/services/ppt_studio.py`
- **_finish_theme()** (10 connections) — `app/services/ppt_designer.py`
- **prepare_image()** (10 connections) — `app/services/ppt_designer.py`
- **resolve_theme()** (9 connections) — `app/services/ppt_designer.py`
- **theme_from_palette()** (8 connections) — `app/services/ppt_designer.py`
- **_load_state()** (6 connections) — `app/services/ppt_studio.py`
- **_reference_theme()** (6 connections) — `app/services/ppt_studio.py`
- **_render_safely()** (6 connections) — `app/services/ppt_studio.py`
- **split_request()** (5 connections) — `app/services/ppt_content.py`
- **_lum()** (5 connections) — `app/services/ppt_designer.py`
- **_with_progress()** (5 connections) — `app/services/ppt_studio.py`
- **_label()** (5 connections) — `app/services/ppt_template.py`
- **_caption()** (4 connections) — `app/services/ppt_studio.py`
- **has_active_deck()** (4 connections) — `app/services/ppt_studio.py`
- **_out_path()** (4 connections) — `app/services/ppt_studio.py`
- **_push()** (4 connections) — `app/services/ppt_studio.py`
- **_render()** (4 connections) — `app/services/ppt_studio.py`
- **_save_state()** (4 connections) — `app/services/ppt_studio.py`
- **raw_slide_blocks()** (3 connections) — `app/services/ppt_content.py`
- **_collect_attachments()** (3 connections) — `app/services/ppt_studio.py`
- **_desktop()** (3 connections) — `app/services/ppt_studio.py`
- **_images_per_slide()** (3 connections) — `app/services/ppt_studio.py`
- *... and 18 more nodes in this community*

## Relationships

- [ppt_content](ppt_content.md) (21 shared connections)
- [ppt_designer](ppt_designer.md) (11 shared connections)
- [ppt_template](ppt_template.md) (10 shared connections)
- [ppt_composer + ppt_designer](ppt_composer_+_ppt_designer.md) (6 shared connections)
- [benchmark + server](benchmark_+_server.md) (4 shared connections)
- [ppt_tool](ppt_tool.md) (3 shared connections)
- [ppt_studio](ppt_studio.md) (3 shared connections)
- [ppt + KNOWN_ISSUES](ppt_+_KNOWN_ISSUES.md) (3 shared connections)
- [repair + renderer](repair_+_renderer.md) (1 shared connections)
- [nlp_extractor + download_kokoro](nlp_extractor_+_download_kokoro.md) (1 shared connections)
- [assignment_assembler + smart_navigator](assignment_assembler_+_smart_navigator.md) (1 shared connections)
- [social_content_manager + tools](social_content_manager_+_tools.md) (1 shared connections)

## Source Files

- `app/services/ppt_content.py`
- `app/services/ppt_designer.py`
- `app/services/ppt_studio.py`
- `app/services/ppt_template.py`

## Audit Trail

- EXTRACTED: 145 (95%)
- INFERRED: 8 (5%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*