# Graph Report - Jarvis  (2026-10-02)

## Corpus Check
- 188 files · ~245,955 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 3, .css 3, .bat 1)

## Summary
- 3211 nodes · 6870 edges · 154 communities (131 shown, 23 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 717 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ec788919`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Tool registry
- reply_generator.py
- init_rag_memory
- Fixed on 2026-10-01 (PPT)
- ppt_chart_engine.py
- dark_enhancement.py
- window_layout.py
- test_protocol
- youtube_control.py
- rag_memory.py
- ppt_studio.py
- DeckRenderer
- browser_tool.py
- LRUCache
- file_ops.py
- PresentationBuilder
- _run_browser_session
- resume_detector.py
- skill_prompt_enhancer.py
- prompt_enhancer_button.py
- generate_deck
- chat.py
- ppt_research.py
- ppt_template.py
- main.py
- ppt_router.py
- package
- gestureController + gestureInterpreter
- _f
- ppt_image_engine.py
- test_task_resumption.py
- ppt_composer.py
- dsa_enforcer + dsa-mode
- ppt_content.py
- gmail_tool.py
- PromptOverlay
- ui_inspector
- agentic_web.py
- _media_compound
- ._run
- _ClapDetector
- transformEngine
- engine + test_protocol
- air-drawing + air_drawing_tool
- ppt_designer.py
- voice.py
- package + App
- AcousticWakeEngine
- _humanize_via_browser
- message_reader.py
- ._send
- interactionEngine + DrawingCanvas
- Clip
- package
- strokeManager
- SentenceSplitter
- llm.py
- get_engine
- _render_html_inner
- web_search.py
- content_humanizer.py
- NLPExtractor
- Voice: STT, TTS, wake word, clap wake, overlay
- PowerPoint generator
- whatsapp_smart.py
- frontend
- shapeManager
- Flow — create (`ppt_tool.ppt_create` → `ppt_studio.create`, a generator)
- spotify_service
- prompt_enhancer_button
- voice
- drawingEngine
- understand_screen
- test_lru
- get_info
- refresh_docs.py
- _watcher_loop
- Element
- VoiceAgent
- memory
- package
- handTracking
- Architecture
- screen_reader.py
- typing
- datetime
- ControlPanel + HandSkeleton
- strokeRefiner
- ppt_chart_engine
- media_sessions.py
- re
- prompt_enhancer_button
- JarvisOverlay
- ssml_processor.py
- _worker
- Code map
- youtube_player.py
- CacheClient
- ppt_designer
- api/memory.py
- place_image
- package
- create_resume
- test_lru
- Entry points
- ppt_tool.py
- assignment_pipeline.py
- _sanitize_design
- smart_navigator.py
- hinglish_normalizer.py
- speak_text
- README
- ResearchScraper
- __init__
- README
- _Player
- README
- PROMPT_TEMPLATE
- Flow
- FEATURES
- voice_agent
- Content fidelity & page limits (2026-10-02)
- vector_store + database
- server.py
- _assign_images
- Resume creator
- voice_agent.py
- Neural cache (Redis-like LRU server)
- dag_executor.py
- resume_builder.py
- describe_screen_for_llm
- search_site
- edge_tts
- pygame
- browser_mail.py
- scrape_url
- JSONFileBaseline
- screen-vision + screen_vision
- Windows/OS control: windows, media, apps, files
- get_wake_event
- youtube_player
- compute_split_geometry
- run_tool
- test_lru
- _ocr_screen
- debug_wa.py
- _window_rect
- traceback
- .delete
- Flow (`scripts/voice_agent.py`)

## God Nodes (most connected - your core abstractions)
1. `Tool registry` - 123 edges
2. `chat_endpoint()` - 50 edges
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
- `Calendar` --references--> `check_today_schedule()`  [INFERRED]
  docs/features/email-calendar.md → app/services/calendar_tool.py
- `Entry points` --references--> `PresentationBuilder`  [INFERRED]
  docs/features/ppt.md → app/services/ppt_tool.py
- `Gotchas` --references--> `classify_app()`  [INFERRED]
  docs/features/prompt-enhancer.md → app/services/prompt_enhancer_button.py

## Import Cycles
- None detected.

## Communities (154 total, 23 thin omitted)

### Community 0 - "Tool registry"
Cohesion: 0.02
Nodes (130): ppt_styles(), enhance_prompt(), Enhance a prompt and return it under an **ENHANCED PROMPT (DOMAIN)** header., Resolves site name, opens a VISIBLE browser, and performs a search or action…, smart_web_action(), append_to_file(), cache_get(), cache_set() (+122 more)

### Community 1 - "reply_generator.py"
Cohesion: 0.05
Nodes (56): build_style_profile(), generate_reply_draft(), One-time training: parse a WhatsApp .txt chat export to build your personal…, Read the latest WhatsApp thread with a contact and generate 3 reply drafts that…, _build_system_prompt(), _build_user_prompt(), _call_groq(), generate_reply_draft() (+48 more)

### Community 2 - "init_rag_memory"
Cohesion: 0.20
Nodes (12): aiomysql, close_mysql(), init_mysql(), mysql_db.py — Jarvis Async MySQL Connection Pool…, Gracefully close the MySQL connection pool on server shutdown., Initialize the MySQL connection pool and ensure all required tables exist. Safe…, init_rag_memory(), _load_faiss_index() (+4 more)

### Community 3 - "Fixed on 2026-10-01 (PPT)"
Cohesion: 0.20
Nodes (9): _is_instruction(), Restore structure that copy-paste destroyed ("Title and OverviewEvent: …",…, A sentence that talks ABOUT the deck (images, slide count, theme…) rather than…, Pull instruction sentences ("use the images in slide 2 only", "both images go…, repair_text(), split_instructions(), Fixed on 2026-10-01 (PPT), Fixed on 2026-10-01 (voice, round 2) (+1 more)

### Community 4 - "ppt_chart_engine.py"
Cohesion: 0.12
Nodes (34): _bg_color(), _extract_strict_metric(), _fig_to_bytes(), _hex(), _metrics_to_bar(), _palette_colors(), ppt_chart_engine.py — Dynamic Data-Visualization Engine for JARVIS PPT…, Horizontal or vertical bar chart. (+26 more)

### Community 5 - "dark_enhancement.py"
Cohesion: 0.13
Nodes (23): _apply_gamma(), _fusion_and_polish(), get_all_enhancements(), _normalize_to_8bit(), _path_1_retinex(), _path_2_wavelet(), ndarray, run_pipeline_a() (+15 more)

### Community 6 - "window_layout.py"
Cohesion: 0.09
Nodes (38): True if the Spotify desktop app has a window (cheap: EnumWindows, no UIA)., spotify_running(), focus_window(), minimize_window(), Minimizes a specific window by name using Win32 ShowWindow., Bring a window to the foreground by partial name match (Win32 API, no…, adjust_active_window(), _enumerate_app_windows() (+30 more)

### Community 7 - "test_protocol"
Cohesion: 0.10
Nodes (23): decode_message(), encode_message(), protocol.py — Wire Protocol for Neural Cache (Milestone 2)…, Serialise a dict to the wire format: [4-byte length][UTF-8 JSON body] Args:…, Read exactly one message from a socket, handling partial TCP reads correctly.…, Loop until exactly n bytes have been read from sock. This is necessary because…, _recv_exact(), make_fake_socket() (+15 more)

### Community 8 - "youtube_control.py"
Cohesion: 0.05
Nodes (67): keyword_detect_tool(), _media_intent_for(), _media_target(), Which player an ambiguous media command ("pause it", "next song") is for: named…, Media tool intent for one clause (YouTube-mode parser first, then keyword…, Fast, 100% reliable keyword-based tool detection. Runs BEFORE the LLM router to…, get_last(), app: 'spotify' | 'youtube'. (+59 more)

### Community 9 - "rag_memory.py"
Cohesion: 0.06
Nodes (48): rag_memory.py — Jarvis Long-Term RAG Memory Engine…, Persist FAISS index and ID map to disk (sync, runs in thread executor)., Run the sync FAISS save in a thread pool to avoid blocking the event loop., _save_faiss_index(), _save_faiss_index_async(), _approx_token_count(), _assemble_response(), audit_playlist_syllabus() (+40 more)

### Community 10 - "ppt_studio.py"
Cohesion: 0.08
Nodes (43): detect_profile(), parse_instructions(), Separate the user's command, any pasted/attached content and attachment paths., Deterministic reading of the user's instructions. image_rules: [{"images":…, slide_count(), split_request(), choice may be a THEMES key, a legacy palette key, a palette dict, or None…, resolve_theme() (+35 more)

### Community 11 - "DeckRenderer"
Cohesion: 0.14
Nodes (21): _compact_header(), box(), DeckRenderer, fit_size(), _items(), para_h(), Header + lead + list inside a column. Returns nothing., Portrait/square image as a full-height panel flush to one edge. (+13 more)

### Community 12 - "browser_tool.py"
Cohesion: 0.20
Nodes (22): browse_and_paginate(), browse_and_read(), _clean_text(), click_element(), _ensure_url(), fill_form(), _llm_extract(), _new_browser_page() (+14 more)

### Community 13 - "LRUCache"
Cohesion: 0.05
Nodes (29): Design, LRUCache, Node, Any, Insert or update a key-value pair. - If key already exists: update value + TTL,…, Remove a key from the cache. Returns True if the key existed, False if it was…, Serialise the entire live cache to a plain dict. Expired entries are excluded —…, Restore cache state from a snapshot dict (produced by snapshot()). Called once… (+21 more)

### Community 14 - "file_ops.py"
Cohesion: 0.10
Nodes (29): append_file(), bulk_rename(), create_folder(), delete_file(), diff_files(), _fmt_size(), list_directory(), _maybe_summarize() (+21 more)

### Community 15 - "PresentationBuilder"
Cohesion: 0.16
Nodes (21): _clean_image_path(), _corner_L(), _get_image_aspect_ratio(), _oval(), _parse_bullet(), _parse_card(), PresentationBuilder, _frame() (+13 more)

### Community 16 - "_run_browser_session"
Cohesion: 0.13
Nodes (18): _ask_question_on_page(), _find_input(), _get_persistent_page(), Launch a visible (non-headless) Chromium with a persistent profile. Login…, Try CSS selectors to find the visible chat input. Returns locator or None., Type a message into the AI chat input and submit it., Upload PDF to the AI chat page. Returns True if upload was initiated., Wait until the AI stops generating its response. (+10 more)

### Community 17 - "resume_detector.py"
Cohesion: 0.15
Nodes (16): detect_resume_intent(), _extract_task_resource(), _find_best_task_match(), get_resume_context_string(), _has_continuation_verb(), _has_fresh_task_indicator(), _has_reference_phrase(), resume_detector.py — Jarvis Resume Intent Classifier… (+8 more)

### Community 18 - "skill_prompt_enhancer.py"
Cohesion: 0.17
Nodes (19): check_for_hallucination(), clean_output(), detect_domain(), is_bloated(), protect_blocks(), prompt_enhancement_library.py…, Replace ``` fenced blocks with [[BLOCK_n]] placeholders., Put protected blocks back; append any the model dropped. (+11 more)

### Community 19 - "prompt_enhancer_button.py"
Cohesion: 0.10
Nodes (27): _acquire_single_instance(), _app_title_match(), _browser_url(), classify_app(), _exe_name(), install_autostart(), _load_state(), main() (+19 more)

### Community 20 - "generate_deck"
Cohesion: 0.10
Nodes (31): _budget_left(), _compact(), _content_prompt(), _flatten(), _gemini_json(), generate_deck(), _is_note(), run() (+23 more)

### Community 21 - "chat.py"
Cohesion: 0.08
Nodes (34): chat_endpoint(), _dag_stream_with_history(), planner_stream(), response_stream_with_history(), resume_stream(), tool_stream(), ChatRequest, _clean_yt_query() (+26 more)

### Community 22 - "ppt_research.py"
Cohesion: 0.12
Nodes (32): plan_queries(), 4-6 web queries covering the angles a deck on `topic` needs. Templates, not an…, Web + Wikipedia → verified facts. [] when offline (the deck is then written…, research_facts(), allowed_numbers(), _anchors(), audit_slide(), _clean_html() (+24 more)

### Community 23 - "ppt_template.py"
Cohesion: 0.06
Nodes (59): prepare_image(), Return a PPTX-safe copy (EXIF-rotated, RGB, ≤2400px, png/jpg) and its aspect., Edge-energy profile along an axis ('x' or 'y') for smart cropping., _saliency_profile(), analyze_format(), _analyze_slide(), classify_box(), _clear() (+51 more)

### Community 24 - "main.py"
Cohesion: 0.11
Nodes (20): get_alerts(), _on_screen_alert(), get, Stop watcher, acoustic tripwire, and close DB pool cleanly on server shutdown., Frontend polls this endpoint to receive proactive JARVIS screen alerts. e.g.…, Return current acoustic tripwire state for the frontend toggle., Callback fired by the background watcher when something notable is detected.…, Start background screen watcher and RAG memory system when the server boots. (+12 more)

### Community 25 - "ppt_router.py"
Cohesion: 0.09
Nodes (28): build_ppt(), generate(), create_ppt_backend(), generate(), extract_theme(), get_styles(), PPTBuildRequest, PPTCreateRequest (+20 more)

### Community 26 - "package"
Cohesion: 0.11
Nodes (20): name, private, type, version, autoprefixer, eslint, ref_eslint_config, @eslint/js (+12 more)

### Community 28 - "_f"
Cohesion: 0.23
Nodes (18): _competencies_html(), _contact_html(), _education_html(), _experience_html(), _f(), _guess_icon(), _icon(), _it() (+10 more)

### Community 29 - "ppt_image_engine.py"
Cohesion: 0.15
Nodes (16): build_image_descriptors(), _extract_keywords(), get_aspect_ratio(), ImageDescriptor, _parse_slide_ref(), _parse_slide_ref_by_title(), ppt_image_engine.py — Semantic Image-Slide Matcher for JARVIS PPT Engine…, Return (aspect_ratio, width_px, height_px) for an image. Falls back to (1.78,… (+8 more)

### Community 30 - "test_task_resumption.py"
Cohesion: 0.13
Nodes (20): _ensure_ledger_file(), find_resumable_task(), get_recent_tasks(), get_recent_tasks_raw(), get_task_ledger_for_prompt(), _load_ledger(), log_task(), task_ledger.py — Jarvis Task Context Ledger… (+12 more)

### Community 31 - "ppt_composer.py"
Cohesion: 0.10
Nodes (54): _balanced_rows(), _body_cards(), _body_fields(), _body_list(), _body_paragraph(), _body_stats(), _body_steps(), _body_table() (+46 more)

### Community 32 - "dsa_enforcer + dsa-mode"
Cohesion: 0.11
Nodes (17): _cache_del(), _cache_set(), DSAEnforcer, get_dsa_enforcer(), Write to Neural Cache, silently skipping if unavailable., Delete from Neural Cache, silently skipping if unavailable., Data, DSA / LeetCode enforcer mode (+9 more)

### Community 33 - "ppt_content.py"
Cohesion: 0.10
Nodes (32): apply_edit(), apply_structure(), _as_dated(), _as_stat(), _clauses(), _edit_facts(), finalize_slides(), find_targets() (+24 more)

### Community 34 - "gmail_tool.py"
Cohesion: 0.08
Nodes (39): check_emails(), _decode_body(), _format_date(), get_email_body(), _get_gmail_service(), _get_header(), list_unread(), gmail_tool.py — Jarvis Gmail Integration (Step 5)… (+31 more)

### Community 35 - "PromptOverlay"
Cohesion: 0.14
Nodes (3): main(), PromptOverlay, Strip the **ENHANCED PROMPT (CODING):** header if present.

### Community 36 - "ui_inspector"
Cohesion: 0.10
Nodes (11): Walk all descendants looking for any control whose window_text contains `text`…, Fire an element's primary action via UIA Invoke pattern. No mouse movement —…, Inject text into an input element via UIA Value pattern. No simulated…, Read text from an element via UIA TextPattern or window_text. Returns empty…, Walk the accessibility tree and return all elements up to `depth` levels. Use…, Core wrapper around pywinauto's UIA backend. All interactions go through the OS…, Get a window wrapper by partial title match (regex-safe). Returns None if not…, Get the currently focused window via Win32 HWND matching. (+3 more)

### Community 37 - "agentic_web.py"
Cohesion: 0.06
Nodes (34): agentic_web_action(), _worker(), _build_search_queries(), _fetch_page_text(), __init__(), _get_api_key(), agentic_web.py — Smart Web Research Engine for Jarvis…, Download a page and return clean readable text (no HTML tags). (+26 more)

### Community 38 - "_media_compound"
Cohesion: 0.33
Nodes (4): _media_compound(), Re-target an unspecific media intent (pause/next/play X) to the given platform., "close this song and play shape of you", "pause the video then open mrbeast's…, _to_platform()

### Community 39 - "._run"
Cohesion: 0.21
Nodes (9): calibrate_tripwire(), _generate_chime(), ndarray, Root Mean Square amplitude. Cast to float64 to prevent int16 overflow., FFT-based dominant frequency. Only inspect the positive half-spectrum (0 ……, Return True if this chunk looks like a clap/snap (loud + right frequency)., Main loop — opened inside the thread so PyAudio errors stay contained. State…, Generate a pleasant two-tone wake chime as a float32 numpy array. (+1 more)

### Community 40 - "_ClapDetector"
Cohesion: 0.13
Nodes (9): AbstractEventLoop, _ClapDetector, _EnergyVAD, ndarray, Queue, Stateful frame-by-frame Silero VAD using the ONNX model bundled with faster-…, Fallback if Silero can't load: adaptive noise floor., Strict double clap. The old tripwire fired on ANY two loud 2–8 kHz frames… (+1 more)

### Community 42 - "engine + test_protocol"
Cohesion: 0.14
Nodes (14): CacheEngine, Any, engine.py — Single-Writer Command Queue (Milestone 3)…, Route a command dict to the appropriate handler. All handlers return a response…, Owns the LRUCache. Runs a single consumer loop on a dedicated thread. External…, Spawn the single writer thread. Call once at server boot., Gracefully stop the engine writer thread., The single consumer loop. Runs on CacheEngineThread. Processes one command at a… (+6 more)

### Community 43 - "air-drawing + air_drawing_tool"
Cohesion: 0.18
Nodes (9): open_air_drawing(), Opens the Air Drawing Canvas on the screen. This feature allows the user to…, Air drawing (webcam hand drawing), Files & symbols (auto-generated, line numbers are current), Flow, Gotchas, Graphify, Purpose (+1 more)

### Community 44 - "ppt_designer.py"
Cohesion: 0.08
Nodes (32): _contrast(), count_lines(), E(), _finish_theme(), gradient_box(), _justified_fixed(), justified_rows(), _line_factor() (+24 more)

### Community 45 - "voice.py"
Cohesion: 0.12
Nodes (26): devanagari_to_hinglish(), Romanize a Devanagari (Hindi) transcript for the backend, keeping any Latin…, _clean_transcript(), _finish(), _get_groq(), _groq_once(), groq_stt_available(), _load_whisper_model() (+18 more)

### Community 46 - "package + App"
Cohesion: 0.16
Nodes (11): App(), ChatMessage(), API_BASE, frontend_src_index, lucide-react, react, ref_react_dom_client, react-markdown (+3 more)

### Community 47 - "AcousticWakeEngine"
Cohesion: 0.12
Nodes (9): AcousticWakeEngine, Background thread that watches the microphone for a double-clap pattern. Usage…, Start the background listening thread., Signal the background thread to exit and wait for it., Resume detection after a disable()., Pause detection without stopping the thread (fast resume)., Signal the background thread to re-run calibration on the next cycle. Returns…, Override the volume threshold (used by voice_agent inline mode). (+1 more)

### Community 48 - "_humanize_via_browser"
Cohesion: 0.09
Nodes (24): _extract_output_text(), _fill_input(), _find_element(), _get_browser_page(), humanize_all_answers(), _humanize_chunk_via_browser(), humanize_text(), _humanize_via_browser() (+16 more)

### Community 49 - "message_reader.py"
Cohesion: 0.06
Nodes (40): _focus_or_open_whatsapp(), _bring_whatsapp_to_front(), _get_whatsapp_window(), _heuristic_parse_ocr_lines(), _parse_uia_message_string(), message_reader.py — Jarvis WhatsApp Intelligence: Message Reader…, Restores and focuses WhatsApp window. Returns True on success., Walks the WhatsApp UIA accessibility tree to extract messages. WhatsApp Desktop… (+32 more)

### Community 50 - "._send"
Cohesion: 0.13
Nodes (9): Send one of the reply drafts generated by generate_reply_draft. draft_index is…, send_style_reply(), Any, Store a key-value pair, optionally with a TTL. Args: key: Cache key. value:…, Retrieve server statistics (hit rate, evictions, cache size, etc.). Returns…, Send a command and return the response. Thread-safe. Handles lazy connect and…, Open a socket to the server if not already connected. Called within the lock —…, Send a PING and return True if the server replies PONG. Useful for health… (+1 more)

### Community 52 - "Clip"
Cohesion: 0.15
Nodes (10): Clip, prewarm(), PCM (int16, 24 kHz) that fills while synthesis streams; playable immediately., Begin synthesising `text` now; returns a Clip that can be played while it fills., Synthesise short stock phrases (greetings, acks) into the cache for instant…, _sapi_sync(), start_clip(), _synth_edge() (+2 more)

### Community 53 - "package"
Cohesion: 0.14
Nodes (14): devDependencies, autoprefixer, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, postcss (+6 more)

### Community 55 - "SentenceSplitter"
Cohesion: 0.17
Nodes (9): Feed streamed tokens; get back speakable sentences as early as possible., Speak an async generator of text chunks, sentence by sentence, pipelined., SentenceSplitter, speak_stream(), AsyncClient, POST /chat with the spoken language, speak the reply into `ch` as it streams.…, stream_chat(), on_event() (+1 more)

### Community 56 - "llm.py"
Cohesion: 0.08
Nodes (39): classify_context(), context_classifier.py — Jarvis Situational Awareness…, Classify the situation from user input. Returns a dict with keys: urgency :…, check_for_tool_intent(), generate_chat_response(), _groq_generate(), _is_complex_response(), _is_rate_limit() (+31 more)

### Community 57 - "get_engine"
Cohesion: 0.20
Nodes (12): post, Arm the acoustic tripwire so double-claps wake Jarvis., Disarm the acoustic tripwire (engine keeps running, just paused)., Schedule an ambient-noise recalibration pass. The engine samples the mic for ~2…, Upload a file to the data/uploads folder for Jarvis to process., tripwire_calibrate(), tripwire_disable(), tripwire_enable() (+4 more)

### Community 58 - "_render_html_inner"
Cohesion: 0.10
Nodes (30): _apply_layout_answer(), _balance_columns(), _css_extra(), _data_uri(), _decor_html(), _e(), editor_page(), _editor_toolbar() (+22 more)

### Community 59 - "web_search.py"
Cohesion: 0.20
Nodes (13): research_scraper.py — Autonomous Web Research Scraper…, _duckduckgo_search(), web_search.py — Jarvis Reliable Web Search (Step 3)…, PRIMARY PUBLIC FUNCTION — used by get_info() in tools.py. Enhanced with: -…, Use a fast LLM call to synthesize multiple search sources into a single…, Search DuckDuckGo using direct HTML scraping (faster, no brittle dependencies).…, Query the Wikipedia API for clean, factual information. Returns the first 3…, smart_search() (+5 more)

### Community 60 - "content_humanizer.py"
Cohesion: 0.09
Nodes (34): build_structure_prompt(), build_vocab_prompt(), call_groq(), check_similarity(), detect_tone(), fact_check(), get_groq_client(), get_sentence_scores() (+26 more)

### Community 61 - "NLPExtractor"
Cohesion: 0.25
Nodes (6): NLPExtractor, Runs extraction on each scraped source and aggregates the results. Returns a…, Scrapes the web for a topic and extracts verified facts and statistics. Yields…, research_topic(), Phase 3: Autonomous Research Aggregator. Scrapes live facts from the web,…, _research_and_create_ppt()

### Community 62 - "Voice: STT, TTS, wake word, clap wake, overlay"
Cohesion: 0.18
Nodes (10): preload_local_stt(), Load the local Whisper models in the background (voice agent startup)., Config (`app/core/config.py` + env), Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Measured (2026-09-30/10-01, i9-13900H, no GPU), Purpose (+2 more)

### Community 63 - "PowerPoint generator"
Cohesion: 0.33
Nodes (5): Entry points, Files & symbols (auto-generated, line numbers are current), Graphify, PowerPoint generator, Purpose

### Community 64 - "whatsapp_smart.py"
Cohesion: 0.07
Nodes (38): flow_stream(), _click_voice_call_button(), confirm_whatsapp_call(), _focus_or_open_whatsapp(), _get_whatsapp_window(), initiate_whatsapp_call(), whatsapp_call.py — Jarvis Smart WhatsApp Calling Integration (Fully Isolated)…, Focus the WhatsApp window or open it if not running. Returns True on success. (+30 more)

### Community 65 - "frontend"
Cohesion: 0.22
Nodes (8): Frontend (`frontend/src`), Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Key behaviour (App.jsx), Purpose, Web UI (React/Vite), DagPlanPanel()

### Community 67 - "Flow — create (`ppt_tool.ppt_create` → `ppt_studio.create`, a generator)"
Cohesion: 0.16
Nodes (21): architect_slides(), ask(), _retry(), run(), _complete_from_source(), deck_facts(), extractive_ok(), _missing_parts() (+13 more)

### Community 68 - "spotify_service"
Cohesion: 0.10
Nodes (35): _buttons(), _clean_query(), _close_spotify(), _com_init(), _content_play_buttons(), _find_spotify_window(), _cb(), _is_playing() (+27 more)

### Community 69 - "prompt_enhancer_button"
Cohesion: 0.14
Nodes (4): EnhanceButton, Move (and optionally show) without ever activating the window; Tk's deiconify()…, Default spot: just above the prompt box's top-right corner; below it or inside…, _save_state()

### Community 70 - "voice"
Cohesion: 0.11
Nodes (12): hinglish_to_devanagari(), Rewrite the Hindi words of a romanized Hinglish sentence in Devanagari, leaving…, Channel, _norm_words(), The speech stream of one command's reply., Plays sentences from many Channels without overlap: - urgent phrases (acks,…, Barge-in "stop": silence now and drop everything queued., Did the mic just hear Jarvis himself (speaker → mic bleed)? Echo comes back… (+4 more)

### Community 72 - "understand_screen"
Cohesion: 0.18
Nodes (12): Tool-callable version — called when user asks 'what's on my screen?' Routes…, read_screen_as_tool(), _build_history_context(), _build_system_prompt(), _call_gemma_reasoning(), _classify_intent(), Summarise the last N screen states so the VLM can reason about what changed.…, Send a scene description to Groq (openai/gpt-oss-20b) for reasoning. (+4 more)

### Community 73 - "test_lru"
Cohesion: 0.20
Nodes (5): Accessing 'a' should move it to MRU and save it from eviction., Re-setting an existing key should move it to MRU., len(cache.map) must never exceed capacity., Fill to capacity+1. The first key inserted (LRU) should be evicted., TestEviction

### Community 74 - "get_info"
Cohesion: 0.17
Nodes (11): _extract_location(), get_info(), get_weather(), Pulls a clean location name out of a weather query., Get current weather using wttr.in — returns a clean spoken string., Smart information lookup (Step 3 upgrade): - Weather queries -> wttr.in (real-…, Files & symbols (auto-generated, line numbers are current), Gotchas (+3 more)

### Community 75 - "refresh_docs.py"
Cohesion: 0.24
Nodes (11): ast, fnmatch, auto_block(), _js_symbols(), label_communities(), Path, _py_symbols(), refresh_docs.py — keep docs/features/*.md and the graphify graph in sync with… (+3 more)

### Community 76 - "_watcher_loop"
Cohesion: 0.15
Nodes (14): capture_screen_b64(), _get_active_process_name(), _get_active_window_title(), _pixel_diff_percent(), ndarray, Returns the foreground window title using WinAPI., Returns the executable name of the foreground window's process., Match window title / process name to a per-app prompt. (+6 more)

### Community 77 - "Element"
Cohesion: 0.11
Nodes (6): Element, focused_element(), uia_local.py — thread-safe UI Automation access (helper, not a tool)…, Minimal pywinauto-style wrapper around an IUIAutomationElement., Rect, ctypes

### Community 78 - "VoiceAgent"
Cohesion: 0.18
Nodes (7): _is_stop(), _pick(), Write Jarvis UI state so the overlay can animate accordingly., Was Jarvis talking (or just finished) during [t0, t1]?, set_ui_state(), VoiceAgent, filler()

### Community 79 - "memory"
Cohesion: 0.15
Nodes (18): find_skill(), format_preferences_for_prompt(), get_all_preferences(), list_skills(), Jarvis Vector Memory — ChromaDB-based long-term memory engine. Stores and…, Returns a string suitable for injecting into LLM prompts., Stable short ID based on content hash., Persist a successful dynamic skill for future reuse. (+10 more)

### Community 80 - "package"
Cohesion: 0.22
Nodes (9): dependencies, framer-motion, lucide-react, react, react-dom, react-markdown, react-syntax-highlighter, remark-gfm (+1 more)

### Community 81 - "handTracking"
Cohesion: 0.31
Nodes (3): CameraView(), getHandsConstructor(), HandTracker

### Community 82 - "Architecture"
Cohesion: 0.18
Nodes (9): _play_chime(), Inline (shared-stream) mode — called by voice_agent.py on every audio frame it…, Play the wake chime via sounddevice (non-blocking from caller's perspective)., Architecture, HTTP endpoints, LLM usage, Memory layers (five separate stores), Processes (+1 more)

### Community 83 - "screen_reader.py"
Cohesion: 0.17
Nodes (16): _accessibility_tree(), get_screen_screenshot_b64(), _groq_vision_screen(), screen_reader.py — Jarvis Screen Vision (VLM-first architecture)…, Reads the active window's accessibility tree. Works best for native Win32 apps.…, Always works — returns at minimum the active window title., Main function — returns the richest available description of the screen.…, Takes a screenshot and returns it as a base64-encoded JPEG string. Used as… (+8 more)

### Community 84 - "typing"
Cohesion: 0.22
Nodes (6): debug_ui_tree(), ui_inspector.py — Jarvis UIA Engine (Upgraded)…, Dump the full accessibility tree of an app window as a readable string. Use…, google_generativeai, lru.py — Hand-rolled LRU Cache (Milestone 1)…, typing

### Community 85 - "datetime"
Cohesion: 0.24
Nodes (10): add_event(), check_today_schedule(), _get_calendar_service(), get_upcoming_events(), calendar_tool.py — Jarvis Google Calendar Integration (Step 8)…, Create a new event in Google Calendar. - title: "Project Meeting" - date:…, Authenticate and return a Google Calendar API service object., List events in the next N days. (+2 more)

### Community 86 - "ControlPanel + HandSkeleton"
Cohesion: 0.13
Nodes (13): frontend_src_airdrawing_airdrawing, COLORS, ControlPanel(), FONTS, SHAPES, FINGERTIP_INDICES, HAND_CONNECTIONS, HandSkeleton() (+5 more)

### Community 88 - "ppt_chart_engine"
Cohesion: 0.33
Nodes (3): ChartEngine, Stateless chart renderer. All colors are derived from the active PPT palette —…, Render a chart from structured data. Args: chart_data: {"type": "bar",…

### Community 89 - "media_sessions.py"
Cohesion: 0.17
Nodes (18): app_kind(), control(), run(), _do(), _filter(), kind_playing(), _label(), media_command() (+10 more)

### Community 90 - "re"
Cohesion: 0.05
Nodes (57): Settings, Jarvis Assignment Tool — Phase 2: Answer Generation…, Jarvis Assignment Tool — Phase 3: Answer Humanizer…, _classify_question_type(), _clean_text(), _extract_marks(), _extract_via_vision(), _has_figure_reference() (+49 more)

### Community 91 - "prompt_enhancer_button"
Cohesion: 0.21
Nodes (11): _box_contains(), _box_set_value(), _clip_get(), _clip_set(), _ctrl(), _focus(), _focused_text(), _norm() (+3 more)

### Community 92 - "JarvisOverlay"
Cohesion: 0.20
Nodes (5): Image, generate_arc_reactor(), JarvisOverlay, Draws a beautiful arc reactor using PIL when no icon file is found., read_state()

### Community 94 - "ssml_processor.py"
Cohesion: 0.33
Nodes (5): add_human_prosody(), ssml_processor.py — Human Prosody Pre-processor…, Add natural speech prosody to plain text. Args: text: Plain text (already…, Remove all SSML tags from text — used when falling back to edge-tts which does…, strip_ssml()

### Community 95 - "_worker"
Cohesion: 0.20
Nodes (8): Lock, 50 concurrent clients, each doing 1000 ops. After completion: - Server still…, The engine should report meaningful stats after the load test., While 10 threads hammer the cache, a separate thread pings repeatedly. All…, One client thread. Performs `ops` random GET/SET/DEL operations. Records any…, TestConcurrency, _ping_loop(), _worker()

### Community 96 - "Code map"
Cohesion: 0.11
Nodes (15): Backend core & API, Code map, Frontend (`frontend/src`, React 19 + Vite + Tailwind 4), Ignore these (no runtime role), Neural cache (neural_cache/, see its README.md), Scripts, Services (app/services), WhatsApp intelligence (app/services/whatsapp_intelligence) (+7 more)

### Community 97 - "youtube_player.py"
Cohesion: 0.08
Nodes (64): element_from_handle(), This thread's IUIAutomation (COM initialised for the thread on first use)., uia(), _address_bar_focused(), _address_bar_value(), _clip_get(), _clip_restore(), _clip_set() (+56 more)

### Community 98 - "CacheClient"
Cohesion: 0.24
Nodes (4): CacheClient, Explicitly close the socket connection., Close self._sock, suppressing errors. Called within the lock., Thread-safe client for the Neural Cache server. One instance can be safely…

### Community 99 - "ppt_designer"
Cohesion: 0.40
Nodes (3): _as_plain_content(), _deep_plain(), Last-resort fallback: every word of a composite slide as plain bullets (never…

### Community 100 - "api/memory.py"
Cohesion: 0.05
Nodes (54): forget_memory(), ForgetRequest, get_history(), ingest_memory(), IngestRequest, memory_stats(), BaseModel, delete (+46 more)

### Community 101 - "place_image"
Cohesion: 0.22
Nodes (8): _best_window(), place_image(), Start fraction of the window (length=keep fraction) with most detail, biased to…, cover: fill box, crop with saliency. contain: fit inside box, centred., Largest body size so all items fit in (w,h). style: 'stack'|'inline'., _round_pic(), _soft_shadow(), Layout engine (`ppt_designer.py`)

### Community 102 - "package"
Cohesion: 0.40
Nodes (5): scripts, build, dev, lint, preview

### Community 103 - "create_resume"
Cohesion: 0.12
Nodes (27): _analyse_design(), _apply_layout_hint(), _apply_op(), _attachments(), create_resume(), detect_resume_request(), _edit_content(), editor_save() (+19 more)

### Community 105 - "Entry points"
Cohesion: 0.16
Nodes (13): _has_pattern(), _hint_text(), _ide_allows(), _is_editable(), is_prompt_box(), Writable text input: <textarea>/<input>/native edit, or a contenteditable…, In IDEs only chat / agent inputs qualify, never the code editor, the terminal,…, Entry points (+5 more)

### Community 106 - "ppt_tool.py"
Cohesion: 0.08
Nodes (29): match_images_to_slides(), Assign images to slides intelligently. Assignment priority: 1. Explicit slide…, _auto_select_image_layout(), _bg_fill(), _c(), _detect_purpose(), extract_theme_from_image(), _extract_theme_pil_local() (+21 more)

### Community 107 - "assignment_pipeline.py"
Cohesion: 0.05
Nodes (51): generate_answer(), generate_answers(), _groq_answer(), Generate an answer using Groq LLM with automatic model fallback chain. Tries…, Generate complete answers for ALL questions from an assignment. Tries these…, Generate an answer for a SINGLE question using Groq LLM directly (fast, no…, assemble_assignment(), _create_powerpoint() (+43 more)

### Community 108 - "_sanitize_design"
Cohesion: 0.23
Nodes (16): _apply_color(), _contrast(), _css(), _hex(), _lum(), _measure_band(), near(), _measure_frame() (+8 more)

### Community 109 - "smart_navigator.py"
Cohesion: 0.25
Nodes (8): _get_api_key(), _llm_extract(), smart_navigator.py — Isolated Smart Web Navigator for Jarvis…, Attempt to find the GROQ API key safely., Pass scraped text through LLM for structured extraction., Resolve a verbal site name like 'unstop' to a URL like 'https://unstop.com'., _resolve_url(), playwright_sync_api

### Community 110 - "hinglish_normalizer.py"
Cohesion: 0.18
Nodes (10): _sub(), loanword_ratio(), normalize_for_tts(), hinglish_normalizer.py — Devanagari Crash Prevention + Text Normalizer…, One Devanagari word → casual Hinglish roman ("चलाओ" → "chalao", "करना" →…, Share of Devanagari words that are English loanwords ("ओपन क्रोम" → 1.0). High…, Transform text so it's safe and natural-sounding for TTS: 1. Replace known…, Markdown → plain speakable text (keeps Devanagari). Also drops URLs and emoji. (+2 more)

### Community 111 - "speak_text"
Cohesion: 0.29
Nodes (6): get_player(), Speak a complete text. All sentences synthesise in parallel, play in order., speak_text(), split_sentences(), main(), Test language-adaptive TTS - plays English then Hindi to verify both engines…

### Community 112 - "README"
Cohesion: 0.50
Nodes (3): Expanding the ESLint configuration, React Compiler, React + Vite

### Community 119 - "_Player"
Cohesion: 0.27
Nodes (3): _Player, One persistent 24 kHz output stream driven by a callback that pulls from a…, Play a clip as it arrives. Returns False if interrupted.

### Community 120 - "README"
Cohesion: 0.20
Nodes (9): Architecture, Benchmark, Files, LRU Cache Design, Neural Cache, Persistence, Running, Tests (+1 more)

### Community 122 - "Flow"
Cohesion: 0.20
Nodes (11): _closest_preset(), _crop_photo(), _grow_photo_box(), _merge_design(), _palette(), Dominant colours (hex, share) — gives the VLM exact values to pick from., Grow from the face outwards until each edge hits a flat (uniform) line = the…, Cut the portrait out of the reference resume: face-anchored edge growth → VLM… (+3 more)

### Community 124 - "voice_agent"
Cohesion: 0.33
Nodes (3): MicListener, Initial ambient noise floor (kept up to date on every non-speech frame)., One 32 ms frame → clap check + VAD state machine → events.

### Community 125 - "Content fidelity & page limits (2026-10-02)"
Cohesion: 0.13
Nodes (25): _build_content(), _condense_content(), _content_brief(), _drop_invented(), clean_text(), ok(), _finalize_content(), _fit_render() (+17 more)

### Community 126 - "vector_store + database"
Cohesion: 0.33
Nodes (7): get_db_pool(), init_db(), Queries the table and uses the pgvector cosine distance operator (<=>) to fetch…, Inserts text chunks and vectors into the knowledge_store table., save_document_chunk(), search_similar_chunks(), asyncpg

### Community 127 - "server.py"
Cohesion: 0.05
Nodes (37): argparse, neural_cache, client.py — Python Client Library for Neural Cache (Milestone 5)…, Any, Path, Queue, persistence.py — WAL + Snapshot for Neural Cache (Milestone 6)…, Flush and close the file handle cleanly on server shutdown. (+29 more)

### Community 128 - "_assign_images"
Cohesion: 0.33
Nodes (4): _assign_images(), Put each image on its best slide. Explicit instructions win. Mutates deck;…, Move images off slides whose layout can't show them (or has too many) onto…, _rebalance()

### Community 129 - "Resume creator"
Cohesion: 0.22
Nodes (8): _image_b64(), Downscaled JPEG (a 1080x2400 phone screenshot costs far fewer vision tokens at…, Data/config, Files & symbols (auto-generated, line numbers are current), Graphify, Purpose, Resume creator, UI

### Community 130 - "voice_agent.py"
Cohesion: 0.11
Nodes (18): app_services, acoustic_tripwire.py — Jarvis Acoustic Wake Engine…, screen_vision.py — Jarvis VLM Screen Understanding (Layer 1 Upgrade)…, collections, difflib, httpx, mss, numpy (+10 more)

### Community 131 - "Neural cache (Redis-like LRU server)"
Cohesion: 0.29
Nodes (6): Files & symbols (auto-generated, line numbers are current), Graphify, Neural cache (Redis-like LRU server), Purpose, Runtime, Tests

### Community 132 - "dag_executor.py"
Cohesion: 0.07
Nodes (48): _semantic_window_adjust(), _call_dag_planner(), DAGNode, _execute_node(), is_dag_task(), dag_executor.py — Jarvis DAG-Based Multi-Step Agent Planner…, Ask the LLM to produce a DAG plan. Returns parsed dict., Returns execution waves — each wave is a list of node IDs that can run in… (+40 more)

### Community 133 - "resume_builder.py"
Cohesion: 0.18
Nodes (13): _face_ratio(), _faces(), _gemini(), _groq(), _llm_json(), _parse_json(), resume_builder.py — Resume Creator Upload a picture of any resume → Jarvis…, Fallback when Groq is rate-limited (its vision model has a 200k tokens/DAY cap). (+5 more)

### Community 134 - "describe_screen_for_llm"
Cohesion: 0.50
Nodes (4): describe_screen_for_llm(), Returns a clean, LLM-optimized description of the current screen. Used as…, describe_screen_vlm(), Lightweight passive description — used as context injection in chat.py. Always…

### Community 135 - "search_site"
Cohesion: 0.33
Nodes (6): Search for a query within a specific website using DuckDuckGo site: operator., search_site_tool(), _format_ddg_results(), PUBLIC TOOL: Search for a query within a specific website. Uses DuckDuckGo with…, Convert DDG result list into a clean readable string for the LLM., search_site()

### Community 138 - "browser_mail.py"
Cohesion: 0.28
Nodes (6): check_emails(), _get_api_key(), list_unread(), browser_mail.py — Standard Browser Mail Automation…, A generic tool to perform any mail task (like sending or reading) by pre-…, smart_mail_action()

### Community 139 - "scrape_url"
Cohesion: 0.33
Nodes (6): Read and extract readable text content from a specific URL., scrape_url_tool(), _clean_html_text(), Parse HTML and extract readable text. Removes scripts, styles, navbars,…, PUBLIC TOOL: Read and extract readable text from any URL. Called when user says…, scrape_url()

### Community 140 - "JSONFileBaseline"
Cohesion: 0.14
Nodes (7): JSONFileBaseline, main(), measure_latency(), measure_throughput(), Spin up n_threads threads each doing ops_per_thread SET+GET pairs. Returns…, Mimics memory_tool.py's approach: every read/write touches disk. Uses a…, Run op_fn warmup times (discard), then timed times (measure). Returns (mean_µs,…

### Community 141 - "screen-vision + screen_vision"
Cohesion: 0.25
Nodes (7): _call_gemini_vision(), Send screenshot + context to the Groq vision model (settings.GROQ_VISION_MODEL)., Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Purpose, Screen understanding & UI automation

### Community 142 - "Windows/OS control: windows, media, apps, files"
Cohesion: 0.40
Nodes (4): Files & symbols (auto-generated, line numbers are current), Graphify, Purpose, Windows/OS control: windows, media, apps, files

### Community 143 - "get_wake_event"
Cohesion: 0.50
Nodes (3): get_wake_event(), Return the threading.Event that the engine sets on a double-clap., Event

### Community 144 - "youtube_player"
Cohesion: 0.33
Nodes (7): _num(), parse_clock(), parse_duration(), parse_player_command(), Map a spoken player command to (action, amount, value), or None. `t` should…, 10 minutes' → 600, '1 hour 5 min' → 3900, 'half a minute' → 30, '90 s' → 90.…, 5:30' → 330, '1:02:03' → 3723, 'to 5 30' → 330. None if absent.

### Community 145 - "compute_split_geometry"
Cohesion: 0.50
Nodes (4): compute_split_geometry(), Computed image + text zone dimensions (in EMU — python-pptx native)., Dynamically compute left-text / right-image split geometry. The split ratio…, SlotGeometry

### Community 146 - "run_tool"
Cohesion: 0.13
Nodes (17): execute_tool(), BaseModel, post, ToolExecuteRequest, format_recall_for_prompt(), Format recalled memory turns into an injectable LLM context block with clear…, _call_sync(), tool_runner.py — Async execution of TOOL_REGISTRY entries for orchestrators… (+9 more)

### Community 148 - "_ocr_screen"
Cohesion: 0.50
Nodes (4): _init_tesseract(), _ocr_screen(), Legacy OCR layer. Works on any app but extracts raw text only — no layout,…, Find and configure pytesseract. Returns True if ready.

### Community 151 - "traceback"
Cohesion: 0.29
Nodes (4): download(), Download Kokoro TTS model files from GitHub releases. Run this ONCE to get the…, traceback, urllib_request

### Community 155 - "Flow (`scripts/voice_agent.py`)"
Cohesion: 0.20
Nodes (9): detect_language(), Detect whether the user spoke English, Hinglish, or Hindi. Returns: 'english' —…, language_mismatch(), True if a reply sentence is in the other language than the one the user spoke., hi' → Hindi voice, 'en' → English voice, for one sentence., Loudest output RMS in the last `window` s — the voice agent's echo reference., Strict check used when there is no wake word to vouch for the audio., route_language() (+1 more)

## Knowledge Gaps
- **156 isolated node(s):** `Settings`, `name`, `private`, `version`, `type` (+151 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1369 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **23 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Tool registry` connect `Tool registry` to `dark_enhancement.py`, `window_layout.py`, `search_site`, `youtube_control.py`, `rag_memory.py`, `browser_mail.py`, `ppt_studio.py`, `browser_tool.py`, `scrape_url`, `file_ops.py`, `run_tool`, `chat.py`, `test_task_resumption.py`, `gmail_tool.py`, `agentic_web.py`, `_media_compound`, `air-drawing + air_drawing_tool`, `_humanize_via_browser`, `content_humanizer.py`, `whatsapp_smart.py`, `spotify_service`, `get_info`, `datetime`, `api/memory.py`, `create_resume`, `ppt_tool.py`, `assignment_pipeline.py`?**
  _High betweenness centrality (0.126) - this node is a cross-community bridge._
- **Why does `open_air_drawing()` connect `air-drawing + air_drawing_tool` to `Tool registry`?**
  _High betweenness centrality (0.083) - this node is a cross-community bridge._
- **Are the 122 inferred relationships involving `Tool registry` (e.g. with `keyword_detect_tool()` and `_media_compound()`) actually correct?**
  _`Tool registry` has 122 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `chat_endpoint()` (e.g. with `describe_screen_for_llm()` and `get_screen_text_summary()`) actually correct?**
  _`chat_endpoint()` has 8 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Settings`, `name`, `private` to the rest of the system?**
  _156 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Tool registry` be split into smaller, more focused modules?**
  _Cohesion score 0.023229716081247895 - nodes in this community are weakly interconnected._
- **Should `reply_generator.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05323653962492438 - nodes in this community are weakly interconnected._