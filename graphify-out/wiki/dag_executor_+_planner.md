# dag_executor + planner

> 50 nodes · cohesion 0.07

## Key Concepts

- **dag_executor.py** (25 connections) — `app/services/dag_executor.py`
- **planner.py** (19 connections) — `app/services/planner.py`
- **`/chat` pipeline (`app/api/chat.py:chat_endpoint`, L1066)** (19 connections) — `docs/ARCHITECTURE.md`
- **run_dynamic_skill()** (17 connections) — `app/services/dynamic_skill.py`
- **run_agentic_plan()** (15 connections) — `app/services/planner.py`
- **Jump table for the big files** (15 connections) — `docs/CODEMAP.md`
- **run_dag_plan()** (14 connections) — `app/services/dag_executor.py`
- **get_screen_text_summary()** (13 connections) — `app/services/ui_inspector.py`
- **Flow (`chat_endpoint`, order matters, first hit wins)** (12 connections) — `docs/features/chat-routing.md`
- **is_complex_task()** (10 connections) — `app/services/planner.py`
- **is_dag_task()** (9 connections) — `app/services/dag_executor.py`
- **_execute_node()** (8 connections) — `app/services/dag_executor.py`
- **DAGNode** (7 connections) — `app/services/dag_executor.py`
- **_run_node_with_retry()** (7 connections) — `app/services/dag_executor.py`
- **_execute_step()** (6 connections) — `app/services/planner.py`
- **/chat request flow (short)** (5 connections) — `CLAUDE.md`
- **_semantic_window_adjust()** (4 connections) — `app/api/chat.py`
- **_resolve_args()** (4 connections) — `app/services/dag_executor.py`
- **_sse()** (4 connections) — `app/services/dag_executor.py`
- **_topological_sort()** (4 connections) — `app/services/dag_executor.py`
- **_call_planner()** (4 connections) — `app/services/planner.py`
- **_call_dag_planner()** (3 connections) — `app/services/dag_executor.py`
- **run_one()** (3 connections) — `app/services/dag_executor.py`
- **_llm_fix_code()** (3 connections) — `app/services/dynamic_skill.py`
- **_llm_write_code()** (3 connections) — `app/services/dynamic_skill.py`
- *... and 25 more nodes in this community*

## Relationships

- [chat](chat.md) (18 shared connections)
- [assignment_tool + safe_executor](assignment_tool_+_safe_executor.md) (15 shared connections)
- [youtube_control](youtube_control.md) (10 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (7 shared connections)
- [agents + tool_runner](agents_+_tool_runner.md) (6 shared connections)
- [ui_inspector + lru](ui_inspector_+_lru.md) (5 shared connections)
- [tools](tools.md) (3 shared connections)
- [task_ledger](task_ledger.md) (3 shared connections)
- [memory](memory.md) (2 shared connections)
- [rag_memory + memory](rag_memory_+_memory.md) (2 shared connections)
- [file_ops](file_ops.md) (2 shared connections)
- [CODEMAP + chat-routing](CODEMAP_+_chat-routing.md) (2 shared connections)

## Source Files

- `CLAUDE.md`
- `app/api/chat.py`
- `app/services/dag_executor.py`
- `app/services/dynamic_skill.py`
- `app/services/planner.py`
- `app/services/tools.py`
- `app/services/ui_inspector.py`
- `docs/ARCHITECTURE.md`
- `docs/CODEMAP.md`
- `docs/features/chat-routing.md`

## Audit Trail

- EXTRACTED: 121 (68%)
- INFERRED: 56 (32%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*