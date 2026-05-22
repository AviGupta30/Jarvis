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
  create_file(filepath, content)           — create text file
  get_info(query)                           — search the web for information
  calculate(expression)                     — evaluate math
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
    yield f"[PLAN] Analyzing your request — breaking it into steps..."

    plan = await _call_planner(task, context)
    steps = plan.get("steps", [])
    summary = plan.get("plan_summary", "Working on it...")

    if not steps:
        yield f"[DONE] I couldn't break this task into steps. Let me try directly.\n"
        # Fall back to dynamic skill
        result = await run_dynamic_skill(task, ui_context=context)
        yield f"[RESULT] {result}"
        return

    yield f"[PLAN] {summary} — {len(steps)} step(s) identified."

    # ── Phase 2: Execute steps ────────────────────────────────────────────────
    results: dict = {}       # stored results from steps
    completed: list = []     # log of completed steps
    current_steps = steps
    step_index = 0

    while step_index < len(current_steps):
        step = current_steps[step_index]
        step_num = step.get("step", step_index + 1)
        desc = step.get("description", f"Step {step_num}")
        store_as = step.get("store_result_as")

        yield f"[STEP {step_num}] {desc}"

        success, output = await _execute_step(step, results)

        if store_as:
            results[store_as] = output

        step["result"] = output[:200]

        if success:
            completed.append(step)
            yield f"[STEP {step_num} ✓] {output[:150]}"
            step_index += 1
        else:
            # Step failed — try to replan
            yield f"[STEP {step_num} ✗] Failed: {output[:120]}. Replanning..."

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
                yield f"[DONE] I couldn't recover from that failure. Here's what I completed:\n"
                for c in completed:
                    yield f"  ✓ Step {c['step']}: {c['description']}"
                yield f"\nFailed at Step {step_num}: {desc} — {output[:200]}"
                return

            yield f"[REPLAN] Adjusted approach — {len(new_steps)} remaining step(s)."
            current_steps = new_steps
            step_index = 0  # restart loop with new steps
            continue

    # ── Phase 3: Summary ──────────────────────────────────────────────────────
    yield f"[DONE] All {len(completed)} step(s) complete."
    # Build a short spoken summary from the results
    key_results = [
        f"Step {c['step']} ({c['description'][:40]}): {c.get('result', 'done')[:80]}"
        for c in completed[-3:]  # last 3 steps
    ]
    yield "[SUMMARY] " + " | ".join(key_results)


def is_complex_task(prompt: str) -> bool:
    """
    Returns True ONLY for tasks that genuinely need the multi-step agentic planner.
    Deliberately conservative: simple commands with 'then', 'first', 'and' do NOT trigger.
    """
    lower = prompt.lower().strip()

    # Must be a substantive request to be a real multi-step pipeline
    if len(lower.split()) < 7:
        return False

    # Pattern 1: File reading + output creation pipeline
    file_read = [
        "from the pdf", "from my pdf", "read the pdf", "read my pdf",
        "extract from", "questions from", "content of the pdf",
        "from the document", "from the file", "my assignment pdf",
        "using the pdf", "in the pdf",
    ]
    file_output = [
        "create a word", "make a word doc", "save to word", "write to a file",
        "create a document", "make a document", "copy into word",
        "paste into word", "save answers", "save the answers",
        "create a new file with", "write the answers",
    ]
    has_file_read = any(w in lower for w in file_read)
    has_file_output = any(w in lower for w in file_output)
    if has_file_read and has_file_output:
        return True

    # Pattern 2: Copilot automation with file input
    copilot_kw = [
        "ask copilot each", "ask copilot the questions",
        "use copilot to answer", "copilot each question",
        "type in copilot", "send to copilot",
    ]
    if any(w in lower for w in copilot_kw) and has_file_read:
        return True

    # Pattern 3: Explicit batch operations over many files
    batch_kw = [
        "each question", "every question", "all the questions",
        "for each file", "for every file", "rename all files",
        "move all files", "organize all files", "batch rename",
        "batch convert", "batch compress",
    ]
    if any(w in lower for w in batch_kw):
        return True

    return False


    # Explicit multi-step connectors
    multi_step_words = [
        " and then ", " then ", " after that ", " afterwards ", " next ",
        " followed by ", " after opening ", " once it opens ", " once you open ",
        " first ", "step by step", "step-by-step",
    ]
    if any(w in lower for w in multi_step_words):
        return True

    # Requires reading file content
    file_read_words = [
        "from the pdf", "from my pdf", "the questions in", "based on the",
        "read the pdf", "extract from", "questions from", "content of",
        "from the file", "from the document",
    ]
    if any(w in lower for w in file_read_words):
        return True

    # Requires looping over multiple items
    loop_words = [
        "each question", "every question", "all the questions",
        "for each", "for every", "all of them", "all files",
        "batch", "multiple",
    ]
    if any(w in lower for w in loop_words):
        return True

    # Requires waiting for apps / UI interaction
    wait_words = [
        "open copilot", "open word", "ask copilot", "type in copilot",
        "ask it", "paste into", "copy into", "save as",
        "wait for", "once it", "when it opens",
    ]
    if any(w in lower for w in wait_words):
        return True

    # Multiple distinct action verbs (open + copy + save, etc.)
    action_verbs = ["open", "copy", "paste", "create", "save", "download",
                    "read", "write", "send", "ask", "type", "click", "find",
                    "rename", "move", "convert", "compress", "organize"]
    found_verbs = [v for v in action_verbs if f" {v} " in f" {lower} "]
    if len(found_verbs) >= 3:
        return True

    return False
