# window_layout

> 37 nodes · cohesion 0.10

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
- **_cb()** (3 connections) — `app/services/window_layout.py`
- **media_state.py — which media app the user used last (Spotify or YouTube)…** (1 connections) — `app/services/media_state.py`
- **True if the Spotify desktop app has a window (cheap: EnumWindows, no UIA).** (1 connections) — `app/services/media_state.py`
- **window_layout.py — Isolated Window Layout & Window Manager…** (1 connections) — `app/services/window_layout.py`
- **Return True if this HWND looks like a real user-facing application window.** (1 connections) — `app/services/window_layout.py`
- **Normalise string for fuzzy comparison.** (1 connections) — `app/services/window_layout.py`
- **Return list of (hwnd, title) for all real user-facing windows, in Z-order…** (1 connections) — `app/services/window_layout.py`
- *... and 12 more nodes in this community*

## Relationships

- [tools](tools.md) (16 shared connections)
- [youtube_player](youtube_player.md) (6 shared connections)
- [whatsapp_smart + tools](whatsapp_smart_+_tools.md) (3 shared connections)
- [whatsapp + dump_wa_ui](whatsapp_+_dump_wa_ui.md) (2 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (2 shared connections)
- [agentic_web](agentic_web.md) (1 shared connections)
- [task_ledger + test_task_resumption](task_ledger_+_test_task_resumption.md) (1 shared connections)
- [media_sessions](media_sessions.md) (1 shared connections)
- [chat + llm](chat_+_llm.md) (1 shared connections)
- [uia_local](uia_local.md) (1 shared connections)
- [prompt_enhancer_button](prompt_enhancer_button.md) (1 shared connections)
- [ssml_processor + debug_wa](ssml_processor_+_debug_wa.md) (1 shared connections)

## Source Files

- `app/services/media_state.py`
- `app/services/window_layout.py`

## Audit Trail

- EXTRACTED: 97 (96%)
- INFERRED: 4 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*