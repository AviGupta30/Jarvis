# resume_builder

> 21 nodes · cohesion 0.13

## Key Concepts

- **create_resume()** (16 connections) — `app/services/resume_builder.py`
- **detect_resume_request()** (13 connections) — `app/services/resume_builder.py`
- **_analyse_design()** (10 connections) — `app/services/resume_builder.py`
- **_load_state()** (7 connections) — `app/services/resume_builder.py`
- **_split_images()** (6 connections) — `app/services/resume_builder.py`
- **resume_tool()** (5 connections) — `app/services/resume_builder.py`
- **_apply_layout_answer()** (4 connections) — `app/services/resume_builder.py`
- **_has_details()** (4 connections) — `app/services/resume_builder.py`
- **list_resume_templates()** (4 connections) — `app/services/resume_builder.py`
- **_palette()** (4 connections) — `app/services/resume_builder.py`
- **_save_state()** (4 connections) — `app/services/resume_builder.py`
- **_attachments()** (3 connections) — `app/services/resume_builder.py`
- **resume_awaiting_details()** (3 connections) — `app/services/resume_builder.py`
- **_strip_tags()** (3 connections) — `app/services/resume_builder.py`
- **_file_hash()** (2 connections) — `app/services/resume_builder.py`
- **_title_key()** (2 connections) — `app/services/resume_builder.py`
- **→ (reference_image, photo). A photo is labelled as such or is a close-up face.** (1 connections) — `app/services/resume_builder.py`
- **Fast regex router → create_resume kwargs (or {"_list": True}), else None.** (1 connections) — `app/services/resume_builder.py`
- **Generator: progress lines, then markdown with PNG preview(s) + PDF/HTML links.** (1 connections) — `app/services/resume_builder.py`
- **Registry entry: also handles a bare 'list templates' request.** (1 connections) — `app/services/resume_builder.py`
- **Dominant colours (hex, share) — gives the VLM exact values to pick from.** (1 connections) — `app/services/resume_builder.py`

## Relationships

- [resume_builder](resume_builder.md) (29 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (6 shared connections)
- [resume-creator](resume-creator.md) (2 shared connections)
- [tools](tools.md) (2 shared connections)

## Source Files

- `app/services/resume_builder.py`

## Audit Trail

- EXTRACTED: 58 (87%)
- INFERRED: 9 (13%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*