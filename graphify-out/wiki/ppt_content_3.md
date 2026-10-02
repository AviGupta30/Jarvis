# ppt_content

> 22 nodes · cohesion 0.16

## Key Concepts

- **Flow — create (`ppt_tool.ppt_create` → `ppt_studio.create`, a generator)** (27 connections) — `docs/features/ppt.md`
- **architect_slides()** (13 connections) — `app/services/ppt_content.py`
- **_complete_from_source()** (9 connections) — `app/services/ppt_content.py`
- **_missing_parts()** (8 connections) — `app/services/ppt_content.py`
- **extractive_ok()** (7 connections) — `app/services/ppt_content.py`
- **sections_fallback()** (5 connections) — `app/services/ppt_content.py`
- **_tok()** (5 connections) — `app/services/ppt_content.py`
- **ask()** (4 connections) — `app/services/ppt_content.py`
- **_retry()** (4 connections) — `app/services/ppt_content.py`
- **deck_facts()** (4 connections) — `app/services/ppt_content.py`
- **needs_architect()** (4 connections) — `app/services/ppt_content.py`
- **plain_md()** (4 connections) — `app/services/ppt_content.py`
- **run()** (3 connections) — `app/services/ppt_content.py`
- **_spec_texts()** (3 connections) — `app/services/ppt_content.py`
- **_copy_sec()** (1 connections) — `app/services/ppt_content.py`
- **True if the slide only re-uses the user's words (≥ min_ratio of tokens) and…** (1 connections) — `app/services/ppt_content.py`
- **Deterministic structure: 'Label:' lines start sections, 'Head: text' lines…** (1 connections) — `app/services/ppt_content.py`
- **Names worth knowing on every slide (product, team, event) — pulled verbatim…** (1 connections) — `app/services/ppt_content.py`
- **Labelled parts of the user's content ('Skill Gaps: …', 'Before vs. After …:')…** (1 connections) — `app/services/ppt_content.py`
- **Guarantee no content loss: labelled parts of the user's text that the designed…** (1 connections) — `app/services/ppt_content.py`
- **LLM restructures each slide's raw content (wording kept, verified);…** (1 connections) — `app/services/ppt_content.py`
- **Rich / paragraph-style content needs real restructuring, not a bullet dump.** (1 connections) — `app/services/ppt_content.py`

## Relationships

- [ppt_content](ppt_content.md) (19 shared connections)
- [ppt_studio + ppt_content](ppt_studio_+_ppt_content.md) (6 shared connections)
- [ppt_content + KNOWN_ISSUES](ppt_content_+_KNOWN_ISSUES.md) (4 shared connections)
- [ppt_tool + ppt_image_engine](ppt_tool_+_ppt_image_engine.md) (2 shared connections)
- [youtube_player](youtube_player.md) (1 shared connections)
- [ppt](ppt.md) (1 shared connections)
- [ppt_designer](ppt_designer.md) (1 shared connections)
- [ppt_studio](ppt_studio.md) (1 shared connections)
- [ppt_template](ppt_template.md) (1 shared connections)

## Source Files

- `app/services/ppt_content.py`
- `docs/features/ppt.md`

## Audit Trail

- EXTRACTED: 41 (57%)
- INFERRED: 31 (43%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*