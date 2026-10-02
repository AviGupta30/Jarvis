# ppt_content

> 33 nodes · cohesion 0.10

## Key Concepts

- **Flow — create (`ppt_tool.ppt_create` → `ppt_studio.create`, a generator)** (27 connections) — `docs/features/ppt.md`
- **ppt_create()** (15 connections) — `app/services/ppt_tool.py`
- **architect_slides()** (13 connections) — `app/services/ppt_content.py`
- **_complete_from_source()** (9 connections) — `app/services/ppt_content.py`
- **_missing_parts()** (8 connections) — `app/services/ppt_content.py`
- **Fixed on 2026-10-01 (PPT)** (8 connections) — `docs/KNOWN_ISSUES.md`
- **extractive_ok()** (7 connections) — `app/services/ppt_content.py`
- **repair_text()** (6 connections) — `app/services/ppt_content.py`
- **split_instructions()** (6 connections) — `app/services/ppt_content.py`
- **_is_instruction()** (5 connections) — `app/services/ppt_content.py`
- **sections_fallback()** (5 connections) — `app/services/ppt_content.py`
- **_tok()** (5 connections) — `app/services/ppt_content.py`
- **ask()** (4 connections) — `app/services/ppt_content.py`
- **_retry()** (4 connections) — `app/services/ppt_content.py`
- **deck_facts()** (4 connections) — `app/services/ppt_content.py`
- **needs_architect()** (4 connections) — `app/services/ppt_content.py`
- **plain_md()** (4 connections) — `app/services/ppt_content.py`
- **run()** (3 connections) — `app/services/ppt_content.py`
- **detect_profile()** (3 connections) — `app/services/ppt_content.py`
- **_spec_texts()** (3 connections) — `app/services/ppt_content.py`
- **_copy_sec()** (1 connections) — `app/services/ppt_content.py`
- **True if the slide only re-uses the user's words (≥ min_ratio of tokens) and…** (1 connections) — `app/services/ppt_content.py`
- **Deterministic structure: 'Label:' lines start sections, 'Head: text' lines…** (1 connections) — `app/services/ppt_content.py`
- **Names worth knowing on every slide (product, team, event) — pulled verbatim…** (1 connections) — `app/services/ppt_content.py`
- **Labelled parts of the user's content ('Skill Gaps: …', 'Before vs. After …:')…** (1 connections) — `app/services/ppt_content.py`
- *... and 8 more nodes in this community*

## Relationships

- [ppt_content](ppt_content.md) (25 shared connections)
- [ppt_studio](ppt_studio.md) (9 shared connections)
- [chat + KNOWN_ISSUES](chat_+_KNOWN_ISSUES.md) (3 shared connections)
- [ppt_tool](ppt_tool.md) (3 shared connections)
- [ppt_router](ppt_router.md) (2 shared connections)
- [tools](tools.md) (2 shared connections)
- [ppt_composer + ppt_designer](ppt_composer_+_ppt_designer.md) (2 shared connections)
- [research_scraper + nlp_extractor](research_scraper_+_nlp_extractor.md) (1 shared connections)
- [chat-routing + chat](chat-routing_+_chat.md) (1 shared connections)
- [ppt_research](ppt_research.md) (1 shared connections)
- [tool-registry + memory](tool-registry_+_memory.md) (1 shared connections)
- [tools + whatsapp_smart](tools_+_whatsapp_smart.md) (1 shared connections)

## Source Files

- `app/services/ppt_content.py`
- `app/services/ppt_tool.py`
- `docs/KNOWN_ISSUES.md`
- `docs/features/ppt.md`

## Audit Trail

- EXTRACTED: 62 (59%)
- INFERRED: 43 (41%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*