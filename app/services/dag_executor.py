"""
dag_executor.py — Jarvis DAG-Based Multi-Step Agent Planner
------------------------------------------------------------
Upgrades the linear planner into a true Directed Acyclic Graph (DAG) executor.

Architecture Rule #4 compliant:
  - Completely isolated file (no imports from other tool modules)
  - All output streams through /chat → voice.py speak_stream() AND frontend SSE
  - Dual interface: both voice and UI receive real-time node status updates

How it works:
  1. DECOMPOSE:  LLM breaks the task into a DAG of nodes with explicit depends_on edges
  2. VALIDATE:   Kahn's algorithm detects cycles and computes topological order
  3. WAVE EXEC:  Nodes with no pending dependencies form a "wave" and run via asyncio.gather()
  4. RETRY:      Each node has its own retry budget + optional fallback_tool
  5. AGGREGATE:  Final AGGREGATE pseudo-node merges all results into one spoken summary
  6. STREAM:     Every state change yields a structured SSE JSON event

Example:
  Input: "Plan my week, email my professor, and remind me Friday"
  DAG:
    [check_calendar] ──┐
    [draft_email]   ──►── [aggregate]
    [set_reminder]  ──┘

  Execution:
    Wave 1: check_calendar + draft_email + set_reminder (all parallel)
    Wave 2: aggregate (waits for all three)
"""

import json
import asyncio
import logging
from dataclasses import dataclass, field
from typing import AsyncGenerator
from collections import deque

from groq import AsyncGroq
from app.core.config import settings
from app.services.tools import TOOL_REGISTRY
from app.services.dynamic_skill import run_dynamic_skill
from app.services.ui_inspector import get_screen_text_summary

logger = logging.getLogger(__name__)
client = AsyncGroq(api_key=settings.GROQ_API_KEY)

# ── Configuration ─────────────────────────────────────────────────────────────
MAX_PARALLEL    = 2       # max nodes running at the same time (avoids Groq rate limits)
RETRY_BACKOFF   = [0.5, 1.0]   # seconds to wait between retries (len = max retries)
AGGREGATE_MODEL = "llama-3.1-8b-instant"


# ── Data Structures ────────────────────────────────────────────────────────────

@dataclass
class DAGNode:
    """Represents a single task node in the execution graph."""
    id: str
    description: str
    tool: str                          # tool name, "DYNAMIC", or "AGGREGATE"
    args: dict = field(default_factory=dict)
    depends_on: list = field(default_factory=list)   # list of node ids
    store_result_as: str | None = None
    retry_limit: int = 2
    fallback_tool: str | None = None

    # Runtime state
    status: str = "pending"            # pending | running | done | failed | skipped
    result: str = ""
    error: str = ""
    attempt: int = 0


# ── Planner Prompt ─────────────────────────────────────────────────────────────

