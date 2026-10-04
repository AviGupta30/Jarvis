# assignment_tool

> 4 nodes · cohesion 0.50

## Key Concepts

- **_extract_via_llm_text()** (5 connections) — `app/services/assignment_tool.py`
- **_pdf_pages_to_text()** (4 connections) — `app/services/assignment_tool.py`
- **Extract text from each PDF page separately. Returns list of page strings.** (1 connections) — `app/services/assignment_tool.py`
- **LLM-based text extraction as fallback for when regex fails.** (1 connections) — `app/services/assignment_tool.py`

## Relationships

- [assignment_tool](assignment_tool.md) (3 shared connections)
- [assignment_tool + assignment_pipeline](assignment_tool_+_assignment_pipeline.md) (2 shared connections)

## Source Files

- `app/services/assignment_tool.py`

## Audit Trail

- EXTRACTED: 8 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*