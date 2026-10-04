# assignment_answers

> 26 nodes · cohesion 0.12

## Key Concepts

- **assignment_answers.py** (22 connections) — `app/services/assignment_answers.py`
- **_run_browser_session()** (9 connections) — `app/services/assignment_answers.py`
- **_ask_question_on_page()** (8 connections) — `app/services/assignment_answers.py`
- **generate_answers()** (6 connections) — `app/services/assignment_answers.py`
- **generate_answer()** (5 connections) — `app/services/assignment_answers.py`
- **_find_input()** (4 connections) — `app/services/assignment_answers.py`
- **_groq_answer()** (4 connections) — `app/services/assignment_answers.py`
- **_send_message()** (4 connections) — `app/services/assignment_answers.py`
- **_wait_for_generation()** (4 connections) — `app/services/assignment_answers.py`
- **_get_persistent_page()** (3 connections) — `app/services/assignment_answers.py`
- **_screenshot_extract()** (3 connections) — `app/services/assignment_answers.py`
- **_try_copy_button()** (3 connections) — `app/services/assignment_answers.py`
- **_upload_pdf()** (3 connections) — `app/services/assignment_answers.py`
- **Jarvis Assignment Tool — Phase 2: Answer Generation…** (1 connections) — `app/services/assignment_answers.py`
- **Launch a visible (non-headless) Chromium with a persistent profile. Login…** (1 connections) — `app/services/assignment_answers.py`
- **Try CSS selectors to find the visible chat input. Returns locator or None.** (1 connections) — `app/services/assignment_answers.py`
- **Type a message into the AI chat input and submit it.** (1 connections) — `app/services/assignment_answers.py`
- **Upload PDF to the AI chat page. Returns True if upload was initiated.** (1 connections) — `app/services/assignment_answers.py`
- **Wait until the AI stops generating its response.** (1 connections) — `app/services/assignment_answers.py`
- **Click the copy button on the last AI response and return clipboard text.** (1 connections) — `app/services/assignment_answers.py`
- **Take a page screenshot and use Groq Vision to extract the AI's answer.** (1 connections) — `app/services/assignment_answers.py`
- **Send one question to the open AI page and return the answer text.** (1 connections) — `app/services/assignment_answers.py`
- **Full browser session: open site → upload PDF → ask all questions → close.…** (1 connections) — `app/services/assignment_answers.py`
- **Generate an answer using Groq LLM with automatic model fallback chain. Tries…** (1 connections) — `app/services/assignment_answers.py`
- **Generate complete answers for ALL questions from an assignment. Tries these…** (1 connections) — `app/services/assignment_answers.py`
- *... and 1 more nodes in this community*

## Relationships

- [server + persistence](server_+_persistence.md) (3 shared connections)
- [assignment_tool + assignment](assignment_tool_+_assignment.md) (3 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (2 shared connections)
- [tools + window_layout](tools_+_window_layout.md) (2 shared connections)
- [assignment_assembler + smart_navigator](assignment_assembler_+_smart_navigator.md) (1 shared connections)
- [jarvis_overlay + prompt_overlay](jarvis_overlay_+_prompt_overlay.md) (1 shared connections)
- [assignment_humanizer](assignment_humanizer.md) (1 shared connections)

## Source Files

- `app/services/assignment_answers.py`

## Audit Trail

- EXTRACTED: 49 (94%)
- INFERRED: 3 (6%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*