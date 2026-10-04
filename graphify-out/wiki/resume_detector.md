# resume_detector

> 17 nodes · cohesion 0.15

## Key Concepts

- **detect_resume_intent()** (12 connections) — `app/services/resume_detector.py`
- **resume_detector.py** (11 connections) — `app/services/resume_detector.py`
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

- [task_ledger + test_task_resumption](task_ledger_+_test_task_resumption.md) (3 shared connections)
- [chat + llm](chat_+_llm.md) (2 shared connections)
- [planner + dynamic_skill](planner_+_dynamic_skill.md) (2 shared connections)
- [assignment_assembler + smart_navigator](assignment_assembler_+_smart_navigator.md) (1 shared connections)
- [dag_executor](dag_executor.md) (1 shared connections)
- [resume_builder](resume_builder.md) (1 shared connections)

## Source Files

- `app/services/resume_detector.py`

## Audit Trail

- EXTRACTED: 29 (94%)
- INFERRED: 2 (6%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*