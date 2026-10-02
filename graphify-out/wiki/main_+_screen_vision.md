# main + screen_vision

> 9 nodes · cohesion 0.25

## Key Concepts

- **Entry points** (10 connections) — `docs/features/screen-vision.md`
- **startup_event()** (8 connections) — `app/main.py`
- **start_background_watcher()** (6 connections) — `app/services/screen_vision.py`
- **dump_app_ui_tree()** (6 connections) — `app/services/tools.py`
- **_on_screen_alert()** (3 connections) — `app/main.py`
- **Callback fired by the background watcher when something notable is detected.…** (1 connections) — `app/main.py`
- **Start background screen watcher and RAG memory system when the server boots.** (1 connections) — `app/main.py`
- **Start the passive background screen watcher. Args: callback: Function called…** (1 connections) — `app/services/screen_vision.py`
- **Dump the full Windows UI Automation accessibility tree of an app window. Use…** (1 connections) — `app/services/tools.py`

## Relationships

- [screen_vision + screen_reader](screen_vision_+_screen_reader.md) (4 shared connections)
- [main](main.md) (3 shared connections)
- [tools + ui_inspector](tools_+_ui_inspector.md) (3 shared connections)
- [safe_executor + ui_inspector](safe_executor_+_ui_inspector.md) (2 shared connections)
- [tools + whatsapp_smart](tools_+_whatsapp_smart.md) (2 shared connections)
- [mysql_db + rag_memory](mysql_db_+_rag_memory.md) (1 shared connections)
- [voice_agent](voice_agent.md) (1 shared connections)
- [memory + rag_memory](memory_+_rag_memory.md) (1 shared connections)
- [tools](tools.md) (1 shared connections)
- [ui_inspector](ui_inspector.md) (1 shared connections)

## Source Files

- `app/main.py`
- `app/services/screen_vision.py`
- `app/services/tools.py`
- `docs/features/screen-vision.md`

## Audit Trail

- EXTRACTED: 13 (46%)
- INFERRED: 15 (54%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*