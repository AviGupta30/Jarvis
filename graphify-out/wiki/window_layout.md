# window_layout

> 39 nodes · cohesion 0.08

## Key Concepts

- **window_layout.py** (20 connections) — `app/services/window_layout.py`
- **win32_find_window()** (14 connections) — `app/services/window_layout.py`
- **_get_title()** (11 connections) — `app/services/window_layout.py`
- **_enumerate_app_windows()** (9 connections) — `app/services/window_layout.py`
- **_pick_target_window()** (9 connections) — `app/services/window_layout.py`
- **adjust_active_window()** (7 connections) — `app/services/window_layout.py`
- **win32_focus_window()** (7 connections) — `app/services/window_layout.py`
- **_is_real_app_window()** (6 connections) — `app/services/window_layout.py`
- **win32_close_window()** (6 connections) — `app/services/window_layout.py`
- **win32_maximize_window()** (6 connections) — `app/services/window_layout.py`
- **win32_minimize_window()** (6 connections) — `app/services/window_layout.py`
- **win32_snap_two_windows()** (6 connections) — `app/services/window_layout.py`
- **win32_close_active_tab()** (5 connections) — `app/services/window_layout.py`
- **win32_close_active_window()** (5 connections) — `app/services/window_layout.py`
- **close_specific_window()** (4 connections) — `app/services/tools.py`
- **close_tab()** (4 connections) — `app/services/tools.py`
- **minimize_window()** (4 connections) — `app/services/tools.py`
- **wait_for_window()** (4 connections) — `app/services/tools.py`
- **_norm()** (4 connections) — `app/services/window_layout.py`
- **_cb()** (3 connections) — `app/services/window_layout.py`
- **Closes the current browser tab using Ctrl+W, targeting the real foreground app.** (1 connections) — `app/services/tools.py`
- **Closes a specific window/app by name using Win32 PostMessage WM_CLOSE.** (1 connections) — `app/services/tools.py`
- **Minimizes a specific window by name using Win32 ShowWindow.** (1 connections) — `app/services/tools.py`
- **Block until a window with the given name appears, then focus it.** (1 connections) — `app/services/tools.py`
- **window_layout.py — Isolated Window Layout & Window Manager…** (1 connections) — `app/services/window_layout.py`
- *... and 14 more nodes in this community*

## Relationships

- [tools](tools.md) (21 shared connections)
- [youtube_player](youtube_player.md) (4 shared connections)
- [whatsapp_smart + tools](whatsapp_smart_+_tools.md) (3 shared connections)
- [dump_wa_ui + test_wa](dump_wa_ui_+_test_wa.md) (2 shared connections)
- [uia_local](uia_local.md) (1 shared connections)
- [prompt_enhancer_button](prompt_enhancer_button.md) (1 shared connections)
- [assignment_assembler + smart_navigator](assignment_assembler_+_smart_navigator.md) (1 shared connections)
- [tool-registry + vector_store](tool-registry_+_vector_store.md) (1 shared connections)
- [youtube_control](youtube_control.md) (1 shared connections)

## Source Files

- `app/services/tools.py`
- `app/services/window_layout.py`

## Audit Trail

- EXTRACTED: 85 (88%)
- INFERRED: 12 (12%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*