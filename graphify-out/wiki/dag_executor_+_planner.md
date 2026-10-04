# dag_executor + planner

> 35 nodes · cohesion 0.10

## Key Concepts

- **dag_executor.py** (25 connections) — `app/services/dag_executor.py`
- **`/chat` pipeline (`app/api/chat.py:chat_endpoint`, L1066)** (19 connections) — `docs/ARCHITECTURE.md`
- **run_dynamic_skill()** (17 connections) — `app/services/dynamic_skill.py`
- **run_agentic_plan()** (15 connections) — `app/services/planner.py`
- **Jump table for the big files** (15 connections) — `docs/CODEMAP.md`
- **run_dag_plan()** (14 connections) — `app/services/dag_executor.py`
- **get_screen_text_summary()** (13 connections) — `app/services/ui_inspector.py`
- **is_dag_task()** (9 connections) — `app/services/dag_executor.py`
- **_execute_node()** (8 connections) — `app/services/dag_executor.py`
- **DAGNode** (7 connections) — `app/services/dag_executor.py`
- **_run_node_with_retry()** (7 connections) — `app/services/dag_executor.py`
- **_execute_step()** (6 connections) — `app/services/planner.py`
- **_semantic_window_adjust()** (4 connections) — `app/api/chat.py`
- **_resolve_args()** (4 connections) — `app/services/dag_executor.py`
- **_sse()** (4 connections) — `app/services/dag_executor.py`
- **_topological_sort()** (4 connections) — `app/services/dag_executor.py`
- **_call_dag_planner()** (3 connections) — `app/services/dag_executor.py`
- **run_one()** (3 connections) — `app/services/dag_executor.py`
- **_recall_memory_placeholder()** (3 connections) — `app/services/tools.py`
- **Purpose** (3 connections) — `docs/features/agents.md`
- **dag_executor.py — Jarvis DAG-Based Multi-Step Agent Planner…** (1 connections) — `app/services/dag_executor.py`
- **Ask the LLM to produce a DAG plan. Returns parsed dict.** (1 connections) — `app/services/dag_executor.py`
- **Returns execution waves — each wave is a list of node IDs that can run in…** (1 connections) — `app/services/dag_executor.py`
- **Replace $variable references in args with actual stored results.** (1 connections) — `app/services/dag_executor.py`
- **Execute a single DAG node. Returns (success, output_string). Handles DYNAMIC…** (1 connections) — `app/services/dag_executor.py`
- *... and 10 more nodes in this community*

## Relationships

- [chat + youtube_control](chat_+_youtube_control.md) (22 shared connections)
- [dynamic_skill + planner](dynamic_skill_+_planner.md) (13 shared connections)
- [tools](tools.md) (5 shared connections)
- [rag_memory + tool_runner](rag_memory_+_tool_runner.md) (4 shared connections)
- [voice_agent + download_kokoro](voice_agent_+_download_kokoro.md) (3 shared connections)
- [memory](memory.md) (3 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (3 shared connections)
- [ppt_tool](ppt_tool.md) (3 shared connections)
- [message_reader + thread_extractor](message_reader_+_thread_extractor.md) (2 shared connections)
- [safe_executor](safe_executor.md) (2 shared connections)
- [youtube_player](youtube_player.md) (1 shared connections)
- [ppt_image_engine](ppt_image_engine.md) (1 shared connections)

## Source Files

- `app/api/chat.py`
- `app/services/dag_executor.py`
- `app/services/dynamic_skill.py`
- `app/services/planner.py`
- `app/services/tools.py`
- `app/services/ui_inspector.py`
- `docs/ARCHITECTURE.md`
- `docs/CODEMAP.md`
- `docs/features/agents.md`

## Audit Trail

- EXTRACTED: 92 (68%)
- INFERRED: 44 (32%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*