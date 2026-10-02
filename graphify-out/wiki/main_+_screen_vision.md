# main + screen_vision

> 16 nodes · cohesion 0.15

## Key Concepts

- **main.py** (27 connections) — `app/main.py`
- **shutdown_event()** (5 connections) — `app/main.py`
- **tripwire_status()** (4 connections) — `app/main.py`
- **stop_background_watcher()** (4 connections) — `app/services/screen_vision.py`
- **get_alerts()** (3 connections) — `app/main.py`
- **get** (3 connections)
- **shutil** (3 connections)
- **test_fastapi.py** (3 connections) — `test_fastapi.py`
- **read_root()** (2 connections) — `app/main.py`
- **Stop watcher, acoustic tripwire, and close DB pool cleanly on server shutdown.** (1 connections) — `app/main.py`
- **Frontend polls this endpoint to receive proactive JARVIS screen alerts. e.g.…** (1 connections) — `app/main.py`
- **Return current acoustic tripwire state for the frontend toggle.** (1 connections) — `app/main.py`
- **Stop the background screen watcher thread cleanly.** (1 connections) — `app/services/screen_vision.py`
- **fastapi_middleware_cors** (1 connections)
- **fastapi_staticfiles** (1 connections)
- **fastapi_testclient** (1 connections)

## Relationships

- [main](main.md) (6 shared connections)
- [main + screen_vision](main_+_screen_vision.md) (3 shared connections)
- [mysql_db + init_rag_memory](mysql_db_+_init_rag_memory.md) (2 shared connections)
- [resume_router](resume_router.md) (2 shared connections)
- [persistence + server](persistence_+_server.md) (1 shared connections)
- [rag_memory + test_rag_memory](rag_memory_+_test_rag_memory.md) (1 shared connections)
- [assignment_tool + assignment_humanizer](assignment_tool_+_assignment_humanizer.md) (1 shared connections)
- [chat + rag_memory](chat_+_rag_memory.md) (1 shared connections)
- [memory + memory](memory_+_memory.md) (1 shared connections)
- [agents + tool_runner](agents_+_tool_runner.md) (1 shared connections)
- [ppt_router + ppt_tool](ppt_router_+_ppt_tool.md) (1 shared connections)
- [voice_agent](voice_agent.md) (1 shared connections)

## Source Files

- `app/main.py`
- `app/services/screen_vision.py`
- `test_fastapi.py`

## Audit Trail

- EXTRACTED: 43 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*