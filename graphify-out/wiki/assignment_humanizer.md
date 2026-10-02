# assignment_humanizer

> 27 nodes · cohesion 0.12

## Key Concepts

- **assignment_humanizer.py** (20 connections) — `app/services/assignment_humanizer.py`
- **_humanize_via_browser()** (8 connections) — `app/services/assignment_humanizer.py`
- **humanize_text()** (7 connections) — `app/services/assignment_humanizer.py`
- **_humanize_via_llm()** (7 connections) — `app/services/assignment_humanizer.py`
- **_humanize_chunk_via_browser()** (6 connections) — `app/services/assignment_humanizer.py`
- **humanize_all_answers()** (5 connections) — `app/services/assignment_humanizer.py`
- **_protect_technical()** (5 connections) — `app/services/assignment_humanizer.py`
- **_restore_technical()** (4 connections) — `app/services/assignment_humanizer.py`
- **_split_into_chunks()** (4 connections) — `app/services/assignment_humanizer.py`
- **_extract_output_text()** (3 connections) — `app/services/assignment_humanizer.py`
- **_fill_input()** (3 connections) — `app/services/assignment_humanizer.py`
- **_find_element()** (3 connections) — `app/services/assignment_humanizer.py`
- **_get_browser_page()** (3 connections) — `app/services/assignment_humanizer.py`
- **make_placeholder()** (1 connections) — `app/services/assignment_humanizer.py`
- **Jarvis Assignment Tool — Phase 3: Answer Humanizer…** (1 connections) — `app/services/assignment_humanizer.py`
- **Replace technical content with numbered placeholders. Returns (modified_text,…** (1 connections) — `app/services/assignment_humanizer.py`
- **Restore original technical content from placeholders.** (1 connections) — `app/services/assignment_humanizer.py`
- **Split text into chunks at sentence boundaries, each ≤ max_chars. Ensures no…** (1 connections) — `app/services/assignment_humanizer.py`
- **Get a persistent browser page (non-headless, saves session).** (1 connections) — `app/services/assignment_humanizer.py`
- **Try multiple CSS selectors to find a visible element.** (1 connections) — `app/services/assignment_humanizer.py`
- **Fill an input area with text using the most reliable method available.** (1 connections) — `app/services/assignment_humanizer.py`
- **Extract text from the output area of the humanizer.** (1 connections) — `app/services/assignment_humanizer.py`
- **Humanize a single text chunk on an already-open browser page. Returns humanized…** (1 connections) — `app/services/assignment_humanizer.py`
- **Open a humanizer site in browser, process text in chunks, return humanized…** (1 connections) — `app/services/assignment_humanizer.py`
- **Humanize text using Groq LLM with 'write like a student' prompt. Model fallback…** (1 connections) — `app/services/assignment_humanizer.py`
- *... and 2 more nodes in this community*

## Relationships

- [dag_executor + planner](dag_executor_+_planner.md) (2 shared connections)
- [tools](tools.md) (2 shared connections)
- [ssml_processor + debug_wa](ssml_processor_+_debug_wa.md) (1 shared connections)
- [task_ledger + test_task_resumption](task_ledger_+_test_task_resumption.md) (1 shared connections)
- [whatsapp + dump_wa_ui](whatsapp_+_dump_wa_ui.md) (1 shared connections)
- [screen_reader](screen_reader.md) (1 shared connections)
- [assignment_tool](assignment_tool.md) (1 shared connections)
- [assignment_tool + assignment_pipeline](assignment_tool_+_assignment_pipeline.md) (1 shared connections)

## Source Files

- `app/services/assignment_humanizer.py`

## Audit Trail

- EXTRACTED: 48 (94%)
- INFERRED: 3 (6%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*