"""
Jarvis Agentic Planner — The Brain for Complex Multi-Step Tasks
---------------------------------------------------------------
When a user gives a complex command (multiple actions, file processing,
UI automation, etc.), this planner:

  1. PLANS:   LLM breaks the task into ordered steps with tool assignments
  2. EXECUTES: Each step runs the right tool or generates dynamic code
  3. OBSERVES: Reads screen/output to verify the step succeeded
  4. ADAPTS:   If a step fails, re-plans the remaining steps with the error context
  5. NARRATES: Streams step-by-step status updates back to the voice agent

Example task: "Take my assignment PDF, ask Copilot each question, save Q&A in Word"
  Step 1: find_file("assignment", "Desktop")
  Step 2: read_pdf_text(path=<result>)
  Step 3: Extract questions from text
  Step 4: open_windows_copilot()
  Step 5-N: For each question: send_to_copilot(q), collect answer
  Step N+1: create_word_doc("Assignment_Answers", content)
"""

import json
import asyncio
from typing import AsyncGenerator
from groq import AsyncGroq
from app.core.config import settings
from app.services.tools import TOOL_REGISTRY
from app.services.dynamic_skill import run_dynamic_skill
from app.services.ui_inspector import get_screen_text_summary

client = AsyncGroq(api_key=settings.GROQ_API_KEY)

# ── Planner System Prompt ─────────────────────────────────────────────────────

PLANNER_PROMPT = """\
You are Jarvis's agentic task planner for Windows 11. Your job is to break a complex user task into a precise ordered list of steps.

AVAILABLE TOOLS (call by exact name with arguments as JSON):
  find_file(name, location="all")           — find file on Desktop/Documents/Downloads
  read_pdf_text(path=null, filename=null)   — extract all text from a PDF
  open_file(path)                           — open any file with default app
  focus_window(name, timeout=5.0)          — bring a window to foreground by partial name
  wait_for_window(name, timeout=15.0)       — wait until window appears then focus it
  open_windows_copilot()                    — open Windows Copilot sidebar (Win+C)
  send_to_copilot(question, wait_seconds=8) — type question in Copilot, return response
  create_word_doc(filename, content)        — create .docx on Desktop
  type_text(text)                           — type text into focused field
  type_and_submit(text)                     — type text and press Enter
  copy_selected_text()                      — Ctrl+A + Ctrl+C, return clipboard
  read_active_window_text()                 — read UI text from active window
  open_app(app_name)                        — open notepad, word, chrome, etc.
  open_website(url)                         — open a URL in browser
  take_screenshot()                         — screenshot to Desktop
  create_folder(folder_name)               — create folder on Desktop
  read_file(path)                           — read contents of any text file or PDF
  write_file(path, content)                 — create or overwrite a file with content
  append_file(path, content)                — add content to existing file
  list_directory(path)                      — list files/folders with sizes and dates
  move_file(src, dst)                       — move or rename a file
  delete_file(path)                         — move to Recycle Bin safely
  search_files(name, root_dir)              — find files by name or pattern (supports *)
  create_folder(path)                       — create folder anywhere
  create_word_doc(filename, content)        — create .docx on Desktop
  get_info(query)                           — search the web for information
  calculate(expression)                     — evaluate math
  check_emails(query, max_results)          — search Gmail inbox by keyword/sender/topic
  list_unread(max_results)                  — list unread emails with preview
  get_email_body(email_id)                  — read full body of a specific email by ID
  summarize_inbox(max_results)              — summarize recent emails in inbox
  browse_and_read(url)                      — open URL and extract all visible text
  search_on_site(site_url, query)           — find search box on site, type query, get results
  click_element(page_url, text)             — click a button/link by its visible text
  scroll_and_read(url, px=1000)             — scroll down to load dynamic content
  get_upcoming_events(days)                 — get calendar events for next N days
  check_today_schedule()                    — get calendar events for today
  add_event(title, date, time, notes)       — add an event to Google Calendar
  save_fact(topic, fact)                    — remember a fact about a topic
  recall_facts(topic)                       — read saved facts about a topic
  get_morning_brief()                       — summarize calendar and emails for the morning
  click_ui_element_uia(app_title, element_name=None, automation_id=None, control_type=None)
                                            — click a button/control inside any app WITHOUT moving the mouse.
                                              Preferred over coordinate clicks. Use automation_id when known.
  type_into_ui_element(app_title, element_name=None, text="", automation_id=None)
                                            — inject text into an input field in any app via UIA Value pattern.
                                              No simulated keystrokes. Works on background windows.
  read_ui_element_text(app_title, element_name=None, automation_id=None)
                                            — read text from a specific control (e.g. terminal output pane).
  dump_app_ui_tree(app_title, depth=3)      — dump the accessibility tree of an app to discover AutomationIds.
                                              Run once per new app to map its controls.
  DYNAMIC(description)                      — for anything not in the above list, write a description and Jarvis will generate code

OUTPUT FORMAT — return ONLY valid JSON, exactly this structure:
{
  "plan_summary": "One sentence describing the overall plan",
  "steps": [
    {
      "step": 1,
      "description": "What this step does (for narrating to user)",
      "tool": "tool_name_or_DYNAMIC",
      "args": {"arg1": "value1", "arg2": "value2"},
      "depends_on_result_of": null,
      "store_result_as": "variable_name_or_null"
    }
  ]
}

RULES:
- Use "depends_on_result_of": "variable_name" when a step needs the output from a previous step.
- Use "store_result_as": "variable_name" to name outputs that later steps need.
- For loops (e.g., ask Copilot N questions), use tool="DYNAMIC" and describe the full loop in the description.
- Keep steps atomic: one tool call per step.
- If you need to open an app and wait for it, use open_app + wait_for_window as separate steps.
- Be precise about file names (keep the user's exact words).
- Maximum 20 steps.

TASK: {task}
SCREEN CONTEXT: {context}
"""

