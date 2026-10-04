# ppt_content

> 15 nodes · cohesion 0.18

## Key Concepts

- **generate_deck()** (18 connections) — `app/services/ppt_content.py`
- **_flatten()** (8 connections) — `app/services/ppt_content.py`
- **_s()** (7 connections) — `app/services/ppt_content.py`
- **interpret_image_instructions()** (6 connections) — `app/services/ppt_content.py`
- **take()** (5 connections) — `app/services/ppt_content.py`
- **slide_has_content()** (5 connections) — `app/services/ppt_content.py`
- **_content_prompt()** (4 connections) — `app/services/ppt_content.py`
- **run()** (3 connections) — `app/services/ppt_content.py`
- **_outline_prompt()** (3 connections) — `app/services/ppt_content.py`
- **_schema_for()** (3 connections) — `app/services/ppt_content.py`
- **_is_note()** (2 connections) — `app/services/ppt_content.py`
- **Only the schema lines for the kinds in this chunk (saves ~400 tokens per call…** (1 connections) — `app/services/ppt_content.py`
- **LLM outline + content, grounded in `facts` and fact-checked afterwards. `fixed`…** (1 connections) — `app/services/ppt_content.py`
- **LLMs love nesting: {"cards": {"bullets": […]}}, {"subtitle": {"subtitle": "…"}}…** (1 connections) — `app/services/ppt_content.py`
- **LLM fallback for phrasings the regexes can't resolve. Returns image_rules (same…** (1 connections) — `app/services/ppt_content.py`

## Relationships

- [ppt_content](ppt_content.md) (21 shared connections)
- [ppt_research](ppt_research.md) (5 shared connections)
- [ppt_studio + ppt_designer](ppt_studio_+_ppt_designer.md) (3 shared connections)
- [ppt + KNOWN_ISSUES](ppt_+_KNOWN_ISSUES.md) (1 shared connections)

## Source Files

- `app/services/ppt_content.py`

## Audit Trail

- EXTRACTED: 44 (90%)
- INFERRED: 5 (10%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*