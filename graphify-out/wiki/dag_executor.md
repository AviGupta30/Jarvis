# dag_executor

> 26 nodes · cohesion 0.13

## Key Concepts

- **dag_executor.py** (25 connections) — `app/services/dag_executor.py`
- **`/chat` pipeline (`app/api/chat.py:chat_endpoint`, L1066)** (19 connections) — `docs/ARCHITECTURE.md`
- **Jump table for the big files** (15 connections) — `docs/CODEMAP.md`
- **run_dag_plan()** (14 connections) — `app/services/dag_executor.py`
- **is_dag_task()** (9 connections) — `app/services/dag_executor.py`
- **_execute_node()** (8 connections) — `app/services/dag_executor.py`
- **DAGNode** (7 connections) — `app/services/dag_executor.py`
- **_run_node_with_retry()** (7 connections) — `app/services/dag_executor.py`
- **_semantic_window_adjust()** (4 connections) — `app/api/chat.py`
- **_resolve_args()** (4 connections) — `app/services/dag_executor.py`
- **_sse()** (4 connections) — `app/services/dag_executor.py`
- **_topological_sort()** (4 connections) — `app/services/dag_executor.py`
- **detect_note_intent()** (3 connections) — `app/api/chat.py`
- **_call_dag_planner()** (3 connections) — `app/services/dag_executor.py`
- **run_one()** (3 connections) — `app/services/dag_executor.py`
- **Purpose** (3 connections) — `docs/features/agents.md`
- **dag_executor.py — Jarvis DAG-Based Multi-Step Agent Planner…** (1 connections) — `app/services/dag_executor.py`
- **Ask the LLM to produce a DAG plan. Returns parsed dict.** (1 connections) — `app/services/dag_executor.py`
- **Returns execution waves — each wave is a list of node IDs that can run in…** (1 connections) — `app/services/dag_executor.py`
- **Replace $variable references in args with actual stored results.** (1 connections) — `app/services/dag_executor.py`
- **Execute a single DAG node. Returns (success, output_string). Handles DYNAMIC…** (1 connections) — `app/services/dag_executor.py`
- **Run a node with retry logic and optional fallback tool. Returns (success,…** (1 connections) — `app/services/dag_executor.py`
- **Returns True when the user's request requires a multi-branch DAG plan. More…** (1 connections) — `app/services/dag_executor.py`
- **Main DAG execution entry point. Yields structured SSE JSON strings: data:…** (1 connections) — `app/services/dag_executor.py`
- **Represents a single task node in the execution graph.** (1 connections) — `app/services/dag_executor.py`
- *... and 1 more nodes in this community*

## Relationships

- [planner + dynamic_skill](planner_+_dynamic_skill.md) (20 shared connections)
- [chat + llm](chat_+_llm.md) (4 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (4 shared connections)
- [chat-routing + chat](chat-routing_+_chat.md) (3 shared connections)
- [tools](tools.md) (3 shared connections)
- [agents + tool_runner](agents_+_tool_runner.md) (3 shared connections)
- [benchmark + download_kokoro](benchmark_+_download_kokoro.md) (3 shared connections)
- [ppt_tool](ppt_tool.md) (3 shared connections)
- [tool-registry + vector_store](tool-registry_+_vector_store.md) (2 shared connections)
- [server + persistence](server_+_persistence.md) (1 shared connections)
- [ppt_image_engine](ppt_image_engine.md) (1 shared connections)
- [style_profiler + reply_generator](style_profiler_+_reply_generator.md) (1 shared connections)

## Source Files

- `app/api/chat.py`
- `app/services/dag_executor.py`
- `docs/ARCHITECTURE.md`
- `docs/CODEMAP.md`
- `docs/features/agents.md`

## Audit Trail

- EXTRACTED: 63 (63%)
- INFERRED: 37 (37%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*