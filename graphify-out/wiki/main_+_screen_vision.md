# main + screen_vision

> 14 nodes · cohesion 0.18

## Key Concepts

- **main.py** (27 connections) — `app/main.py`
- **startup_event()** (8 connections) — `app/main.py`
- **start_background_watcher()** (6 connections) — `app/services/screen_vision.py`
- **shutdown_event()** (5 connections) — `app/main.py`
- **stop_background_watcher()** (4 connections) — `app/services/screen_vision.py`
- **_on_screen_alert()** (3 connections) — `app/main.py`
- **shutil** (3 connections)
- **Stop watcher, acoustic tripwire, and close DB pool cleanly on server shutdown.** (1 connections) — `app/main.py`
- **Callback fired by the background watcher when something notable is detected.…** (1 connections) — `app/main.py`
- **Start background screen watcher and RAG memory system when the server boots.** (1 connections) — `app/main.py`
- **Start the passive background screen watcher. Args: callback: Function called…** (1 connections) — `app/services/screen_vision.py`
- **Stop the background screen watcher thread cleanly.** (1 connections) — `app/services/screen_vision.py`
- **fastapi_middleware_cors** (1 connections)
- **fastapi_staticfiles** (1 connections)

## Relationships

- [main](main.md) (8 shared connections)
- [rag_memory + mysql_db](rag_memory_+_mysql_db.md) (5 shared connections)
- [screen_vision + screen_reader](screen_vision_+_screen_reader.md) (3 shared connections)
- [benchmark + server](benchmark_+_server.md) (2 shared connections)
- [resume_router](resume_router.md) (2 shared connections)
- [voice_agent](voice_agent.md) (2 shared connections)
- [tools](tools.md) (2 shared connections)
- [chat + llm](chat_+_llm.md) (1 shared connections)
- [memory + CLAUDE](memory_+_CLAUDE.md) (1 shared connections)
- [social_content_manager + tools](social_content_manager_+_tools.md) (1 shared connections)
- [ppt_router](ppt_router.md) (1 shared connections)
- [nlp_extractor + download_kokoro](nlp_extractor_+_download_kokoro.md) (1 shared connections)

## Source Files

- `app/main.py`
- `app/services/screen_vision.py`

## Audit Trail

- EXTRACTED: 42 (89%)
- INFERRED: 5 (11%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*