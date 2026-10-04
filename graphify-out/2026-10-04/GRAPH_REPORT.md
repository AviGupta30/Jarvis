# Graph Report - Jarvis  (2026-10-04)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 3786 nodes · 8191 edges · 168 communities (140 shown, 28 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 803 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `82115375`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- tools
- style_profiler + reply_generator
- analyzer
- plate
- ppt_chart_engine + jarvis_overlay
- dark_enhancement + dark_video_enhancement
- window_layout + tools
- engine + test_protocol
- youtube_control + youtube_player
- syllabus_auditor
- ppt_studio
- ppt_designer
- browser_tool
- lru
- file_ops
- ppt_tool
- assignment_answers
- resume_detector
- fontmatch + fonts
- prompt_enhancer_button
- ppt_content
- chat-routing + chat
- ppt_research
- ppt_template
- media_sessions + media_state
- ppt_router + ppt_tool
- package
- gestureController + gestureInterpreter
- storage + orchestrator
- ppt_image_engine
- assignment_humanizer + task_ledger
- ppt_composer + ppt_designer
- dsa_enforcer + dsa-mode
- ppt_content
- gmail_tool + memory_tool
- prompt_overlay
- ui_inspector
- agentic_web + email-calendar
- exact_render
- pipeline
- memory
- transformEngine
- resume_builder + integrate
- air-drawing + air_drawing_tool
- ppt_designer
- voice
- package + App
- acoustic_tripwire
- syllabus-auditor
- agents
- client + test_concurrency
- interactionEngine + DrawingCanvas
- calendar_tool
- package
- strokeManager
- recolor + exact_render
- llm + llm-personality
- prompt_enhancement_library + skill_prompt_enhancer
- resume_builder
- web_search + tools
- content_humanizer
- tools + ui_inspector
- voice + voice
- ppt + KNOWN_ISSUES
- whatsapp_smart + tools
- frontend
- shapeManager
- ppt_content
- spotify_service
- prompt_enhancer_button
- voice
- drawingEngine
- assignment_tool + assignment_pipeline
- test_lru
- voice
- renderer
- youtube_player
- uia_local
- server
- assignment_assembler
- package
- handTracking
- chat + youtube_control
- screen_vision + screen_reader
- youtube_player
- voice_agent
- ControlPanel + HandSkeleton
- strokeRefiner
- ppt_chart_engine
- compiler
- ingest
- measure
- repair
- nlp_extractor + research_scraper
- test_lru
- social_content_manager + content-tools
- youtube_player
- compiler
- compiler
- mysql_db + rag_memory
- ppt_composer + ppt_designer
- package
- schema
- test_lru
- message_reader + thread_extractor
- ppt_tool
- assignment_pipeline
- assignment
- test_protocol
- bindings
- compiler
- README
- test_lru
- __init__
- README
- safe_executor + refresh_docs
- README
- PROMPT_TEMPLATE
- resume_builder + resume-exact-replica
- FEATURES
- voice
- resume_builder
- compiler
- os-control
- schema
- main + screen_vision
- voice_agent
- resume_router + tools
- dag_executor + dynamic_skill
- download_kokoro
- assignment_tool
- prompt_enhancer_button
- edge_tts
- pygame
- browser_mail
- whatsapp_call
- schema
- prompt_enhancer_button
- web
- hinglish_normalizer
- neural-cache
- voice_agent
- schema
- schema
- test_lru
- memory + rag_memory
- test_lru
- schema
- lru
- smart_navigator + ssml_processor
- prompt_enhancer_button + prompt-enhancer
- schema
- assignment_tool
- schema
- voice + tools
- compiler
- CODEMAP
- schema
- compiler
- schema + bindings
- whatsapp
- persistence
- benchmark
- ppt_designer

## God Nodes (most connected - your core abstractions)
1. `Tool registry` - 123 edges
2. `chat_endpoint()` - 50 edges
3. `DeckRenderer` - 49 edges
4. `Key pieces` - 49 edges
5. `text()` - 41 edges
6. `create()` - 34 edges
7. `2. Tool Registry (`tools.py`)` - 34 edges
8. `PresentationBuilder` - 32 edges
9. `box()` - 32 edges
10. `EnhanceButton` - 29 edges

## Surprising Connections (you probably didn't know these)
- `Entry points` --references--> `PresentationBuilder`  [INFERRED]
  docs/features/ppt.md → app/services/ppt_tool.py
- `HTTP endpoints` --references--> `init_rag_memory()`  [INFERRED]
  docs/ARCHITECTURE.md → app/services/rag_memory.py
- `Tool registry` --references--> `initiate_whatsapp_call()`  [INFERRED]
  docs/TOOLS.md → app/services/whatsapp_call.py
- `Gotchas` --references--> `run_tool()`  [INFERRED]
  docs/features/agents.md → app/services/tool_runner.py
- `Gotchas` --references--> `classify_app()`  [INFERRED]
  docs/features/prompt-enhancer.md → app/services/prompt_enhancer_button.py

## Import Cycles
- None detected.

## Communities (168 total, 28 thin omitted)

### Community 0 - "tools"
Cohesion: 0.03
Nodes (86): list_skills(), List all saved skill descriptions., Store a user preference (e.g. key='browser', value='Chrome')., save_preference(), ppt_styles(), append_to_file(), cache_get(), cache_set() (+78 more)

### Community 1 - "style_profiler + reply_generator"
Cohesion: 0.06
Nodes (51): build_style_profile(), generate_reply_draft(), One-time training: parse a WhatsApp .txt chat export to build your personal…, Read the latest WhatsApp thread with a contact and generate 3 reply drafts that…, _build_system_prompt(), _build_user_prompt(), _call_groq(), generate_reply_draft() (+43 more)

### Community 2 - "analyzer"
Cohesion: 0.10
Nodes (51): _file_hash(), _gemini(), _groq(), _hex(), _llm_json(), _parse_json(), Fallback when Groq is rate-limited (its vision model has a 200k tokens/DAY cap)., _vision() (+43 more)

### Community 3 - "plate"
Cohesion: 0.09
Nodes (41): contact_type(), _hex(), background_mask(), _bg_model(), _bgr(), build(), comps_in(), _chip_gap() (+33 more)

### Community 4 - "ppt_chart_engine + jarvis_overlay"
Cohesion: 0.08
Nodes (40): _bg_color(), _extract_strict_metric(), _fig_to_bytes(), _hex(), _metrics_to_bar(), _palette_colors(), ppt_chart_engine.py — Dynamic Data-Visualization Engine for JARVIS PPT…, Horizontal or vertical bar chart. (+32 more)

