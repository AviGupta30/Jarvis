# Tool registry & adding tools

## Purpose
`TOOL_REGISTRY` (bottom of `app/services/tools.py`) is the only tool surface the routers, planner and DAG see. Full table with triggers: `docs/TOOLS.md`.

## Adding a tool (checklist)
1. Implement in its own `app/services/<name>.py`. Wrap in try/except, return a string (or a generator of progress strings), keep it stateless, import no other tool module.
2. Register: `"my_tool": lambda a, b=1: __import__('app.services.my_mod', fromlist=['fn']).fn(a, b),` (lazy import keeps startup fast).
3. LLM router: one terse line in `TOOL_ROUTER_PROMPT` (`app/services/personality.py`).
4. Optional fast path: regex in `keyword_detect_tool` (`app/api/chat.py`).
5. Optional: list it in `PLANNER_PROMPT` (planner.py) / the DAG prompt (dag_executor.py).
6. Update `docs/TOOLS.md` row + run `python scripts/refresh_docs.py`.

## Calling tools from code
- From `/chat`: done inline in `chat_endpoint`.
- From any other async code: `await tool_runner.run_tool(name, args)`. It uses a thread pool, joins generators, and awaits `recall_memory`.
- `POST /execute {tool_name, arguments}` uses tool_runner too.

## Gotchas
- `recall_memory` in the registry is a placeholder (it's async). Never call it directly.
- Email tools go through `_mail_tool` (Gmail API → browser fallback).
- Generator tools: `ppt_create`, `ppt_edit`, `research_and_create_ppt`, `agentic_web_action`, `do_assignment` and others. `/chat` streams them and skips the LLM rephrase.

## Graphify
`graphify explain "run_tool"` · `graphify query "which tools call file_ops"`

<!-- AUTO:BEGIN (scripts/refresh_docs.py) -->
## Files & symbols (auto-generated, line numbers are current)

- `app/services/tools.py` (1217 lines): Jarvis Tool Registry — All callable actions Jarvis can perform.  *(filtered to this feature)*
  L804 _ppt_create() · L819 _research_and_create_ppt() · L845 _ppt_edit() · L857 _ppt_styles() · L1000 _mail_tool() · L1020 _recall_memory_placeholder() · L1025 TOOL_REGISTRY
- `app/services/tool_runner.py` (43 lines): tool_runner.py — Async execution of TOOL_REGISTRY entries for orchestrators
  L19 _call_sync() · L26 run_tool()
- `app/api/tools.py` (32 lines)
  L9 class ToolExecuteRequest · L14 execute_tool()
<!-- AUTO:END -->
