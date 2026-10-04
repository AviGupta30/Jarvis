# screen_reader

> 23 nodes · cohesion 0.13

## Key Concepts

- **screen_reader.py** (24 connections) — `app/services/screen_reader.py`
- **read_screen()** (10 connections) — `app/services/screen_reader.py`
- **describe_screen_for_llm()** (8 connections) — `app/services/screen_reader.py`
- **_groq_vision_screen()** (5 connections) — `app/services/screen_reader.py`
- **describe_screen_vlm()** (5 connections) — `app/services/screen_vision.py`
- **_accessibility_tree()** (4 connections) — `app/services/screen_reader.py`
- **_ocr_screen()** (4 connections) — `app/services/screen_reader.py`
- **_vlm_screen()** (4 connections) — `app/services/screen_reader.py`
- **Layers (`screen_reader.read_screen`)** (4 connections) — `docs/features/screen-vision.md`
- **get_screen_screenshot_b64()** (3 connections) — `app/services/screen_reader.py`
- **_init_tesseract()** (3 connections) — `app/services/screen_reader.py`
- **_window_title_only()** (3 connections) — `app/services/screen_reader.py`
- **screen_reader.py — Jarvis Screen Vision (VLM-first architecture)…** (1 connections) — `app/services/screen_reader.py`
- **Legacy OCR layer. Works on any app but extracts raw text only — no layout,…** (1 connections) — `app/services/screen_reader.py`
- **Reads the active window's accessibility tree. Works best for native Win32 apps.…** (1 connections) — `app/services/screen_reader.py`
- **Always works — returns at minimum the active window title.** (1 connections) — `app/services/screen_reader.py`
- **Main function — returns the richest available description of the screen.…** (1 connections) — `app/services/screen_reader.py`
- **Returns a clean, LLM-optimized description of the current screen. Used as…** (1 connections) — `app/services/screen_reader.py`
- **Takes a screenshot and returns it as a base64-encoded JPEG string. Used as…** (1 connections) — `app/services/screen_reader.py`
- **Find and configure pytesseract. Returns True if ready.** (1 connections) — `app/services/screen_reader.py`
- **Primary layer: sends screenshot to Gemini 2.0 Flash VLM. Returns rich…** (1 connections) — `app/services/screen_reader.py`
- **Fallback vision layer using Groq LLaVA. Faster (~200ms) but weaker at complex…** (1 connections) — `app/services/screen_reader.py`
- **Lightweight passive description — used as context injection in chat.py. Always…** (1 connections) — `app/services/screen_vision.py`

## Relationships

- [server + persistence](server_+_persistence.md) (4 shared connections)
- [screen_vision](screen_vision.md) (4 shared connections)
- [tools + ui_inspector](tools_+_ui_inspector.md) (3 shared connections)
- [screen_reader + screen_vision](screen_reader_+_screen_vision.md) (3 shared connections)
- [jarvis_overlay + prompt_overlay](jarvis_overlay_+_prompt_overlay.md) (2 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (2 shared connections)
- [assignment_assembler + smart_navigator](assignment_assembler_+_smart_navigator.md) (1 shared connections)
- [assignment_humanizer](assignment_humanizer.md) (1 shared connections)
- [dump_wa_ui + find_call_btn](dump_wa_ui_+_find_call_btn.md) (1 shared connections)
- [chat](chat.md) (1 shared connections)
- [llm-personality + ARCHITECTURE](llm-personality_+_ARCHITECTURE.md) (1 shared connections)
- [screen-vision + screen_vision](screen-vision_+_screen_vision.md) (1 shared connections)

## Source Files

- `app/services/screen_reader.py`
- `app/services/screen_vision.py`
- `docs/features/screen-vision.md`

## Audit Trail

- EXTRACTED: 50 (89%)
- INFERRED: 6 (11%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*