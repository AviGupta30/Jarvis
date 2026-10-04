# ui_inspector

> 20 nodes · cohesion 0.10

## Key Concepts

- **UIAEngine** (12 connections) — `app/services/ui_inspector.py`
- **.dump_tree()** (3 connections) — `app/services/ui_inspector.py`
- **walk()** (3 connections) — `app/services/ui_inspector.py`
- **.find_element()** (2 connections) — `app/services/ui_inspector.py`
- **.find_element_fuzzy()** (2 connections) — `app/services/ui_inspector.py`
- **.get_foreground_window()** (2 connections) — `app/services/ui_inspector.py`
- **.get_text()** (2 connections) — `app/services/ui_inspector.py`
- **.get_window()** (2 connections) — `app/services/ui_inspector.py`
- **.invoke()** (2 connections) — `app/services/ui_inspector.py`
- **.set_value()** (2 connections) — `app/services/ui_inspector.py`
- **Walk all descendants looking for any control whose window_text contains `text`…** (1 connections) — `app/services/ui_inspector.py`
- **Fire an element's primary action via UIA Invoke pattern. No mouse movement —…** (1 connections) — `app/services/ui_inspector.py`
- **Inject text into an input element via UIA Value pattern. No simulated…** (1 connections) — `app/services/ui_inspector.py`
- **Read text from an element via UIA TextPattern or window_text. Returns empty…** (1 connections) — `app/services/ui_inspector.py`
- **Walk the accessibility tree and return all elements up to `depth` levels. Use…** (1 connections) — `app/services/ui_inspector.py`
- **Core wrapper around pywinauto's UIA backend. All interactions go through the OS…** (1 connections) — `app/services/ui_inspector.py`
- **Get a window wrapper by partial title match (regex-safe). Returns None if not…** (1 connections) — `app/services/ui_inspector.py`
- **Get the currently focused window via Win32 HWND matching.** (1 connections) — `app/services/ui_inspector.py`
- **Walk the accessibility tree and find a matching element. Priority: AutomationId…** (1 connections) — `app/services/ui_inspector.py`
- **.__init__()** (1 connections) — `app/services/ui_inspector.py`

## Relationships

- [ui_inspector + tools](ui_inspector_+_tools.md) (2 shared connections)

## Source Files

- `app/services/ui_inspector.py`

## Audit Trail

- EXTRACTED: 21 (95%)
- INFERRED: 1 (5%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*