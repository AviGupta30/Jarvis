# main + screen_vision

> 13 nodes · cohesion 0.17

## Key Concepts

- **get_active_window_info()** (10 connections) — `app/services/ui_inspector.py`
- **Entry points** (10 connections) — `docs/features/screen-vision.md`
- **startup_event()** (8 connections) — `app/main.py`
- **describe_screen_for_llm()** (8 connections) — `app/services/screen_reader.py`
- **start_background_watcher()** (6 connections) — `app/services/screen_vision.py`
- **describe_screen_vlm()** (5 connections) — `app/services/screen_vision.py`
- **_on_screen_alert()** (3 connections) — `app/main.py`
- **Callback fired by the background watcher when something notable is detected.…** (1 connections) — `app/main.py`
- **Start background screen watcher and RAG memory system when the server boots.** (1 connections) — `app/main.py`
- **Returns a clean, LLM-optimized description of the current screen. Used as…** (1 connections) — `app/services/screen_reader.py`
- **Lightweight passive description — used as context injection in chat.py. Always…** (1 connections) — `app/services/screen_vision.py`
- **Start the passive background screen watcher. Args: callback: Function called…** (1 connections) — `app/services/screen_vision.py`
- **Returns a text summary of the currently focused window: window title + list of…** (1 connections) — `app/services/ui_inspector.py`

## Relationships

- [screen_reader](screen_reader.md) (5 shared connections)
- [ui_inspector + tools](ui_inspector_+_tools.md) (5 shared connections)
- [screen_vision](screen_vision.md) (4 shared connections)
- [main](main.md) (3 shared connections)
- [rag_memory + memory](rag_memory_+_memory.md) (2 shared connections)
- [chat + llm](chat_+_llm.md) (2 shared connections)
- [dag_executor + planner](dag_executor_+_planner.md) (2 shared connections)
- [tools](tools.md) (2 shared connections)
- [safe_executor](safe_executor.md) (2 shared connections)
- [voice_agent](voice_agent.md) (1 shared connections)
- [screen-vision + screen_vision](screen-vision_+_screen_vision.md) (1 shared connections)
- [ui_inspector](ui_inspector.md) (1 shared connections)

## Source Files

- `app/main.py`
- `app/services/screen_reader.py`
- `app/services/screen_vision.py`
- `app/services/ui_inspector.py`
- `docs/features/screen-vision.md`

## Audit Trail

- EXTRACTED: 28 (65%)
- INFERRED: 15 (35%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*