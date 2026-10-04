# main

> 21 nodes · cohesion 0.14

## Key Concepts

- **main.py** (27 connections) — `app/main.py`
- **get_engine()** (8 connections) — `app/services/acoustic_tripwire.py`
- **post** (4 connections)
- **tripwire_calibrate()** (4 connections) — `app/main.py`
- **tripwire_disable()** (4 connections) — `app/main.py`
- **tripwire_enable()** (4 connections) — `app/main.py`
- **tripwire_status()** (4 connections) — `app/main.py`
- **upload_file()** (4 connections) — `app/main.py`
- **get_alerts()** (3 connections) — `app/main.py`
- **get** (3 connections)
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
- **UploadFile** (1 connections)

## Relationships

- [main + screen_vision](main_+_screen_vision.md) (3 shared connections)
- [message_reader + thread_extractor](message_reader_+_thread_extractor.md) (2 shared connections)
- [mysql_db + rag_memory](mysql_db_+_rag_memory.md) (2 shared connections)
- [voice_agent + main](voice_agent_+_main.md) (2 shared connections)
- [voice_agent + download_kokoro](voice_agent_+_download_kokoro.md) (2 shared connections)
- [resume_router](resume_router.md) (2 shared connections)
- [task_ledger + rag_memory](task_ledger_+_rag_memory.md) (1 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (1 shared connections)
- [memory](memory.md) (1 shared connections)
- [rag_memory + tool_runner](rag_memory_+_tool_runner.md) (1 shared connections)
- [ppt_router + ppt_tool](ppt_router_+_ppt_tool.md) (1 shared connections)
- [acoustic_tripwire](acoustic_tripwire.md) (1 shared connections)

## Source Files

- `app/main.py`
- `app/services/acoustic_tripwire.py`

## Audit Trail

- EXTRACTED: 48 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*