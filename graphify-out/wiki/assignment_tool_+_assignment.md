# assignment_tool + assignment

> 20 nodes · cohesion 0.13

## Key Concepts

- **extract_questions()** (12 connections) — `app/services/assignment_tool.py`
- **do_assignment()** (10 connections) — `app/services/assignment_pipeline.py`
- **_resolve_pdf_path()** (8 connections) — `app/services/assignment_tool.py`
- **Assignment solver (5 phases)** (7 connections) — `docs/features/assignment.md`
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
- **assignment.md** (1 connections) — `docs/features/assignment.md`
- **Files & symbols (auto-generated, line numbers are current)** (1 connections) — `docs/features/assignment.md`
- **Gotchas** (1 connections) — `docs/features/assignment.md`
- **Graphify** (1 connections) — `docs/features/assignment.md`
- **Purpose** (1 connections) — `docs/features/assignment.md`

## Relationships

- [assignment_tool](assignment_tool.md) (8 shared connections)
- [assignment_pipeline](assignment_pipeline.md) (4 shared connections)
- [tools + window_layout](tools_+_window_layout.md) (3 shared connections)
- [assignment_answers](assignment_answers.md) (3 shared connections)
- [assignment_assembler + smart_navigator](assignment_assembler_+_smart_navigator.md) (1 shared connections)
- [tool-registry + tools](tool-registry_+_tools.md) (1 shared connections)
- [file_ops](file_ops.md) (1 shared connections)
- [assignment_humanizer](assignment_humanizer.md) (1 shared connections)

## Source Files

- `app/services/assignment_pipeline.py`
- `app/services/assignment_tool.py`
- `docs/features/assignment.md`

## Audit Trail

- EXTRACTED: 31 (67%)
- INFERRED: 15 (33%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*