DAG_PLANNER_PROMPT = """\
You are Jarvis's DAG task planner. Break the user's request into a dependency graph of sub-tasks.

AVAILABLE TOOLS:
  get_upcoming_events(days)           — get calendar events for next N days
  check_today_schedule()              — get today's calendar events
  add_event(title, date, time, notes) — add event to Google Calendar
  check_emails(query, max_results)    — search Gmail by keyword/sender
  list_unread(max_results)            — list unread emails
  summarize_inbox(max_results)        — summarize recent emails
  get_info(query)                     — web search / weather / general info
  get_system_time()                   — current date and time
  get_system_info()                   — CPU, RAM, battery
  set_reminder(message, seconds)      — set a timed reminder
  save_fact(topic, fact)              — remember a fact
  recall_facts(topic)                 — recall facts about a topic
  take_screenshot()                   — capture screen
  get_morning_brief()                 — calendar + email morning summary
  read_file(path)                     — read a text/PDF file
  write_file(path, content)           — write content to a file
  list_directory(path)                — list files in a directory
  create_word_doc(filename, content)  — create a Word document
  open_app(app_name)                  — open a desktop application
  open_website(url)                   — open a website in browser
  initiate_whatsapp_send(contact_name, message) — PREPARE a WhatsApp message for confirmation. Returns a confirmation prompt, does NOT send yet. Use for any "message/text/whatsapp [person]" requests.
  DYNAMIC(description)                — generate Python code for anything not listed above
  AGGREGATE                           — special: collect all results and summarize (always last node)

CRITICAL RULES FOR WHATSAPP/MESSAGING:
  - ALWAYS use initiate_whatsapp_send for ANY "message", "text", "whatsapp" tasks.
  - The result will be a confirmation prompt like "Ready to send to X — confirm?"
  - NEVER say the message was sent in the aggregate summary. Say "I have prepared a message to X ready for your confirmation."
  - If the message content is not specified in the prompt, set message arg to "(ask user for message content)".

OUTPUT FORMAT — return ONLY valid JSON, exactly this structure:
{{
  "plan_summary": "One sentence describing the full plan",
  "nodes": [
    {{
      "id": "unique_snake_case_id",
      "description": "What this step does (spoken to user)",
      "tool": "tool_name_or_DYNAMIC_or_AGGREGATE",
      "args": {{"arg1": "value1"}},
      "depends_on": [],
      "store_result_as": "variable_name_or_null",
      "retry_limit": 2,
      "fallback_tool": "fallback_tool_name_or_null"
    }}
  ]
}}

RULES:
- Each node id must be unique, lowercase, snake_case.
- depends_on lists the IDs of nodes that must finish before this node starts.
- Use "$variable_name" in args values to reference a stored result from a previous node.
- Always end with exactly one AGGREGATE node that depends_on ALL other non-aggregate nodes.
- The AGGREGATE node has no args (args: {{}}) and store_result_as: null.
- Keep it to max 8 nodes (excluding AGGREGATE).
- Independent tasks (no data dependency) MUST have empty depends_on so they run in parallel.
- Only add a depends_on edge if the node truly needs the result of another node.
- For each tool, suggest a sensible fallback_tool or null.
- NEVER return more than one AGGREGATE node.

EXAMPLES of parallel vs sequential:
  "email professor AND check calendar AND set reminder"
    → email, calendar, reminder all have depends_on: []  ← PARALLEL
    → aggregate depends_on: ["email", "calendar", "reminder"]

  "check emails THEN summarize them into a doc"
    → check_emails depends_on: []
    → create_doc depends_on: ["check_emails"]  ← SEQUENTIAL
    → aggregate depends_on: ["create_doc"]

TASK: {task}
SCREEN CONTEXT: {context}
"""


AGGREGATE_PROMPT = """\
You are Jarvis. The user asked: "{task}"

You just completed all the sub-tasks. Here are the results:

{results}

Give a concise, natural spoken summary of everything you accomplished.
Speak directly to the user as Jarvis would — confident, helpful, first-person.
Maximum 4 sentences. Do NOT list items with bullets or numbers — just natural speech.
"""


# ── DAG Planner LLM Call ──────────────────────────────────────────────────────

async def _call_dag_planner(task: str, context: str) -> dict:
    """Ask the LLM to produce a DAG plan. Returns parsed dict."""
    prompt = DAG_PLANNER_PROMPT.format(task=task, context=context or "Desktop")
    try:
        resp = await client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            max_tokens=2000,
            temperature=0.1,
        )
        return json.loads(resp.choices[0].message.content)
    except Exception as e:
        logger.error(f"[DAG] Planner LLM call failed: {e}")
        return {"plan_summary": "plan error", "nodes": []}


# ── Cycle Detection & Topological Sort (Kahn's Algorithm) ────────────────────

