# Graph Report - Jarvis  (2026-09-30)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 2885 nodes · 6004 edges · 139 communities (115 shown, 24 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 581 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `cb8a3aa4`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- tools
- server + acoustic_tripwire
- assignment_tool
- calendar_tool + memory_tool
- ppt_chart_engine
- rag_memory + memory
- window_layout
- test_protocol
- youtube_control
- syllabus_auditor
- ppt_studio
- ppt_designer
- browser_tool
- youtube_player
- file_ops
- ppt_tool
- assignment_humanizer
- ppt_content
- prompt_enhancement_library + skill_prompt_enhancer
- prompt_enhancer_button
- assignment_answers
- task_ledger
- style_profiler + reply_generator
- ppt_template
- gmail_tool + main
- ppt_router
- package
- gestureController + gestureInterpreter
- memory
- ppt_image_engine
- content_humanizer + content-tools
- dark_enhancement + dark_video_enhancement
- dsa_enforcer + dsa-mode
- whatsapp_smart + tools
- memory_tool
- prompt_overlay
- ui_inspector
- agentic_web + tool-registry
- dag_executor + dynamic_skill
- ppt_composer
- rag_memory + chat
- transformEngine
- refresh_docs + dump_wa_ui
- air-drawing + air_drawing_tool
- safe_executor + smart_navigator
- voice
- package + App
- acoustic_tripwire
- engine + test_protocol
- assignment_pipeline
- client + benchmark
- interactionEngine + DrawingCanvas
- agents + tool_runner
- package
- strokeManager
- youtube_player
- voice_agent
- lru + README
- screen_vision
- web_search + tools
- ui_inspector + tools
- jarvis_overlay
- resume_detector
- research_scraper + nlp_extractor
- ppt_designer
- frontend
- shapeManager
- persistence + server
- spotify_service
- prompt_enhancer_button
- voice
- drawingEngine
- screen_reader
- test_lru
- test_lru
- vector_store + database
- ppt_content
- voice
- voice_agent
- ppt + ppt_content
- package
- handTracking
- neural-cache
- reply_generator
- ppt_designer
- ppt_tool
- ControlPanel + HandSkeleton
- strokeRefiner
- ppt_chart_engine
- test_lru
- whatsapp_call
- prompt_enhancer_button
- chat-routing
- voice + hinglish_normalizer
- voice + voice_agent
- CODEMAP
- assignment_answers + assignment_tool
- test_lru
- llm + llm-personality
- message_reader + thread_extractor
- youtube_control + KNOWN_ISSUES
- package
- ppt_content
- whatsapp
- prompt-enhancer + prompt_enhancer_button
- ppt_tool
- ppt_studio + ppt_tool
- hinglish_normalizer
- voice + tools
- screen-vision + screen_vision
- youtube_control
- README
- ssml_processor
- __init__
- README
- voice
- browser_mail
- PROMPT_TEMPLATE
- assignment_assembler
- FEATURES
- ppt_designer
- screen_vision + screen_reader
- voice + context_classifier
- assignment
- chat + youtube_control
- screen_reader + screen_vision
- smart_navigator
- ppt_studio
- ppt_tool
- whatsapp
- ppt_content
- ppt_designer
- edge_tts
- pygame
- ppt_content

## God Nodes (most connected - your core abstractions)
1. `Tool registry` - 119 edges
2. `DeckRenderer` - 49 edges
3. `chat_endpoint()` - 42 edges
4. `text()` - 41 edges
5. `Key pieces` - 36 edges
6. `2. Tool Registry (`tools.py`)` - 34 edges
7. `create()` - 33 edges
8. `PresentationBuilder` - 32 edges
9. `box()` - 32 edges
10. `EnhanceButton` - 29 edges

## Surprising Connections (you probably didn't know these)
- `Entry points` --references--> `PresentationBuilder`  [INFERRED]
  docs/features/ppt.md → app/services/ppt_tool.py
- `Change recipes` --references--> `keyword_detect_tool()`  [INFERRED]
  docs/features/chat-routing.md → app/api/chat.py
- `Adding a tool (checklist)` --references--> `keyword_detect_tool()`  [INFERRED]
  docs/features/tool-registry.md → app/api/chat.py
- `Router` --references--> `check_for_tool_intent()`  [INFERRED]
  docs/features/llm-personality.md → app/services/llm.py
- `Gotchas` --references--> `classify_app()`  [INFERRED]
  docs/features/prompt-enhancer.md → app/services/prompt_enhancer_button.py

## Import Cycles
- None detected.

## Communities (139 total, 24 thin omitted)

### Community 0 - "tools"
Cohesion: 0.04
Nodes (78): ppt_styles(), append_to_file(), cache_get(), cache_set(), calculate(), close_sticky_notes(), close_tab(), copy_selected_text() (+70 more)

### Community 1 - "server + acoustic_tripwire"
Cohesion: 0.10
Nodes (24): acoustic_tripwire.py — Jarvis Acoustic Wake Engine…, screen_vision.py — Jarvis VLM Screen Understanding (Layer 1 Upgrade)…, argparse, base64, collections, google_generativeai, logging, mss (+16 more)

### Community 2 - "assignment_tool"
Cohesion: 0.10
Nodes (27): _classify_question_type(), _clean_text(), _extract_marks(), extract_questions(), _extract_via_llm_text(), _extract_via_vision(), _has_figure_reference(), _merge_and_deduplicate() (+19 more)

### Community 3 - "calendar_tool + memory_tool"
Cohesion: 0.16
Nodes (14): add_event(), check_today_schedule(), _get_calendar_service(), get_upcoming_events(), calendar_tool.py — Jarvis Google Calendar Integration (Step 8)…, Create a new event in Google Calendar. - title: "Project Meeting" - date:…, Authenticate and return a Google Calendar API service object., List events in the next N days. (+6 more)

