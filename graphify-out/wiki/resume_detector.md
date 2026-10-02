# resume_detector

> 17 nodes · cohesion 0.15

## Key Concepts

- **resume_detector.py** (11 connections) — `app/services/resume_detector.py`
- **detect_resume_intent()** (11 connections) — `app/services/resume_detector.py`
- **get_resume_context_string()** (5 connections) — `app/services/resume_detector.py`
- **_extract_task_resource()** (3 connections) — `app/services/resume_detector.py`
- **_find_best_task_match()** (3 connections) — `app/services/resume_detector.py`
- **_has_continuation_verb()** (3 connections) — `app/services/resume_detector.py`
- **_has_fresh_task_indicator()** (3 connections) — `app/services/resume_detector.py`
- **_has_reference_phrase()** (3 connections) — `app/services/resume_detector.py`
- **resume_detector.py — Jarvis Resume Intent Classifier…** (1 connections) — `app/services/resume_detector.py`
- **Return True if the text contains a strong resume-intent reference phrase.** (1 connections) — `app/services/resume_detector.py`
- **Return True if the text clearly indicates a FRESH (new) task, not a…** (1 connections) — `app/services/resume_detector.py`
- **Return True if the text contains an action verb suggesting continuation.** (1 connections) — `app/services/resume_detector.py`
- **Extract the most human-readable resource identifier from a ledger entry. E.g.,…** (1 connections) — `app/services/resume_detector.py`
- **Given the user's text and a list of recent ledger entries, find the best…** (1 connections) — `app/services/resume_detector.py`
- **Determine whether the user's message is a continuation of a prior task. This is…** (1 connections) — `app/services/resume_detector.py`
- **Convert a resume detection result into a human-readable context string that can…** (1 connections) — `app/services/resume_detector.py`
- **# NOTE: 'send another message' is deliberately EXCLUDED — it is a resume (send…** (1 connections) — `app/services/resume_detector.py`

## Relationships

- [chat + rag_memory](chat_+_rag_memory.md) (4 shared connections)
- [task_ledger + test_task_resumption](task_ledger_+_test_task_resumption.md) (3 shared connections)
- [assignment_tool + assignment_humanizer](assignment_tool_+_assignment_humanizer.md) (1 shared connections)
- [chat-routing + CLAUDE](chat-routing_+_CLAUDE.md) (1 shared connections)

## Source Files

- `app/services/resume_detector.py`

## Audit Trail

- EXTRACTED: 29 (97%)
- INFERRED: 1 (3%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*