# tools + ui_inspector

> 4 nodes · cohesion 0.50

## Key Concepts

- **get_active_window_info()** (10 connections) — `app/services/ui_inspector.py`
- **read_active_window_text()** (4 connections) — `app/services/tools.py`
- **Get all readable text from the currently active window.** (1 connections) — `app/services/tools.py`
- **Returns a text summary of the currently focused window: window title + list of…** (1 connections) — `app/services/ui_inspector.py`

## Relationships

- [tools + window_layout](tools_+_window_layout.md) (3 shared connections)
- [screen_reader](screen_reader.md) (2 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (2 shared connections)
- [tools + ui_inspector](tools_+_ui_inspector.md) (2 shared connections)
- [safe_executor](safe_executor.md) (1 shared connections)

## Source Files

- `app/services/tools.py`
- `app/services/ui_inspector.py`

## Audit Trail

- EXTRACTED: 9 (69%)
- INFERRED: 4 (31%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*