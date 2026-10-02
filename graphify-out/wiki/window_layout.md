# window_layout

> 41 nodes · cohesion 0.08

## Key Concepts

- **window_layout.py** (20 connections) — `app/services/window_layout.py`
- **win32_find_window()** (14 connections) — `app/services/window_layout.py`
- **_get_title()** (11 connections) — `app/services/window_layout.py`
- **_enumerate_app_windows()** (9 connections) — `app/services/window_layout.py`
- **_get_process_name()** (9 connections) — `app/services/window_layout.py`
- **_pick_target_window()** (9 connections) — `app/services/window_layout.py`
- **adjust_active_window()** (7 connections) — `app/services/window_layout.py`
- **spotify_running()** (6 connections) — `app/services/media_state.py`
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
- **_norm()** (4 connections) — `app/services/window_layout.py`
- **_find_window_fuzzy()** (3 connections) — `app/services/tools.py`
- **_cb()** (3 connections) — `app/services/window_layout.py`
- **True if the Spotify desktop app has a window (cheap: EnumWindows, no UIA).** (1 connections) — `app/services/media_state.py`
- **Closes the current browser tab using Ctrl+W, targeting the real foreground app.** (1 connections) — `app/services/tools.py`
- **Find a window HWND by fuzzy name matching using Win32 API (no pygetwindow).** (1 connections) — `app/services/tools.py`
- **Closes a specific window/app by name using Win32 PostMessage WM_CLOSE.** (1 connections) — `app/services/tools.py`
- *... and 16 more nodes in this community*

## Relationships

- [tools](tools.md) (12 shared connections)
- [tools + whatsapp_smart](tools_+_whatsapp_smart.md) (7 shared connections)
- [smart_navigator + rag_memory](smart_navigator_+_rag_memory.md) (5 shared connections)
- [tools + window_layout](tools_+_window_layout.md) (3 shared connections)
- [youtube_control](youtube_control.md) (3 shared connections)
- [youtube_player](youtube_player.md) (3 shared connections)
- [chat + KNOWN_ISSUES](chat_+_KNOWN_ISSUES.md) (1 shared connections)
- [chat + llm](chat_+_llm.md) (1 shared connections)
- [safe_executor + ui_inspector](safe_executor_+_ui_inspector.md) (1 shared connections)
- [prompt_enhancer_button](prompt_enhancer_button.md) (1 shared connections)

## Source Files

- `app/services/media_state.py`
- `app/services/tools.py`
- `app/services/window_layout.py`

## Audit Trail

- EXTRACTED: 92 (90%)
- INFERRED: 10 (10%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*