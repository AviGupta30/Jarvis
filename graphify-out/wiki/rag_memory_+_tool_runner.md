# rag_memory + tool_runner

> 21 nodes · cohesion 0.14

## Key Concepts

- **recall()** (15 connections) — `app/services/rag_memory.py`
- **asyncio** (15 connections)
- **run_tool()** (13 connections) — `app/services/tool_runner.py`
- **test_rag_memory.py** (10 connections) — `scripts/test_rag_memory.py`
- **api/tools.py** (9 connections) — `app/api/tools.py`
- **tool_runner.py** (9 connections) — `app/services/tool_runner.py`
- **get_memory_stats()** (7 connections) — `app/services/rag_memory.py`
- **test()** (6 connections) — `scripts/test_rag_memory.py`
- **smart_filter()** (5 connections) — `app/services/rag_memory.py`
- **execute_tool()** (4 connections) — `app/api/tools.py`
- **ToolExecuteRequest** (3 connections) — `app/api/tools.py`
- **_call_sync()** (2 connections) — `app/services/tool_runner.py`
- **BaseModel** (1 connections)
- **post** (1 connections)
- **Returns True if the turn is meaningful enough to store. Skips trivial single-…** (1 connections) — `app/services/rag_memory.py`
- **Semantically recall the most relevant past conversation turns. Args: query: The…** (1 connections) — `app/services/rag_memory.py`
- **Return statistics about stored long-term memory.** (1 connections) — `app/services/rag_memory.py`
- **tool_runner.py — Async execution of TOOL_REGISTRY entries for orchestrators…** (1 connections) — `app/services/tool_runner.py`
- **Run a registry tool and return its output as a string. Raises on unknown tool…** (1 connections) — `app/services/tool_runner.py`
- **inspect** (1 connections)
- **End-to-end test for Jarvis RAG memory system. Tests: init, smart filter,…** (1 connections) — `scripts/test_rag_memory.py`

## Relationships

- [chat + youtube_control](chat_+_youtube_control.md) (8 shared connections)
- [memory](memory.md) (6 shared connections)
- [mysql_db + rag_memory](mysql_db_+_rag_memory.md) (6 shared connections)
- [task_ledger + rag_memory](task_ledger_+_rag_memory.md) (4 shared connections)
- [dag_executor + planner](dag_executor_+_planner.md) (4 shared connections)
- [tools](tools.md) (3 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (3 shared connections)
- [dynamic_skill + planner](dynamic_skill_+_planner.md) (3 shared connections)
- [voice_agent + download_kokoro](voice_agent_+_download_kokoro.md) (3 shared connections)
- [voice](voice.md) (2 shared connections)
- [resume_router](resume_router.md) (1 shared connections)
- [ppt_router + ppt_tool](ppt_router_+_ppt_tool.md) (1 shared connections)

## Source Files

- `app/api/tools.py`
- `app/services/rag_memory.py`
- `app/services/tool_runner.py`
- `scripts/test_rag_memory.py`

## Audit Trail

- EXTRACTED: 75 (96%)
- INFERRED: 3 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*