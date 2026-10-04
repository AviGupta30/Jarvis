# screen_vision + screen_reader

> 63 nodes · cohesion 0.05

## Key Concepts

- **screen_vision.py** (28 connections) — `app/services/screen_vision.py`
- **screen_reader.py** (24 connections) — `app/services/screen_reader.py`
- **understand_screen()** (16 connections) — `app/services/screen_vision.py`
- **read_screen()** (10 connections) — `app/services/screen_reader.py`
- **get_active_window_info()** (10 connections) — `app/services/ui_inspector.py`
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
- *... and 38 more nodes in this community*

## Relationships

- [tools](tools.md) (7 shared connections)
- [benchmark + server](benchmark_+_server.md) (6 shared connections)
- [chat + llm](chat_+_llm.md) (4 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (4 shared connections)
- [safe_executor](safe_executor.md) (3 shared connections)
- [main + screen_vision](main_+_screen_vision.md) (3 shared connections)
- [repair + renderer](repair_+_renderer.md) (2 shared connections)
- [file_ops](file_ops.md) (2 shared connections)
- [assignment_assembler + smart_navigator](assignment_assembler_+_smart_navigator.md) (1 shared connections)
- [whatsapp + dump_wa_ui](whatsapp_+_dump_wa_ui.md) (1 shared connections)
- [chat + chat-routing](chat_+_chat-routing.md) (1 shared connections)
- [youtube_player](youtube_player.md) (1 shared connections)

## Source Files

- `app/services/screen_reader.py`
- `app/services/screen_vision.py`
- `app/services/ui_inspector.py`
- `docs/features/screen-vision.md`

## Audit Trail

- EXTRACTED: 129 (92%)
- INFERRED: 11 (8%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*