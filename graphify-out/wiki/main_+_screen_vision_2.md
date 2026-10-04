# main + screen_vision

> 4 nodes · cohesion 0.50

## Key Concepts

- **shutdown_event()** (5 connections) — `app/main.py`
- **stop_background_watcher()** (4 connections) — `app/services/screen_vision.py`
- **Stop watcher, acoustic tripwire, and close DB pool cleanly on server shutdown.** (1 connections) — `app/main.py`
- **Stop the background screen watcher thread cleanly.** (1 connections) — `app/services/screen_vision.py`

## Relationships

- [main](main.md) (2 shared connections)
- [rag_memory + mysql_db](rag_memory_+_mysql_db.md) (1 shared connections)
- [voice_agent](voice_agent.md) (1 shared connections)
- [server + persistence](server_+_persistence.md) (1 shared connections)

## Source Files

- `app/main.py`
- `app/services/screen_vision.py`

## Audit Trail

- EXTRACTED: 8 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*