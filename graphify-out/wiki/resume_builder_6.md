# resume_builder

> 16 nodes · cohesion 0.17

## Key Concepts

- **_build_content()** (9 connections) — `app/services/resume_builder.py`
- **_drop_invented()** (8 connections) — `app/services/resume_builder.py`
- **_llm_json()** (6 connections) — `app/services/resume_builder.py`
- **_edit_content()** (5 connections) — `app/services/resume_builder.py`
- **_normalise_content()** (5 connections) — `app/services/resume_builder.py`
- **_vision()** (5 connections) — `app/services/resume_builder.py`
- **_gemini()** (4 connections) — `app/services/resume_builder.py`
- **ok()** (3 connections) — `app/services/resume_builder.py`
- **_groq()** (3 connections) — `app/services/resume_builder.py`
- **_nums()** (3 connections) — `app/services/resume_builder.py`
- **_parse_json()** (3 connections) — `app/services/resume_builder.py`
- **_content_brief()** (2 connections) — `app/services/resume_builder.py`
- **clean_text()** (2 connections) — `app/services/resume_builder.py`
- **_str_list()** (2 connections) — `app/services/resume_builder.py`
- **Fallback when Groq is rate-limited (its vision model has a 200k tokens/DAY cap).** (1 connections) — `app/services/resume_builder.py`
- **The LLM likes to 'improve' bullets with made-up metrics. Drop any…** (1 connections) — `app/services/resume_builder.py`

## Relationships

- [resume_builder](resume_builder.md) (20 shared connections)

## Source Files

- `app/services/resume_builder.py`

## Audit Trail

- EXTRACTED: 37 (90%)
- INFERRED: 4 (10%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*