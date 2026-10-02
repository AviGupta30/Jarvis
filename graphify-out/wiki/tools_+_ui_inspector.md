# tools + ui_inspector

> 15 nodes · cohesion 0.13

## Key Concepts

- **Entry points** (10 connections) — `docs/features/screen-vision.md`
- **click_ui_element_uia()** (6 connections) — `app/services/tools.py`
- **dump_app_ui_tree()** (6 connections) — `app/services/tools.py`
- **read_ui_element_text()** (6 connections) — `app/services/tools.py`
- **type_into_ui_element()** (6 connections) — `app/services/tools.py`
- **read_element_text()** (4 connections) — `app/services/ui_inspector.py`
- **smart_click()** (4 connections) — `app/services/ui_inspector.py`
- **type_into_element()** (4 connections) — `app/services/ui_inspector.py`
- **Click a UI element inside an app by AutomationId, name, or control type. Does…** (1 connections) — `app/services/tools.py`
- **Inject text into a specific input field in an app via UIA Value pattern. No…** (1 connections) — `app/services/tools.py`
- **Read the current text content of a UI element — e.g. a terminal output pane, a…** (1 connections) — `app/services/tools.py`
- **Dump the full Windows UI Automation accessibility tree of an app window. Use…** (1 connections) — `app/services/tools.py`
- **Click a UI element by AutomationId, name, or control type inside an app. Does…** (1 connections) — `app/services/ui_inspector.py`
- **Inject text into a specific input field in an app via UIA Value pattern. No…** (1 connections) — `app/services/ui_inspector.py`
- **Read the current text content of a UI element (e.g. terminal output pane,…** (1 connections) — `app/services/ui_inspector.py`

## Relationships

- [tools](tools.md) (11 shared connections)
- [whatsapp_smart + tools](whatsapp_smart_+_tools.md) (4 shared connections)
- [social_content_manager + ui_inspector](social_content_manager_+_ui_inspector.md) (4 shared connections)
- [screen_vision + screen_reader](screen_vision_+_screen_reader.md) (2 shared connections)
- [memory + main](memory_+_main.md) (2 shared connections)
- [safe_executor + ui_inspector](safe_executor_+_ui_inspector.md) (1 shared connections)
- [ui_inspector](ui_inspector.md) (1 shared connections)

## Source Files

- `app/services/tools.py`
- `app/services/ui_inspector.py`
- `docs/features/screen-vision.md`

## Audit Trail

- EXTRACTED: 18 (46%)
- INFERRED: 21 (54%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*