def _topological_sort(nodes: list[DAGNode]) -> list[list[str]] | None:
    """
    Returns execution waves — each wave is a list of node IDs that can run in parallel.
    Returns None if the graph has a cycle.

    Kahn's algorithm:
      1. Build in-degree count for each node
      2. Start with all zero-in-degree nodes (wave 1)
      3. After processing a wave, decrement in-degree of dependents
      4. Any new zero-in-degree nodes form the next wave
      5. If not all nodes processed → cycle detected
    """
    id_to_node = {n.id: n for n in nodes}
    in_degree = {n.id: 0 for n in nodes}
    dependents = {n.id: [] for n in nodes}  # who depends ON this node

    for node in nodes:
        for dep_id in node.depends_on:
            if dep_id not in id_to_node:
                logger.warning(f"[DAG] Node '{node.id}' depends on unknown id '{dep_id}' — skipping edge")
                continue
            in_degree[node.id] += 1
            dependents[dep_id].append(node.id)

    waves = []
    queue = deque([nid for nid, deg in in_degree.items() if deg == 0])
    processed = 0

    while queue:
        # All nodes currently at in-degree 0 form one wave
        wave = list(queue)
        queue.clear()
        waves.append(wave)
        processed += len(wave)

        for nid in wave:
            for dep_nid in dependents[nid]:
                in_degree[dep_nid] -= 1
                if in_degree[dep_nid] == 0:
                    queue.append(dep_nid)

    if processed != len(nodes):
        logger.error(f"[DAG] Cycle detected! Processed {processed}/{len(nodes)} nodes.")
        return None

    return waves


# ── Argument Resolver ─────────────────────────────────────────────────────────

def _resolve_args(raw_args: dict, results: dict) -> dict:
    """Replace $variable references in args with actual stored results."""
    resolved = {}
    for k, v in raw_args.items():
        if isinstance(v, str) and v.startswith("$"):
            var = v[1:]
            resolved[k] = results.get(var, v)   # keep raw string if not found
        elif isinstance(v, list):
            resolved[k] = [
                results.get(item[1:], item) if isinstance(item, str) and item.startswith("$") else item
                for item in v
            ]
        else:
            resolved[k] = v
    return resolved


# ── Single Node Executor ──────────────────────────────────────────────────────

async def _execute_node(node: DAGNode, results: dict, task: str) -> tuple[bool, str]:
    """
    Execute a single DAG node. Returns (success, output_string).
    Handles DYNAMIC and AGGREGATE pseudo-tools internally.
    """
    resolved_args = _resolve_args(node.args, results)

    # — AGGREGATE pseudo-tool: call Groq to synthesize all stored results —
    if node.tool == "AGGREGATE":
        result_lines = []
        for key, val in results.items():
            short_val = str(val)[:300]
            result_lines.append(f"  [{key}]: {short_val}")
        results_text = "\n".join(result_lines) or "(no results captured)"
        prompt = AGGREGATE_PROMPT.format(task=task, results=results_text)
        try:
            resp = await client.chat.completions.create(
                model=AGGREGATE_MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0.6,
            )
            return True, resp.choices[0].message.content.strip()
        except Exception as e:
            return False, f"Aggregation failed: {e}"

    # — DYNAMIC tool: generate + execute Python code —
    if node.tool == "DYNAMIC":
        desc = node.description
        ctx_lines = [f"{k}: {str(v)[:150]}" for k, v in results.items()]
        ctx = get_screen_text_summary() + "\n\nPrevious results:\n" + "\n".join(ctx_lines)
        try:
            result = await run_dynamic_skill(desc, ui_context=ctx)
            return True, result
        except Exception as e:
            return False, str(e)

    # — Known tool from registry —
    if node.tool in TOOL_REGISTRY:
        try:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None, lambda: TOOL_REGISTRY[node.tool](**resolved_args)
            )
            return True, str(result)
        except Exception as e:
            return False, str(e)

    return False, f"Unknown tool: {node.tool}"


# ── Node Runner with Retry + Fallback ─────────────────────────────────────────

