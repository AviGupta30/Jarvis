# dag_executor + dynamic_skill

> 38 nodes · cohesion 0.09

## Key Concepts

- **dag_executor.py** (25 connections) — `app/services/dag_executor.py`
- **run_dynamic_skill()** (17 connections) — `app/services/dynamic_skill.py`
- **run_agentic_plan()** (15 connections) — `app/services/planner.py`
- **Jump table for the big files** (15 connections) — `docs/CODEMAP.md`
- **run_dag_plan()** (14 connections) — `app/services/dag_executor.py`
- **get_screen_text_summary()** (13 connections) — `app/services/ui_inspector.py`
- **_execute_node()** (8 connections) — `app/services/dag_executor.py`
- **DAGNode** (7 connections) — `app/services/dag_executor.py`
- **_run_node_with_retry()** (7 connections) — `app/services/dag_executor.py`
- **_execute_step()** (6 connections) — `app/services/planner.py`
- **_resolve_args()** (4 connections) — `app/services/dag_executor.py`
- **_sse()** (4 connections) — `app/services/dag_executor.py`
- **_topological_sort()** (4 connections) — `app/services/dag_executor.py`
- **_call_dag_planner()** (3 connections) — `app/services/dag_executor.py`
- **run_one()** (3 connections) — `app/services/dag_executor.py`
- **_llm_fix_code()** (3 connections) — `app/services/dynamic_skill.py`
- **_llm_write_code()** (3 connections) — `app/services/dynamic_skill.py`
- **_strip_fences()** (3 connections) — `app/services/dynamic_skill.py`
- **_call_replanner()** (3 connections) — `app/services/planner.py`
- **_recall_memory_placeholder()** (3 connections) — `app/services/tools.py`
- **dag_executor.py — Jarvis DAG-Based Multi-Step Agent Planner…** (1 connections) — `app/services/dag_executor.py`
- **Ask the LLM to produce a DAG plan. Returns parsed dict.** (1 connections) — `app/services/dag_executor.py`
- **Returns execution waves — each wave is a list of node IDs that can run in…** (1 connections) — `app/services/dag_executor.py`
- **Replace $variable references in args with actual stored results.** (1 connections) — `app/services/dag_executor.py`
- **Execute a single DAG node. Returns (success, output_string). Handles DYNAMIC…** (1 connections) — `app/services/dag_executor.py`
- *... and 13 more nodes in this community*

## Relationships

- [assignment_tool + assignment_humanizer](assignment_tool_+_assignment_humanizer.md) (14 shared connections)
- [chat-routing + CLAUDE](chat-routing_+_CLAUDE.md) (10 shared connections)
- [chat + rag_memory](chat_+_rag_memory.md) (9 shared connections)
- [agents + tool_runner](agents_+_tool_runner.md) (3 shared connections)
- [voice_agent + ui_inspector](voice_agent_+_ui_inspector.md) (3 shared connections)
- [safe_executor](safe_executor.md) (3 shared connections)
- [ppt_tool](ppt_tool.md) (3 shared connections)
- [persistence + server](persistence_+_server.md) (2 shared connections)
- [tools](tools.md) (2 shared connections)
- [memory](memory.md) (2 shared connections)
- [ppt_image_engine](ppt_image_engine.md) (1 shared connections)
- [task_ledger + test_task_resumption](task_ledger_+_test_task_resumption.md) (1 shared connections)

## Source Files

- `app/services/dag_executor.py`
- `app/services/dynamic_skill.py`
- `app/services/planner.py`
- `app/services/tools.py`
- `app/services/ui_inspector.py`
- `docs/CODEMAP.md`

## Audit Trail

- EXTRACTED: 94 (80%)
- INFERRED: 24 (20%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*