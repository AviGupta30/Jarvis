# dag_executor + dynamic_skill

> 35 nodes · cohesion 0.09

## Key Concepts

- **dag_executor.py** (25 connections) — `app/services/dag_executor.py`
- **run_dynamic_skill()** (17 connections) — `app/services/dynamic_skill.py`
- **run_agentic_plan()** (15 connections) — `app/services/planner.py`
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
- **dag_executor.py — Jarvis DAG-Based Multi-Step Agent Planner…** (1 connections) — `app/services/dag_executor.py`
- **Ask the LLM to produce a DAG plan. Returns parsed dict.** (1 connections) — `app/services/dag_executor.py`
- **Returns execution waves — each wave is a list of node IDs that can run in…** (1 connections) — `app/services/dag_executor.py`
- **Replace $variable references in args with actual stored results.** (1 connections) — `app/services/dag_executor.py`
- **Execute a single DAG node. Returns (success, output_string). Handles DYNAMIC…** (1 connections) — `app/services/dag_executor.py`
- **Run a node with retry logic and optional fallback tool. Returns (success,…** (1 connections) — `app/services/dag_executor.py`
- **Main DAG execution entry point. Yields structured SSE JSON strings: data:…** (1 connections) — `app/services/dag_executor.py`
- *... and 10 more nodes in this community*

## Relationships

- [safe_executor + ui_inspector](safe_executor_+_ui_inspector.md) (11 shared connections)
- [smart_navigator + rag_memory](smart_navigator_+_rag_memory.md) (10 shared connections)
- [chat-routing + chat](chat-routing_+_chat.md) (9 shared connections)
- [chat + llm](chat_+_llm.md) (8 shared connections)
- [agents + tool_runner](agents_+_tool_runner.md) (3 shared connections)
- [memory](memory.md) (2 shared connections)
- [memory + rag_memory](memory_+_rag_memory.md) (1 shared connections)
- [screen_vision + screen_reader](screen_vision_+_screen_reader.md) (1 shared connections)
- [ppt_image_engine](ppt_image_engine.md) (1 shared connections)
- [refresh_docs](refresh_docs.md) (1 shared connections)
- [tools](tools.md) (1 shared connections)
- [chat + KNOWN_ISSUES](chat_+_KNOWN_ISSUES.md) (1 shared connections)

## Source Files

- `app/services/dag_executor.py`
- `app/services/dynamic_skill.py`
- `app/services/planner.py`
- `app/services/ui_inspector.py`

## Audit Trail

- EXTRACTED: 92 (88%)
- INFERRED: 12 (12%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*