# assignment_tool + assignment_pipeline

> 14 nodes · cohesion 0.19

## Key Concepts

- **extract_questions()** (12 connections) — `app/services/assignment_tool.py`
- **do_assignment()** (10 connections) — `app/services/assignment_pipeline.py`
- **_resolve_pdf_path()** (8 connections) — `app/services/assignment_tool.py`
- **_merge_and_deduplicate()** (6 connections) — `app/services/assignment_tool.py`
- **list_assignments()** (5 connections) — `app/services/assignment_tool.py`
- **Phases** (5 connections) — `docs/features/assignment.md`
- **Triggers** (5 connections) — `docs/features/assignment.md`
- **Master orchestrator. Uses a background thread for all Playwright code. Yields…** (1 connections) — `app/services/assignment_pipeline.py`
- **is_duplicate()** (1 connections) — `app/services/assignment_tool.py`
- **sort_key()** (1 connections) — `app/services/assignment_tool.py`
- **Merge questions from all three tracks. Priority: regex > vision > llm text. A…** (1 connections) — `app/services/assignment_tool.py`
- **Extract ALL questions from an assignment PDF using a 3-track hybrid system.…** (1 connections) — `app/services/assignment_tool.py`
- **Resolve PDF path: handles full paths, filenames, partial names.** (1 connections) — `app/services/assignment_tool.py`
- **Scan Desktop, Documents, and Downloads for PDF files.** (1 connections) — `app/services/assignment_tool.py`

## Relationships

- [assignment_tool](assignment_tool.md) (8 shared connections)
- [assignment_pipeline](assignment_pipeline.md) (4 shared connections)
- [tools](tools.md) (3 shared connections)
- [assignment_answers](assignment_answers.md) (3 shared connections)
- [assignment](assignment.md) (2 shared connections)
- [assignment_assembler](assignment_assembler.md) (1 shared connections)
- [tool-registry](tool-registry.md) (1 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (1 shared connections)
- [assignment_humanizer](assignment_humanizer.md) (1 shared connections)

## Source Files

- `app/services/assignment_pipeline.py`
- `app/services/assignment_tool.py`
- `docs/features/assignment.md`

## Audit Trail

- EXTRACTED: 26 (63%)
- INFERRED: 15 (37%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*