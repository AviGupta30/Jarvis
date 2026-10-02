# screen_reader

> 17 nodes · cohesion 0.17

## Key Concepts

- **screen_reader.py** (24 connections) — `app/services/screen_reader.py`
- **read_screen()** (10 connections) — `app/services/screen_reader.py`
- **get_active_window_info()** (10 connections) — `app/services/ui_inspector.py`
- **_groq_vision_screen()** (5 connections) — `app/services/screen_reader.py`
- **_accessibility_tree()** (4 connections) — `app/services/screen_reader.py`
- **_vlm_screen()** (4 connections) — `app/services/screen_reader.py`
- **Layers (`screen_reader.read_screen`)** (4 connections) — `docs/features/screen-vision.md`
- **get_screen_screenshot_b64()** (3 connections) — `app/services/screen_reader.py`
- **_window_title_only()** (3 connections) — `app/services/screen_reader.py`
- **screen_reader.py — Jarvis Screen Vision (VLM-first architecture)…** (1 connections) — `app/services/screen_reader.py`
- **Reads the active window's accessibility tree. Works best for native Win32 apps.…** (1 connections) — `app/services/screen_reader.py`
- **Always works — returns at minimum the active window title.** (1 connections) — `app/services/screen_reader.py`
- **Main function — returns the richest available description of the screen.…** (1 connections) — `app/services/screen_reader.py`
- **Takes a screenshot and returns it as a base64-encoded JPEG string. Used as…** (1 connections) — `app/services/screen_reader.py`
- **Primary layer: sends screenshot to Gemini 2.0 Flash VLM. Returns rich…** (1 connections) — `app/services/screen_reader.py`
- **Fallback vision layer using Groq LLaVA. Faster (~200ms) but weaker at complex…** (1 connections) — `app/services/screen_reader.py`
- **Returns a text summary of the currently focused window: window title + list of…** (1 connections) — `app/services/ui_inspector.py`

## Relationships

- [assignment_tool + safe_executor](assignment_tool_+_safe_executor.md) (8 shared connections)
- [screen_vision](screen_vision.md) (6 shared connections)
- [screen_reader + screen_vision](screen_reader_+_screen_vision.md) (3 shared connections)
- [screen_reader](screen_reader.md) (3 shared connections)
- [tools](tools.md) (3 shared connections)
- [syllabus_auditor + syllabus-auditor](syllabus_auditor_+_syllabus-auditor.md) (1 shared connections)
- [message_reader + whatsapp](message_reader_+_whatsapp.md) (1 shared connections)
- [chat](chat.md) (1 shared connections)
- [dag_executor + planner](dag_executor_+_planner.md) (1 shared connections)
- [ui_inspector + lru](ui_inspector_+_lru.md) (1 shared connections)
- [screen-vision + screen_vision](screen-vision_+_screen_vision.md) (1 shared connections)

## Source Files

- `app/services/screen_reader.py`
- `app/services/ui_inspector.py`
- `docs/features/screen-vision.md`

## Audit Trail

- EXTRACTED: 47 (90%)
- INFERRED: 5 (10%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*