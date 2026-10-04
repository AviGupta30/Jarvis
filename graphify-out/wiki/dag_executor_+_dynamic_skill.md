# dag_executor + dynamic_skill

> 54 nodes · cohesion 0.07

## Key Concepts

- **dag_executor.py** (25 connections) — `app/services/dag_executor.py`
- **config.py** (20 connections) — `app/core/config.py`
- **planner.py** (19 connections) — `app/services/planner.py`
- **dynamic_skill.py** (18 connections) — `app/services/dynamic_skill.py`
- **run_dynamic_skill()** (17 connections) — `app/services/dynamic_skill.py`
- **run_agentic_plan()** (15 connections) — `app/services/planner.py`
- **asyncio** (15 connections)
- **Jump table for the big files** (15 connections) — `docs/CODEMAP.md`
- **run_dag_plan()** (14 connections) — `app/services/dag_executor.py`
- **get_screen_text_summary()** (13 connections) — `app/services/ui_inspector.py`
- **execute_safe()** (11 connections) — `app/services/safe_executor.py`
- **groq** (11 connections)
- **_execute_node()** (8 connections) — `app/services/dag_executor.py`
- **get_task_ledger_for_prompt()** (8 connections) — `app/services/task_ledger.py`
- **DAGNode** (7 connections) — `app/services/dag_executor.py`
- **_run_node_with_retry()** (7 connections) — `app/services/dag_executor.py`
- **find_skill()** (6 connections) — `app/memory/memory.py`
- **_execute_step()** (6 connections) — `app/services/planner.py`
- **_resolve_args()** (4 connections) — `app/services/dag_executor.py`
- **_sse()** (4 connections) — `app/services/dag_executor.py`
- **_topological_sort()** (4 connections) — `app/services/dag_executor.py`
- **_call_planner()** (4 connections) — `app/services/planner.py`
- **_call_dag_planner()** (3 connections) — `app/services/dag_executor.py`
- **run_one()** (3 connections) — `app/services/dag_executor.py`
- **_llm_fix_code()** (3 connections) — `app/services/dynamic_skill.py`
- *... and 29 more nodes in this community*

## Relationships

- [chat + youtube_control](chat_+_youtube_control.md) (15 shared connections)
- [jarvis_overlay + prompt_overlay](jarvis_overlay_+_prompt_overlay.md) (7 shared connections)
- [safe_executor](safe_executor.md) (7 shared connections)
- [ppt_tool](ppt_tool.md) (6 shared connections)
- [memory + tool_runner](memory_+_tool_runner.md) (6 shared connections)
- [tools + ui_inspector](tools_+_ui_inspector.md) (6 shared connections)
- [chat](chat.md) (6 shared connections)
- [server + persistence](server_+_persistence.md) (5 shared connections)
- [rag_memory + mysql_db](rag_memory_+_mysql_db.md) (4 shared connections)
- [memory + tools](memory_+_tools.md) (4 shared connections)
- [llm-personality + ARCHITECTURE](llm-personality_+_ARCHITECTURE.md) (4 shared connections)
- [llm + context_classifier](llm_+_context_classifier.md) (3 shared connections)

## Source Files

- `app/core/config.py`
- `app/memory/memory.py`
- `app/services/dag_executor.py`
- `app/services/dynamic_skill.py`
- `app/services/planner.py`
- `app/services/safe_executor.py`
- `app/services/task_ledger.py`
- `app/services/ui_inspector.py`
- `docs/CODEMAP.md`
- `test_exec.py`

## Audit Trail

- EXTRACTED: 174 (87%)
- INFERRED: 27 (13%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*