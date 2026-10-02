# assignment + assignment_answers

> 20 nodes · cohesion 0.12

## Key Concepts

- **do_assignment()** (10 connections) — `app/services/assignment_pipeline.py`
- **_resolve_pdf_path()** (8 connections) — `app/services/assignment_tool.py`
- **Assignment solver (5 phases)** (7 connections) — `docs/features/assignment.md`
- **generate_answers()** (6 connections) — `app/services/assignment_answers.py`
- **generate_answer()** (5 connections) — `app/services/assignment_answers.py`
- **list_assignments()** (5 connections) — `app/services/assignment_tool.py`
- **Phases** (5 connections) — `docs/features/assignment.md`
- **Triggers** (5 connections) — `docs/features/assignment.md`
- **_groq_answer()** (4 connections) — `app/services/assignment_answers.py`
- **Generate an answer using Groq LLM with automatic model fallback chain. Tries…** (1 connections) — `app/services/assignment_answers.py`
- **Generate complete answers for ALL questions from an assignment. Tries these…** (1 connections) — `app/services/assignment_answers.py`
- **Generate an answer for a SINGLE question using Groq LLM directly (fast, no…** (1 connections) — `app/services/assignment_answers.py`
- **Master orchestrator. Uses a background thread for all Playwright code. Yields…** (1 connections) — `app/services/assignment_pipeline.py`
- **Resolve PDF path: handles full paths, filenames, partial names.** (1 connections) — `app/services/assignment_tool.py`
- **Scan Desktop, Documents, and Downloads for PDF files.** (1 connections) — `app/services/assignment_tool.py`
- **assignment.md** (1 connections) — `docs/features/assignment.md`
- **Files & symbols (auto-generated, line numbers are current)** (1 connections) — `docs/features/assignment.md`
- **Gotchas** (1 connections) — `docs/features/assignment.md`
- **Graphify** (1 connections) — `docs/features/assignment.md`
- **Purpose** (1 connections) — `docs/features/assignment.md`

## Relationships

- [assignment_answers](assignment_answers.md) (5 shared connections)
- [tools](tools.md) (4 shared connections)
- [assignment_tool](assignment_tool.md) (4 shared connections)
- [assignment_pipeline](assignment_pipeline.md) (3 shared connections)
- [social_content_manager + ui_inspector](social_content_manager_+_ui_inspector.md) (2 shared connections)
- [assignment_assembler](assignment_assembler.md) (1 shared connections)
- [email-calendar + tools](email-calendar_+_tools.md) (1 shared connections)
- [agentic_web](agentic_web.md) (1 shared connections)
- [assignment_humanizer](assignment_humanizer.md) (1 shared connections)

## Source Files

- `app/services/assignment_answers.py`
- `app/services/assignment_pipeline.py`
- `app/services/assignment_tool.py`
- `docs/features/assignment.md`

## Audit Trail

- EXTRACTED: 29 (66%)
- INFERRED: 15 (34%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*