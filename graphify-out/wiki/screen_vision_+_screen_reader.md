# screen_vision + screen_reader

> 62 nodes · cohesion 0.05

## Key Concepts

- **screen_vision.py** (28 connections) — `app/services/screen_vision.py`
- **screen_reader.py** (24 connections) — `app/services/screen_reader.py`
- **understand_screen()** (16 connections) — `app/services/screen_vision.py`
- **base64** (11 connections)
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
- **pil** (4 connections)
- **get_screen_screenshot_b64()** (3 connections) — `app/services/screen_reader.py`
- **_init_tesseract()** (3 connections) — `app/services/screen_reader.py`
- *... and 37 more nodes in this community*

## Relationships

- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (6 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (5 shared connections)
- [message_reader + thread_extractor](message_reader_+_thread_extractor.md) (4 shared connections)
- [assignment_answers](assignment_answers.md) (3 shared connections)
- [main + screen_vision](main_+_screen_vision.md) (3 shared connections)
- [tools + ui_inspector](tools_+_ui_inspector.md) (2 shared connections)
- [tools](tools.md) (2 shared connections)
- [social_content_manager + content-tools](social_content_manager_+_content-tools.md) (1 shared connections)
- [smart_navigator + ssml_processor](smart_navigator_+_ssml_processor.md) (1 shared connections)
- [server](server.md) (1 shared connections)
- [youtube_player](youtube_player.md) (1 shared connections)
- [fontmatch + fonts](fontmatch_+_fonts.md) (1 shared connections)

## Source Files

- `app/services/screen_reader.py`
- `app/services/screen_vision.py`
- `docs/features/screen-vision.md`

## Audit Trail

- EXTRACTED: 132 (94%)
- INFERRED: 9 (6%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*