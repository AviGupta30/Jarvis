# agents + tool_runner

> 19 nodes · cohesion 0.13

## Key Concepts

- **run_tool()** (13 connections) — `app/services/tool_runner.py`
- **format_recall_for_prompt()** (10 connections) — `app/services/rag_memory.py`
- **api/tools.py** (9 connections) — `app/api/tools.py`
- **tool_runner.py** (9 connections) — `app/services/tool_runner.py`
- **Agents: DAG executor, linear planner, dynamic skills** (6 connections) — `docs/features/agents.md`
- **execute_tool()** (4 connections) — `app/api/tools.py`
- **ToolExecuteRequest** (3 connections) — `app/api/tools.py`
- **_call_sync()** (2 connections) — `app/services/tool_runner.py`
- **Gotchas** (2 connections) — `docs/features/agents.md`
- **BaseModel** (1 connections)
- **post** (1 connections)
- **Format recalled memory turns into an injectable LLM context block with clear…** (1 connections) — `app/services/rag_memory.py`
- **tool_runner.py — Async execution of TOOL_REGISTRY entries for orchestrators…** (1 connections) — `app/services/tool_runner.py`
- **Run a registry tool and return its output as a string. Raises on unknown tool…** (1 connections) — `app/services/tool_runner.py`
- **agents.md** (1 connections) — `docs/features/agents.md`
- **Data** (1 connections) — `docs/features/agents.md`
- **Files & symbols (auto-generated, line numbers are current)** (1 connections) — `docs/features/agents.md`
- **Graphify** (1 connections) — `docs/features/agents.md`
- **inspect** (1 connections)

## Relationships

- [chat + rag_memory](chat_+_rag_memory.md) (4 shared connections)
- [memory + memory](memory_+_memory.md) (3 shared connections)
- [tools](tools.md) (3 shared connections)
- [assignment_tool + assignment_humanizer](assignment_tool_+_assignment_humanizer.md) (3 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (3 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (2 shared connections)
- [resume_router](resume_router.md) (1 shared connections)
- [persistence + server](persistence_+_server.md) (1 shared connections)
- [main + screen_vision](main_+_screen_vision.md) (1 shared connections)
- [chat-routing + CLAUDE](chat-routing_+_CLAUDE.md) (1 shared connections)

## Source Files

- `app/api/tools.py`
- `app/services/rag_memory.py`
- `app/services/tool_runner.py`
- `docs/features/agents.md`

## Audit Trail

- EXTRACTED: 42 (93%)
- INFERRED: 3 (7%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*