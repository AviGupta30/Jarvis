# resume_builder + exact_render

> 34 nodes · cohesion 0.09

## Key Concepts

- **editor_save()** (29 connections) — `app/services/resume_builder.py`
- **Visual editor (/resume/editor)** (16 connections) — `docs/features/resume-creator.md`
- **editor_page()** (15 connections) — `app/services/resume_builder.py`
- **_normalise_content()** (10 connections) — `app/services/resume_builder.py`
- **_ref_copy_design()** (9 connections) — `app/services/resume_builder.py`
- **replica_design()** (8 connections) — `app/services/resume_replica/integrate.py`
- **_tpl_key()** (7 connections) — `app/services/resume_builder.py`
- **load_spec()** (7 connections) — `app/services/resume_replica/exact_render.py`
- **5. Integration in Jarvis** (7 connections) — `docs/plans/resume-exact-replica.md`
- **_custom_sections()** (6 connections) — `app/services/resume_builder.py`
- **_raster_palette()** (6 connections) — `app/services/resume_builder.py`
- **_stash_design()** (6 connections) — `app/services/resume_builder.py`
- **_state_rev()** (6 connections) — `app/services/resume_builder.py`
- **asset_files()** (6 connections) — `app/services/resume_replica/exact_render.py`
- **_undo_push()** (5 connections) — `app/services/resume_builder.py`
- **_file_hash()** (5 connections) — `app/services/resume_replica/pipeline.py`
- **main()** (5 connections) — `scripts/replica_eval.py`
- **_apply_op()** (4 connections) — `app/services/resume_builder.py`
- **undo_id()** (3 connections) — `app/services/resume_builder.py`
- **_str_list()** (3 connections) — `app/services/resume_builder.py`
- **_undo_snap()** (3 connections) — `app/services/resume_builder.py`
- **walk()** (3 connections) — `app/services/resume_replica/exact_render.py`
- **_undo_get()** (2 connections) — `app/services/resume_builder.py`
- **User-made sections from the editor: {id: custom_N, title, style, items}. Kept…** (1 connections) — `app/services/resume_builder.py`
- **Which template a design is: a preset name, 'copy:<sha>' for an exact copy,…** (1 connections) — `app/services/resume_builder.py`
- *... and 9 more nodes in this community*

## Relationships

- [resume_builder](resume_builder.md) (43 shared connections)
- [resume_builder + integrate](resume_builder_+_integrate.md) (12 shared connections)
- [resume_builder + resume-exact-replica](resume_builder_+_resume-exact-replica.md) (5 shared connections)
- [resume_router](resume_router.md) (4 shared connections)
- [exact_render](exact_render.md) (4 shared connections)
- [pipeline](pipeline.md) (4 shared connections)
- [voice_agent + download_kokoro](voice_agent_+_download_kokoro.md) (2 shared connections)
- [analyzer](analyzer.md) (1 shared connections)
- [youtube_player](youtube_player.md) (1 shared connections)
- [lru](lru.md) (1 shared connections)
- [compiler](compiler.md) (1 shared connections)

## Source Files

- `app/services/resume_builder.py`
- `app/services/resume_replica/exact_render.py`
- `app/services/resume_replica/integrate.py`
- `app/services/resume_replica/pipeline.py`
- `docs/features/resume-creator.md`
- `docs/plans/resume-exact-replica.md`
- `scripts/replica_eval.py`

## Audit Trail

- EXTRACTED: 104 (80%)
- INFERRED: 26 (20%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*