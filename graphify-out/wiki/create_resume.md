# create_resume()

> God node · 31 connections · `app/services/resume_builder.py`

**Community:** [resume_builder + integrate](resume_builder_+_integrate.md)

## Connections by Relation

### calls
- [chat_endpoint()](chat_endpoint.md) `EXTRACTED`
- _build_content() `EXTRACTED`
- _sanitize_design() `EXTRACTED`
- _resolve_design() `EXTRACTED`
- _load_state() `EXTRACTED`
- _apply_color() `EXTRACTED`
- _edit_content() `EXTRACTED`
- replica_design() `EXTRACTED`
- _split_images() `EXTRACTED`
- detect() `EXTRACTED`
- analyse_with_progress() `EXTRACTED`
- _tpl_key() `EXTRACTED`
- _logo_image() `EXTRACTED`
- _stash_design() `EXTRACTED`
- _crop_photo() `EXTRACTED`
- _save_state() `EXTRACTED`
- resume_tool() `EXTRACTED`
- replica_note() `EXTRACTED`
- _has_details() `EXTRACTED`
- _apply_layout_hint() `EXTRACTED`
- *…and 3 more `calls` connection(s) not listed (lowest-degree first to go)*

### contains
- resume_builder.py `EXTRACTED`

### imports
- chat.py `EXTRACTED`

### rationale_for
- Generator: progress lines, then markdown with PNG preview(s) + PDF/HTML links. `EXTRACTED`

### references
- [Tool registry](Tool_registry.md) `INFERRED`
- Exact replica engine (`app/services/resume_replica/`, 2026-10-03) `INFERRED`
- Plan: exact design replication for the resume creator `INFERRED`
- 5. Integration in Jarvis `INFERRED`
- Campus / placement format (`app/services/resume_campus.py`, 2026-10-04) `INFERRED`

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*