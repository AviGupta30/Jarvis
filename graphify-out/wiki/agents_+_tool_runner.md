# agents + tool_runner

> 20 nodes · cohesion 0.13

## Key Concepts

- **run_tool()** (13 connections) — `app/services/tool_runner.py`
- **format_recall_for_prompt()** (10 connections) — `app/services/rag_memory.py`
- **api/tools.py** (9 connections) — `app/api/tools.py`
- **tool_runner.py** (9 connections) — `app/services/tool_runner.py`
- **Agents: DAG executor, linear planner, dynamic skills** (6 connections) — `docs/features/agents.md`
- **execute_tool()** (4 connections) — `app/api/tools.py`
- **ToolExecuteRequest** (3 connections) — `app/api/tools.py`
- **Purpose** (3 connections) — `docs/features/agents.md`
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

- [dag_executor + planner](dag_executor_+_planner.md) (6 shared connections)
- [rag_memory + memory](rag_memory_+_memory.md) (4 shared connections)
- [tools](tools.md) (3 shared connections)
- [chat](chat.md) (3 shared connections)
- [ppt_router + resume_router](ppt_router_+_resume_router.md) (2 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (2 shared connections)
- [ui_inspector + lru](ui_inspector_+_lru.md) (1 shared connections)
- [main + screen_vision](main_+_screen_vision.md) (1 shared connections)
- [syllabus_auditor + syllabus-auditor](syllabus_auditor_+_syllabus-auditor.md) (1 shared connections)

## Source Files

- `app/api/tools.py`
- `app/services/rag_memory.py`
- `app/services/tool_runner.py`
- `docs/features/agents.md`

## Audit Trail

- EXTRACTED: 42 (89%)
- INFERRED: 5 (11%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*