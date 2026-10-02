# tools + window_layout

> 6 nodes · cohesion 0.33

## Key Concepts

- **win32_focus_window()** (7 connections) — `app/services/window_layout.py`
- **focus_window()** (4 connections) — `app/services/tools.py`
- **wait_for_window()** (4 connections) — `app/services/tools.py`
- **Bring a window to the foreground by partial name match (Win32 API, no…** (1 connections) — `app/services/tools.py`
- **Block until a window with the given name appears, then focus it.** (1 connections) — `app/services/tools.py`
- **Bring the named window to the foreground.** (1 connections) — `app/services/window_layout.py`

## Relationships

- [tools](tools.md) (3 shared connections)
- [window_layout](window_layout.md) (3 shared connections)
- [tools + whatsapp_smart](tools_+_whatsapp_smart.md) (2 shared connections)

## Source Files

- `app/services/tools.py`
- `app/services/window_layout.py`

## Audit Trail

- EXTRACTED: 9 (69%)
- INFERRED: 4 (31%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*