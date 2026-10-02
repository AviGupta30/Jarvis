# main + screen_vision

> 22 nodes · cohesion 0.11

## Key Concepts

- **main.py** (27 connections) — `app/main.py`
- **startup_event()** (8 connections) — `app/main.py`
- **start_background_watcher()** (6 connections) — `app/services/screen_vision.py`
- **shutdown_event()** (5 connections) — `app/main.py`
- **tripwire_status()** (4 connections) — `app/main.py`
- **stop_background_watcher()** (4 connections) — `app/services/screen_vision.py`
- **get_alerts()** (3 connections) — `app/main.py`
- **_on_screen_alert()** (3 connections) — `app/main.py`
- **get** (3 connections)
- **shutil** (3 connections)
- **test_fastapi.py** (3 connections) — `test_fastapi.py`
- **read_root()** (2 connections) — `app/main.py`
- **Stop watcher, acoustic tripwire, and close DB pool cleanly on server shutdown.** (1 connections) — `app/main.py`
- **Frontend polls this endpoint to receive proactive JARVIS screen alerts. e.g.…** (1 connections) — `app/main.py`
- **Return current acoustic tripwire state for the frontend toggle.** (1 connections) — `app/main.py`
- **Callback fired by the background watcher when something notable is detected.…** (1 connections) — `app/main.py`
- **Start background screen watcher and RAG memory system when the server boots.** (1 connections) — `app/main.py`
- **Start the passive background screen watcher. Args: callback: Function called…** (1 connections) — `app/services/screen_vision.py`
- **Stop the background screen watcher thread cleanly.** (1 connections) — `app/services/screen_vision.py`
- **fastapi_middleware_cors** (1 connections)
- **fastapi_staticfiles** (1 connections)
- **fastapi_testclient** (1 connections)

## Relationships

- [main](main.md) (6 shared connections)
- [mysql_db + rag_memory](mysql_db_+_rag_memory.md) (4 shared connections)
- [ppt_router + resume_router](ppt_router_+_resume_router.md) (3 shared connections)
- [rag_memory + memory](rag_memory_+_memory.md) (2 shared connections)
- [voice + voice_agent](voice_+_voice_agent.md) (2 shared connections)
- [tools](tools.md) (2 shared connections)
- [voice_agent + acoustic_tripwire](voice_agent_+_acoustic_tripwire.md) (2 shared connections)
- [syllabus_auditor + syllabus-auditor](syllabus_auditor_+_syllabus-auditor.md) (1 shared connections)
- [assignment_tool + safe_executor](assignment_tool_+_safe_executor.md) (1 shared connections)
- [chat](chat.md) (1 shared connections)
- [agents + tool_runner](agents_+_tool_runner.md) (1 shared connections)
- [screen_vision](screen_vision.md) (1 shared connections)

## Source Files

- `app/main.py`
- `app/services/screen_vision.py`
- `test_fastapi.py`

## Audit Trail

- EXTRACTED: 50 (91%)
- INFERRED: 5 (9%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*