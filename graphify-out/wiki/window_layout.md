# window_layout

> 39 nodes · cohesion 0.09

## Key Concepts

- **window_layout.py** (20 connections) — `app/services/window_layout.py`
- **win32_find_window()** (14 connections) — `app/services/window_layout.py`
- **_get_title()** (11 connections) — `app/services/window_layout.py`
- **media_state.py** (9 connections) — `app/services/media_state.py`
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
- **_norm()** (4 connections) — `app/services/window_layout.py`
- **_find_window_fuzzy()** (3 connections) — `app/services/tools.py`
- **_cb()** (3 connections) — `app/services/window_layout.py`
- **media_state.py — which media app the user used last (Spotify or YouTube)…** (1 connections) — `app/services/media_state.py`
- **True if the Spotify desktop app has a window (cheap: EnumWindows, no UIA).** (1 connections) — `app/services/media_state.py`
- **Find a window HWND by fuzzy name matching using Win32 API (no pygetwindow).** (1 connections) — `app/services/tools.py`
- **window_layout.py — Isolated Window Layout & Window Manager…** (1 connections) — `app/services/window_layout.py`
- **Return True if this HWND looks like a real user-facing application window.** (1 connections) — `app/services/window_layout.py`
- *... and 14 more nodes in this community*

## Relationships

- [tools](tools.md) (16 shared connections)
- [youtube_player](youtube_player.md) (5 shared connections)
- [assignment_tool + assignment_humanizer](assignment_tool_+_assignment_humanizer.md) (3 shared connections)
- [youtube_control + youtube_player](youtube_control_+_youtube_player.md) (3 shared connections)
- [tools + ui_inspector](tools_+_ui_inspector.md) (3 shared connections)
- [persistence + server](persistence_+_server.md) (2 shared connections)
- [spotify_service + media_sessions](spotify_service_+_media_sessions.md) (1 shared connections)
- [chat + rag_memory](chat_+_rag_memory.md) (1 shared connections)
- [voice_agent + ui_inspector](voice_agent_+_ui_inspector.md) (1 shared connections)
- [prompt_enhancer_button](prompt_enhancer_button.md) (1 shared connections)

## Source Files

- `app/services/media_state.py`
- `app/services/tools.py`
- `app/services/window_layout.py`

## Audit Trail

- EXTRACTED: 99 (96%)
- INFERRED: 4 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*