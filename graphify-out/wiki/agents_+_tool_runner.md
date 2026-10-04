# agents + tool_runner

> 14 nodes · cohesion 0.16

## Key Concepts

- **run_tool()** (13 connections) — `app/services/tool_runner.py`
- **format_recall_for_prompt()** (10 connections) — `app/services/rag_memory.py`
- **tool_runner.py** (9 connections) — `app/services/tool_runner.py`
- **Agents: DAG executor, linear planner, dynamic skills** (6 connections) — `docs/features/agents.md`
- **_call_sync()** (2 connections) — `app/services/tool_runner.py`
- **Gotchas** (2 connections) — `docs/features/agents.md`
- **Format recalled memory turns into an injectable LLM context block with clear…** (1 connections) — `app/services/rag_memory.py`
- **tool_runner.py — Async execution of TOOL_REGISTRY entries for orchestrators…** (1 connections) — `app/services/tool_runner.py`
- **Run a registry tool and return its output as a string. Raises on unknown tool…** (1 connections) — `app/services/tool_runner.py`
- **agents.md** (1 connections) — `docs/features/agents.md`
- **Data** (1 connections) — `docs/features/agents.md`
- **Files & symbols (auto-generated, line numbers are current)** (1 connections) — `docs/features/agents.md`
- **Graphify** (1 connections) — `docs/features/agents.md`
- **inspect** (1 connections)

## Relationships

- [planner + dynamic_skill](planner_+_dynamic_skill.md) (4 shared connections)
- [rag_memory + memory](rag_memory_+_memory.md) (4 shared connections)
- [resume_router + tools](resume_router_+_tools.md) (3 shared connections)
- [dag_executor](dag_executor.md) (3 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (2 shared connections)
- [tools](tools.md) (2 shared connections)
- [chat + llm](chat_+_llm.md) (1 shared connections)
- [tool-registry + vector_store](tool-registry_+_vector_store.md) (1 shared connections)

## Source Files

- `app/services/rag_memory.py`
- `app/services/tool_runner.py`
- `docs/features/agents.md`

## Audit Trail

- EXTRACTED: 32 (91%)
- INFERRED: 3 (9%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*