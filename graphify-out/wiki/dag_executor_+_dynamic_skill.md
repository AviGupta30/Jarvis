# dag_executor + dynamic_skill

> 57 nodes · cohesion 0.06

## Key Concepts

- **dag_executor.py** (25 connections) — `app/services/dag_executor.py`
- **config.py** (20 connections) — `app/core/config.py`
- **planner.py** (19 connections) — `app/services/planner.py`
- **dynamic_skill.py** (18 connections) — `app/services/dynamic_skill.py`
- **ui_inspector.py** (18 connections) — `app/services/ui_inspector.py`
- **run_dynamic_skill()** (17 connections) — `app/services/dynamic_skill.py`
- **run_agentic_plan()** (15 connections) — `app/services/planner.py`
- **Jump table for the big files** (15 connections) — `docs/CODEMAP.md`
- **run_dag_plan()** (14 connections) — `app/services/dag_executor.py`
- **get_screen_text_summary()** (13 connections) — `app/services/ui_inspector.py`
- **execute_safe()** (11 connections) — `app/services/safe_executor.py`
- **_execute_node()** (8 connections) — `app/services/dag_executor.py`
- **DAGNode** (7 connections) — `app/services/dag_executor.py`
- **_run_node_with_retry()** (7 connections) — `app/services/dag_executor.py`
- **find_skill()** (6 connections) — `app/memory/memory.py`
- **save_skill()** (6 connections) — `app/memory/memory.py`
- **_execute_step()** (6 connections) — `app/services/planner.py`
- **debug_ui_tree()** (5 connections) — `app/services/ui_inspector.py`
- **_resolve_args()** (4 connections) — `app/services/dag_executor.py`
- **_sse()** (4 connections) — `app/services/dag_executor.py`
- **_topological_sort()** (4 connections) — `app/services/dag_executor.py`
- **_call_planner()** (4 connections) — `app/services/planner.py`
- **dump_spotify.py** (4 connections) — `dump_spotify.py`
- **_call_dag_planner()** (3 connections) — `app/services/dag_executor.py`
- **run_one()** (3 connections) — `app/services/dag_executor.py`
- *... and 32 more nodes in this community*

## Relationships

- [chat + llm](chat_+_llm.md) (15 shared connections)
- [chat + chat-routing](chat_+_chat-routing.md) (11 shared connections)
- [tools](tools.md) (10 shared connections)
- [rag_memory + mysql_db](rag_memory_+_mysql_db.md) (8 shared connections)
- [safe_executor](safe_executor.md) (7 shared connections)
- [benchmark + server](benchmark_+_server.md) (6 shared connections)
- [memory](memory.md) (5 shared connections)
- [nlp_extractor + download_kokoro](nlp_extractor_+_download_kokoro.md) (5 shared connections)
- [ppt_tool](ppt_tool.md) (4 shared connections)
- [screen_vision + screen_reader](screen_vision_+_screen_reader.md) (4 shared connections)
- [social_content_manager + tools](social_content_manager_+_tools.md) (3 shared connections)
- [chat + tools](chat_+_tools.md) (3 shared connections)

## Source Files

- `app/core/config.py`
- `app/memory/memory.py`
- `app/services/dag_executor.py`
- `app/services/dynamic_skill.py`
- `app/services/planner.py`
- `app/services/safe_executor.py`
- `app/services/tools.py`
- `app/services/ui_inspector.py`
- `docs/CODEMAP.md`
- `dump_spotify.py`

## Audit Trail

- EXTRACTED: 172 (86%)
- INFERRED: 28 (14%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*