REPLANNER_PROMPT = """\
You are Jarvis's adaptive task replanner. A step failed — replan the remaining steps to recover.

ORIGINAL TASK: {task}
COMPLETED STEPS: {completed}
FAILED STEP: {failed_step}
ERROR: {error}
CURRENT SCREEN: {context}

Produce a new JSON plan for ONLY the remaining steps needed to complete the task.
Use the same JSON format: {{ "plan_summary": "...", "steps": [...] }}
Number steps starting from {next_step_num}.
If recovery is impossible, return: {{ "plan_summary": "failed", "steps": [] }}
"""


async def _call_planner(task: str, context: str) -> dict:
    """Ask the LLM to produce a step-by-step plan."""
    prompt = PLANNER_PROMPT.format(task=task, context=context or "Desktop")
    resp = await client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        max_tokens=2000,
        temperature=0.1,
    )
    content = resp.choices[0].message.content
    try:
        return json.loads(content)
    except Exception:
        return {"plan_summary": "plan parse error", "steps": []}


async def _call_replanner(task: str, completed: list, failed_step: dict,
                           error: str, next_num: int, context: str) -> dict:
    """Ask the LLM to replan after a failure."""
    completed_str = "\n".join(
        f"  Step {s['step']}: {s['description']} → {s.get('result', 'done')}"
        for s in completed
    )
    prompt = REPLANNER_PROMPT.format(
        task=task,
        completed=completed_str or "(none yet)",
        failed_step=json.dumps(failed_step),
        error=error[:300],
        context=context or "unknown",
        next_step_num=next_num,
    )
    resp = await client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        max_tokens=1500,
        temperature=0.1,
    )
    content = resp.choices[0].message.content
    try:
        return json.loads(content)
    except Exception:
        return {"plan_summary": "failed", "steps": []}


