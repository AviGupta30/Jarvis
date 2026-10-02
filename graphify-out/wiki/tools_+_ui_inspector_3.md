# tools + ui_inspector

> 4 nodes · cohesion 0.50

## Key Concepts

- **read_ui_element_text()** (6 connections) — `app/services/tools.py`
- **read_element_text()** (4 connections) — `app/services/ui_inspector.py`
- **Read the current text content of a UI element — e.g. a terminal output pane, a…** (1 connections) — `app/services/tools.py`
- **Read the current text content of a UI element (e.g. terminal output pane,…** (1 connections) — `app/services/ui_inspector.py`

## Relationships

- [tools](tools.md) (2 shared connections)
- [tools + whatsapp_smart](tools_+_whatsapp_smart.md) (2 shared connections)
- [main + screen_vision](main_+_screen_vision.md) (1 shared connections)
- [safe_executor + ui_inspector](safe_executor_+_ui_inspector.md) (1 shared connections)

## Source Files

- `app/services/tools.py`
- `app/services/ui_inspector.py`

## Audit Trail

- EXTRACTED: 5 (56%)
- INFERRED: 4 (44%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*