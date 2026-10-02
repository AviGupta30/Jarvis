# screen_vision + screen_reader

> 64 nodes · cohesion 0.05

## Key Concepts

- **screen_vision.py** (28 connections) — `app/services/screen_vision.py`
- **screen_reader.py** (24 connections) — `app/services/screen_reader.py`
- **understand_screen()** (16 connections) — `app/services/screen_vision.py`
- **logging** (14 connections)
- **acoustic_tripwire.py** (11 connections) — `app/services/acoustic_tripwire.py`
- **read_screen()** (10 connections) — `app/services/screen_reader.py`
- **_watcher_loop()** (9 connections) — `app/services/screen_vision.py`
- **describe_screen_for_llm()** (8 connections) — `app/services/screen_reader.py`
- **read_screen_as_tool()** (8 connections) — `app/services/screen_reader.py`
- **Screen understanding & UI automation** (8 connections) — `docs/features/screen-vision.md`
- **numpy** (8 connections)
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
- *... and 39 more nodes in this community*

## Relationships

- [smart_navigator + rag_memory](smart_navigator_+_rag_memory.md) (11 shared connections)
- [server + test_concurrency](server_+_test_concurrency.md) (5 shared connections)
- [persistence + engine](persistence_+_engine.md) (5 shared connections)
- [acoustic_tripwire](acoustic_tripwire.md) (4 shared connections)
- [safe_executor + ui_inspector](safe_executor_+_ui_inspector.md) (4 shared connections)
- [chat + llm](chat_+_llm.md) (4 shared connections)
- [main + screen_vision](main_+_screen_vision.md) (4 shared connections)
- [main](main.md) (3 shared connections)
- [chat-routing + chat](chat-routing_+_chat.md) (2 shared connections)
- [tools](tools.md) (2 shared connections)
- [voice](voice.md) (2 shared connections)
- [dark_enhancement + dark_video_enhancement](dark_enhancement_+_dark_video_enhancement.md) (2 shared connections)

## Source Files

- `app/services/acoustic_tripwire.py`
- `app/services/screen_reader.py`
- `app/services/screen_vision.py`
- `docs/features/screen-vision.md`

## Audit Trail

- EXTRACTED: 149 (94%)
- INFERRED: 9 (6%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*