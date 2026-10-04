# resume_builder + integrate

> 32 nodes · cohesion 0.09

## Key Concepts

- **create_resume()** (31 connections) — `app/services/resume_builder.py`
- **Exact replica engine (`app/services/resume_replica/`, 2026-10-03)** (23 connections) — `docs/features/resume-creator.md`
- **detect_resume_request()** (15 connections) — `app/services/resume_builder.py`
- **_load_state()** (10 connections) — `app/services/resume_builder.py`
- **integrate.py** (10 connections) — `app/services/resume_replica/integrate.py`
- **_split_images()** (7 connections) — `app/services/resume_builder.py`
- **analyse_with_progress()** (7 connections) — `app/services/resume_replica/integrate.py`
- **_logo_image()** (6 connections) — `app/services/resume_builder.py`
- **open_resume_editor()** (5 connections) — `app/services/resume_builder.py`
- **resume_tool()** (5 connections) — `app/services/resume_builder.py`
- **_save_state()** (5 connections) — `app/services/resume_builder.py`
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
- **replica_enabled()** (3 connections) — `app/services/resume_replica/integrate.py`
- **UI** (2 connections) — `docs/features/resume-creator.md`
- **The user said which column a section goes in → that wins over the reference…** (1 connections) — `app/services/resume_builder.py`
- **An attachment labelled as a (college/company) logo → its path.** (1 connections) — `app/services/resume_builder.py`
- *... and 7 more nodes in this community*

## Relationships

- [resume_builder](resume_builder.md) (29 shared connections)
- [resume_builder + exact_render](resume_builder_+_exact_render.md) (12 shared connections)
- [resume_builder + resume-exact-replica](resume_builder_+_resume-exact-replica.md) (10 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (8 shared connections)
- [exact_render](exact_render.md) (7 shared connections)
- [plate](plate.md) (5 shared connections)
- [measure](measure.md) (4 shared connections)
- [pipeline](pipeline.md) (4 shared connections)
- [tools](tools.md) (2 shared connections)
- [message_reader + thread_extractor](message_reader_+_thread_extractor.md) (2 shared connections)
- [voice_agent + download_kokoro](voice_agent_+_download_kokoro.md) (1 shared connections)

## Source Files

- `app/services/resume_builder.py`
- `app/services/resume_replica/integrate.py`
- `docs/features/resume-creator.md`

## Audit Trail

- EXTRACTED: 93 (72%)
- INFERRED: 36 (28%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*