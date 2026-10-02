# resume_detector

> 15 nodes · cohesion 0.18

## Key Concepts

- **resume_detector.py** (11 connections) — `app/services/resume_detector.py`
- **detect_resume_intent()** (11 connections) — `app/services/resume_detector.py`
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
- **# NOTE: 'send another message' is deliberately EXCLUDED — it is a resume (send…** (1 connections) — `app/services/resume_detector.py`

## Relationships

- [chat + llm](chat_+_llm.md) (3 shared connections)
- [task_ledger + test_task_resumption](task_ledger_+_test_task_resumption.md) (2 shared connections)
- [smart_navigator + rag_memory](smart_navigator_+_rag_memory.md) (1 shared connections)
- [chat-routing + chat](chat-routing_+_chat.md) (1 shared connections)

## Source Files

- `app/services/resume_detector.py`

## Audit Trail

- EXTRACTED: 25 (96%)
- INFERRED: 1 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*