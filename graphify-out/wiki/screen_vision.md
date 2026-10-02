# screen_vision

> 26 nodes · cohesion 0.12

## Key Concepts

- **screen_vision.py** (28 connections) — `app/services/screen_vision.py`
- **understand_screen()** (16 connections) — `app/services/screen_vision.py`
- **_watcher_loop()** (9 connections) — `app/services/screen_vision.py`
- **capture_screen_b64()** (6 connections) — `app/services/screen_vision.py`
- **_get_active_process_name()** (4 connections) — `app/services/screen_vision.py`
- **_get_active_window_title()** (4 connections) — `app/services/screen_vision.py`
- **_pixel_diff_percent()** (4 connections) — `app/services/screen_vision.py`
- **_resolve_app_prompt()** (4 connections) — `app/services/screen_vision.py`
- **pil** (4 connections)
- **_build_history_context()** (3 connections) — `app/services/screen_vision.py`
- **_build_system_prompt()** (3 connections) — `app/services/screen_vision.py`
- **_call_gemma_reasoning()** (3 connections) — `app/services/screen_vision.py`
- **ndarray** (2 connections)
- **Config** (2 connections) — `docs/features/screen-vision.md`
- **screen_vision.py — Jarvis VLM Screen Understanding (Layer 1 Upgrade)…** (1 connections) — `app/services/screen_vision.py`
- **Returns the foreground window title using WinAPI.** (1 connections) — `app/services/screen_vision.py`
- **Returns the executable name of the foreground window's process.** (1 connections) — `app/services/screen_vision.py`
- **Match window title / process name to a per-app prompt.** (1 connections) — `app/services/screen_vision.py`
- **Summarise the last N screen states so the VLM can reason about what changed.…** (1 connections) — `app/services/screen_vision.py`
- **Send a scene description to Groq (openai/gpt-oss-20b) for reasoning.** (1 connections) — `app/services/screen_vision.py`
- **Assemble the full system prompt based on intent mode and context.** (1 connections) — `app/services/screen_vision.py`
- **Main entry point. Captures screen, resolves context, calls VLM, routes…** (1 connections) — `app/services/screen_vision.py`
- **Returns the percentage of pixels that changed significantly between two frames.…** (1 connections) — `app/services/screen_vision.py`
- **Background thread body. Every WATCHER_INTERVAL_SECONDS: - Capture screen -…** (1 connections) — `app/services/screen_vision.py`
- **Capture the primary monitor using mss (~10ms). Returns (base64_jpeg_string,…** (1 connections) — `app/services/screen_vision.py`
- *... and 1 more nodes in this community*

## Relationships

- [screen_reader](screen_reader.md) (9 shared connections)
- [screen-vision + screen_vision](screen-vision_+_screen_vision.md) (4 shared connections)
- [main + screen_vision](main_+_screen_vision.md) (4 shared connections)
- [server + test_concurrency](server_+_test_concurrency.md) (1 shared connections)
- [whatsapp + dump_wa_ui](whatsapp_+_dump_wa_ui.md) (1 shared connections)
- [uia_local](uia_local.md) (1 shared connections)
- [rag_memory + memory](rag_memory_+_memory.md) (1 shared connections)
- [dark_enhancement + dark_video_enhancement](dark_enhancement_+_dark_video_enhancement.md) (1 shared connections)
- [refresh_docs](refresh_docs.md) (1 shared connections)
- [reply_generator](reply_generator.md) (1 shared connections)
- [dag_executor + planner](dag_executor_+_planner.md) (1 shared connections)
- [main](main.md) (1 shared connections)

## Source Files

- `app/services/screen_vision.py`
- `docs/features/screen-vision.md`

## Audit Trail

- EXTRACTED: 63 (95%)
- INFERRED: 3 (5%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*