# assignment_humanizer

> 22 nodes · cohesion 0.11

## Key Concepts

- **_humanize_via_browser()** (8 connections) — `app/services/assignment_humanizer.py`
- **humanize_text()** (7 connections) — `app/services/assignment_humanizer.py`
- **_humanize_via_llm()** (7 connections) — `app/services/assignment_humanizer.py`
- **_merge_and_deduplicate()** (6 connections) — `app/services/assignment_tool.py`
- **humanize_all_answers()** (5 connections) — `app/services/assignment_humanizer.py`
- **_protect_technical()** (5 connections) — `app/services/assignment_humanizer.py`
- **Phases** (5 connections) — `docs/features/assignment.md`
- **_restore_technical()** (4 connections) — `app/services/assignment_humanizer.py`
- **_split_into_chunks()** (4 connections) — `app/services/assignment_humanizer.py`
- **_get_browser_page()** (3 connections) — `app/services/assignment_humanizer.py`
- **make_placeholder()** (1 connections) — `app/services/assignment_humanizer.py`
- **Replace technical content with numbered placeholders. Returns (modified_text,…** (1 connections) — `app/services/assignment_humanizer.py`
- **Restore original technical content from placeholders.** (1 connections) — `app/services/assignment_humanizer.py`
- **Split text into chunks at sentence boundaries, each ≤ max_chars. Ensures no…** (1 connections) — `app/services/assignment_humanizer.py`
- **Get a persistent browser page (non-headless, saves session).** (1 connections) — `app/services/assignment_humanizer.py`
- **Open a humanizer site in browser, process text in chunks, return humanized…** (1 connections) — `app/services/assignment_humanizer.py`
- **Humanize text using Groq LLM with 'write like a student' prompt. Model fallback…** (1 connections) — `app/services/assignment_humanizer.py`
- **Humanize a single block of AI-generated text to sound like a student wrote it.…** (1 connections) — `app/services/assignment_humanizer.py`
- **Humanize ALL answers in a QA_JSON block from Phase 2 (generate_answers). Each…** (1 connections) — `app/services/assignment_humanizer.py`
- **is_duplicate()** (1 connections) — `app/services/assignment_tool.py`
- **sort_key()** (1 connections) — `app/services/assignment_tool.py`
- **Merge questions from all three tracks. Priority: regex > vision > llm text. A…** (1 connections) — `app/services/assignment_tool.py`

## Relationships

- [repair + assignment_humanizer](repair_+_assignment_humanizer.md) (9 shared connections)
- [assignment_tool](assignment_tool.md) (3 shared connections)
- [tools](tools.md) (2 shared connections)
- [assignment](assignment.md) (2 shared connections)

## Source Files

- `app/services/assignment_humanizer.py`
- `app/services/assignment_tool.py`
- `docs/features/assignment.md`

## Audit Trail

- EXTRACTED: 34 (83%)
- INFERRED: 7 (17%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*