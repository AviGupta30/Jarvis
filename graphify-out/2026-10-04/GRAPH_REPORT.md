# Graph Report - Jarvis  (2026-10-04)

## Corpus Check
- 218 files · ~332,439 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 3, .css 3, .bat 1)

## Summary
- 3759 nodes · 8112 edges · 185 communities (155 shown, 30 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 798 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d81c4976`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Tool registry
- style_profiler.py
- analyzer
- plate.py
- ppt_chart_engine
- dark_enhancement.py
- window_layout.py
- CacheEngine
- youtube_control.py
- syllabus_auditor
- ppt_studio.py
- ppt_designer
- browser_tool.py
- LRUCache
- file_ops.py
- ppt_tool
- assignment_answers.py
- resume_detector
- fontmatch.py
- prompt_enhancer_button.py
- generate_deck
- keyword_detect_tool
- ppt_research
- ppt_template
- main
- ppt_router
- package
- gestureController + gestureInterpreter
- orchestrator.py
- ppt_image_engine
- test_task_resumption.py
- ppt_composer + ppt_designer
- dsa_enforcer
- ppt_content.py
- memory_tool.py
- PromptOverlay
- ui_inspector
- agentic_web.py
- exact_render.py
- pipeline.py
- memory/memory.py
- transformEngine
- create_resume
- air-drawing + air_drawing_tool
- ppt_designer
- voice.py
- package + App
- acoustic_tripwire
- assignment_humanizer
- pyautogui
- client
- interactionEngine + DrawingCanvas
- calendar_tool.py
- package
- strokeManager
- repair
- llm.py
- prompt_enhancement_library + skill_prompt_enhancer
- resume_builder.py
- web_search
- content_humanizer
- research_scraper
- Voice: STT, TTS, wake word, clap wake, overlay
- PowerPoint generator
- whatsapp_smart
- frontend
- shapeManager
- Flow — create (`ppt_tool.ppt_create` → `ppt_studio.create`, a generator)
- spotify_service.py
- prompt_enhancer_button
- voice
- drawingEngine
- tool-registry
- test_lru
- render_replica_html
- refresh_docs
- reply_generator.py
- Element
- engine.py
- Flow (`scripts/voice_agent.py`)
- package
- handTracking
- chat.py
- screen_vision.py
- jarvis_overlay.py
- voice_agent.py
- ControlPanel + HandSkeleton
- strokeRefiner
- ppt_chart_engine
- compiler
- ingest
- measure.py
- repair.py
- json
- editor_save
- typing
- youtube_player.py
- compiler
- compiler
- rag_memory.py
- ppt_designer
- package
- schema
- test_lru
- message_reader.py
- ppt_tool
- assignment_pipeline.py
- resume_builder
- encode_message
- bindings
- compiler
- README
- test_lru
- __init__
- README
- safe_executor.py
- README
- PROMPT_TEMPLATE
- resume_builder + resume-exact-replica
- FEATURES
- _Player
- resume_builder
- compiler
- test_concurrency
- exact_render
- main + screen_vision
- voice_agent
- resume_router
- dag_executor.py
- ppt_tool
- ppt_tool
- dsa_enforcer
- edge_tts
- pygame
- browser_mail
- whatsapp_call
- gmail_tool.py
- prompt_enhancer_button
- search_site
- hinglish_normalizer.py
- neural-cache
- voice_agent
- thread_extractor.py
- test_lru
- test_lru
- api/memory.py
- test_lru.py
- schema
- Node
- re
- Entry points
- test_protocol.py
- dsa-mode
- assignment_tool.py
- schema
- ppt_tool
- speak_text
- compiler
- Code map
- ssml_processor
- schema
- compiler
- schema + bindings
- main
- ppt_designer + ppt_composer
- ppt_studio
- whatsapp
- Any
- Content humanizer & social content
- os
- Dark image/video enhancement
- Fixed on 2026-09-28
- ppt_designer
- _long_lines
- ppt_tool
- ppt_tool + ppt_router
- _photo_edges
- .start_background_thread
- schema
- schema
- _ring_contrast

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
- `Adding a tool (checklist)` --references--> `keyword_detect_tool()`  [INFERRED]
  docs/features/tool-registry.md → app/api/chat.py
- `Calendar` --references--> `check_today_schedule()`  [INFERRED]
  docs/features/email-calendar.md → app/services/calendar_tool.py
- `Flow` --references--> `get_dsa_enforcer()`  [INFERRED]
  docs/features/dsa-mode.md → app/services/dsa_enforcer.py
- `Entry points` --references--> `PresentationBuilder`  [INFERRED]
  docs/features/ppt.md → app/services/ppt_tool.py
- `Gotchas` --references--> `classify_app()`  [INFERRED]
  docs/features/prompt-enhancer.md → app/services/prompt_enhancer_button.py

## Import Cycles
- None detected.

## Communities (185 total, 30 thin omitted)

### Community 0 - "Tool registry"
Cohesion: 0.02
Nodes (138): list_skills(), List all saved skill descriptions., Store a user preference (e.g. key='browser', value='Chrome')., save_preference(), ppt_styles(), Resolves site name, opens a VISIBLE browser, and performs a search or action…, smart_web_action(), append_to_file() (+130 more)

### Community 1 - "style_profiler.py"
Cohesion: 0.12
Nodes (27): build_style_profile(), One-time training: parse a WhatsApp .txt chat export to build your personal…, add_deflection_phrase(), build_style_profile(), _compute_profile_stats(), _empty_profile(), get_profile(), get_profile_summary() (+19 more)

### Community 2 - "analyzer"
Cohesion: 0.09
Nodes (53): _file_hash(), _hex(), _measure_band(), near(), _measure_frame(), near(), White frame around the coloured blocks (sidebar / header band) in the…, Gaps around a light name band (e.g. grey box behind the name next to a… (+45 more)

### Community 3 - "plate.py"
Cohesion: 0.12
Nodes (35): contact_type(), _hex(), background_mask(), _bg_model(), _bgr(), build(), comps_in(), _chip_gap() (+27 more)

### Community 4 - "ppt_chart_engine"
Cohesion: 0.12
Nodes (34): _bg_color(), _extract_strict_metric(), _fig_to_bytes(), _hex(), _metrics_to_bar(), _palette_colors(), ppt_chart_engine.py — Dynamic Data-Visualization Engine for JARVIS PPT…, Horizontal or vertical bar chart. (+26 more)

### Community 5 - "dark_enhancement.py"
Cohesion: 0.17
Nodes (20): _apply_gamma(), _fusion_and_polish(), get_all_enhancements(), _normalize_to_8bit(), _path_1_retinex(), _path_2_wavelet(), ndarray, run_pipeline_a() (+12 more)

### Community 6 - "window_layout.py"
Cohesion: 0.09
Nodes (38): True if the Spotify desktop app has a window (cheap: EnumWindows, no UIA)., spotify_running(), close_tab(), minimize_window(), Closes the current browser tab using Ctrl+W, targeting the real foreground app., Minimizes a specific window by name using Win32 ShowWindow., adjust_active_window(), _enumerate_app_windows() (+30 more)

### Community 7 - "CacheEngine"
Cohesion: 0.15
Nodes (13): CacheEngine, Any, Route a command dict to the appropriate handler. All handlers return a response…, Owns the LRUCache. Runs a single consumer loop on a dedicated thread. External…, Spawn the single writer thread. Call once at server boot., Gracefully stop the engine writer thread., The single consumer loop. Runs on CacheEngineThread. Processes one command at a…, err_response() (+5 more)

### Community 8 - "youtube_control.py"
Cohesion: 0.07
Nodes (56): _media_intent_for(), Media tool intent for one clause (YouTube-mode parser first, then keyword…, _dur_to_sec(), _end_session(), _fetch_results(), _find_channel(), _find_channel_at(), walk() (+48 more)

### Community 9 - "syllabus_auditor"
Cohesion: 0.07
Nodes (41): _approx_token_count(), _assemble_response(), audit_playlist_syllabus(), _build_vector_store(), _chunk_transcript(), _coverage_level(), _embed_texts(), _extract_playlist_id() (+33 more)

### Community 10 - "ppt_studio.py"
Cohesion: 0.09
Nodes (41): Separate the user's command, any pasted/attached content and attachment paths., [(n, heading, raw content)] split on 'Slide N:' markers of repaired text., raw_slide_blocks(), split_request(), _finish_theme(), _lum(), prepare_image(), Convert a legacy ppt_tool palette (bg/card/text/sub/ac1..) into a theme. (+33 more)

### Community 11 - "ppt_designer"
Cohesion: 0.14
Nodes (21): _compact_header(), box(), DeckRenderer, fit_size(), _items(), para_h(), Header + lead + list inside a column. Returns nothing., Portrait/square image as a full-height panel flush to one edge. (+13 more)

### Community 12 - "browser_tool.py"
Cohesion: 0.20
Nodes (22): browse_and_paginate(), browse_and_read(), _clean_text(), click_element(), _ensure_url(), fill_form(), _llm_extract(), _new_browser_page() (+14 more)

### Community 13 - "LRUCache"
Cohesion: 0.18
Nodes (8): LRUCache, Insert or update a key-value pair. - If key already exists: update value + TTL,…, Remove a key from the cache. Returns True if the key existed, False if it was…, Place node at the MRU (most-recently-used) end of the list., Remove node from its current position in the list (O(1) because doubly-linked)., Evict a specific node (unlink + remove from map)., O(1) Least-Recently-Used cache backed by: - dict[str, Node] — hash map for O(1)…, Return the value for key, or None on miss / expiry. On hit: moves node to the…

### Community 14 - "file_ops.py"
Cohesion: 0.11
Nodes (26): append_file(), bulk_rename(), delete_file(), diff_files(), _fmt_size(), list_directory(), _maybe_summarize(), move_file() (+18 more)

### Community 15 - "ppt_tool"
Cohesion: 0.32
Nodes (8): _corner_L(), PresentationBuilder, Fluid split layout that adapts natively to image aspect ratio: • Landscape…, Draw 4 L-shaped corner brackets., _rect(), _round(), _tb(), test_builder()

### Community 16 - "assignment_answers.py"
Cohesion: 0.12
Nodes (25): _ask_question_on_page(), _find_input(), generate_answer(), generate_answers(), _get_persistent_page(), _groq_answer(), Jarvis Assignment Tool — Phase 2: Answer Generation…, Launch a visible (non-headless) Chromium with a persistent profile. Login… (+17 more)

### Community 17 - "resume_detector"
Cohesion: 0.18
Nodes (14): detect_resume_intent(), _extract_task_resource(), _find_best_task_match(), _has_continuation_verb(), _has_fresh_task_indicator(), _has_reference_phrase(), resume_detector.py — Jarvis Resume Intent Classifier…, Return True if the text contains a strong resume-intent reference phrase. (+6 more)

### Community 18 - "fontmatch.py"
Cohesion: 0.08
Nodes (26): all_faces(), _core_norm(), FontMatcher, identify(), ndarray, fontmatch.py — Font identification against the local library (fonts.py), all in…, Scale so the stroke cores read 1.0 (same rule as the JS side: mean of values…, Reference intensity map (0 = background, 1 = text colour) of a line's ink box… (+18 more)

### Community 19 - "prompt_enhancer_button.py"
Cohesion: 0.08
Nodes (33): _acquire_single_instance(), _app_title_match(), _browser_url(), classify_app(), _exe_name(), _has_pattern(), install_autostart(), _is_editable() (+25 more)

### Community 20 - "generate_deck"
Cohesion: 0.18
Nodes (15): _content_prompt(), _flatten(), generate_deck(), _is_note(), run(), take(), interpret_image_instructions(), _outline_prompt() (+7 more)

### Community 21 - "keyword_detect_tool"
Cohesion: 0.06
Nodes (39): _clean_yt_query(), detect_note_intent(), keyword_detect_tool(), _semantic_window_adjust(), _named_app(), spotify' / 'youtube' if the sentence names a player, else '' (= whatever is…, Fast, 100% reliable keyword-based tool detection. Runs BEFORE the LLM router to…, Remove trailing action phrases from a YouTube search query. (+31 more)

### Community 22 - "ppt_research"
Cohesion: 0.11
Nodes (36): ground_slides(), plan_queries(), 4-6 web queries covering the angles a deck on `topic` needs. Templates, not an…, Web + Wikipedia → verified facts. [] when offline (the deck is then written…, Audit every generated slide; LLM-repair flagged ones with their facts; scrub…, research_facts(), allowed_numbers(), _anchors() (+28 more)

### Community 23 - "ppt_template"
Cohesion: 0.06
Nodes (57): Edge-energy profile along an axis ('x' or 'y') for smart cropping., _saliency_profile(), analyze_format(), _analyze_slide(), classify_box(), _clear(), clone_slide(), delete_slide() (+49 more)

### Community 24 - "main"
Cohesion: 0.20
Nodes (12): post, Arm the acoustic tripwire so double-claps wake Jarvis., Disarm the acoustic tripwire (engine keeps running, just paused)., Schedule an ambient-noise recalibration pass. The engine samples the mic for ~2…, Upload a file to the data/uploads folder for Jarvis to process., tripwire_calibrate(), tripwire_disable(), tripwire_enable() (+4 more)

### Community 25 - "ppt_router"
Cohesion: 0.15
Nodes (18): build_ppt(), create_ppt_backend(), generate(), extract_theme(), get_styles(), PPTBuildRequest, PPTCreateRequest, PPTExtractThemeRequest (+10 more)

### Community 26 - "package"
Cohesion: 0.11
Nodes (20): name, private, type, version, autoprefixer, eslint, ref_eslint_config, @eslint/js (+12 more)

### Community 28 - "orchestrator.py"
Cohesion: 0.09
Nodes (33): resume_replica — Scene-graph-based resume replication engine. Import the public…, build_replica(), compile_replica_html(), _compute_fit_scale(), create_replica_resume(), _data_uri(), _design_with_replica(), orchestrator.py — Main pipeline for replica resume creation. The public API:… (+25 more)

### Community 29 - "ppt_image_engine"
Cohesion: 0.16
Nodes (18): build_image_descriptors(), _extract_keywords(), get_aspect_ratio(), ImageDescriptor, match_images_to_slides(), _parse_slide_ref(), _parse_slide_ref_by_title(), ppt_image_engine.py — Semantic Image-Slide Matcher for JARVIS PPT Engine… (+10 more)

### Community 30 - "test_task_resumption.py"
Cohesion: 0.13
Nodes (20): _ensure_ledger_file(), find_resumable_task(), get_recent_tasks(), get_recent_tasks_raw(), get_task_ledger_for_prompt(), _load_ledger(), log_task(), task_ledger.py — Jarvis Task Context Ledger… (+12 more)

### Community 31 - "ppt_composer + ppt_designer"
Cohesion: 0.10
Nodes (55): _balanced_rows(), _body_cards(), _body_fields(), _body_list(), _body_paragraph(), _body_stats(), _body_steps(), _body_table() (+47 more)

### Community 32 - "dsa_enforcer"
Cohesion: 0.28
Nodes (4): _cache_set(), DSAEnforcer, Write to Neural Cache, silently skipping if unavailable., Flow

### Community 33 - "ppt_content.py"
Cohesion: 0.08
Nodes (46): apply_edit(), apply_structure(), _as_dated(), _as_stat(), _budget_left(), _clauses(), _compact(), _edit_facts() (+38 more)

### Community 34 - "memory_tool.py"
Cohesion: 0.11
Nodes (26): _ensure_memory_file(), forget_fact(), _fuzzy_match_topics(), get_all_facts_as_context(), get_morning_brief(), _load_memory(), memory_tool.py — Jarvis Persistent Memory (Step 10 — ENHANCED)…, Replace an existing fact with an updated version. (+18 more)

### Community 36 - "ui_inspector"
Cohesion: 0.10
Nodes (11): Walk all descendants looking for any control whose window_text contains `text`…, Fire an element's primary action via UIA Invoke pattern. No mouse movement —…, Inject text into an input element via UIA Value pattern. No simulated…, Read text from an element via UIA TextPattern or window_text. Returns empty…, Walk the accessibility tree and return all elements up to `depth` levels. Use…, Core wrapper around pywinauto's UIA backend. All interactions go through the OS…, Get a window wrapper by partial title match (regex-safe). Returns None if not…, Get the currently focused window via Win32 HWND matching. (+3 more)

### Community 37 - "agentic_web.py"
Cohesion: 0.12
Nodes (18): agentic_web_action(), _worker(), _build_search_queries(), _fetch_page_text(), __init__(), _get_api_key(), agentic_web.py — Smart Web Research Engine for Jarvis…, Download a page and return clean readable text (no HTML tags). (+10 more)

### Community 38 - "exact_render.py"
Cohesion: 0.16
Nodes (34): _abs_text(), _bar_grid_html(), _chips_html(), _contact_html(), _content_html(), _face_pos(), _fix_bar_rows(), _glyph() (+26 more)

### Community 39 - "pipeline.py"
Cohesion: 0.11
Nodes (25): load_spec(), run(), _align(), analyse_reference(), line_box(), _choose_families(), best_in(), total() (+17 more)

### Community 40 - "memory/memory.py"
Cohesion: 0.21
Nodes (10): format_preferences_for_prompt(), get_all_preferences(), Jarvis Vector Memory — ChromaDB-based long-term memory engine. Stores and…, Returns a string suitable for injecting into LLM prompts., Stable short ID based on content hash., Return all stored preferences as a plain dict., _uid(), chromadb (+2 more)

### Community 42 - "create_resume"
Cohesion: 0.11
Nodes (26): _apply_layout_hint(), _attachments(), create_resume(), detect_resume_request(), _face_ratio(), _has_details(), _load_state(), open_resume_editor() (+18 more)

### Community 43 - "air-drawing + air_drawing_tool"
Cohesion: 0.18
Nodes (9): open_air_drawing(), Opens the Air Drawing Canvas on the screen. This feature allows the user to…, Air drawing (webcam hand drawing), Files & symbols (auto-generated, line numbers are current), Flow, Gotchas, Graphify, Purpose (+1 more)

### Community 44 - "ppt_designer"
Cohesion: 0.09
Nodes (26): _best_window(), E(), gradient_box(), _line_factor(), line_shape(), _pil_font(), place_image(), ppt_designer.py — Adaptive Design Engine (PPT v6)… (+18 more)

### Community 45 - "voice.py"
Cohesion: 0.08
Nodes (36): devanagari_to_hinglish(), Romanize a Devanagari (Hindi) transcript for the backend, keeping any Latin…, _clean_transcript(), Clip, _finish(), _get_groq(), _groq_once(), groq_stt_available() (+28 more)

### Community 46 - "package + App"
Cohesion: 0.16
Nodes (11): App(), ChatMessage(), API_BASE, frontend_src_index, lucide-react, react, ref_react_dom_client, react-markdown (+3 more)

### Community 47 - "acoustic_tripwire"
Cohesion: 0.05
Nodes (30): AcousticWakeEngine, calibrate_tripwire(), _generate_chime(), get_wake_event(), _play_chime(), ndarray, Background thread that watches the microphone for a double-clap pattern. Usage…, Start the background listening thread. (+22 more)

### Community 48 - "assignment_humanizer"
Cohesion: 0.12
Nodes (25): _extract_output_text(), _fill_input(), _find_element(), _get_browser_page(), humanize_all_answers(), _humanize_chunk_via_browser(), humanize_text(), _humanize_via_browser() (+17 more)

### Community 49 - "pyautogui"
Cohesion: 0.10
Nodes (17): _focus_or_open_whatsapp(), open_whatsapp(), WhatsApp Windows Desktop App Automation Uses the native Windows app via…, Focus the WhatsApp window or open it if not running. Returns True on success., Opens the WhatsApp desktop app., find_controls(), Dump WhatsApp Desktop UI tree to find the Voice Call button name. Run this…, search_tree() (+9 more)

### Community 50 - "client"
Cohesion: 0.10
Nodes (14): Send one of the reply drafts generated by generate_reply_draft. draft_index is…, send_style_reply(), CacheClient, Any, Store a key-value pair, optionally with a TTL. Args: key: Cache key. value:…, Delete a key from the cache. Returns: True if the key existed and was deleted,…, Retrieve server statistics (hit rate, evictions, cache size, etc.). Returns…, Explicitly close the socket connection. (+6 more)

### Community 52 - "calendar_tool.py"
Cohesion: 0.27
Nodes (9): add_event(), check_today_schedule(), _get_calendar_service(), get_upcoming_events(), calendar_tool.py — Jarvis Google Calendar Integration (Step 8)…, Create a new event in Google Calendar. - title: "Project Meeting" - date:…, Authenticate and return a Google Calendar API service object., List events in the next N days. (+1 more)

### Community 53 - "package"
Cohesion: 0.14
Nodes (14): devDependencies, autoprefixer, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, postcss (+6 more)

### Community 55 - "repair"
Cohesion: 0.20
Nodes (6): apply_diff_patches(), _patch_fill(), Converts VLM diffs into structured patches and applies them to the replica_doc.…, Finds the frame with the given ID in the scene graph and updates its fill.…, make_linear_fill(), stops = [{"offset_pct": 0, "color": "#hex"}, {"offset_pct": 100, "color":…

### Community 56 - "llm.py"
Cohesion: 0.07
Nodes (43): classify_context(), detect_language(), context_classifier.py — Jarvis Situational Awareness…, Detect whether the user spoke English, Hinglish, or Hindi. Returns: 'english' —…, Classify the situation from user input. Returns a dict with keys: urgency :…, check_for_tool_intent(), generate_chat_response(), _groq_generate() (+35 more)

### Community 57 - "prompt_enhancement_library + skill_prompt_enhancer"
Cohesion: 0.17
Nodes (19): check_for_hallucination(), clean_output(), detect_domain(), is_bloated(), protect_blocks(), prompt_enhancement_library.py…, Replace ``` fenced blocks with [[BLOCK_n]] placeholders., Put protected blocks back; append any the model dropped. (+11 more)

### Community 58 - "resume_builder.py"
Cohesion: 0.08
Nodes (59): _clean_free(), _competencies_html(), _contact_html(), _css_val(), _custom_section_html(), _data_uri(), _decor_html(), _e() (+51 more)

### Community 59 - "web_search"
Cohesion: 0.18
Nodes (15): research_scraper.py — Autonomous Web Research Scraper…, _duckduckgo_search(), _format_ddg_results(), web_search.py — Jarvis Reliable Web Search (Step 3)…, PRIMARY PUBLIC FUNCTION — used by get_info() in tools.py. Enhanced with: -…, Use a fast LLM call to synthesize multiple search sources into a single…, Search DuckDuckGo using direct HTML scraping (faster, no brittle dependencies).…, Convert DDG result list into a clean readable string for the LLM. (+7 more)

### Community 60 - "content_humanizer"
Cohesion: 0.17
Nodes (21): build_structure_prompt(), build_vocab_prompt(), call_groq(), check_similarity(), detect_tone(), fact_check(), get_groq_client(), get_sentence_scores() (+13 more)

### Community 62 - "Voice: STT, TTS, wake word, clap wake, overlay"
Cohesion: 0.15
Nodes (12): _load_whisper_model(), preload_local_stt(), _load(), Load the local Whisper models in the background (voice agent startup)., Config (`app/core/config.py` + env), Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify (+4 more)

### Community 63 - "PowerPoint generator"
Cohesion: 0.11
Nodes (16): ppt_edit(), Follow-up edit of the last deck (generator). See ppt_studio.edit., _ppt_edit(), Generator wrapper — follow-up edits of the last deck ("on slide 3 …", "make it…, Entry points, Files & symbols (auto-generated, line numbers are current), Flow — edit (`ppt_edit` → `ppt_studio.edit` → `ppt_content.apply_edit`), Graphify (+8 more)

### Community 64 - "whatsapp_smart"
Cohesion: 0.14
Nodes (21): _clear_search(), confirm_whatsapp_send(), _focus_or_open_whatsapp(), _fuzzy_score(), _get_visible_search_results(), _get_whatsapp_window(), open_whatsapp(), whatsapp_smart.py — Jarvis Smart WhatsApp Integration (Fully Isolated)… (+13 more)

### Community 65 - "frontend"
Cohesion: 0.22
Nodes (8): Frontend (`frontend/src`), Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Key behaviour (App.jsx), Purpose, Web UI (React/Vite), DagPlanPanel()

### Community 67 - "Flow — create (`ppt_tool.ppt_create` → `ppt_studio.create`, a generator)"
Cohesion: 0.11
Nodes (28): architect_slides(), ask(), _retry(), run(), _complete_from_source(), deck_facts(), detect_profile(), extractive_ok() (+20 more)

### Community 68 - "spotify_service.py"
Cohesion: 0.05
Nodes (62): app_kind(), control(), run(), _do(), _filter(), kind_playing(), _label(), media_command() (+54 more)

### Community 69 - "prompt_enhancer_button"
Cohesion: 0.14
Nodes (4): EnhanceButton, Move (and optionally show) without ever activating the window; Tk's deiconify()…, Default spot: just above the prompt box's top-right corner; below it or inside…, _save_state()

### Community 70 - "voice"
Cohesion: 0.11
Nodes (12): hinglish_to_devanagari(), Rewrite the Hindi words of a romanized Hinglish sentence in Devanagari, leaving…, Channel, _norm_words(), The speech stream of one command's reply., Plays sentences from many Channels without overlap: - urgent phrases (acks,…, Barge-in "stop": silence now and drop everything queued., Did the mic just hear Jarvis himself (speaker → mic bleed)? Echo comes back… (+4 more)

### Community 72 - "tool-registry"
Cohesion: 0.29
Nodes (6): Adding a tool (checklist), Calling tools from code, Files & symbols (auto-generated, line numbers are current), Graphify, Purpose, Tool registry & adding tools

### Community 73 - "test_lru"
Cohesion: 0.20
Nodes (5): Accessing 'a' should move it to MRU and save it from eviction., Re-setting an existing key should move it to MRU., len(cache.map) must never exceed capacity., Fill to capacity+1. The first key inserted (LRU) should be evicted., TestEviction

### Community 74 - "render_replica_html"
Cohesion: 0.12
Nodes (15): _bg_grid(), canon_title(), _est_height(), _has(), _place_sections(), bottom(), Coarse RGB grid of both background plates (for the contrast guard)., Per column: [(ref_section or template section, content key, title,… (+7 more)

### Community 75 - "refresh_docs"
Cohesion: 0.27
Nodes (10): fnmatch, auto_block(), _js_symbols(), label_communities(), Path, _py_symbols(), refresh_docs.py — keep docs/features/*.md and the graphify graph in sync with…, Name each graph community after its dominant source file(s) (no LLM). (+2 more)

### Community 76 - "reply_generator.py"
Cohesion: 0.11
Nodes (23): generate_reply_draft(), Read the latest WhatsApp thread with a contact and generate 3 reply drafts that…, _build_system_prompt(), _build_user_prompt(), _call_groq(), generate_reply_draft(), get_cached_contact(), get_cached_drafts() (+15 more)

### Community 77 - "Element"
Cohesion: 0.12
Nodes (3): Element, Minimal pywinauto-style wrapper around an IUIAutomationElement., Rect

### Community 78 - "engine.py"
Cohesion: 0.08
Nodes (19): engine.py — Single-Writer Command Queue (Milestone 3)…, Path, Flush and close the file handle cleanly on server shutdown., Manages periodic full-state snapshots. The snapshot itself is triggered through…, Append-only write-ahead log. Each SET/DEL command is written as a JSON line…, Empty the WAL file after a successful snapshot. We truncate (overwrite with…, SnapshotManager, WALWriter (+11 more)

### Community 79 - "Flow (`scripts/voice_agent.py`)"
Cohesion: 0.25
Nodes (6): language_mismatch(), True if a reply sentence is in the other language than the one the user spoke., Loudest output RMS in the last `window` s — the voice agent's echo reference., Strict check used when there is no wake word to vouch for the audio., Flow (`scripts/voice_agent.py`), _is_stop()

### Community 80 - "package"
Cohesion: 0.22
Nodes (9): dependencies, framer-motion, lucide-react, react, react-dom, react-markdown, react-syntax-highlighter, remark-gfm (+1 more)

### Community 81 - "handTracking"
Cohesion: 0.31
Nodes (3): CameraView(), getHandsConstructor(), HandTracker

### Community 82 - "chat.py"
Cohesion: 0.08
Nodes (32): chat_endpoint(), _dag_stream_with_history(), planner_stream(), response_stream_with_history(), resume_stream(), tool_stream(), ChatRequest, clear_history() (+24 more)

### Community 83 - "screen_vision.py"
Cohesion: 0.05
Nodes (60): _accessibility_tree(), describe_screen_for_llm(), get_screen_screenshot_b64(), _groq_vision_screen(), _init_tesseract(), _ocr_screen(), screen_reader.py — Jarvis Screen Vision (VLM-first architecture)…, Legacy OCR layer. Works on any app but extracts raw text only — no layout,… (+52 more)

### Community 84 - "jarvis_overlay.py"
Cohesion: 0.18
Nodes (7): Image, generate_arc_reactor(), JarvisOverlay, Jarvis Arc Reactor Overlay -------------------------- A floating, always-on-…, Draws a beautiful arc reactor using PIL when no icon file is found., read_state(), tkinter

### Community 85 - "voice_agent.py"
Cohesion: 0.08
Nodes (24): app_services, AsyncClient, difflib, httpx, pyaudio, random, _clean_agentic_line(), extract_wake_word_command() (+16 more)

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

### Community 91 - "measure.py"
Cohesion: 0.12
Nodes (26): analyse(), _cdist(), _get_ocr(), _h_overlap(), _is_upper(), _item_roles(), _letters(), measure_line() (+18 more)

### Community 92 - "repair.py"
Cohesion: 0.10
Nodes (25): compile_replica_html(), Main entry point. Returns a complete HTML document string. content : normalised…, _count_pages_and_fill(), _launch_browser(), renderer.py — Browser rendering and output verification for replica resumes.…, Launches Chromium (or msedge fallback). Same as resume_builder._launch., Uses PyMuPDF (fitz) to count pages and measure fill of last page. Returns…, Extracts PNG previews from the PDF using PyMuPDF. Returns list of PNG file… (+17 more)

### Community 94 - "json"
Cohesion: 0.12
Nodes (11): NLPExtractor, nlp_extractor.py — LLM-Powered Fact & Entity Extractor…, Runs extraction on each scraped source and aggregates the results. Returns a…, research_pipeline.py — End-to-End Autonomous Research Orchestrator…, fastapi_testclient, groq, json, download() (+3 more)

### Community 95 - "editor_save"
Cohesion: 0.18
Nodes (17): _apply_op(), _custom_sections(), editor_save(), undo_id(), _normalise_content(), User-made sections from the editor: {id: custom_N, title, style, items}. Kept…, Fingerprint of what the editor shows; its client-side undo history is only…, Store a whole editor state (before a structural change); returns its id for the… (+9 more)

### Community 96 - "typing"
Cohesion: 0.18
Nodes (13): execute_tool(), BaseModel, post, ToolExecuteRequest, build_prompt(), call_llm(), generate_social_content(), Refine an existing piece of social media content based on user instructions.… (+5 more)

### Community 97 - "youtube_player.py"
Cohesion: 0.07
Nodes (66): element_from_handle(), focused_element(), uia_local.py — thread-safe UI Automation access (helper, not a tool)…, This thread's IUIAutomation (COM initialised for the thread on first use)., uia(), _address_bar_focused(), _address_bar_value(), _clip_get() (+58 more)

### Community 98 - "compiler"
Cohesion: 0.18
Nodes (18): _compile_chart(), _compile_section(), _it(), Simple <ul><li> list of skill names., High-level section renderer. Returns complete HTML for the section (heading +…, Returns data-item attribute string in edit mode, else empty string., Compiles a CHART node to the appropriate skill/language visualisation., Progress bar skills. Supports 2-column CSS grid. (+10 more)

### Community 99 - "compiler"
Cohesion: 0.15
Nodes (14): _compile_image(), _compile_node(), _compile_rule(), _compile_text(), _initials_block(), Returns the initials text for the photo placeholder., Converts a TEXT_STYLE dict to a CSS properties string., Dispatches to the appropriate node compiler based on node['type']. (+6 more)

### Community 100 - "rag_memory.py"
Cohesion: 0.06
Nodes (48): aiomysql, close_mysql(), get_mysql_pool(), init_mysql(), mysql_db.py — Jarvis Async MySQL Connection Pool…, Gracefully close the MySQL connection pool on server shutdown., Return the shared MySQL connection pool, initializing it if needed., Initialize the MySQL connection pool and ensure all required tables exist. Safe… (+40 more)

### Community 101 - "ppt_designer"
Cohesion: 0.29
Nodes (5): _as_plain_content(), _deep_plain(), RGBColor, Last-resort fallback: every word of a composite slide as plain bullets (never…, _rgb()

### Community 102 - "package"
Cohesion: 0.40
Nodes (5): scripts, build, dev, lint, preview

### Community 103 - "schema"
Cohesion: 0.09
Nodes (22): make_chart_node(), make_commands_geometry(), make_radial_fill(), make_repeat_node(), make_ring_spec(), make_rule_node(), make_text_node(), make_text_style() (+14 more)

### Community 105 - "message_reader.py"
Cohesion: 0.15
Nodes (18): _bring_whatsapp_to_front(), _get_whatsapp_window(), _heuristic_parse_ocr_lines(), _parse_uia_message_string(), message_reader.py — Jarvis WhatsApp Intelligence: Message Reader…, Restores and focuses WhatsApp window. Returns True on success., Walks the WhatsApp UIA accessibility tree to extract messages. WhatsApp Desktop…, Parses a raw UIA ListItem Name string into a structured message dict.… (+10 more)

### Community 106 - "ppt_tool"
Cohesion: 0.14
Nodes (21): _auto_select_image_layout(), _bg_fill(), _c(), _detect_purpose(), extract_theme_from_image(), _groq_call(), _normalize_and_recover(), _oval() (+13 more)

### Community 107 - "assignment_pipeline.py"
Cohesion: 0.08
Nodes (34): _browser_thread(), do_assignment(), _find_el(), _get_answer(), _get_browser_ctx(), _groq_answer(), _groq_humanize(), _humanize_browser() (+26 more)

### Community 108 - "resume_builder"
Cohesion: 0.24
Nodes (13): _apply_color(), _contrast(), _css(), _css_extra(), _design_set(), _lum(), _mix(), Make sure colours stay readable and every section has a home. (+5 more)

### Community 109 - "encode_message"
Cohesion: 0.14
Nodes (13): decode_message(), encode_message(), Serialise a dict to the wire format: [4-byte length][UTF-8 JSON body] Args:…, Read exactly one message from a socket, handling partial TCP reads correctly.…, make_fake_socket(), fake_recv(), 1 MB value — tests that the length prefix handles large messages., The fake socket returns 1 byte at a time. _recv_exact must loop until it has… (+5 more)

### Community 110 - "bindings"
Cohesion: 0.20
Nodes (9): format_binding_value(), iter_content_items(), bindings.py — Content binding resolution and editor path mapping. Binding paths…, Iterator for repeat bindings. Yields (index, item) for each item in the list at…, Returns the display title for a section, checking content['section_titles']…, Resolves a binding path against content dict. Returns the value at that path,…, Converts a resolved binding value to a display string. - None / empty string /…, resolve_binding() (+1 more)

### Community 111 - "compiler"
Cohesion: 0.23
Nodes (12): _compile_repeat(), _ef(), Renders a single experience entry (same format as legacy builder's…, Renders a single education entry., Renders a single project entry (same format as legacy builder's _projects_html)., Renders the contact section with icons., Returns escaped text in normal mode, or a contenteditable span in edit mode.…, Compiles a REPEAT node by iterating content[binding] and rendering items. (+4 more)

### Community 112 - "README"
Cohesion: 0.50
Nodes (3): Expanding the ESLint configuration, React Compiler, React + Vite

### Community 119 - "safe_executor.py"
Cohesion: 0.13
Nodes (15): Exception, Safe Code Executor for Jarvis ------------------------------- Runs LLM-…, Restricted open(): blocks writes to system paths., Restricted __import__: blocks dangerous modules., Raised when generated code violates safety constraints., AST visitor that inspects generated code before execution., Parse and walk the AST, raising SecurityError on violations., _safe_import() (+7 more)

### Community 120 - "README"
Cohesion: 0.20
Nodes (9): Architecture, Benchmark, Files, LRU Cache Design, Neural Cache, Persistence, Running, Tests (+1 more)

### Community 122 - "resume_builder + resume-exact-replica"
Cohesion: 0.06
Nodes (41): _analyse_design(), _apply_layout_answer(), _balance_columns(), _closest_preset(), _crop_photo(), _faces(), _grow_photo_box(), _image_b64() (+33 more)

### Community 124 - "_Player"
Cohesion: 0.27
Nodes (3): _Player, One persistent 24 kHz output stream driven by a callback that pulls from a…, Play a clip as it arrives. Returns False if interrupted.

### Community 125 - "resume_builder"
Cohesion: 0.10
Nodes (33): _build_content(), _condense_content(), _content_brief(), _drop_invented(), clean_text(), ok(), _edit_content(), _finalize_content() (+25 more)

### Community 126 - "compiler"
Cohesion: 0.18
Nodes (9): _compile_group(), _e(), Radar/spider chart as inline SVG. 100x100 viewBox, center (50,50), max radius…, Tags where size/opacity indicates level (higher → larger/more saturated)., Renders a single ring/donut chart SVG for a skill., Compiles a GROUP node to a <div>. Used for section headings and composites., _render_radar(), _render_tag_level() (+1 more)

### Community 127 - "test_concurrency"
Cohesion: 0.20
Nodes (8): Lock, 50 concurrent clients, each doing 1000 ops. After completion: - Server still…, The engine should report meaningful stats after the load test., While 10 threads hammer the cache, a separate thread pings repeatedly. All…, One client thread. Performs `ops` random GET/SET/DEL operations. Records any…, TestConcurrency, _ping_loop(), _worker()

### Community 128 - "exact_render"
Cohesion: 0.31
Nodes (3): Line box top → ink top (mm) for a line of style k (half-leading model, line-…, Same for line-height:1 (absolutely positioned header text)., Styles

### Community 129 - "main + screen_vision"
Cohesion: 0.18
Nodes (13): _on_screen_alert(), Stop watcher, acoustic tripwire, and close DB pool cleanly on server shutdown., Callback fired by the background watcher when something notable is detected.…, Start background screen watcher and RAG memory system when the server boots., shutdown_event(), startup_event(), Start the passive background screen watcher. Args: callback: Function called…, Stop the background screen watcher thread cleanly. (+5 more)

### Community 130 - "voice_agent"
Cohesion: 0.12
Nodes (10): AbstractEventLoop, Fixed on 2026-10-01 (voice, round 2), _ClapDetector, _EnergyVAD, ndarray, Queue, Stateful frame-by-frame Silero VAD using the ONNX model bundled with faster-…, Fallback if Silero can't load: adaptive noise floor. (+2 more)

### Community 131 - "resume_router"
Cohesion: 0.25
Nodes (7): get, post, resume_router.py — FastAPI router for the visual resume editor…, resume_editor(), resume_save(), fastapi, fastapi_responses

### Community 132 - "dag_executor.py"
Cohesion: 0.06
Nodes (51): Settings, find_skill(), Persist a successful dynamic skill for future reuse., Returns up to n most relevant saved skills for a given task description. Each…, save_skill(), _call_dag_planner(), DAGNode, _execute_node() (+43 more)

### Community 133 - "ppt_tool"
Cohesion: 0.24
Nodes (6): _parse_bullet(), _parse_card(), Dynamic constraint-based layout engine. Analyses the slide content at runtime…, Clean full grid card without messy overlapping header bands., Safely parse any bullet item into (bold_text, body_text). Handles: proper…, Safely parse a card item into a dict with 'header' and 'bullets'.

### Community 134 - "ppt_tool"
Cohesion: 0.27
Nodes (7): _clean_image_path(), _get_image_aspect_ratio(), _frame(), Render a single image with CONTAIN-FIT (object-fit: contain). The image is…, Pure visual layout for 1–6 images. Grid patterns: 1 image → full-width hero 2…, Returns width / height of image using PIL if available, else 1.78 (16:9), Draws one or multiple premium images intelligently tiled within the bounding…

### Community 135 - "dsa_enforcer"
Cohesion: 0.25
Nodes (7): _cache_del(), get_dsa_enforcer(), Delete from Neural Cache, silently skipping if unavailable., selenium, selenium_webdriver_edge_options, selenium_webdriver_edge_service, webdriver_manager_microsoft

### Community 138 - "browser_mail"
Cohesion: 0.28
Nodes (6): check_emails(), _get_api_key(), list_unread(), browser_mail.py — Standard Browser Mail Automation…, A generic tool to perform any mail task (like sending or reading) by pre-…, smart_mail_action()

### Community 139 - "whatsapp_call"
Cohesion: 0.27
Nodes (10): flow_stream(), _click_voice_call_button(), confirm_whatsapp_call(), _focus_or_open_whatsapp(), _get_whatsapp_window(), initiate_whatsapp_call(), whatsapp_call.py — Jarvis Smart WhatsApp Calling Integration (Fully Isolated)…, Focus the WhatsApp window or open it if not running. Returns True on success. (+2 more)

### Community 140 - "gmail_tool.py"
Cohesion: 0.17
Nodes (19): check_emails(), _decode_body(), _format_date(), get_email_body(), _get_gmail_service(), _get_header(), list_unread(), gmail_tool.py — Jarvis Gmail Integration (Step 5)… (+11 more)

### Community 141 - "prompt_enhancer_button"
Cohesion: 0.21
Nodes (11): _box_contains(), _box_set_value(), _clip_get(), _clip_set(), _ctrl(), _focus(), _focused_text(), _norm() (+3 more)

### Community 142 - "search_site"
Cohesion: 0.13
Nodes (15): Search for a query within a specific website using DuckDuckGo site: operator., Read and extract readable text content from a specific URL., scrape_url_tool(), search_site_tool(), _clean_html_text(), Parse HTML and extract readable text. Removes scripts, styles, navbars,…, PUBLIC TOOL: Read and extract readable text from any URL. Called when user says…, PUBLIC TOOL: Search for a query within a specific website. Uses DuckDuckGo with… (+7 more)

### Community 143 - "hinglish_normalizer.py"
Cohesion: 0.18
Nodes (10): _sub(), loanword_ratio(), normalize_for_tts(), hinglish_normalizer.py — Devanagari Crash Prevention + Text Normalizer…, One Devanagari word → casual Hinglish roman ("चलाओ" → "chalao", "करना" →…, Share of Devanagari words that are English loanwords ("ओपन क्रोम" → 1.0). High…, Transform text so it's safe and natural-sounding for TTS: 1. Replace known…, Markdown → plain speakable text (keeps Devanagari). Also drops URLs and emoji. (+2 more)

### Community 144 - "neural-cache"
Cohesion: 0.25
Nodes (7): Design, Files & symbols (auto-generated, line numbers are current), Graphify, Neural cache (Redis-like LRU server), Purpose, Runtime, Tests

### Community 145 - "voice_agent"
Cohesion: 0.33
Nodes (3): MicListener, Initial ambient noise floor (kept up to date on every non-speech frame)., One 32 ms frame → clap check + VAD state machine → events.

### Community 146 - "thread_extractor.py"
Cohesion: 0.19
Nodes (13): extract_thread(), extract_thread_as_string(), _find_latest_incoming(), _get_current_chat_title(), _group_into_turns(), _open_contact_chat(), thread_extractor.py — Jarvis WhatsApp Intelligence: Thread Extractor…, Merges consecutive messages from the same sender into a single turn. This makes… (+5 more)

### Community 148 - "test_lru"
Cohesion: 0.50
Nodes (3): Return average time per (set + get) operation in microseconds., Per-op time for N=1000 vs N=100000 should be within 3x of each other. If the…, TestO1Timing

### Community 149 - "api/memory.py"
Cohesion: 0.06
Nodes (36): forget_memory(), ForgetRequest, get_history(), ingest_memory(), IngestRequest, memory_stats(), BaseModel, delete (+28 more)

### Community 150 - "test_lru.py"
Cohesion: 0.15
Nodes (8): lru.py — Hand-rolled LRU Cache (Milestone 1)…, large_cache(), fixture, test_lru.py — Unit tests for neural_cache.lru (Milestone 7)…, LRU cache with capacity 3 — easy to reason about eviction., small_cache(), TestSentinels, pytest

### Community 151 - "schema"
Cohesion: 0.25
Nodes (8): make_frame_node(), make_no_fill(), make_padding(), make_path_node(), Returns {"type": "none"}, Returns a complete FRAME node., Returns a complete PATH node., Returns {"top_mm": ..., "right_mm": ..., "bottom_mm": ..., "left_mm": ...}

### Community 152 - "Node"
Cohesion: 0.14
Nodes (8): Node, Any, Serialise the entire live cache to a plain dict. Expired entries are excluded —…, Restore cache state from a snapshot dict (produced by snapshot()). Called once…, Place node at the LRU (least-recently-used) end of the list., A doubly-linked list node holding one cache entry. Attributes: key (str): Cache…, Evict the LRU entry (the node just before the tail sentinel). Returns the…, Return True if this entry has a TTL and it has elapsed.

### Community 153 - "re"
Cohesion: 0.11
Nodes (18): assemble_assignment(), _create_powerpoint(), _create_word_doc(), _parse_qa_json(), Jarvis Assignment Tool — Phase 4: Document Assembly…, Assemble the extracted/humanized questions and answers into a formatted…, Extract and parse the JSON array from the input string., _get_api_key() (+10 more)

### Community 154 - "Entry points"
Cohesion: 0.22
Nodes (10): _hint_text(), _ide_allows(), is_prompt_box(), In IDEs only chat / agent inputs qualify, never the code editor, the terminal,…, Entry points, Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify (+2 more)

### Community 155 - "test_protocol.py"
Cohesion: 0.19
Nodes (10): protocol.py — Wire Protocol for Neural Cache (Milestone 2)…, Loop until exactly n bytes have been read from sock. This is necessary because…, _recv_exact(), make_socket_from_messages(), test_protocol.py — Unit tests for neural_cache.protocol (Milestone 7)…, Encode two separate messages and feed them through the same socket.…, Encode multiple messages and concatenate them into a single stream., TestMultiMessage (+2 more)

### Community 156 - "dsa-mode"
Cohesion: 0.29
Nodes (6): Data, DSA / LeetCode enforcer mode, Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Purpose

### Community 157 - "assignment_tool.py"
Cohesion: 0.12
Nodes (23): _classify_question_type(), _clean_text(), _extract_marks(), _extract_via_llm_text(), _extract_via_vision(), _has_figure_reference(), _parse_llm_json_response(), _pdf_pages_to_images() (+15 more)

### Community 158 - "schema"
Cohesion: 0.33
Nodes (6): make_default_replica_document(), make_page_node(), make_solid_fill(), Returns {"type": "solid", "color": color}, Returns a complete PAGE node., Returns a skeleton replica document with an empty scene graph. The caller is…

### Community 160 - "speak_text"
Cohesion: 0.14
Nodes (10): get_player(), Feed streamed tokens; get back speakable sentences as early as possible., Speak a complete text. All sentences synthesise in parallel, play in order., Speak an async generator of text chunks, sentence by sentence, pipelined., SentenceSplitter, speak_stream(), speak_text(), split_sentences() (+2 more)

### Community 161 - "compiler"
Cohesion: 0.33
Nodes (6): _guess_icon(), _icon_svg(), Renders a single competency as an icon+title+description card., Returns an inline SVG icon using the _ICONS dict., Guesses an icon name from a competency title string., _render_competency_item()

### Community 162 - "Code map"
Cohesion: 0.22
Nodes (8): Backend core & API, Code map, Frontend (`frontend/src`, React 19 + Vite + Tailwind 4), Ignore these (no runtime role), Neural cache (neural_cache/, see its README.md), Scripts, Services (app/services), WhatsApp intelligence (app/services/whatsapp_intelligence)

### Community 163 - "ssml_processor"
Cohesion: 0.33
Nodes (5): add_human_prosody(), ssml_processor.py — Human Prosody Pre-processor…, Add natural speech prosody to plain text. Args: text: Plain text (already…, Remove all SSML tags from text — used when falling back to edge-tts which does…, strip_ssml()

### Community 164 - "schema"
Cohesion: 0.50
Nodes (4): make_image_node(), make_size(), Returns a complete IMAGE node., Returns size dict, only including non-None values.

### Community 165 - "compiler"
Cohesion: 0.67
Nodes (3): _collect_google_fonts(), _walk(), Scans the scene graph and style registry for font families. Returns a Google…

### Community 166 - "schema + bindings"
Cohesion: 0.22
Nodes (7): build_editor_path_map(), Walks the scene graph and builds a map from binding path -> list of node IDs…, collect_bindings(), Depth-first traversal of the scene graph. visitor(node, parent, depth) is…, Returns all unique binding paths referenced in the scene graph. E.g. ["name",…, walk_nodes(), _walk()

### Community 167 - "main"
Cohesion: 0.33
Nodes (6): get_alerts(), get, Frontend polls this endpoint to receive proactive JARVIS screen alerts. e.g.…, Return current acoustic tripwire state for the frontend toggle., read_root(), tripwire_status()

### Community 168 - "ppt_designer + ppt_composer"
Cohesion: 0.33
Nodes (6): image_block(), Boxes for the images at full column width in exactly `rows` rows (scaled down…, _justified_fixed(), justified_rows(), Google-Photos-style justified layout. Returns list of (x, y, w, h) relative to…, Justified layout with an exact number of rows (top-aligned). None if impossible.

### Community 169 - "ppt_studio"
Cohesion: 0.33
Nodes (4): _assign_images(), Put each image on its best slide. Explicit instructions win. Mutates deck;…, Move images off slides whose layout can't show them (or has too many) onto…, _rebalance()

### Community 170 - "whatsapp"
Cohesion: 0.33
Nodes (5): Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Purpose, WhatsApp: send, call, read, reply-style cloning

### Community 171 - "Any"
Cohesion: 0.22
Nodes (5): Any, Serialise cache state to disk and truncate the WAL. Called by CacheEngine on…, Load the snapshot from disk. Returns None if no snapshot exists yet. Called…, Append one command to the WAL and flush immediately. Flushing on every write is…, Read and parse all commands from the WAL file. Called once at startup for…

### Community 172 - "Content humanizer & social content"
Cohesion: 0.29
Nodes (6): Content humanizer & social content, Files & symbols (auto-generated, line numbers are current), Graphify, Purpose, Related, Social content (`social_content_manager`)

### Community 173 - "os"
Cohesion: 0.06
Nodes (33): acoustic_tripwire.py — Jarvis Acoustic Wake Engine…, media_state.py — which media app the user used last (Spotify or YouTube)…, main(), prompt_overlay.py ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Jarvis…, fonts.py — Local font library + font identification for exact resume…, argparse, glob, html (+25 more)

### Community 174 - "Dark image/video enhancement"
Cohesion: 0.40
Nodes (4): Dark image/video enhancement, Files & symbols (auto-generated, line numbers are current), Graphify, Purpose

### Community 175 - "Fixed on 2026-09-28"
Cohesion: 0.09
Nodes (21): _media_compound(), _media_target(), Which player an ambiguous media command ("pause it", "next song") is for: named…, Re-target an unspecific media intent (pause/next/play X) to the given platform., "close this song and play shape of you", "pause the video then open mrbeast's…, _to_platform(), create_folder(), Create a new folder. Supports path shortcuts (Desktop, Downloads, etc.).… (+13 more)

### Community 178 - "ppt_tool"
Cohesion: 0.50
Nodes (4): compute_split_geometry(), Computed image + text zone dimensions (in EMU — python-pptx native)., Dynamically compute left-text / right-image split geometry. The split ratio…, SlotGeometry

### Community 179 - "ppt_tool + ppt_router"
Cohesion: 0.67
Nodes (3): generate(), _pick(), Intelligently pick a palette based on the presentation topic.

## Knowledge Gaps
- **165 isolated node(s):** `Settings`, `name`, `private`, `version`, `type` (+160 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1602 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **30 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Tool registry` connect `Tool registry` to `dark_enhancement.py`, `window_layout.py`, `youtube_control.py`, `syllabus_auditor`, `browser_mail`, `whatsapp_call`, `browser_tool.py`, `file_ops.py`, `search_site`, `assignment_answers.py`, `keyword_detect_tool`, `api/memory.py`, `re`, `test_task_resumption.py`, `memory_tool.py`, `agentic_web.py`, `create_resume`, `air-drawing + air_drawing_tool`, `Fixed on 2026-09-28`, `assignment_humanizer`, `calendar_tool.py`, `PowerPoint generator`, `whatsapp_smart`, `spotify_service.py`, `chat.py`, `typing`, `rag_memory.py`, `assignment_pipeline.py`?**
  _High betweenness centrality (0.125) - this node is a cross-community bridge._
- **Why does `open_air_drawing()` connect `air-drawing + air_drawing_tool` to `Tool registry`?**
  _High betweenness centrality (0.086) - this node is a cross-community bridge._
- **Are the 122 inferred relationships involving `Tool registry` (e.g. with `keyword_detect_tool()` and `_media_compound()`) actually correct?**
  _`Tool registry` has 122 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `chat_endpoint()` (e.g. with `describe_screen_for_llm()` and `get_screen_text_summary()`) actually correct?**
  _`chat_endpoint()` has 8 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Settings`, `name`, `private` to the rest of the system?**
  _165 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Tool registry` be split into smaller, more focused modules?**
  _Cohesion score 0.022075716711617222 - nodes in this community are weakly interconnected._
- **Should `style_profiler.py` be split into smaller, more focused modules?**
  _Cohesion score 0.11904761904761904 - nodes in this community are weakly interconnected._