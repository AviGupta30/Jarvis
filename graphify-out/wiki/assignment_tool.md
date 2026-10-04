# assignment_tool

> 8 nodes · cohesion 0.29

## Key Concepts

- **extract_questions()** (12 connections) — `app/services/assignment_tool.py`
- **_resolve_pdf_path()** (8 connections) — `app/services/assignment_tool.py`
- **_extract_via_llm_text()** (5 connections) — `app/services/assignment_tool.py`
- **_pdf_pages_to_text()** (4 connections) — `app/services/assignment_tool.py`
- **Extract text from each PDF page separately. Returns list of page strings.** (1 connections) — `app/services/assignment_tool.py`
- **LLM-based text extraction as fallback for when regex fails.** (1 connections) — `app/services/assignment_tool.py`
- **Extract ALL questions from an assignment PDF using a 3-track hybrid system.…** (1 connections) — `app/services/assignment_tool.py`
- **Resolve PDF path: handles full paths, filenames, partial names.** (1 connections) — `app/services/assignment_tool.py`

## Relationships

- [assignment_tool](assignment_tool.md) (7 shared connections)
- [assignment_pipeline](assignment_pipeline.md) (4 shared connections)
- [assignment_humanizer](assignment_humanizer.md) (2 shared connections)
- [assignment_answers](assignment_answers.md) (2 shared connections)
- [assignment](assignment.md) (1 shared connections)
- [tools](tools.md) (1 shared connections)

## Source Files

- `app/services/assignment_tool.py`

## Audit Trail

- EXTRACTED: 22 (88%)
- INFERRED: 3 (12%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*