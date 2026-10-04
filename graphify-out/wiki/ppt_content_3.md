# ppt_content

> 24 nodes · cohesion 0.11

## Key Concepts

- **generate_deck()** (18 connections) — `app/services/ppt_content.py`
- **_llm_json()** (15 connections) — `app/services/ppt_content.py`
- **_flatten()** (8 connections) — `app/services/ppt_content.py`
- **_s()** (7 connections) — `app/services/ppt_content.py`
- **interpret_image_instructions()** (6 connections) — `app/services/ppt_content.py`
- **take()** (5 connections) — `app/services/ppt_content.py`
- **slide_has_content()** (5 connections) — `app/services/ppt_content.py`
- **_content_prompt()** (4 connections) — `app/services/ppt_content.py`
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
- **LLM outline + content, grounded in `facts` and fact-checked afterwards. `fixed`…** (1 connections) — `app/services/ppt_content.py`
- **LLMs love nesting: {"cards": {"bullets": […]}}, {"subtitle": {"subtitle": "…"}}…** (1 connections) — `app/services/ppt_content.py`
- **Client-side pacing: wait until this call fits in the model's per-minute budget…** (1 connections) — `app/services/ppt_content.py`
- **LLM fallback for phrasings the regexes can't resolve. Returns image_rules (same…** (1 connections) — `app/services/ppt_content.py`
- **Backup provider when Groq's daily token cap is reached (same JSON contract).** (1 connections) — `app/services/ppt_content.py`

## Relationships

- [ppt_content](ppt_content.md) (27 shared connections)
- [ppt_research](ppt_research.md) (7 shared connections)
- [ppt_studio + ppt_designer](ppt_studio_+_ppt_designer.md) (5 shared connections)

## Source Files

- `app/services/ppt_content.py`

## Audit Trail

- EXTRACTED: 62 (90%)
- INFERRED: 7 (10%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*