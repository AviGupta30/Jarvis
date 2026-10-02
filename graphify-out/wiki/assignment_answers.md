# assignment_answers

> 18 nodes · cohesion 0.13

## Key Concepts

- **_run_browser_session()** (9 connections) — `app/services/assignment_answers.py`
- **_ask_question_on_page()** (8 connections) — `app/services/assignment_answers.py`
- **_find_input()** (4 connections) — `app/services/assignment_answers.py`
- **_send_message()** (4 connections) — `app/services/assignment_answers.py`
- **_wait_for_generation()** (4 connections) — `app/services/assignment_answers.py`
- **_get_persistent_page()** (3 connections) — `app/services/assignment_answers.py`
- **_screenshot_extract()** (3 connections) — `app/services/assignment_answers.py`
- **_try_copy_button()** (3 connections) — `app/services/assignment_answers.py`
- **_upload_pdf()** (3 connections) — `app/services/assignment_answers.py`
- **Launch a visible (non-headless) Chromium with a persistent profile. Login…** (1 connections) — `app/services/assignment_answers.py`
- **Try CSS selectors to find the visible chat input. Returns locator or None.** (1 connections) — `app/services/assignment_answers.py`
- **Type a message into the AI chat input and submit it.** (1 connections) — `app/services/assignment_answers.py`
- **Upload PDF to the AI chat page. Returns True if upload was initiated.** (1 connections) — `app/services/assignment_answers.py`
- **Wait until the AI stops generating its response.** (1 connections) — `app/services/assignment_answers.py`
- **Click the copy button on the last AI response and return clipboard text.** (1 connections) — `app/services/assignment_answers.py`
- **Take a page screenshot and use Groq Vision to extract the AI's answer.** (1 connections) — `app/services/assignment_answers.py`
- **Send one question to the open AI page and return the answer text.** (1 connections) — `app/services/assignment_answers.py`
- **Full browser session: open site → upload PDF → ask all questions → close.…** (1 connections) — `app/services/assignment_answers.py`

## Relationships

- [assignment_tool + safe_executor](assignment_tool_+_safe_executor.md) (9 shared connections)
- [assignment_pipeline + assignment_tool](assignment_pipeline_+_assignment_tool.md) (1 shared connections)

## Source Files

- `app/services/assignment_answers.py`

## Audit Trail

- EXTRACTED: 30 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*