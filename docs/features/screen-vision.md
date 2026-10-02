# Screen understanding & UI automation

## Purpose
Understand what's on screen and drive app UIs without the mouse.

## Layers (`screen_reader.read_screen`)
`screen_vision.understand_screen` (mss capture → vision model, per-app prompts, recent-screen history, intent describe/suggest/execute) → `_groq_vision_screen` → Tesseract OCR → UIA accessibility tree → window title only.

## Entry points
- Tool `read_my_screen(user_query, intent_mode)`. Keywords: "what's on my screen" (describe), "what should I do" (suggest), "fix this" (execute).
- Passive context: `describe_screen_for_llm()` is injected into chat when no tool ran.
- Background watcher: `start_background_watcher` (started in `main.startup_event` only if `GEMINI_API_KEY` is set) samples ~8 s, calls the VLM only on a large pixel diff, and queues alerts → UI polls `GET /alerts`.
- UIA (`ui_inspector.UIAEngine`, pywinauto): `click_ui_element_uia`, `type_into_ui_element`, `read_ui_element_text`, `dump_app_ui_tree`, `get_active_window_info`.

## Config
`settings.GROQ_VISION_MODEL` (default `qwen/qwen3.8-27b`; verified reading screenshots). `capture_screen_b64()` returns `(b64, np_array)`. Note it's a tuple.

## Gotchas
- `_call_gemini_vision` is a legacy name; it calls Groq.
- Screenshots are downscaled to 1280 px width, JPEG q70.

## Graphify
`graphify explain "understand_screen"` · `graphify explain "UIAEngine"`

<!-- AUTO:BEGIN (scripts/refresh_docs.py) -->
## Files & symbols (auto-generated, line numbers are current)

- `app/services/screen_vision.py` (512 lines): screen_vision.py — Jarvis VLM Screen Understanding (Layer 1 Upgrade)
  L42 VISION_MODEL · L43 REASON_MODEL · L75 DIFF_THRESHOLD_PERCENT · L76 WATCHER_INTERVAL_SECONDS · L77 WATCHER_STARTUP_DELAY · L82 capture_screen_b64() · L112 _get_active_window_title() · L123 _get_active_process_name() · L136 _resolve_app_prompt() · L145 _build_history_context() · L163 _call_gemini_vision() · L198 _call_gemma_reasoning() · L234 INTENT_DESCRIBE · L235 INTENT_SUGGEST · L236 INTENT_EXECUTE · L238 _classify_intent() · L274 _build_system_prompt() · L316 understand_screen() · L395 describe_screen_vlm() · L405 _pixel_diff_percent() · L420 _watcher_loop() · L481 start_background_watcher() · L506 stop_background_watcher()
- `app/services/screen_reader.py` (329 lines): screen_reader.py — Jarvis Screen Vision (VLM-first architecture)
  L37 _TESSERACT_PATHS · L47 _init_tesseract() · L68 _vlm_screen() · L84 _groq_vision_screen() · L125 _ocr_screen() · L152 _accessibility_tree() · L169 _window_title_only() · L184 read_screen() · L222 describe_screen_for_llm() · L243 read_screen_as_tool() · L310 get_screen_screenshot_b64()
- `app/services/ui_inspector.py` (430 lines): ui_inspector.py — Jarvis UIA Engine (Upgraded)
  L34 class UIAEngine · (L52 .get_window, L66 .get_foreground_window, L84 .find_element, L117 .find_element_fuzzy, L140 .invoke, L160 .set_value, L180 .get_text, L194 .dump_tree) · L232 click_ui_element() · L245 smart_click() · L290 type_into_element() · L322 read_element_text() · L347 debug_ui_tree() · L375 get_active_window_info() · L416 get_screen_text_summary()
- `app/services/tools.py` (1217 lines): Jarvis Tool Registry — All callable actions Jarvis can perform.  *(filtered to this feature)*
  L31 read_my_screen() · L645 read_active_window_text() · L655 click_ui_element_uia() · L676 type_into_ui_element() · L696 read_ui_element_text() · L714 dump_app_ui_tree()
<!-- AUTO:END -->
