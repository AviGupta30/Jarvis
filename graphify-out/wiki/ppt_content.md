# ppt_content

> 31 nodes · cohesion 0.10

## Key Concepts

- **generate_deck()** (18 connections) — `app/services/ppt_content.py`
- **ground_slides()** (16 connections) — `app/services/ppt_content.py`
- **_llm_json()** (15 connections) — `app/services/ppt_content.py`
- **normalize_slide()** (10 connections) — `app/services/ppt_content.py`
- **_flatten()** (8 connections) — `app/services/ppt_content.py`
- **_llm_edit()** (8 connections) — `app/services/ppt_content.py`
- **_s()** (7 connections) — `app/services/ppt_content.py`
- **interpret_image_instructions()** (6 connections) — `app/services/ppt_content.py`
- **take()** (5 connections) — `app/services/ppt_content.py`
- **slide_has_content()** (5 connections) — `app/services/ppt_content.py`
- **strip_fact_ids()** (5 connections) — `app/services/ppt_research.py`
- **_content_prompt()** (4 connections) — `app/services/ppt_content.py`
- **_compact()** (3 connections) — `app/services/ppt_content.py`
- **_gemini_json()** (3 connections) — `app/services/ppt_content.py`
- **run()** (3 connections) — `app/services/ppt_content.py`
- **repair()** (3 connections) — `app/services/ppt_content.py`
- **_outline_prompt()** (3 connections) — `app/services/ppt_content.py`
- **_reserve()** (3 connections) — `app/services/ppt_content.py`
- **_schema_for()** (3 connections) — `app/services/ppt_content.py`
- **_budget_left()** (2 connections) — `app/services/ppt_content.py`
- **_is_note()** (2 connections) — `app/services/ppt_content.py`
- **_groq()** (2 connections) — `app/services/ppt_content.py`
- **JSON completion with pacing + fallback. fast=True → 20b first (copy/extraction…** (1 connections) — `app/services/ppt_content.py`
- **Only the schema lines for the kinds in this chunk (saves ~400 tokens per call…** (1 connections) — `app/services/ppt_content.py`
- **Audit every generated slide; LLM-repair flagged ones with their facts; scrub…** (1 connections) — `app/services/ppt_content.py`
- *... and 6 more nodes in this community*

## Relationships

- [ppt_content](ppt_content.md) (32 shared connections)
- [ppt_research](ppt_research.md) (11 shared connections)
- [ppt_studio + ppt_content](ppt_studio_+_ppt_content.md) (5 shared connections)
- [ppt_content + KNOWN_ISSUES](ppt_content_+_KNOWN_ISSUES.md) (1 shared connections)

## Source Files

- `app/services/ppt_content.py`
- `app/services/ppt_research.py`

## Audit Trail

- EXTRACTED: 86 (90%)
- INFERRED: 10 (10%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*