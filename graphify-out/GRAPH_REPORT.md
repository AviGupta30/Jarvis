# Graph Report - Jarvis  (2026-10-04)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 3814 nodes · 8254 edges · 176 communities (153 shown, 23 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 809 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e305648d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- tools + window_layout
- style_profiler
- analyzer
- plate
- ppt_chart_engine
- dark_enhancement + dark_video_enhancement
- resume_builder
- resume_builder + resume-creator
- youtube_control
- syllabus_auditor
- ppt_studio + ppt_designer
- ppt_designer
- browser_tool
- lru
- file_ops
- ppt_tool
- assignment_answers
- memory_tool + memory
- fontmatch + fonts
- prompt_enhancer_button
- ppt_content
- CLAUDE + agents
- ppt_research
- ppt_template
- reply_generator
- ppt_router + resume_router
- package
- gestureController + gestureInterpreter
- orchestrator + renderer
- ppt_image_engine
- task_ledger + resume_detector
- ppt_composer + ppt_designer
- dsa_enforcer
- ppt_content
- gmail_tool
- prompt_overlay
- ui_inspector
- agentic_web
- exact_render
- pipeline
- memory + tools
- transformEngine
- resume_builder + integrate
- air-drawing + air_drawing_tool
- ppt_designer
- voice
- package + App
- acoustic_tripwire
- llm-personality + ARCHITECTURE
- screen_vision
- client
- interactionEngine + DrawingCanvas
- calendar_tool + email-calendar
- package
- strokeManager
- resume_builder
- llm + context_classifier
- prompt_enhancement_library + skill_prompt_enhancer
- resume_builder
- web_search + tools
- content_humanizer + content-tools
- tools + ui_inspector
- voice + context_classifier
- ppt + KNOWN_ISSUES
- whatsapp_smart
- frontend
- shapeManager
- ppt_content
- spotify_service + media_sessions
- prompt_enhancer_button
- voice
- drawingEngine
- assignment_tool + assignment
- test_lru
- voice
- assignment_humanizer
- storage
- uia_local
- server + persistence
- thread_extractor
- package
- handTracking
- chat + youtube_control
- screen_reader
- dump_wa_ui + find_call_btn
- voice_agent
- ControlPanel + HandSkeleton
- strokeRefiner
- ppt_chart_engine
- compiler
- ingest
- measure
- repair
- research_scraper + nlp_extractor
- assignment_humanizer
- jarvis_overlay + prompt_overlay
- youtube_player
- compiler
- compiler
- rag_memory + mysql_db
- ppt_designer
- package
- schema
- screen-vision + screen_vision
- message_reader
- ppt_tool
- assignment_pipeline
- tool-registry + tools
- test_protocol + engine
- bindings
- compiler
- README
- whatsapp
- __init__
- README
- safe_executor
- README + tools
- PROMPT_TEMPLATE
- resume_builder + resume-exact-replica
- FEATURES
- voice
- resume_builder
- compiler
- os-control
- schema
- main
- voice_agent
- refresh_docs
- dag_executor + dynamic_skill
- test_concurrency
- chat
- prompt_enhancer_button
- edge_tts
- pygame
- browser_mail
- whatsapp_call
- vector_store + database
- prompt_enhancer_button
- dsa_enforcer
- hinglish_normalizer
- neural-cache
- voice_agent
- schema
- plate
- dsa-mode
- memory + tool_runner
- test_lru
- schema
- main + screen_vision
- assignment_assembler + smart_navigator
- prompt_enhancer_button + prompt-enhancer
- ppt_designer + ppt_composer
- ppt_studio
- assignment_tool
- screen_reader + screen_vision
- ssml_processor
- voice + tools
- compiler
- CODEMAP
- fontmatch
- schema
- compiler
- schema + bindings
- main + screen_vision
- ppt_tool
- tools + ui_inspector
- whatsapp
- persistence
- ppt_tool
- benchmark
- schema
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
10. `create_resume()` - 32 edges

## Surprising Connections (you probably didn't know these)
- `Entry points` --references--> `PresentationBuilder`  [INFERRED]
  docs/features/ppt.md → app/services/ppt_tool.py
- `HTTP endpoints` --references--> `init_rag_memory()`  [INFERRED]
  docs/ARCHITECTURE.md → app/services/rag_memory.py
- `Tool registry` --references--> `initiate_whatsapp_call()`  [INFERRED]
  docs/TOOLS.md → app/services/whatsapp_call.py
- `Flow` --references--> `get_dsa_enforcer()`  [INFERRED]
  docs/features/dsa-mode.md → app/services/dsa_enforcer.py
- `Gotchas` --references--> `recall_memory()`  [INFERRED]
  docs/features/memory.md → app/api/memory.py

## Import Cycles
- None detected.

## Communities (176 total, 23 thin omitted)

### Community 0 - "tools + window_layout"
Cohesion: 0.03
Nodes (109): media_state.py — which media app the user used last (Spotify or YouTube)…, True if the Spotify desktop app has a window (cheap: EnumWindows, no UIA)., spotify_running(), append_to_file(), calculate(), close_specific_window(), close_sticky_notes(), close_tab() (+101 more)

### Community 1 - "style_profiler"
Cohesion: 0.12
Nodes (27): build_style_profile(), One-time training: parse a WhatsApp .txt chat export to build your personal…, add_deflection_phrase(), build_style_profile(), _compute_profile_stats(), _empty_profile(), get_profile(), get_profile_summary() (+19 more)

### Community 2 - "analyzer"
Cohesion: 0.10
Nodes (50): _file_hash(), _gemini(), _groq(), _hex(), _parse_json(), Fallback when Groq is rate-limited (its vision model has a 200k tokens/DAY cap)., _vision(), analyze_reference() (+42 more)

### Community 3 - "plate"
Cohesion: 0.09
Nodes (43): contact_type(), _hex(), background_mask(), _bg_model(), _bgr(), build(), comps_in(), _chip_gap() (+35 more)

### Community 4 - "ppt_chart_engine"
Cohesion: 0.12
Nodes (34): _bg_color(), _extract_strict_metric(), _fig_to_bytes(), _hex(), _metrics_to_bar(), _palette_colors(), ppt_chart_engine.py — Dynamic Data-Visualization Engine for JARVIS PPT…, Horizontal or vertical bar chart. (+26 more)

### Community 5 - "dark_enhancement + dark_video_enhancement"
Cohesion: 0.13
Nodes (23): _apply_gamma(), _fusion_and_polish(), get_all_enhancements(), _normalize_to_8bit(), _path_1_retinex(), _path_2_wavelet(), ndarray, run_pipeline_a() (+15 more)

### Community 6 - "resume_builder"
Cohesion: 0.10
Nodes (27): _clean_free(), _css_val(), _data_uri(), _design_set(), _editor_meta(), shown(), _effective_design(), _free_html() (+19 more)