async def _execute_step(step: dict, results: dict) -> tuple[bool, str]:
    """
    Execute a single plan step.
    Returns (success, output_string).
    """
    tool_name = step.get("tool", "")
    raw_args = step.get("args", {}) or {}

    # Resolve any arg that references a stored result
    resolved_args = {}
    for k, v in raw_args.items():
        if isinstance(v, str) and v.startswith("$"):
            # $variable_name → look up in results
            var = v[1:]
            resolved_args[k] = results.get(var, v)
        else:
            resolved_args[k] = v

    # DYNAMIC tool → use dynamic skill engine
    if tool_name == "DYNAMIC":
        desc = step.get("description", "")
        # Pass in all stored results as context
        ctx_lines = [f"{k}: {str(v)[:200]}" for k, v in results.items()]
        ctx = get_screen_text_summary() + "\n\nPrevious step results:\n" + "\n".join(ctx_lines)
        try:
            result = await run_dynamic_skill(desc, ui_context=ctx)
            return True, result
        except Exception as e:
            return False, str(e)

    # Known tool → call from registry
    if tool_name in TOOL_REGISTRY:
        try:
            loop = asyncio.get_event_loop()
            # Run blocking tools in executor to avoid blocking the event loop
            result = await loop.run_in_executor(None, lambda: TOOL_REGISTRY[tool_name](**resolved_args))
            return True, str(result)
        except Exception as e:
            return False, str(e)

    return False, f"Unknown tool: {tool_name}"


async def run_agentic_plan(task: str) -> AsyncGenerator[str, None]:
    """
    Main agentic execution loop.
    Yields status strings that the voice/chat layer streams to the user.

    Usage:
        async for update in run_agentic_plan(task):
            # stream update to user
    """
    # ── Phase 1: Plan ─────────────────────────────────────────────────────────
    context = get_screen_text_summary()
    yield "I am analyzing your request and breaking it down into steps."

    plan = await _call_planner(task, context)
    steps = plan.get("steps", [])
    summary = plan.get("plan_summary", "Working on it...")

    if not steps:
        yield "I couldn't break this into steps, so I'll try to handle it directly."
        # Fall back to dynamic skill
        result = await run_dynamic_skill(task, ui_context=context)
        yield f"Result: {result}"
        return

    yield f"Plan ready: {summary}. I have identified {len(steps)} steps to complete this."

    # ── Phase 2: Execute steps ────────────────────────────────────────────────
    results: dict = {}       # stored results from steps
    completed: list = []     # log of completed steps
    current_steps = steps
    step_index = 0
    replan_attempts = 0      # Guard against infinite loops

    while step_index < len(current_steps):
        step = current_steps[step_index]
        step_num = step.get("step", step_index + 1)
        desc = step.get("description", f"Step {step_num}")
        store_as = step.get("store_result_as")

        yield f"Starting Step {step_num}: {desc}."

        success, output = await _execute_step(step, results)

        if store_as:
            results[store_as] = output

        step["result"] = output[:200]

        if success:
            completed.append(step)
            # Remove long output text from speech, just say it succeeded
            yield f"Step {step_num} completed successfully."
            step_index += 1
            replan_attempts = 0  # reset on success
        else:
            if replan_attempts >= 2:
                yield f"I've failed to recover after multiple attempts. Stopping here. The error was: {output[:150]}"
                return

            replan_attempts += 1
            # Step failed — try to replan
            yield f"Step {step_num} failed. I am adjusting my plan and trying again."

            context = get_screen_text_summary()
            next_num = step_num + 1
            new_plan = await _call_replanner(
                task=task,
                completed=completed,
                failed_step=step,
                error=output,
                next_num=next_num,
                context=context,
            )
            new_steps = new_plan.get("steps", [])

            if not new_steps or new_plan.get("plan_summary") == "failed":
                yield f"I couldn't figure out a way to recover. I have stopped working."
                return

            yield f"I've updated my approach. There are {len(new_steps)} steps remaining."
            current_steps = new_steps
            step_index = 0  # restart loop with new steps
            continue

    # ── Phase 3: Summary ──────────────────────────────────────────────────────
    yield f"Task complete. All steps finished."
    # Build a short spoken summary from the results
    key_results = [
        f"For step {c['step']} ({c['description'][:40]}), the result was: {c.get('result', 'done')[:80]}"
        for c in completed[-3:]  # last 3 steps
    ]
    yield "Summary: " + ". ".join(key_results)