### Community 5 - "dark_enhancement + dark_video_enhancement"
Cohesion: 0.13
Nodes (23): _apply_gamma(), _fusion_and_polish(), get_all_enhancements(), _normalize_to_8bit(), _path_1_retinex(), _path_2_wavelet(), ndarray, run_pipeline_a() (+15 more)

### Community 6 - "window_layout + tools"
Cohesion: 0.07
Nodes (42): close_specific_window(), close_window(), _find_window_fuzzy(), maximize_window(), minimize_window(), Closes the current active real app window (skips the Jarvis overlay)., Find a window HWND by fuzzy name matching using Win32 API (no pygetwindow)., Closes a specific window/app by name using Win32 PostMessage WM_CLOSE. (+34 more)

### Community 7 - "engine + test_protocol"
Cohesion: 0.14
Nodes (14): CacheEngine, Any, engine.py — Single-Writer Command Queue (Milestone 3)…, Route a command dict to the appropriate handler. All handlers return a response…, Owns the LRUCache. Runs a single consumer loop on a dedicated thread. External…, Spawn the single writer thread. Call once at server boot., Gracefully stop the engine writer thread., The single consumer loop. Runs on CacheEngineThread. Processes one command at a… (+6 more)

### Community 8 - "youtube_control + youtube_player"
Cohesion: 0.08
Nodes (54): _media_target(), Which player an ambiguous media command ("pause it", "next song") is for: named…, _dur_to_sec(), _end_session(), _fetch_results(), _find_channel(), _find_channel_at(), walk() (+46 more)

### Community 9 - "syllabus_auditor"
Cohesion: 0.09
Nodes (35): _approx_token_count(), _assemble_response(), audit_playlist_syllabus(), _build_vector_store(), _chunk_transcript(), _coverage_level(), _embed_texts(), _extract_playlist_id() (+27 more)

### Community 10 - "ppt_studio"
Cohesion: 0.09
Nodes (37): Separate the user's command, any pasted/attached content and attachment paths., split_request(), choice may be a THEMES key, a legacy palette key, a palette dict, or None…, resolve_theme(), _assign_images(), _caption(), _collect_attachments(), create() (+29 more)

### Community 11 - "ppt_designer"
Cohesion: 0.15
Nodes (21): _compact_header(), box(), DeckRenderer, fit_size(), _items(), para_h(), Header + lead + list inside a column. Returns nothing., Portrait/square image as a full-height panel flush to one edge. (+13 more)

### Community 12 - "browser_tool"
Cohesion: 0.20
Nodes (22): browse_and_paginate(), browse_and_read(), _clean_text(), click_element(), _ensure_url(), fill_form(), _llm_extract(), _new_browser_page() (+14 more)

### Community 13 - "lru"
Cohesion: 0.13
Nodes (12): LRUCache, Node, Insert or update a key-value pair. - If key already exists: update value + TTL,…, Remove a key from the cache. Returns True if the key existed, False if it was…, Place node at the MRU (most-recently-used) end of the list., Remove node from its current position in the list (O(1) because doubly-linked)., Evict a specific node (unlink + remove from map)., A doubly-linked list node holding one cache entry. Attributes: key (str): Cache… (+4 more)

### Community 14 - "file_ops"
Cohesion: 0.11
Nodes (26): append_file(), bulk_rename(), create_folder(), delete_file(), diff_files(), _fmt_size(), list_directory(), _maybe_summarize() (+18 more)

### Community 15 - "ppt_tool"
Cohesion: 0.18
Nodes (19): _clean_image_path(), _get_image_aspect_ratio(), _oval(), _parse_bullet(), _parse_card(), PresentationBuilder, _frame(), Render a single image with CONTAIN-FIT (object-fit: contain). The image is… (+11 more)

### Community 16 - "assignment_answers"
Cohesion: 0.11
Nodes (26): _ask_question_on_page(), _find_input(), generate_answer(), generate_answers(), _get_persistent_page(), _groq_answer(), Jarvis Assignment Tool — Phase 2: Answer Generation…, Launch a visible (non-headless) Chromium with a persistent profile. Login… (+18 more)

### Community 17 - "resume_detector"
Cohesion: 0.18
Nodes (14): detect_resume_intent(), _extract_task_resource(), _find_best_task_match(), _has_continuation_verb(), _has_fresh_task_indicator(), _has_reference_phrase(), resume_detector.py — Jarvis Resume Intent Classifier…, Return True if the text contains a strong resume-intent reference phrase. (+6 more)

