# resume_builder

> 17 nodes · cohesion 0.18

## Key Concepts

- **editor_save()** (25 connections) — `app/services/resume_builder.py`
- **Visual editor (/resume/editor)** (12 connections) — `docs/features/resume-creator.md`
- **_normalise_content()** (10 connections) — `app/services/resume_builder.py`
- **5. Integration in Jarvis** (7 connections) — `docs/plans/resume-exact-replica.md`
- **_custom_sections()** (6 connections) — `app/services/resume_builder.py`
- **_state_rev()** (6 connections) — `app/services/resume_builder.py`
- **_undo_push()** (5 connections) — `app/services/resume_builder.py`
- **main()** (5 connections) — `scripts/replica_eval.py`
- **_apply_op()** (4 connections) — `app/services/resume_builder.py`
- **undo_id()** (3 connections) — `app/services/resume_builder.py`
- **_str_list()** (3 connections) — `app/services/resume_builder.py`
- **_undo_snap()** (3 connections) — `app/services/resume_builder.py`
- **_undo_get()** (2 connections) — `app/services/resume_builder.py`
- **User-made sections from the editor: {id: custom_N, title, style, items}. Kept…** (1 connections) — `app/services/resume_builder.py`
- **Fingerprint of what the editor shows; its client-side undo history is only…** (1 connections) — `app/services/resume_builder.py`
- **Store a whole editor state (before a structural change); returns its id for the…** (1 connections) — `app/services/resume_builder.py`
- **Backend of the editor: apply text edits + one optional action, persist,…** (1 connections) — `app/services/resume_builder.py`

## Relationships

- [resume_builder](resume_builder.md) (27 shared connections)
- [resume_builder + integrate](resume_builder_+_integrate.md) (7 shared connections)
- [resume_builder + resume-exact-replica](resume_builder_+_resume-exact-replica.md) (4 shared connections)
- [resume_router](resume_router.md) (2 shared connections)
- [youtube_control](youtube_control.md) (1 shared connections)
- [lru](lru.md) (1 shared connections)
- [compiler](compiler.md) (1 shared connections)
- [pipeline](pipeline.md) (1 shared connections)
- [benchmark + server](benchmark_+_server.md) (1 shared connections)

## Source Files

- `app/services/resume_builder.py`
- `docs/features/resume-creator.md`
- `docs/plans/resume-exact-replica.md`
- `scripts/replica_eval.py`

## Audit Trail

- EXTRACTED: 49 (70%)
- INFERRED: 21 (30%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*