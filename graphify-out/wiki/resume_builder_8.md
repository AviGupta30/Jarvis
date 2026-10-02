# resume_builder

> 15 nodes · cohesion 0.21

## Key Concepts

- **resume_builder.py** (89 connections) — `app/services/resume_builder.py`
- **_llm_json()** (6 connections) — `app/services/resume_builder.py`
- **resume_tool()** (5 connections) — `app/services/resume_builder.py`
- **_vision()** (5 connections) — `app/services/resume_builder.py`
- **_gemini()** (4 connections) — `app/services/resume_builder.py`
- **list_resume_templates()** (4 connections) — `app/services/resume_builder.py`
- **_sec()** (4 connections) — `app/services/resume_builder.py`
- **_groq()** (3 connections) — `app/services/resume_builder.py`
- **_parse_json()** (3 connections) — `app/services/resume_builder.py`
- **_title()** (2 connections) — `app/services/resume_builder.py`
- **resume_builder.py — Resume Creator Upload a picture of any resume → Jarvis…** (1 connections) — `app/services/resume_builder.py`
- **Registry entry: also handles a bare 'list templates' request.** (1 connections) — `app/services/resume_builder.py`
- **Fallback when Groq is rate-limited (its vision model has a 200k tokens/DAY cap).** (1 connections) — `app/services/resume_builder.py`
- **contextvars** (1 connections)
- **html** (1 connections)

## Relationships

- [resume_builder](resume_builder.md) (77 shared connections)
- [assignment_tool + assignment_humanizer](assignment_tool_+_assignment_humanizer.md) (5 shared connections)
- [chat + rag_memory](chat_+_rag_memory.md) (2 shared connections)
- [persistence + server](persistence_+_server.md) (1 shared connections)
- [resume-creator](resume-creator.md) (1 shared connections)

## Source Files

- `app/services/resume_builder.py`

## Audit Trail

- EXTRACTED: 107 (99%)
- INFERRED: 1 (1%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*