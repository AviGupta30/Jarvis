# assignment_answers

> 27 nodes · cohesion 0.11

## Key Concepts

- **assignment_answers.py** (22 connections) — `app/services/assignment_answers.py`
- **io** (11 connections)
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
- *... and 2 more nodes in this community*

## Relationships

- [assignment_humanizer + task_ledger](assignment_humanizer_+_task_ledger.md) (3 shared connections)
- [screen_vision + screen_reader](screen_vision_+_screen_reader.md) (3 shared connections)
- [assignment_tool + assignment_pipeline](assignment_tool_+_assignment_pipeline.md) (3 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (2 shared connections)
- [tools](tools.md) (2 shared connections)
- [smart_navigator + ssml_processor](smart_navigator_+_ssml_processor.md) (1 shared connections)
- [message_reader + thread_extractor](message_reader_+_thread_extractor.md) (1 shared connections)
- [assignment_tool](assignment_tool.md) (1 shared connections)
- [ppt_chart_engine + jarvis_overlay](ppt_chart_engine_+_jarvis_overlay.md) (1 shared connections)
- [ppt_tool](ppt_tool.md) (1 shared connections)
- [recolor + exact_render](recolor_+_exact_render.md) (1 shared connections)
- [safe_executor + refresh_docs](safe_executor_+_refresh_docs.md) (1 shared connections)

## Source Files

- `app/services/assignment_answers.py`

## Audit Trail

- EXTRACTED: 59 (95%)
- INFERRED: 3 (5%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*