# Graph Report - Jarvis  (2026-09-28)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 2253 nodes · 4304 edges · 132 communities (112 shown, 20 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 468 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `cb8a3aa4`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- tools
- chat + dag_executor
- assignment_tool
- screen-vision + main
- ppt_chart_engine
- rag_memory
- window_layout
- engine + test_protocol
- reply_generator
- syllabus_auditor
- persistence + config
- test_protocol
- browser_tool + smart_navigator
- jarvis_overlay + test_hindi_tts
- file_ops
- ppt_tool
- assignment_humanizer
- memory_tool + calendar_tool
- skill_prompt_enhancer + prompt_enhancement_library
- mysql_db + init_rag_memory
- assignment_answers
- task_ledger + resume_detector
- style_profiler
- chat
- message_reader
- ppt_router + ppt_tool
- package
- gestureController + gestureInterpreter
- memory
- agentic_web
- content_humanizer + content-tools
- dark_enhancement + dark_video_enhancement
- dsa_enforcer + dsa-mode
- whatsapp_smart + tools
- gmail_tool
- prompt_overlay
- ui_inspector
- server
- dag_executor + dynamic_skill
- ppt_image_engine + ppt_tool
- thread_extractor
- transformEngine
- voice_agent
- air-drawing + air_drawing_tool
- safe_executor
- voice
- package + App
- acoustic_tripwire
- memory + rag_memory
- assignment_pipeline
- client
- interactionEngine + DrawingCanvas
- personality + llm
- package
- strokeManager
- benchmark
- test_lru
- lru
- main
- web_search + tools
- test_lru
- tool-registry
- spotify_service + whatsapp_call
- acoustic_tripwire
- test_protocol + protocol
- ARCHITECTURE + frontend
- shapeManager
- assignment_answers + assignment_tool
- youtube_control
- test_wa + find_call_btn
- assignment_tool
- drawingEngine
- screen_vision + screen_reader
- test_lru
- test_lru
- vector_store + database
- email-calendar + agentic_web
- voice_agent
- jarvis_overlay
- test_concurrency
- package
- handTracking
- persistence
- chat-routing
- assignment_tool
- tool_runner + tools
- ControlPanel + HandSkeleton
- strokeRefiner
- voice + hinglish_normalizer
- test_lru
- README
- client
- ppt_chart_engine
- CLAUDE
- assignment_assembler + assignment_pipeline
- CODEMAP
- neural-cache
- test_lru
- llm + llm-personality
- tools
- ppt
- package
- test_protocol + protocol
- tools + ui_inspector
- lru
- ppt_tool
- calendar_tool
- agents
- voice + acoustic_tripwire
- assignment + assignment_answers
- whatsapp
- README
- ssml_processor
- __init__
- README
- chat
- ui_inspector
- PROMPT_TEMPLATE
- os-control
- FEATURES
- dump_wa_ui
- benchmark
- KNOWN_ISSUES + chat
- memory
- memory
- tools + ui_inspector
- tools + ui_inspector
- debug_wa

## God Nodes (most connected - your core abstractions)
1. `Tool registry` - 111 edges
2. `chat_endpoint()` - 40 edges
3. `2. Tool Registry (`tools.py`)` - 34 edges
4. `PresentationBuilder` - 31 edges
5. `CacheClient` - 27 edges
6. `LRUCache` - 26 edges
7. `ppt_create()` - 23 edges
8. `TransformEngine` - 21 edges
9. `PromptOverlay` - 20 edges
10. `CacheEngine` - 20 edges

## Surprising Connections (you probably didn't know these)
- `Change recipes` --references--> `keyword_detect_tool()`  [INFERRED]
  docs/features/chat-routing.md → app/api/chat.py
- `Adding a tool (checklist)` --references--> `keyword_detect_tool()`  [INFERRED]
  docs/features/tool-registry.md → app/api/chat.py
- `Graphify` --references--> `ppt_create()`  [INFERRED]
  docs/features/ppt.md → app/services/ppt_tool.py
- `HTTP endpoints` --references--> `init_rag_memory()`  [INFERRED]
  docs/ARCHITECTURE.md → app/services/rag_memory.py
- `Tool registry` --references--> `initiate_whatsapp_call()`  [INFERRED]
  docs/TOOLS.md → app/services/whatsapp_call.py

## Import Cycles
- None detected.

## Communities (132 total, 20 thin omitted)

### Community 0 - "tools"
Cohesion: 0.04
Nodes (73): append_to_file(), cache_get(), cache_set(), close_specific_window(), close_sticky_notes(), close_tab(), copy_selected_text(), create_file() (+65 more)

### Community 1 - "chat + dag_executor"
Cohesion: 0.13
Nodes (22): _clean_yt_query(), detect_note_intent(), keyword_detect_tool(), _semantic_window_adjust(), Fast, 100% reliable keyword-based tool detection. Runs BEFORE the LLM router to…, Remove trailing action phrases from a YouTube search query., is_dag_task(), Returns True when the user's request requires a multi-branch DAG plan. More… (+14 more)

### Community 2 - "assignment_tool"
Cohesion: 0.22
Nodes (10): _clean_text(), _extract_marks(), _has_figure_reference(), Clean up PDF text extraction artifacts., Smart regex-based question extractor for structured, numbered assignments.…, Given a parent question body, split out sub-questions (i, ii, iii, a, b, c) and…, Extract marks from question text if mentioned., Check if question references a figure or diagram. (+2 more)

