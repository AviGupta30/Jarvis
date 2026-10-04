# dag_executor + dynamic_skill

> 61 nodes · cohesion 0.06

## Key Concepts

- **dag_executor.py** (25 connections) — `app/services/dag_executor.py`
- **config.py** (20 connections) — `app/core/config.py`
- **planner.py** (19 connections) — `app/services/planner.py`
- **`/chat` pipeline (`app/api/chat.py:chat_endpoint`, L1066)** (19 connections) — `docs/ARCHITECTURE.md`
- **dynamic_skill.py** (18 connections) — `app/services/dynamic_skill.py`
- **ui_inspector.py** (18 connections) — `app/services/ui_inspector.py`
- **run_dynamic_skill()** (17 connections) — `app/services/dynamic_skill.py`
- **run_agentic_plan()** (15 connections) — `app/services/planner.py`
- **asyncio** (15 connections)
- **Jump table for the big files** (15 connections) — `docs/CODEMAP.md`
- **run_dag_plan()** (14 connections) — `app/services/dag_executor.py`
- **logging** (14 connections)
- **get_screen_text_summary()** (13 connections) — `app/services/ui_inspector.py`
- **execute_safe()** (11 connections) — `app/services/safe_executor.py`
- **groq** (11 connections)
- **get_active_window_info()** (10 connections) — `app/services/ui_inspector.py`
- **_execute_node()** (8 connections) — `app/services/dag_executor.py`
- **DAGNode** (7 connections) — `app/services/dag_executor.py`
- **_run_node_with_retry()** (7 connections) — `app/services/dag_executor.py`
- **find_skill()** (6 connections) — `app/memory/memory.py`
- **save_skill()** (6 connections) — `app/memory/memory.py`
- **_execute_step()** (6 connections) — `app/services/planner.py`
- **click_ui_element()** (6 connections) — `app/services/ui_inspector.py`
- **_semantic_window_adjust()** (4 connections) — `app/api/chat.py`
- **_resolve_args()** (4 connections) — `app/services/dag_executor.py`
- *... and 36 more nodes in this community*

## Relationships

- [chat + youtube_control](chat_+_youtube_control.md) (28 shared connections)
- [safe_executor + refresh_docs](safe_executor_+_refresh_docs.md) (11 shared connections)
- [assignment_humanizer + task_ledger](assignment_humanizer_+_task_ledger.md) (9 shared connections)
- [memory + rag_memory](memory_+_rag_memory.md) (7 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (6 shared connections)
- [ppt_tool](ppt_tool.md) (6 shared connections)
- [screen_vision + screen_reader](screen_vision_+_screen_reader.md) (6 shared connections)
- [tools](tools.md) (6 shared connections)
- [memory](memory.md) (5 shared connections)
- [tools + ui_inspector](tools_+_ui_inspector.md) (5 shared connections)
- [social_content_manager + content-tools](social_content_manager_+_content-tools.md) (4 shared connections)
- [chat-routing + chat](chat-routing_+_chat.md) (3 shared connections)

## Source Files

- `app/api/chat.py`
- `app/core/config.py`
- `app/memory/memory.py`
- `app/services/dag_executor.py`
- `app/services/dynamic_skill.py`
- `app/services/planner.py`
- `app/services/safe_executor.py`
- `app/services/ui_inspector.py`
- `docs/ARCHITECTURE.md`
- `docs/CODEMAP.md`

## Audit Trail

- EXTRACTED: 209 (83%)
- INFERRED: 44 (17%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*