# screen_vision

> 14 nodes · cohesion 0.15

## Key Concepts

- **_watcher_loop()** (9 connections) — `app/services/screen_vision.py`
- **capture_screen_b64()** (6 connections) — `app/services/screen_vision.py`
- **_get_active_process_name()** (4 connections) — `app/services/screen_vision.py`
- **_get_active_window_title()** (4 connections) — `app/services/screen_vision.py`
- **_pixel_diff_percent()** (4 connections) — `app/services/screen_vision.py`
- **_resolve_app_prompt()** (4 connections) — `app/services/screen_vision.py`
- **ndarray** (2 connections)
- **Config** (2 connections) — `docs/features/screen-vision.md`
- **Returns the foreground window title using WinAPI.** (1 connections) — `app/services/screen_vision.py`
- **Returns the executable name of the foreground window's process.** (1 connections) — `app/services/screen_vision.py`
- **Match window title / process name to a per-app prompt.** (1 connections) — `app/services/screen_vision.py`
- **Returns the percentage of pixels that changed significantly between two frames.…** (1 connections) — `app/services/screen_vision.py`
- **Background thread body. Every WATCHER_INTERVAL_SECONDS: - Capture screen -…** (1 connections) — `app/services/screen_vision.py`
- **Capture the primary monitor using mss (~10ms). Returns (base64_jpeg_string,…** (1 connections) — `app/services/screen_vision.py`

## Relationships

- [voice_agent + acoustic_tripwire](voice_agent_+_acoustic_tripwire.md) (6 shared connections)
- [screen_vision](screen_vision.md) (4 shared connections)
- [screen-vision + screen_vision](screen-vision_+_screen_vision.md) (2 shared connections)
- [main + screen_vision](main_+_screen_vision.md) (1 shared connections)

## Source Files

- `app/services/screen_vision.py`
- `docs/features/screen-vision.md`

## Audit Trail

- EXTRACTED: 25 (93%)
- INFERRED: 2 (7%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*