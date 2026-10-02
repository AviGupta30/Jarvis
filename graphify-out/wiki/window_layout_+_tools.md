# window_layout + tools

> 43 nodes · cohesion 0.07

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
- **close_window()** (5 connections) — `app/services/tools.py`
- **snap_windows()** (5 connections) — `app/services/tools.py`
- **win32_close_active_tab()** (5 connections) — `app/services/window_layout.py`
- **win32_close_active_window()** (5 connections) — `app/services/window_layout.py`
- **close_specific_window()** (4 connections) — `app/services/tools.py`
- **focus_window()** (4 connections) — `app/services/tools.py`
- **wait_for_window()** (4 connections) — `app/services/tools.py`
- **_norm()** (4 connections) — `app/services/window_layout.py`
- **_find_window_fuzzy()** (3 connections) — `app/services/tools.py`
- **_cb()** (3 connections) — `app/services/window_layout.py`
- **Snaps left_app to left half and right_app to right half using Win32 API (no…** (1 connections) — `app/services/tools.py`
- **Closes the current active real app window (skips the Jarvis overlay).** (1 connections) — `app/services/tools.py`
- **Find a window HWND by fuzzy name matching using Win32 API (no pygetwindow).** (1 connections) — `app/services/tools.py`
- *... and 18 more nodes in this community*

## Relationships

- [tools](tools.md) (23 shared connections)
- [media_state + youtube_control](media_state_+_youtube_control.md) (5 shared connections)
- [whatsapp_smart + tools](whatsapp_smart_+_tools.md) (3 shared connections)
- [youtube_player](youtube_player.md) (3 shared connections)
- [social_content_manager + ui_inspector](social_content_manager_+_ui_inspector.md) (2 shared connections)
- [prompt_enhancer_button](prompt_enhancer_button.md) (1 shared connections)
- [message_reader + reply_generator](message_reader_+_reply_generator.md) (1 shared connections)

## Source Files

- `app/services/tools.py`
- `app/services/window_layout.py`

## Audit Trail

- EXTRACTED: 88 (85%)
- INFERRED: 16 (15%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*