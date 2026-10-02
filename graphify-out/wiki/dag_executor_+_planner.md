# dag_executor + planner

> 56 nodes · cohesion 0.07

## Key Concepts

- **dag_executor.py** (25 connections) — `app/services/dag_executor.py`
- **config.py** (19 connections) — `app/core/config.py`
- **planner.py** (19 connections) — `app/services/planner.py`
- **`/chat` pipeline (`app/api/chat.py:chat_endpoint`, L1066)** (19 connections) — `docs/ARCHITECTURE.md`
- **dynamic_skill.py** (18 connections) — `app/services/dynamic_skill.py`
- **run_dynamic_skill()** (17 connections) — `app/services/dynamic_skill.py`
- **run_agentic_plan()** (15 connections) — `app/services/planner.py`
- **Jump table for the big files** (15 connections) — `docs/CODEMAP.md`
- **run_dag_plan()** (14 connections) — `app/services/dag_executor.py`
- **get_screen_text_summary()** (13 connections) — `app/services/ui_inspector.py`
- **Flow (`chat_endpoint`, order matters, first hit wins)** (12 connections) — `docs/features/chat-routing.md`
- **read_file()** (11 connections) — `app/services/file_ops.py`
- **groq** (11 connections)
- **is_complex_task()** (10 connections) — `app/services/planner.py`
- **is_dag_task()** (9 connections) — `app/services/dag_executor.py`
- **_execute_node()** (8 connections) — `app/services/dag_executor.py`
- **DAGNode** (7 connections) — `app/services/dag_executor.py`
- **_run_node_with_retry()** (7 connections) — `app/services/dag_executor.py`
- **_execute_step()** (6 connections) — `app/services/planner.py`
- **_semantic_window_adjust()** (4 connections) — `app/api/chat.py`
- **_resolve_args()** (4 connections) — `app/services/dag_executor.py`
- **_sse()** (4 connections) — `app/services/dag_executor.py`
- **_topological_sort()** (4 connections) — `app/services/dag_executor.py`
- **_call_planner()** (4 connections) — `app/services/planner.py`
- **_call_dag_planner()** (3 connections) — `app/services/dag_executor.py`
- *... and 31 more nodes in this community*

## Relationships

- [chat + llm](chat_+_llm.md) (24 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (8 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (8 shared connections)
- [task_ledger + test_task_resumption](task_ledger_+_test_task_resumption.md) (7 shared connections)
- [ppt_tool](ppt_tool.md) (5 shared connections)
- [agents + tool_runner](agents_+_tool_runner.md) (5 shared connections)
- [safe_executor](safe_executor.md) (5 shared connections)
- [tools](tools.md) (4 shared connections)
- [memory](memory.md) (4 shared connections)
- [rag_memory + memory](rag_memory_+_memory.md) (3 shared connections)
- [ui_inspector + tools](ui_inspector_+_tools.md) (3 shared connections)
- [file_ops](file_ops.md) (3 shared connections)

## Source Files

- `app/api/chat.py`
- `app/core/config.py`
- `app/services/dag_executor.py`
- `app/services/dynamic_skill.py`
- `app/services/file_ops.py`
- `app/services/planner.py`
- `app/services/ui_inspector.py`
- `docs/ARCHITECTURE.md`
- `docs/CODEMAP.md`
- `docs/features/agents.md`
- `docs/features/chat-routing.md`

## Audit Trail

- EXTRACTED: 164 (75%)
- INFERRED: 54 (25%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*