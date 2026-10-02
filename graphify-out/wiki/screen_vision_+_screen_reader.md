# screen_vision + screen_reader

> 57 nodes · cohesion 0.05

## Key Concepts

- **screen_reader.py** (24 connections) — `app/services/screen_reader.py`
- **understand_screen()** (16 connections) — `app/services/screen_vision.py`
- **read_screen()** (10 connections) — `app/services/screen_reader.py`
- **_watcher_loop()** (9 connections) — `app/services/screen_vision.py`
- **describe_screen_for_llm()** (8 connections) — `app/services/screen_reader.py`
- **read_screen_as_tool()** (8 connections) — `app/services/screen_reader.py`
- **Screen understanding & UI automation** (8 connections) — `docs/features/screen-vision.md`
- **_call_gemini_vision()** (7 connections) — `app/services/screen_vision.py`
- **capture_screen_b64()** (6 connections) — `app/services/screen_vision.py`
- **_groq_vision_screen()** (5 connections) — `app/services/screen_reader.py`
- **_classify_intent()** (5 connections) — `app/services/screen_vision.py`
- **describe_screen_vlm()** (5 connections) — `app/services/screen_vision.py`
- **_accessibility_tree()** (4 connections) — `app/services/screen_reader.py`
- **_ocr_screen()** (4 connections) — `app/services/screen_reader.py`
- **_vlm_screen()** (4 connections) — `app/services/screen_reader.py`
- **_get_active_process_name()** (4 connections) — `app/services/screen_vision.py`
- **_get_active_window_title()** (4 connections) — `app/services/screen_vision.py`
- **_pixel_diff_percent()** (4 connections) — `app/services/screen_vision.py`
- **_resolve_app_prompt()** (4 connections) — `app/services/screen_vision.py`
- **Layers (`screen_reader.read_screen`)** (4 connections) — `docs/features/screen-vision.md`
- **get_screen_screenshot_b64()** (3 connections) — `app/services/screen_reader.py`
- **_init_tesseract()** (3 connections) — `app/services/screen_reader.py`
- **_window_title_only()** (3 connections) — `app/services/screen_reader.py`
- **_build_history_context()** (3 connections) — `app/services/screen_vision.py`
- **_build_system_prompt()** (3 connections) — `app/services/screen_vision.py`
- *... and 32 more nodes in this community*

## Relationships

- [social_content_manager + ui_inspector](social_content_manager_+_ui_inspector.md) (19 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (5 shared connections)
- [safe_executor + ui_inspector](safe_executor_+_ui_inspector.md) (2 shared connections)
- [message_reader + reply_generator](message_reader_+_reply_generator.md) (2 shared connections)
- [tools + ui_inspector](tools_+_ui_inspector.md) (2 shared connections)
- [tools](tools.md) (2 shared connections)
- [file_ops](file_ops.md) (2 shared connections)
- [memory + main](memory_+_main.md) (1 shared connections)

## Source Files

- `app/services/screen_reader.py`
- `app/services/screen_vision.py`
- `docs/features/screen-vision.md`

## Audit Trail

- EXTRACTED: 106 (92%)
- INFERRED: 9 (8%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*