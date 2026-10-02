# assignment_pipeline + assignment_tool

> 56 nodes · cohesion 0.05

## Key Concepts

- **assignment_pipeline.py** (22 connections) — `app/services/assignment_pipeline.py`
- **_browser_thread()** (13 connections) — `app/services/assignment_pipeline.py`
- **extract_questions()** (12 connections) — `app/services/assignment_tool.py`
- **do_assignment()** (10 connections) — `app/services/assignment_pipeline.py`
- **assignment_assembler.py** (9 connections) — `app/services/assignment_assembler.py`
- **assemble_assignment()** (8 connections) — `app/services/assignment_assembler.py`
- **_resolve_pdf_path()** (8 connections) — `app/services/assignment_tool.py`
- **Assignment solver (5 phases)** (7 connections) — `docs/features/assignment.md`
- **generate_answers()** (6 connections) — `app/services/assignment_answers.py`
- **_merge_and_deduplicate()** (6 connections) — `app/services/assignment_tool.py`
- **generate_answer()** (5 connections) — `app/services/assignment_answers.py`
- **_extract_via_llm_text()** (5 connections) — `app/services/assignment_tool.py`
- **list_assignments()** (5 connections) — `app/services/assignment_tool.py`
- **Phases** (5 connections) — `docs/features/assignment.md`
- **Triggers** (5 connections) — `docs/features/assignment.md`
- **_groq_answer()** (4 connections) — `app/services/assignment_answers.py`
- **_find_el()** (4 connections) — `app/services/assignment_pipeline.py`
- **_get_browser_ctx()** (4 connections) — `app/services/assignment_pipeline.py`
- **_humanize_browser()** (4 connections) — `app/services/assignment_pipeline.py`
- **_pdf_pages_to_text()** (4 connections) — `app/services/assignment_tool.py`
- **_parse_qa_json()** (3 connections) — `app/services/assignment_assembler.py`
- **_get_answer()** (3 connections) — `app/services/assignment_pipeline.py`
- **_groq_answer()** (3 connections) — `app/services/assignment_pipeline.py`
- **_groq_humanize()** (3 connections) — `app/services/assignment_pipeline.py`
- **Queue** (3 connections)
- *... and 31 more nodes in this community*

## Relationships

- [smart_navigator + rag_memory](smart_navigator_+_rag_memory.md) (19 shared connections)
- [tools + whatsapp_smart](tools_+_whatsapp_smart.md) (6 shared connections)
- [assignment_tool](assignment_tool.md) (3 shared connections)
- [assignment_answers](assignment_answers.md) (1 shared connections)
- [server + test_concurrency](server_+_test_concurrency.md) (1 shared connections)
- [tool-registry + memory](tool-registry_+_memory.md) (1 shared connections)
- [chat + KNOWN_ISSUES](chat_+_KNOWN_ISSUES.md) (1 shared connections)
- [assignment_humanizer](assignment_humanizer.md) (1 shared connections)

## Source Files

- `app/services/assignment_answers.py`
- `app/services/assignment_assembler.py`
- `app/services/assignment_pipeline.py`
- `app/services/assignment_tool.py`
- `docs/features/assignment.md`

## Audit Trail

- EXTRACTED: 98 (84%)
- INFERRED: 18 (16%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*