def is_complex_task(prompt: str) -> bool:
    """
    Returns True when a task genuinely needs the multi-step agentic planner.
    Conservative for simple commands, broad enough to catch real pipelines.

    FIXED: Previous version had dead code — patterns below 'return False' were
    never reached. All patterns are now live and properly ordered.
    """
    lower = prompt.lower().strip()

    # Very short commands are never complex
    if len(lower.split()) < 6:
        return False

    # -- Pattern 1: File reading + output creation pipeline --
    file_read_kw = [
        "from the pdf", "from my pdf", "read the pdf", "read my pdf",
        "extract from", "questions from", "content of the pdf",
        "from the document", "from the file", "my assignment pdf",
        "using the pdf", "in the pdf", "from the doc",
    ]
    file_output_kw = [
        "create a word", "make a word doc", "save to word", "write to a file",
        "create a document", "make a document", "copy into word",
        "paste into word", "save answers", "save the answers",
        "create a new file", "write the answers", "save it to",
        "write it to", "put it in a file",
    ]
    has_file_read = any(w in lower for w in file_read_kw)
    has_file_output = any(w in lower for w in file_output_kw)
    if has_file_read and has_file_output:
        return True

    # -- Pattern 2: Copilot automation with file input --
    copilot_kw = [
        "ask copilot each", "ask copilot the questions",
        "use copilot to answer", "copilot each question",
        "type in copilot", "send to copilot",
    ]
    if any(w in lower for w in copilot_kw) and has_file_read:
        return True

    # -- Pattern 3: Batch file operations --
    batch_kw = [
        "each question", "every question", "all the questions",
        "for each file", "for every file", "rename all files",
        "move all files", "organize all files", "batch rename",
        "batch convert", "batch compress", "all files in",
        "every file in",
    ]
    if any(w in lower for w in batch_kw):
        return True

    # -- Pattern 4: Email + action chains (NEW) --
    email_kw = [
        "check my email", "check my mail", "check my gmail",
        "look at my email", "emails about", "email from",
        "any emails", "new emails", "unread emails",
        "internship email", "internship mail",
        "competition email", "college email",
    ]
    email_action_kw = [
        "and", "then", "if yes", "if any", "if there are",
        "make a note", "create a file", "save them", "list them",
        "write them", "tell me", "summarize",
    ]
    has_email = any(w in lower for w in email_kw)
    has_email_action = any(w in lower for w in email_action_kw)
    if has_email and has_email_action:
        return True

    # -- Pattern 5: Browser + action chains (NEW) --
    browser_nav_kw = [
        "go to ", "browse ", "open the site", "navigate to",
        "on internshala", "on linkedin", "on naukri", "on github",
        "on the website", "on the site", "on the page",
        ".com and", ".in and",
    ]
    browser_action_kw = [
        "and find", "and read", "and get", "and list", "and save",
        "and tell me", "and create", "and download", "and note",
        "and summarize", "and write",
    ]
    has_browser_nav = any(w in lower for w in browser_nav_kw)
    has_browser_action = any(w in lower for w in browser_action_kw)
    if has_browser_nav and has_browser_action:
        return True

    # -- Pattern 6: Explicit multi-step connectors (length-gated) --
    multi_step_kw = [
        " and then ", " after that ", " afterwards ",
        " followed by ", " after opening ", " once it opens ",
        " once you open ", "step by step", "step-by-step",
    ]
    if any(w in lower for w in multi_step_kw) and len(lower.split()) >= 10:
        return True

    # -- Pattern 7: Multi-verb pipelines (3+ distinct action verbs) --
    action_verbs = [
        "open", "copy", "paste", "create", "save", "download",
        "read", "write", "send", "ask", "type", "click", "find",
        "rename", "move", "convert", "compress", "organize",
        "search", "browse", "check", "extract", "summarize",
    ]
    found_verbs = [v for v in action_verbs if f" {v} " in f" {lower} "]
    if len(found_verbs) >= 3 and len(lower.split()) >= 12:
        return True

    # -- Pattern 8: Waiting on apps / UI interaction --
    wait_kw = [
        "open copilot", "open word", "ask copilot", "type in copilot",
        "paste into", "copy into", "wait for", "once it opens",
        "when it opens",
    ]
    if any(w in lower for w in wait_kw) and len(lower.split()) >= 8:
        return True

    return False

