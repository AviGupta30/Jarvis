# screen_reader

> 25 nodes · cohesion 0.11

## Key Concepts

- **screen_reader.py** (24 connections) — `app/services/screen_reader.py`
- **read_screen()** (10 connections) — `app/services/screen_reader.py`
- **io** (10 connections)
- **base64** (9 connections)
- **read_screen_as_tool()** (8 connections) — `app/services/screen_reader.py`
- **_groq_vision_screen()** (5 connections) — `app/services/screen_reader.py`
- **_classify_intent()** (5 connections) — `app/services/screen_vision.py`
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
- **Tool-callable version — called when user asks 'what's on my screen?' Routes…** (1 connections) — `app/services/screen_reader.py`
- **Takes a screenshot and returns it as a base64-encoded JPEG string. Used as…** (1 connections) — `app/services/screen_reader.py`
- **Find and configure pytesseract. Returns True if ready.** (1 connections) — `app/services/screen_reader.py`
- **Primary layer: sends screenshot to Gemini 2.0 Flash VLM. Returns rich…** (1 connections) — `app/services/screen_reader.py`
- **Fallback vision layer using Groq LLaVA. Faster (~200ms) but weaker at complex…** (1 connections) — `app/services/screen_reader.py`
- **Parse the user's phrasing to determine the response mode. describe → "What am I…** (1 connections) — `app/services/screen_vision.py`

## Relationships

- [screen_vision](screen_vision.md) (9 shared connections)
- [main + screen_vision](main_+_screen_vision.md) (5 shared connections)
- [whatsapp + dump_wa_ui](whatsapp_+_dump_wa_ui.md) (2 shared connections)
- [chat + llm](chat_+_llm.md) (2 shared connections)
- [tools](tools.md) (2 shared connections)
- [assignment_answers](assignment_answers.md) (2 shared connections)
- [assignment_tool](assignment_tool.md) (2 shared connections)
- [agentic_web](agentic_web.md) (1 shared connections)
- [ssml_processor + debug_wa](ssml_processor_+_debug_wa.md) (1 shared connections)
- [rag_memory + memory](rag_memory_+_memory.md) (1 shared connections)
- [assignment_humanizer](assignment_humanizer.md) (1 shared connections)
- [gmail_tool](gmail_tool.md) (1 shared connections)

## Source Files

- `app/services/screen_reader.py`
- `app/services/screen_vision.py`
- `docs/features/screen-vision.md`

## Audit Trail

- EXTRACTED: 70 (96%)
- INFERRED: 3 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*