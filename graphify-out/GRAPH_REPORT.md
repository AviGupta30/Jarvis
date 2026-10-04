# Graph Report - Jarvis  (2026-10-04)

## Corpus Check
- 232 files · ~363,666 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 6 file(s) not represented in the graph (top: (none) 3, .css 2, .bat 1)

## Summary
- 3912 nodes · 8501 edges · 176 communities (155 shown, 21 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 847 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c7c71aaa`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- tools
- planner + dynamic_skill
- analyzer
- plate
- ppt_chart_engine
- content_humanizer.py
- window_layout
- resume_builder + resume-exact-replica
- youtube_control
- syllabus_auditor
- ppt_studio + ppt_designer
- ppt_designer
- browser_tool
- lru
- file_ops
- ppt_tool
- assignment_answers
- resume_builder
- fontmatch + fonts
- prompt_enhancer_button
- engine + test_protocol
- ui_inspector + tools
- ppt_research
- ppt_template
- chat + llm
- ppt_router + ppt_tool
- package
- persistence
- storage + orchestrator
- ppt_image_engine
- task_ledger + test_task_resumption
- ppt_composer + ppt_designer
- dsa_enforcer + dsa-mode
- ppt_content
- server + persistence
- prompt_overlay
- ui_inspector
- agentic_web
- exact_render
- pipeline
- memory
- transformEngine
- resume_builder
- air-drawing + air_drawing_tool
- ppt_designer
- voice
- App.jsx
- AcousticWakeEngine
- ppt_composer + ppt_designer
- resume_builder
- client + test_concurrency
- interactionEngine + DrawingCanvas
- calendar_tool
- package
- strokeManager
- voice
- llm + llm-personality
- prompt_enhancement_library + skill_prompt_enhancer
- dark_video_enhancement.py
- web_search + tools
- safe_executor
- lru
- youtube_control + os-control
- ppt
- whatsapp_smart + tools
- Architecture
- shapeManager
- ppt_content
- spotify_service + media_sessions
- prompt_enhancer_button
- rag_memory + memory
- drawingEngine
- jarvis_overlay
- test_lru
- voice
- assignment_humanizer
- agents + tool_runner
- uia_local
- VoiceAgent
- gmail_tool + memory_tool
- package
- Content humanizer & social content
- dag_executor
- screen_vision + screen_reader
- repair
- hinglish_normalizer + voice
- AirDrawingApp.jsx
- strokeRefiner
- ppt_chart_engine
- compiler
- ingest
- measure
- ppt_content
- tool-registry + vector_store
- voice_agent.py
- schema + bindings
- youtube_player
- compiler
- compiler
- resume_campus + measure
- resume_detector
- repair
- schema
- modes
- style_profiler + reply_generator
- ppt_tool
- assignment_tool + assignment_pipeline
- youtube_player
- test_protocol
- bindings
- compiler
- README
- README
- __init__
- README
- voice
- resume_router + tools
- PROMPT_TEMPLATE
- numpy
- FEATURES
- voice
- resume_builder
- compiler
- recolor
- dark_enhancement.py
- main
- voice_agent
- refresh_docs
- dump_wa_ui + test_wa
- ppt_studio
- schema
- voice + hinglish_normalizer
- edge_tts
- pygame
- browser_mail
- ppt_designer
- whatsapp_call
- youtube_control
- chat-routing + chat
- .process_chunk
- neural-cache
- ChatMessage.jsx
- voice_agent
- plate
- chat
- schema
- test_lru
- ssml_processor
- voice
- assignment_assembler + smart_navigator
- youtube_player
- voice_agent
- test_lru
- youtube_control
- plate
- research_scraper + nlp_extractor
- media-enhancement
- compiler
- CODEMAP
- ControlPanel.jsx
- test_lru
- compiler
- test_lru
- App
- schema
- test_lru
- lru
- schema
- schema
- benchmark + download_kokoro
- KNOWN_ISSUES
- whatsapp

## God Nodes (most connected - your core abstractions)
1. `Tool registry` - 123 edges
2. `chat_endpoint()` - 51 edges
3. `DeckRenderer` - 49 edges
4. `Key pieces` - 49 edges
5. `text()` - 41 edges
6. `create()` - 34 edges
7. `2. Tool Registry (`tools.py`)` - 34 edges
8. `box()` - 32 edges
9. `PresentationBuilder` - 32 edges
10. `create_resume()` - 31 edges

## Surprising Connections (you probably didn't know these)
- `Adding a tool (checklist)` --references--> `keyword_detect_tool()`  [INFERRED]
  docs/features/tool-registry.md → app/api/chat.py
- `Gotchas` --references--> `recall_memory()`  [INFERRED]
  docs/features/memory.md → app/api/memory.py
- `Calendar` --references--> `check_today_schedule()`  [INFERRED]
  docs/features/email-calendar.md → app/services/calendar_tool.py
- `Gotchas` --references--> `is_complex_task()`  [INFERRED]
  docs/features/frontend.md → app/services/planner.py
- `Entry points` --references--> `PresentationBuilder`  [INFERRED]
  docs/features/ppt.md → app/services/ppt_tool.py

## Import Cycles
- None detected.

## Communities (176 total, 21 thin omitted)

### Community 0 - "tools"
Cohesion: 0.03
Nodes (103): list_skills(), List all saved skill descriptions., Store a user preference (e.g. key='browser', value='Chrome')., save_preference(), ppt_styles(), append_to_file(), build_style_profile(), cache_get() (+95 more)

### Community 1 - "planner + dynamic_skill"
Cohesion: 0.08
Nodes (40): clear_history(), delete, Clears the conversation history (start fresh)., app_memory, find_skill(), Persist a successful dynamic skill for future reuse., Returns up to n most relevant saved skills for a given task description. Each…, save_skill() (+32 more)

### Community 2 - "analyzer"
Cohesion: 0.08
Nodes (61): _file_hash(), _gemini(), _groq(), _hex(), _llm_json(), _measure_band(), near(), _measure_frame() (+53 more)

### Community 3 - "plate"
Cohesion: 0.09
Nodes (42): contact_type(), _hex(), background_mask(), _bg_model(), _bgr(), build(), comps_in(), _chip_gap() (+34 more)

### Community 4 - "ppt_chart_engine"
Cohesion: 0.12
Nodes (34): _bg_color(), _extract_strict_metric(), _fig_to_bytes(), _hex(), _metrics_to_bar(), _palette_colors(), ppt_chart_engine.py — Dynamic Data-Visualization Engine for JARVIS PPT…, Horizontal or vertical bar chart. (+26 more)

### Community 5 - "content_humanizer.py"
Cohesion: 0.17
Nodes (21): build_structure_prompt(), build_vocab_prompt(), call_groq(), check_similarity(), detect_tone(), fact_check(), get_groq_client(), get_sentence_scores() (+13 more)

### Community 6 - "window_layout"
Cohesion: 0.08
Nodes (38): close_specific_window(), close_tab(), minimize_window(), Closes the current browser tab using Ctrl+W, targeting the real foreground app., Closes a specific window/app by name using Win32 PostMessage WM_CLOSE., Minimizes a specific window by name using Win32 ShowWindow., Block until a window with the given name appears, then focus it., wait_for_window() (+30 more)

### Community 7 - "resume_builder + resume-exact-replica"
Cohesion: 0.06
Nodes (41): _analyse_design(), _apply_layout_answer(), _balance_columns(), _closest_preset(), _crop_photo(), _faces(), _grow_photo_box(), _image_b64() (+33 more)

### Community 8 - "youtube_control"
Cohesion: 0.11
Nodes (37): _media_intent_for(), Media tool intent for one clause (YouTube-mode parser first, then keyword…, _end_session(), _fetch_results(), _format_results(), _initial_data(), _load(), _mark_last() (+29 more)

### Community 9 - "syllabus_auditor"
Cohesion: 0.07
Nodes (41): _approx_token_count(), _assemble_response(), audit_playlist_syllabus(), _build_vector_store(), _chunk_transcript(), _coverage_level(), _embed_texts(), _extract_playlist_id() (+33 more)

### Community 10 - "ppt_studio + ppt_designer"
Cohesion: 0.09
Nodes (43): Separate the user's command, any pasted/attached content and attachment paths., split_request(), _finish_theme(), _lum(), Convert a legacy ppt_tool palette (bg/card/text/sub/ac1..) into a theme., choice may be a THEMES key, a legacy palette key, a palette dict, or None…, resolve_theme(), theme_from_palette() (+35 more)

### Community 11 - "ppt_designer"
Cohesion: 0.15
Nodes (21): _compact_header(), box(), DeckRenderer, fit_size(), _items(), para_h(), Header + lead + list inside a column. Returns nothing., Portrait/square image as a full-height panel flush to one edge. (+13 more)

### Community 12 - "browser_tool"
Cohesion: 0.14
Nodes (27): browse_and_paginate(), browse_and_read(), _clean_text(), click_element(), _ensure_url(), fill_form(), _llm_extract(), _new_browser_page() (+19 more)

### Community 13 - "lru"
Cohesion: 0.18
Nodes (8): LRUCache, Insert or update a key-value pair. - If key already exists: update value + TTL,…, Remove a key from the cache. Returns True if the key existed, False if it was…, Place node at the MRU (most-recently-used) end of the list., Remove node from its current position in the list (O(1) because doubly-linked)., Evict a specific node (unlink + remove from map)., O(1) Least-Recently-Used cache backed by: - dict[str, Node] — hash map for O(1)…, Return the value for key, or None on miss / expiry. On hit: moves node to the…

### Community 14 - "file_ops"
Cohesion: 0.11
Nodes (26): append_file(), bulk_rename(), create_folder(), delete_file(), diff_files(), _fmt_size(), list_directory(), _maybe_summarize() (+18 more)

### Community 15 - "ppt_tool"
Cohesion: 0.18
Nodes (19): _clean_image_path(), _get_image_aspect_ratio(), _oval(), _parse_bullet(), _parse_card(), PresentationBuilder, _frame(), Render a single image with CONTAIN-FIT (object-fit: contain). The image is… (+11 more)

### Community 16 - "assignment_answers"
Cohesion: 0.12
Nodes (25): _ask_question_on_page(), _find_input(), generate_answer(), generate_answers(), _get_persistent_page(), _groq_answer(), Jarvis Assignment Tool — Phase 2: Answer Generation…, Launch a visible (non-headless) Chromium with a persistent profile. Login… (+17 more)

### Community 17 - "resume_builder"
Cohesion: 0.06
Nodes (76): _apply_color(), _clean_free(), _competencies_html(), _contact_html(), _contrast(), _css(), _css_extra(), _css_val() (+68 more)

### Community 18 - "fontmatch + fonts"
Cohesion: 0.10
Nodes (22): all_faces(), FontMatcher, identify(), fontmatch.py — Font identification against the local library (fonts.py), all in…, One warm Chromium page with the whole font library loaded. Use as a context…, samples: [{text, ref, rw, rh, src_h}] (see ref_map). Returns per sample a…, items: [{text, family, weight, ls}] → font/ink metrics in em (for the CSS half-…, Runs in a separate process: jobs = [(sample, candidates, top_k)] → result lists. (+14 more)

### Community 19 - "prompt_enhancer_button"
Cohesion: 0.07
Nodes (41): _acquire_single_instance(), _app_title_match(), _box_contains(), _box_set_value(), _browser_url(), classify_app(), _exe_name(), _focused_text() (+33 more)

### Community 20 - "engine + test_protocol"
Cohesion: 0.15
Nodes (13): CacheEngine, Any, Route a command dict to the appropriate handler. All handlers return a response…, Owns the LRUCache. Runs a single consumer loop on a dedicated thread. External…, Spawn the single writer thread. Call once at server boot., Gracefully stop the engine writer thread., The single consumer loop. Runs on CacheEngineThread. Processes one command at a…, err_response() (+5 more)

### Community 21 - "ui_inspector + tools"
Cohesion: 0.10
Nodes (22): click_ui_element_uia(), dump_app_ui_tree(), Click a UI element inside an app by AutomationId, name, or control type. Does…, Inject text into a specific input field in an app via UIA Value pattern. No…, Read the current text content of a UI element — e.g. a terminal output pane, a…, Dump the full Windows UI Automation accessibility tree of an app window. Use…, Type a question into the Windows Copilot sidebar and retrieve the response.…, read_ui_element_text() (+14 more)

### Community 22 - "ppt_research"
Cohesion: 0.11
Nodes (36): ground_slides(), plan_queries(), 4-6 web queries covering the angles a deck on `topic` needs. Templates, not an…, Web + Wikipedia → verified facts. [] when offline (the deck is then written…, Audit every generated slide; LLM-repair flagged ones with their facts; scrub…, research_facts(), allowed_numbers(), _anchors() (+28 more)

### Community 23 - "ppt_template"
Cohesion: 0.06
Nodes (56): analyze_format(), _analyze_slide(), classify_box(), _clear(), clone_slide(), delete_slide(), describe_template(), _field_label() (+48 more)

### Community 24 - "chat + llm"
Cohesion: 0.11
Nodes (21): chat_endpoint(), _dag_stream_with_history(), planner_stream(), response_stream_with_history(), resume_stream(), tool_stream(), ChatRequest, detect_whatsapp_call() (+13 more)

### Community 25 - "ppt_router + ppt_tool"
Cohesion: 0.11
Nodes (24): build_ppt(), generate(), create_ppt_backend(), generate(), extract_theme(), get_styles(), PPTBuildRequest, PPTCreateRequest (+16 more)

### Community 26 - "package"
Cohesion: 0.08
Nodes (25): name, private, scripts, build, dev, lint, preview, type (+17 more)

### Community 27 - "persistence"
Cohesion: 0.10
Nodes (11): Any, Path, Flush and close the file handle cleanly on server shutdown., Serialise cache state to disk and truncate the WAL. Called by CacheEngine on…, Load the snapshot from disk. Returns None if no snapshot exists yet. Called…, Append-only write-ahead log. Each SET/DEL command is written as a JSON line…, Append one command to the WAL and flush immediately. Flushing on every write is…, Read and parse all commands from the WAL file. Called once at startup for… (+3 more)

### Community 28 - "storage + orchestrator"
Cohesion: 0.07
Nodes (44): resume_replica — Scene-graph-based resume replication engine. Import the public…, build_replica(), compile_replica_html(), _compute_fit_scale(), create_replica_resume(), _data_uri(), _design_with_replica(), orchestrator.py — Main pipeline for replica resume creation. The public API:… (+36 more)

### Community 29 - "ppt_image_engine"
Cohesion: 0.16
Nodes (18): build_image_descriptors(), _extract_keywords(), get_aspect_ratio(), ImageDescriptor, match_images_to_slides(), _parse_slide_ref(), _parse_slide_ref_by_title(), ppt_image_engine.py — Semantic Image-Slide Matcher for JARVIS PPT Engine… (+10 more)

### Community 30 - "task_ledger + test_task_resumption"
Cohesion: 0.11
Nodes (21): _ensure_ledger_file(), find_resumable_task(), get_recent_tasks(), get_recent_tasks_raw(), _load_ledger(), log_task(), task_ledger.py — Jarvis Task Context Ledger…, Return a formatted string of the last N tasks, suitable for display or speech.… (+13 more)

### Community 31 - "ppt_composer + ppt_designer"
Cohesion: 0.16
Nodes (38): _body_cards(), _body_fields(), _body_list(), _body_paragraph(), _body_stats(), _body_steps(), _body_table(), _cols_for() (+30 more)

### Community 32 - "dsa_enforcer + dsa-mode"
Cohesion: 0.11
Nodes (17): _cache_del(), _cache_set(), DSAEnforcer, get_dsa_enforcer(), Write to Neural Cache, silently skipping if unavailable., Delete from Neural Cache, silently skipping if unavailable., Data, DSA / LeetCode enforcer mode (+9 more)

### Community 33 - "ppt_content"
Cohesion: 0.09
Nodes (39): apply_edit(), apply_structure(), _as_dated(), _as_stat(), _clauses(), _compact(), _edit_facts(), finalize_slides() (+31 more)

### Community 34 - "server + persistence"
Cohesion: 0.08
Nodes (28): logging, neural_cache, client.py — Python Client Library for Neural Cache (Milestone 5)…, engine.py — Single-Writer Command Queue (Milestone 3)…, Queue, persistence.py — WAL + Snapshot for Neural Cache (Milestone 6)…, Manages periodic full-state snapshots. The snapshot itself is triggered through…, Start a daemon thread that enqueues a SNAPSHOT command every interval_seconds.… (+20 more)

### Community 35 - "prompt_overlay"
Cohesion: 0.14
Nodes (3): main(), PromptOverlay, Strip the **ENHANCED PROMPT (CODING):** header if present.

### Community 36 - "ui_inspector"
Cohesion: 0.10
Nodes (11): Walk all descendants looking for any control whose window_text contains `text`…, Fire an element's primary action via UIA Invoke pattern. No mouse movement —…, Inject text into an input element via UIA Value pattern. No simulated…, Read text from an element via UIA TextPattern or window_text. Returns empty…, Walk the accessibility tree and return all elements up to `depth` levels. Use…, Core wrapper around pywinauto's UIA backend. All interactions go through the OS…, Get a window wrapper by partial title match (regex-safe). Returns None if not…, Get the currently focused window via Win32 HWND matching. (+3 more)

### Community 37 - "agentic_web"
Cohesion: 0.12
Nodes (18): agentic_web_action(), _worker(), _build_search_queries(), _fetch_page_text(), __init__(), _get_api_key(), agentic_web.py — Smart Web Research Engine for Jarvis…, Download a page and return clean readable text (no HTML tags). (+10 more)

### Community 38 - "exact_render"
Cohesion: 0.06
Nodes (66): _e(), _f(), Escaped text; in editor mode an editable span carrying the content JSON path it…, _abs_text(), _bar_grid_html(), _bg_grid(), canon_title(), _chips_html() (+58 more)

### Community 39 - "pipeline"
Cohesion: 0.10
Nodes (29): _core_norm(), ndarray, Scale so the stroke cores read 1.0 (same rule as the JS side: mean of values…, Reference intensity map (0 = background, 1 = text colour) of a line's ink box…, ref_map(), run(), _align(), analyse_reference() (+21 more)

### Community 40 - "memory"
Cohesion: 0.21
Nodes (10): format_preferences_for_prompt(), get_all_preferences(), Jarvis Vector Memory — ChromaDB-based long-term memory engine. Stores and…, Returns a string suitable for injecting into LLM prompts., Stable short ID based on content hash., Return all stored preferences as a plain dict., _uid(), chromadb (+2 more)

### Community 42 - "resume_builder"
Cohesion: 0.07
Nodes (49): _apply_op(), _attachments(), create_resume(), detect_resume_request(), editor_page(), editor_save(), undo_id(), _editor_toolbar() (+41 more)

### Community 43 - "air-drawing + air_drawing_tool"
Cohesion: 0.18
Nodes (9): open_air_drawing(), Opens the Air Drawing Canvas on the screen. This feature allows the user to…, Air drawing (webcam hand drawing), Files & symbols (auto-generated, line numbers are current), Flow, Gotchas, Graphify, Purpose (+1 more)

### Community 44 - "ppt_designer"
Cohesion: 0.08
Nodes (30): _best_window(), count_lines(), E(), gradient_box(), _line_factor(), line_shape(), _pil_font(), place_image() (+22 more)

### Community 45 - "voice"
Cohesion: 0.11
Nodes (19): Clip, _get_groq(), _groq_once(), prewarm(), voice.py — Jarvis Voice Engine ------------------------------ STT Groq whisper-…, Translate one reply sentence into the user's language (canned tool/flow replies…, PCM (int16, 24 kHz) that fills while synthesis streams; playable immediately., hi' → Hindi voice, 'en' → English voice, for one sentence. (+11 more)

### Community 46 - "App.jsx"
Cohesion: 0.14
Nodes (17): Composer(), container, EmptyState(), greeting(), item, MemoryPanel(), Orb(), Sidebar() (+9 more)

### Community 47 - "AcousticWakeEngine"
Cohesion: 0.09
Nodes (16): AcousticWakeEngine, _generate_chime(), ndarray, Background thread that watches the microphone for a double-clap pattern. Usage…, Start the background listening thread., Signal the background thread to exit and wait for it., Resume detection after a disable()., Pause detection without stopping the thread (fast resume). (+8 more)

### Community 48 - "ppt_composer + ppt_designer"
Cohesion: 0.11
Nodes (25): _balanced_rows(), _fill(), image_block(), _image_panel(), _masonry(), Split items into rows with at most one item difference (5 in 3 cols → 3+2, 7 →…, How much extra height a section can absorb before it looks inflated., Framed images (no crop) + numbered captions under each. Returns used height. (+17 more)

### Community 49 - "resume_builder"
Cohesion: 0.17
Nodes (16): Pasted resumes often lose their line breaks, gluing a heading to the next word…, (position, section key) of every heading line marked in the person's text., The exact source text of v (case, dashes, quotes and spacing may differ), or…, The person's own pieces of text: lines/bullets/cells (coarse) and their…, The resume shows the person's own words only. Every sentence-like field is…, _region_keys(), _segments(), _src_span() (+8 more)

### Community 50 - "client + test_concurrency"
Cohesion: 0.07
Nodes (22): Send one of the reply drafts generated by generate_reply_draft. draft_index is…, send_style_reply(), CacheClient, Any, Store a key-value pair, optionally with a TTL. Args: key: Cache key. value:…, Delete a key from the cache. Returns: True if the key existed and was deleted,…, Retrieve server statistics (hit rate, evictions, cache size, etc.). Returns…, Explicitly close the socket connection. (+14 more)

### Community 52 - "calendar_tool"
Cohesion: 0.27
Nodes (9): add_event(), check_today_schedule(), _get_calendar_service(), get_upcoming_events(), calendar_tool.py — Jarvis Google Calendar Integration (Step 8)…, Create a new event in Google Calendar. - title: "Project Meeting" - date:…, Authenticate and return a Google Calendar API service object., List events in the next N days. (+1 more)

### Community 53 - "package"
Cohesion: 0.14
Nodes (14): devDependencies, autoprefixer, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, postcss (+6 more)

### Community 55 - "voice"
Cohesion: 0.11
Nodes (15): get_player(), _load_whisper_model(), preload_local_stt(), _load(), Load the local Whisper models in the background (voice agent startup)., Feed streamed tokens; get back speakable sentences as early as possible., Speak a complete text. All sentences synthesise in parallel, play in order., Speak an async generator of text chunks, sentence by sentence, pipelined. (+7 more)

### Community 56 - "llm + llm-personality"
Cohesion: 0.07
Nodes (46): classify_context(), detect_language(), context_classifier.py — Jarvis Situational Awareness…, Detect whether the user spoke English, Hinglish, or Hindi. Returns: 'english' —…, Classify the situation from user input. Returns a dict with keys: urgency :…, check_for_tool_intent(), generate_chat_response(), _groq_generate() (+38 more)

### Community 57 - "prompt_enhancement_library + skill_prompt_enhancer"
Cohesion: 0.12
Nodes (26): check_for_hallucination(), clean_output(), detect_domain(), is_bloated(), protect_blocks(), prompt_enhancement_library.py…, Replace ``` fenced blocks with [[BLOCK_n]] placeholders., Put protected blocks back; append any the model dropped. (+18 more)

### Community 58 - "dark_video_enhancement.py"
Cohesion: 0.26
Nodes (12): get_all_enhancements(), ndarray, run_pipeline_a(), _enhance_frame(), _get_ffmpeg_binary(), process_video_smartly(), Re-encode a video to H.264 MP4 so browsers can play it., _reencode_to_h264() (+4 more)

### Community 59 - "web_search + tools"
Cohesion: 0.09
Nodes (32): research_scraper.py — Autonomous Web Research Scraper…, _extract_location(), get_info(), get_weather(), Pulls a clean location name out of a weather query., Get current weather using wttr.in — returns a clean spoken string., Search for a query within a specific website using DuckDuckGo site: operator., Read and extract readable text content from a specific URL. (+24 more)

### Community 60 - "safe_executor"
Cohesion: 0.14
Nodes (15): Exception, Safe Code Executor for Jarvis ------------------------------- Runs LLM-…, Restricted open(): blocks writes to system paths., Restricted __import__: blocks dangerous modules., Raised when generated code violates safety constraints., AST visitor that inspects generated code before execution., Parse and walk the AST, raising SecurityError on violations., _safe_import() (+7 more)

### Community 61 - "lru"
Cohesion: 0.18
Nodes (6): Node, Restore cache state from a snapshot dict (produced by snapshot()). Called once…, Place node at the LRU (least-recently-used) end of the list., A doubly-linked list node holding one cache entry. Attributes: key (str): Cache…, Evict the LRU entry (the node just before the tail sentinel). Returns the…, Return True if this entry has a TTL and it has elapsed.

### Community 62 - "youtube_control + os-control"
Cohesion: 0.12
Nodes (16): _channel_name(), _is_positional(), _last_media(), _latest_of(), parse_youtube_followup(), A pick by position, not by title: 'the first result', 'number 3', 'the latest…, play mrbeast's latest video' / 'play the latest video of t series' → channel…, Channel name from a request like 'open MrBeast's channel', else None. (+8 more)

### Community 63 - "ppt"
Cohesion: 0.33
Nodes (5): Entry points, Files & symbols (auto-generated, line numbers are current), Graphify, PowerPoint generator, Purpose

### Community 64 - "whatsapp_smart + tools"
Cohesion: 0.07
Nodes (39): Resolve a verbal site name like 'unstop' to a URL like 'https://unstop.com'., Resolves site name, opens a VISIBLE browser, and performs a search or action…, _resolve_url(), smart_web_action(), close_window(), get_system_time(), Returns current date and time naturally., Snaps left_app to left half and right_app to right half using Win32 API (no… (+31 more)

### Community 65 - "Architecture"
Cohesion: 0.13
Nodes (12): Architecture, Frontend (`frontend/src`), HTTP endpoints, LLM usage, Memory layers (five separate stores), Processes, Files & symbols (auto-generated, line numbers are current), Gotchas (+4 more)

### Community 67 - "ppt_content"
Cohesion: 0.11
Nodes (28): architect_slides(), ask(), _retry(), run(), _complete_from_source(), deck_facts(), detect_profile(), extractive_ok() (+20 more)

### Community 68 - "spotify_service + media_sessions"
Cohesion: 0.06
Nodes (55): app_kind(), control(), run(), _do(), _filter(), kind_playing(), _label(), media_command() (+47 more)

### Community 69 - "prompt_enhancer_button"
Cohesion: 0.10
Nodes (11): _clip_get(), _clip_set(), _ctrl(), EnhanceButton, _focus(), _load_state(), Visible frame bounds (excludes the invisible resize border)., Move (and optionally show) without ever activating the window; Tk's deiconify()… (+3 more)

### Community 70 - "rag_memory + memory"
Cohesion: 0.06
Nodes (57): aiomysql, forget_memory(), ForgetRequest, get_history(), ingest_memory(), IngestRequest, memory_stats(), BaseModel (+49 more)

### Community 72 - "jarvis_overlay"
Cohesion: 0.19
Nodes (6): Image, generate_arc_reactor(), JarvisOverlay, Jarvis Arc Reactor Overlay -------------------------- A floating, always-on-…, Draws a beautiful arc reactor using PIL when no icon file is found., read_state()

### Community 73 - "test_lru"
Cohesion: 0.20
Nodes (5): Accessing 'a' should move it to MRU and save it from eviction., Re-setting an existing key should move it to MRU., len(cache.map) must never exceed capacity., Fill to capacity+1. The first key inserted (LRU) should be evicted., TestEviction

### Community 74 - "voice"
Cohesion: 0.16
Nodes (9): hinglish_to_devanagari(), Rewrite the Hindi words of a romanized Hinglish sentence in Devanagari, leaving…, _norm_words(), Plays sentences from many Channels without overlap: - urgent phrases (acks,…, Barge-in "stop": silence now and drop everything queued., Next (channel, text, lang) or None. Non-blocking., Speaker, TTS (`voice.Speaker`, `start_clip`, `_Player`) (+1 more)

### Community 75 - "assignment_humanizer"
Cohesion: 0.12
Nodes (25): _extract_output_text(), _fill_input(), _find_element(), _get_browser_page(), humanize_all_answers(), _humanize_chunk_via_browser(), humanize_text(), _humanize_via_browser() (+17 more)

### Community 76 - "agents + tool_runner"
Cohesion: 0.16
Nodes (12): format_recall_for_prompt(), Format recalled memory turns into an injectable LLM context block with clear…, _call_sync(), tool_runner.py — Async execution of TOOL_REGISTRY entries for orchestrators…, Run a registry tool and return its output as a string. Raises on unknown tool…, run_tool(), Agents: DAG executor, linear planner, dynamic skills, Data (+4 more)

### Community 77 - "uia_local"
Cohesion: 0.11
Nodes (6): Element, focused_element(), uia_local.py — thread-safe UI Automation access (helper, not a tool)…, Minimal pywinauto-style wrapper around an IUIAutomationElement., Rect, ctypes

### Community 78 - "VoiceAgent"
Cohesion: 0.23
Nodes (4): _pick(), Was Jarvis talking (or just finished) during [t0, t1]?, VoiceAgent, filler()

### Community 79 - "gmail_tool + memory_tool"
Cohesion: 0.06
Nodes (50): check_emails(), _decode_body(), _format_date(), get_email_body(), _get_gmail_service(), _get_header(), list_unread(), gmail_tool.py — Jarvis Gmail Integration (Step 5)… (+42 more)

### Community 80 - "package"
Cohesion: 0.22
Nodes (9): dependencies, framer-motion, lucide-react, react, react-dom, react-markdown, react-syntax-highlighter, remark-gfm (+1 more)

### Community 81 - "Content humanizer & social content"
Cohesion: 0.15
Nodes (13): build_prompt(), call_llm(), generate_social_content(), Refine an existing piece of social media content based on user instructions.…, Calls Groq Llama 3.3 70B directly for maximum speed. No slow fallbacks., Generate professional, multi-version social media content., refine_social_content(), Content humanizer & social content (+5 more)

### Community 82 - "dag_executor"
Cohesion: 0.13
Nodes (25): detect_note_intent(), _semantic_window_adjust(), _call_dag_planner(), DAGNode, _execute_node(), is_dag_task(), dag_executor.py — Jarvis DAG-Based Multi-Step Agent Planner…, Ask the LLM to produce a DAG plan. Returns parsed dict. (+17 more)

### Community 83 - "screen_vision + screen_reader"
Cohesion: 0.05
Nodes (60): _accessibility_tree(), describe_screen_for_llm(), get_screen_screenshot_b64(), _groq_vision_screen(), _init_tesseract(), _ocr_screen(), screen_reader.py — Jarvis Screen Vision (VLM-first architecture)…, Legacy OCR layer. Works on any app but extracts raw text only — no layout,… (+52 more)

### Community 84 - "repair"
Cohesion: 0.20
Nodes (6): apply_diff_patches(), _patch_fill(), Converts VLM diffs into structured patches and applies them to the replica_doc.…, Finds the frame with the given ID in the scene graph and updates its fill.…, make_linear_fill(), stops = [{"offset_pct": 0, "color": "#hex"}, {"offset_pct": 100, "color":…

### Community 85 - "hinglish_normalizer + voice"
Cohesion: 0.16
Nodes (13): devanagari_to_hinglish(), _sub(), loanword_ratio(), hinglish_normalizer.py — Devanagari Crash Prevention + Text Normalizer…, One Devanagari word → casual Hinglish roman ("चलाओ" → "chalao", "करना" →…, Share of Devanagari words that are English loanwords ("ओपन क्रोम" → 1.0). High…, Romanize a Devanagari (Hindi) transcript for the backend, keeping any Latin…, _translit_dev_word() (+5 more)

### Community 86 - "AirDrawingApp.jsx"
Cohesion: 0.10
Nodes (13): frontend_src_airdrawing_airdrawing, CameraView(), FINGERTIP_INDICES, HAND_CONNECTIONS, HandSkeleton(), gestures, HelpPanel(), GestureController (+5 more)

### Community 88 - "ppt_chart_engine"
Cohesion: 0.33
Nodes (3): ChartEngine, Stateless chart renderer. All colors are derived from the active PPT palette —…, Render a chart from structured data. Args: chart_data: {"type": "bar",…

### Community 89 - "compiler"
Cohesion: 0.13
Nodes (17): _commands_to_d(), _compile_document_css(), _compile_path(), _fill_to_css_background(), _fill_to_svg_fill(), _mm_to_pt(), _parametric_to_commands(), _pt_to_mm() (+9 more)

### Community 90 - "ingest"
Cohesion: 0.26
Nodes (12): _imread(), load_reference(), ndarray, ingest.py — Reference file → clean page image at a fixed working resolution. *…, Returns {img (BGR, page width = 210 mm at PX_PER_MM), page_h_mm, src_dpi,…, Grey/dark colours typical of a viewer background (a white or tinted border is…, Trims uniform viewer-coloured borders. Returns x0, y0, x1, y1., Phone screenshots carry app overlays on top of the page: Google Lens' dark… (+4 more)

### Community 91 - "measure"
Cohesion: 0.14
Nodes (22): analyse(), _cdist(), _h_overlap(), _is_upper(), _item_roles(), _letters(), measure_line(), ndarray (+14 more)

### Community 92 - "ppt_content"
Cohesion: 0.11
Nodes (24): _budget_left(), _content_prompt(), _flatten(), _gemini_json(), generate_deck(), _is_note(), run(), take() (+16 more)

### Community 94 - "tool-registry + vector_store"
Cohesion: 0.09
Nodes (25): _media_target(), Which player an ambiguous media command ("pause it", "next song") is for: named…, post, Semantic search over all stored conversation turns. Returns the most relevant…, recall_memory(), get_db_pool(), init_db(), True if the Spotify desktop app has a window (cheap: EnumWindows, no UIA). (+17 more)

### Community 95 - "voice_agent.py"
Cohesion: 0.12
Nodes (16): app_services, difflib, httpx, pyaudio, random, _clean_agentic_line(), extract_wake_word_command(), _is_stop() (+8 more)

### Community 96 - "schema + bindings"
Cohesion: 0.22
Nodes (7): build_editor_path_map(), Walks the scene graph and builds a map from binding path -> list of node IDs…, collect_bindings(), Depth-first traversal of the scene graph. visitor(node, parent, depth) is…, Returns all unique binding paths referenced in the scene graph. E.g. ["name",…, walk_nodes(), _walk()

### Community 97 - "youtube_player"
Cohesion: 0.11
Nodes (44): element_from_handle(), This thread's IUIAutomation (COM initialised for the thread on first use)., uia(), _get_process_name(), Get the executable name of the process owning this HWND., _address_bar_focused(), _address_bar_value(), _clip_get() (+36 more)

### Community 98 - "compiler"
Cohesion: 0.50
Nodes (4): Renders a single ring/donut chart SVG for a skill., Ring/donut chart skills (up to 9, max 3 per row)., _render_rings(), _ring_svg()

### Community 99 - "compiler"
Cohesion: 0.13
Nodes (21): _compile_frame(), _compile_group(), _compile_image(), _compile_node(), compile_replica_html(), _compile_rule(), _compile_text(), _e() (+13 more)

### Community 100 - "resume_campus + measure"
Cohesion: 0.18
Nodes (11): detect(), resume_campus.py — campus / placement-cell resume format (renderer helper of…, Design overrides if the image is a campus-format resume (education table header…, render(), _uri(), _get_ocr(), _merge_spaced(), ocr_lines() (+3 more)

### Community 101 - "resume_detector"
Cohesion: 0.15
Nodes (16): detect_resume_intent(), _extract_task_resource(), _find_best_task_match(), get_resume_context_string(), _has_continuation_verb(), _has_fresh_task_indicator(), _has_reference_phrase(), resume_detector.py — Jarvis Resume Intent Classifier… (+8 more)

### Community 102 - "repair"
Cohesion: 0.19
Nodes (12): compute_visual_diff(), _images_to_base64_pair(), _parse_diff_json(), repair.py — Visual diff and bounded repair loop. Runs after an initial render…, Sends both images to the VLM and asks it to describe differences. Returns a…, Runs the bounded repair loop: 1. Compare rendered PNG against reference image…, Loads two images, downscales if needed, and returns (b64_1, b64_2, mime). Uses…, Computes a quality score from a diff list. high severity = -3 points, medium =… (+4 more)

### Community 103 - "schema"
Cohesion: 0.09
Nodes (21): make_chart_node(), make_group_node(), make_parametric_geometry(), make_radial_fill(), make_repeat_node(), make_ring_spec(), make_rule_node(), make_text_node() (+13 more)

### Community 104 - "modes"
Cohesion: 0.26
Nodes (13): Modes (`src/modes.js`, like Gemini's Deep Research / Image modes), buildRequest(), fwd(), isPPTEdit(), isPPTRequest(), isResumeRequest(), pick(), PPT_KW (+5 more)

### Community 105 - "style_profiler + reply_generator"
Cohesion: 0.04
Nodes (78): _bring_whatsapp_to_front(), _get_whatsapp_window(), _heuristic_parse_ocr_lines(), _parse_uia_message_string(), message_reader.py — Jarvis WhatsApp Intelligence: Message Reader…, Restores and focuses WhatsApp window. Returns True on success., Walks the WhatsApp UIA accessibility tree to extract messages. WhatsApp Desktop…, Parses a raw UIA ListItem Name string into a structured message dict.… (+70 more)

### Community 106 - "ppt_tool"
Cohesion: 0.08
Nodes (30): _auto_select_image_layout(), _bg_fill(), _c(), compute_split_geometry(), _corner_L(), _detect_purpose(), extract_theme_from_image(), _extract_theme_pil_local() (+22 more)

### Community 107 - "assignment_tool + assignment_pipeline"
Cohesion: 0.05
Nodes (57): _browser_thread(), do_assignment(), _find_el(), _get_answer(), _get_browser_ctx(), _groq_answer(), _groq_humanize(), _humanize_browser() (+49 more)

### Community 108 - "youtube_player"
Cohesion: 0.19
Nodes (14): current_video_info(), _fallback(), fmt_span(), fmt_time(), _js(), player_action(), _pos(), _rate() (+6 more)

### Community 109 - "test_protocol"
Cohesion: 0.09
Nodes (23): decode_message(), encode_message(), Serialise a dict to the wire format: [4-byte length][UTF-8 JSON body] Args:…, Read exactly one message from a socket, handling partial TCP reads correctly.…, Loop until exactly n bytes have been read from sock. This is necessary because…, _recv_exact(), make_fake_socket(), fake_recv() (+15 more)

### Community 110 - "bindings"
Cohesion: 0.20
Nodes (9): format_binding_value(), iter_content_items(), bindings.py — Content binding resolution and editor path mapping. Binding paths…, Iterator for repeat bindings. Yields (index, item) for each item in the list at…, Returns the display title for a section, checking content['section_titles']…, Resolves a binding path against content dict. Returns the value at that path,…, Converts a resolved binding value to a display string. - None / empty string /…, resolve_binding() (+1 more)

### Community 111 - "compiler"
Cohesion: 0.16
Nodes (23): _compile_repeat(), _compile_section(), _ef(), _it(), Simple <ul><li> list of skill names., Renders a single experience entry (same format as legacy builder's…, Renders a single education entry., Renders a single project entry (same format as legacy builder's _projects_html). (+15 more)

### Community 112 - "README"
Cohesion: 0.50
Nodes (3): Expanding the ESLint configuration, React Compiler, React + Vite

### Community 113 - "README"
Cohesion: 0.20
Nodes (9): Architecture, Benchmark, Files, LRU Cache Design, Neural Cache, Persistence, Running, Tests (+1 more)

### Community 119 - "voice"
Cohesion: 0.24
Nodes (11): groq_stt_available(), pcm_to_wav_bytes(), ndarray, Returns (text, 'en'|'hi', logprob, no_speech). Raises on network/API failure., Transcribe one VAD-segmented utterance (int16 mono 16 kHz). prefer_local=True…, Back-compat: transcribe a WAV file path → romanized text ('' on failure)., transcribe_audio(), _transcribe_groq() (+3 more)

### Community 120 - "resume_router + tools"
Cohesion: 0.15
Nodes (12): get, post, resume_router.py — FastAPI router for the visual resume editor…, resume_editor(), resume_save(), execute_tool(), BaseModel, post (+4 more)

### Community 122 - "numpy"
Cohesion: 0.22
Nodes (7): calibrate_tripwire(), get_wake_event(), acoustic_tripwire.py — Jarvis Acoustic Wake Engine…, Return the threading.Event that the engine sets on a double-clap., Sample ambient noise for `sample_seconds`, calculate the mean RMS, then set…, Event, numpy

### Community 124 - "voice"
Cohesion: 0.21
Nodes (4): _Player, One persistent 24 kHz output stream driven by a callback that pulls from a…, Loudest output RMS in the last `window` s — the voice agent's echo reference., Play a clip as it arrives. Returns False if interrupted.

### Community 125 - "resume_builder"
Cohesion: 0.07
Nodes (41): _apply_layout_hint(), _build_content(), _condense_content(), _content_brief(), _custom_sections(), _design_slots(), _drop_invented(), clean_text() (+33 more)

### Community 126 - "compiler"
Cohesion: 0.18
Nodes (9): _compile_chart(), Radar/spider chart as inline SVG. 100x100 viewBox, center (50,50), max radius…, Tags where size/opacity indicates level (higher → larger/more saturated)., Compiles a CHART node to the appropriate skill/language visualisation., 3-circle Venn diagram using the first 3 skills., _render_dots(), _render_radar(), _render_tag_level() (+1 more)

### Community 127 - "recolor"
Cohesion: 0.32
Nodes (11): clean_pairs(), dominant(), _hex(), palette_of(), ndarray, recolor.py — "change this colour everywhere" for the raster parts of an exact…, The dominant colours over a set of images (weighted by pixels) as hex, most…, Greedy merge of the most frequent colours → [(colour, pixel count)], most used… (+3 more)

### Community 128 - "dark_enhancement.py"
Cohesion: 0.39
Nodes (7): _apply_gamma(), _fusion_and_polish(), _normalize_to_8bit(), _path_1_retinex(), _path_2_wavelet(), run_pipeline_b(), pywt

### Community 129 - "main"
Cohesion: 0.09
Nodes (31): get_alerts(), _on_screen_alert(), get, post, Stop watcher, acoustic tripwire, and close DB pool cleanly on server shutdown., Frontend polls this endpoint to receive proactive JARVIS screen alerts. e.g.…, Return current acoustic tripwire state for the frontend toggle., Arm the acoustic tripwire so double-claps wake Jarvis. (+23 more)

### Community 130 - "voice_agent"
Cohesion: 0.12
Nodes (10): AbstractEventLoop, Fixed on 2026-10-01 (voice, round 2), _ClapDetector, _EnergyVAD, ndarray, Queue, Stateful frame-by-frame Silero VAD using the ONNX model bundled with faster-…, Fallback if Silero can't load: adaptive noise floor. (+2 more)

### Community 131 - "refresh_docs"
Cohesion: 0.24
Nodes (11): collections, fnmatch, auto_block(), _js_symbols(), label_communities(), Path, _py_symbols(), refresh_docs.py — keep docs/features/*.md and the graphify graph in sync with… (+3 more)

### Community 132 - "dump_wa_ui + test_wa"
Cohesion: 0.11
Nodes (18): media_state.py — which media app the user used last (Spotify or YouTube)…, prompt_overlay.py ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Jarvis…, WhatsApp Windows Desktop App Automation Uses the native Windows app via…, find_controls(), Dump WhatsApp Desktop UI tree to find the Voice Call button name. Run this…, search_tree(), Find the Voice Call button position in WhatsApp Desktop window. Run this while…, Step 1: Open WhatsApp, go to any chat (e.g. Archit Shukla) Step 2: Hover your… (+10 more)

### Community 133 - "ppt_studio"
Cohesion: 0.33
Nodes (4): _assign_images(), Put each image on its best slide. Explicit instructions win. Mutates deck;…, Move images off slides whose layout can't show them (or has too many) onto…, _rebalance()

### Community 134 - "schema"
Cohesion: 0.25
Nodes (8): make_frame_node(), make_no_fill(), make_padding(), make_path_node(), Returns {"type": "none"}, Returns a complete FRAME node., Returns a complete PATH node., Returns {"top_mm": ..., "right_mm": ..., "bottom_mm": ..., "left_mm": ...}

### Community 135 - "voice + hinglish_normalizer"
Cohesion: 0.18
Nodes (6): normalize_for_tts(), Transform text so it's safe and natural-sounding for TTS: 1. Replace known…, Markdown → plain speakable text (keeps Devanagari). Also drops URLs and emoji., strip_markdown(), Channel, The speech stream of one command's reply.

### Community 138 - "browser_mail"
Cohesion: 0.24
Nodes (7): check_emails(), _get_api_key(), list_unread(), browser_mail.py — Standard Browser Mail Automation…, A generic tool to perform any mail task (like sending or reading) by pre-…, smart_mail_action(), webbrowser

### Community 139 - "ppt_designer"
Cohesion: 0.40
Nodes (3): _as_plain_content(), _deep_plain(), Last-resort fallback: every word of a composite slide as plain bullets (never…

### Community 140 - "whatsapp_call"
Cohesion: 0.27
Nodes (10): flow_stream(), _click_voice_call_button(), confirm_whatsapp_call(), _focus_or_open_whatsapp(), _get_whatsapp_window(), initiate_whatsapp_call(), whatsapp_call.py — Jarvis Smart WhatsApp Calling Integration (Fully Isolated)…, Focus the WhatsApp window or open it if not running. Returns True on success. (+2 more)

### Community 141 - "youtube_control"
Cohesion: 0.20
Nodes (11): _dur_to_sec(), _parse_videos(), add(), walk(), Collect videos from ytInitialData: classic videoRenderer (search) and the newer…, Replace the session's result list with the videos actually on screen in the…, 1,234,567 views' / '82 million views' / '1.2M' → int., _screen_results() (+3 more)

### Community 142 - "chat-routing + chat"
Cohesion: 0.08
Nodes (21): _clean_yt_query(), keyword_detect_tool(), _named_app(), spotify' / 'youtube' if the sentence names a player, else '' (= whatever is…, Fast, 100% reliable keyword-based tool detection. Runs BEFORE the LLM router to…, Remove trailing action phrases from a YouTube search query., get_last(), Last media app used within max_age seconds, else None. (+13 more)

### Community 143 - ".process_chunk"
Cohesion: 0.40
Nodes (4): _play_chime(), Inline (shared-stream) mode — called by voice_agent.py on every audio frame it…, Play the wake chime via sounddevice (non-blocking from caller's perspective)., Voice path (`scripts/voice_agent.py`)

### Community 144 - "neural-cache"
Cohesion: 0.25
Nodes (7): Design, Files & symbols (auto-generated, line numbers are current), Graphify, Neural cache (Redis-like LRU server), Purpose, Runtime, Tests

### Community 145 - "ChatMessage.jsx"
Cohesion: 0.14
Nodes (17): Key behaviour (App.jsx), Attachments(), ChatMessage(), CodeBlock(), mdComponents, useCopy(), AttachmentChip(), DagPlanPanel() (+9 more)

### Community 146 - "voice_agent"
Cohesion: 0.33
Nodes (3): MicListener, Initial ambient noise floor (kept up to date on every non-speech frame)., One 32 ms frame → clap check + VAD state machine → events.

### Community 147 - "plate"
Cohesion: 0.14
Nodes (10): is_ornament_text(), _flat_outside(), _ornaments(), _photo_edges(), Just outside the circle the colour is flat (a ring, frame or background), not…, Colour difference just inside vs just outside a circle (high = a real frame…, Decorative runs the plate must keep: ≥ 3 identical marks (same size and shape),…, Frame of the photo: every strong colour edge along 96 rays from the face is a… (+2 more)

### Community 148 - "chat"
Cohesion: 0.25
Nodes (6): _explicit_platform(), _media_compound(), youtube' / 'spotify' if the text names one platform (song/music are neutral)., Re-target an unspecific media intent (pause/next/play X) to the given platform., "close this song and play shape of you", "pause the video then open mrbeast's…, _to_platform()

### Community 149 - "schema"
Cohesion: 0.33
Nodes (6): make_default_replica_document(), make_page_node(), make_solid_fill(), Returns {"type": "solid", "color": color}, Returns a complete PAGE node., Returns a skeleton replica document with an empty scene graph. The caller is…

### Community 151 - "ssml_processor"
Cohesion: 0.33
Nodes (5): add_human_prosody(), ssml_processor.py — Human Prosody Pre-processor…, Add natural speech prosody to plain text. Args: text: Plain text (already…, Remove all SSML tags from text — used when falling back to edge-tts which does…, strip_ssml()

### Community 152 - "voice"
Cohesion: 0.25
Nodes (7): Config (`app/core/config.py` + env), Files & symbols (auto-generated, line numbers are current), Graphify, Measured (2026-09-30/10-01, i9-13900H, no GPU), Purpose, Server-side tripwire, Voice: STT, TTS, wake word, clap wake, overlay

### Community 153 - "assignment_assembler + smart_navigator"
Cohesion: 0.13
Nodes (15): assemble_assignment(), _create_powerpoint(), _create_word_doc(), _parse_qa_json(), Jarvis Assignment Tool — Phase 4: Document Assembly…, Assemble the extracted/humanized questions and answers into a formatted…, Extract and parse the JSON array from the input string., _get_api_key() (+7 more)

### Community 154 - "youtube_player"
Cohesion: 0.33
Nodes (7): _num(), parse_clock(), parse_duration(), parse_player_command(), Map a spoken player command to (action, amount, value), or None. `t` should…, 10 minutes' → 600, '1 hour 5 min' → 3900, 'half a minute' → 30, '90 s' → 90.…, 5:30' → 330, '1:02:03' → 3723, 'to 5 30' → 330. None if absent.

### Community 155 - "voice_agent"
Cohesion: 0.40
Nodes (5): AsyncClient, POST /chat with the spoken language, speak the reply into `ch` as it streams.…, stream_chat(), on_event(), say_text()

### Community 157 - "youtube_control"
Cohesion: 0.40
Nodes (4): _find_channel(), _find_channel_at(), walk(), Best channel for a name → (title, '/@handle'), or None. Tries the 'Channels'…

### Community 158 - "plate"
Cohesion: 0.33
Nodes (6): _band_extent(), The photo's width from the flat bands that border it above and below (their run…, Rectangular photo whose frame the ray fit can't see (a translucent band across…, _straight_edges(), flat(), horizontal()

### Community 159 - "research_scraper + nlp_extractor"
Cohesion: 0.15
Nodes (8): NLPExtractor, Runs extraction on each scraped source and aggregates the results. Returns a…, Scrapes the web for a topic and extracts verified facts and statistics. Yields…, research_topic(), Searches DDG for the topic, fetches the top N links concurrently, and returns…, ResearchScraper, Phase 3: Autonomous Research Aggregator. Scrapes live facts from the web,…, _research_and_create_ppt()

### Community 160 - "media-enhancement"
Cohesion: 0.40
Nodes (4): Dark image/video enhancement, Files & symbols (auto-generated, line numbers are current), Graphify, Purpose

### Community 161 - "compiler"
Cohesion: 0.33
Nodes (6): _guess_icon(), _icon_svg(), Renders a single competency as an icon+title+description card., Returns an inline SVG icon using the _ICONS dict., Guesses an icon name from a competency title string., _render_competency_item()

### Community 162 - "CODEMAP"
Cohesion: 0.22
Nodes (8): Backend core & API, Code map, Frontend (`frontend/src`, React 19 + Vite + Tailwind 4), Ignore these (no runtime role), Neural cache (neural_cache/, see its README.md), Scripts, Services (app/services), WhatsApp intelligence (app/services/whatsapp_intelligence)

### Community 163 - "ControlPanel.jsx"
Cohesion: 0.25
Nodes (4): COLORS, ControlPanel(), FONTS, SHAPES

### Community 164 - "test_lru"
Cohesion: 0.12
Nodes (5): lru.py — Hand-rolled LRU Cache (Milestone 1)…, test_lru.py — Unit tests for neural_cache.lru (Milestone 7)…, TestSentinels, TestTTL, pathlib

### Community 165 - "compiler"
Cohesion: 0.67
Nodes (3): _collect_google_fonts(), _walk(), Scans the scene graph and style registry for font families. Returns a Google…

### Community 166 - "test_lru"
Cohesion: 0.50
Nodes (3): Return average time per (set + get) operation in microseconds., Per-op time for N=1000 vs N=100000 should be within 3x of each other. If the…, TestO1Timing

### Community 167 - "App"
Cohesion: 0.29
Nodes (7): App(), load(), save(), uid(), useSpeech(), frontend_src_index, ref_react_dom_client

### Community 168 - "schema"
Cohesion: 0.50
Nodes (4): make_image_node(), make_size(), Returns a complete IMAGE node., Returns size dict, only including non-None values.

### Community 169 - "test_lru"
Cohesion: 0.50
Nodes (4): large_cache(), fixture, LRU cache with capacity 3 — easy to reason about eviction., small_cache()

### Community 173 - "benchmark + download_kokoro"
Cohesion: 0.06
Nodes (24): Settings, nlp_extractor.py — LLM-Powered Fact & Entity Extractor…, research_pipeline.py — End-to-End Autonomous Research Orchestrator…, argparse, dotenv, glob, google_generativeai, groq (+16 more)

### Community 174 - "KNOWN_ISSUES"
Cohesion: 0.29
Nodes (6): Fixed on 2026-10-03 (resume creator), Fixed on 2026-10-03 (resume editor), Fixed on 2026-10-04 (resume creator, exact replica), Fixed on 2026-10-04, round 3 (resume creator), Fixed on 2026-10-04, round 6 (resume creator), Known issues

### Community 177 - "whatsapp"
Cohesion: 0.33
Nodes (5): Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Purpose, WhatsApp: send, call, read, reply-style cloning

## Knowledge Gaps
- **173 isolated node(s):** `Settings`, `name`, `private`, `version`, `type` (+168 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1657 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **21 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Tool registry` connect `tools` to `planner + dynamic_skill`, `window_layout`, `youtube_control`, `syllabus_auditor`, `browser_mail`, `ppt_studio + ppt_designer`, `browser_tool`, `whatsapp_call`, `chat-routing + chat`, `file_ops`, `assignment_answers`, `chat`, `ui_inspector + tools`, `chat + llm`, `ppt_router + ppt_tool`, `assignment_assembler + smart_navigator`, `task_ledger + test_task_resumption`, `agentic_web`, `resume_builder`, `air-drawing + air_drawing_tool`, `calendar_tool`, `prompt_enhancement_library + skill_prompt_enhancer`, `dark_video_enhancement.py`, `web_search + tools`, `whatsapp_smart + tools`, `spotify_service + media_sessions`, `assignment_humanizer`, `agents + tool_runner`, `gmail_tool + memory_tool`, `Content humanizer & social content`, `tool-registry + vector_store`, `assignment_tool + assignment_pipeline`?**
  _High betweenness centrality (0.075) - this node is a cross-community bridge._
- **Why does `Modes (`src/modes.js`, like Gemini's Deep Research / Image modes)` connect `modes` to `Architecture`, `ppt_studio + ppt_designer`, `agentic_web`?**
  _High betweenness centrality (0.059) - this node is a cross-community bridge._
- **Why does `ppt_edit()` connect `ppt_studio + ppt_designer` to `tools`, `ppt_tool`, `modes`, `tool-registry + vector_store`?**
  _High betweenness centrality (0.050) - this node is a cross-community bridge._
- **Are the 122 inferred relationships involving `Tool registry` (e.g. with `keyword_detect_tool()` and `_media_compound()`) actually correct?**
  _`Tool registry` has 122 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `chat_endpoint()` (e.g. with `describe_screen_for_llm()` and `get_screen_text_summary()`) actually correct?**
  _`chat_endpoint()` has 9 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Settings`, `name`, `private` to the rest of the system?**
  _173 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `tools` be split into smaller, more focused modules?**
  _Cohesion score 0.02839173405211141 - nodes in this community are weakly interconnected._