async def _run_node_with_retry(node: DAGNode, results: dict, task: str) -> tuple[bool, str]:
    """
    Run a node with retry logic and optional fallback tool.
    Returns (success, final_output).
    """
    last_error = ""
    for attempt in range(node.retry_limit + 1):
        node.attempt = attempt
        success, output = await _execute_node(node, results, task)
        if success:
            return True, output
        last_error = output
        if attempt < node.retry_limit:
            backoff = RETRY_BACKOFF[min(attempt, len(RETRY_BACKOFF) - 1)]
            await asyncio.sleep(backoff)

    # All retries exhausted — try fallback tool if available
    if node.fallback_tool and node.fallback_tool in TOOL_REGISTRY:
        resolved_args = _resolve_args(node.args, results)
        try:
            loop = asyncio.get_event_loop()
            fallback_result = await loop.run_in_executor(
                None, lambda: TOOL_REGISTRY[node.fallback_tool](**resolved_args)
            )
            return True, f"[via fallback '{node.fallback_tool}'] {fallback_result}"
        except Exception as e:
            last_error = f"Fallback also failed: {e}"

    return False, last_error


# ── DAG Detector ──────────────────────────────────────────────────────────────

_DAG_MULTI_BRANCH_PATTERNS = [
    # Explicit multi-branch conjunctions with distinct actions
    r"\b(email|message|msg|text|whatsapp)\b.{3,60}\b(and|also|plus)\b.{3,60}\b(remind|reminder|calendar|schedule|event)\b",
    r"\b(check|read|look at)\b.{3,40}\b(and|also)\b.{3,40}\b(remind|set|add|create|message|text)\b",
    r"\b(plan|organize|schedule)\b.{3,40}\b(and|also|plus)\b.{3,40}\b(email|message|text|whatsapp|send|notify)\b",
    r"\b(remind me|set a reminder)\b.{3,60}\b(and|also|plus)\b.{3,60}\b(email|check|look|send|message|text)\b",
    r"\b(message|text|whatsapp)\b.{2,40}\b(and|also)\b.{3,40}\b(remind|calendar|schedule|event|plan)\b",
]

_DAG_COMPOUND_VERBS = [
    # Three or more distinct action verb groups separated by 'and'/'also'/'plus'
    ("email", "calendar"),
    ("email", "remind"),
    ("check email", "check calendar"),
    ("read email", "check schedule"),
    ("plan", "email", "remind"),
    ("summarize email", "check calendar"),
    ("check inbox", "upcoming events"),
]

_EXCLUDED_FROM_DAG = [
    # These are complex but handled by the existing linear planner
    "do my assignment", "complete my assignment", "solve my assignment",
    "from the pdf", "from my pdf", "read the pdf",
    "create a presentation", "make a ppt", "ppt on", "ppt about",
    # Single-tool tasks that happen to contain 'and'
    "play music and", "open spotify and",
    "search for", "find me", "look up",
]


def is_dag_task(prompt: str) -> bool:
    """
    Returns True when the user's request requires a multi-branch DAG plan.
    More targeted than is_complex_task — specifically catches multi-intent
    prompts where independent sub-tasks should run in parallel.

    Must NOT fire for:
      - Single-tool commands
      - Assignment pipeline tasks (handled by linear planner)
      - PPT generation tasks
      - Prompts already caught by keyword routes
    """
    import re
    lower = prompt.lower().strip()

    # Too short to be multi-branch
    if len(lower.split()) < 5:
        return False

    # Explicitly excluded patterns (linear planner territory)
    if any(kw in lower for kw in _EXCLUDED_FROM_DAG):
        return False

    # Must contain a conjunction that hints at multiple distinct intents
    if not any(kw in lower for kw in [" and ", " also ", " plus ", " as well as ", " additionally "]):
        return False

    # Pattern matching for multi-branch intents
    for pattern in _DAG_MULTI_BRANCH_PATTERNS:
        if re.search(pattern, lower):
            return True

    # Compound domain check: count distinct action verb domains
    # A prompt touching 2+ domains = multi-branch DAG task
    domains_found = 0

    email_kw    = ["email", "mail", "inbox", "gmail", "unread emails", "check email", "read email"]
    calendar_kw = ["calendar", "schedule", "event", "remind", "reminder", "upcoming",
                   "plan my week", "plan my day", "plan my month", "plan my schedule",
                   "plan the week", "organize my week", "organize my day",
                   "morning brief", "what's on my schedule"]
    messaging_kw= ["message ", "msg ", "text to", "whatsapp to", "send a message",
                   "send whatsapp", "ping ", "dm "]
    file_kw     = ["file", "document", "write", "save", "create doc", "word doc"]
    web_kw      = ["search", "browse", "look up", "find", "google"]
    system_kw   = ["system info", "screenshot", "volume", "open app"]

    if any(kw in lower for kw in email_kw):
        domains_found += 1
    if any(kw in lower for kw in calendar_kw):
        domains_found += 1
    if any(kw in lower for kw in messaging_kw):
        domains_found += 1
    if any(kw in lower for kw in file_kw):
        domains_found += 1
    if any(kw in lower for kw in web_kw):
        domains_found += 1
    if any(kw in lower for kw in system_kw):
        domains_found += 1

    # Two or more distinct domains + a conjunction = multi-branch DAG task
    if domains_found >= 2:
        return True

    return False


