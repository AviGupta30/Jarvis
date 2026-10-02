"""
tool_runner.py — Async execution of TOOL_REGISTRY entries for orchestrators
---------------------------------------------------------------------------
Used by planner.py, dag_executor.py and POST /execute so every non-streaming
caller runs tools the same way:
  - Blocking tools run in a thread pool (never block the event loop)
  - Generator tools (ppt_create, do_assignment, agentic_web_action, ...) are
    fully consumed and their progress chunks joined into one string
  - recall_memory is async (MySQL pool lives on the main loop), so it is
    awaited here instead of being called through the registry
"""

import asyncio
import inspect

from app.services.tools import TOOL_REGISTRY


def _call_sync(tool_name: str, args: dict) -> str:
    result = TOOL_REGISTRY[tool_name](**args)
    if inspect.isgenerator(result):
        return "\n".join(str(chunk) for chunk in result)
    return str(result)


async def run_tool(tool_name: str, args: dict | None = None) -> str:
    """Run a registry tool and return its output as a string. Raises on unknown tool or tool error."""
    args = args or {}

    if tool_name == "recall_memory":
        from app.services.rag_memory import recall, format_recall_for_prompt
        query = args.get("query", "")
        recalled = await recall(query, top_k=10, min_score=0.20)
        if not recalled:
            return "No relevant memories found."
        return format_recall_for_prompt(recalled, query=query)

    if tool_name not in TOOL_REGISTRY:
        raise KeyError(f"Unknown tool: {tool_name}")

    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, _call_sync, tool_name, args)