### Community 18 - "fontmatch + fonts"
Cohesion: 0.08
Nodes (28): all_faces(), _core_norm(), FontMatcher, identify(), ndarray, fontmatch.py — Font identification against the local library (fonts.py), all in…, Scale so the stroke cores read 1.0 (same rule as the JS side: mean of values…, Reference intensity map (0 = background, 1 = text colour) of a line's ink box… (+20 more)

### Community 19 - "prompt_enhancer_button"
Cohesion: 0.10
Nodes (27): _acquire_single_instance(), _app_title_match(), _browser_url(), classify_app(), _exe_name(), install_autostart(), _load_state(), main() (+19 more)

### Community 20 - "ppt_content"
Cohesion: 0.10
Nodes (31): _budget_left(), _compact(), _content_prompt(), _flatten(), _gemini_json(), generate_deck(), _is_note(), run() (+23 more)

### Community 21 - "chat-routing + chat"
Cohesion: 0.08
Nodes (21): _clean_yt_query(), keyword_detect_tool(), _named_app(), spotify' / 'youtube' if the sentence names a player, else '' (= whatever is…, Fast, 100% reliable keyword-based tool detection. Runs BEFORE the LLM router to…, Remove trailing action phrases from a YouTube search query., enhance_prompt(), Enhance a prompt and return it under an **ENHANCED PROMPT (DOMAIN)** header. (+13 more)

### Community 22 - "ppt_research"
Cohesion: 0.12
Nodes (32): plan_queries(), 4-6 web queries covering the angles a deck on `topic` needs. Templates, not an…, Web + Wikipedia → verified facts. [] when offline (the deck is then written…, research_facts(), allowed_numbers(), _anchors(), audit_slide(), _clean_html() (+24 more)

### Community 23 - "ppt_template"
Cohesion: 0.06
Nodes (58): prepare_image(), Return a PPTX-safe copy (EXIF-rotated, RGB, ≤2400px, png/jpg) and its aspect., Edge-energy profile along an axis ('x' or 'y') for smart cropping., _saliency_profile(), analyze_format(), _analyze_slide(), classify_box(), _clear() (+50 more)

### Community 24 - "media_sessions + media_state"
Cohesion: 0.11
Nodes (26): app_kind(), control(), run(), _do(), _filter(), kind_playing(), _label(), media_command() (+18 more)

### Community 25 - "ppt_router + ppt_tool"
Cohesion: 0.11
Nodes (24): build_ppt(), generate(), create_ppt_backend(), generate(), extract_theme(), get_styles(), PPTBuildRequest, PPTCreateRequest (+16 more)

### Community 26 - "package"
Cohesion: 0.11
Nodes (20): name, private, type, version, autoprefixer, eslint, ref_eslint_config, @eslint/js (+12 more)

### Community 28 - "storage + orchestrator"
Cohesion: 0.09
Nodes (33): resume_replica — Scene-graph-based resume replication engine. Import the public…, build_replica(), compile_replica_html(), _compute_fit_scale(), create_replica_resume(), _data_uri(), _design_with_replica(), orchestrator.py — Main pipeline for replica resume creation. The public API:… (+25 more)

### Community 29 - "ppt_image_engine"
Cohesion: 0.16
Nodes (18): build_image_descriptors(), _extract_keywords(), get_aspect_ratio(), ImageDescriptor, match_images_to_slides(), _parse_slide_ref(), _parse_slide_ref_by_title(), ppt_image_engine.py — Semantic Image-Slide Matcher for JARVIS PPT Engine… (+10 more)

### Community 30 - "assignment_humanizer + task_ledger"
Cohesion: 0.05
Nodes (60): _extract_output_text(), _fill_input(), _find_element(), _get_browser_page(), humanize_all_answers(), _humanize_chunk_via_browser(), humanize_text(), _humanize_via_browser() (+52 more)

### Community 31 - "ppt_composer + ppt_designer"
Cohesion: 0.14
Nodes (42): _body_cards(), _body_fields(), _body_list(), _body_paragraph(), _body_stats(), _body_steps(), _body_table(), _cols_for() (+34 more)

### Community 32 - "dsa_enforcer + dsa-mode"
Cohesion: 0.11
Nodes (17): _cache_del(), _cache_set(), DSAEnforcer, get_dsa_enforcer(), Write to Neural Cache, silently skipping if unavailable., Delete from Neural Cache, silently skipping if unavailable., Data, DSA / LeetCode enforcer mode (+9 more)

### Community 33 - "ppt_content"
Cohesion: 0.10
Nodes (35): apply_edit(), apply_structure(), _as_dated(), _as_stat(), _clauses(), _edit_facts(), finalize_slides(), find_targets() (+27 more)

### Community 34 - "gmail_tool + memory_tool"
Cohesion: 0.08
Nodes (39): check_emails(), _decode_body(), _format_date(), get_email_body(), _get_gmail_service(), _get_header(), list_unread(), gmail_tool.py — Jarvis Gmail Integration (Step 5)… (+31 more)

### Community 36 - "ui_inspector"
Cohesion: 0.10
Nodes (11): Walk all descendants looking for any control whose window_text contains `text`…, Fire an element's primary action via UIA Invoke pattern. No mouse movement —…, Inject text into an input element via UIA Value pattern. No simulated…, Read text from an element via UIA TextPattern or window_text. Returns empty…, Walk the accessibility tree and return all elements up to `depth` levels. Use…, Core wrapper around pywinauto's UIA backend. All interactions go through the OS…, Get a window wrapper by partial title match (regex-safe). Returns None if not…, Get the currently focused window via Win32 HWND matching. (+3 more)

### Community 37 - "agentic_web + email-calendar"
Cohesion: 0.06
Nodes (34): agentic_web_action(), _worker(), _build_search_queries(), _fetch_page_text(), __init__(), _get_api_key(), agentic_web.py — Smart Web Research Engine for Jarvis…, Download a page and return clean readable text (no HTML tags). (+26 more)

### Community 38 - "exact_render"
Cohesion: 0.07
Nodes (55): _abs_text(), _bar_grid_html(), _bg_grid(), canon_title(), _chips_html(), _contact_html(), _content_html(), _est_height() (+47 more)

### Community 39 - "pipeline"
Cohesion: 0.12
Nodes (23): run(), _align(), analyse_reference(), line_box(), _choose_families(), best_in(), total(), _font_styles() (+15 more)

### Community 40 - "memory"
Cohesion: 0.21
Nodes (10): format_preferences_for_prompt(), get_all_preferences(), Jarvis Vector Memory — ChromaDB-based long-term memory engine. Stores and…, Returns a string suitable for injecting into LLM prompts., Stable short ID based on content hash., Return all stored preferences as a plain dict., _uid(), chromadb (+2 more)

### Community 42 - "resume_builder + integrate"
Cohesion: 0.06
Nodes (56): _apply_op(), _attachments(), create_resume(), _custom_sections(), detect_resume_request(), _edit_content(), editor_page(), editor_save() (+48 more)

### Community 43 - "air-drawing + air_drawing_tool"
Cohesion: 0.18
Nodes (9): open_air_drawing(), Opens the Air Drawing Canvas on the screen. This feature allows the user to…, Air drawing (webcam hand drawing), Files & symbols (auto-generated, line numbers are current), Flow, Gotchas, Graphify, Purpose (+1 more)

### Community 44 - "ppt_designer"
Cohesion: 0.09
Nodes (25): _best_window(), E(), gradient_box(), _line_factor(), line_shape(), _pil_font(), place_image(), ppt_designer.py — Adaptive Design Engine (PPT v6)… (+17 more)

### Community 45 - "voice"
Cohesion: 0.10
Nodes (30): loanword_ratio(), Share of Devanagari words that are English loanwords ("ओपन क्रोम" → 1.0). High…, _clean_transcript(), _finish(), _get_groq(), _groq_once(), groq_stt_available(), _load_whisper_model() (+22 more)

### Community 46 - "package + App"
Cohesion: 0.16
Nodes (11): App(), ChatMessage(), API_BASE, frontend_src_index, lucide-react, react, ref_react_dom_client, react-markdown (+3 more)

### Community 47 - "acoustic_tripwire"
Cohesion: 0.05
Nodes (30): AcousticWakeEngine, calibrate_tripwire(), _generate_chime(), get_wake_event(), _play_chime(), ndarray, Background thread that watches the microphone for a double-clap pattern. Usage…, Start the background listening thread. (+22 more)

### Community 48 - "syllabus-auditor"
Cohesion: 0.29
Nodes (6): Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Purpose, Syllabus auditor (YouTube playlist vs syllabus), Triggers

### Community 49 - "agents"
Cohesion: 0.33
Nodes (5): Agents: DAG executor, linear planner, dynamic skills, Data, Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify

### Community 50 - "client + test_concurrency"
Cohesion: 0.06
Nodes (27): Send one of the reply drafts generated by generate_reply_draft. draft_index is…, send_style_reply(), CacheClient, Any, Store a key-value pair, optionally with a TTL. Args: key: Cache key. value:…, Delete a key from the cache. Returns: True if the key existed and was deleted,…, Retrieve server statistics (hit rate, evictions, cache size, etc.). Returns…, Explicitly close the socket connection. (+19 more)

### Community 52 - "calendar_tool"
Cohesion: 0.27
Nodes (9): add_event(), check_today_schedule(), _get_calendar_service(), get_upcoming_events(), calendar_tool.py — Jarvis Google Calendar Integration (Step 8)…, Create a new event in Google Calendar. - title: "Project Meeting" - date:…, Authenticate and return a Google Calendar API service object., List events in the next N days. (+1 more)

### Community 53 - "package"
Cohesion: 0.14
Nodes (14): devDependencies, autoprefixer, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, postcss (+6 more)

### Community 55 - "recolor + exact_render"
Cohesion: 0.17
Nodes (18): _raster_palette(), Dominant colours of an exact copy's images (background, heading boxes, icons)…, asset_files(), walk(), Every image of the copy (background plates, heading boxes, icons, bars...),…, clean_pairs(), dominant(), _hex() (+10 more)

### Community 56 - "llm + llm-personality"
Cohesion: 0.07
Nodes (41): classify_context(), detect_language(), context_classifier.py — Jarvis Situational Awareness…, Detect whether the user spoke English, Hinglish, or Hindi. Returns: 'english' —…, Classify the situation from user input. Returns a dict with keys: urgency :…, check_for_tool_intent(), generate_chat_response(), _groq_generate() (+33 more)

### Community 57 - "prompt_enhancement_library + skill_prompt_enhancer"
Cohesion: 0.17
Nodes (19): check_for_hallucination(), clean_output(), detect_domain(), is_bloated(), protect_blocks(), prompt_enhancement_library.py…, Replace ``` fenced blocks with [[BLOCK_n]] placeholders., Put protected blocks back; append any the model dropped. (+11 more)

### Community 58 - "resume_builder"
Cohesion: 0.08
Nodes (59): _clean_free(), _competencies_html(), _contact_html(), _css_val(), _custom_section_html(), _data_uri(), _decor_html(), _design_set() (+51 more)

### Community 59 - "web_search + tools"
Cohesion: 0.09
Nodes (32): research_scraper.py — Autonomous Web Research Scraper…, _extract_location(), get_info(), get_weather(), Pulls a clean location name out of a weather query., Get current weather using wttr.in — returns a clean spoken string., Search for a query within a specific website using DuckDuckGo site: operator., Read and extract readable text content from a specific URL. (+24 more)

### Community 60 - "content_humanizer"
Cohesion: 0.17
Nodes (21): build_structure_prompt(), build_vocab_prompt(), call_groq(), check_similarity(), detect_tone(), fact_check(), get_groq_client(), get_sentence_scores() (+13 more)

### Community 61 - "tools + ui_inspector"
Cohesion: 0.12
Nodes (17): click_ui_element_uia(), dump_app_ui_tree(), Click a UI element inside an app by AutomationId, name, or control type. Does…, Inject text into a specific input field in an app via UIA Value pattern. No…, Read the current text content of a UI element — e.g. a terminal output pane, a…, Dump the full Windows UI Automation accessibility tree of an app window. Use…, read_ui_element_text(), type_into_ui_element() (+9 more)

### Community 62 - "voice + voice"
Cohesion: 0.17
Nodes (11): language_mismatch(), True if a reply sentence is in the other language than the one the user spoke., Config (`app/core/config.py` + env), Files & symbols (auto-generated, line numbers are current), Flow (`scripts/voice_agent.py`), Graphify, Measured (2026-09-30/10-01, i9-13900H, no GPU), Purpose (+3 more)

### Community 63 - "ppt + KNOWN_ISSUES"
Cohesion: 0.11
Nodes (16): ppt_edit(), Follow-up edit of the last deck (generator). See ppt_studio.edit., _ppt_edit(), Generator wrapper — follow-up edits of the last deck ("on slide 3 …", "make it…, Entry points, Files & symbols (auto-generated, line numbers are current), Flow — edit (`ppt_edit` → `ppt_studio.edit` → `ppt_content.apply_edit`), Graphify (+8 more)

### Community 64 - "whatsapp_smart + tools"
Cohesion: 0.06
Nodes (41): Resolves site name, opens a VISIBLE browser, and performs a search or action…, smart_web_action(), create_word_doc(), get_system_info(), Returns CPU usage, RAM usage, and battery status., Takes a full screenshot and saves to Desktop., Snaps left_app to left half and right_app to right half using Win32 API (no…, Create a .docx Word document with the given content. content can be a list of… (+33 more)

### Community 65 - "frontend"
Cohesion: 0.22
Nodes (8): Frontend (`frontend/src`), Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Key behaviour (App.jsx), Purpose, Web UI (React/Vite), DagPlanPanel()

### Community 67 - "ppt_content"
Cohesion: 0.11
Nodes (29): architect_slides(), ask(), _retry(), run(), _complete_from_source(), deck_facts(), detect_profile(), extractive_ok() (+21 more)

### Community 68 - "spotify_service"
Cohesion: 0.09
Nodes (38): _buttons(), _clean_query(), _close_spotify(), _com_init(), _content_play_buttons(), _find_spotify_window(), _cb(), _is_playing() (+30 more)

### Community 69 - "prompt_enhancer_button"
Cohesion: 0.14
Nodes (4): EnhanceButton, Move (and optionally show) without ever activating the window; Tk's deiconify()…, Default spot: just above the prompt box's top-right corner; below it or inside…, _save_state()

### Community 70 - "voice"
Cohesion: 0.11
Nodes (12): hinglish_to_devanagari(), Rewrite the Hindi words of a romanized Hinglish sentence in Devanagari, leaving…, Channel, _norm_words(), The speech stream of one command's reply., Plays sentences from many Channels without overlap: - urgent phrases (acks,…, Barge-in "stop": silence now and drop everything queued., Did the mic just hear Jarvis himself (speaker → mic bleed)? Echo comes back… (+4 more)

### Community 72 - "assignment_tool + assignment_pipeline"
Cohesion: 0.19
Nodes (12): do_assignment(), Master orchestrator. Uses a background thread for all Playwright code. Yields…, extract_questions(), list_assignments(), _merge_and_deduplicate(), Merge questions from all three tracks. Priority: regex > vision > llm text. A…, Extract ALL questions from an assignment PDF using a 3-track hybrid system.…, Resolve PDF path: handles full paths, filenames, partial names. (+4 more)

### Community 73 - "test_lru"
Cohesion: 0.20
Nodes (5): Accessing 'a' should move it to MRU and save it from eviction., Re-setting an existing key should move it to MRU., len(cache.map) must never exceed capacity., Fill to capacity+1. The first key inserted (LRU) should be evicted., TestEviction

### Community 74 - "voice"
Cohesion: 0.15
Nodes (8): Clip, prewarm(), PCM (int16, 24 kHz) that fills while synthesis streams; playable immediately., hi' → Hindi voice, 'en' → English voice, for one sentence., Begin synthesising `text` now; returns a Clip that can be played while it fills., Synthesise short stock phrases (greetings, acks) into the cache for instant…, route_language(), start_clip()

### Community 75 - "renderer"
Cohesion: 0.23
Nodes (11): _count_pages_and_fill(), _launch_browser(), renderer.py — Browser rendering and output verification for replica resumes.…, Launches Chromium (or msedge fallback). Same as resume_builder._launch., Uses PyMuPDF (fitz) to count pages and measure fill of last page. Returns…, Extracts PNG previews from the PDF using PyMuPDF. Returns list of PNG file…, Renders the compiled HTML to PDF + PNG previews. Uses Playwright Chromium (or…, Renders the HTML to a PNG screenshot (full page). Used by the repair loop to… (+3 more)

### Community 76 - "youtube_player"
Cohesion: 0.31
Nodes (9): _fallback(), fmt_span(), fmt_time(), player_action(), _pos(), _rate(), 10 → '10 seconds', 600 → '10 minutes', 90 → '1 minute 30 seconds'., Keyboard-only version of an action. Only used for Firefox (which blocks the… (+1 more)

### Community 77 - "uia_local"
Cohesion: 0.12
Nodes (3): Element, Minimal pywinauto-style wrapper around an IUIAutomationElement., Rect

### Community 78 - "server"
Cohesion: 0.11
Nodes (15): acoustic_tripwire.py — Jarvis Acoustic Wake Engine…, neural_cache, client.py — Python Client Library for Neural Cache (Milestone 5)…, CacheServer, main(), server.py — TCP Accept Loop for Neural Cache (Milestone 4)…, Full startup: recover state, start engine, begin accepting connections., Restore cache state from disk before the engine thread starts. Called on the… (+7 more)

### Community 79 - "assignment_assembler"
Cohesion: 0.36
Nodes (7): assemble_assignment(), _create_powerpoint(), _create_word_doc(), _parse_qa_json(), Jarvis Assignment Tool — Phase 4: Document Assembly…, Assemble the extracted/humanized questions and answers into a formatted…, Extract and parse the JSON array from the input string.

### Community 80 - "package"
Cohesion: 0.22
Nodes (9): dependencies, framer-motion, lucide-react, react, react-dom, react-markdown, react-syntax-highlighter, remark-gfm (+1 more)

### Community 81 - "handTracking"
Cohesion: 0.31
Nodes (3): CameraView(), getHandsConstructor(), HandTracker

### Community 82 - "chat + youtube_control"
Cohesion: 0.05
Nodes (63): chat_endpoint(), _dag_stream_with_history(), planner_stream(), response_stream_with_history(), resume_stream(), tool_stream(), ChatRequest, clear_history() (+55 more)

### Community 83 - "screen_vision + screen_reader"
Cohesion: 0.05
Nodes (59): _accessibility_tree(), describe_screen_for_llm(), get_screen_screenshot_b64(), _groq_vision_screen(), _init_tesseract(), _ocr_screen(), screen_reader.py — Jarvis Screen Vision (VLM-first architecture)…, Legacy OCR layer. Works on any app but extracts raw text only — no layout,… (+51 more)

### Community 84 - "youtube_player"
Cohesion: 0.33
Nodes (7): _num(), parse_clock(), parse_duration(), parse_player_command(), Map a spoken player command to (action, amount, value), or None. `t` should…, 10 minutes' → 600, '1 hour 5 min' → 3900, 'half a minute' → 30, '90 s' → 90.…, 5:30' → 330, '1:02:03' → 3723, 'to 5 30' → 330. None if absent.

### Community 85 - "voice_agent"
Cohesion: 0.09
Nodes (23): app_services, AsyncClient, difflib, httpx, pyaudio, _clean_agentic_line(), extract_wake_word_command(), _is_wake_token() (+15 more)

### Community 86 - "ControlPanel + HandSkeleton"
Cohesion: 0.13
Nodes (13): frontend_src_airdrawing_airdrawing, COLORS, ControlPanel(), FONTS, SHAPES, FINGERTIP_INDICES, HAND_CONNECTIONS, HandSkeleton() (+5 more)

### Community 88 - "ppt_chart_engine"
Cohesion: 0.33
Nodes (3): ChartEngine, Stateless chart renderer. All colors are derived from the active PPT palette —…, Render a chart from structured data. Args: chart_data: {"type": "bar",…

### Community 89 - "compiler"
Cohesion: 0.11
Nodes (20): _commands_to_d(), _compile_document_css(), _compile_frame(), _compile_path(), _fill_to_css_background(), _fill_to_svg_fill(), _mm_to_pt(), _parametric_to_commands() (+12 more)

### Community 90 - "ingest"
Cohesion: 0.26
Nodes (12): _imread(), load_reference(), ndarray, ingest.py — Reference file → clean page image at a fixed working resolution. *…, Returns {img (BGR, page width = 210 mm at PX_PER_MM), page_h_mm, src_dpi,…, Grey/dark colours typical of a viewer background (a white or tinted border is…, Trims uniform viewer-coloured borders. Returns x0, y0, x1, y1., Phone screenshots carry app overlays on top of the page: Google Lens' dark… (+4 more)

### Community 91 - "measure"
Cohesion: 0.12
Nodes (26): analyse(), _cdist(), _get_ocr(), _h_overlap(), _is_upper(), _item_roles(), _letters(), measure_line() (+18 more)

### Community 92 - "repair"
Cohesion: 0.10
Nodes (21): compile_replica_html(), Main entry point. Returns a complete HTML document string. content : normalised…, apply_diff_patches(), compute_visual_diff(), _images_to_base64_pair(), _parse_diff_json(), _patch_fill(), repair.py — Visual diff and bounded repair loop. Runs after an initial render… (+13 more)

### Community 94 - "nlp_extractor + research_scraper"
Cohesion: 0.12
Nodes (11): NLPExtractor, nlp_extractor.py — LLM-Powered Fact & Entity Extractor…, Runs extraction on each scraped source and aggregates the results. Returns a…, research_pipeline.py — End-to-End Autonomous Research Orchestrator…, Scrapes the web for a topic and extracts verified facts and statistics. Yields…, research_topic(), Searches DDG for the topic, fetches the top N links concurrently, and returns…, ResearchScraper (+3 more)

### Community 96 - "social_content_manager + content-tools"
Cohesion: 0.11
Nodes (19): main(), prompt_overlay.py ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Jarvis…, build_prompt(), call_llm(), generate_social_content(), Refine an existing piece of social media content based on user instructions.…, Calls Groq Llama 3.3 70B directly for maximum speed. No slow fallbacks., Generate professional, multi-version social media content. (+11 more)

### Community 97 - "youtube_player"
Cohesion: 0.08
Nodes (52): element_from_handle(), focused_element(), uia_local.py — thread-safe UI Automation access (helper, not a tool)…, This thread's IUIAutomation (COM initialised for the thread on first use)., uia(), _get_process_name(), Get the executable name of the process owning this HWND., _address_bar_focused() (+44 more)

### Community 98 - "compiler"
Cohesion: 0.18
Nodes (18): _compile_chart(), _compile_section(), _it(), Simple <ul><li> list of skill names., High-level section renderer. Returns complete HTML for the section (heading +…, Returns data-item attribute string in edit mode, else empty string., Compiles a CHART node to the appropriate skill/language visualisation., Progress bar skills. Supports 2-column CSS grid. (+10 more)

### Community 99 - "compiler"
Cohesion: 0.15
Nodes (14): _compile_image(), _compile_node(), _compile_rule(), _compile_text(), _initials_block(), Returns the initials text for the photo placeholder., Converts a TEXT_STYLE dict to a CSS properties string., Dispatches to the appropriate node compiler based on node['type']. (+6 more)

### Community 100 - "mysql_db + rag_memory"
Cohesion: 0.20
Nodes (12): aiomysql, close_mysql(), init_mysql(), mysql_db.py — Jarvis Async MySQL Connection Pool…, Gracefully close the MySQL connection pool on server shutdown., Initialize the MySQL connection pool and ensure all required tables exist. Safe…, init_rag_memory(), _load_faiss_index() (+4 more)

### Community 101 - "ppt_composer + ppt_designer"
Cohesion: 0.08
Nodes (29): _balanced_rows(), _fill(), image_block(), _image_panel(), _masonry(), Split items into rows with at most one item difference (5 in 3 cols → 3+2, 7 →…, How much extra height a section can absorb before it looks inflated., Framed images (no crop) + numbered captions under each. Returns used height. (+21 more)

### Community 102 - "package"
Cohesion: 0.40
Nodes (5): scripts, build, dev, lint, preview

### Community 103 - "schema"
Cohesion: 0.12
Nodes (15): make_chart_node(), make_group_node(), make_repeat_node(), make_ring_spec(), make_text_node(), make_text_style(), schema.py — Scene-graph node types, constants, and factory helpers. A Replica…, Returns a complete TEXT_STYLE dict. (+7 more)

### Community 105 - "message_reader + thread_extractor"
Cohesion: 0.05
Nodes (50): _focus_or_open_whatsapp(), _bring_whatsapp_to_front(), _get_whatsapp_window(), _heuristic_parse_ocr_lines(), _parse_uia_message_string(), message_reader.py — Jarvis WhatsApp Intelligence: Message Reader…, Restores and focuses WhatsApp window. Returns True on success., Walks the WhatsApp UIA accessibility tree to extract messages. WhatsApp Desktop… (+42 more)

### Community 106 - "ppt_tool"
Cohesion: 0.08
Nodes (29): _auto_select_image_layout(), _bg_fill(), _c(), compute_split_geometry(), _corner_L(), _detect_purpose(), extract_theme_from_image(), _extract_theme_pil_local() (+21 more)

### Community 107 - "assignment_pipeline"
Cohesion: 0.20
Nodes (17): _browser_thread(), _find_el(), _get_answer(), _get_browser_ctx(), _groq_answer(), _groq_humanize(), _humanize_browser(), Queue (+9 more)

### Community 108 - "assignment"
Cohesion: 0.33
Nodes (5): Assignment solver (5 phases), Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Purpose

### Community 109 - "test_protocol"
Cohesion: 0.10
Nodes (23): decode_message(), encode_message(), protocol.py — Wire Protocol for Neural Cache (Milestone 2)…, Serialise a dict to the wire format: [4-byte length][UTF-8 JSON body] Args:…, Read exactly one message from a socket, handling partial TCP reads correctly.…, Loop until exactly n bytes have been read from sock. This is necessary because…, _recv_exact(), make_fake_socket() (+15 more)

### Community 110 - "bindings"
Cohesion: 0.20
Nodes (9): format_binding_value(), iter_content_items(), bindings.py — Content binding resolution and editor path mapping. Binding paths…, Iterator for repeat bindings. Yields (index, item) for each item in the list at…, Returns the display title for a section, checking content['section_titles']…, Resolves a binding path against content dict. Returns the value at that path,…, Converts a resolved binding value to a display string. - None / empty string /…, resolve_binding() (+1 more)

### Community 111 - "compiler"
Cohesion: 0.23
Nodes (12): _compile_repeat(), _ef(), Renders a single experience entry (same format as legacy builder's…, Renders a single education entry., Renders a single project entry (same format as legacy builder's _projects_html)., Renders the contact section with icons., Returns escaped text in normal mode, or a contenteditable span in edit mode.…, Compiles a REPEAT node by iterating content[binding] and rendering items. (+4 more)

### Community 112 - "README"
Cohesion: 0.50
Nodes (3): Expanding the ESLint configuration, React Compiler, React + Vite

### Community 119 - "safe_executor + refresh_docs"
Cohesion: 0.08
Nodes (26): Exception, Safe Code Executor for Jarvis ------------------------------- Runs LLM-…, Restricted open(): blocks writes to system paths., Restricted __import__: blocks dangerous modules., Raised when generated code violates safety constraints., AST visitor that inspects generated code before execution., Parse and walk the AST, raising SecurityError on violations., _safe_import() (+18 more)

### Community 120 - "README"
Cohesion: 0.20
Nodes (9): Architecture, Benchmark, Files, LRU Cache Design, Neural Cache, Persistence, Running, Tests (+1 more)

### Community 122 - "resume_builder + resume-exact-replica"
Cohesion: 0.05
Nodes (66): _analyse_design(), _apply_color(), _apply_layout_answer(), _apply_layout_hint(), _balance_columns(), _closest_preset(), _contrast(), _crop_photo() (+58 more)

### Community 124 - "voice"
Cohesion: 0.18
Nodes (5): get_player(), _Player, One persistent 24 kHz output stream driven by a callback that pulls from a…, Loudest output RMS in the last `window` s — the voice agent's echo reference., Play a clip as it arrives. Returns False if interrupted.

### Community 125 - "resume_builder"
Cohesion: 0.13
Nodes (22): _build_content(), _condense_content(), _content_brief(), _drop_invented(), clean_text(), ok(), _finalize_content(), _fit_render() (+14 more)

### Community 126 - "compiler"
Cohesion: 0.18
Nodes (9): _compile_group(), _e(), Radar/spider chart as inline SVG. 100x100 viewBox, center (50,50), max radius…, Tags where size/opacity indicates level (higher → larger/more saturated)., Renders a single ring/donut chart SVG for a skill., Compiles a GROUP node to a <div>. Used for section headings and composites., _render_radar(), _render_tag_level() (+1 more)

### Community 127 - "os-control"
Cohesion: 0.40
Nodes (4): Files & symbols (auto-generated, line numbers are current), Graphify, Purpose, Windows/OS control: windows, media, apps, files

### Community 128 - "schema"
Cohesion: 0.50
Nodes (4): make_default_replica_document(), make_page_node(), Returns a complete PAGE node., Returns a skeleton replica document with an empty scene graph. The caller is…

### Community 129 - "main + screen_vision"
Cohesion: 0.08
Nodes (32): get_alerts(), _on_screen_alert(), get, post, Stop watcher, acoustic tripwire, and close DB pool cleanly on server shutdown., Frontend polls this endpoint to receive proactive JARVIS screen alerts. e.g.…, Return current acoustic tripwire state for the frontend toggle., Arm the acoustic tripwire so double-claps wake Jarvis. (+24 more)

### Community 130 - "voice_agent"
Cohesion: 0.12
Nodes (10): AbstractEventLoop, Fixed on 2026-10-01 (voice, round 2), _ClapDetector, _EnergyVAD, ndarray, Queue, Stateful frame-by-frame Silero VAD using the ONNX model bundled with faster-…, Fallback if Silero can't load: adaptive noise floor. (+2 more)

### Community 131 - "resume_router + tools"
Cohesion: 0.15
Nodes (12): get, post, resume_router.py — FastAPI router for the visual resume editor…, resume_editor(), resume_save(), execute_tool(), BaseModel, post (+4 more)

### Community 132 - "dag_executor + dynamic_skill"
Cohesion: 0.06
Nodes (56): _semantic_window_adjust(), Settings, find_skill(), Persist a successful dynamic skill for future reuse., Returns up to n most relevant saved skills for a given task description. Each…, save_skill(), _call_dag_planner(), DAGNode (+48 more)

### Community 133 - "download_kokoro"
Cohesion: 0.40
Nodes (3): download(), Download Kokoro TTS model files from GitHub releases. Run this ONCE to get the…, urllib_request

### Community 134 - "assignment_tool"
Cohesion: 0.50
Nodes (4): _extract_via_llm_text(), _pdf_pages_to_text(), Extract text from each PDF page separately. Returns list of page strings., LLM-based text extraction as fallback for when regex fails.

### Community 138 - "browser_mail"
Cohesion: 0.24
Nodes (7): check_emails(), _get_api_key(), list_unread(), browser_mail.py — Standard Browser Mail Automation…, A generic tool to perform any mail task (like sending or reading) by pre-…, smart_mail_action(), webbrowser

### Community 139 - "whatsapp_call"
Cohesion: 0.27
Nodes (10): flow_stream(), _click_voice_call_button(), confirm_whatsapp_call(), _focus_or_open_whatsapp(), _get_whatsapp_window(), initiate_whatsapp_call(), whatsapp_call.py — Jarvis Smart WhatsApp Calling Integration (Fully Isolated)…, Focus the WhatsApp window or open it if not running. Returns True on success. (+2 more)

### Community 141 - "prompt_enhancer_button"
Cohesion: 0.21
Nodes (11): _box_contains(), _box_set_value(), _clip_get(), _clip_set(), _ctrl(), _focus(), _focused_text(), _norm() (+3 more)

### Community 142 - "web"
Cohesion: 0.40
Nodes (4): Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Web search, research & browser automation

### Community 143 - "hinglish_normalizer"
Cohesion: 0.18
Nodes (11): devanagari_to_hinglish(), _sub(), normalize_for_tts(), hinglish_normalizer.py — Devanagari Crash Prevention + Text Normalizer…, One Devanagari word → casual Hinglish roman ("चलाओ" → "chalao", "करना" →…, Romanize a Devanagari (Hindi) transcript for the backend, keeping any Latin…, Transform text so it's safe and natural-sounding for TTS: 1. Replace known…, Markdown → plain speakable text (keeps Devanagari). Also drops URLs and emoji. (+3 more)

### Community 144 - "neural-cache"
Cohesion: 0.25
Nodes (7): Design, Files & symbols (auto-generated, line numbers are current), Graphify, Neural cache (Redis-like LRU server), Purpose, Runtime, Tests

### Community 145 - "voice_agent"
Cohesion: 0.33
Nodes (3): MicListener, Initial ambient noise floor (kept up to date on every non-speech frame)., One 32 ms frame → clap check + VAD state machine → events.

### Community 148 - "test_lru"
Cohesion: 0.50
Nodes (3): Return average time per (set + get) operation in microseconds., Per-op time for N=1000 vs N=100000 should be within 3x of each other. If the…, TestO1Timing

### Community 149 - "memory + rag_memory"
Cohesion: 0.06
Nodes (47): forget_memory(), ForgetRequest, get_history(), ingest_memory(), IngestRequest, memory_stats(), BaseModel, delete (+39 more)

### Community 150 - "test_lru"
Cohesion: 0.18
Nodes (7): large_cache(), fixture, test_lru.py — Unit tests for neural_cache.lru (Milestone 7)…, LRU cache with capacity 3 — easy to reason about eviction., small_cache(), TestSentinels, pytest

### Community 151 - "schema"
Cohesion: 0.25
Nodes (8): make_frame_node(), make_no_fill(), make_padding(), make_path_node(), Returns {"type": "none"}, Returns a complete FRAME node., Returns a complete PATH node., Returns {"top_mm": ..., "right_mm": ..., "bottom_mm": ..., "left_mm": ...}

### Community 152 - "lru"
Cohesion: 0.29
Nodes (4): Any, Serialise the entire live cache to a plain dict. Expired entries are excluded —…, Restore cache state from a snapshot dict (produced by snapshot()). Called once…, Place node at the LRU (least-recently-used) end of the list.

### Community 153 - "smart_navigator + ssml_processor"
Cohesion: 0.10
Nodes (16): _get_api_key(), _llm_extract(), smart_navigator.py — Isolated Smart Web Navigator for Jarvis…, Attempt to find the GROQ API key safely., Pass scraped text through LLM for structured extraction., Resolve a verbal site name like 'unstop' to a URL like 'https://unstop.com'., _resolve_url(), add_human_prosody() (+8 more)

### Community 154 - "prompt_enhancer_button + prompt-enhancer"
Cohesion: 0.16
Nodes (13): _has_pattern(), _hint_text(), _ide_allows(), _is_editable(), is_prompt_box(), Writable text input: <textarea>/<input>/native edit, or a contenteditable…, In IDEs only chat / agent inputs qualify, never the code editor, the terminal,…, Entry points (+5 more)

### Community 157 - "assignment_tool"
Cohesion: 0.15
Nodes (19): _classify_question_type(), _clean_text(), _extract_marks(), _extract_via_vision(), _has_figure_reference(), _parse_llm_json_response(), _pdf_pages_to_images(), Jarvis Assignment Tool — Phase 1: Smart Question Extractor… (+11 more)

### Community 160 - "voice + tools"
Cohesion: 0.12
Nodes (14): Sets a reminder that Jarvis will speak after a given number of seconds., set_reminder(), preload_local_stt(), Load the local Whisper models in the background (voice agent startup)., Feed streamed tokens; get back speakable sentences as early as possible., Speak a complete text. All sentences synthesise in parallel, play in order., Speak an async generator of text chunks, sentence by sentence, pipelined., SentenceSplitter (+6 more)

### Community 161 - "compiler"
Cohesion: 0.33
Nodes (6): _guess_icon(), _icon_svg(), Renders a single competency as an icon+title+description card., Returns an inline SVG icon using the _ICONS dict., Guesses an icon name from a competency title string., _render_competency_item()

### Community 162 - "CODEMAP"
Cohesion: 0.22
Nodes (8): Backend core & API, Code map, Frontend (`frontend/src`, React 19 + Vite + Tailwind 4), Ignore these (no runtime role), Neural cache (neural_cache/, see its README.md), Scripts, Services (app/services), WhatsApp intelligence (app/services/whatsapp_intelligence)

### Community 164 - "schema"
Cohesion: 0.50
Nodes (4): make_image_node(), make_size(), Returns a complete IMAGE node., Returns size dict, only including non-None values.

### Community 165 - "compiler"
Cohesion: 0.67
Nodes (3): _collect_google_fonts(), _walk(), Scans the scene graph and style registry for font families. Returns a Google…

### Community 166 - "schema + bindings"
Cohesion: 0.22
Nodes (7): build_editor_path_map(), Walks the scene graph and builds a map from binding path -> list of node IDs…, collect_bindings(), Depth-first traversal of the scene graph. visitor(node, parent, depth) is…, Returns all unique binding paths referenced in the scene graph. E.g. ["name",…, walk_nodes(), _walk()

### Community 170 - "whatsapp"
Cohesion: 0.33
Nodes (5): Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Purpose, WhatsApp: send, call, read, reply-style cloning

### Community 171 - "persistence"
Cohesion: 0.09
Nodes (17): Any, Path, Queue, persistence.py — WAL + Snapshot for Neural Cache (Milestone 6)…, Flush and close the file handle cleanly on server shutdown., Manages periodic full-state snapshots. The snapshot itself is triggered through…, Serialise cache state to disk and truncate the WAL. Called by CacheEngine on…, Load the snapshot from disk. Returns None if no snapshot exists yet. Called… (+9 more)

### Community 173 - "benchmark"
Cohesion: 0.13
Nodes (10): JSONFileBaseline, main(), measure_latency(), measure_throughput(), benchmark.py — Neural Cache vs JSON-file Baseline (Milestone 8)…, Spin up n_threads threads each doing ops_per_thread SET+GET pairs. Returns…, Mimics memory_tool.py's approach: every read/write touches disk. Uses a…, Run op_fn warmup times (discard), then timed times (measure). Returns (mean_µs,… (+2 more)

## Knowledge Gaps
- **165 isolated node(s):** `Settings`, `build`, `dev`, `lint`, `preview` (+160 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1612 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **28 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Tool registry` connect `tools` to `dark_enhancement + dark_video_enhancement`, `window_layout + tools`, `youtube_control + youtube_player`, `syllabus_auditor`, `browser_mail`, `whatsapp_call`, `browser_tool`, `file_ops`, `assignment_answers`, `chat-routing + chat`, `memory + rag_memory`, `ppt_router + ppt_tool`, `assignment_humanizer + task_ledger`, `voice + tools`, `gmail_tool + memory_tool`, `agentic_web + email-calendar`, `resume_builder + integrate`, `air-drawing + air_drawing_tool`, `calendar_tool`, `web_search + tools`, `tools + ui_inspector`, `ppt + KNOWN_ISSUES`, `whatsapp_smart + tools`, `spotify_service`, `assignment_tool + assignment_pipeline`, `assignment_assembler`, `chat + youtube_control`, `social_content_manager + content-tools`?**
  _High betweenness centrality (0.136) - this node is a cross-community bridge._
- **Why does `open_air_drawing()` connect `air-drawing + air_drawing_tool` to `tools`?**
  _High betweenness centrality (0.080) - this node is a cross-community bridge._
- **Are the 122 inferred relationships involving `Tool registry` (e.g. with `keyword_detect_tool()` and `_media_compound()`) actually correct?**
  _`Tool registry` has 122 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `chat_endpoint()` (e.g. with `describe_screen_for_llm()` and `get_screen_text_summary()`) actually correct?**
  _`chat_endpoint()` has 8 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Settings`, `build`, `dev` to the rest of the system?**
  _165 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `tools` be split into smaller, more focused modules?**
  _Cohesion score 0.033176593521421105 - nodes in this community are weakly interconnected._
- **Should `style_profiler + reply_generator` be split into smaller, more focused modules?**
  _Cohesion score 0.0602322206095791 - nodes in this community are weakly interconnected._