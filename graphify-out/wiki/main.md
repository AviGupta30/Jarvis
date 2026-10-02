# main

> 25 nodes · cohesion 0.11

## Key Concepts

- **main.py** (27 connections) — `app/main.py`
- **get_engine()** (8 connections) — `app/services/acoustic_tripwire.py`
- **shutdown_event()** (5 connections) — `app/main.py`
- **post** (4 connections)
- **tripwire_calibrate()** (4 connections) — `app/main.py`
- **tripwire_disable()** (4 connections) — `app/main.py`
- **tripwire_enable()** (4 connections) — `app/main.py`
- **tripwire_status()** (4 connections) — `app/main.py`
- **upload_file()** (4 connections) — `app/main.py`
- **stop_background_watcher()** (4 connections) — `app/services/screen_vision.py`
- **get_alerts()** (3 connections) — `app/main.py`
- **get** (3 connections)
- **read_root()** (2 connections) — `app/main.py`
- **Stop watcher, acoustic tripwire, and close DB pool cleanly on server shutdown.** (1 connections) — `app/main.py`
- **Frontend polls this endpoint to receive proactive JARVIS screen alerts. e.g.…** (1 connections) — `app/main.py`
- **Return current acoustic tripwire state for the frontend toggle.** (1 connections) — `app/main.py`
- **Arm the acoustic tripwire so double-claps wake Jarvis.** (1 connections) — `app/main.py`
- **Disarm the acoustic tripwire (engine keeps running, just paused).** (1 connections) — `app/main.py`
- **Schedule an ambient-noise recalibration pass. The engine samples the mic for ~2…** (1 connections) — `app/main.py`
- **Upload a file to the data/uploads folder for Jarvis to process.** (1 connections) — `app/main.py`
- **Return the module-level singleton engine, creating it if necessary. Thread-…** (1 connections) — `app/services/acoustic_tripwire.py`
- **Stop the background screen watcher thread cleanly.** (1 connections) — `app/services/screen_vision.py`
- **fastapi_middleware_cors** (1 connections)
- **fastapi_staticfiles** (1 connections)
- **UploadFile** (1 connections)

## Relationships

- [rag_memory + memory](rag_memory_+_memory.md) (5 shared connections)
- [main + screen_vision](main_+_screen_vision.md) (3 shared connections)
- [resume_builder](resume_builder.md) (2 shared connections)
- [agentic_web](agentic_web.md) (1 shared connections)
- [file_ops](file_ops.md) (1 shared connections)
- [chat + llm](chat_+_llm.md) (1 shared connections)
- [agents + tool_runner](agents_+_tool_runner.md) (1 shared connections)
- [ppt_router + ppt_tool](ppt_router_+_ppt_tool.md) (1 shared connections)
- [task_ledger + test_task_resumption](task_ledger_+_test_task_resumption.md) (1 shared connections)
- [voice_agent](voice_agent.md) (1 shared connections)
- [acoustic_tripwire](acoustic_tripwire.md) (1 shared connections)
- [server + test_concurrency](server_+_test_concurrency.md) (1 shared connections)

## Source Files

- `app/main.py`
- `app/services/acoustic_tripwire.py`
- `app/services/screen_vision.py`

## Audit Trail

- EXTRACTED: 54 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*