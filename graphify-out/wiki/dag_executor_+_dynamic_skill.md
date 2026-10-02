# dag_executor + dynamic_skill

> 50 nodes · cohesion 0.07

## Key Concepts

- **dag_executor.py** (25 connections) — `app/services/dag_executor.py`
- **config.py** (19 connections) — `app/core/config.py`
- **planner.py** (19 connections) — `app/services/planner.py`
- **dynamic_skill.py** (18 connections) — `app/services/dynamic_skill.py`
- **run_dynamic_skill()** (17 connections) — `app/services/dynamic_skill.py`
- **run_agentic_plan()** (15 connections) — `app/services/planner.py`
- **asyncio** (15 connections)
- **run_dag_plan()** (14 connections) — `app/services/dag_executor.py`
- **run_tool()** (13 connections) — `app/services/tool_runner.py`
- **get_screen_text_summary()** (13 connections) — `app/services/ui_inspector.py`
- **groq** (11 connections)
- **_execute_node()** (8 connections) — `app/services/dag_executor.py`
- **get_task_ledger_for_prompt()** (8 connections) — `app/services/task_ledger.py`
- **DAGNode** (7 connections) — `app/services/dag_executor.py`
- **_run_node_with_retry()** (7 connections) — `app/services/dag_executor.py`
- **_execute_step()** (6 connections) — `app/services/planner.py`
- **_resolve_args()** (4 connections) — `app/services/dag_executor.py`
- **_sse()** (4 connections) — `app/services/dag_executor.py`
- **_topological_sort()** (4 connections) — `app/services/dag_executor.py`
- **_call_planner()** (4 connections) — `app/services/planner.py`
- **_call_dag_planner()** (3 connections) — `app/services/dag_executor.py`
- **run_one()** (3 connections) — `app/services/dag_executor.py`
- **_llm_fix_code()** (3 connections) — `app/services/dynamic_skill.py`
- **_llm_write_code()** (3 connections) — `app/services/dynamic_skill.py`
- **_strip_fences()** (3 connections) — `app/services/dynamic_skill.py`
- *... and 25 more nodes in this community*

## Relationships

- [chat + youtube_control](chat_+_youtube_control.md) (25 shared connections)
- [social_content_manager + ui_inspector](social_content_manager_+_ui_inspector.md) (14 shared connections)
- [safe_executor + ui_inspector](safe_executor_+_ui_inspector.md) (6 shared connections)
- [tools](tools.md) (5 shared connections)
- [memory](memory.md) (5 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (3 shared connections)
- [ppt_tool](ppt_tool.md) (3 shared connections)
- [task_ledger + test_task_resumption](task_ledger_+_test_task_resumption.md) (3 shared connections)
- [rag_memory](rag_memory.md) (3 shared connections)
- [tool_runner](tool_runner.md) (3 shared connections)
- [mysql_db + rag_memory](mysql_db_+_rag_memory.md) (2 shared connections)
- [assignment_answers](assignment_answers.md) (2 shared connections)

## Source Files

- `app/core/config.py`
- `app/services/dag_executor.py`
- `app/services/dynamic_skill.py`
- `app/services/planner.py`
- `app/services/task_ledger.py`
- `app/services/tool_runner.py`
- `app/services/ui_inspector.py`

## Audit Trail

- EXTRACTED: 170 (92%)
- INFERRED: 15 (8%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*