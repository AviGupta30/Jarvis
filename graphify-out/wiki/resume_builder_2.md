# resume_builder

> 23 nodes · cohesion 0.13

## Key Concepts

- **_build_content()** (12 connections) — `app/services/resume_builder.py`
- **_drop_invented()** (9 connections) — `app/services/resume_builder.py`
- **_fit_render()** (9 connections) — `app/services/resume_builder.py`
- **Gotchas** (9 connections) — `docs/features/resume-creator.md`
- **Fixed on 2026-10-02 (resume creator)** (9 connections) — `docs/KNOWN_ISSUES.md`
- **_condense_content()** (8 connections) — `app/services/resume_builder.py`
- **_restore_dropped()** (7 connections) — `app/services/resume_builder.py`
- **_finalize_content()** (6 connections) — `app/services/resume_builder.py`
- **_guess_name()** (5 connections) — `app/services/resume_builder.py`
- **_similar()** (5 connections) — `app/services/resume_builder.py`
- **_guess_title()** (4 connections) — `app/services/resume_builder.py`
- **_nums()** (4 connections) — `app/services/resume_builder.py`
- **_user_headings()** (4 connections) — `app/services/resume_builder.py`
- **ok()** (3 connections) — `app/services/resume_builder.py`
- **_content_brief()** (2 connections) — `app/services/resume_builder.py`
- **clean_text()** (2 connections) — `app/services/resume_builder.py`
- **_words()** (2 connections) — `app/services/resume_builder.py`
- **The LLM likes to 'improve' bullets with made-up metrics. Drop any…** (1 connections) — `app/services/resume_builder.py`
- **Smaller fallback models sometimes drop the name; recover it from the user's own…** (1 connections) — `app/services/resume_builder.py`
- **Deterministic clean-up after the LLM: invented job entries, repeated facts,…** (1 connections) — `app/services/resume_builder.py`
- **Fallback models sometimes silently drop a project's/job's points. Re-add any…** (1 connections) — `app/services/resume_builder.py`
- **Render; with a page target, shrink → AI-condense → trim until it fits. Returns…** (1 connections) — `app/services/resume_builder.py`
- **where()** (1 connections) — `app/services/resume_builder.py`

## Relationships

- [resume_builder](resume_builder.md) (18 shared connections)
- [resume_builder + resume-exact-replica](resume_builder_+_resume-exact-replica.md) (13 shared connections)
- [resume_builder + integrate](resume_builder_+_integrate.md) (8 shared connections)
- [analyzer](analyzer.md) (2 shared connections)
- [ppt + KNOWN_ISSUES](ppt_+_KNOWN_ISSUES.md) (1 shared connections)

## Source Files

- `app/services/resume_builder.py`
- `docs/KNOWN_ISSUES.md`
- `docs/features/resume-creator.md`

## Audit Trail

- EXTRACTED: 47 (64%)
- INFERRED: 27 (36%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*