### Community 7 - "resume_builder + resume-creator"
Cohesion: 0.10
Nodes (26): _analyse_design(), _apply_layout_answer(), _closest_preset(), _crop_photo(), _grow_photo_box(), _image_b64(), _merge_design(), _palette() (+18 more)

### Community 8 - "youtube_control"
Cohesion: 0.09
Nodes (42): _dur_to_sec(), _end_session(), _fetch_results(), _find_channel(), _find_channel_at(), walk(), _format_results(), _initial_data() (+34 more)

### Community 9 - "syllabus_auditor"
Cohesion: 0.07
Nodes (41): _approx_token_count(), _assemble_response(), audit_playlist_syllabus(), _build_vector_store(), _chunk_transcript(), _coverage_level(), _embed_texts(), _extract_playlist_id() (+33 more)

### Community 10 - "ppt_studio + ppt_designer"
Cohesion: 0.09
Nodes (41): Separate the user's command, any pasted/attached content and attachment paths., [(n, heading, raw content)] split on 'Slide N:' markers of repaired text., raw_slide_blocks(), split_request(), _finish_theme(), _lum(), prepare_image(), Convert a legacy ppt_tool palette (bg/card/text/sub/ac1..) into a theme. (+33 more)

### Community 11 - "ppt_designer"
Cohesion: 0.14
Nodes (21): _compact_header(), box(), DeckRenderer, fit_size(), _items(), para_h(), Header + lead + list inside a column. Returns nothing., Portrait/square image as a full-height panel flush to one edge. (+13 more)

### Community 12 - "browser_tool"
Cohesion: 0.15
Nodes (26): browse_and_paginate(), browse_and_read(), _clean_text(), click_element(), _ensure_url(), fill_form(), _llm_extract(), _new_browser_page() (+18 more)

### Community 13 - "lru"
Cohesion: 0.09
Nodes (19): LRUCache, Node, Any, Insert or update a key-value pair. - If key already exists: update value + TTL,…, Remove a key from the cache. Returns True if the key existed, False if it was…, Serialise the entire live cache to a plain dict. Expired entries are excluded —…, Restore cache state from a snapshot dict (produced by snapshot()). Called once…, Place node at the MRU (most-recently-used) end of the list. (+11 more)

### Community 14 - "file_ops"
Cohesion: 0.10
Nodes (29): append_file(), bulk_rename(), create_folder(), delete_file(), diff_files(), _fmt_size(), list_directory(), _maybe_summarize() (+21 more)

### Community 15 - "ppt_tool"
Cohesion: 0.18
Nodes (19): _clean_image_path(), _get_image_aspect_ratio(), _oval(), _parse_bullet(), _parse_card(), PresentationBuilder, _frame(), Render a single image with CONTAIN-FIT (object-fit: contain). The image is… (+11 more)

### Community 16 - "assignment_answers"
Cohesion: 0.12
Nodes (25): _ask_question_on_page(), _find_input(), generate_answer(), generate_answers(), _get_persistent_page(), _groq_answer(), Jarvis Assignment Tool — Phase 2: Answer Generation…, Launch a visible (non-headless) Chromium with a persistent profile. Login… (+17 more)

### Community 17 - "memory_tool + memory"
Cohesion: 0.14
Nodes (22): _ensure_memory_file(), forget_fact(), _fuzzy_match_topics(), get_all_facts_as_context(), _load_memory(), memory_tool.py — Jarvis Persistent Memory (Step 10 — ENHANCED)…, Replace an existing fact with an updated version., Remove all facts under a topic. (+14 more)

