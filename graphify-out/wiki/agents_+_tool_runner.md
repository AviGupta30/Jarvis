# agents + tool_runner

> 23 nodes · cohesion 0.11

## Key Concepts

- **recall()** (15 connections) — `app/services/rag_memory.py`
- **run_tool()** (13 connections) — `app/services/tool_runner.py`
- **format_recall_for_prompt()** (10 connections) — `app/services/rag_memory.py`
- **api/tools.py** (9 connections) — `app/api/tools.py`
- **tool_runner.py** (9 connections) — `app/services/tool_runner.py`
- **Agents: DAG executor, linear planner, dynamic skills** (6 connections) — `docs/features/agents.md`
- **fastapi** (6 connections)
- **execute_tool()** (4 connections) — `app/api/tools.py`
- **pydantic** (4 connections)
- **ToolExecuteRequest** (3 connections) — `app/api/tools.py`
- **_call_sync()** (2 connections) — `app/services/tool_runner.py`
- **Gotchas** (2 connections) — `docs/features/agents.md`
- **BaseModel** (1 connections)
- **post** (1 connections)
- **Semantically recall the most relevant past conversation turns. Args: query: The…** (1 connections) — `app/services/rag_memory.py`
- **Format recalled memory turns into an injectable LLM context block with clear…** (1 connections) — `app/services/rag_memory.py`
- **tool_runner.py — Async execution of TOOL_REGISTRY entries for orchestrators…** (1 connections) — `app/services/tool_runner.py`
- **Run a registry tool and return its output as a string. Raises on unknown tool…** (1 connections) — `app/services/tool_runner.py`
- **agents.md** (1 connections) — `docs/features/agents.md`
- **Data** (1 connections) — `docs/features/agents.md`
- **Files & symbols (auto-generated, line numbers are current)** (1 connections) — `docs/features/agents.md`
- **Graphify** (1 connections) — `docs/features/agents.md`
- **inspect** (1 connections)

## Relationships

- [memory + rag_memory](memory_+_rag_memory.md) (9 shared connections)
- [chat + llm](chat_+_llm.md) (6 shared connections)
- [smart_navigator + rag_memory](smart_navigator_+_rag_memory.md) (4 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (4 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (3 shared connections)
- [tools](tools.md) (2 shared connections)
- [main](main.md) (2 shared connections)
- [tool-registry + memory](tool-registry_+_memory.md) (2 shared connections)
- [ppt_router](ppt_router.md) (2 shared connections)
- [mysql_db + rag_memory](mysql_db_+_rag_memory.md) (1 shared connections)
- [tools + whatsapp_smart](tools_+_whatsapp_smart.md) (1 shared connections)
- [chat-routing + chat](chat-routing_+_chat.md) (1 shared connections)

## Source Files

- `app/api/tools.py`
- `app/services/rag_memory.py`
- `app/services/tool_runner.py`
- `docs/features/agents.md`

## Audit Trail

- EXTRACTED: 63 (95%)
- INFERRED: 3 (5%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*