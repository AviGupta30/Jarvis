# main + screen_vision

> 6 nodes · cohesion 0.33

## Key Concepts

- **startup_event()** (8 connections) — `app/main.py`
- **start_background_watcher()** (6 connections) — `app/services/screen_vision.py`
- **_on_screen_alert()** (3 connections) — `app/main.py`
- **Callback fired by the background watcher when something notable is detected.…** (1 connections) — `app/main.py`
- **Start background screen watcher and RAG memory system when the server boots.** (1 connections) — `app/main.py`
- **Start the passive background screen watcher. Args: callback: Function called…** (1 connections) — `app/services/screen_vision.py`

## Relationships

- [main](main.md) (3 shared connections)
- [rag_memory + mysql_db](rag_memory_+_mysql_db.md) (2 shared connections)
- [tools + ui_inspector](tools_+_ui_inspector.md) (2 shared connections)
- [voice_agent](voice_agent.md) (1 shared connections)
- [server + persistence](server_+_persistence.md) (1 shared connections)
- [screen_vision](screen_vision.md) (1 shared connections)

## Source Files

- `app/main.py`
- `app/services/screen_vision.py`

## Audit Trail

- EXTRACTED: 10 (67%)
- INFERRED: 5 (33%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*