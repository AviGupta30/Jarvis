# resume_builder

> 6 nodes · cohesion 0.47

## Key Concepts

- **_llm_json()** (7 connections) — `app/services/resume_builder.py`
- **_vision()** (5 connections) — `app/services/resume_builder.py`
- **_gemini()** (4 connections) — `app/services/resume_builder.py`
- **_groq()** (3 connections) — `app/services/resume_builder.py`
- **_parse_json()** (3 connections) — `app/services/resume_builder.py`
- **Fallback when Groq is rate-limited (its vision model has a 200k tokens/DAY cap).** (1 connections) — `app/services/resume_builder.py`

## Relationships

- [resume_builder](resume_builder.md) (9 shared connections)

## Source Files

- `app/services/resume_builder.py`

## Audit Trail

- EXTRACTED: 15 (94%)
- INFERRED: 1 (6%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*