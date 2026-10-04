# resume_builder + integrate

> 37 nodes · cohesion 0.08

## Key Concepts

- **create_resume()** (32 connections) — `app/services/resume_builder.py`
- **Exact replica engine (`app/services/resume_replica/`, 2026-10-03)** (23 connections) — `docs/features/resume-creator.md`
- **detect_resume_request()** (15 connections) — `app/services/resume_builder.py`
- **_load_state()** (10 connections) — `app/services/resume_builder.py`
- **integrate.py** (10 connections) — `app/services/resume_replica/integrate.py`
- **replica_design()** (8 connections) — `app/services/resume_replica/integrate.py`
- **_split_images()** (7 connections) — `app/services/resume_builder.py`
- **detect()** (7 connections) — `app/services/resume_campus.py`
- **analyse_with_progress()** (7 connections) — `app/services/resume_replica/integrate.py`
- **_logo_image()** (6 connections) — `app/services/resume_builder.py`
- **open_resume_editor()** (5 connections) — `app/services/resume_builder.py`
- **resume_tool()** (5 connections) — `app/services/resume_builder.py`
- **_save_state()** (5 connections) — `app/services/resume_builder.py`
- **title_key()** (5 connections) — `app/services/resume_replica/measure.py`
- **main()** (5 connections) — `scripts/replica_eval.py`
- **_apply_layout_hint()** (4 connections) — `app/services/resume_builder.py`
- **_attachments()** (4 connections) — `app/services/resume_builder.py`
- **_has_details()** (4 connections) — `app/services/resume_builder.py`
- **list_resume_templates()** (4 connections) — `app/services/resume_builder.py`
- **replica_note()** (4 connections) — `app/services/resume_replica/integrate.py`
- **Campus / placement format (`app/services/resume_campus.py`, 2026-10-04)** (4 connections) — `docs/features/resume-creator.md`
- **_is_logo_label()** (3 connections) — `app/services/resume_builder.py`
- **_recent_resume()** (3 connections) — `app/services/resume_builder.py`
- **resume_awaiting_details()** (3 connections) — `app/services/resume_builder.py`
- **_strip_tags()** (3 connections) — `app/services/resume_builder.py`
- *... and 12 more nodes in this community*

## Relationships

- [resume_builder](resume_builder.md) (45 shared connections)
- [resume_builder + resume-creator](resume_builder_+_resume-creator.md) (8 shared connections)
- [exact_render](exact_render.md) (6 shared connections)
- [resume_builder + resume-exact-replica](resume_builder_+_resume-exact-replica.md) (5 shared connections)
- [pipeline](pipeline.md) (5 shared connections)
- [plate](plate.md) (5 shared connections)
- [chat](chat.md) (4 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (4 shared connections)
- [measure](measure.md) (4 shared connections)
- [jarvis_overlay + prompt_overlay](jarvis_overlay_+_prompt_overlay.md) (3 shared connections)
- [tools + window_layout](tools_+_window_layout.md) (2 shared connections)
- [server + persistence](server_+_persistence.md) (2 shared connections)

## Source Files

- `app/services/resume_builder.py`
- `app/services/resume_campus.py`
- `app/services/resume_replica/integrate.py`
- `app/services/resume_replica/measure.py`
- `docs/features/resume-creator.md`
- `scripts/replica_eval.py`

## Audit Trail

- EXTRACTED: 111 (76%)
- INFERRED: 36 (24%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*