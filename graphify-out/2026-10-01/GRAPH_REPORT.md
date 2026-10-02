# Graph Report - Jarvis  (2026-10-01)

## Corpus Check
- 187 files · ~234,700 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 3, .css 3, .bat 1)

## Summary
- 3134 nodes · 6652 edges · 157 communities (132 shown, 25 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 674 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e0271761`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Tool registry
- style_profiler.py
- assignment_tool.py
- Flow (`scripts/voice_agent.py`)
- ppt_chart_engine
- main.py
- window_layout.py
- CacheEngine
- youtube_control.py
- syllabus_auditor.py
- ppt_studio.py
- DeckRenderer
- browser_tool.py
- youtube_player.py
- file_ops.py
- PresentationBuilder
- assignment_answers
- ppt_content.py
- skill_prompt_enhancer.py
- prompt_enhancer_button.py
- extract_thread
- chat.py
- ppt_research.py
- ppt_template.py
- get_engine
- ppt_router.py
- package
- gestureController + gestureInterpreter
- resume_builder.py
- ppt_image_engine
- json
- ppt_composer.py
- DSAEnforcer
- generate_deck
- gmail_tool.py
- PromptOverlay
- ui_inspector
- agentic_web.py
- parse_youtube_followup
- time
- voice_agent
- transformEngine
- refresh_docs.py
- air-drawing + air_drawing_tool
- ppt_designer.py
- voice.py
- package + App
- AcousticWakeEngine
- assignment_humanizer.py
- render_sections
- CacheClient
- interactionEngine + DrawingCanvas
- Key pieces
- package
- strokeManager
- pyautogui
- llm.py
- safe_executor.py
- reply_generator.py
- web_search.py
- content_humanizer.py
- jarvis_overlay.py
- Assignment solver (5 phases)
- ppt_create
- whatsapp_smart
- frontend
- shapeManager
- CacheServer
- spotify_service.py
- prompt_enhancer_button
- Speaker
- drawingEngine
- message_reader.py
- test_lru
- test_lru
- resume_detector.py
- re
- Element
- voice_agent.py
- ._run
- package
- handTracking
- Node
- screen_reader.py
- 2. Tool Registry (`tools.py`)
- _worker
- ControlPanel + HandSkeleton
- strokeRefiner
- ppt_chart_engine
- LRUCache
- assignment_pipeline
- prompt_enhancer_button
- whatsapp_call
- ssml_processor
- assignment_assembler + assignment_pipeline
- CODEMAP
- youtube_windows
- Architecture
- screen-vision + screen_vision
- hinglish_normalizer.py
- README
- package
- startup_event
- TestBasicOps
- Entry points
- ppt_tool.py
- youtube_player
- dsa_enforcer.py
- youtube_control
- send_style_reply
- Chat pipeline & routing (/chat)
- README
- ppt_tool
- __init__
- README
- _Player
- browser_mail
- PROMPT_TEMPLATE
- smart_navigator
- FEATURES
- MicListener
- extract_questions
- ppt_tool
- whatsapp
- screen_vision.py
- ppt_edit
- persistence
- Neural cache (Redis-like LRU server)
- dag_executor.py
- detect_language
- Flow — create (`ppt_tool.ppt_create` → `ppt_studio.create`, a generator)
- test_builder
- edge_tts
- pygame
- DSA / LeetCode enforcer mode
- tools + ui_inspector
- benchmark
- Syllabus auditor (YouTube playlist vs syllabus)
- tripwire_status
- _resolve_pdf_path
- PowerPoint generator
- api/memory.py
- run_tool
- TestTTL
- Web search, research & browser automation
- TestO1Timing
- TestSentinels
- get_wake_event
- small_cache
- _pick
- _corner_L
- Voice: STT, TTS, wake word, clap wake, overlay
- _window_rect

## God Nodes (most connected - your core abstractions)
1. `Tool registry` - 123 edges
2. `chat_endpoint()` - 49 edges
3. `DeckRenderer` - 49 edges
4. `Key pieces` - 49 edges
5. `text()` - 41 edges
6. `create()` - 34 edges
7. `2. Tool Registry (`tools.py`)` - 34 edges
8. `box()` - 32 edges
9. `PresentationBuilder` - 32 edges
10. `EnhanceButton` - 29 edges

## Surprising Connections (you probably didn't know these)
- `Change recipes` --references--> `keyword_detect_tool()`  [INFERRED]
  docs/features/chat-routing.md → app/api/chat.py
- `Adding a tool (checklist)` --references--> `keyword_detect_tool()`  [INFERRED]
  docs/features/tool-registry.md → app/api/chat.py
- `Gotchas` --references--> `recall_memory()`  [INFERRED]
  docs/features/memory.md → app/api/memory.py
- `Calendar` --references--> `check_today_schedule()`  [INFERRED]
  docs/features/email-calendar.md → app/services/calendar_tool.py
- `Flow` --references--> `get_dsa_enforcer()`  [INFERRED]
  docs/features/dsa-mode.md → app/services/dsa_enforcer.py

## Import Cycles
- None detected.

## Communities (157 total, 25 thin omitted)

### Community 0 - "Tool registry"
Cohesion: 0.03
Nodes (83): get_styles(), get, Return all available design personalities., ppt_styles(), append_to_file(), cache_get(), cache_set(), calculate() (+75 more)

### Community 1 - "style_profiler.py"
Cohesion: 0.13
Nodes (25): build_style_profile(), One-time training: parse a WhatsApp .txt chat export to build your personal…, add_deflection_phrase(), build_style_profile(), _compute_profile_stats(), _empty_profile(), get_profile_summary(), _load_profile() (+17 more)

### Community 2 - "assignment_tool.py"
Cohesion: 0.15
Nodes (19): _classify_question_type(), _clean_text(), _extract_marks(), _extract_via_vision(), _has_figure_reference(), _parse_llm_json_response(), _pdf_pages_to_images(), Jarvis Assignment Tool — Phase 1: Smart Question Extractor… (+11 more)

### Community 3 - "Flow (`scripts/voice_agent.py`)"
Cohesion: 0.25
Nodes (7): loanword_ratio(), Share of Devanagari words that are English loanwords ("ओपन क्रोम" → 1.0). High…, _reply_language_note(), language_mismatch(), True if a reply sentence is in the other language than the one the user spoke., Loudest output RMS in the last `window` s — the voice agent's echo reference., Flow (`scripts/voice_agent.py`)

### Community 4 - "ppt_chart_engine"
Cohesion: 0.13
Nodes (33): _bg_color(), _extract_strict_metric(), _fig_to_bytes(), _hex(), _metrics_to_bar(), _palette_colors(), ppt_chart_engine.py — Dynamic Data-Visualization Engine for JARVIS PPT…, Horizontal or vertical bar chart. (+25 more)

### Community 5 - "main.py"
Cohesion: 0.11
Nodes (21): aiomysql, close_mysql(), init_mysql(), mysql_db.py — Jarvis Async MySQL Connection Pool…, Gracefully close the MySQL connection pool on server shutdown., Initialize the MySQL connection pool and ensure all required tables exist. Safe…, Stop watcher, acoustic tripwire, and close DB pool cleanly on server shutdown., shutdown_event() (+13 more)

### Community 6 - "window_layout.py"
Cohesion: 0.07
Nodes (46): True if the Spotify desktop app has a window (cheap: EnumWindows, no UIA)., spotify_running(), close_specific_window(), close_tab(), _find_window_fuzzy(), focus_window(), minimize_window(), Closes the current browser tab using Ctrl+W, targeting the real foreground app. (+38 more)

### Community 7 - "CacheEngine"
Cohesion: 0.06
Nodes (36): CacheEngine, Any, Route a command dict to the appropriate handler. All handlers return a response…, Owns the LRUCache. Runs a single consumer loop on a dedicated thread. External…, Spawn the single writer thread. Call once at server boot., Gracefully stop the engine writer thread., The single consumer loop. Runs on CacheEngineThread. Processes one command at a…, decode_message() (+28 more)

### Community 8 - "youtube_control.py"
Cohesion: 0.12
Nodes (31): _end_session(), _find_channel(), _find_channel_at(), walk(), _format_results(), _initial_data(), _load(), _mark_last() (+23 more)

### Community 9 - "syllabus_auditor.py"
Cohesion: 0.09
Nodes (35): _approx_token_count(), _assemble_response(), audit_playlist_syllabus(), _build_vector_store(), _chunk_transcript(), _coverage_level(), _embed_texts(), _extract_playlist_id() (+27 more)

### Community 10 - "ppt_studio.py"
Cohesion: 0.09
Nodes (38): parse_instructions(), Separate the user's command, any pasted/attached content and attachment paths., slide 2' / 'second slide' / 'slide two' / 'the solution slide' → slide number., Deterministic reading of the user's instructions. image_rules: [{"images":…, [(n, heading, raw content)] split on 'Slide N:' markers of repaired text., raw_slide_blocks(), slide_count(), _slide_ref() (+30 more)

### Community 11 - "DeckRenderer"
Cohesion: 0.12
Nodes (26): _compact_header(), box(), DeckRenderer, fit_size(), gradient_box(), _items(), line_shape(), para_h() (+18 more)

### Community 12 - "browser_tool.py"
Cohesion: 0.20
Nodes (22): browse_and_paginate(), browse_and_read(), _clean_text(), click_element(), _ensure_url(), fill_form(), _llm_extract(), _new_browser_page() (+14 more)

### Community 13 - "youtube_player.py"
Cohesion: 0.11
Nodes (36): _address_bar_value(), _clip_get(), _clip_restore(), _clip_set(), current_video_info(), _fallback(), fmt_span(), fmt_time() (+28 more)

### Community 14 - "file_ops.py"
Cohesion: 0.10
Nodes (27): append_file(), bulk_rename(), create_folder(), delete_file(), diff_files(), _fmt_size(), list_directory(), _maybe_summarize() (+19 more)

### Community 15 - "PresentationBuilder"
Cohesion: 0.19
Nodes (17): _clean_image_path(), _oval(), _parse_bullet(), _parse_card(), PresentationBuilder, _frame(), Render a single image with CONTAIN-FIT (object-fit: contain). The image is…, Fluid split layout that adapts natively to image aspect ratio: • Landscape… (+9 more)

### Community 16 - "assignment_answers"
Cohesion: 0.15
Nodes (20): _ask_question_on_page(), _find_input(), _get_persistent_page(), Jarvis Assignment Tool — Phase 2: Answer Generation…, Launch a visible (non-headless) Chromium with a persistent profile. Login…, Try CSS selectors to find the visible chat input. Returns locator or None., Type a message into the AI chat input and submit it., Upload PDF to the AI chat page. Returns True if upload was initiated. (+12 more)

### Community 17 - "ppt_content.py"
Cohesion: 0.08
Nodes (44): apply_edit(), apply_structure(), architect_slides(), ask(), _retry(), run(), _as_dated(), _as_stat() (+36 more)

### Community 18 - "skill_prompt_enhancer.py"
Cohesion: 0.17
Nodes (19): check_for_hallucination(), clean_output(), detect_domain(), is_bloated(), protect_blocks(), prompt_enhancement_library.py…, Replace ``` fenced blocks with [[BLOCK_n]] placeholders., Put protected blocks back; append any the model dropped. (+11 more)

### Community 19 - "prompt_enhancer_button.py"
Cohesion: 0.10
Nodes (27): _acquire_single_instance(), _app_title_match(), _browser_url(), classify_app(), _exe_name(), install_autostart(), _load_state(), main() (+19 more)

### Community 20 - "extract_thread"
Cohesion: 0.33
Nodes (6): extract_thread(), _find_latest_incoming(), _group_into_turns(), Merges consecutive messages from the same sender into a single turn. This makes…, Scans the thread from the end to find the most recent message from 'them' —…, Main entry point. Opens the contact's chat and extracts a structured thread.…

### Community 21 - "chat.py"
Cohesion: 0.05
Nodes (63): chat_endpoint(), _dag_stream_with_history(), planner_stream(), response_stream_with_history(), resume_stream(), tool_stream(), ChatRequest, _clean_yt_query() (+55 more)

### Community 22 - "ppt_research.py"
Cohesion: 0.12
Nodes (32): plan_queries(), 4-6 web queries covering the angles a deck on `topic` needs. Templates, not an…, Web + Wikipedia → verified facts. [] when offline (the deck is then written…, research_facts(), allowed_numbers(), _anchors(), audit_slide(), _clean_html() (+24 more)

### Community 23 - "ppt_template.py"
Cohesion: 0.06
Nodes (59): prepare_image(), Return a PPTX-safe copy (EXIF-rotated, RGB, ≤2400px, png/jpg) and its aspect., Edge-energy profile along an axis ('x' or 'y') for smart cropping., _saliency_profile(), analyze_format(), _analyze_slide(), classify_box(), _clear() (+51 more)

### Community 24 - "get_engine"
Cohesion: 0.20
Nodes (12): post, Arm the acoustic tripwire so double-claps wake Jarvis., Disarm the acoustic tripwire (engine keeps running, just paused)., Schedule an ambient-noise recalibration pass. The engine samples the mic for ~2…, Upload a file to the data/uploads folder for Jarvis to process., tripwire_calibrate(), tripwire_disable(), tripwire_enable() (+4 more)

### Community 25 - "ppt_router.py"
Cohesion: 0.19
Nodes (15): build_ppt(), create_ppt_backend(), generate(), extract_theme(), PPTBuildRequest, PPTCreateRequest, PPTExtractThemeRequest, PPTStylesResponse (+7 more)

### Community 26 - "package"
Cohesion: 0.11
Nodes (20): name, private, type, version, autoprefixer, eslint, ref_eslint_config, @eslint/js (+12 more)

### Community 28 - "resume_builder.py"
Cohesion: 0.05
Nodes (86): _analyse_design(), _apply_color(), _apply_layout_answer(), _attachments(), _build_content(), _closest_preset(), _competencies_html(), _contact_html() (+78 more)

### Community 29 - "ppt_image_engine"
Cohesion: 0.16
Nodes (18): build_image_descriptors(), _extract_keywords(), get_aspect_ratio(), ImageDescriptor, match_images_to_slides(), _parse_slide_ref(), _parse_slide_ref_by_title(), ppt_image_engine.py — Semantic Image-Slide Matcher for JARVIS PPT Engine… (+10 more)

### Community 30 - "json"
Cohesion: 0.07
Nodes (34): _extract_topics(), _get_faiss_lock(), Lock, rag_memory.py — Jarvis Long-Term RAG Memory Engine…, Persist FAISS index and ID map to disk (sync, runs in thread executor)., Run the sync FAISS save in a thread pool to avoid blocking the event loop., Lightweight keyword-based topic extraction (no LLM call). Returns a CSV of the…, Lazily create the FAISS lock inside a running event loop. (+26 more)

### Community 31 - "ppt_composer.py"
Cohesion: 0.14
Nodes (41): _balanced_rows(), _body_cards(), _body_fields(), _body_list(), _body_paragraph(), _body_stats(), _body_steps(), _body_table() (+33 more)

### Community 32 - "DSAEnforcer"
Cohesion: 0.28
Nodes (4): _cache_set(), DSAEnforcer, Write to Neural Cache, silently skipping if unavailable., Flow

### Community 33 - "generate_deck"
Cohesion: 0.10
Nodes (31): _budget_left(), _compact(), _content_prompt(), _flatten(), _gemini_json(), generate_deck(), _is_note(), run() (+23 more)

### Community 34 - "gmail_tool.py"
Cohesion: 0.07
Nodes (44): check_emails(), _decode_body(), _format_date(), get_email_body(), _get_gmail_service(), _get_header(), list_unread(), gmail_tool.py — Jarvis Gmail Integration (Step 5)… (+36 more)

### Community 35 - "PromptOverlay"
Cohesion: 0.14
Nodes (3): main(), PromptOverlay, Strip the **ENHANCED PROMPT (CODING):** header if present.

### Community 36 - "ui_inspector"
Cohesion: 0.10
Nodes (11): Walk all descendants looking for any control whose window_text contains `text`…, Fire an element's primary action via UIA Invoke pattern. No mouse movement —…, Inject text into an input element via UIA Value pattern. No simulated…, Read text from an element via UIA TextPattern or window_text. Returns empty…, Walk the accessibility tree and return all elements up to `depth` levels. Use…, Core wrapper around pywinauto's UIA backend. All interactions go through the OS…, Get a window wrapper by partial title match (regex-safe). Returns None if not…, Get the currently focused window via Win32 HWND matching. (+3 more)

### Community 37 - "agentic_web.py"
Cohesion: 0.06
Nodes (33): agentic_web_action(), _worker(), _build_search_queries(), _fetch_page_text(), __init__(), _get_api_key(), agentic_web.py — Smart Web Research Engine for Jarvis…, Download a page and return clean readable text (no HTML tags). (+25 more)

### Community 38 - "parse_youtube_followup"
Cohesion: 0.13
Nodes (14): _channel_name(), _is_positional(), _last_media(), _latest_of(), parse_youtube_followup(), A pick by position, not by title: 'the first result', 'number 3', 'the latest…, play mrbeast's latest video' / 'play the latest video of t series' → channel…, Channel name from a request like 'open MrBeast's channel', else None. (+6 more)

### Community 39 - "time"
Cohesion: 0.12
Nodes (23): acoustic_tripwire.py — Jarvis Acoustic Wake Engine…, prompt_overlay.py ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Jarvis…, argparse, keyboard, logging, neural_cache, benchmark.py — Neural Cache vs JSON-file Baseline (Milestone 8)…, client.py — Python Client Library for Neural Cache (Milestone 5)… (+15 more)

### Community 40 - "voice_agent"
Cohesion: 0.13
Nodes (9): AbstractEventLoop, _ClapDetector, _EnergyVAD, ndarray, Queue, Stateful frame-by-frame Silero VAD using the ONNX model bundled with faster-…, Fallback if Silero can't load: adaptive noise floor., Strict double clap. The old tripwire fired on ANY two loud 2–8 kHz frames… (+1 more)

### Community 42 - "refresh_docs.py"
Cohesion: 0.22
Nodes (12): ast, collections, fnmatch, auto_block(), _js_symbols(), label_communities(), Path, _py_symbols() (+4 more)

### Community 43 - "air-drawing + air_drawing_tool"
Cohesion: 0.18
Nodes (9): open_air_drawing(), Opens the Air Drawing Canvas on the screen. This feature allows the user to…, Air drawing (webcam hand drawing), Files & symbols (auto-generated, line numbers are current), Flow, Gotchas, Graphify, Purpose (+1 more)

### Community 44 - "ppt_designer.py"
Cohesion: 0.08
Nodes (31): _best_window(), _contrast(), count_lines(), E(), _finish_theme(), _line_factor(), _lum(), _pil_font() (+23 more)

### Community 45 - "voice.py"
Cohesion: 0.09
Nodes (30): _clean_transcript(), Clip, _finish(), _get_groq(), _groq_once(), groq_stt_available(), _load_whisper_model(), pcm_to_wav_bytes() (+22 more)

### Community 46 - "package + App"
Cohesion: 0.16
Nodes (11): App(), ChatMessage(), API_BASE, frontend_src_index, lucide-react, react, ref_react_dom_client, react-markdown (+3 more)

### Community 47 - "AcousticWakeEngine"
Cohesion: 0.12
Nodes (9): AcousticWakeEngine, Background thread that watches the microphone for a double-clap pattern. Usage…, Start the background listening thread., Signal the background thread to exit and wait for it., Resume detection after a disable()., Pause detection without stopping the thread (fast resume)., Signal the background thread to re-run calibration on the next cycle. Returns…, Override the volume threshold (used by voice_agent inline mode). (+1 more)

### Community 48 - "assignment_humanizer.py"
Cohesion: 0.11
Nodes (26): _extract_output_text(), _fill_input(), _find_element(), _get_browser_page(), humanize_all_answers(), _humanize_chunk_via_browser(), humanize_text(), _humanize_via_browser() (+18 more)

### Community 49 - "render_sections"
Cohesion: 0.11
Nodes (21): _fill(), image_block(), _image_panel(), _masonry(), How much extra height a section can absorb before it looks inflated., Framed images (no crop) + numbered captions under each. Returns used height., Boxes for the images at full column width in exactly `rows` rows (scaled down…, Balanced split of sections into columns (reading order kept inside each… (+13 more)

### Community 50 - "CacheClient"
Cohesion: 0.10
Nodes (14): Send one of the reply drafts generated by generate_reply_draft. draft_index is…, send_style_reply(), CacheClient, Any, Store a key-value pair, optionally with a TTL. Args: key: Cache key. value:…, Delete a key from the cache. Returns: True if the key existed and was deleted,…, Retrieve server statistics (hit rate, evictions, cache size, etc.). Returns…, Explicitly close the socket connection. (+6 more)

### Community 52 - "Key pieces"
Cohesion: 0.16
Nodes (22): _address_bar_focused(), com_init(), focus(), _focus_address_bar(), _focus_page(), _focused_is_toolbar(), _in_page(), _page_focused() (+14 more)

### Community 53 - "package"
Cohesion: 0.14
Nodes (14): devDependencies, autoprefixer, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, postcss (+6 more)

### Community 55 - "pyautogui"
Cohesion: 0.10
Nodes (17): _focus_or_open_whatsapp(), open_whatsapp(), WhatsApp Windows Desktop App Automation Uses the native Windows app via…, Focus the WhatsApp window or open it if not running. Returns True on success., Opens the WhatsApp desktop app., find_controls(), Dump WhatsApp Desktop UI tree to find the Voice Call button name. Run this…, search_tree() (+9 more)

### Community 56 - "llm.py"
Cohesion: 0.09
Nodes (35): is_dag_task(), Returns True when the user's request requires a multi-branch DAG plan. More…, Read and return the contents of a text file or PDF. Long files are…, read_file(), check_for_tool_intent(), generate_chat_response(), _groq_generate(), _is_complex_response() (+27 more)

### Community 57 - "safe_executor.py"
Cohesion: 0.15
Nodes (15): execute_safe(), Exception, Safe Code Executor for Jarvis ------------------------------- Runs LLM-…, Restricted open(): blocks writes to system paths., Restricted __import__: blocks dangerous modules., Raised when generated code violates safety constraints., AST visitor that inspects generated code before execution., Parse and walk the AST, raising SecurityError on violations. (+7 more)

### Community 58 - "reply_generator.py"
Cohesion: 0.15
Nodes (17): generate_reply_draft(), Read the latest WhatsApp thread with a contact and generate 3 reply drafts that…, _build_system_prompt(), _build_user_prompt(), _call_groq(), generate_reply_draft(), _get_groq_api_key(), _parse_drafts_from_response() (+9 more)

### Community 59 - "web_search.py"
Cohesion: 0.09
Nodes (32): research_scraper.py — Autonomous Web Research Scraper…, _extract_location(), get_info(), get_weather(), Pulls a clean location name out of a weather query., Get current weather using wttr.in — returns a clean spoken string., Search for a query within a specific website using DuckDuckGo site: operator., Read and extract readable text content from a specific URL. (+24 more)

### Community 60 - "content_humanizer.py"
Cohesion: 0.06
Nodes (52): build_structure_prompt(), build_vocab_prompt(), call_groq(), check_similarity(), detect_tone(), fact_check(), get_groq_client(), get_sentence_scores() (+44 more)

### Community 61 - "jarvis_overlay.py"
Cohesion: 0.15
Nodes (9): Image, math, pil, generate_arc_reactor(), JarvisOverlay, Jarvis Arc Reactor Overlay -------------------------- A floating, always-on-…, Draws a beautiful arc reactor using PIL when no icon file is found., read_state() (+1 more)

### Community 62 - "Assignment solver (5 phases)"
Cohesion: 0.18
Nodes (11): generate_answer(), Generate an answer for a SINGLE question using Groq LLM directly (fast, no…, list_assignments(), Scan Desktop, Documents, and Downloads for PDF files., Assignment solver (5 phases), Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify (+3 more)

### Community 63 - "ppt_create"
Cohesion: 0.11
Nodes (13): NLPExtractor, Runs extraction on each scraped source and aggregates the results. Returns a…, ppt_create(), PPT v6 entry point → ppt_studio.create (adaptive layouts, strict user content,…, research_pipeline.py — End-to-End Autonomous Research Orchestrator…, Scrapes the web for a topic and extracts verified facts and statistics. Yields…, research_topic(), Searches DDG for the topic, fetches the top N links concurrently, and returns… (+5 more)

### Community 64 - "whatsapp_smart"
Cohesion: 0.13
Nodes (23): _clear_search(), confirm_whatsapp_send(), _focus_or_open_whatsapp(), _fuzzy_score(), _get_visible_search_results(), _get_whatsapp_window(), initiate_whatsapp_send(), open_whatsapp() (+15 more)

### Community 65 - "frontend"
Cohesion: 0.22
Nodes (8): Frontend (`frontend/src`), Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Key behaviour (App.jsx), Purpose, Web UI (React/Vite), DagPlanPanel()

### Community 67 - "CacheServer"
Cohesion: 0.14
Nodes (11): CacheServer, main(), Full startup: recover state, start engine, begin accepting connections., Restore cache state from disk before the engine thread starts. Called on the…, Main thread: bind socket and accept connections indefinitely., One thread per connected client. Reads commands, enqueues them to the engine,…, Graceful shutdown: take a final snapshot, stop engine, close socket., TCP server that wires incoming connections to the CacheEngine. Each accepted… (+3 more)

### Community 68 - "spotify_service.py"
Cohesion: 0.06
Nodes (58): app_kind(), control(), run(), _do(), _filter(), kind_playing(), _label(), media_command() (+50 more)

### Community 69 - "prompt_enhancer_button"
Cohesion: 0.14
Nodes (4): EnhanceButton, Move (and optionally show) without ever activating the window; Tk's deiconify()…, Default spot: just above the prompt box's top-right corner; below it or inside…, _save_state()

### Community 70 - "Speaker"
Cohesion: 0.10
Nodes (13): Channel, _norm_words(), prewarm(), Begin synthesising `text` now; returns a Clip that can be played while it fills., Synthesise short stock phrases (greetings, acks) into the cache for instant…, The speech stream of one command's reply., Plays sentences from many Channels without overlap: - urgent phrases (acks,…, Barge-in "stop": silence now and drop everything queued. (+5 more)

### Community 72 - "message_reader.py"
Cohesion: 0.12
Nodes (23): _bring_whatsapp_to_front(), _get_whatsapp_window(), _heuristic_parse_ocr_lines(), _parse_uia_message_string(), message_reader.py — Jarvis WhatsApp Intelligence: Message Reader…, Restores and focuses WhatsApp window. Returns True on success., Walks the WhatsApp UIA accessibility tree to extract messages. WhatsApp Desktop…, Parses a raw UIA ListItem Name string into a structured message dict.… (+15 more)

### Community 73 - "test_lru"
Cohesion: 0.20
Nodes (5): Accessing 'a' should move it to MRU and save it from eviction., Re-setting an existing key should move it to MRU., len(cache.map) must never exceed capacity., Fill to capacity+1. The first key inserted (LRU) should be evicted., TestEviction

### Community 75 - "resume_detector.py"
Cohesion: 0.15
Nodes (16): detect_resume_intent(), _extract_task_resource(), _find_best_task_match(), get_resume_context_string(), _has_continuation_verb(), _has_fresh_task_indicator(), _has_reference_phrase(), resume_detector.py — Jarvis Resume Intent Classifier… (+8 more)

### Community 76 - "re"
Cohesion: 0.10
Nodes (18): Jarvis Assignment Tool — Phase 4: Document Assembly…, nlp_extractor.py — LLM-Powered Fact & Entity Extractor…, build_prompt(), call_llm(), generate_social_content(), Refine an existing piece of social media content based on user instructions.…, Calls Groq Llama 3.3 70B directly for maximum speed. No slow fallbacks., Generate professional, multi-version social media content. (+10 more)

### Community 77 - "Element"
Cohesion: 0.11
Nodes (9): Element, element_from_handle(), focused_element(), uia_local.py — thread-safe UI Automation access (helper, not a tool)…, This thread's IUIAutomation (COM initialised for the thread on first use)., Minimal pywinauto-style wrapper around an IUIAutomationElement., Rect, uia() (+1 more)

### Community 78 - "voice_agent.py"
Cohesion: 0.08
Nodes (24): app_services, AsyncClient, difflib, httpx, pyaudio, _clean_agentic_line(), extract_wake_word_command(), _is_stop() (+16 more)

### Community 79 - "._run"
Cohesion: 0.17
Nodes (11): calibrate_tripwire(), _generate_chime(), _play_chime(), ndarray, Root Mean Square amplitude. Cast to float64 to prevent int16 overflow., FFT-based dominant frequency. Only inspect the positive half-spectrum (0 ……, Return True if this chunk looks like a clap/snap (loud + right frequency)., Main loop — opened inside the thread so PyAudio errors stay contained. State… (+3 more)

### Community 80 - "package"
Cohesion: 0.22
Nodes (9): dependencies, framer-motion, lucide-react, react, react-dom, react-markdown, react-syntax-highlighter, remark-gfm (+1 more)

### Community 81 - "handTracking"
Cohesion: 0.31
Nodes (3): CameraView(), getHandsConstructor(), HandTracker

### Community 82 - "Node"
Cohesion: 0.15
Nodes (7): Node, Any, Serialise the entire live cache to a plain dict. Expired entries are excluded —…, Restore cache state from a snapshot dict (produced by snapshot()). Called once…, Place node at the LRU (least-recently-used) end of the list., A doubly-linked list node holding one cache entry. Attributes: key (str): Cache…, Return True if this entry has a TTL and it has elapsed.

### Community 83 - "screen_reader.py"
Cohesion: 0.13
Nodes (22): _accessibility_tree(), get_screen_screenshot_b64(), _groq_vision_screen(), _init_tesseract(), _ocr_screen(), screen_reader.py — Jarvis Screen Vision (VLM-first architecture)…, Legacy OCR layer. Works on any app but extracts raw text only — no layout,…, Reads the active window's accessibility tree. Works best for native Win32 apps.… (+14 more)

### Community 84 - "2. Tool Registry (`tools.py`)"
Cohesion: 0.07
Nodes (32): add_event(), check_today_schedule(), _get_calendar_service(), get_upcoming_events(), calendar_tool.py — Jarvis Google Calendar Integration (Step 8)…, Create a new event in Google Calendar. - title: "Project Meeting" - date:…, Authenticate and return a Google Calendar API service object., List events in the next N days. (+24 more)

### Community 85 - "_worker"
Cohesion: 0.20
Nodes (8): Lock, 50 concurrent clients, each doing 1000 ops. After completion: - Server still…, The engine should report meaningful stats after the load test., While 10 threads hammer the cache, a separate thread pings repeatedly. All…, One client thread. Performs `ops` random GET/SET/DEL operations. Records any…, TestConcurrency, _ping_loop(), _worker()

### Community 86 - "ControlPanel + HandSkeleton"
Cohesion: 0.13
Nodes (13): frontend_src_airdrawing_airdrawing, COLORS, ControlPanel(), FONTS, SHAPES, FINGERTIP_INDICES, HAND_CONNECTIONS, HandSkeleton() (+5 more)

### Community 88 - "ppt_chart_engine"
Cohesion: 0.33
Nodes (3): ChartEngine, Stateless chart renderer. All colors are derived from the active PPT palette —…, Render a chart from structured data. Args: chart_data: {"type": "bar",…

### Community 89 - "LRUCache"
Cohesion: 0.17
Nodes (9): LRUCache, Insert or update a key-value pair. - If key already exists: update value + TTL,…, Remove a key from the cache. Returns True if the key existed, False if it was…, Place node at the MRU (most-recently-used) end of the list., Remove node from its current position in the list (O(1) because doubly-linked)., Evict a specific node (unlink + remove from map)., Evict the LRU entry (the node just before the tail sentinel). Returns the…, O(1) Least-Recently-Used cache backed by: - dict[str, Node] — hash map for O(1)… (+1 more)

### Community 90 - "assignment_pipeline"
Cohesion: 0.20
Nodes (17): _browser_thread(), _find_el(), _get_answer(), _get_browser_ctx(), _groq_answer(), _groq_humanize(), _humanize_browser(), Queue (+9 more)

### Community 91 - "prompt_enhancer_button"
Cohesion: 0.21
Nodes (11): _box_contains(), _box_set_value(), _clip_get(), _clip_set(), _ctrl(), _focus(), _focused_text(), _norm() (+3 more)

### Community 92 - "whatsapp_call"
Cohesion: 0.27
Nodes (10): flow_stream(), _click_voice_call_button(), confirm_whatsapp_call(), _focus_or_open_whatsapp(), _get_whatsapp_window(), initiate_whatsapp_call(), whatsapp_call.py — Jarvis Smart WhatsApp Calling Integration (Fully Isolated)…, Focus the WhatsApp window or open it if not running. Returns True on success. (+2 more)

### Community 94 - "ssml_processor"
Cohesion: 0.33
Nodes (5): add_human_prosody(), ssml_processor.py — Human Prosody Pre-processor…, Add natural speech prosody to plain text. Args: text: Plain text (already…, Remove all SSML tags from text — used when falling back to edge-tts which does…, strip_ssml()

### Community 95 - "assignment_assembler + assignment_pipeline"
Cohesion: 0.25
Nodes (8): assemble_assignment(), _create_powerpoint(), _create_word_doc(), _parse_qa_json(), Assemble the extracted/humanized questions and answers into a formatted…, Extract and parse the JSON array from the input string., do_assignment(), Master orchestrator. Uses a background thread for all Playwright code. Yields…

### Community 96 - "CODEMAP"
Cohesion: 0.22
Nodes (8): Backend core & API, Code map, Frontend (`frontend/src`, React 19 + Vite + Tailwind 4), Ignore these (no runtime role), Neural cache (neural_cache/, see its README.md), Scripts, Services (app/services), WhatsApp intelligence (app/services/whatsapp_intelligence)

### Community 97 - "youtube_windows"
Cohesion: 0.22
Nodes (9): _media_intent_for(), Media tool intent for one clause (YouTube-mode parser first, then keyword…, _fetch_results(), Scrape YouTube's results page → [{id,title,channel,duration,seconds,views}]; []…, True if some browser window's active tab is YouTube., youtube_tab_open(), Visible browser windows whose active tab is YouTube → [(hwnd, title)],…, youtube_windows() (+1 more)

### Community 98 - "Architecture"
Cohesion: 0.22
Nodes (7): Inline (shared-stream) mode — called by voice_agent.py on every audio frame it…, Architecture, HTTP endpoints, LLM usage, Memory layers (five separate stores), Processes, Voice path (`scripts/voice_agent.py`)

### Community 99 - "screen-vision + screen_vision"
Cohesion: 0.25
Nodes (7): _call_gemini_vision(), Send screenshot + context to the Groq vision model (settings.GROQ_VISION_MODEL)., Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Purpose, Screen understanding & UI automation

### Community 100 - "hinglish_normalizer.py"
Cohesion: 0.18
Nodes (11): devanagari_to_hinglish(), _sub(), normalize_for_tts(), hinglish_normalizer.py — Devanagari Crash Prevention + Text Normalizer…, One Devanagari word → casual Hinglish roman ("चलाओ" → "chalao", "करना" →…, Romanize a Devanagari (Hindi) transcript for the backend, keeping any Latin…, Transform text so it's safe and natural-sounding for TTS: 1. Replace known…, Markdown → plain speakable text (keeps Devanagari). Also drops URLs and emoji. (+3 more)

### Community 101 - "README"
Cohesion: 0.20
Nodes (9): Architecture, Benchmark, Files, LRU Cache Design, Neural Cache, Persistence, Running, Tests (+1 more)

### Community 102 - "package"
Cohesion: 0.40
Nodes (5): scripts, build, dev, lint, preview

### Community 103 - "startup_event"
Cohesion: 0.50
Nodes (4): _on_screen_alert(), Callback fired by the background watcher when something notable is detected.…, Start background screen watcher and RAG memory system when the server boots., startup_event()

### Community 105 - "Entry points"
Cohesion: 0.16
Nodes (13): _has_pattern(), _hint_text(), _ide_allows(), _is_editable(), is_prompt_box(), Writable text input: <textarea>/<input>/native edit, or a contenteditable…, In IDEs only chat / agent inputs qualify, never the code editor, the terminal,…, Entry points (+5 more)

### Community 106 - "ppt_tool.py"
Cohesion: 0.13
Nodes (22): _auto_select_image_layout(), _bg_fill(), _c(), _detect_purpose(), extract_theme_from_image(), _get_image_aspect_ratio(), _groq_call(), _normalize_and_recover() (+14 more)

### Community 107 - "youtube_player"
Cohesion: 0.33
Nodes (7): _num(), parse_clock(), parse_duration(), parse_player_command(), Map a spoken player command to (action, amount, value), or None. `t` should…, 10 minutes' → 600, '1 hour 5 min' → 3900, 'half a minute' → 30, '90 s' → 90.…, 5:30' → 330, '1:02:03' → 3723, 'to 5 30' → 330. None if absent.

### Community 108 - "dsa_enforcer.py"
Cohesion: 0.25
Nodes (7): _cache_del(), get_dsa_enforcer(), Delete from Neural Cache, silently skipping if unavailable., selenium, selenium_webdriver_edge_options, selenium_webdriver_edge_service, webdriver_manager_microsoft

### Community 109 - "youtube_control"
Cohesion: 0.25
Nodes (9): _dur_to_sec(), _parse_videos(), add(), walk(), Collect videos from ytInitialData: classic videoRenderer (search) and the newer…, Replace the session's result list with the videos actually on screen in the…, 1,234,567 views' / '82 million views' / '1.2M' → int., _screen_results() (+1 more)

### Community 110 - "send_style_reply"
Cohesion: 0.25
Nodes (8): get_cached_contact(), get_cached_drafts(), get_cached_incoming(), Returns the in-memory draft cache. Used by send_style_reply() in tools.py., Returns the contact name from the last draft generation., Returns the incoming message from the last draft generation., Picks draft N from the cache and sends it via confirm_whatsapp_send. Args:…, send_style_reply()

### Community 111 - "Chat pipeline & routing (/chat)"
Cohesion: 0.25
Nodes (7): Change recipes, Chat pipeline & routing (/chat), Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Purpose, Response formats

### Community 112 - "README"
Cohesion: 0.50
Nodes (3): Expanding the ESLint configuration, React Compiler, React + Vite

### Community 119 - "_Player"
Cohesion: 0.21
Nodes (4): get_player(), _Player, One persistent 24 kHz output stream driven by a callback that pulls from a…, Play a clip as it arrives. Returns False if interrupted.

### Community 120 - "browser_mail"
Cohesion: 0.24
Nodes (7): check_emails(), _get_api_key(), list_unread(), browser_mail.py — Standard Browser Mail Automation…, A generic tool to perform any mail task (like sending or reading) by pre-…, smart_mail_action(), webbrowser

### Community 122 - "smart_navigator"
Cohesion: 0.24
Nodes (10): _get_api_key(), _llm_extract(), smart_navigator.py — Isolated Smart Web Navigator for Jarvis…, Attempt to find the GROQ API key safely., Pass scraped text through LLM for structured extraction., Resolve a verbal site name like 'unstop' to a URL like 'https://unstop.com'., Resolves site name, opens a VISIBLE browser, and performs a search or action…, _resolve_url() (+2 more)

### Community 124 - "MicListener"
Cohesion: 0.17
Nodes (8): hinglish_to_devanagari(), Rewrite the Hindi words of a romanized Hinglish sentence in Devanagari, leaving…, Fixed on 2026-09-30 (voice), Fixed on 2026-10-01 (voice, round 2), Known issues, MicListener, Initial ambient noise floor (kept up to date on every non-speech frame)., One 32 ms frame → clap check + VAD state machine → events.

### Community 125 - "extract_questions"
Cohesion: 0.22
Nodes (8): extract_questions(), _extract_via_llm_text(), _merge_and_deduplicate(), _pdf_pages_to_text(), Extract text from each PDF page separately. Returns list of page strings., LLM-based text extraction as fallback for when regex fails., Merge questions from all three tracks. Priority: regex > vision > llm text. A…, Extract ALL questions from an assignment PDF using a 3-track hybrid system.…

### Community 126 - "ppt_tool"
Cohesion: 0.50
Nodes (4): compute_split_geometry(), Computed image + text zone dimensions (in EMU — python-pptx native)., Dynamically compute left-text / right-image split geometry. The split ratio…, SlotGeometry

### Community 127 - "whatsapp"
Cohesion: 0.33
Nodes (5): Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Purpose, WhatsApp: send, call, read, reply-style cloning

### Community 128 - "screen_vision.py"
Cohesion: 0.11
Nodes (28): _build_history_context(), _build_system_prompt(), _call_gemma_reasoning(), capture_screen_b64(), describe_screen_vlm(), _get_active_process_name(), _get_active_window_title(), _pixel_diff_percent() (+20 more)

### Community 129 - "ppt_edit"
Cohesion: 0.33
Nodes (6): ppt_edit(), Follow-up edit of the last deck (generator). See ppt_studio.edit., _ppt_edit(), Generator wrapper — follow-up edits of the last deck ("on slide 3 …", "make it…, Flow — edit (`ppt_edit` → `ppt_studio.edit` → `ppt_content.apply_edit`), Fixed on 2026-09-30 (PPT v6)

### Community 130 - "persistence"
Cohesion: 0.09
Nodes (15): Any, Path, Queue, Flush and close the file handle cleanly on server shutdown., Manages periodic full-state snapshots. The snapshot itself is triggered through…, Serialise cache state to disk and truncate the WAL. Called by CacheEngine on…, Load the snapshot from disk. Returns None if no snapshot exists yet. Called…, Start a daemon thread that enqueues a SNAPSHOT command every interval_seconds.… (+7 more)

### Community 131 - "Neural cache (Redis-like LRU server)"
Cohesion: 0.25
Nodes (7): Design, Files & symbols (auto-generated, line numbers are current), Graphify, Neural cache (Redis-like LRU server), Purpose, Runtime, Tests

### Community 132 - "dag_executor.py"
Cohesion: 0.05
Nodes (63): Settings, find_skill(), format_preferences_for_prompt(), get_all_preferences(), list_skills(), Jarvis Vector Memory — ChromaDB-based long-term memory engine. Stores and…, Returns a string suitable for injecting into LLM prompts., Stable short ID based on content hash. (+55 more)

### Community 133 - "detect_language"
Cohesion: 0.11
Nodes (19): classify_context(), detect_language(), context_classifier.py — Jarvis Situational Awareness…, Detect whether the user spoke English, Hinglish, or Hindi. Returns: 'english' —…, Classify the situation from user input. Returns a dict with keys: urgency :…, _maybe_compress_history(), When conversation history exceeds 15 messages, compress the oldest 10 into a…, get_context_aware_prompt() (+11 more)

### Community 134 - "Flow — create (`ppt_tool.ppt_create` → `ppt_studio.create`, a generator)"
Cohesion: 0.13
Nodes (15): detect_profile(), _is_instruction(), needs_architect(), Restore structure that copy-paste destroyed ("Title and OverviewEvent: …",…, A sentence that talks ABOUT the deck (images, slide count, theme…) rather than…, Pull instruction sentences ("use the images in slide 2 only", "both images go…, Rich / paragraph-style content needs real restructuring, not a bullet dump., repair_text() (+7 more)

### Community 138 - "DSA / LeetCode enforcer mode"
Cohesion: 0.29
Nodes (6): Data, DSA / LeetCode enforcer mode, Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Purpose

### Community 139 - "tools + ui_inspector"
Cohesion: 0.12
Nodes (17): click_ui_element_uia(), dump_app_ui_tree(), Click a UI element inside an app by AutomationId, name, or control type. Does…, Inject text into a specific input field in an app via UIA Value pattern. No…, Read the current text content of a UI element — e.g. a terminal output pane, a…, Dump the full Windows UI Automation accessibility tree of an app window. Use…, read_ui_element_text(), type_into_ui_element() (+9 more)

### Community 140 - "benchmark"
Cohesion: 0.14
Nodes (7): JSONFileBaseline, main(), measure_latency(), measure_throughput(), Spin up n_threads threads each doing ops_per_thread SET+GET pairs. Returns…, Mimics memory_tool.py's approach: every read/write touches disk. Uses a…, Run op_fn warmup times (discard), then timed times (measure). Returns (mean_µs,…

### Community 141 - "Syllabus auditor (YouTube playlist vs syllabus)"
Cohesion: 0.29
Nodes (6): Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Purpose, Syllabus auditor (YouTube playlist vs syllabus), Triggers

### Community 142 - "tripwire_status"
Cohesion: 0.33
Nodes (6): get_alerts(), get, Frontend polls this endpoint to receive proactive JARVIS screen alerts. e.g.…, Return current acoustic tripwire state for the frontend toggle., read_root(), tripwire_status()

### Community 143 - "_resolve_pdf_path"
Cohesion: 0.33
Nodes (6): generate_answers(), _groq_answer(), Generate an answer using Groq LLM with automatic model fallback chain. Tries…, Generate complete answers for ALL questions from an assignment. Tries these…, Resolve PDF path: handles full paths, filenames, partial names., _resolve_pdf_path()

### Community 144 - "PowerPoint generator"
Cohesion: 0.33
Nodes (5): Entry points, Files & symbols (auto-generated, line numbers are current), Graphify, PowerPoint generator, Purpose

### Community 145 - "api/memory.py"
Cohesion: 0.06
Nodes (37): _media_target(), Which player an ambiguous media command ("pause it", "next song") is for: named…, forget_memory(), ForgetRequest, get_history(), ingest_memory(), IngestRequest, memory_stats() (+29 more)

### Community 146 - "run_tool"
Cohesion: 0.14
Nodes (15): execute_tool(), BaseModel, post, ToolExecuteRequest, _call_sync(), tool_runner.py — Async execution of TOOL_REGISTRY entries for orchestrators…, Run a registry tool and return its output as a string. Raises on unknown tool…, run_tool() (+7 more)

### Community 148 - "Web search, research & browser automation"
Cohesion: 0.40
Nodes (4): Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Web search, research & browser automation

### Community 149 - "TestO1Timing"
Cohesion: 0.50
Nodes (3): Return average time per (set + get) operation in microseconds., Per-op time for N=1000 vs N=100000 should be within 3x of each other. If the…, TestO1Timing

### Community 151 - "get_wake_event"
Cohesion: 0.50
Nodes (3): get_wake_event(), Return the threading.Event that the engine sets on a double-clap., Event

### Community 152 - "small_cache"
Cohesion: 0.50
Nodes (4): large_cache(), fixture, LRU cache with capacity 3 — easy to reason about eviction., small_cache()

### Community 153 - "_pick"
Cohesion: 0.67
Nodes (3): generate(), _pick(), Intelligently pick a palette based on the presentation topic.

### Community 155 - "Voice: STT, TTS, wake word, clap wake, overlay"
Cohesion: 0.08
Nodes (21): Sets a reminder that Jarvis will speak after a given number of seconds., set_reminder(), preload_local_stt(), Load the local Whisper models in the background (voice agent startup)., Feed streamed tokens; get back speakable sentences as early as possible., Speak a complete text. All sentences synthesise in parallel, play in order., Speak an async generator of text chunks, sentence by sentence, pipelined., SentenceSplitter (+13 more)

## Knowledge Gaps
- **158 isolated node(s):** `Settings`, `name`, `private`, `version`, `type` (+153 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1342 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **25 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Tool registry` connect `Tool registry` to `ppt_edit`, `window_layout.py`, `youtube_control.py`, `syllabus_auditor.py`, `tools + ui_inspector`, `browser_tool.py`, `file_ops.py`, `_resolve_pdf_path`, `api/memory.py`, `run_tool`, `chat.py`, `Voice: STT, TTS, wake word, clap wake, overlay`, `resume_builder.py`, `json`, `gmail_tool.py`, `agentic_web.py`, `air-drawing + air_drawing_tool`, `assignment_humanizer.py`, `llm.py`, `web_search.py`, `content_humanizer.py`, `Assignment solver (5 phases)`, `ppt_create`, `whatsapp_smart`, `spotify_service.py`, `re`, `2. Tool Registry (`tools.py`)`, `whatsapp_call`, `assignment_assembler + assignment_pipeline`, `browser_mail`, `smart_navigator`, `extract_questions`?**
  _High betweenness centrality (0.147) - this node is a cross-community bridge._
- **Why does `open_air_drawing()` connect `air-drawing + air_drawing_tool` to `Tool registry`?**
  _High betweenness centrality (0.091) - this node is a cross-community bridge._
- **Are the 122 inferred relationships involving `Tool registry` (e.g. with `keyword_detect_tool()` and `_media_compound()`) actually correct?**
  _`Tool registry` has 122 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `chat_endpoint()` (e.g. with `describe_screen_for_llm()` and `get_screen_text_summary()`) actually correct?**
  _`chat_endpoint()` has 8 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Settings`, `name`, `private` to the rest of the system?**
  _158 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Tool registry` be split into smaller, more focused modules?**
  _Cohesion score 0.033893557422969185 - nodes in this community are weakly interconnected._
- **Should `style_profiler.py` be split into smaller, more focused modules?**
  _Cohesion score 0.12923076923076923 - nodes in this community are weakly interconnected._