# ── Main DAG Execution Loop ───────────────────────────────────────────────────

async def run_dag_plan(task: str) -> AsyncGenerator[str, None]:
    """
    Main DAG execution entry point.

    Yields structured SSE JSON strings:
      data: {"type": "plan", "summary": "...", "nodes": [...]}
      data: {"type": "node_start", "id": "...", "description": "..."}
      data: {"type": "node_done", "id": "...", "result": "..."}
      data: {"type": "node_failed", "id": "...", "error": "...", "retrying": bool}
      data: {"type": "aggregate", "text": "..."}
      data: {"type": "done"}

    The frontend parses these to render a live DAG panel.
    The voice layer reads the embedded text fields for spoken narration.
    """
    # ── Phase 1: Plan ─────────────────────────────────────────────────────────
    context = get_screen_text_summary()
    yield _sse({"type": "thinking", "text": "Analyzing your request and building a task graph..."})

    raw_plan = await _call_dag_planner(task, context)
    plan_summary = raw_plan.get("plan_summary", "Working on it...")
    raw_nodes = raw_plan.get("nodes", [])

    if not raw_nodes:
        # Fallback to linear planner when DAG decomposition fails
        yield _sse({"type": "fallback", "text": "I couldn't decompose this into parallel tasks. Running sequentially..."})
        try:
            from app.services.planner import run_agentic_plan
            async for update in run_agentic_plan(task):
                yield _sse({"type": "narration", "text": update})
        except Exception as e:
            yield _sse({"type": "error", "text": f"Could not execute plan: {e}"})
        yield _sse({"type": "done"})
        return

    # Build DAGNode objects
    nodes: list[DAGNode] = []
    for raw in raw_nodes:
        nodes.append(DAGNode(
            id=raw.get("id", f"node_{len(nodes)}"),
            description=raw.get("description", ""),
            tool=raw.get("tool", "DYNAMIC"),
            args=raw.get("args", {}),
            depends_on=raw.get("depends_on", []),
            store_result_as=raw.get("store_result_as"),
            retry_limit=int(raw.get("retry_limit", 2)),
            fallback_tool=raw.get("fallback_tool"),
        ))

    # Validate + sort
    waves = _topological_sort(nodes)
    if waves is None:
        yield _sse({"type": "error", "text": "Cycle detected in task graph — falling back to sequential execution."})
        try:
            from app.services.planner import run_agentic_plan
            async for update in run_agentic_plan(task):
                yield _sse({"type": "narration", "text": update})
        except Exception as e:
            yield _sse({"type": "error", "text": f"Fallback also failed: {e}"})
        yield _sse({"type": "done"})
        return

    # Emit plan to frontend for graph rendering
    node_list = [
        {
            "id": n.id,
            "description": n.description,
            "tool": n.tool,
            "depends_on": n.depends_on,
            "status": "pending",
        }
        for n in nodes
    ]
    yield _sse({
        "type": "plan",
        "summary": plan_summary,
        "nodes": node_list,
        "wave_count": len(waves),
    })

    parallel_count = sum(1 for w in waves if len(w) > 1)
    wave_text = f"{len(waves)} stage{'s' if len(waves) != 1 else ''}"
    if parallel_count > 0:
        wave_text += f" ({parallel_count} parallel)"
    yield _sse({
        "type": "narration",
        "text": f"Plan ready: {plan_summary}. Running {len(nodes)} tasks across {wave_text}."
    })

    # ── Phase 2: Execute Waves ────────────────────────────────────────────────
    id_to_node = {n.id: n for n in nodes}
    results: dict = {}   # stores variable outputs

    for wave_idx, wave_ids in enumerate(waves):
        wave_nodes = [id_to_node[nid] for nid in wave_ids]

        if len(wave_ids) > 1:
            yield _sse({
                "type": "wave_start",
                "wave": wave_idx + 1,
                "text": f"Running {len(wave_ids)} tasks in parallel: {', '.join(n.description[:30] for n in wave_nodes)}",
            })

        # Semaphore to cap concurrency
        sem = asyncio.Semaphore(MAX_PARALLEL)

        async def run_one(node: DAGNode):
            async with sem:
                node.status = "running"
                yield_queue.append(_sse({
                    "type": "node_start",
                    "id": node.id,
                    "description": node.description,
                    "tool": node.tool,
                }))

                success, output = await _run_node_with_retry(node, results, task)

                if success:
                    node.status = "done"
                    node.result = output
                    if node.store_result_as:
                        results[node.store_result_as] = output
                    yield_queue.append(_sse({
                        "type": "node_done",
                        "id": node.id,
                        "result": output[:200],
                    }))
                else:
                    node.status = "failed"
                    node.error = output
                    yield_queue.append(_sse({
                        "type": "node_failed",
                        "id": node.id,
                        "error": output[:200],
                        "retrying": False,
                    }))

        # asyncio.gather doesn't support async generators directly —
        # use a shared queue to collect events from concurrent tasks
        yield_queue = []

        await asyncio.gather(*[run_one(node) for node in wave_nodes])

        # Flush all events from this wave
        for event in yield_queue:
            yield event

    # ── Phase 3: Final aggregate narration ───────────────────────────────────
    aggregate_node = next((n for n in nodes if n.tool == "AGGREGATE"), None)
    if aggregate_node:
        aggregate_node.status = "running"
        yield _sse({"type": "node_start", "id": aggregate_node.id, "description": "Compiling final summary..."})
        success, summary = await _run_node_with_retry(aggregate_node, results, task)
        if success:
            aggregate_node.status = "done"
            yield _sse({"type": "node_done", "id": aggregate_node.id, "result": summary[:200]})
            yield _sse({"type": "aggregate", "text": summary})
        else:
            # Produce a basic fallback summary
            done_nodes = [n for n in nodes if n.status == "done" and n.tool != "AGGREGATE"]
            if done_nodes:
                fallback_summary = f"I completed {len(done_nodes)} tasks: " + ", ".join(
                    n.description[:40] for n in done_nodes
                ) + "."
            else:
                fallback_summary = "The tasks were attempted but some steps encountered errors."
            yield _sse({"type": "aggregate", "text": fallback_summary})
    else:
        # No aggregate node — build a simple summary
        done_nodes = [n for n in nodes if n.status == "done"]
        failed_nodes = [n for n in nodes if n.status == "failed"]
        parts = []
        if done_nodes:
            parts.append(f"Completed {len(done_nodes)} task(s)")
        if failed_nodes:
            parts.append(f"{len(failed_nodes)} task(s) failed")
        yield _sse({"type": "aggregate", "text": ". ".join(parts) + "."})

    yield _sse({"type": "done"})


# ── SSE Helper ────────────────────────────────────────────────────────────────

def _sse(data: dict) -> str:
    """Format a dict as a Server-Sent Event data line."""
    return f"data: {json.dumps(data)}\n\n"