### Community 4 - "ppt_chart_engine"
Cohesion: 0.12
Nodes (34): _bg_color(), _extract_strict_metric(), _fig_to_bytes(), _hex(), _metrics_to_bar(), _palette_colors(), ppt_chart_engine.py — Dynamic Data-Visualization Engine for JARVIS PPT…, Horizontal or vertical bar chart. (+26 more)

### Community 5 - "rag_memory + memory"
Cohesion: 0.05
Nodes (59): aiomysql, forget_memory(), ForgetRequest, get_history(), ingest_memory(), IngestRequest, memory_stats(), BaseModel (+51 more)

### Community 6 - "window_layout"
Cohesion: 0.08
Nodes (40): close_specific_window(), close_window(), _find_window_fuzzy(), minimize_window(), Closes the current active real app window (skips the Jarvis overlay)., Find a window HWND by fuzzy name matching using Win32 API (no pygetwindow)., Closes a specific window/app by name using Win32 PostMessage WM_CLOSE., Minimizes a specific window by name using Win32 ShowWindow. (+32 more)

### Community 7 - "test_protocol"
Cohesion: 0.10
Nodes (23): decode_message(), encode_message(), protocol.py — Wire Protocol for Neural Cache (Milestone 2)…, Serialise a dict to the wire format: [4-byte length][UTF-8 JSON body] Args:…, Read exactly one message from a socket, handling partial TCP reads correctly.…, Loop until exactly n bytes have been read from sock. This is necessary because…, _recv_exact(), make_fake_socket() (+15 more)

### Community 8 - "youtube_control"
Cohesion: 0.12
Nodes (32): _end_session(), _format_results(), _is_positional(), _load(), _mark_last(), youtube_control.py — YouTube search, result picking, player control and…, Speakable short title: drop [..]/(..)/|-tails, emoji and hashtags, cap the…, True if some browser window's active tab is YouTube. (+24 more)

### Community 9 - "syllabus_auditor"
Cohesion: 0.07
Nodes (41): _approx_token_count(), _assemble_response(), audit_playlist_syllabus(), _build_vector_store(), _chunk_transcript(), _coverage_level(), _embed_texts(), _extract_playlist_id() (+33 more)

### Community 10 - "ppt_studio"
Cohesion: 0.13
Nodes (26): parse_instructions(), Pull instruction sentences ("use the images in slide 2 only", "make 6 slides")…, [(n, heading, raw content)] split on 'Slide N:' markers of repaired text., raw_slide_blocks(), slide_count(), split_instructions(), _caption(), create() (+18 more)

### Community 11 - "ppt_designer"
Cohesion: 0.15
Nodes (18): DeckRenderer, fit_size(), _items(), para_h(), Header + lead + list inside a column. Returns nothing., Portrait/square image as a full-height panel flush to one edge., True = image on the right. Honours an explicit image_side, else alternates., Landscape image framed at its natural aspect next to text (zero crop). (+10 more)

### Community 12 - "browser_tool"
Cohesion: 0.14
Nodes (27): browse_and_paginate(), browse_and_read(), _clean_text(), click_element(), _ensure_url(), fill_form(), _llm_extract(), _new_browser_page() (+19 more)

### Community 13 - "youtube_player"
Cohesion: 0.11
Nodes (34): _address_bar_focused(), _address_bar_value(), _clip_get(), _clip_restore(), _clip_set(), com_init(), current_video_info(), fmt_time() (+26 more)

### Community 14 - "file_ops"
Cohesion: 0.10
Nodes (28): append_file(), bulk_rename(), create_folder(), delete_file(), diff_files(), _fmt_size(), list_directory(), _maybe_summarize() (+20 more)

### Community 15 - "ppt_tool"
Cohesion: 0.19
Nodes (17): _clean_image_path(), _get_image_aspect_ratio(), _oval(), _parse_bullet(), PresentationBuilder, _frame(), Render a single image with CONTAIN-FIT (object-fit: contain). The image is…, Fluid split layout that adapts natively to image aspect ratio: • Landscape… (+9 more)

### Community 16 - "assignment_humanizer"
Cohesion: 0.12
Nodes (25): _extract_output_text(), _fill_input(), _find_element(), _get_browser_page(), humanize_all_answers(), _humanize_chunk_via_browser(), humanize_text(), _humanize_via_browser() (+17 more)

### Community 17 - "ppt_content"
Cohesion: 0.14
Nodes (31): apply_edit(), apply_structure(), _as_dated(), _as_stat(), _clauses(), _compact(), _content_prompt(), finalize_slides() (+23 more)

