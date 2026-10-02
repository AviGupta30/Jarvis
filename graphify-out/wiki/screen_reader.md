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

- [screen_vision](screen_vision.md) (6 shared connections)
- [assignment_tool + assignment_humanizer](assignment_tool_+_assignment_humanizer.md) (4 shared connections)
- [screen_reader + screen_vision](screen_reader_+_screen_vision.md) (3 shared connections)
- [screen_reader](screen_reader.md) (3 shared connections)
- [persistence + server](persistence_+_server.md) (2 shared connections)
- [dump_wa_ui + test_wa](dump_wa_ui_+_test_wa.md) (2 shared connections)
- [tools](tools.md) (2 shared connections)
- [safe_executor](safe_executor.md) (2 shared connections)
- [chat + rag_memory](chat_+_rag_memory.md) (1 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (1 shared connections)
- [voice_agent + ui_inspector](voice_agent_+_ui_inspector.md) (1 shared connections)
- [tools + ui_inspector](tools_+_ui_inspector.md) (1 shared connections)

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