# agents + tool_runner

> 17 nodes · cohesion 0.15

## Key Concepts

- **run_tool()** (13 connections) — `app/services/tool_runner.py`
- **api/tools.py** (9 connections) — `app/api/tools.py`
- **tool_runner.py** (9 connections) — `app/services/tool_runner.py`
- **Agents: DAG executor, linear planner, dynamic skills** (6 connections) — `docs/features/agents.md`
- **execute_tool()** (4 connections) — `app/api/tools.py`
- **ToolExecuteRequest** (3 connections) — `app/api/tools.py`
- **_call_sync()** (2 connections) — `app/services/tool_runner.py`
- **Gotchas** (2 connections) — `docs/features/agents.md`
- **BaseModel** (1 connections)
- **post** (1 connections)
- **tool_runner.py — Async execution of TOOL_REGISTRY entries for orchestrators…** (1 connections) — `app/services/tool_runner.py`
- **Run a registry tool and return its output as a string. Raises on unknown tool…** (1 connections) — `app/services/tool_runner.py`
- **agents.md** (1 connections) — `docs/features/agents.md`
- **Data** (1 connections) — `docs/features/agents.md`
- **Files & symbols (auto-generated, line numbers are current)** (1 connections) — `docs/features/agents.md`
- **Graphify** (1 connections) — `docs/features/agents.md`
- **inspect** (1 connections)

## Relationships

- [dag_executor + planner](dag_executor_+_planner.md) (5 shared connections)
- [rag_memory + memory](rag_memory_+_memory.md) (4 shared connections)
- [tools](tools.md) (3 shared connections)
- [resume_builder](resume_builder.md) (1 shared connections)
- [ppt_router + ppt_tool](ppt_router_+_ppt_tool.md) (1 shared connections)
- [reply_generator](reply_generator.md) (1 shared connections)
- [main](main.md) (1 shared connections)
- [chat + llm](chat_+_llm.md) (1 shared connections)

## Source Files

- `app/api/tools.py`
- `app/services/tool_runner.py`
- `docs/features/agents.md`

## Audit Trail

- EXTRACTED: 34 (92%)
- INFERRED: 3 (8%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*