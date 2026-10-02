# resume_builder

> 26 nodes · cohesion 0.13

## Key Concepts

- **_build_content()** (12 connections) — `app/services/resume_builder.py`
- **Content fidelity & page limits (2026-10-02)** (12 connections) — `docs/features/resume-creator.md`
- **_drop_invented()** (9 connections) — `app/services/resume_builder.py`
- **Fixed on 2026-10-02 (resume creator)** (9 connections) — `docs/KNOWN_ISSUES.md`
- **_fit_render()** (8 connections) — `app/services/resume_builder.py`
- **_restore_dropped()** (7 connections) — `app/services/resume_builder.py`
- **_condense_content()** (6 connections) — `app/services/resume_builder.py`
- **_finalize_content()** (6 connections) — `app/services/resume_builder.py`
- **_placement()** (6 connections) — `app/services/resume_builder.py`
- **_guess_name()** (5 connections) — `app/services/resume_builder.py`
- **_similar()** (5 connections) — `app/services/resume_builder.py`
- **Gotchas** (5 connections) — `docs/features/resume-creator.md`
- **_guess_title()** (4 connections) — `app/services/resume_builder.py`
- **_nums()** (4 connections) — `app/services/resume_builder.py`
- **_user_headings()** (4 connections) — `app/services/resume_builder.py`
- **ok()** (3 connections) — `app/services/resume_builder.py`
- **_content_brief()** (2 connections) — `app/services/resume_builder.py`
- **clean_text()** (2 connections) — `app/services/resume_builder.py`
- **_words()** (2 connections) — `app/services/resume_builder.py`
- **Smaller fallback models sometimes drop the name; recover it from the user's own…** (1 connections) — `app/services/resume_builder.py`
- **Deterministic clean-up after the LLM: invented job entries, repeated facts,…** (1 connections) — `app/services/resume_builder.py`
- **Fallback models sometimes silently drop a project's/job's points. Re-add any…** (1 connections) — `app/services/resume_builder.py`
- **Design's column lists + every other section (content or not) appended where it…** (1 connections) — `app/services/resume_builder.py`
- **Render; with a page target, shrink → AI-condense → trim until it fits. Returns…** (1 connections) — `app/services/resume_builder.py`
- **The LLM likes to 'improve' bullets with made-up metrics. Drop any…** (1 connections) — `app/services/resume_builder.py`
- *... and 1 more nodes in this community*

## Relationships

- [resume_builder](resume_builder.md) (33 shared connections)
- [resume-creator](resume-creator.md) (2 shared connections)
- [ppt + KNOWN_ISSUES](ppt_+_KNOWN_ISSUES.md) (1 shared connections)

## Source Files

- `app/services/resume_builder.py`
- `docs/KNOWN_ISSUES.md`
- `docs/features/resume-creator.md`

## Audit Trail

- EXTRACTED: 52 (68%)
- INFERRED: 25 (32%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*