### Community 18 - "prompt_enhancement_library + skill_prompt_enhancer"
Cohesion: 0.17
Nodes (19): check_for_hallucination(), clean_output(), detect_domain(), is_bloated(), protect_blocks(), prompt_enhancement_library.py…, Replace ``` fenced blocks with [[BLOCK_n]] placeholders., Put protected blocks back; append any the model dropped. (+11 more)

### Community 19 - "prompt_enhancer_button"
Cohesion: 0.08
Nodes (33): _acquire_single_instance(), _app_title_match(), _browser_url(), classify_app(), _exe_name(), _has_pattern(), install_autostart(), _is_editable() (+25 more)

### Community 20 - "assignment_answers"
Cohesion: 0.15
Nodes (20): _ask_question_on_page(), _find_input(), _get_persistent_page(), Jarvis Assignment Tool — Phase 2: Answer Generation…, Launch a visible (non-headless) Chromium with a persistent profile. Login…, Try CSS selectors to find the visible chat input. Returns locator or None., Type a message into the AI chat input and submit it., Upload PDF to the AI chat page. Returns True if upload was initiated. (+12 more)

### Community 21 - "task_ledger"
Cohesion: 0.12
Nodes (21): _ensure_ledger_file(), find_resumable_task(), get_recent_tasks(), get_recent_tasks_raw(), get_task_ledger_for_prompt(), _load_ledger(), log_task(), task_ledger.py — Jarvis Task Context Ledger… (+13 more)

### Community 22 - "style_profiler + reply_generator"
Cohesion: 0.08
Nodes (37): build_style_profile(), One-time training: parse a WhatsApp .txt chat export to build your personal…, Send one of the reply drafts generated by generate_reply_draft. draft_index is…, send_style_reply(), get_cached_contact(), get_cached_drafts(), get_cached_incoming(), Returns the in-memory draft cache. Used by send_style_reply() in tools.py. (+29 more)

### Community 23 - "ppt_template"
Cohesion: 0.06
Nodes (61): prepare_image(), Return a PPTX-safe copy (EXIF-rotated, RGB, ≤2400px, png/jpg) and its aspect., Edge-energy profile along an axis ('x' or 'y') for smart cropping., _saliency_profile(), analyze_format(), _analyze_slide(), classify_box(), _clear() (+53 more)

### Community 24 - "gmail_tool + main"
Cohesion: 0.05
Nodes (50): get_alerts(), _on_screen_alert(), get, post, Stop watcher, acoustic tripwire, and close DB pool cleanly on server shutdown., Frontend polls this endpoint to receive proactive JARVIS screen alerts. e.g.…, Return current acoustic tripwire state for the frontend toggle., Arm the acoustic tripwire so double-claps wake Jarvis. (+42 more)

### Community 25 - "ppt_router"
Cohesion: 0.13
Nodes (21): build_ppt(), generate(), create_ppt_backend(), generate(), extract_theme(), get_styles(), PPTBuildRequest, PPTCreateRequest (+13 more)

### Community 26 - "package"
Cohesion: 0.11
Nodes (20): name, private, type, version, autoprefixer, eslint, ref_eslint_config, @eslint/js (+12 more)

### Community 28 - "memory"
Cohesion: 0.16
Nodes (16): format_preferences_for_prompt(), get_all_preferences(), list_skills(), Jarvis Vector Memory — ChromaDB-based long-term memory engine. Stores and…, Returns a string suitable for injecting into LLM prompts., Stable short ID based on content hash., Persist a successful dynamic skill for future reuse., List all saved skill descriptions. (+8 more)

### Community 29 - "ppt_image_engine"
Cohesion: 0.16
Nodes (18): build_image_descriptors(), _extract_keywords(), get_aspect_ratio(), ImageDescriptor, match_images_to_slides(), _parse_slide_ref(), _parse_slide_ref_by_title(), ppt_image_engine.py — Semantic Image-Slide Matcher for JARVIS PPT Engine… (+10 more)

### Community 30 - "content_humanizer + content-tools"
Cohesion: 0.09
Nodes (34): build_structure_prompt(), build_vocab_prompt(), call_groq(), check_similarity(), detect_tone(), fact_check(), get_groq_client(), get_sentence_scores() (+26 more)

### Community 31 - "dark_enhancement + dark_video_enhancement"
Cohesion: 0.13
Nodes (23): _apply_gamma(), _fusion_and_polish(), get_all_enhancements(), _normalize_to_8bit(), _path_1_retinex(), _path_2_wavelet(), ndarray, run_pipeline_a() (+15 more)

### Community 32 - "dsa_enforcer + dsa-mode"
Cohesion: 0.11
Nodes (17): _cache_del(), _cache_set(), DSAEnforcer, get_dsa_enforcer(), Write to Neural Cache, silently skipping if unavailable., Delete from Neural Cache, silently skipping if unavailable., Data, DSA / LeetCode enforcer mode (+9 more)

### Community 33 - "whatsapp_smart + tools"
Cohesion: 0.06
Nodes (41): create_word_doc(), get_system_time(), lock_screen(), open_windows_copilot(), Returns current date and time naturally., Takes a full screenshot and saves to Desktop., Snaps left_app to left half and right_app to right half using Win32 API (no…, Locks the Windows screen. (+33 more)

### Community 34 - "memory_tool"
Cohesion: 0.18
Nodes (19): _ensure_memory_file(), forget_fact(), _fuzzy_match_topics(), get_all_facts_as_context(), _load_memory(), memory_tool.py — Jarvis Persistent Memory (Step 10 — ENHANCED)…, Replace an existing fact with an updated version., Remove all facts under a topic. (+11 more)

### Community 35 - "prompt_overlay"
Cohesion: 0.14
Nodes (3): main(), PromptOverlay, Strip the **ENHANCED PROMPT (CODING):** header if present.

### Community 36 - "ui_inspector"
Cohesion: 0.10
Nodes (11): Walk all descendants looking for any control whose window_text contains `text`…, Fire an element's primary action via UIA Invoke pattern. No mouse movement —…, Inject text into an input element via UIA Value pattern. No simulated…, Read text from an element via UIA TextPattern or window_text. Returns empty…, Walk the accessibility tree and return all elements up to `depth` levels. Use…, Core wrapper around pywinauto's UIA backend. All interactions go through the OS…, Get a window wrapper by partial title match (regex-safe). Returns None if not…, Get the currently focused window via Win32 HWND matching. (+3 more)

### Community 37 - "agentic_web + tool-registry"
Cohesion: 0.06
Nodes (33): agentic_web_action(), _worker(), _build_search_queries(), _fetch_page_text(), __init__(), _get_api_key(), agentic_web.py — Smart Web Research Engine for Jarvis…, Download a page and return clean readable text (no HTML tags). (+25 more)

### Community 38 - "dag_executor + dynamic_skill"
Cohesion: 0.07
Nodes (48): Settings, find_skill(), Returns up to n most relevant saved skills for a given task description. Each…, _call_dag_planner(), DAGNode, _execute_node(), dag_executor.py — Jarvis DAG-Based Multi-Step Agent Planner…, Ask the LLM to produce a DAG plan. Returns parsed dict. (+40 more)

### Community 39 - "ppt_composer"
Cohesion: 0.14
Nodes (40): _body_cards(), _body_fields(), _body_list(), _body_paragraph(), _body_stats(), _body_steps(), _body_table(), _cols_for() (+32 more)

### Community 40 - "rag_memory + chat"
Cohesion: 0.11
Nodes (22): chat_endpoint(), _dag_stream_with_history(), planner_stream(), response_stream_with_history(), tool_stream(), ChatRequest, BaseModel, post (+14 more)

### Community 42 - "refresh_docs + dump_wa_ui"
Cohesion: 0.06
Nodes (35): media_state.py — which media app the user used last (Spotify or YouTube)…, nlp_extractor.py — LLM-Powered Fact & Entity Extractor…, prompt_overlay.py ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Jarvis…, research_pipeline.py — End-to-End Autonomous Research Orchestrator…, WhatsApp Windows Desktop App Automation Uses the native Windows app via…, find_controls(), Dump WhatsApp Desktop UI tree to find the Voice Call button name. Run this…, search_tree() (+27 more)

### Community 43 - "air-drawing + air_drawing_tool"
Cohesion: 0.18
Nodes (9): open_air_drawing(), Opens the Air Drawing Canvas on the screen. This feature allows the user to…, Air drawing (webcam hand drawing), Files & symbols (auto-generated, line numbers are current), Flow, Gotchas, Graphify, Purpose (+1 more)

### Community 44 - "safe_executor + smart_navigator"
Cohesion: 0.09
Nodes (22): Safe Code Executor for Jarvis ------------------------------- Runs LLM-…, Restricted open(): blocks writes to system paths., Restricted __import__: blocks dangerous modules., Raised when generated code violates safety constraints., AST visitor that inspects generated code before execution., Parse and walk the AST, raising SecurityError on violations., _safe_import(), _safe_open() (+14 more)

### Community 45 - "voice"
Cohesion: 0.12
Nodes (25): loanword_ratio(), Share of Devanagari words that are English loanwords ("ओपन क्रोम" → 1.0). High…, _clean_transcript(), _finish(), _get_groq(), _groq_once(), groq_stt_available(), _load_whisper_model() (+17 more)

### Community 46 - "package + App"
Cohesion: 0.16
Nodes (11): App(), ChatMessage(), API_BASE, frontend_src_index, lucide-react, react, ref_react_dom_client, react-markdown (+3 more)

### Community 47 - "acoustic_tripwire"
Cohesion: 0.05
Nodes (30): AcousticWakeEngine, calibrate_tripwire(), _generate_chime(), get_wake_event(), _play_chime(), ndarray, Background thread that watches the microphone for a double-clap pattern. Usage…, Start the background listening thread. (+22 more)

### Community 48 - "engine + test_protocol"
Cohesion: 0.14
Nodes (14): CacheEngine, Any, engine.py — Single-Writer Command Queue (Milestone 3)…, Route a command dict to the appropriate handler. All handlers return a response…, Owns the LRUCache. Runs a single consumer loop on a dedicated thread. External…, Spawn the single writer thread. Call once at server boot., Gracefully stop the engine writer thread., The single consumer loop. Runs on CacheEngineThread. Processes one command at a… (+6 more)

### Community 49 - "assignment_pipeline"
Cohesion: 0.20
Nodes (17): _browser_thread(), _find_el(), _get_answer(), _get_browser_ctx(), _groq_answer(), _groq_humanize(), _humanize_browser(), Queue (+9 more)

### Community 50 - "client + benchmark"
Cohesion: 0.05
Nodes (27): JSONFileBaseline, main(), measure_latency(), measure_throughput(), Spin up n_threads threads each doing ops_per_thread SET+GET pairs. Returns…, Mimics memory_tool.py's approach: every read/write touches disk. Uses a…, Run op_fn warmup times (discard), then timed times (measure). Returns (mean_µs,…, CacheClient (+19 more)

### Community 52 - "agents + tool_runner"
Cohesion: 0.13
Nodes (16): execute_tool(), BaseModel, post, ToolExecuteRequest, _call_sync(), tool_runner.py — Async execution of TOOL_REGISTRY entries for orchestrators…, Run a registry tool and return its output as a string. Raises on unknown tool…, run_tool() (+8 more)

### Community 53 - "package"
Cohesion: 0.14
Nodes (14): devDependencies, autoprefixer, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, postcss (+6 more)

### Community 55 - "youtube_player"
Cohesion: 0.14
Nodes (20): _fallback(), fmt_span(), _js(), _js_str(), _num(), parse_clock(), parse_duration(), parse_player_command() (+12 more)

### Community 56 - "voice_agent"
Cohesion: 0.18
Nodes (11): app_services, difflib, httpx, pyaudio, _clean_agentic_line(), extract_wake_word_command(), _is_wake_token(), voice_agent.py — hands-free JARVIS voice loop (separate process → POST /chat)… (+3 more)

### Community 57 - "lru + README"
Cohesion: 0.07
Nodes (23): Node, Any, Insert or update a key-value pair. - If key already exists: update value + TTL,…, Remove a key from the cache. Returns True if the key existed, False if it was…, Serialise the entire live cache to a plain dict. Expired entries are excluded —…, Restore cache state from a snapshot dict (produced by snapshot()). Called once…, Place node at the MRU (most-recently-used) end of the list., Place node at the LRU (least-recently-used) end of the list. (+15 more)

### Community 58 - "screen_vision"
Cohesion: 0.12
Nodes (19): _build_history_context(), _build_system_prompt(), _call_gemini_vision(), _call_gemma_reasoning(), _get_active_process_name(), _get_active_window_title(), Returns the foreground window title using WinAPI., Returns the executable name of the foreground window's process. (+11 more)

### Community 59 - "web_search + tools"
Cohesion: 0.09
Nodes (32): research_scraper.py — Autonomous Web Research Scraper…, _extract_location(), get_info(), get_weather(), Pulls a clean location name out of a weather query., Get current weather using wttr.in — returns a clean spoken string., Search for a query within a specific website using DuckDuckGo site: operator., Read and extract readable text content from a specific URL. (+24 more)

### Community 60 - "ui_inspector + tools"
Cohesion: 0.09
Nodes (22): click_ui_element_uia(), dump_app_ui_tree(), Click a UI element inside an app by AutomationId, name, or control type. Does…, Inject text into a specific input field in an app via UIA Value pattern. No…, Read the current text content of a UI element — e.g. a terminal output pane, a…, Dump the full Windows UI Automation accessibility tree of an app window. Use…, Type a question into the Windows Copilot sidebar and retrieve the response.…, read_ui_element_text() (+14 more)

### Community 61 - "jarvis_overlay"
Cohesion: 0.20
Nodes (5): Image, generate_arc_reactor(), JarvisOverlay, Draws a beautiful arc reactor using PIL when no icon file is found., read_state()

### Community 62 - "resume_detector"
Cohesion: 0.15
Nodes (16): detect_resume_intent(), _extract_task_resource(), _find_best_task_match(), get_resume_context_string(), _has_continuation_verb(), _has_fresh_task_indicator(), _has_reference_phrase(), resume_detector.py — Jarvis Resume Intent Classifier… (+8 more)

### Community 63 - "research_scraper + nlp_extractor"
Cohesion: 0.15
Nodes (8): NLPExtractor, Runs extraction on each scraped source and aggregates the results. Returns a…, Scrapes the web for a topic and extracts verified facts and statistics. Yields…, research_topic(), Searches DDG for the topic, fetches the top N links concurrently, and returns…, ResearchScraper, Phase 3: Autonomous Research Aggregator. Scrapes live facts from the web,…, _research_and_create_ppt()

### Community 64 - "ppt_designer"
Cohesion: 0.09
Nodes (30): _contrast(), count_lines(), _finish_theme(), _justified_fixed(), justified_rows(), _line_factor(), line_h(), _lum() (+22 more)

### Community 65 - "frontend"
Cohesion: 0.22
Nodes (8): Frontend (`frontend/src`), Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Key behaviour (App.jsx), Purpose, Web UI (React/Vite), DagPlanPanel()

### Community 67 - "persistence + server"
Cohesion: 0.06
Nodes (25): Any, Path, Queue, Flush and close the file handle cleanly on server shutdown., Manages periodic full-state snapshots. The snapshot itself is triggered through…, Serialise cache state to disk and truncate the WAL. Called by CacheEngine on…, Load the snapshot from disk. Returns None if no snapshot exists yet. Called…, Start a daemon thread that enqueues a SNAPSHOT command every interval_seconds.… (+17 more)

### Community 68 - "spotify_service"
Cohesion: 0.08
Nodes (41): app: 'spotify' | 'youtube'., set_last(), _buttons(), _clean_query(), _close_spotify(), _com_init(), _content_play_buttons(), _find_spotify_window() (+33 more)

### Community 69 - "prompt_enhancer_button"
Cohesion: 0.14
Nodes (4): EnhanceButton, Move (and optionally show) without ever activating the window; Tk's deiconify()…, Default spot: just above the prompt box's top-right corner; below it or inside…, _save_state()

### Community 70 - "voice"
Cohesion: 0.13
Nodes (8): Channel, _norm_words(), The speech stream of one command's reply., Plays sentences from many Channels without overlap: - urgent phrases (acks,…, Did the mic just hear Jarvis himself (speaker → mic bleed)? Echo comes back…, Next (channel, text, lang) or None. Non-blocking., Speaker, Flow (`scripts/voice_agent.py`)

### Community 72 - "screen_reader"
Cohesion: 0.15
Nodes (18): _accessibility_tree(), get_screen_screenshot_b64(), _groq_vision_screen(), _init_tesseract(), _ocr_screen(), screen_reader.py — Jarvis Screen Vision (VLM-first architecture)…, Legacy OCR layer. Works on any app but extracts raw text only — no layout,…, Reads the active window's accessibility tree. Works best for native Win32 apps.… (+10 more)

### Community 73 - "test_lru"
Cohesion: 0.20
Nodes (5): Accessing 'a' should move it to MRU and save it from eviction., Re-setting an existing key should move it to MRU., len(cache.map) must never exceed capacity., Fill to capacity+1. The first key inserted (LRU) should be evicted., TestEviction

### Community 75 - "vector_store + database"
Cohesion: 0.33
Nodes (7): get_db_pool(), init_db(), Queries the table and uses the pgvector cosine distance operator (<=>) to fetch…, Inserts text chunks and vectors into the knowledge_store table., save_document_chunk(), search_similar_chunks(), asyncpg

### Community 76 - "ppt_content"
Cohesion: 0.17
Nodes (15): architect_slides(), ask(), run(), deck_facts(), extractive_ok(), _missing_parts(), plain_md(), True if the slide only re-uses the user's words (≥ min_ratio of tokens) and… (+7 more)

### Community 77 - "voice"
Cohesion: 0.15
Nodes (10): Clip, prewarm(), PCM (int16, 24 kHz) that fills while synthesis streams; playable immediately., Begin synthesising `text` now; returns a Clip that can be played while it fills., Synthesise short stock phrases (greetings, acks) into the cache for instant…, _sapi_sync(), start_clip(), _synth_edge() (+2 more)

### Community 78 - "voice_agent"
Cohesion: 0.06
Nodes (20): AbstractEventLoop, _ClapDetector, _EnergyVAD, _is_stop(), MicListener, _pick(), ndarray, Queue (+12 more)

### Community 79 - "ppt + ppt_content"
Cohesion: 0.14
Nodes (13): detect_profile(), Separate the user's command, any pasted/attached content and attachment paths., split_request(), ppt_create(), PPT v6 entry point → ppt_studio.create (adaptive layouts, strict user content,…, _ppt_create(), Generator wrapper — streams live progress to the frontend via chat.py's…, Entry points (+5 more)

### Community 80 - "package"
Cohesion: 0.22
Nodes (9): dependencies, framer-motion, lucide-react, react, react-dom, react-markdown, react-syntax-highlighter, remark-gfm (+1 more)

### Community 81 - "handTracking"
Cohesion: 0.31
Nodes (3): CameraView(), getHandsConstructor(), HandTracker

### Community 82 - "neural-cache"
Cohesion: 0.29
Nodes (6): Files & symbols (auto-generated, line numbers are current), Graphify, Neural cache (Redis-like LRU server), Purpose, Runtime, Tests

### Community 83 - "reply_generator"
Cohesion: 0.20
Nodes (13): _build_system_prompt(), _build_user_prompt(), _call_groq(), generate_reply_draft(), _get_groq_api_key(), _parse_drafts_from_response(), reply_generator.py — Jarvis WhatsApp Intelligence: Reply Generator…, Builds the LLM system prompt that injects the user's style profile. The LLM is… (+5 more)

### Community 84 - "ppt_designer"
Cohesion: 0.18
Nodes (12): box(), E(), gradient_box(), line_shape(), place_image(), RGBColor, cover: fill box, crop with saliency. contain: fit inside box, centred., Rectangle with a single-colour alpha gradient (angle in degrees, 0 =… (+4 more)

### Community 86 - "ControlPanel + HandSkeleton"
Cohesion: 0.13
Nodes (13): frontend_src_airdrawing_airdrawing, COLORS, ControlPanel(), FONTS, SHAPES, FINGERTIP_INDICES, HAND_CONNECTIONS, HandSkeleton() (+5 more)

### Community 88 - "ppt_chart_engine"
Cohesion: 0.33
Nodes (3): ChartEngine, Stateless chart renderer. All colors are derived from the active PPT palette —…, Render a chart from structured data. Args: chart_data: {"type": "bar",…

### Community 89 - "test_lru"
Cohesion: 0.08
Nodes (16): Design, LRUCache, lru.py — Hand-rolled LRU Cache (Milestone 1)…, O(1) Least-Recently-Used cache backed by: - dict[str, Node] — hash map for O(1)…, large_cache(), fixture, test_lru.py — Unit tests for neural_cache.lru (Milestone 7)…, Return average time per (set + get) operation in microseconds. (+8 more)

### Community 90 - "whatsapp_call"
Cohesion: 0.27
Nodes (10): flow_stream(), _click_voice_call_button(), confirm_whatsapp_call(), _focus_or_open_whatsapp(), _get_whatsapp_window(), initiate_whatsapp_call(), whatsapp_call.py — Jarvis Smart WhatsApp Calling Integration (Fully Isolated)…, Focus the WhatsApp window or open it if not running. Returns True on success. (+2 more)

### Community 91 - "prompt_enhancer_button"
Cohesion: 0.21
Nodes (11): _box_contains(), _box_set_value(), _clip_get(), _clip_set(), _ctrl(), _focus(), _focused_text(), _norm() (+3 more)

### Community 92 - "chat-routing"
Cohesion: 0.25
Nodes (7): Change recipes, Chat pipeline & routing (/chat), Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Purpose, Response formats

### Community 94 - "voice + hinglish_normalizer"
Cohesion: 0.15
Nodes (12): devanagari_to_hinglish(), _sub(), One Devanagari word → casual Hinglish roman ("चलाओ" → "chalao", "करना" →…, Romanize a Devanagari (Hindi) transcript for the backend, keeping any Latin…, _translit_dev_word(), Config (`app/core/config.py`, all optional env vars), Files & symbols (auto-generated, line numbers are current), Graphify (+4 more)

### Community 95 - "voice + voice_agent"
Cohesion: 0.15
Nodes (10): Feed streamed tokens; get back speakable sentences as early as possible., Speak an async generator of text chunks, sentence by sentence, pipelined., SentenceSplitter, speak_stream(), split_sentences(), AsyncClient, POST /chat with the spoken language, speak the reply into `ch` as it streams.…, stream_chat() (+2 more)

### Community 96 - "CODEMAP"
Cohesion: 0.22
Nodes (8): Backend core & API, Code map, Frontend (`frontend/src`, React 19 + Vite + Tailwind 4), Ignore these (no runtime role), Neural cache (neural_cache/, see its README.md), Scripts, Services (app/services), WhatsApp intelligence (app/services/whatsapp_intelligence)

### Community 97 - "assignment_answers + assignment_tool"
Cohesion: 0.16
Nodes (14): generate_answer(), generate_answers(), _groq_answer(), Generate an answer using Groq LLM with automatic model fallback chain. Tries…, Generate complete answers for ALL questions from an assignment. Tries these…, Generate an answer for a SINGLE question using Groq LLM directly (fast, no…, do_assignment(), Master orchestrator. Uses a background thread for all Playwright code. Yields… (+6 more)

### Community 99 - "llm + llm-personality"
Cohesion: 0.10
Nodes (24): classify_context(), context_classifier.py — Jarvis Situational Awareness…, Classify the situation from user input. Returns a dict with keys: urgency :…, generate_chat_response(), _groq_generate(), _is_complex_response(), _maybe_compress_history(), llm.py — Jarvis LLM Brain --------------------------- Model routing (all Groq):… (+16 more)

### Community 100 - "message_reader + thread_extractor"
Cohesion: 0.09
Nodes (31): _bring_whatsapp_to_front(), _get_whatsapp_window(), _heuristic_parse_ocr_lines(), _parse_uia_message_string(), message_reader.py — Jarvis WhatsApp Intelligence: Message Reader…, Restores and focuses WhatsApp window. Returns True on success., Walks the WhatsApp UIA accessibility tree to extract messages. WhatsApp Desktop…, Parses a raw UIA ListItem Name string into a structured message dict.… (+23 more)

### Community 101 - "youtube_control + KNOWN_ISSUES"
Cohesion: 0.15
Nodes (11): _fetch_results(), _find_channel(), _find_channel_at(), walk(), _initial_data(), Scrape YouTube's results page → [{id,title,channel,duration,seconds,views}]; []…, Best channel for a name → (title, '/@handle'), or None. Tries the 'Channels'…, Fixed on 2026-09-28 (+3 more)

### Community 102 - "package"
Cohesion: 0.40
Nodes (5): scripts, build, dev, lint, preview

### Community 103 - "ppt_content"
Cohesion: 0.29
Nodes (8): _parse_block(), _parse_chart(), parse_user_slides(), **Head**: text' / 'Head: text' / 'Head – text' → {head, text}. Verbatim…, Type: bar' + lines like 'Label: 42' or 'A=1, B=2' → chart dict (numbers…, Return strict slides if the text is written slide-by-slide, else []., _split_head(), _strip_md()

### Community 104 - "whatsapp"
Cohesion: 0.33
Nodes (6): _focus_or_open_whatsapp(), open_whatsapp(), Focus the WhatsApp window or open it if not running. Returns True on success., Opens the WhatsApp desktop app., Sends a WhatsApp message using the Windows desktop app via keyboard automation.…, send_whatsapp_message()

### Community 105 - "prompt-enhancer + prompt_enhancer_button"
Cohesion: 0.22
Nodes (10): _hint_text(), _ide_allows(), is_prompt_box(), In IDEs only chat / agent inputs qualify, never the code editor, the terminal,…, Entry points, Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify (+2 more)

### Community 106 - "ppt_tool"
Cohesion: 0.10
Nodes (27): _auto_select_image_layout(), _bg_fill(), _c(), compute_split_geometry(), _corner_L(), _detect_purpose(), extract_theme_from_image(), _groq_call() (+19 more)

### Community 107 - "ppt_studio + ppt_tool"
Cohesion: 0.20
Nodes (11): _collect_attachments(), edit(), Run fn(progress=cb) in a thread, yield progress strings live; result in…, _theme_from_text(), _with_progress(), ppt_edit(), Follow-up edit of the last deck (generator). See ppt_studio.edit., _ppt_edit() (+3 more)

### Community 108 - "hinglish_normalizer"
Cohesion: 0.25
Nodes (7): hinglish_to_devanagari(), normalize_for_tts(), hinglish_normalizer.py — Devanagari Crash Prevention + Text Normalizer…, Rewrite the Hindi words of a romanized Hinglish sentence in Devanagari, leaving…, Transform text so it's safe and natural-sounding for TTS: 1. Replace known…, Markdown → plain speakable text (keeps Devanagari). Also drops URLs and emoji., strip_markdown()

### Community 109 - "voice + tools"
Cohesion: 0.18
Nodes (10): Sets a reminder that Jarvis will speak after a given number of seconds., set_reminder(), get_player(), preload_local_stt(), Load the local Whisper models in the background (voice agent startup)., Speak a complete text. All sentences synthesise in parallel, play in order., speak_text(), Gotchas (+2 more)

### Community 110 - "screen-vision + screen_vision"
Cohesion: 0.18
Nodes (10): capture_screen_b64(), _pixel_diff_percent(), ndarray, Returns the percentage of pixels that changed significantly between two frames.…, Capture the primary monitor using mss (~10ms). Returns (base64_jpeg_string,…, Config, Files & symbols (auto-generated, line numbers are current), Graphify (+2 more)

### Community 111 - "youtube_control"
Cohesion: 0.20
Nodes (11): _dur_to_sec(), _parse_videos(), add(), walk(), Collect videos from ytInitialData: classic videoRenderer (search) and the newer…, Replace the session's result list with the videos actually on screen in the…, 1,234,567 views' / '82 million views' / '1.2M' → int., _screen_results() (+3 more)

### Community 112 - "README"
Cohesion: 0.50
Nodes (3): Expanding the ESLint configuration, React Compiler, React + Vite

### Community 113 - "ssml_processor"
Cohesion: 0.33
Nodes (5): add_human_prosody(), ssml_processor.py — Human Prosody Pre-processor…, Add natural speech prosody to plain text. Args: text: Plain text (already…, Remove all SSML tags from text — used when falling back to edge-tts which does…, strip_ssml()

### Community 119 - "voice"
Cohesion: 0.18
Nodes (5): _Player, ndarray, One persistent 24 kHz output stream driven by a callback that pulls from a…, Loudest output RMS in the last `window` s — the voice agent's echo reference., Play a clip as it arrives. Returns False if interrupted.

### Community 120 - "browser_mail"
Cohesion: 0.24
Nodes (7): check_emails(), _get_api_key(), list_unread(), browser_mail.py — Standard Browser Mail Automation…, A generic tool to perform any mail task (like sending or reading) by pre-…, smart_mail_action(), webbrowser

### Community 122 - "assignment_assembler"
Cohesion: 0.36
Nodes (7): assemble_assignment(), _create_powerpoint(), _create_word_doc(), _parse_qa_json(), Jarvis Assignment Tool — Phase 4: Document Assembly…, Assemble the extracted/humanized questions and answers into a formatted…, Extract and parse the JSON array from the input string.

### Community 124 - "ppt_designer"
Cohesion: 0.22
Nodes (7): _best_window(), Start fraction of the window (length=keep fraction) with most detail, biased to…, Largest body size so all items fit in (w,h). style: 'stack'|'inline'., Row-aligned multi-column list: item i sits in row i//cols, so rows line up., _runs_for(), _sizes(), Layout engine (`ppt_designer.py`)

### Community 125 - "screen_vision + screen_reader"
Cohesion: 0.22
Nodes (9): describe_screen_for_llm(), Returns a clean, LLM-optimized description of the current screen. Used as…, describe_screen_vlm(), Lightweight passive description — used as context injection in chat.py. Always…, Start the passive background screen watcher. Args: callback: Function called…, start_background_watcher(), get_active_window_info(), Returns a text summary of the currently focused window: window title + list of… (+1 more)

### Community 126 - "voice + context_classifier"
Cohesion: 0.25
Nodes (8): detect_language(), Detect whether the user spoke English, Hinglish, or Hindi. Returns: 'english' —…, language_mismatch(), True if a reply sentence is in the other language than the one the user spoke., hi' → Hindi voice, 'en' → English voice, for one sentence., Barge-in "stop": silence now and drop everything queued., route_language(), TTS (`voice.Speaker`, `start_clip`, `_Player`)

### Community 127 - "assignment"
Cohesion: 0.33
Nodes (5): Assignment solver (5 phases), Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Purpose

### Community 128 - "chat + youtube_control"
Cohesion: 0.06
Nodes (50): _clean_yt_query(), clear_history(), detect_note_intent(), detect_whatsapp_call(), detect_whatsapp_send(), keyword_detect_tool(), _semantic_window_adjust(), _media_target() (+42 more)

### Community 129 - "screen_reader + screen_vision"
Cohesion: 0.50
Nodes (4): Tool-callable version — called when user asks 'what's on my screen?' Routes…, read_screen_as_tool(), _classify_intent(), Parse the user's phrasing to determine the response mode. describe → "What am I…

### Community 130 - "smart_navigator"
Cohesion: 0.50
Nodes (4): Resolve a verbal site name like 'unstop' to a URL like 'https://unstop.com'., Resolves site name, opens a VISIBLE browser, and performs a search or action…, _resolve_url(), smart_web_action()

### Community 131 - "ppt_studio"
Cohesion: 0.33
Nodes (4): _assign_images(), Put each image on its best slide. Explicit instructions win. Mutates deck;…, Move images off slides whose layout can't show them (or has too many) onto…, _rebalance()

### Community 133 - "whatsapp"
Cohesion: 0.33
Nodes (5): Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Purpose, WhatsApp: send, call, read, reply-style cloning

## Knowledge Gaps
- **152 isolated node(s):** `Settings`, `build`, `dev`, `lint`, `preview` (+147 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1256 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **24 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Tool registry` connect `tools` to `chat + youtube_control`, `assignment_tool`, `calendar_tool + memory_tool`, `smart_navigator`, `rag_memory + memory`, `window_layout`, `youtube_control`, `syllabus_auditor`, `browser_tool`, `file_ops`, `assignment_humanizer`, `task_ledger`, `content_humanizer + content-tools`, `dark_enhancement + dark_video_enhancement`, `whatsapp_smart + tools`, `memory_tool`, `agentic_web + tool-registry`, `rag_memory + chat`, `air-drawing + air_drawing_tool`, `agents + tool_runner`, `web_search + tools`, `ui_inspector + tools`, `spotify_service`, `ppt + ppt_content`, `whatsapp_call`, `assignment_answers + assignment_tool`, `whatsapp`, `ppt_studio + ppt_tool`, `voice + tools`, `browser_mail`, `assignment_assembler`?**
  _High betweenness centrality (0.179) - this node is a cross-community bridge._
- **Why does `open_air_drawing()` connect `air-drawing + air_drawing_tool` to `tools`?**
  _High betweenness centrality (0.115) - this node is a cross-community bridge._
- **Are the 118 inferred relationships involving `Tool registry` (e.g. with `keyword_detect_tool()` and `_run_direct_tool()`) actually correct?**
  _`Tool registry` has 118 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `chat_endpoint()` (e.g. with `describe_screen_for_llm()` and `get_screen_text_summary()`) actually correct?**
  _`chat_endpoint()` has 7 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Settings`, `build`, `dev` to the rest of the system?**
  _152 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `tools` be split into smaller, more focused modules?**
  _Cohesion score 0.03639240506329114 - nodes in this community are weakly interconnected._
- **Should `server + acoustic_tripwire` be split into smaller, more focused modules?**
  _Cohesion score 0.09848484848484848 - nodes in this community are weakly interconnected._