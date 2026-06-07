# JARVIS 2.0 SYSTEM ARCHITECTURE
**Core Directive:** Jarvis is a proactive, autonomous Windows 11 AI assistant. All components MUST remain strictly isolated. Tools do not import other tools.

## 1. System Overview
*   **Backend:** FastAPI (`Main.py`, `chat.py`)
*   **LLM Brain:** `llm.py` (Routing/Fast responses via Groq LLaMA 3.3 70B), `planner.py` (Complex multi-step reasoning via Gemma 4/Gemini 1.5 Flash).
*   **Vision Stack:** `screen_vision.py` (Gemini 2.0 Flash VLM), `screen_reader.py` (Fallback OCR/Vision), `ui_inspector.py` (Windows UIA native accessibility tree). Includes a passive background screen watcher.
*   **Voice & Personality Stack:** `voice.py` (Local faster-whisper STT + ElevenLabs TTS), `personality.py`, `context_classifier.py`, `hinglish_normalizer.py`, `ssml_processor.py` (Dynamic mood, Hinglish support, SSML natural pauses).
*   **Memory Stack:** `memory_tool.py` (Persistent JSON facts), `embeddings.py` (fastembed ONNX), `vector_score.py` (pgvector).
*   **Dynamic Execution:** `dynamic_tool.py`, `safe_executer.py` (AST-sandboxed Python execution for on-the-fly skills).

## 2. Tool Registry (`tools.py`)
This is the central hub. The LLM router ONLY sees the functions registered here. 
*   **System & OS:** `take_screenshot`, `snap_windows`, `close_window`, `adjust_active_window`, `volume_up/down/mute`, `lock_screen`, `get_system_info`, `get_system_time`.
*   **App Control:** `open_app`, `open_windows_copilot`, `send_to_copilot`.
*   **UI Automation (Mouse-free):** `click_ui_element_uia`, `type_into_ui_element`, `read_ui_element_text`, `dump_app_ui_tree`.
*   **Web & Browsing:** `smart_web_action` (Isolated navigator), `browse_and_read`, `search_on_site`, `scrape_url`, `get_info` (DuckDuckGo + Wikipedia + wttr.in), `youtube_search`.
*   **File System (`file_ops.py`):** `read_file` (TXT/PDF/DOCX), `write_file`, `list_directory`, `move_file`, `delete_file` (send2trash), `create_word_doc`.
*   **Content & Document Generation:**
    *   **PPT Generator:** Can autonomously create PowerPoint presentations from scratch on a given topic (e.g., "create a ppt on X").
    *   **Assignment Solver:** Can read assignment Word files, use Gemini to generate answers, and output a new completed Word file.
    *   **Content Humanizer:** Basic text humanizer tool to make AI-generated content sound more natural and partially bypass AI detection.
*   **Utilities & Enhancements:**
    *   **Prompt Enhancer:** Triggered globally via `Ctrl+Space`. Opens an interface where the user can type a basic prompt and instantly receive an enhanced, optimized prompt.
*   **Integrations:** 
    *   **WhatsApp (`whatsapp_smart.py`):** `search_whatsapp_contact`, `initiate_whatsapp_send`, `confirm_whatsapp_send`, `read_whatsapp_messages`.
    *   **Gmail (`gmail_tool.py`):** `check_emails`, `list_unread`, `summarize_inbox`.
    *   **Calendar (`calendar_tool.py`):** `check_today_schedule`, `get_upcoming_events`, `add_event`.

## 3. Strict Development Rules
1.  **Absolute Isolation:** A tool module (e.g., `gmail_tool.py`) CANNOT import from another tool module (e.g., `file_ops.py`). If a complex task requires both, the `planner.py` Agent orchestrates them via `tools.py`.
2.  **Failsafe Execution:** Every tool must wrap its core logic in `try/except` blocks and return a human-readable string explaining success or failure. NEVER crash the FastAPI server.
3.  **Zero State:** Tools must be stateless. Rely on `memory_tool.py` for persistence.
4.  **Universal Connectivity & Isolation:** Each new function/skill MUST be isolated in its own separate file. Furthermore, every function must be designed to connect to BOTH the frontend UI and `voice.py` simultaneously via the unified `/chat` backend route. Do not implement features that only work for one interface.