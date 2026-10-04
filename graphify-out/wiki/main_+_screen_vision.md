# main + screen_vision

> 34 nodes · cohesion 0.08

## Key Concepts

- **main.py** (27 connections) — `app/main.py`
- **startup_event()** (8 connections) — `app/main.py`
- **get_engine()** (8 connections) — `app/services/acoustic_tripwire.py`
- **start_background_watcher()** (6 connections) — `app/services/screen_vision.py`
- **shutdown_event()** (5 connections) — `app/main.py`
- **post** (4 connections)
- **tripwire_calibrate()** (4 connections) — `app/main.py`
- **tripwire_disable()** (4 connections) — `app/main.py`
- **tripwire_enable()** (4 connections) — `app/main.py`
- **tripwire_status()** (4 connections) — `app/main.py`
- **upload_file()** (4 connections) — `app/main.py`
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
- **Arm the acoustic tripwire so double-claps wake Jarvis.** (1 connections) — `app/main.py`
- **Disarm the acoustic tripwire (engine keeps running, just paused).** (1 connections) — `app/main.py`
- **Schedule an ambient-noise recalibration pass. The engine samples the mic for ~2…** (1 connections) — `app/main.py`
- **Upload a file to the data/uploads folder for Jarvis to process.** (1 connections) — `app/main.py`
- *... and 9 more nodes in this community*

## Relationships

- [mysql_db + rag_memory](mysql_db_+_rag_memory.md) (4 shared connections)
- [resume_router + tools](resume_router_+_tools.md) (3 shared connections)
- [screen_vision + screen_reader](screen_vision_+_screen_reader.md) (3 shared connections)
- [memory + rag_memory](memory_+_rag_memory.md) (2 shared connections)
- [voice_agent](voice_agent.md) (2 shared connections)
- [tools + ui_inspector](tools_+_ui_inspector.md) (2 shared connections)
- [assignment_humanizer + task_ledger](assignment_humanizer_+_task_ledger.md) (2 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (1 shared connections)
- [social_content_manager + content-tools](social_content_manager_+_content-tools.md) (1 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (1 shared connections)
- [ppt_router + ppt_tool](ppt_router_+_ppt_tool.md) (1 shared connections)
- [acoustic_tripwire](acoustic_tripwire.md) (1 shared connections)

## Source Files

- `app/main.py`
- `app/services/acoustic_tripwire.py`
- `app/services/screen_vision.py`
- `test_fastapi.py`

## Audit Trail

- EXTRACTED: 65 (93%)
- INFERRED: 5 (7%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*