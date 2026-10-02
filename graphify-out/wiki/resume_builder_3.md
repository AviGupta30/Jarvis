# resume_builder

> 20 nodes · cohesion 0.17

## Key Concepts

- **create_resume()** (16 connections) — `app/services/resume_builder.py`
- **detect_resume_request()** (14 connections) — `app/services/resume_builder.py`
- **editor_save()** (13 connections) — `app/services/resume_builder.py`
- **_load_state()** (10 connections) — `app/services/resume_builder.py`
- **Visual editor (/resume/editor)** (8 connections) — `docs/features/resume-creator.md`
- **_normalise_content()** (7 connections) — `app/services/resume_builder.py`
- **_edit_content()** (6 connections) — `app/services/resume_builder.py`
- **_split_images()** (6 connections) — `app/services/resume_builder.py`
- **open_resume_editor()** (5 connections) — `app/services/resume_builder.py`
- **_save_state()** (5 connections) — `app/services/resume_builder.py`
- **_has_details()** (4 connections) — `app/services/resume_builder.py`
- **_apply_op()** (3 connections) — `app/services/resume_builder.py`
- **_attachments()** (3 connections) — `app/services/resume_builder.py`
- **resume_awaiting_details()** (3 connections) — `app/services/resume_builder.py`
- **_strip_tags()** (3 connections) — `app/services/resume_builder.py`
- **_str_list()** (2 connections) — `app/services/resume_builder.py`
- **Backend of the editor: apply text edits + one optional action, persist,…** (1 connections) — `app/services/resume_builder.py`
- **→ (reference_image, photo). A photo is labelled as such or is a close-up face.** (1 connections) — `app/services/resume_builder.py`
- **Fast regex router → create_resume kwargs (or {"_list": True}), else None.** (1 connections) — `app/services/resume_builder.py`
- **Generator: progress lines, then markdown with PNG preview(s) + PDF/HTML links.** (1 connections) — `app/services/resume_builder.py`

## Relationships

- [resume_builder](resume_builder.md) (36 shared connections)
- [chat + rag_memory](chat_+_rag_memory.md) (6 shared connections)
- [tools](tools.md) (2 shared connections)
- [resume-creator](resume-creator.md) (2 shared connections)
- [resume_router](resume_router.md) (2 shared connections)

## Source Files

- `app/services/resume_builder.py`
- `docs/features/resume-creator.md`

## Audit Trail

- EXTRACTED: 67 (84%)
- INFERRED: 13 (16%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*