# ppt_content + ppt_designer

> 29 nodes · cohesion 0.11

## Key Concepts

- **create()** (34 connections) — `app/services/ppt_studio.py`
- **Flow — create (`ppt_tool.ppt_create` → `ppt_studio.create`, a generator)** (27 connections) — `docs/features/ppt.md`
- **_finish_theme()** (10 connections) — `app/services/ppt_designer.py`
- **resolve_theme()** (9 connections) — `app/services/ppt_designer.py`
- **theme_from_palette()** (8 connections) — `app/services/ppt_designer.py`
- **Fixed on 2026-10-01 (PPT)** (8 connections) — `docs/KNOWN_ISSUES.md`
- **interpret_image_instructions()** (6 connections) — `app/services/ppt_content.py`
- **parse_user_slides()** (6 connections) — `app/services/ppt_content.py`
- **repair_text()** (6 connections) — `app/services/ppt_content.py`
- **split_instructions()** (6 connections) — `app/services/ppt_content.py`
- **_reference_theme()** (6 connections) — `app/services/ppt_studio.py`
- **_is_instruction()** (5 connections) — `app/services/ppt_content.py`
- **split_request()** (5 connections) — `app/services/ppt_content.py`
- **_lum()** (5 connections) — `app/services/ppt_designer.py`
- **needs_architect()** (4 connections) — `app/services/ppt_content.py`
- **detect_profile()** (3 connections) — `app/services/ppt_content.py`
- **raw_slide_blocks()** (3 connections) — `app/services/ppt_content.py`
- **Separate the user's command, any pasted/attached content and attachment paths.** (1 connections) — `app/services/ppt_content.py`
- **Return strict slides if the text is written slide-by-slide, else [].** (1 connections) — `app/services/ppt_content.py`
- **Restore structure that copy-paste destroyed ("Title and OverviewEvent: …",…** (1 connections) — `app/services/ppt_content.py`
- **A sentence that talks ABOUT the deck (images, slide count, theme…) rather than…** (1 connections) — `app/services/ppt_content.py`
- **Pull instruction sentences ("use the images in slide 2 only", "both images go…** (1 connections) — `app/services/ppt_content.py`
- **LLM fallback for phrasings the regexes can't resolve. Returns image_rules (same…** (1 connections) — `app/services/ppt_content.py`
- **[(n, heading, raw content)] split on 'Slide N:' markers of repaired text.** (1 connections) — `app/services/ppt_content.py`
- **Rich / paragraph-style content needs real restructuring, not a bullet dump.** (1 connections) — `app/services/ppt_content.py`
- *... and 4 more nodes in this community*

## Relationships

- [ppt_content](ppt_content.md) (32 shared connections)
- [ppt_studio](ppt_studio.md) (22 shared connections)
- [ppt_composer + ppt_designer](ppt_composer_+_ppt_designer.md) (7 shared connections)
- [ppt_designer](ppt_designer.md) (6 shared connections)
- [ppt_template](ppt_template.md) (2 shared connections)
- [ppt_tool](ppt_tool.md) (2 shared connections)
- [ppt_router + ppt_tool](ppt_router_+_ppt_tool.md) (2 shared connections)
- [ppt + KNOWN_ISSUES](ppt_+_KNOWN_ISSUES.md) (2 shared connections)

## Source Files

- `app/services/ppt_content.py`
- `app/services/ppt_designer.py`
- `app/services/ppt_studio.py`
- `docs/KNOWN_ISSUES.md`
- `docs/features/ppt.md`

## Audit Trail

- EXTRACTED: 85 (71%)
- INFERRED: 34 (29%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*