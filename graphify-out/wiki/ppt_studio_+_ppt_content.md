# ppt_studio + ppt_content

> 40 nodes · cohesion 0.09

## Key Concepts

- **ppt_studio.py** (45 connections) — `app/services/ppt_studio.py`
- **create()** (34 connections) — `app/services/ppt_studio.py`
- **_create_format()** (12 connections) — `app/services/ppt_studio.py`
- **_finish_theme()** (10 connections) — `app/services/ppt_designer.py`
- **resolve_theme()** (9 connections) — `app/services/ppt_designer.py`
- **theme_from_palette()** (8 connections) — `app/services/ppt_designer.py`
- **parse_instructions()** (7 connections) — `app/services/ppt_content.py`
- **_load_state()** (6 connections) — `app/services/ppt_studio.py`
- **_reference_theme()** (6 connections) — `app/services/ppt_studio.py`
- **_render_safely()** (6 connections) — `app/services/ppt_studio.py`
- **_lum()** (5 connections) — `app/services/ppt_designer.py`
- **_label()** (5 connections) — `app/services/ppt_template.py`
- **_caption()** (4 connections) — `app/services/ppt_studio.py`
- **has_active_deck()** (4 connections) — `app/services/ppt_studio.py`
- **_out_path()** (4 connections) — `app/services/ppt_studio.py`
- **_push()** (4 connections) — `app/services/ppt_studio.py`
- **_render()** (4 connections) — `app/services/ppt_studio.py`
- **_save_state()** (4 connections) — `app/services/ppt_studio.py`
- **detect_profile()** (3 connections) — `app/services/ppt_content.py`
- **raw_slide_blocks()** (3 connections) — `app/services/ppt_content.py`
- **slide_count()** (3 connections) — `app/services/ppt_content.py`
- **_slide_ref()** (3 connections) — `app/services/ppt_content.py`
- **_desktop()** (3 connections) — `app/services/ppt_studio.py`
- **_images_per_slide()** (3 connections) — `app/services/ppt_studio.py`
- **_theme_from_text()** (3 connections) — `app/services/ppt_studio.py`
- *... and 15 more nodes in this community*

## Relationships

- [ppt_content](ppt_content.md) (23 shared connections)
- [ppt + ppt_studio](ppt_+_ppt_studio.md) (11 shared connections)
- [ppt_designer](ppt_designer.md) (10 shared connections)
- [ppt_composer + ppt_designer](ppt_composer_+_ppt_designer.md) (6 shared connections)
- [ppt_template](ppt_template.md) (6 shared connections)
- [message_reader + thread_extractor](message_reader_+_thread_extractor.md) (5 shared connections)
- [voice_agent + download_kokoro](voice_agent_+_download_kokoro.md) (3 shared connections)
- [ppt_tool](ppt_tool.md) (3 shared connections)
- [ppt_studio](ppt_studio.md) (3 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (2 shared connections)
- [repair + assignment_humanizer](repair_+_assignment_humanizer.md) (1 shared connections)
- [ppt_router + ppt_tool](ppt_router_+_ppt_tool.md) (1 shared connections)

## Source Files

- `app/services/ppt_content.py`
- `app/services/ppt_designer.py`
- `app/services/ppt_studio.py`
- `app/services/ppt_template.py`

## Audit Trail

- EXTRACTED: 139 (96%)
- INFERRED: 6 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*