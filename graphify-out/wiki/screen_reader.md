# screen_reader

> 29 nodes · cohesion 0.11

## Key Concepts

- **screen_reader.py** (24 connections) — `app/services/screen_reader.py`
- **understand_screen()** (16 connections) — `app/services/screen_vision.py`
- **read_screen()** (10 connections) — `app/services/screen_reader.py`
- **describe_screen_for_llm()** (8 connections) — `app/services/screen_reader.py`
- **read_screen_as_tool()** (8 connections) — `app/services/screen_reader.py`
- **_groq_vision_screen()** (5 connections) — `app/services/screen_reader.py`
- **_classify_intent()** (5 connections) — `app/services/screen_vision.py`
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
- **Tool-callable version — called when user asks 'what's on my screen?' Routes…** (1 connections) — `app/services/screen_reader.py`
- **Takes a screenshot and returns it as a base64-encoded JPEG string. Used as…** (1 connections) — `app/services/screen_reader.py`
- **Find and configure pytesseract. Returns True if ready.** (1 connections) — `app/services/screen_reader.py`
- **Primary layer: sends screenshot to Gemini 2.0 Flash VLM. Returns rich…** (1 connections) — `app/services/screen_reader.py`
- *... and 4 more nodes in this community*

## Relationships

- [screen_vision](screen_vision.md) (7 shared connections)
- [voice_agent + download_kokoro](voice_agent_+_download_kokoro.md) (6 shared connections)
- [tools](tools.md) (5 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (4 shared connections)
- [message_reader + thread_extractor](message_reader_+_thread_extractor.md) (3 shared connections)
- [screen-vision + screen_vision](screen-vision_+_screen_vision.md) (2 shared connections)
- [repair + assignment_humanizer](repair_+_assignment_humanizer.md) (1 shared connections)
- [jarvis_overlay](jarvis_overlay.md) (1 shared connections)
- [dag_executor + planner](dag_executor_+_planner.md) (1 shared connections)

## Source Files

- `app/services/screen_reader.py`
- `app/services/screen_vision.py`
- `docs/features/screen-vision.md`

## Audit Trail

- EXTRACTED: 69 (92%)
- INFERRED: 6 (8%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*