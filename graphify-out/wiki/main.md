# main

> 24 nodes · cohesion 0.12

## Key Concepts

- **main.py** (26 connections) — `app/main.py`
- **get_engine()** (8 connections) — `app/services/acoustic_tripwire.py`
- **post** (4 connections)
- **tripwire_calibrate()** (4 connections) — `app/main.py`
- **tripwire_disable()** (4 connections) — `app/main.py`
- **tripwire_enable()** (4 connections) — `app/main.py`
- **tripwire_status()** (4 connections) — `app/main.py`
- **upload_file()** (4 connections) — `app/main.py`
- **get_alerts()** (3 connections) — `app/main.py`
- **get** (3 connections)
- **shutil** (3 connections)
- **test_fastapi.py** (3 connections) — `test_fastapi.py`
- **read_root()** (2 connections) — `app/main.py`
- **Frontend polls this endpoint to receive proactive JARVIS screen alerts. e.g.…** (1 connections) — `app/main.py`
- **Return current acoustic tripwire state for the frontend toggle.** (1 connections) — `app/main.py`
- **Arm the acoustic tripwire so double-claps wake Jarvis.** (1 connections) — `app/main.py`
- **Disarm the acoustic tripwire (engine keeps running, just paused).** (1 connections) — `app/main.py`
- **Schedule an ambient-noise recalibration pass. The engine samples the mic for ~2…** (1 connections) — `app/main.py`
- **Upload a file to the data/uploads folder for Jarvis to process.** (1 connections) — `app/main.py`
- **Return the module-level singleton engine, creating it if necessary. Thread-…** (1 connections) — `app/services/acoustic_tripwire.py`
- **fastapi_middleware_cors** (1 connections)
- **fastapi_staticfiles** (1 connections)
- **fastapi_testclient** (1 connections)
- **UploadFile** (1 connections)

## Relationships

- [memory + main](memory_+_main.md) (5 shared connections)
- [mysql_db + rag_memory](mysql_db_+_rag_memory.md) (2 shared connections)
- [social_content_manager + ui_inspector](social_content_manager_+_ui_inspector.md) (2 shared connections)
- [tools](tools.md) (2 shared connections)
- [acoustic_tripwire](acoustic_tripwire.md) (2 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (1 shared connections)
- [memory](memory.md) (1 shared connections)
- [ppt_router + ppt_tool](ppt_router_+_ppt_tool.md) (1 shared connections)
- [file_ops](file_ops.md) (1 shared connections)
- [task_ledger + test_task_resumption](task_ledger_+_test_task_resumption.md) (1 shared connections)
- [safe_executor + ui_inspector](safe_executor_+_ui_inspector.md) (1 shared connections)

## Source Files

- `app/main.py`
- `app/services/acoustic_tripwire.py`
- `test_fastapi.py`

## Audit Trail

- EXTRACTED: 51 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*