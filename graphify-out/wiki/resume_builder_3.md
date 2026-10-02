# resume_builder

> 17 nodes · cohesion 0.16

## Key Concepts

- **create_resume()** (18 connections) — `app/services/resume_builder.py`
- **detect_resume_request()** (14 connections) — `app/services/resume_builder.py`
- **_load_state()** (10 connections) — `app/services/resume_builder.py`
- **_split_images()** (6 connections) — `app/services/resume_builder.py`
- **open_resume_editor()** (5 connections) — `app/services/resume_builder.py`
- **resume_tool()** (5 connections) — `app/services/resume_builder.py`
- **_apply_layout_hint()** (4 connections) — `app/services/resume_builder.py`
- **_has_details()** (4 connections) — `app/services/resume_builder.py`
- **_attachments()** (3 connections) — `app/services/resume_builder.py`
- **_parse_pages()** (3 connections) — `app/services/resume_builder.py`
- **resume_awaiting_details()** (3 connections) — `app/services/resume_builder.py`
- **_strip_tags()** (3 connections) — `app/services/resume_builder.py`
- **The user said which column a section goes in → that wins over the reference…** (1 connections) — `app/services/resume_builder.py`
- **→ (reference_image, photo). A photo is labelled as such or is a close-up face.** (1 connections) — `app/services/resume_builder.py`
- **Fast regex router → create_resume kwargs (or {"_list": True}), else None.** (1 connections) — `app/services/resume_builder.py`
- **Generator: progress lines, then markdown with PNG preview(s) + PDF/HTML links.** (1 connections) — `app/services/resume_builder.py`
- **Registry entry: also handles a bare 'list templates' request.** (1 connections) — `app/services/resume_builder.py`

## Relationships

- [resume_builder](resume_builder.md) (29 shared connections)
- [chat + llm](chat_+_llm.md) (7 shared connections)
- [tools + whatsapp_smart](tools_+_whatsapp_smart.md) (2 shared connections)
- [resume-creator](resume-creator.md) (1 shared connections)

## Source Files

- `app/services/resume_builder.py`

## Audit Trail

- EXTRACTED: 52 (85%)
- INFERRED: 9 (15%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*