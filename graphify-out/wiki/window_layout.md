# window_layout

> 39 nodes · cohesion 0.09

## Key Concepts

- **window_layout.py** (20 connections) — `app/services/window_layout.py`
- **win32_find_window()** (14 connections) — `app/services/window_layout.py`
- **_get_title()** (11 connections) — `app/services/window_layout.py`
- **_enumerate_app_windows()** (9 connections) — `app/services/window_layout.py`
- **_get_process_name()** (9 connections) — `app/services/window_layout.py`
- **_pick_target_window()** (9 connections) — `app/services/window_layout.py`
- **adjust_active_window()** (7 connections) — `app/services/window_layout.py`
- **win32_focus_window()** (7 connections) — `app/services/window_layout.py`
- **spotify_running()** (6 connections) — `app/services/media_state.py`
- **_is_real_app_window()** (6 connections) — `app/services/window_layout.py`
- **win32_close_window()** (6 connections) — `app/services/window_layout.py`
- **win32_maximize_window()** (6 connections) — `app/services/window_layout.py`
- **win32_minimize_window()** (6 connections) — `app/services/window_layout.py`
- **win32_snap_two_windows()** (6 connections) — `app/services/window_layout.py`
- **win32_close_active_tab()** (5 connections) — `app/services/window_layout.py`
- **win32_close_active_window()** (5 connections) — `app/services/window_layout.py`
- **focus_window()** (4 connections) — `app/services/tools.py`
- **minimize_window()** (4 connections) — `app/services/tools.py`
- **_norm()** (4 connections) — `app/services/window_layout.py`
- **_cb()** (3 connections) — `app/services/window_layout.py`
- **True if the Spotify desktop app has a window (cheap: EnumWindows, no UIA).** (1 connections) — `app/services/media_state.py`
- **Minimizes a specific window by name using Win32 ShowWindow.** (1 connections) — `app/services/tools.py`
- **Bring a window to the foreground by partial name match (Win32 API, no…** (1 connections) — `app/services/tools.py`
- **window_layout.py — Isolated Window Layout & Window Manager…** (1 connections) — `app/services/window_layout.py`
- **Return True if this HWND looks like a real user-facing application window.** (1 connections) — `app/services/window_layout.py`
- *... and 14 more nodes in this community*

## Relationships

- [tools](tools.md) (21 shared connections)
- [youtube_player](youtube_player.md) (6 shared connections)
- [assignment_tool + safe_executor](assignment_tool_+_safe_executor.md) (5 shared connections)
- [youtube_control](youtube_control.md) (1 shared connections)
- [chat](chat.md) (1 shared connections)
- [uia_local](uia_local.md) (1 shared connections)
- [prompt_enhancer_button](prompt_enhancer_button.md) (1 shared connections)

## Source Files

- `app/services/media_state.py`
- `app/services/tools.py`
- `app/services/window_layout.py`

## Audit Trail

- EXTRACTED: 93 (92%)
- INFERRED: 8 (8%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*