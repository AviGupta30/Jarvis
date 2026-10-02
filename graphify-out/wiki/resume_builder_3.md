# resume_builder

> 27 nodes · cohesion 0.12

## Key Concepts

- **create_resume()** (18 connections) — `app/services/resume_builder.py`
- **detect_resume_request()** (14 connections) — `app/services/resume_builder.py`
- **editor_save()** (14 connections) — `app/services/resume_builder.py`
- **_analyse_design()** (12 connections) — `app/services/resume_builder.py`
- **_load_state()** (10 connections) — `app/services/resume_builder.py`
- **_normalise_content()** (8 connections) — `app/services/resume_builder.py`
- **Visual editor (/resume/editor)** (8 connections) — `docs/features/resume-creator.md`
- **_edit_content()** (6 connections) — `app/services/resume_builder.py`
- **_split_images()** (6 connections) — `app/services/resume_builder.py`
- **open_resume_editor()** (5 connections) — `app/services/resume_builder.py`
- **resume_tool()** (5 connections) — `app/services/resume_builder.py`
- **_save_state()** (5 connections) — `app/services/resume_builder.py`
- **_apply_layout_hint()** (4 connections) — `app/services/resume_builder.py`
- **_has_details()** (4 connections) — `app/services/resume_builder.py`
- **_apply_op()** (3 connections) — `app/services/resume_builder.py`
- **_attachments()** (3 connections) — `app/services/resume_builder.py`
- **_parse_pages()** (3 connections) — `app/services/resume_builder.py`
- **resume_awaiting_details()** (3 connections) — `app/services/resume_builder.py`
- **_strip_tags()** (3 connections) — `app/services/resume_builder.py`
- **_file_hash()** (2 connections) — `app/services/resume_builder.py`
- **_str_list()** (2 connections) — `app/services/resume_builder.py`
- **The user said which column a section goes in → that wins over the reference…** (1 connections) — `app/services/resume_builder.py`
- **Backend of the editor: apply text edits + one optional action, persist,…** (1 connections) — `app/services/resume_builder.py`
- **→ (reference_image, photo). A photo is labelled as such or is a close-up face.** (1 connections) — `app/services/resume_builder.py`
- **Fast regex router → create_resume kwargs (or {"_list": True}), else None.** (1 connections) — `app/services/resume_builder.py`
- *... and 2 more nodes in this community*

## Relationships

- [resume_builder](resume_builder.md) (48 shared connections)
- [chat](chat.md) (7 shared connections)
- [resume-creator](resume-creator.md) (3 shared connections)
- [tools](tools.md) (2 shared connections)
- [ppt_router + resume_router](ppt_router_+_resume_router.md) (2 shared connections)

## Source Files

- `app/services/resume_builder.py`
- `docs/features/resume-creator.md`

## Audit Trail

- EXTRACTED: 86 (83%)
- INFERRED: 17 (17%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*