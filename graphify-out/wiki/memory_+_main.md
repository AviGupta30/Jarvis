# memory + main

> 18 nodes · cohesion 0.11

## Key Concepts

- **startup_event()** (8 connections) — `app/main.py`
- **Memory: RAG, facts, task ledger, resume, skills** (7 connections) — `docs/features/memory.md`
- **start_background_watcher()** (6 connections) — `app/services/screen_vision.py`
- **shutdown_event()** (5 connections) — `app/main.py`
- **RAG details** (5 connections) — `docs/features/memory.md`
- **stop_background_watcher()** (4 connections) — `app/services/screen_vision.py`
- **on_event()** (4 connections) — `scripts/voice_agent.py`
- **_on_screen_alert()** (3 connections) — `app/main.py`
- **Gotchas** (2 connections) — `docs/features/memory.md`
- **Stop watcher, acoustic tripwire, and close DB pool cleanly on server shutdown.** (1 connections) — `app/main.py`
- **Callback fired by the background watcher when something notable is detected.…** (1 connections) — `app/main.py`
- **Start background screen watcher and RAG memory system when the server boots.** (1 connections) — `app/main.py`
- **Start the passive background screen watcher. Args: callback: Function called…** (1 connections) — `app/services/screen_vision.py`
- **Stop the background screen watcher thread cleanly.** (1 connections) — `app/services/screen_vision.py`
- **memory.md** (1 connections) — `docs/features/memory.md`
- **API** (1 connections) — `docs/features/memory.md`
- **Files & symbols (auto-generated, line numbers are current)** (1 connections) — `docs/features/memory.md`
- **Graphify** (1 connections) — `docs/features/memory.md`

## Relationships

- [main](main.md) (5 shared connections)
- [mysql_db + rag_memory](mysql_db_+_rag_memory.md) (3 shared connections)
- [tools + ui_inspector](tools_+_ui_inspector.md) (2 shared connections)
- [social_content_manager + ui_inspector](social_content_manager_+_ui_inspector.md) (2 shared connections)
- [rag_memory](rag_memory.md) (2 shared connections)
- [voice_agent](voice_agent.md) (2 shared connections)
- [screen_vision + screen_reader](screen_vision_+_screen_reader.md) (1 shared connections)
- [memory](memory.md) (1 shared connections)
- [memory_tool + calendar_tool](memory_tool_+_calendar_tool.md) (1 shared connections)

## Source Files

- `app/main.py`
- `app/services/screen_vision.py`
- `docs/features/memory.md`
- `scripts/voice_agent.py`

## Audit Trail

- EXTRACTED: 27 (75%)
- INFERRED: 9 (25%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*