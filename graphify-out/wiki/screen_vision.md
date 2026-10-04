# screen_vision

> 19 nodes · cohesion 0.12

## Key Concepts

- **understand_screen()** (16 connections) — `app/services/screen_vision.py`
- **_watcher_loop()** (9 connections) — `app/services/screen_vision.py`
- **_call_gemini_vision()** (7 connections) — `app/services/screen_vision.py`
- **_get_active_process_name()** (4 connections) — `app/services/screen_vision.py`
- **_get_active_window_title()** (4 connections) — `app/services/screen_vision.py`
- **_resolve_app_prompt()** (4 connections) — `app/services/screen_vision.py`
- **_build_history_context()** (3 connections) — `app/services/screen_vision.py`
- **_build_system_prompt()** (3 connections) — `app/services/screen_vision.py`
- **_call_gemma_reasoning()** (3 connections) — `app/services/screen_vision.py`
- **Gotchas** (2 connections) — `docs/features/screen-vision.md`
- **Returns the foreground window title using WinAPI.** (1 connections) — `app/services/screen_vision.py`
- **Returns the executable name of the foreground window's process.** (1 connections) — `app/services/screen_vision.py`
- **Match window title / process name to a per-app prompt.** (1 connections) — `app/services/screen_vision.py`
- **Summarise the last N screen states so the VLM can reason about what changed.…** (1 connections) — `app/services/screen_vision.py`
- **Send screenshot + context to the Groq vision model (settings.GROQ_VISION_MODEL).** (1 connections) — `app/services/screen_vision.py`
- **Send a scene description to Groq (openai/gpt-oss-20b) for reasoning.** (1 connections) — `app/services/screen_vision.py`
- **Assemble the full system prompt based on intent mode and context.** (1 connections) — `app/services/screen_vision.py`
- **Main entry point. Captures screen, resolves context, calls VLM, routes…** (1 connections) — `app/services/screen_vision.py`
- **Background thread body. Every WATCHER_INTERVAL_SECONDS: - Capture screen -…** (1 connections) — `app/services/screen_vision.py`

## Relationships

- [server + persistence](server_+_persistence.md) (9 shared connections)
- [screen_reader](screen_reader.md) (4 shared connections)
- [screen-vision + screen_vision](screen-vision_+_screen_vision.md) (4 shared connections)
- [file_ops](file_ops.md) (2 shared connections)
- [screen_reader + screen_vision](screen_reader_+_screen_vision.md) (2 shared connections)
- [main + screen_vision](main_+_screen_vision.md) (1 shared connections)

## Source Files

- `app/services/screen_vision.py`
- `docs/features/screen-vision.md`

## Audit Trail

- EXTRACTED: 40 (93%)
- INFERRED: 3 (7%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*