### Community 3 - "screen-vision + main"
Cohesion: 0.14
Nodes (14): _on_screen_alert(), Callback fired by the background watcher when something notable is detected.…, Start background screen watcher and RAG memory system when the server boots., startup_event(), Start the passive background screen watcher. Args: callback: Function called…, start_background_watcher(), Config, Entry points (+6 more)

### Community 4 - "ppt_chart_engine"
Cohesion: 0.12
Nodes (34): _bg_color(), _extract_strict_metric(), _fig_to_bytes(), _hex(), _metrics_to_bar(), _palette_colors(), ppt_chart_engine.py — Dynamic Data-Visualization Engine for JARVIS PPT…, Horizontal or vertical bar chart. (+26 more)

### Community 5 - "rag_memory"
Cohesion: 0.13
Nodes (23): _extract_topics(), _get_faiss_lock(), get_memory_stats(), init_rag_memory(), _load_faiss_index(), Lock, rag_memory.py — Jarvis Long-Term RAG Memory Engine…, Persist FAISS index and ID map to disk (sync, runs in thread executor). (+15 more)

### Community 6 - "window_layout"
Cohesion: 0.08
Nodes (39): focus_window(), maximize_window(), Maximizes a specific window by name using Win32 ShowWindow., Bring a window to the foreground by partial name match (Win32 API, no…, Block until a window with the given name appears, then focus it., wait_for_window(), adjust_active_window(), _enumerate_app_windows() (+31 more)

### Community 7 - "engine + test_protocol"
Cohesion: 0.15
Nodes (13): CacheEngine, Any, Route a command dict to the appropriate handler. All handlers return a response…, Owns the LRUCache. Runs a single consumer loop on a dedicated thread. External…, Spawn the single writer thread. Call once at server boot., Gracefully stop the engine writer thread., The single consumer loop. Runs on CacheEngineThread. Processes one command at a…, err_response() (+5 more)

### Community 8 - "reply_generator"
Cohesion: 0.10
Nodes (25): generate_reply_draft(), Read the latest WhatsApp thread with a contact and generate 3 reply drafts that…, _build_system_prompt(), _build_user_prompt(), _call_groq(), generate_reply_draft(), get_cached_contact(), get_cached_drafts() (+17 more)

### Community 9 - "syllabus_auditor"
Cohesion: 0.05
Nodes (40): _approx_token_count(), _assemble_response(), audit_playlist_syllabus(), _build_vector_store(), _chunk_transcript(), _coverage_level(), _embed_texts(), _extract_playlist_id() (+32 more)

### Community 10 - "persistence + config"
Cohesion: 0.07
Nodes (38): Settings, acoustic_tripwire.py — Jarvis Acoustic Wake Engine…, agentic_web.py — Smart Web Research Engine for Jarvis…, Jarvis Assignment Tool — Phase 4: Document Assembly…, Jarvis Assignment Tool — Phase 3: Answer Humanizer…, Jarvis Assignment Tool — Phase 1: Smart Question Extractor…, nlp_extractor.py — LLM-Powered Fact & Entity Extractor…, research_pipeline.py — End-to-End Autonomous Research Orchestrator… (+30 more)

### Community 11 - "test_protocol"
Cohesion: 0.18
Nodes (10): decode_message(), Read exactly one message from a socket, handling partial TCP reads correctly.…, make_fake_socket(), fake_recv(), 1 MB value — tests that the length prefix handles large messages., The fake socket returns 1 byte at a time. _recv_exact must loop until it has…, Socket closes after 2 bytes — ConnectionError expected., Socket delivers the header but then closes before the body. (+2 more)

### Community 12 - "browser_tool + smart_navigator"
Cohesion: 0.09
Nodes (36): browse_and_paginate(), browse_and_read(), _clean_text(), click_element(), _ensure_url(), fill_form(), _llm_extract(), _new_browser_page() (+28 more)

### Community 13 - "jarvis_overlay + test_hindi_tts"
Cohesion: 0.25
Nodes (4): pil, Jarvis Arc Reactor Overlay -------------------------- A floating, always-on-…, Test language-adaptive TTS - plays English then Hindi to verify both engines…, sys

### Community 14 - "file_ops"
Cohesion: 0.10
Nodes (26): append_file(), bulk_rename(), delete_file(), diff_files(), _fmt_size(), list_directory(), _maybe_summarize(), move_file() (+18 more)

### Community 15 - "ppt_tool"
Cohesion: 0.16
Nodes (22): _clean_image_path(), compute_split_geometry(), _get_image_aspect_ratio(), _oval(), _parse_bullet(), _parse_card(), PresentationBuilder, _frame() (+14 more)

### Community 16 - "assignment_humanizer"
Cohesion: 0.09
Nodes (24): _extract_output_text(), _fill_input(), _find_element(), _get_browser_page(), humanize_all_answers(), _humanize_chunk_via_browser(), humanize_text(), _humanize_via_browser() (+16 more)

### Community 17 - "memory_tool + calendar_tool"
Cohesion: 0.13
Nodes (25): check_today_schedule(), What's on today's agenda, with time remaining until each event., _ensure_memory_file(), forget_fact(), _fuzzy_match_topics(), get_all_facts_as_context(), get_morning_brief(), _load_memory() (+17 more)

### Community 18 - "skill_prompt_enhancer + prompt_enhancement_library"
Cohesion: 0.11
Nodes (32): check_for_hallucination(), classify_prompt(), detect_domain(), prompt_enhancement_library.py…, Returns: 'conversational' | 'vague' | 'technical', Returns True if hallucination or chatbot-mode signals are detected., If the output starts with a chatbot filler opener, strip the first sentence. If…, Cut the output at the first leaked-reasoning pattern found. (+24 more)

### Community 19 - "mysql_db + init_rag_memory"
Cohesion: 0.17
Nodes (13): aiomysql, close_mysql(), get_mysql_pool(), init_mysql(), mysql_db.py — Jarvis Async MySQL Connection Pool…, Gracefully close the MySQL connection pool on server shutdown., Return the shared MySQL connection pool, initializing it if needed., Initialize the MySQL connection pool and ensure all required tables exist. Safe… (+5 more)

### Community 20 - "assignment_answers"
Cohesion: 0.15
Nodes (20): _ask_question_on_page(), _find_input(), _get_persistent_page(), Jarvis Assignment Tool — Phase 2: Answer Generation…, Launch a visible (non-headless) Chromium with a persistent profile. Login…, Try CSS selectors to find the visible chat input. Returns locator or None., Type a message into the AI chat input and submit it., Upload PDF to the AI chat page. Returns True if upload was initiated. (+12 more)

### Community 21 - "task_ledger + resume_detector"
Cohesion: 0.07
Nodes (35): detect_resume_intent(), _extract_task_resource(), _find_best_task_match(), get_resume_context_string(), _has_continuation_verb(), _has_fresh_task_indicator(), _has_reference_phrase(), resume_detector.py — Jarvis Resume Intent Classifier… (+27 more)

### Community 22 - "style_profiler"
Cohesion: 0.13
Nodes (25): build_style_profile(), One-time training: parse a WhatsApp .txt chat export to build your personal…, add_deflection_phrase(), build_style_profile(), _compute_profile_stats(), _empty_profile(), get_profile_summary(), _load_profile() (+17 more)

### Community 23 - "chat"
Cohesion: 0.20
Nodes (12): chat_endpoint(), _dag_stream_with_history(), planner_stream(), response_stream_with_history(), tool_stream(), detect_whatsapp_call(), detect_whatsapp_send(), post (+4 more)

### Community 24 - "message_reader"
Cohesion: 0.15
Nodes (18): _bring_whatsapp_to_front(), _get_whatsapp_window(), _heuristic_parse_ocr_lines(), _parse_uia_message_string(), message_reader.py — Jarvis WhatsApp Intelligence: Message Reader…, Restores and focuses WhatsApp window. Returns True on success., Walks the WhatsApp UIA accessibility tree to extract messages. WhatsApp Desktop…, Parses a raw UIA ListItem Name string into a structured message dict.… (+10 more)

### Community 25 - "ppt_router + ppt_tool"
Cohesion: 0.10
Nodes (26): build_ppt(), generate(), create_ppt_backend(), generate(), extract_theme(), get_styles(), PPTBuildRequest, PPTCreateRequest (+18 more)

### Community 26 - "package"
Cohesion: 0.11
Nodes (20): name, private, type, version, autoprefixer, eslint, ref_eslint_config, @eslint/js (+12 more)

### Community 28 - "memory"
Cohesion: 0.17
Nodes (14): format_preferences_for_prompt(), get_all_preferences(), list_skills(), Jarvis Vector Memory — ChromaDB-based long-term memory engine. Stores and…, Returns a string suitable for injecting into LLM prompts., Stable short ID based on content hash., List all saved skill descriptions., Store a user preference (e.g. key='browser', value='Chrome'). (+6 more)

### Community 29 - "agentic_web"
Cohesion: 0.12
Nodes (14): _build_search_queries(), _fetch_page_text(), __init__(), _get_api_key(), Download a page and return clean readable text (no HTML tags)., Use the LLM to extract specific listings from the fetched content., Return known direct listing URLs for a site+task combo., Build 2-3 specific search queries that will hit listing pages, not homepages. (+6 more)

### Community 30 - "content_humanizer + content-tools"
Cohesion: 0.09
Nodes (34): build_structure_prompt(), build_vocab_prompt(), call_groq(), check_similarity(), detect_tone(), fact_check(), get_groq_client(), get_sentence_scores() (+26 more)

### Community 31 - "dark_enhancement + dark_video_enhancement"
Cohesion: 0.09
Nodes (29): _apply_gamma(), _fusion_and_polish(), get_all_enhancements(), _normalize_to_8bit(), _path_1_retinex(), _path_2_wavelet(), ndarray, run_pipeline_a() (+21 more)

### Community 32 - "dsa_enforcer + dsa-mode"
Cohesion: 0.11
Nodes (17): _cache_del(), _cache_set(), DSAEnforcer, get_dsa_enforcer(), Write to Neural Cache, silently skipping if unavailable., Delete from Neural Cache, silently skipping if unavailable., Data, DSA / LeetCode enforcer mode (+9 more)

### Community 33 - "whatsapp_smart + tools"
Cohesion: 0.08
Nodes (33): close_window(), Snaps left_app to left half and right_app to right half using Win32 API (no…, Closes the current active real app window (skips the Jarvis overlay)., Open a WhatsApp chat, read the last N messages, and return a structured thread…, read_whatsapp_thread(), snap_windows(), _clear_search(), confirm_whatsapp_send() (+25 more)

### Community 34 - "gmail_tool"
Cohesion: 0.17
Nodes (19): check_emails(), _decode_body(), _format_date(), get_email_body(), _get_gmail_service(), _get_header(), list_unread(), gmail_tool.py — Jarvis Gmail Integration (Step 5)… (+11 more)

### Community 35 - "prompt_overlay"
Cohesion: 0.11
Nodes (6): main(), PromptOverlay, prompt_overlay.py ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Jarvis…, Strip the **ENHANCED PROMPT (CODING):** header if present., keyboard, tkinter

### Community 36 - "ui_inspector"
Cohesion: 0.10
Nodes (11): Walk all descendants looking for any control whose window_text contains `text`…, Fire an element's primary action via UIA Invoke pattern. No mouse movement —…, Inject text into an input element via UIA Value pattern. No simulated…, Read text from an element via UIA TextPattern or window_text. Returns empty…, Walk the accessibility tree and return all elements up to `depth` levels. Use…, Core wrapper around pywinauto's UIA backend. All interactions go through the OS…, Get a window wrapper by partial title match (regex-safe). Returns None if not…, Get the currently focused window via Win32 HWND matching. (+3 more)

### Community 37 - "server"
Cohesion: 0.12
Nodes (12): CacheServer, main(), Path, Full startup: recover state, start engine, begin accepting connections., Restore cache state from disk before the engine thread starts. Called on the…, Main thread: bind socket and accept connections indefinitely., One thread per connected client. Reads commands, enqueues them to the engine,…, Graceful shutdown: take a final snapshot, stop engine, close socket. (+4 more)

### Community 38 - "dag_executor + dynamic_skill"
Cohesion: 0.07
Nodes (48): app_memory, find_skill(), Persist a successful dynamic skill for future reuse., Returns up to n most relevant saved skills for a given task description. Each…, save_skill(), _call_dag_planner(), DAGNode, _execute_node() (+40 more)

### Community 39 - "ppt_image_engine + ppt_tool"
Cohesion: 0.09
Nodes (32): build_image_descriptors(), _extract_keywords(), get_aspect_ratio(), ImageDescriptor, match_images_to_slides(), _parse_slide_ref(), _parse_slide_ref_by_title(), ppt_image_engine.py — Semantic Image-Slide Matcher for JARVIS PPT Engine… (+24 more)

### Community 40 - "thread_extractor"
Cohesion: 0.19
Nodes (13): extract_thread(), extract_thread_as_string(), _find_latest_incoming(), _get_current_chat_title(), _group_into_turns(), _open_contact_chat(), thread_extractor.py — Jarvis WhatsApp Intelligence: Thread Extractor…, Merges consecutive messages from the same sender into a single turn. This makes… (+5 more)

### Community 42 - "voice_agent"
Cohesion: 0.13
Nodes (22): detect_language(), Detect whether the user spoke English, Hinglish, or Hindi. Returns: 'english' —…, Speaks a full text response — splits into sentences for faster first word., speak_text(), httpx, psutil, pyaudio, random (+14 more)

### Community 43 - "air-drawing + air_drawing_tool"
Cohesion: 0.18
Nodes (9): open_air_drawing(), Opens the Air Drawing Canvas on the screen. This feature allows the user to…, Air drawing (webcam hand drawing), Files & symbols (auto-generated, line numbers are current), Flow, Gotchas, Graphify, Purpose (+1 more)

### Community 44 - "safe_executor"
Cohesion: 0.14
Nodes (17): execute_safe(), Safe Code Executor for Jarvis ------------------------------- Runs LLM-…, Restricted open(): blocks writes to system paths., Restricted __import__: blocks dangerous modules., Raised when generated code violates safety constraints., AST visitor that inspects generated code before execution., Parse and walk the AST, raising SecurityError on violations., Validates and runs 'code' in a restricted namespace. Returns: (success: bool,… (+9 more)

### Community 45 - "voice"
Cohesion: 0.10
Nodes (22): hinglish_normalizer.py — Devanagari Crash Prevention + Text Normalizer…, _filter_hallucinations(), _kokoro_speak_sync(), _load_kokoro(), _load_whisper_model(), voice.py — Jarvis Voice Engine ------------------------------ STT: faster-…, Return empty string if text is a known Whisper hallucination., Transcribe audio using the local faster-whisper model. Runs synchronously… (+14 more)

### Community 46 - "package + App"
Cohesion: 0.16
Nodes (11): App(), ChatMessage(), API_BASE, frontend_src_index, lucide-react, react, ref_react_dom_client, react-markdown (+3 more)

### Community 47 - "acoustic_tripwire"
Cohesion: 0.10
Nodes (12): AcousticWakeEngine, get_wake_event(), Background thread that watches the microphone for a double-clap pattern. Usage…, Start the background listening thread., Signal the background thread to exit and wait for it., Resume detection after a disable()., Pause detection without stopping the thread (fast resume)., Signal the background thread to re-run calibration on the next cycle. Returns… (+4 more)

### Community 48 - "memory + rag_memory"
Cohesion: 0.15
Nodes (20): forget_memory(), ForgetRequest, ingest_memory(), IngestRequest, BaseModel, delete, post, app/api/memory.py — Jarvis Long-Term Memory API Router… (+12 more)

### Community 49 - "assignment_pipeline"
Cohesion: 0.20
Nodes (17): _browser_thread(), _find_el(), _get_answer(), _get_browser_ctx(), _groq_answer(), _groq_humanize(), _humanize_browser(), Queue (+9 more)

### Community 50 - "client"
Cohesion: 0.12
Nodes (10): Send one of the reply drafts generated by generate_reply_draft. draft_index is…, send_style_reply(), Any, Store a key-value pair, optionally with a TTL. Args: key: Cache key. value:…, Delete a key from the cache. Returns: True if the key existed and was deleted,…, Retrieve server statistics (hit rate, evictions, cache size, etc.). Returns…, Send a command and return the response. Thread-safe. Handles lazy connect and…, Open a socket to the server if not already connected. Called within the lock —… (+2 more)

### Community 52 - "personality + llm"
Cohesion: 0.19
Nodes (8): calendar_tool.py — Jarvis Google Calendar Integration (Step 8)…, context_classifier.py — Jarvis Situational Awareness…, llm.py — Jarvis LLM Brain --------------------------- Model routing (all Groq):…, get_context_aware_prompt(), personality.py — Jarvis Character & Personality Engine…, Returns a dynamically adjusted system prompt based on: - Time of day (hour:…, collections, datetime

### Community 53 - "package"
Cohesion: 0.14
Nodes (14): devDependencies, autoprefixer, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, postcss (+6 more)

### Community 55 - "benchmark"
Cohesion: 0.25
Nodes (5): main(), measure_latency(), measure_throughput(), Spin up n_threads threads each doing ops_per_thread SET+GET pairs. Returns…, Run op_fn warmup times (discard), then timed times (measure). Returns (mean_µs,…

### Community 56 - "test_lru"
Cohesion: 0.18
Nodes (7): large_cache(), fixture, test_lru.py — Unit tests for neural_cache.lru (Milestone 7)…, LRU cache with capacity 3 — easy to reason about eviction., small_cache(), TestSentinels, pytest

### Community 57 - "lru"
Cohesion: 0.13
Nodes (12): LRUCache, Node, Insert or update a key-value pair. - If key already exists: update value + TTL,…, Remove a key from the cache. Returns True if the key existed, False if it was…, Place node at the MRU (most-recently-used) end of the list., Remove node from its current position in the list (O(1) because doubly-linked)., Evict a specific node (unlink + remove from map)., A doubly-linked list node holding one cache entry. Attributes: key (str): Cache… (+4 more)

### Community 58 - "main"
Cohesion: 0.10
Nodes (26): get_alerts(), get, post, Stop watcher, acoustic tripwire, and close DB pool cleanly on server shutdown., Frontend polls this endpoint to receive proactive JARVIS screen alerts. e.g.…, Return current acoustic tripwire state for the frontend toggle., Arm the acoustic tripwire so double-claps wake Jarvis., Disarm the acoustic tripwire (engine keeps running, just paused). (+18 more)

### Community 59 - "web_search + tools"
Cohesion: 0.05
Nodes (41): NLPExtractor, Runs extraction on each scraped source and aggregates the results. Returns a…, Scrapes the web for a topic and extracts verified facts and statistics. Yields…, research_topic(), research_scraper.py — Autonomous Web Research Scraper…, Searches DDG for the topic, fetches the top N links concurrently, and returns…, ResearchScraper, _extract_location() (+33 more)

### Community 60 - "test_lru"
Cohesion: 0.50
Nodes (3): Return average time per (set + get) operation in microseconds., Per-op time for N=1000 vs N=100000 should be within 3x of each other. If the…, TestO1Timing

### Community 61 - "tool-registry"
Cohesion: 0.29
Nodes (6): Adding a tool (checklist), Calling tools from code, Files & symbols (auto-generated, line numbers are current), Graphify, Purpose, Tool registry & adding tools

### Community 62 - "spotify_service + whatsapp_call"
Cohesion: 0.06
Nodes (48): flow_stream(), _buttons(), _clean_query(), _com_init(), _content_play_buttons(), _find_spotify_window(), _is_playing(), _now_playing_title() (+40 more)

### Community 63 - "acoustic_tripwire"
Cohesion: 0.21
Nodes (9): calibrate_tripwire(), _generate_chime(), ndarray, Root Mean Square amplitude. Cast to float64 to prevent int16 overflow., FFT-based dominant frequency. Only inspect the positive half-spectrum (0 ……, Return True if this chunk looks like a clap/snap (loud + right frequency)., Main loop — opened inside the thread so PyAudio errors stay contained. State…, Generate a pleasant two-tone wake chime as a float32 numpy array. (+1 more)

### Community 64 - "test_protocol + protocol"
Cohesion: 0.19
Nodes (10): protocol.py — Wire Protocol for Neural Cache (Milestone 2)…, Loop until exactly n bytes have been read from sock. This is necessary because…, _recv_exact(), make_socket_from_messages(), test_protocol.py — Unit tests for neural_cache.protocol (Milestone 7)…, Encode two separate messages and feed them through the same socket.…, Encode multiple messages and concatenate them into a single stream., TestMultiMessage (+2 more)

### Community 65 - "ARCHITECTURE + frontend"
Cohesion: 0.13
Nodes (13): Architecture, Frontend (`frontend/src`), HTTP endpoints, LLM usage, Memory layers (five separate stores), Processes, Files & symbols (auto-generated, line numbers are current), Gotchas (+5 more)

### Community 67 - "assignment_answers + assignment_tool"
Cohesion: 0.33
Nodes (6): generate_answers(), _groq_answer(), Generate an answer using Groq LLM with automatic model fallback chain. Tries…, Generate complete answers for ALL questions from an assignment. Tries these…, Resolve PDF path: handles full paths, filenames, partial names., _resolve_pdf_path()

### Community 68 - "youtube_control"
Cohesion: 0.08
Nodes (38): check_emails(), _get_api_key(), list_unread(), browser_mail.py — Standard Browser Mail Automation…, A generic tool to perform any mail task (like sending or reading) by pre-…, smart_mail_action(), _dur_to_sec(), _end_session() (+30 more)

### Community 69 - "test_wa + find_call_btn"
Cohesion: 0.21
Nodes (6): Find the Voice Call button position in WhatsApp Desktop window. Run this while…, Step 1: Open WhatsApp, go to any chat (e.g. Archit Shukla) Step 2: Hover your…, pyautogui, pygetwindow, pyperclip, Validate the computed call button position and take a screenshot to verify. Run…

### Community 70 - "assignment_tool"
Cohesion: 0.25
Nodes (8): _classify_question_type(), _extract_via_vision(), _parse_llm_json_response(), _pdf_pages_to_images(), Render each PDF page to a base64-encoded JPEG using PyMuPDF., Heuristically classify a question type based on its text., Render each PDF page as an image and extract questions using Groq Vision. Best…, Robustly parse an LLM response expected to be a JSON array of question dicts.

### Community 72 - "screen_vision + screen_reader"
Cohesion: 0.06
Nodes (53): _accessibility_tree(), describe_screen_for_llm(), get_screen_screenshot_b64(), _groq_vision_screen(), _init_tesseract(), _ocr_screen(), screen_reader.py — Jarvis Screen Vision (VLM-first architecture)…, Legacy OCR layer. Works on any app but extracts raw text only — no layout,… (+45 more)

### Community 73 - "test_lru"
Cohesion: 0.20
Nodes (5): Accessing 'a' should move it to MRU and save it from eviction., Re-setting an existing key should move it to MRU., len(cache.map) must never exceed capacity., Fill to capacity+1. The first key inserted (LRU) should be evicted., TestEviction

### Community 75 - "vector_store + database"
Cohesion: 0.33
Nodes (7): get_db_pool(), init_db(), Queries the table and uses the pgvector cosine distance operator (<=>) to fetch…, Inserts text chunks and vectors into the knowledge_store table., save_document_chunk(), search_similar_chunks(), asyncpg

### Community 76 - "email-calendar + agentic_web"
Cohesion: 0.13
Nodes (15): agentic_web_action(), _worker(), Generator that streams progress and final answer., create_folder(), Create a new folder. Supports path shortcuts (Desktop, Downloads, etc.).…, _mail_tool(), Email tools: try the real Gmail API (gmail_tool) first, fall back to opening…, Email (+7 more)

### Community 77 - "voice_agent"
Cohesion: 0.18
Nodes (11): Accepts an async generator of text chunks. Buffers until a sentence is…, speak_stream(), AsyncClient, _clean_agentic_line(), _is_agentic_line(), Convert an agentic tag line into natural spoken text., Write Jarvis UI state so the overlay can animate accordingly., Streams the backend response and speaks it sentence-by-sentence. Handles two… (+3 more)

### Community 78 - "jarvis_overlay"
Cohesion: 0.20
Nodes (5): Image, generate_arc_reactor(), JarvisOverlay, Draws a beautiful arc reactor using PIL when no icon file is found., read_state()

### Community 79 - "test_concurrency"
Cohesion: 0.20
Nodes (8): Lock, 50 concurrent clients, each doing 1000 ops. After completion: - Server still…, The engine should report meaningful stats after the load test., While 10 threads hammer the cache, a separate thread pings repeatedly. All…, One client thread. Performs `ops` random GET/SET/DEL operations. Records any…, TestConcurrency, _ping_loop(), _worker()

### Community 80 - "package"
Cohesion: 0.22
Nodes (9): dependencies, framer-motion, lucide-react, react, react-dom, react-markdown, react-syntax-highlighter, remark-gfm (+1 more)

### Community 81 - "handTracking"
Cohesion: 0.31
Nodes (3): CameraView(), getHandsConstructor(), HandTracker

### Community 82 - "persistence"
Cohesion: 0.12
Nodes (10): Any, Path, Flush and close the file handle cleanly on server shutdown., Serialise cache state to disk and truncate the WAL. Called by CacheEngine on…, Load the snapshot from disk. Returns None if no snapshot exists yet. Called…, Append-only write-ahead log. Each SET/DEL command is written as a JSON line…, Append one command to the WAL and flush immediately. Flushing on every write is…, Read and parse all commands from the WAL file. Called once at startup for… (+2 more)

### Community 83 - "chat-routing"
Cohesion: 0.25
Nodes (7): Change recipes, Chat pipeline & routing (/chat), Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Purpose, Response formats

### Community 84 - "assignment_tool"
Cohesion: 0.22
Nodes (8): extract_questions(), _extract_via_llm_text(), _merge_and_deduplicate(), _pdf_pages_to_text(), Extract text from each PDF page separately. Returns list of page strings., LLM-based text extraction as fallback for when regex fails., Merge questions from all three tracks. Priority: regex > vision > llm text. A…, Extract ALL questions from an assignment PDF using a 3-track hybrid system.…

### Community 85 - "tool_runner + tools"
Cohesion: 0.20
Nodes (11): execute_tool(), BaseModel, post, ToolExecuteRequest, format_recall_for_prompt(), Format recalled memory turns into an injectable LLM context block with clear…, _call_sync(), tool_runner.py — Async execution of TOOL_REGISTRY entries for orchestrators… (+3 more)

### Community 86 - "ControlPanel + HandSkeleton"
Cohesion: 0.13
Nodes (13): frontend_src_airdrawing_airdrawing, COLORS, ControlPanel(), FONTS, SHAPES, FINGERTIP_INDICES, HAND_CONNECTIONS, HandSkeleton() (+5 more)

### Community 88 - "voice + hinglish_normalizer"
Cohesion: 0.22
Nodes (10): normalize_for_tts(), Transform text so it's safe and natural-sounding for TTS: 1. Replace known…, Speak via edge-tts + pygame. Uses the specified voice, defaults to English., Language-adaptive TTS pipeline: - English text → Kokoro am_adam (local, clear…, _tts_edge(), _tts_play(), TTS (`voice._tts_play`), main() (+2 more)

### Community 90 - "README"
Cohesion: 0.20
Nodes (9): Architecture, Benchmark, Files, LRU Cache Design, Neural Cache, Persistence, Running, Tests (+1 more)

### Community 91 - "client"
Cohesion: 0.24
Nodes (4): CacheClient, Explicitly close the socket connection., Close self._sock, suppressing errors. Called within the lock., Thread-safe client for the Neural Cache server. One instance can be safely…

### Community 92 - "ppt_chart_engine"
Cohesion: 0.33
Nodes (3): ChartEngine, Stateless chart renderer. All colors are derived from the active PPT palette —…, Render a chart from structured data. Args: chart_data: {"type": "bar",…

### Community 94 - "CLAUDE"
Cohesion: 0.29
Nodes (6): Adding / changing a tool (project rules, from JARVIS_ARCHITECTURE.md), Gotchas, graphify, Jarvis — Claude Code guide, Run, Where things are

### Community 95 - "assignment_assembler + assignment_pipeline"
Cohesion: 0.25
Nodes (8): assemble_assignment(), _create_powerpoint(), _create_word_doc(), _parse_qa_json(), Assemble the extracted/humanized questions and answers into a formatted…, Extract and parse the JSON array from the input string., do_assignment(), Master orchestrator. Uses a background thread for all Playwright code. Yields…

### Community 96 - "CODEMAP"
Cohesion: 0.22
Nodes (8): Backend core & API, Code map, Frontend (`frontend/src`, React 19 + Vite + Tailwind 4), Ignore these (no runtime role), Neural cache (neural_cache/, see its README.md), Scripts, Services (app/services), WhatsApp intelligence (app/services/whatsapp_intelligence)

### Community 97 - "neural-cache"
Cohesion: 0.25
Nodes (7): Design, Files & symbols (auto-generated, line numbers are current), Graphify, Neural cache (Redis-like LRU server), Purpose, Runtime, Tests

### Community 99 - "llm + llm-personality"
Cohesion: 0.13
Nodes (17): classify_context(), Classify the situation from user input. Returns a dict with keys: urgency :…, generate_chat_response(), _groq_generate(), _is_complex_response(), _maybe_compress_history(), Main LLM response generator. Streams response token by token. Injects user…, When conversation history exceeds 15 messages, compress the oldest 10 into a… (+9 more)

### Community 100 - "tools"
Cohesion: 0.08
Nodes (25): calculate(), create_word_doc(), get_system_info(), lock_screen(), open_app(), open_windows_copilot(), play_music(), Returns CPU usage, RAM usage, and battery status. (+17 more)

### Community 101 - "ppt"
Cohesion: 0.29
Nodes (6): Entry points, Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, PowerPoint generator, Purpose

### Community 102 - "package"
Cohesion: 0.40
Nodes (5): scripts, build, dev, lint, preview

### Community 103 - "test_protocol + protocol"
Cohesion: 0.39
Nodes (3): encode_message(), Serialise a dict to the wire format: [4-byte length][UTF-8 JSON body] Args:…, TestEncode

### Community 104 - "tools + ui_inspector"
Cohesion: 0.50
Nodes (4): Read the current text content of a UI element — e.g. a terminal output pane, a…, read_ui_element_text(), Read the current text content of a UI element (e.g. terminal output pane,…, read_element_text()

### Community 105 - "lru"
Cohesion: 0.29
Nodes (4): Any, Serialise the entire live cache to a plain dict. Expired entries are excluded —…, Restore cache state from a snapshot dict (produced by snapshot()). Called once…, Place node at the LRU (least-recently-used) end of the list.

### Community 106 - "ppt_tool"
Cohesion: 0.09
Nodes (18): _bg_fill(), _c(), _corner_L(), _detect_purpose(), _extract_theme_pil_local(), ppt_tool.py — Premium Visual-First PPT Engine v5…, Auto-detect presentation purpose from the user prompt., Computed image + text zone dimensions (in EMU — python-pptx native). (+10 more)

### Community 107 - "calendar_tool"
Cohesion: 0.33
Nodes (6): add_event(), _get_calendar_service(), get_upcoming_events(), Create a new event in Google Calendar. - title: "Project Meeting" - date:…, Authenticate and return a Google Calendar API service object., List events in the next N days.

### Community 108 - "agents"
Cohesion: 0.33
Nodes (5): Agents: DAG executor, linear planner, dynamic skills, Data, Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify

### Community 109 - "voice + acoustic_tripwire"
Cohesion: 0.18
Nodes (9): _play_chime(), Inline (shared-stream) mode — called by voice_agent.py on every audio frame it…, Play the wake chime via sounddevice (non-blocking from caller's perspective)., Files & symbols (auto-generated, line numbers are current), Flow (`scripts/voice_agent.py`, separate process), Gotchas, Graphify, Purpose (+1 more)

### Community 110 - "assignment + assignment_answers"
Cohesion: 0.18
Nodes (11): generate_answer(), Generate an answer for a SINGLE question using Groq LLM directly (fast, no…, list_assignments(), Scan Desktop, Documents, and Downloads for PDF files., Assignment solver (5 phases), Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify (+3 more)

### Community 111 - "whatsapp"
Cohesion: 0.33
Nodes (5): Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Purpose, WhatsApp: send, call, read, reply-style cloning

### Community 112 - "README"
Cohesion: 0.50
Nodes (3): Expanding the ESLint configuration, React Compiler, React + Vite

### Community 113 - "ssml_processor"
Cohesion: 0.33
Nodes (5): add_human_prosody(), ssml_processor.py — Human Prosody Pre-processor…, Add natural speech prosody to plain text. Args: text: Plain text (already…, Remove all SSML tags from text — used when falling back to edge-tts which does…, strip_ssml()

### Community 119 - "chat"
Cohesion: 0.67
Nodes (3): clear_history(), delete, Clears the conversation history (start fresh).

### Community 120 - "ui_inspector"
Cohesion: 0.40
Nodes (4): debug_ui_tree(), ui_inspector.py — Jarvis UIA Engine (Upgraded)…, Dump the full accessibility tree of an app window as a readable string. Use…, ctypes

### Community 122 - "os-control"
Cohesion: 0.33
Nodes (5): Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Purpose, Windows/OS control: windows, media, apps, files

### Community 124 - "dump_wa_ui"
Cohesion: 0.33
Nodes (5): find_controls(), Dump WhatsApp Desktop UI tree to find the Voice Call button name. Run this…, search_tree(), pywinauto, uiautomation

### Community 126 - "KNOWN_ISSUES + chat"
Cohesion: 0.40
Nodes (4): ChatRequest, BaseModel, Known issues, Open

### Community 127 - "memory"
Cohesion: 0.40
Nodes (5): get_history(), memory_stats(), get, Return statistics about Jarvis's long-term memory store. Includes total turns,…, Retrieve paginated conversation history from MySQL. Query params: limit (int):…

### Community 128 - "memory"
Cohesion: 0.40
Nodes (4): API, Files & symbols (auto-generated, line numbers are current), Graphify, Memory: RAG, facts, task ledger, resume, skills

### Community 129 - "tools + ui_inspector"
Cohesion: 0.50
Nodes (4): click_ui_element_uia(), Click a UI element inside an app by AutomationId, name, or control type. Does…, Click a UI element by AutomationId, name, or control type inside an app. Does…, smart_click()

### Community 130 - "tools + ui_inspector"
Cohesion: 0.50
Nodes (4): Inject text into a specific input field in an app via UIA Value pattern. No…, type_into_ui_element(), Inject text into a specific input field in an app via UIA Value pattern. No…, type_into_element()

## Knowledge Gaps
- **154 isolated node(s):** `Settings`, `Entry points`, `Files & symbols (auto-generated, line numbers are current)`, `Gotchas`, `Purpose` (+149 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1063 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Tool registry` connect `tools` to `chat + dag_executor`, `tools + ui_inspector`, `tools + ui_inspector`, `window_layout`, `syllabus_auditor`, `browser_tool + smart_navigator`, `file_ops`, `assignment_humanizer`, `memory_tool + calendar_tool`, `skill_prompt_enhancer + prompt_enhancement_library`, `task_ledger + resume_detector`, `ppt_router + ppt_tool`, `content_humanizer + content-tools`, `dark_enhancement + dark_video_enhancement`, `whatsapp_smart + tools`, `ppt_image_engine + ppt_tool`, `air-drawing + air_drawing_tool`, `memory + rag_memory`, `web_search + tools`, `spotify_service + whatsapp_call`, `assignment_answers + assignment_tool`, `youtube_control`, `email-calendar + agentic_web`, `assignment_tool`, `tool_runner + tools`, `assignment_assembler + assignment_pipeline`, `tools`, `tools + ui_inspector`, `calendar_tool`, `assignment + assignment_answers`?**
  _High betweenness centrality (0.194) - this node is a cross-community bridge._
- **Why does `open_air_drawing()` connect `air-drawing + air_drawing_tool` to `tools`?**
  _High betweenness centrality (0.122) - this node is a cross-community bridge._
- **Are the 110 inferred relationships involving `Tool registry` (e.g. with `keyword_detect_tool()` and `recall_memory()`) actually correct?**
  _`Tool registry` has 110 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `chat_endpoint()` (e.g. with `Jump table for the big files` and `Flow (`chat_endpoint`, order matters, first hit wins)`) actually correct?**
  _`chat_endpoint()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Settings`, `Entry points`, `Files & symbols (auto-generated, line numbers are current)` to the rest of the system?**
  _154 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `tools` be split into smaller, more focused modules?**
  _Cohesion score 0.03783783783783784 - nodes in this community are weakly interconnected._
- **Should `chat + dag_executor` be split into smaller, more focused modules?**
  _Cohesion score 0.13438735177865613 - nodes in this community are weakly interconnected._