### Community 18 - "fontmatch + fonts"
Cohesion: 0.10
Nodes (23): all_faces(), FontMatcher, identify(), fontmatch.py — Font identification against the local library (fonts.py), all in…, One warm Chromium page with the whole font library loaded. Use as a context…, samples: [{text, ref, rw, rh, src_h}] (see ref_map). Returns per sample a…, items: [{text, family, weight, ls}] → font/ink metrics in em (for the CSS half-…, Runs in a separate process: jobs = [(sample, candidates, top_k)] → result lists. (+15 more)

### Community 19 - "prompt_enhancer_button"
Cohesion: 0.10
Nodes (27): _acquire_single_instance(), _app_title_match(), _browser_url(), classify_app(), _exe_name(), install_autostart(), _load_state(), main() (+19 more)

### Community 20 - "ppt_content"
Cohesion: 0.18
Nodes (15): _content_prompt(), _flatten(), generate_deck(), _is_note(), run(), take(), interpret_image_instructions(), _outline_prompt() (+7 more)

### Community 21 - "CLAUDE + agents"
Cohesion: 0.12
Nodes (15): is_dag_task(), Returns True when the user's request requires a multi-branch DAG plan. More…, Adding / changing a tool (project rules, from JARVIS_ARCHITECTURE.md), /chat request flow (short), Gotchas, graphify, Jarvis — Claude Code guide, Run (+7 more)

### Community 22 - "ppt_research"
Cohesion: 0.11
Nodes (36): ground_slides(), plan_queries(), 4-6 web queries covering the angles a deck on `topic` needs. Templates, not an…, Web + Wikipedia → verified facts. [] when offline (the deck is then written…, Audit every generated slide; LLM-repair flagged ones with their facts; scrub…, research_facts(), allowed_numbers(), _anchors() (+28 more)

### Community 23 - "ppt_template"
Cohesion: 0.06
Nodes (57): Edge-energy profile along an axis ('x' or 'y') for smart cropping., _saliency_profile(), analyze_format(), _analyze_slide(), classify_box(), _clear(), clone_slide(), delete_slide() (+49 more)

### Community 24 - "reply_generator"
Cohesion: 0.11
Nodes (23): generate_reply_draft(), Read the latest WhatsApp thread with a contact and generate 3 reply drafts that…, _build_system_prompt(), _build_user_prompt(), _call_groq(), generate_reply_draft(), get_cached_contact(), get_cached_drafts() (+15 more)

### Community 25 - "ppt_router + resume_router"
Cohesion: 0.08
Nodes (30): build_ppt(), generate(), create_ppt_backend(), generate(), extract_theme(), get_styles(), PPTBuildRequest, PPTCreateRequest (+22 more)

### Community 26 - "package"
Cohesion: 0.11
Nodes (20): name, private, type, version, autoprefixer, eslint, ref_eslint_config, @eslint/js (+12 more)

### Community 28 - "orchestrator + renderer"
Cohesion: 0.07
Nodes (42): compile_replica_html(), Main entry point. Returns a complete HTML document string. content : normalised…, resume_replica — Scene-graph-based resume replication engine. Import the public…, build_replica(), compile_replica_html(), _compute_fit_scale(), create_replica_resume(), _data_uri() (+34 more)

### Community 29 - "ppt_image_engine"
Cohesion: 0.16
Nodes (18): build_image_descriptors(), _extract_keywords(), get_aspect_ratio(), ImageDescriptor, match_images_to_slides(), _parse_slide_ref(), _parse_slide_ref_by_title(), ppt_image_engine.py — Semantic Image-Slide Matcher for JARVIS PPT Engine… (+10 more)

### Community 30 - "task_ledger + resume_detector"
Cohesion: 0.07
Nodes (36): detect_resume_intent(), _extract_task_resource(), _find_best_task_match(), get_resume_context_string(), _has_continuation_verb(), _has_fresh_task_indicator(), _has_reference_phrase(), resume_detector.py — Jarvis Resume Intent Classifier… (+28 more)

### Community 31 - "ppt_composer + ppt_designer"
Cohesion: 0.10
Nodes (55): _balanced_rows(), _body_cards(), _body_fields(), _body_list(), _body_paragraph(), _body_stats(), _body_steps(), _body_table() (+47 more)

### Community 32 - "dsa_enforcer"
Cohesion: 0.28
Nodes (4): _cache_set(), DSAEnforcer, Write to Neural Cache, silently skipping if unavailable., Flow

### Community 33 - "ppt_content"
Cohesion: 0.08
Nodes (46): apply_edit(), apply_structure(), _as_dated(), _as_stat(), _budget_left(), _clauses(), _compact(), _edit_facts() (+38 more)

### Community 34 - "gmail_tool"
Cohesion: 0.11
Nodes (23): check_emails(), _decode_body(), _format_date(), get_email_body(), _get_gmail_service(), _get_header(), list_unread(), gmail_tool.py — Jarvis Gmail Integration (Step 5)… (+15 more)

### Community 36 - "ui_inspector"
Cohesion: 0.10
Nodes (11): Walk all descendants looking for any control whose window_text contains `text`…, Fire an element's primary action via UIA Invoke pattern. No mouse movement —…, Inject text into an input element via UIA Value pattern. No simulated…, Read text from an element via UIA TextPattern or window_text. Returns empty…, Walk the accessibility tree and return all elements up to `depth` levels. Use…, Core wrapper around pywinauto's UIA backend. All interactions go through the OS…, Get a window wrapper by partial title match (regex-safe). Returns None if not…, Get the currently focused window via Win32 HWND matching. (+3 more)

### Community 37 - "agentic_web"
Cohesion: 0.12
Nodes (18): agentic_web_action(), _worker(), _build_search_queries(), _fetch_page_text(), __init__(), _get_api_key(), agentic_web.py — Smart Web Research Engine for Jarvis…, Download a page and return clean readable text (no HTML tags). (+10 more)

### Community 38 - "exact_render"
Cohesion: 0.06
Nodes (67): _abs_text(), _bar_grid_html(), _bg_grid(), canon_title(), _chips_html(), _contact_html(), _content_html(), _est_height() (+59 more)

### Community 39 - "pipeline"
Cohesion: 0.12
Nodes (23): run(), _align(), analyse_reference(), line_box(), _choose_families(), best_in(), total(), _font_styles() (+15 more)

### Community 40 - "memory + tools"
Cohesion: 0.13
Nodes (20): format_preferences_for_prompt(), get_all_preferences(), list_skills(), Jarvis Vector Memory — ChromaDB-based long-term memory engine. Stores and…, Returns a string suitable for injecting into LLM prompts., Stable short ID based on content hash., Persist a successful dynamic skill for future reuse., List all saved skill descriptions. (+12 more)

### Community 42 - "resume_builder + integrate"
Cohesion: 0.08
Nodes (36): _apply_layout_hint(), _attachments(), create_resume(), detect_resume_request(), _has_details(), _is_logo_label(), list_resume_templates(), _load_state() (+28 more)

### Community 43 - "air-drawing + air_drawing_tool"
Cohesion: 0.18
Nodes (9): open_air_drawing(), Opens the Air Drawing Canvas on the screen. This feature allows the user to…, Air drawing (webcam hand drawing), Files & symbols (auto-generated, line numbers are current), Flow, Gotchas, Graphify, Purpose (+1 more)

### Community 44 - "ppt_designer"
Cohesion: 0.09
Nodes (26): _best_window(), E(), gradient_box(), _line_factor(), line_shape(), _pil_font(), place_image(), ppt_designer.py — Adaptive Design Engine (PPT v6)… (+18 more)

### Community 45 - "voice"
Cohesion: 0.08
Nodes (33): loanword_ratio(), Share of Devanagari words that are English loanwords ("ओपन क्रोम" → 1.0). High…, _clean_transcript(), _finish(), _get_groq(), _groq_once(), groq_stt_available(), _load_whisper_model() (+25 more)

### Community 46 - "package + App"
Cohesion: 0.16
Nodes (11): App(), ChatMessage(), API_BASE, frontend_src_index, lucide-react, react, ref_react_dom_client, react-markdown (+3 more)

### Community 47 - "acoustic_tripwire"
Cohesion: 0.07
Nodes (25): AcousticWakeEngine, calibrate_tripwire(), _generate_chime(), get_wake_event(), _play_chime(), ndarray, Background thread that watches the microphone for a double-clap pattern. Usage…, Start the background listening thread. (+17 more)

### Community 48 - "llm-personality + ARCHITECTURE"
Cohesion: 0.11
Nodes (17): detect_note_intent(), _semantic_window_adjust(), _is_complex_response(), Decide whether to use DEEP_MODEL (complex reasoning) vs FAST_MODEL. Complex =…, Architecture, `/chat` pipeline (`app/api/chat.py:chat_endpoint`, L1066), HTTP endpoints, LLM usage (+9 more)

### Community 49 - "screen_vision"
Cohesion: 0.12
Nodes (19): _build_history_context(), _build_system_prompt(), _call_gemini_vision(), _call_gemma_reasoning(), _get_active_process_name(), _get_active_window_title(), Returns the foreground window title using WinAPI., Returns the executable name of the foreground window's process. (+11 more)

### Community 50 - "client"
Cohesion: 0.10
Nodes (14): Send one of the reply drafts generated by generate_reply_draft. draft_index is…, send_style_reply(), CacheClient, Any, Store a key-value pair, optionally with a TTL. Args: key: Cache key. value:…, Delete a key from the cache. Returns: True if the key existed and was deleted,…, Retrieve server statistics (hit rate, evictions, cache size, etc.). Returns…, Explicitly close the socket connection. (+6 more)

### Community 52 - "calendar_tool + email-calendar"
Cohesion: 0.11
Nodes (19): add_event(), check_today_schedule(), _get_calendar_service(), get_upcoming_events(), calendar_tool.py — Jarvis Google Calendar Integration (Step 8)…, Create a new event in Google Calendar. - title: "Project Meeting" - date:…, Authenticate and return a Google Calendar API service object., List events in the next N days. (+11 more)

### Community 53 - "package"
Cohesion: 0.14
Nodes (14): devDependencies, autoprefixer, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, postcss (+6 more)

### Community 55 - "resume_builder"
Cohesion: 0.11
Nodes (31): _apply_op(), _custom_sections(), editor_page(), editor_save(), undo_id(), _editor_toolbar(), _normalise_content(), _raster_palette() (+23 more)

### Community 56 - "llm + context_classifier"
Cohesion: 0.11
Nodes (30): classify_context(), context_classifier.py — Jarvis Situational Awareness…, Classify the situation from user input. Returns a dict with keys: urgency :…, check_for_tool_intent(), generate_chat_response(), _groq_generate(), _is_rate_limit(), _mark_exhausted() (+22 more)

### Community 57 - "prompt_enhancement_library + skill_prompt_enhancer"
Cohesion: 0.17
Nodes (19): check_for_hallucination(), clean_output(), detect_domain(), is_bloated(), protect_blocks(), prompt_enhancement_library.py…, Replace ``` fenced blocks with [[BLOCK_n]] placeholders., Put protected blocks back; append any the model dropped. (+11 more)

### Community 58 - "resume_builder"
Cohesion: 0.13
Nodes (35): _competencies_html(), _contact_html(), _custom_section_html(), _decor_html(), _e(), _education_html(), _experience_html(), _f() (+27 more)

### Community 59 - "web_search + tools"
Cohesion: 0.09
Nodes (32): research_scraper.py — Autonomous Web Research Scraper…, _extract_location(), get_info(), get_weather(), Pulls a clean location name out of a weather query., Get current weather using wttr.in — returns a clean spoken string., Search for a query within a specific website using DuckDuckGo site: operator., Read and extract readable text content from a specific URL. (+24 more)

### Community 60 - "content_humanizer + content-tools"
Cohesion: 0.08
Nodes (35): build_structure_prompt(), build_vocab_prompt(), call_groq(), check_similarity(), detect_tone(), fact_check(), get_groq_client(), get_sentence_scores() (+27 more)

### Community 61 - "tools + ui_inspector"
Cohesion: 0.05
Nodes (41): Resolves site name, opens a VISIBLE browser, and performs a search or action…, smart_web_action(), click_ui_element_uia(), create_word_doc(), dump_app_ui_tree(), get_system_info(), lock_screen(), open_app() (+33 more)

### Community 62 - "voice + context_classifier"
Cohesion: 0.33
Nodes (6): detect_language(), Detect whether the user spoke English, Hinglish, or Hindi. Returns: 'english' —…, language_mismatch(), True if a reply sentence is in the other language than the one the user spoke., Loudest output RMS in the last `window` s — the voice agent's echo reference., Flow (`scripts/voice_agent.py`)

### Community 63 - "ppt + KNOWN_ISSUES"
Cohesion: 0.12
Nodes (14): ppt_edit(), Follow-up edit of the last deck (generator). See ppt_studio.edit., Entry points, Files & symbols (auto-generated, line numbers are current), Flow — edit (`ppt_edit` → `ppt_studio.edit` → `ppt_content.apply_edit`), Graphify, PowerPoint generator, Purpose (+6 more)

### Community 64 - "whatsapp_smart"
Cohesion: 0.13
Nodes (23): _clear_search(), confirm_whatsapp_send(), _focus_or_open_whatsapp(), _fuzzy_score(), _get_visible_search_results(), _get_whatsapp_window(), initiate_whatsapp_send(), open_whatsapp() (+15 more)

### Community 65 - "frontend"
Cohesion: 0.22
Nodes (8): Frontend (`frontend/src`), Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Key behaviour (App.jsx), Purpose, Web UI (React/Vite), DagPlanPanel()

### Community 67 - "ppt_content"
Cohesion: 0.10
Nodes (30): architect_slides(), ask(), _retry(), run(), _complete_from_source(), deck_facts(), detect_profile(), extractive_ok() (+22 more)

### Community 68 - "spotify_service + media_sessions"
Cohesion: 0.06
Nodes (57): app_kind(), control(), run(), _do(), _filter(), kind_playing(), _label(), media_command() (+49 more)

### Community 69 - "prompt_enhancer_button"
Cohesion: 0.14
Nodes (4): EnhanceButton, Move (and optionally show) without ever activating the window; Tk's deiconify()…, Default spot: just above the prompt box's top-right corner; below it or inside…, _save_state()

### Community 70 - "voice"
Cohesion: 0.11
Nodes (12): hinglish_to_devanagari(), Rewrite the Hindi words of a romanized Hinglish sentence in Devanagari, leaving…, Channel, _norm_words(), The speech stream of one command's reply., Plays sentences from many Channels without overlap: - urgent phrases (acks,…, Barge-in "stop": silence now and drop everything queued., Did the mic just hear Jarvis himself (speaker → mic bleed)? Echo comes back… (+4 more)

### Community 72 - "assignment_tool + assignment"
Cohesion: 0.13
Nodes (17): do_assignment(), Master orchestrator. Uses a background thread for all Playwright code. Yields…, extract_questions(), list_assignments(), _merge_and_deduplicate(), Merge questions from all three tracks. Priority: regex > vision > llm text. A…, Extract ALL questions from an assignment PDF using a 3-track hybrid system.…, Resolve PDF path: handles full paths, filenames, partial names. (+9 more)

### Community 73 - "test_lru"
Cohesion: 0.20
Nodes (5): Accessing 'a' should move it to MRU and save it from eviction., Re-setting an existing key should move it to MRU., len(cache.map) must never exceed capacity., Fill to capacity+1. The first key inserted (LRU) should be evicted., TestEviction

### Community 74 - "voice"
Cohesion: 0.12
Nodes (12): Clip, prewarm(), PCM (int16, 24 kHz) that fills while synthesis streams; playable immediately., hi' → Hindi voice, 'en' → English voice, for one sentence., Begin synthesising `text` now; returns a Clip that can be played while it fills., Synthesise short stock phrases (greetings, acks) into the cache for instant…, route_language(), _sapi_sync() (+4 more)

### Community 75 - "assignment_humanizer"
Cohesion: 0.15
Nodes (16): _get_browser_page(), humanize_all_answers(), humanize_text(), _humanize_via_browser(), _humanize_via_llm(), _protect_technical(), Replace technical content with numbered placeholders. Returns (modified_text,…, Restore original technical content from placeholders. (+8 more)

### Community 76 - "storage"
Cohesion: 0.18
Nodes (15): delete_replica_document(), _ensure_dir(), get_document_path(), has_replica_document(), list_replica_documents(), prune_old_documents(), storage.py — Persisting and retrieving replica documents. Replica documents are…, Returns a list of all stored document IDs (filenames without extension). The… (+7 more)

### Community 77 - "uia_local"
Cohesion: 0.12
Nodes (5): Element, focused_element(), uia_local.py — thread-safe UI Automation access (helper, not a tool)…, Minimal pywinauto-style wrapper around an IUIAutomationElement., Rect

### Community 78 - "server + persistence"
Cohesion: 0.05
Nodes (43): acoustic_tripwire.py — Jarvis Acoustic Wake Engine…, screen_vision.py — Jarvis VLM Screen Understanding (Layer 1 Upgrade)…, collections, io, logging, mss, neural_cache, benchmark.py — Neural Cache vs JSON-file Baseline (Milestone 8)… (+35 more)

### Community 79 - "thread_extractor"
Cohesion: 0.16
Nodes (15): Open a WhatsApp chat, read the last N messages, and return a structured thread…, read_whatsapp_thread(), extract_thread(), extract_thread_as_string(), _find_latest_incoming(), _get_current_chat_title(), _group_into_turns(), _open_contact_chat() (+7 more)

### Community 80 - "package"
Cohesion: 0.22
Nodes (9): dependencies, framer-motion, lucide-react, react, react-dom, react-markdown, react-syntax-highlighter, remark-gfm (+1 more)

### Community 81 - "handTracking"
Cohesion: 0.31
Nodes (3): CameraView(), getHandsConstructor(), HandTracker

### Community 82 - "chat + youtube_control"
Cohesion: 0.05
Nodes (54): ChatRequest, _clean_yt_query(), clear_history(), detect_whatsapp_call(), detect_whatsapp_send(), _explicit_platform(), keyword_detect_tool(), _media_compound() (+46 more)

### Community 83 - "screen_reader"
Cohesion: 0.13
Nodes (22): _accessibility_tree(), describe_screen_for_llm(), get_screen_screenshot_b64(), _groq_vision_screen(), _init_tesseract(), _ocr_screen(), screen_reader.py — Jarvis Screen Vision (VLM-first architecture)…, Legacy OCR layer. Works on any app but extracts raw text only — no layout,… (+14 more)

### Community 84 - "dump_wa_ui + find_call_btn"
Cohesion: 0.16
Nodes (11): find_controls(), Dump WhatsApp Desktop UI tree to find the Voice Call button name. Run this…, search_tree(), Find the Voice Call button position in WhatsApp Desktop window. Run this while…, Step 1: Open WhatsApp, go to any chat (e.g. Archit Shukla) Step 2: Hover your…, pyautogui, pygetwindow, pywinauto (+3 more)

### Community 85 - "voice_agent"
Cohesion: 0.08
Nodes (24): app_services, AsyncClient, difflib, httpx, pyaudio, _clean_agentic_line(), extract_wake_word_command(), _is_stop() (+16 more)

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
Cohesion: 0.11
Nodes (29): analyse(), _cdist(), _get_ocr(), _h_overlap(), is_ornament_text(), _is_upper(), _item_roles(), _letters() (+21 more)

### Community 92 - "repair"
Cohesion: 0.20
Nodes (6): apply_diff_patches(), _patch_fill(), Converts VLM diffs into structured patches and applies them to the replica_doc.…, Finds the frame with the given ID in the scene graph and updates its fill.…, make_linear_fill(), stops = [{"offset_pct": 0, "color": "#hex"}, {"offset_pct": 100, "color":…

### Community 94 - "research_scraper + nlp_extractor"
Cohesion: 0.14
Nodes (9): NLPExtractor, Runs extraction on each scraped source and aggregates the results. Returns a…, research_pipeline.py — End-to-End Autonomous Research Orchestrator…, Scrapes the web for a topic and extracts verified facts and statistics. Yields…, research_topic(), Searches DDG for the topic, fetches the top N links concurrently, and returns…, ResearchScraper, Phase 3: Autonomous Research Aggregator. Scrapes live facts from the web,… (+1 more)

### Community 95 - "assignment_humanizer"
Cohesion: 0.24
Nodes (10): _extract_output_text(), _fill_input(), _find_element(), _humanize_chunk_via_browser(), Jarvis Assignment Tool — Phase 3: Answer Humanizer…, Try multiple CSS selectors to find a visible element., Fill an input area with text using the most reliable method available., Extract text from the output area of the humanizer. (+2 more)

### Community 96 - "jarvis_overlay + prompt_overlay"
Cohesion: 0.08
Nodes (21): nlp_extractor.py — LLM-Powered Fact & Entity Extractor…, main(), prompt_overlay.py ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Jarvis…, argparse, dotenv, glob, google_generativeai, html (+13 more)

### Community 97 - "youtube_player"
Cohesion: 0.07
Nodes (73): element_from_handle(), This thread's IUIAutomation (COM initialised for the thread on first use)., uia(), _address_bar_focused(), _address_bar_value(), _clip_get(), _clip_restore(), _clip_set() (+65 more)

### Community 98 - "compiler"
Cohesion: 0.18
Nodes (18): _compile_chart(), _compile_section(), _it(), Simple <ul><li> list of skill names., High-level section renderer. Returns complete HTML for the section (heading +…, Returns data-item attribute string in edit mode, else empty string., Compiles a CHART node to the appropriate skill/language visualisation., Progress bar skills. Supports 2-column CSS grid. (+10 more)

### Community 99 - "compiler"
Cohesion: 0.15
Nodes (14): _compile_image(), _compile_node(), _compile_rule(), _compile_text(), _initials_block(), Returns the initials text for the photo placeholder., Converts a TEXT_STYLE dict to a CSS properties string., Dispatches to the appropriate node compiler based on node['type']. (+6 more)

### Community 100 - "rag_memory + mysql_db"
Cohesion: 0.08
Nodes (38): aiomysql, close_mysql(), get_mysql_pool(), init_mysql(), mysql_db.py — Jarvis Async MySQL Connection Pool…, Gracefully close the MySQL connection pool on server shutdown., Return the shared MySQL connection pool, initializing it if needed., Initialize the MySQL connection pool and ensure all required tables exist. Safe… (+30 more)

### Community 101 - "ppt_designer"
Cohesion: 0.29
Nodes (5): _as_plain_content(), _deep_plain(), RGBColor, Last-resort fallback: every word of a composite slide as plain bullets (never…, _rgb()

### Community 102 - "package"
Cohesion: 0.40
Nodes (5): scripts, build, dev, lint, preview

### Community 103 - "schema"
Cohesion: 0.09
Nodes (21): make_chart_node(), make_group_node(), make_parametric_geometry(), make_radial_fill(), make_repeat_node(), make_ring_spec(), make_rule_node(), make_text_node() (+13 more)

### Community 104 - "screen-vision + screen_vision"
Cohesion: 0.18
Nodes (10): capture_screen_b64(), _pixel_diff_percent(), ndarray, Returns the percentage of pixels that changed significantly between two frames.…, Capture the primary monitor using mss (~10ms). Returns (base64_jpeg_string,…, Config, Files & symbols (auto-generated, line numbers are current), Graphify (+2 more)

### Community 105 - "message_reader"
Cohesion: 0.15
Nodes (18): _bring_whatsapp_to_front(), _get_whatsapp_window(), _heuristic_parse_ocr_lines(), _parse_uia_message_string(), message_reader.py — Jarvis WhatsApp Intelligence: Message Reader…, Restores and focuses WhatsApp window. Returns True on success., Walks the WhatsApp UIA accessibility tree to extract messages. WhatsApp Desktop…, Parses a raw UIA ListItem Name string into a structured message dict.… (+10 more)

### Community 106 - "ppt_tool"
Cohesion: 0.10
Nodes (23): _auto_select_image_layout(), _bg_fill(), _c(), _detect_purpose(), extract_theme_from_image(), _extract_theme_pil_local(), _groq_call(), _normalize_and_recover() (+15 more)

### Community 107 - "assignment_pipeline"
Cohesion: 0.20
Nodes (17): _browser_thread(), _find_el(), _get_answer(), _get_browser_ctx(), _groq_answer(), _groq_humanize(), _humanize_browser(), Queue (+9 more)

### Community 108 - "tool-registry + tools"
Cohesion: 0.18
Nodes (10): _mail_tool(), Email tools: try the real Gmail API (gmail_tool) first, fall back to opening…, Email, Adding a tool (checklist), Calling tools from code, Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify (+2 more)

### Community 109 - "test_protocol + engine"
Cohesion: 0.06
Nodes (36): CacheEngine, Any, Route a command dict to the appropriate handler. All handlers return a response…, Owns the LRUCache. Runs a single consumer loop on a dedicated thread. External…, Spawn the single writer thread. Call once at server boot., Gracefully stop the engine writer thread., The single consumer loop. Runs on CacheEngineThread. Processes one command at a…, decode_message() (+28 more)

### Community 110 - "bindings"
Cohesion: 0.20
Nodes (9): format_binding_value(), iter_content_items(), bindings.py — Content binding resolution and editor path mapping. Binding paths…, Iterator for repeat bindings. Yields (index, item) for each item in the list at…, Returns the display title for a section, checking content['section_titles']…, Resolves a binding path against content dict. Returns the value at that path,…, Converts a resolved binding value to a display string. - None / empty string /…, resolve_binding() (+1 more)

### Community 111 - "compiler"
Cohesion: 0.23
Nodes (12): _compile_repeat(), _ef(), Renders a single experience entry (same format as legacy builder's…, Renders a single education entry., Renders a single project entry (same format as legacy builder's _projects_html)., Renders the contact section with icons., Returns escaped text in normal mode, or a contenteditable span in edit mode.…, Compiles a REPEAT node by iterating content[binding] and rendering items. (+4 more)

### Community 112 - "README"
Cohesion: 0.50
Nodes (3): Expanding the ESLint configuration, React Compiler, React + Vite

### Community 113 - "whatsapp"
Cohesion: 0.22
Nodes (8): _focus_or_open_whatsapp(), open_whatsapp(), WhatsApp Windows Desktop App Automation Uses the native Windows app via…, Focus the WhatsApp window or open it if not running. Returns True on success., Opens the WhatsApp desktop app., Sends a WhatsApp message using the Windows desktop app via keyboard automation.…, send_whatsapp_message(), pyperclip

### Community 119 - "safe_executor"
Cohesion: 0.15
Nodes (14): Exception, Safe Code Executor for Jarvis ------------------------------- Runs LLM-…, Restricted open(): blocks writes to system paths., Restricted __import__: blocks dangerous modules., Raised when generated code violates safety constraints., AST visitor that inspects generated code before execution., Parse and walk the AST, raising SecurityError on violations., _safe_import() (+6 more)

### Community 120 - "README + tools"
Cohesion: 0.13
Nodes (14): cache_get(), cache_set(), Store a key-value pair in Neural Cache (in-memory, O(1) access). Useful for…, Retrieve a value from Neural Cache. Returns the value if found, or a 'not…, Architecture, Benchmark, Files, JARVIS Integration (+6 more)

### Community 122 - "resume_builder + resume-exact-replica"
Cohesion: 0.07
Nodes (38): _apply_color(), _balance_columns(), _contrast(), _css(), _css_extra(), _face_ratio(), _faces(), _lum() (+30 more)

### Community 124 - "voice"
Cohesion: 0.21
Nodes (4): get_player(), _Player, One persistent 24 kHz output stream driven by a callback that pulls from a…, Play a clip as it arrives. Returns False if interrupted.

### Community 125 - "resume_builder"
Cohesion: 0.13
Nodes (26): _build_content(), _condense_content(), _content_brief(), _drop_invented(), clean_text(), ok(), _edit_content(), _finalize_content() (+18 more)

### Community 126 - "compiler"
Cohesion: 0.18
Nodes (9): _compile_group(), _e(), Radar/spider chart as inline SVG. 100x100 viewBox, center (50,50), max radius…, Tags where size/opacity indicates level (higher → larger/more saturated)., Renders a single ring/donut chart SVG for a skill., Compiles a GROUP node to a <div>. Used for section headings and composites., _render_radar(), _render_tag_level() (+1 more)

### Community 127 - "os-control"
Cohesion: 0.40
Nodes (4): Files & symbols (auto-generated, line numbers are current), Graphify, Purpose, Windows/OS control: windows, media, apps, files

### Community 128 - "schema"
Cohesion: 0.33
Nodes (6): make_default_replica_document(), make_page_node(), make_solid_fill(), Returns {"type": "solid", "color": color}, Returns a complete PAGE node., Returns a skeleton replica document with an empty scene graph. The caller is…

### Community 129 - "main"
Cohesion: 0.12
Nodes (21): get_alerts(), get, post, Frontend polls this endpoint to receive proactive JARVIS screen alerts. e.g.…, Return current acoustic tripwire state for the frontend toggle., Arm the acoustic tripwire so double-claps wake Jarvis., Disarm the acoustic tripwire (engine keeps running, just paused)., Schedule an ambient-noise recalibration pass. The engine samples the mic for ~2… (+13 more)

### Community 130 - "voice_agent"
Cohesion: 0.12
Nodes (10): AbstractEventLoop, Fixed on 2026-10-01 (voice, round 2), _ClapDetector, _EnergyVAD, ndarray, Queue, Stateful frame-by-frame Silero VAD using the ONNX model bundled with faster-…, Fallback if Silero can't load: adaptive noise floor. (+2 more)

### Community 131 - "refresh_docs"
Cohesion: 0.27
Nodes (10): fnmatch, auto_block(), _js_symbols(), label_communities(), Path, _py_symbols(), refresh_docs.py — keep docs/features/*.md and the graphify graph in sync with…, Name each graph community after its dominant source file(s) (no LLM). (+2 more)

### Community 132 - "dag_executor + dynamic_skill"
Cohesion: 0.07
Nodes (49): Settings, app_memory, find_skill(), Returns up to n most relevant saved skills for a given task description. Each…, _call_dag_planner(), DAGNode, _execute_node(), dag_executor.py — Jarvis DAG-Based Multi-Step Agent Planner… (+41 more)

### Community 133 - "test_concurrency"
Cohesion: 0.20
Nodes (8): Lock, 50 concurrent clients, each doing 1000 ops. After completion: - Server still…, The engine should report meaningful stats after the load test., While 10 threads hammer the cache, a separate thread pings repeatedly. All…, One client thread. Performs `ops` random GET/SET/DEL operations. Records any…, TestConcurrency, _ping_loop(), _worker()

### Community 134 - "chat"
Cohesion: 0.31
Nodes (9): chat_endpoint(), _dag_stream_with_history(), planner_stream(), response_stream_with_history(), resume_stream(), tool_stream(), post, Call this whenever conversation_history is updated. (+1 more)

### Community 138 - "browser_mail"
Cohesion: 0.24
Nodes (7): check_emails(), _get_api_key(), list_unread(), browser_mail.py — Standard Browser Mail Automation…, A generic tool to perform any mail task (like sending or reading) by pre-…, smart_mail_action(), webbrowser

### Community 139 - "whatsapp_call"
Cohesion: 0.27
Nodes (10): flow_stream(), _click_voice_call_button(), confirm_whatsapp_call(), _focus_or_open_whatsapp(), _get_whatsapp_window(), initiate_whatsapp_call(), whatsapp_call.py — Jarvis Smart WhatsApp Calling Integration (Fully Isolated)…, Focus the WhatsApp window or open it if not running. Returns True on success. (+2 more)

### Community 140 - "vector_store + database"
Cohesion: 0.33
Nodes (7): get_db_pool(), init_db(), Queries the table and uses the pgvector cosine distance operator (<=>) to fetch…, Inserts text chunks and vectors into the knowledge_store table., save_document_chunk(), search_similar_chunks(), asyncpg

### Community 141 - "prompt_enhancer_button"
Cohesion: 0.21
Nodes (11): _box_contains(), _box_set_value(), _clip_get(), _clip_set(), _ctrl(), _focus(), _focused_text(), _norm() (+3 more)

### Community 142 - "dsa_enforcer"
Cohesion: 0.25
Nodes (7): _cache_del(), get_dsa_enforcer(), Delete from Neural Cache, silently skipping if unavailable., selenium, selenium_webdriver_edge_options, selenium_webdriver_edge_service, webdriver_manager_microsoft

### Community 143 - "hinglish_normalizer"
Cohesion: 0.18
Nodes (11): devanagari_to_hinglish(), _sub(), normalize_for_tts(), hinglish_normalizer.py — Devanagari Crash Prevention + Text Normalizer…, One Devanagari word → casual Hinglish roman ("चलाओ" → "chalao", "करना" →…, Romanize a Devanagari (Hindi) transcript for the backend, keeping any Latin…, Transform text so it's safe and natural-sounding for TTS: 1. Replace known…, Markdown → plain speakable text (keeps Devanagari). Also drops URLs and emoji. (+3 more)

### Community 144 - "neural-cache"
Cohesion: 0.25
Nodes (7): Design, Files & symbols (auto-generated, line numbers are current), Graphify, Neural cache (Redis-like LRU server), Purpose, Runtime, Tests

### Community 145 - "voice_agent"
Cohesion: 0.33
Nodes (3): MicListener, Initial ambient noise floor (kept up to date on every non-speech frame)., One 32 ms frame → clap check + VAD state machine → events.

### Community 147 - "plate"
Cohesion: 0.29
Nodes (4): _flat_outside(), _photo_edges(), Frame of the photo: every strong colour edge along 96 rays from the face is a…, Just outside the circle the colour is flat (a ring, frame or background), not…

### Community 148 - "dsa-mode"
Cohesion: 0.29
Nodes (6): Data, DSA / LeetCode enforcer mode, Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Purpose

### Community 149 - "memory + tool_runner"
Cohesion: 0.07
Nodes (36): forget_memory(), ForgetRequest, get_history(), ingest_memory(), IngestRequest, memory_stats(), BaseModel, delete (+28 more)

### Community 150 - "test_lru"
Cohesion: 0.06
Nodes (11): large_cache(), fixture, test_lru.py — Unit tests for neural_cache.lru (Milestone 7)…, Snapshot with more keys than capacity should trigger LRU eviction on load., LRU cache with capacity 3 — easy to reason about eviction., small_cache(), TestBasicOps, TestSentinels (+3 more)

### Community 151 - "schema"
Cohesion: 0.25
Nodes (8): make_frame_node(), make_no_fill(), make_padding(), make_path_node(), Returns {"type": "none"}, Returns a complete FRAME node., Returns a complete PATH node., Returns {"top_mm": ..., "right_mm": ..., "bottom_mm": ..., "left_mm": ...}

### Community 152 - "main + screen_vision"
Cohesion: 0.33
Nodes (6): _on_screen_alert(), Callback fired by the background watcher when something notable is detected.…, Start background screen watcher and RAG memory system when the server boots., startup_event(), Start the passive background screen watcher. Args: callback: Function called…, start_background_watcher()

### Community 153 - "assignment_assembler + smart_navigator"
Cohesion: 0.11
Nodes (18): assemble_assignment(), _create_powerpoint(), _create_word_doc(), _parse_qa_json(), Jarvis Assignment Tool — Phase 4: Document Assembly…, Assemble the extracted/humanized questions and answers into a formatted…, Extract and parse the JSON array from the input string., _get_api_key() (+10 more)

### Community 154 - "prompt_enhancer_button + prompt-enhancer"
Cohesion: 0.16
Nodes (13): _has_pattern(), _hint_text(), _ide_allows(), _is_editable(), is_prompt_box(), Writable text input: <textarea>/<input>/native edit, or a contenteditable…, In IDEs only chat / agent inputs qualify, never the code editor, the terminal,…, Entry points (+5 more)

### Community 155 - "ppt_designer + ppt_composer"
Cohesion: 0.33
Nodes (6): image_block(), Boxes for the images at full column width in exactly `rows` rows (scaled down…, _justified_fixed(), justified_rows(), Google-Photos-style justified layout. Returns list of (x, y, w, h) relative to…, Justified layout with an exact number of rows (top-aligned). None if impossible.

### Community 156 - "ppt_studio"
Cohesion: 0.33
Nodes (4): _assign_images(), Put each image on its best slide. Explicit instructions win. Mutates deck;…, Move images off slides whose layout can't show them (or has too many) onto…, _rebalance()

### Community 157 - "assignment_tool"
Cohesion: 0.12
Nodes (23): _classify_question_type(), _clean_text(), _extract_marks(), _extract_via_llm_text(), _extract_via_vision(), _has_figure_reference(), _parse_llm_json_response(), _pdf_pages_to_images() (+15 more)

### Community 158 - "screen_reader + screen_vision"
Cohesion: 0.33
Nodes (6): Tool-callable version — called when user asks 'what's on my screen?' Routes…, read_screen_as_tool(), _classify_intent(), Parse the user's phrasing to determine the response mode. describe → "What am I…, Read and describe the current screen using the VLM pipeline. Routes to the…, read_my_screen()

### Community 159 - "ssml_processor"
Cohesion: 0.33
Nodes (5): add_human_prosody(), ssml_processor.py — Human Prosody Pre-processor…, Add natural speech prosody to plain text. Args: text: Plain text (already…, Remove all SSML tags from text — used when falling back to edge-tts which does…, strip_ssml()

### Community 160 - "voice + tools"
Cohesion: 0.13
Nodes (14): Sets a reminder that Jarvis will speak after a given number of seconds., set_reminder(), Speak a complete text. All sentences synthesise in parallel, play in order., speak_text(), Config (`app/core/config.py` + env), Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify (+6 more)

### Community 161 - "compiler"
Cohesion: 0.33
Nodes (6): _guess_icon(), _icon_svg(), Renders a single competency as an icon+title+description card., Returns an inline SVG icon using the _ICONS dict., Guesses an icon name from a competency title string., _render_competency_item()

### Community 162 - "CODEMAP"
Cohesion: 0.22
Nodes (8): Backend core & API, Code map, Frontend (`frontend/src`, React 19 + Vite + Tailwind 4), Ignore these (no runtime role), Neural cache (neural_cache/, see its README.md), Scripts, Services (app/services), WhatsApp intelligence (app/services/whatsapp_intelligence)

### Community 163 - "fontmatch"
Cohesion: 0.50
Nodes (5): _core_norm(), ndarray, Scale so the stroke cores read 1.0 (same rule as the JS side: mean of values…, Reference intensity map (0 = background, 1 = text colour) of a line's ink box…, ref_map()

### Community 164 - "schema"
Cohesion: 0.50
Nodes (4): make_image_node(), make_size(), Returns a complete IMAGE node., Returns size dict, only including non-None values.

### Community 165 - "compiler"
Cohesion: 0.67
Nodes (3): _collect_google_fonts(), _walk(), Scans the scene graph and style registry for font families. Returns a Google…

### Community 166 - "schema + bindings"
Cohesion: 0.22
Nodes (7): build_editor_path_map(), Walks the scene graph and builds a map from binding path -> list of node IDs…, collect_bindings(), Depth-first traversal of the scene graph. visitor(node, parent, depth) is…, Returns all unique binding paths referenced in the scene graph. E.g. ["name",…, walk_nodes(), _walk()

### Community 167 - "main + screen_vision"
Cohesion: 0.50
Nodes (4): Stop watcher, acoustic tripwire, and close DB pool cleanly on server shutdown., shutdown_event(), Stop the background screen watcher thread cleanly., stop_background_watcher()

### Community 168 - "ppt_tool"
Cohesion: 0.50
Nodes (4): compute_split_geometry(), Computed image + text zone dimensions (in EMU — python-pptx native)., Dynamically compute left-text / right-image split geometry. The split ratio…, SlotGeometry

### Community 169 - "tools + ui_inspector"
Cohesion: 0.50
Nodes (4): Get all readable text from the currently active window., read_active_window_text(), get_active_window_info(), Returns a text summary of the currently focused window: window title + list of…

### Community 170 - "whatsapp"
Cohesion: 0.33
Nodes (5): Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Purpose, WhatsApp: send, call, read, reply-style cloning

### Community 171 - "persistence"
Cohesion: 0.22
Nodes (5): Any, Serialise cache state to disk and truncate the WAL. Called by CacheEngine on…, Load the snapshot from disk. Returns None if no snapshot exists yet. Called…, Append one command to the WAL and flush immediately. Flushing on every write is…, Read and parse all commands from the WAL file. Called once at startup for…

### Community 173 - "benchmark"
Cohesion: 0.14
Nodes (7): JSONFileBaseline, main(), measure_latency(), measure_throughput(), Spin up n_threads threads each doing ops_per_thread SET+GET pairs. Returns…, Mimics memory_tool.py's approach: every read/write touches disk. Uses a…, Run op_fn warmup times (discard), then timed times (measure). Returns (mean_µs,…

## Knowledge Gaps
- **166 isolated node(s):** `Settings`, `build`, `dev`, `lint`, `preview` (+161 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1626 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **23 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Tool registry` connect `tools + window_layout` to `dark_enhancement + dark_video_enhancement`, `youtube_control`, `syllabus_auditor`, `browser_mail`, `whatsapp_call`, `browser_tool`, `file_ops`, `assignment_answers`, `memory_tool + memory`, `memory + tool_runner`, `assignment_assembler + smart_navigator`, `ppt_router + resume_router`, `task_ledger + resume_detector`, `screen_reader + screen_vision`, `voice + tools`, `agentic_web`, `memory + tools`, `tools + ui_inspector`, `resume_builder + integrate`, `air-drawing + air_drawing_tool`, `calendar_tool + email-calendar`, `web_search + tools`, `content_humanizer + content-tools`, `tools + ui_inspector`, `ppt + KNOWN_ISSUES`, `whatsapp_smart`, `ppt_content`, `spotify_service + media_sessions`, `assignment_tool + assignment`, `assignment_humanizer`, `thread_extractor`, `chat + youtube_control`, `whatsapp`, `README + tools`?**
  _High betweenness centrality (0.139) - this node is a cross-community bridge._
- **Why does `open_air_drawing()` connect `air-drawing + air_drawing_tool` to `tools + window_layout`?**
  _High betweenness centrality (0.100) - this node is a cross-community bridge._
- **Are the 122 inferred relationships involving `Tool registry` (e.g. with `keyword_detect_tool()` and `_media_compound()`) actually correct?**
  _`Tool registry` has 122 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `chat_endpoint()` (e.g. with `describe_screen_for_llm()` and `get_screen_text_summary()`) actually correct?**
  _`chat_endpoint()` has 8 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Settings`, `build`, `dev` to the rest of the system?**
  _166 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `tools + window_layout` be split into smaller, more focused modules?**
  _Cohesion score 0.02970922882427307 - nodes in this community are weakly interconnected._
- **Should `style_profiler` be split into smaller, more focused modules?**
  _Cohesion score 0.11904761904761904 - nodes in this community are weakly interconnected._