# resume_builder + integrate

> 27 nodes · cohesion 0.11

## Key Concepts

- **create_resume()** (25 connections) — `app/services/resume_builder.py`
- **Exact replica engine (`app/services/resume_replica/`, 2026-10-03)** (23 connections) — `docs/features/resume-creator.md`
- **detect_resume_request()** (14 connections) — `app/services/resume_builder.py`
- **_load_state()** (10 connections) — `app/services/resume_builder.py`
- **integrate.py** (10 connections) — `app/services/resume_replica/integrate.py`
- **analyse_with_progress()** (7 connections) — `app/services/resume_replica/integrate.py`
- **replica_design()** (7 connections) — `app/services/resume_replica/integrate.py`
- **_split_images()** (6 connections) — `app/services/resume_builder.py`
- **open_resume_editor()** (5 connections) — `app/services/resume_builder.py`
- **resume_tool()** (5 connections) — `app/services/resume_builder.py`
- **_save_state()** (5 connections) — `app/services/resume_builder.py`
- **_apply_layout_hint()** (4 connections) — `app/services/resume_builder.py`
- **_has_details()** (4 connections) — `app/services/resume_builder.py`
- **replica_note()** (4 connections) — `app/services/resume_replica/integrate.py`
- **_attachments()** (3 connections) — `app/services/resume_builder.py`
- **_face_ratio()** (3 connections) — `app/services/resume_builder.py`
- **resume_awaiting_details()** (3 connections) — `app/services/resume_builder.py`
- **_strip_tags()** (3 connections) — `app/services/resume_builder.py`
- **replica_enabled()** (3 connections) — `app/services/resume_replica/integrate.py`
- **The user said which column a section goes in → that wins over the reference…** (1 connections) — `app/services/resume_builder.py`
- **→ (reference_image, photo). A photo is labelled as such or is a close-up face.** (1 connections) — `app/services/resume_builder.py`
- **Fast regex router → create_resume kwargs (or {"_list": True}), else None.** (1 connections) — `app/services/resume_builder.py`
- **Generator: progress lines, then markdown with PNG preview(s) + PDF/HTML links.** (1 connections) — `app/services/resume_builder.py`
- **Registry entry: also handles a bare 'list templates' request.** (1 connections) — `app/services/resume_builder.py`
- **integrate.py — Glue between resume_builder.create_resume and the exact-replica…** (1 connections) — `app/services/resume_replica/integrate.py`
- *... and 2 more nodes in this community*

## Relationships

- [resume_builder](resume_builder.md) (37 shared connections)
- [resume_builder + resume-exact-replica](resume_builder_+_resume-exact-replica.md) (9 shared connections)
- [chat + llm](chat_+_llm.md) (7 shared connections)
- [exact_render](exact_render.md) (6 shared connections)
- [plate](plate.md) (5 shared connections)
- [benchmark + server](benchmark_+_server.md) (4 shared connections)
- [pipeline](pipeline.md) (4 shared connections)
- [tools](tools.md) (2 shared connections)
- [measure](measure.md) (2 shared connections)

## Source Files

- `app/services/resume_builder.py`
- `app/services/resume_replica/integrate.py`
- `docs/features/resume-creator.md`

## Audit Trail

- EXTRACTED: 81 (71%)
- INFERRED: 33 (29%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*