# assignment_humanizer

> 25 nodes · cohesion 0.09

## Key Concepts

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
- **Humanize a single block of AI-generated text to sound like a student wrote it.…** (1 connections) — `app/services/assignment_humanizer.py`
- **Humanize ALL answers in a QA_JSON block from Phase 2 (generate_answers). Each…** (1 connections) — `app/services/assignment_humanizer.py`

## Relationships

- [assignment_tool + safe_executor](assignment_tool_+_safe_executor.md) (12 shared connections)
- [tools](tools.md) (2 shared connections)
- [assignment_pipeline + assignment_tool](assignment_pipeline_+_assignment_tool.md) (1 shared connections)

## Source Files

- `app/services/assignment_humanizer.py`

## Audit Trail

- EXTRACTED: 40 (93%)
- INFERRED: 3 (7%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*