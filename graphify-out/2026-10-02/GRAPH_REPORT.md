# Graph Report - Jarvis  (2026-10-02)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 3151 nodes · 6697 edges · 163 communities (138 shown, 25 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 684 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e0271761`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- tools
- style_profiler + refresh_docs
- assignment_tool
- persistence
- ppt_chart_engine
- dark_video_enhancement + media_enhancement
- window_layout + tools
- test_protocol + engine
- youtube_control
- syllabus_auditor
- ppt_studio
- ppt_designer
- browser_tool
- youtube_player
- file_ops
- ppt_tool
- assignment_answers
- ppt_content
- prompt_enhancement_library + skill_prompt_enhancer
- prompt_enhancer_button
- vector_store + database
- chat + youtube_control
- ppt_research
- ppt_template
- main
- ppt_router + ppt_tool
- package
- gestureController + gestureInterpreter
- resume_builder
- ppt_image_engine
- task_ledger + test_task_resumption
- ppt_composer + ppt_designer
- dsa_enforcer + dsa-mode
- ppt_content
- gmail_tool
- prompt_overlay
- ui_inspector
- agentic_web
- os-control + youtube_control
- test_lru
- voice_agent
- transformEngine
- media_sessions
- air-drawing + air_drawing_tool
- ppt_designer
- voice
- package + App
- acoustic_tripwire
- assignment_humanizer
- ppt_composer + ppt_designer
- client
- interactionEngine + DrawingCanvas
- memory + main
- package
- strokeManager
- whatsapp
- llm + llm-personality
- safe_executor + ui_inspector
- reply_generator
- web_search + tools
- content_humanizer + content-tools
- jarvis_overlay
- memory_tool + calendar_tool
- research_scraper + nlp_extractor
- whatsapp_smart + tools
- frontend
- shapeManager
- ppt_content
- spotify_service
- prompt_enhancer_button
- voice
- drawingEngine
- message_reader + reply_generator
- test_lru
- test_lru
- resume_detector
- context_classifier + personality
- uia_local
- voice_agent
- memory
- package
- handTracking
- lru
- screen_vision + screen_reader
- tools + ui_inspector
- test_concurrency
- ControlPanel + HandSkeleton
- strokeRefiner
- ppt_chart_engine
- lru
- assignment + assignment_answers
- prompt_enhancer_button
- whatsapp_call
- ssml_processor
- assignment_pipeline
- CODEMAP
- youtube_player
- social_content_manager + ui_inspector
- assignment_tool
- memory
- README
- package
- resume_builder
- test_lru
- prompt-enhancer + prompt_enhancer_button
- ppt_tool
- mysql_db + rag_memory
- resume_builder
- ppt_designer
- voice
- chat-routing
- README
- ppt_tool
- __init__
- README
- voice
- browser_mail
- PROMPT_TEMPLATE
- resume_builder
- FEATURES
- voice_agent
- resume_builder
- media_state + youtube_control
- client
- acoustic_tripwire
- resume-creator
- server + protocol
- neural-cache
- dag_executor + dynamic_skill
- resume_builder
- ppt_content + ppt_designer
- acoustic_tripwire
- edge_tts
- pygame
- ppt_designer
- smart_navigator
- benchmark
- email-calendar + tools
- youtube_control + youtube_player
- ARCHITECTURE
- ppt + KNOWN_ISSUES
- rag_memory
- tools
- test_lru
- dark_enhancement
- test_lru
- assignment_assembler
- tool-registry
- test_lru
- CLAUDE
- agents
- voice + tools
- whatsapp
- memory
- media-enhancement
- download_kokoro
- tool_runner
- debug_wa
- client

## God Nodes (most connected - your core abstractions)
1. `Tool registry` - 123 edges
2. `DeckRenderer` - 49 edges
3. `chat_endpoint()` - 49 edges
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
- `Gotchas` --references--> `recall_memory()`  [INFERRED]
  docs/features/memory.md → app/api/memory.py
- `UI` --references--> `detect_resume_request()`  [INFERRED]
  docs/features/resume-creator.md → app/services/resume_builder.py
- `HTTP endpoints` --references--> `init_rag_memory()`  [INFERRED]
  docs/ARCHITECTURE.md → app/services/rag_memory.py
- `Gotchas` --references--> `run_tool()`  [INFERRED]
  docs/features/agents.md → app/services/tool_runner.py

## Import Cycles
- None detected.

## Communities (163 total, 25 thin omitted)

### Community 0 - "tools"
Cohesion: 0.04
Nodes (78): ppt_styles(), append_to_file(), cache_get(), cache_set(), calculate(), close_sticky_notes(), close_tab(), copy_selected_text() (+70 more)

### Community 1 - "style_profiler + refresh_docs"
Cohesion: 0.08
Nodes (39): build_style_profile(), One-time training: parse a WhatsApp .txt chat export to build your personal…, add_deflection_phrase(), build_style_profile(), _compute_profile_stats(), _empty_profile(), get_profile(), get_profile_summary() (+31 more)

### Community 2 - "assignment_tool"
Cohesion: 0.22
Nodes (10): _clean_text(), _extract_marks(), _has_figure_reference(), Clean up PDF text extraction artifacts., Smart regex-based question extractor for structured, numbered assignments.…, Given a parent question body, split out sub-questions (i, ii, iii, a, b, c) and…, Extract marks from question text if mentioned., Check if question references a figure or diagram. (+2 more)

### Community 3 - "persistence"
Cohesion: 0.09
Nodes (15): Any, Path, Queue, Flush and close the file handle cleanly on server shutdown., Manages periodic full-state snapshots. The snapshot itself is triggered through…, Serialise cache state to disk and truncate the WAL. Called by CacheEngine on…, Load the snapshot from disk. Returns None if no snapshot exists yet. Called…, Start a daemon thread that enqueues a SNAPSHOT command every interval_seconds.… (+7 more)

### Community 4 - "ppt_chart_engine"
Cohesion: 0.12
Nodes (34): _bg_color(), _extract_strict_metric(), _fig_to_bytes(), _hex(), _metrics_to_bar(), _palette_colors(), ppt_chart_engine.py — Dynamic Data-Visualization Engine for JARVIS PPT…, Horizontal or vertical bar chart. (+26 more)

### Community 5 - "dark_video_enhancement + media_enhancement"
Cohesion: 0.26
Nodes (12): get_all_enhancements(), ndarray, run_pipeline_a(), _enhance_frame(), _get_ffmpeg_binary(), process_video_smartly(), Re-encode a video to H.264 MP4 so browsers can play it., _reencode_to_h264() (+4 more)

### Community 6 - "window_layout + tools"
Cohesion: 0.07
Nodes (42): close_specific_window(), close_window(), _find_window_fuzzy(), focus_window(), Snaps left_app to left half and right_app to right half using Win32 API (no…, Closes the current active real app window (skips the Jarvis overlay)., Find a window HWND by fuzzy name matching using Win32 API (no pygetwindow)., Closes a specific window/app by name using Win32 PostMessage WM_CLOSE. (+34 more)

### Community 7 - "test_protocol + engine"
Cohesion: 0.07
Nodes (30): CacheEngine, Any, Route a command dict to the appropriate handler. All handlers return a response…, Owns the LRUCache. Runs a single consumer loop on a dedicated thread. External…, Spawn the single writer thread. Call once at server boot., Gracefully stop the engine writer thread., The single consumer loop. Runs on CacheEngineThread. Processes one command at a…, decode_message() (+22 more)

### Community 8 - "youtube_control"
Cohesion: 0.11
Nodes (36): app: 'spotify' | 'youtube'., set_last(), _dur_to_sec(), _end_session(), _find_channel(), _find_channel_at(), walk(), _format_results() (+28 more)

### Community 9 - "syllabus_auditor"
Cohesion: 0.05
Nodes (40): _approx_token_count(), _assemble_response(), audit_playlist_syllabus(), _build_vector_store(), _chunk_transcript(), _coverage_level(), _embed_texts(), _extract_playlist_id() (+32 more)

### Community 10 - "ppt_studio"
Cohesion: 0.09
Nodes (30): _assign_images(), _caption(), _collect_attachments(), _create_format(), current_deck(), _desktop(), edit(), has_active_deck() (+22 more)

### Community 11 - "ppt_designer"
Cohesion: 0.15
Nodes (21): _compact_header(), box(), DeckRenderer, fit_size(), _items(), para_h(), Header + lead + list inside a column. Returns nothing., Portrait/square image as a full-height panel flush to one edge. (+13 more)

### Community 12 - "browser_tool"
Cohesion: 0.15
Nodes (26): browse_and_paginate(), browse_and_read(), _clean_text(), click_element(), _ensure_url(), fill_form(), _llm_extract(), _new_browser_page() (+18 more)

### Community 13 - "youtube_player"
Cohesion: 0.11
Nodes (31): com_init(), current_video_info(), _fallback(), fmt_span(), fmt_time(), _focused_desc(), _focused_is_toolbar(), _in_page() (+23 more)

### Community 14 - "file_ops"
Cohesion: 0.10
Nodes (29): append_file(), bulk_rename(), create_folder(), delete_file(), diff_files(), _fmt_size(), list_directory(), _maybe_summarize() (+21 more)

### Community 15 - "ppt_tool"
Cohesion: 0.17
Nodes (20): _clean_image_path(), _corner_L(), _get_image_aspect_ratio(), _parse_bullet(), _parse_card(), PresentationBuilder, _frame(), Render a single image with CONTAIN-FIT (object-fit: contain). The image is… (+12 more)

### Community 16 - "assignment_answers"
Cohesion: 0.16
Nodes (19): _ask_question_on_page(), _find_input(), _get_persistent_page(), Jarvis Assignment Tool — Phase 2: Answer Generation…, Launch a visible (non-headless) Chromium with a persistent profile. Login…, Try CSS selectors to find the visible chat input. Returns locator or None., Type a message into the AI chat input and submit it., Upload PDF to the AI chat page. Returns True if upload was initiated. (+11 more)

### Community 17 - "ppt_content"
Cohesion: 0.13
Nodes (27): apply_edit(), apply_structure(), _as_dated(), _as_stat(), _clauses(), finalize_slides(), find_targets(), _guess_targets() (+19 more)

### Community 18 - "prompt_enhancement_library + skill_prompt_enhancer"
Cohesion: 0.16
Nodes (21): check_for_hallucination(), clean_output(), detect_domain(), is_bloated(), protect_blocks(), prompt_enhancement_library.py…, Replace ``` fenced blocks with [[BLOCK_n]] placeholders., Put protected blocks back; append any the model dropped. (+13 more)

### Community 19 - "prompt_enhancer_button"
Cohesion: 0.08
Nodes (32): _acquire_single_instance(), _app_title_match(), _browser_url(), classify_app(), _exe_name(), _has_pattern(), install_autostart(), _is_editable() (+24 more)

### Community 20 - "vector_store + database"
Cohesion: 0.33
Nodes (7): get_db_pool(), init_db(), Queries the table and uses the pgvector cosine distance operator (<=>) to fetch…, Inserts text chunks and vectors into the knowledge_store table., save_document_chunk(), search_similar_chunks(), asyncpg

### Community 21 - "chat + youtube_control"
Cohesion: 0.05
Nodes (61): chat_endpoint(), _dag_stream_with_history(), planner_stream(), response_stream_with_history(), resume_stream(), tool_stream(), ChatRequest, _clean_yt_query() (+53 more)

### Community 22 - "ppt_research"
Cohesion: 0.10
Nodes (34): _edit_facts(), plan_queries(), 4-6 web queries covering the angles a deck on `topic` needs. Templates, not an…, Web + Wikipedia → verified facts. [] when offline (the deck is then written…, Facts relevant to an edit + the fact discipline (edits must not hallucinate…, research_facts(), allowed_numbers(), _anchors() (+26 more)

### Community 23 - "ppt_template"
Cohesion: 0.06
Nodes (56): analyze_format(), _analyze_slide(), classify_box(), _clear(), clone_slide(), delete_slide(), describe_template(), _field_label() (+48 more)

### Community 24 - "main"
Cohesion: 0.12
Nodes (22): get_alerts(), get, post, Frontend polls this endpoint to receive proactive JARVIS screen alerts. e.g.…, Return current acoustic tripwire state for the frontend toggle., Arm the acoustic tripwire so double-claps wake Jarvis., Disarm the acoustic tripwire (engine keeps running, just paused)., Schedule an ambient-noise recalibration pass. The engine samples the mic for ~2… (+14 more)

### Community 25 - "ppt_router + ppt_tool"
Cohesion: 0.11
Nodes (25): build_ppt(), generate(), create_ppt_backend(), generate(), extract_theme(), get_styles(), PPTBuildRequest, PPTCreateRequest (+17 more)

### Community 26 - "package"
Cohesion: 0.11
Nodes (20): name, private, type, version, autoprefixer, eslint, ref_eslint_config, @eslint/js (+12 more)

### Community 28 - "resume_builder"
Cohesion: 0.23
Nodes (22): _competencies_html(), _contact_html(), _e(), _education_html(), _experience_html(), _guess_icon(), _header_html(), _icon() (+14 more)

### Community 29 - "ppt_image_engine"
Cohesion: 0.16
Nodes (18): build_image_descriptors(), _extract_keywords(), get_aspect_ratio(), ImageDescriptor, match_images_to_slides(), _parse_slide_ref(), _parse_slide_ref_by_title(), ppt_image_engine.py — Semantic Image-Slide Matcher for JARVIS PPT Engine… (+10 more)

### Community 30 - "task_ledger + test_task_resumption"
Cohesion: 0.14
Nodes (18): _ensure_ledger_file(), find_resumable_task(), get_recent_tasks(), get_recent_tasks_raw(), _load_ledger(), log_task(), task_ledger.py — Jarvis Task Context Ledger…, Return a formatted string of the last N tasks, suitable for display or speech.… (+10 more)

### Community 31 - "ppt_composer + ppt_designer"
Cohesion: 0.16
Nodes (37): _balanced_rows(), _body_cards(), _body_fields(), _body_list(), _body_paragraph(), _body_stats(), _body_steps(), _body_table() (+29 more)

### Community 32 - "dsa_enforcer + dsa-mode"
Cohesion: 0.11
Nodes (17): _cache_del(), _cache_set(), DSAEnforcer, get_dsa_enforcer(), Write to Neural Cache, silently skipping if unavailable., Delete from Neural Cache, silently skipping if unavailable., Data, DSA / LeetCode enforcer mode (+9 more)

### Community 33 - "ppt_content"
Cohesion: 0.10
Nodes (31): _budget_left(), _compact(), _content_prompt(), _flatten(), _gemini_json(), generate_deck(), _is_note(), run() (+23 more)

### Community 34 - "gmail_tool"
Cohesion: 0.17
Nodes (19): check_emails(), _decode_body(), _format_date(), get_email_body(), _get_gmail_service(), _get_header(), list_unread(), gmail_tool.py — Jarvis Gmail Integration (Step 5)… (+11 more)

### Community 36 - "ui_inspector"
Cohesion: 0.10
Nodes (11): Walk all descendants looking for any control whose window_text contains `text`…, Fire an element's primary action via UIA Invoke pattern. No mouse movement —…, Inject text into an input element via UIA Value pattern. No simulated…, Read text from an element via UIA TextPattern or window_text. Returns empty…, Walk the accessibility tree and return all elements up to `depth` levels. Use…, Core wrapper around pywinauto's UIA backend. All interactions go through the OS…, Get a window wrapper by partial title match (regex-safe). Returns None if not…, Get the currently focused window via Win32 HWND matching. (+3 more)

### Community 37 - "agentic_web"
Cohesion: 0.11
Nodes (19): agentic_web_action(), _worker(), _build_search_queries(), _fetch_page_text(), __init__(), _get_api_key(), agentic_web.py — Smart Web Research Engine for Jarvis…, Download a page and return clean readable text (no HTML tags). (+11 more)

### Community 38 - "os-control + youtube_control"
Cohesion: 0.25
Nodes (7): _is_positional(), A pick by position, not by title: 'the first result', 'number 3', 'the latest…, Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Purpose, Windows/OS control: windows, media, apps, files

### Community 40 - "voice_agent"
Cohesion: 0.12
Nodes (10): AbstractEventLoop, Fixed on 2026-10-01 (voice, round 2), _ClapDetector, _EnergyVAD, ndarray, Queue, Stateful frame-by-frame Silero VAD using the ONNX model bundled with faster-…, Fallback if Silero can't load: adaptive noise floor. (+2 more)

### Community 42 - "media_sessions"
Cohesion: 0.17
Nodes (18): app_kind(), control(), run(), _do(), _filter(), kind_playing(), _label(), media_command() (+10 more)

### Community 43 - "air-drawing + air_drawing_tool"
Cohesion: 0.18
Nodes (9): open_air_drawing(), Opens the Air Drawing Canvas on the screen. This feature allows the user to…, Air drawing (webcam hand drawing), Files & symbols (auto-generated, line numbers are current), Flow, Gotchas, Graphify, Purpose (+1 more)

### Community 44 - "ppt_designer"
Cohesion: 0.09
Nodes (24): _lead_h(), Leads are drawn entirely in the semibold heading font — measure them that way., _as_plain_content(), count_lines(), _deep_plain(), E(), gradient_box(), _line_factor() (+16 more)

### Community 45 - "voice"
Cohesion: 0.06
Nodes (48): devanagari_to_hinglish(), _sub(), loanword_ratio(), normalize_for_tts(), hinglish_normalizer.py — Devanagari Crash Prevention + Text Normalizer…, One Devanagari word → casual Hinglish roman ("चलाओ" → "chalao", "करना" →…, Share of Devanagari words that are English loanwords ("ओपन क्रोम" → 1.0). High…, Romanize a Devanagari (Hindi) transcript for the backend, keeping any Latin… (+40 more)

### Community 46 - "package + App"
Cohesion: 0.16
Nodes (11): App(), ChatMessage(), API_BASE, frontend_src_index, lucide-react, react, ref_react_dom_client, react-markdown (+3 more)

### Community 47 - "acoustic_tripwire"
Cohesion: 0.12
Nodes (9): AcousticWakeEngine, Background thread that watches the microphone for a double-clap pattern. Usage…, Start the background listening thread., Signal the background thread to exit and wait for it., Resume detection after a disable()., Pause detection without stopping the thread (fast resume)., Signal the background thread to re-run calibration on the next cycle. Returns…, Override the volume threshold (used by voice_agent inline mode). (+1 more)

### Community 48 - "assignment_humanizer"
Cohesion: 0.12
Nodes (25): _extract_output_text(), _fill_input(), _find_element(), _get_browser_page(), humanize_all_answers(), _humanize_chunk_via_browser(), humanize_text(), _humanize_via_browser() (+17 more)

### Community 49 - "ppt_composer + ppt_designer"
Cohesion: 0.13
Nodes (21): _fill(), image_block(), _image_panel(), _masonry(), How much extra height a section can absorb before it looks inflated., Framed images (no crop) + numbered captions under each. Returns used height., Boxes for the images at full column width in exactly `rows` rows (scaled down…, Balanced split of sections into columns (reading order kept inside each… (+13 more)

### Community 50 - "client"
Cohesion: 0.17
Nodes (6): Delete a key from the cache. Returns: True if the key existed and was deleted,…, Retrieve server statistics (hit rate, evictions, cache size, etc.). Returns…, Send a command and return the response. Thread-safe. Handles lazy connect and…, Open a socket to the server if not already connected. Called within the lock —…, Send a PING and return True if the server replies PONG. Useful for health…, Retrieve the value for a key, or None on miss / expiry / error. Args: key:…

### Community 52 - "memory + main"
Cohesion: 0.11
Nodes (17): _on_screen_alert(), Stop watcher, acoustic tripwire, and close DB pool cleanly on server shutdown., Callback fired by the background watcher when something notable is detected.…, Start background screen watcher and RAG memory system when the server boots., shutdown_event(), startup_event(), Start the passive background screen watcher. Args: callback: Function called…, Stop the background screen watcher thread cleanly. (+9 more)

### Community 53 - "package"
Cohesion: 0.14
Nodes (14): devDependencies, autoprefixer, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, postcss (+6 more)

### Community 55 - "whatsapp"
Cohesion: 0.33
Nodes (6): _focus_or_open_whatsapp(), open_whatsapp(), Focus the WhatsApp window or open it if not running. Returns True on success., Opens the WhatsApp desktop app., Sends a WhatsApp message using the Windows desktop app via keyboard automation.…, send_whatsapp_message()

### Community 56 - "llm + llm-personality"
Cohesion: 0.10
Nodes (27): check_for_tool_intent(), _groq_generate(), _is_complex_response(), _is_rate_limit(), _mark_exhausted(), _other(), _parse_reset(), pick_model() (+19 more)

### Community 57 - "safe_executor + ui_inspector"
Cohesion: 0.11
Nodes (20): execute_safe(), Exception, Safe Code Executor for Jarvis ------------------------------- Runs LLM-…, Restricted open(): blocks writes to system paths., Restricted __import__: blocks dangerous modules., Raised when generated code violates safety constraints., AST visitor that inspects generated code before execution., Parse and walk the AST, raising SecurityError on violations. (+12 more)

### Community 58 - "reply_generator"
Cohesion: 0.20
Nodes (10): Send one of the reply drafts generated by generate_reply_draft. draft_index is…, send_style_reply(), get_cached_contact(), get_cached_drafts(), get_cached_incoming(), Returns the in-memory draft cache. Used by send_style_reply() in tools.py., Returns the contact name from the last draft generation., Returns the incoming message from the last draft generation. (+2 more)

### Community 59 - "web_search + tools"
Cohesion: 0.09
Nodes (32): research_scraper.py — Autonomous Web Research Scraper…, _extract_location(), get_info(), get_weather(), Pulls a clean location name out of a weather query., Get current weather using wttr.in — returns a clean spoken string., Search for a query within a specific website using DuckDuckGo site: operator., Read and extract readable text content from a specific URL. (+24 more)

### Community 60 - "content_humanizer + content-tools"
Cohesion: 0.11
Nodes (28): build_structure_prompt(), build_vocab_prompt(), call_groq(), check_similarity(), detect_tone(), fact_check(), get_groq_client(), get_sentence_scores() (+20 more)

### Community 61 - "jarvis_overlay"
Cohesion: 0.20
Nodes (5): Image, generate_arc_reactor(), JarvisOverlay, Draws a beautiful arc reactor using PIL when no icon file is found., read_state()

### Community 62 - "memory_tool + calendar_tool"
Cohesion: 0.09
Nodes (32): add_event(), check_today_schedule(), _get_calendar_service(), get_upcoming_events(), calendar_tool.py — Jarvis Google Calendar Integration (Step 8)…, Create a new event in Google Calendar. - title: "Project Meeting" - date:…, Authenticate and return a Google Calendar API service object., List events in the next N days. (+24 more)

### Community 63 - "research_scraper + nlp_extractor"
Cohesion: 0.15
Nodes (8): NLPExtractor, Runs extraction on each scraped source and aggregates the results. Returns a…, Scrapes the web for a topic and extracts verified facts and statistics. Yields…, research_topic(), Searches DDG for the topic, fetches the top N links concurrently, and returns…, ResearchScraper, Phase 3: Autonomous Research Aggregator. Scrapes live facts from the web,…, _research_and_create_ppt()

### Community 64 - "whatsapp_smart + tools"
Cohesion: 0.06
Nodes (41): create_word_doc(), get_system_time(), lock_screen(), open_app(), Returns current date and time naturally., Takes a full screenshot and saves to Desktop., Locks the Windows screen., Opens a Windows application by name. (+33 more)

### Community 65 - "frontend"
Cohesion: 0.22
Nodes (8): Frontend (`frontend/src`), Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Key behaviour (App.jsx), Purpose, Web UI (React/Vite), DagPlanPanel()

### Community 67 - "ppt_content"
Cohesion: 0.16
Nodes (18): architect_slides(), ask(), _retry(), run(), _complete_from_source(), deck_facts(), extractive_ok(), _missing_parts() (+10 more)

### Community 68 - "spotify_service"
Cohesion: 0.10
Nodes (35): _buttons(), _clean_query(), _close_spotify(), _com_init(), _content_play_buttons(), _find_spotify_window(), _cb(), _is_playing() (+27 more)

### Community 69 - "prompt_enhancer_button"
Cohesion: 0.14
Nodes (4): EnhanceButton, Move (and optionally show) without ever activating the window; Tk's deiconify()…, Default spot: just above the prompt box's top-right corner; below it or inside…, _save_state()

### Community 70 - "voice"
Cohesion: 0.11
Nodes (11): hinglish_to_devanagari(), Rewrite the Hindi words of a romanized Hinglish sentence in Devanagari, leaving…, Channel, The speech stream of one command's reply., Plays sentences from many Channels without overlap: - urgent phrases (acks,…, Barge-in "stop": silence now and drop everything queued., Did the mic just hear Jarvis himself (speaker → mic bleed)? Echo comes back…, Next (channel, text, lang) or None. Non-blocking. (+3 more)

### Community 72 - "message_reader + reply_generator"
Cohesion: 0.04
Nodes (63): _bring_whatsapp_to_front(), _get_whatsapp_window(), _heuristic_parse_ocr_lines(), _parse_uia_message_string(), message_reader.py — Jarvis WhatsApp Intelligence: Message Reader…, Restores and focuses WhatsApp window. Returns True on success., Walks the WhatsApp UIA accessibility tree to extract messages. WhatsApp Desktop…, Parses a raw UIA ListItem Name string into a structured message dict.… (+55 more)

### Community 73 - "test_lru"
Cohesion: 0.20
Nodes (5): Accessing 'a' should move it to MRU and save it from eviction., Re-setting an existing key should move it to MRU., len(cache.map) must never exceed capacity., Fill to capacity+1. The first key inserted (LRU) should be evicted., TestEviction

### Community 75 - "resume_detector"
Cohesion: 0.18
Nodes (14): detect_resume_intent(), _extract_task_resource(), _find_best_task_match(), _has_continuation_verb(), _has_fresh_task_indicator(), _has_reference_phrase(), resume_detector.py — Jarvis Resume Intent Classifier…, Return True if the text contains a strong resume-intent reference phrase. (+6 more)

### Community 76 - "context_classifier + personality"
Cohesion: 0.13
Nodes (16): classify_context(), detect_language(), context_classifier.py — Jarvis Situational Awareness…, Detect whether the user spoke English, Hinglish, or Hindi. Returns: 'english' —…, Classify the situation from user input. Returns a dict with keys: urgency :…, _maybe_compress_history(), When conversation history exceeds 15 messages, compress the oldest 10 into a…, _reply_language_note() (+8 more)

### Community 77 - "uia_local"
Cohesion: 0.11
Nodes (8): Element, element_from_handle(), focused_element(), uia_local.py — thread-safe UI Automation access (helper, not a tool)…, This thread's IUIAutomation (COM initialised for the thread on first use)., Minimal pywinauto-style wrapper around an IUIAutomationElement., Rect, uia()

### Community 78 - "voice_agent"
Cohesion: 0.09
Nodes (23): app_services, AsyncClient, difflib, httpx, pyaudio, _clean_agentic_line(), extract_wake_word_command(), _is_stop() (+15 more)

### Community 79 - "memory"
Cohesion: 0.15
Nodes (18): find_skill(), format_preferences_for_prompt(), get_all_preferences(), list_skills(), Jarvis Vector Memory — ChromaDB-based long-term memory engine. Stores and…, Returns a string suitable for injecting into LLM prompts., Stable short ID based on content hash., Persist a successful dynamic skill for future reuse. (+10 more)

### Community 80 - "package"
Cohesion: 0.22
Nodes (9): dependencies, framer-motion, lucide-react, react, react-dom, react-markdown, react-syntax-highlighter, remark-gfm (+1 more)

### Community 81 - "handTracking"
Cohesion: 0.31
Nodes (3): CameraView(), getHandsConstructor(), HandTracker

### Community 82 - "lru"
Cohesion: 0.15
Nodes (7): Node, Any, Serialise the entire live cache to a plain dict. Expired entries are excluded —…, Restore cache state from a snapshot dict (produced by snapshot()). Called once…, Place node at the LRU (least-recently-used) end of the list., A doubly-linked list node holding one cache entry. Attributes: key (str): Cache…, Return True if this entry has a TTL and it has elapsed.

### Community 83 - "screen_vision + screen_reader"
Cohesion: 0.05
Nodes (55): _accessibility_tree(), describe_screen_for_llm(), get_screen_screenshot_b64(), _groq_vision_screen(), _init_tesseract(), _ocr_screen(), screen_reader.py — Jarvis Screen Vision (VLM-first architecture)…, Legacy OCR layer. Works on any app but extracts raw text only — no layout,… (+47 more)

### Community 84 - "tools + ui_inspector"
Cohesion: 0.13
Nodes (15): click_ui_element_uia(), dump_app_ui_tree(), Click a UI element inside an app by AutomationId, name, or control type. Does…, Inject text into a specific input field in an app via UIA Value pattern. No…, Read the current text content of a UI element — e.g. a terminal output pane, a…, Dump the full Windows UI Automation accessibility tree of an app window. Use…, read_ui_element_text(), type_into_ui_element() (+7 more)

### Community 85 - "test_concurrency"
Cohesion: 0.20
Nodes (8): Lock, 50 concurrent clients, each doing 1000 ops. After completion: - Server still…, The engine should report meaningful stats after the load test., While 10 threads hammer the cache, a separate thread pings repeatedly. All…, One client thread. Performs `ops` random GET/SET/DEL operations. Records any…, TestConcurrency, _ping_loop(), _worker()

### Community 86 - "ControlPanel + HandSkeleton"
Cohesion: 0.13
Nodes (13): frontend_src_airdrawing_airdrawing, COLORS, ControlPanel(), FONTS, SHAPES, FINGERTIP_INDICES, HAND_CONNECTIONS, HandSkeleton() (+5 more)

### Community 88 - "ppt_chart_engine"
Cohesion: 0.33
Nodes (3): ChartEngine, Stateless chart renderer. All colors are derived from the active PPT palette —…, Render a chart from structured data. Args: chart_data: {"type": "bar",…

### Community 89 - "lru"
Cohesion: 0.17
Nodes (9): LRUCache, Insert or update a key-value pair. - If key already exists: update value + TTL,…, Remove a key from the cache. Returns True if the key existed, False if it was…, Place node at the MRU (most-recently-used) end of the list., Remove node from its current position in the list (O(1) because doubly-linked)., Evict a specific node (unlink + remove from map)., Evict the LRU entry (the node just before the tail sentinel). Returns the…, O(1) Least-Recently-Used cache backed by: - dict[str, Node] — hash map for O(1)… (+1 more)

### Community 90 - "assignment + assignment_answers"
Cohesion: 0.12
Nodes (19): generate_answer(), generate_answers(), _groq_answer(), Generate an answer using Groq LLM with automatic model fallback chain. Tries…, Generate complete answers for ALL questions from an assignment. Tries these…, Generate an answer for a SINGLE question using Groq LLM directly (fast, no…, do_assignment(), Master orchestrator. Uses a background thread for all Playwright code. Yields… (+11 more)

### Community 91 - "prompt_enhancer_button"
Cohesion: 0.21
Nodes (11): _box_contains(), _box_set_value(), _clip_get(), _clip_set(), _ctrl(), _focus(), _focused_text(), _norm() (+3 more)

### Community 92 - "whatsapp_call"
Cohesion: 0.27
Nodes (10): flow_stream(), _click_voice_call_button(), confirm_whatsapp_call(), _focus_or_open_whatsapp(), _get_whatsapp_window(), initiate_whatsapp_call(), whatsapp_call.py — Jarvis Smart WhatsApp Calling Integration (Fully Isolated)…, Focus the WhatsApp window or open it if not running. Returns True on success. (+2 more)

### Community 94 - "ssml_processor"
Cohesion: 0.33
Nodes (5): add_human_prosody(), ssml_processor.py — Human Prosody Pre-processor…, Add natural speech prosody to plain text. Args: text: Plain text (already…, Remove all SSML tags from text — used when falling back to edge-tts which does…, strip_ssml()

### Community 95 - "assignment_pipeline"
Cohesion: 0.20
Nodes (17): _browser_thread(), _find_el(), _get_answer(), _get_browser_ctx(), _groq_answer(), _groq_humanize(), _humanize_browser(), Queue (+9 more)

### Community 96 - "CODEMAP"
Cohesion: 0.22
Nodes (8): Backend core & API, Code map, Frontend (`frontend/src`, React 19 + Vite + Tailwind 4), Ignore these (no runtime role), Neural cache (neural_cache/, see its README.md), Scripts, Services (app/services), WhatsApp intelligence (app/services/whatsapp_intelligence)

### Community 97 - "youtube_player"
Cohesion: 0.11
Nodes (34): _address_bar_focused(), _address_bar_value(), _clip_get(), _clip_restore(), _clip_set(), focus(), _focus_address_bar(), _focus_page() (+26 more)

### Community 98 - "social_content_manager + ui_inspector"
Cohesion: 0.06
Nodes (32): Jarvis Assignment Tool — Phase 1: Smart Question Extractor…, nlp_extractor.py — LLM-Powered Fact & Entity Extractor…, main(), prompt_overlay.py ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Jarvis…, research_pipeline.py — End-to-End Autonomous Research Orchestrator…, screen_vision.py — Jarvis VLM Screen Understanding (Layer 1 Upgrade)…, build_prompt(), call_llm() (+24 more)

### Community 99 - "assignment_tool"
Cohesion: 0.12
Nodes (16): _classify_question_type(), extract_questions(), _extract_via_llm_text(), _extract_via_vision(), _merge_and_deduplicate(), _parse_llm_json_response(), _pdf_pages_to_images(), _pdf_pages_to_text() (+8 more)

### Community 100 - "memory"
Cohesion: 0.17
Nodes (16): forget_memory(), ForgetRequest, ingest_memory(), IngestRequest, BaseModel, delete, post, app/api/memory.py — Jarvis Long-Term Memory API Router… (+8 more)

### Community 101 - "README"
Cohesion: 0.20
Nodes (9): Architecture, Benchmark, Files, LRU Cache Design, Neural Cache, Persistence, Running, Tests (+1 more)

### Community 102 - "package"
Cohesion: 0.40
Nodes (5): scripts, build, dev, lint, preview

### Community 103 - "resume_builder"
Cohesion: 0.13
Nodes (21): _analyse_design(), _apply_layout_answer(), _attachments(), create_resume(), detect_resume_request(), _file_hash(), _has_details(), list_resume_templates() (+13 more)

### Community 105 - "prompt-enhancer + prompt_enhancer_button"
Cohesion: 0.22
Nodes (10): _hint_text(), _ide_allows(), is_prompt_box(), In IDEs only chat / agent inputs qualify, never the code editor, the terminal,…, Entry points, Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify (+2 more)

### Community 106 - "ppt_tool"
Cohesion: 0.11
Nodes (26): _auto_select_image_layout(), _bg_fill(), _c(), compute_split_geometry(), _detect_purpose(), extract_theme_from_image(), _groq_call(), _normalize_and_recover() (+18 more)

### Community 107 - "mysql_db + rag_memory"
Cohesion: 0.20
Nodes (12): aiomysql, close_mysql(), init_mysql(), mysql_db.py — Jarvis Async MySQL Connection Pool…, Gracefully close the MySQL connection pool on server shutdown., Initialize the MySQL connection pool and ensure all required tables exist. Safe…, init_rag_memory(), _load_faiss_index() (+4 more)

### Community 108 - "resume_builder"
Cohesion: 0.23
Nodes (15): _apply_color(), _closest_preset(), _contrast(), _css(), _hex(), _lum(), _merge_design(), _mix() (+7 more)

### Community 109 - "ppt_designer"
Cohesion: 0.18
Nodes (12): _best_window(), place_image(), prepare_image(), Return a PPTX-safe copy (EXIF-rotated, RGB, ≤2400px, png/jpg) and its aspect., Edge-energy profile along an axis ('x' or 'y') for smart cropping., Start fraction of the window (length=keep fraction) with most detail, biased to…, cover: fill box, crop with saliency. contain: fit inside box, centred., _round_pic() (+4 more)

### Community 110 - "voice"
Cohesion: 0.25
Nodes (7): Config (`app/core/config.py` + env), Files & symbols (auto-generated, line numbers are current), Graphify, Measured (2026-09-30/10-01, i9-13900H, no GPU), Purpose, Server-side tripwire, Voice: STT, TTS, wake word, clap wake, overlay

### Community 111 - "chat-routing"
Cohesion: 0.25
Nodes (7): Change recipes, Chat pipeline & routing (/chat), Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Purpose, Response formats

### Community 112 - "README"
Cohesion: 0.50
Nodes (3): Expanding the ESLint configuration, React Compiler, React + Vite

### Community 119 - "voice"
Cohesion: 0.18
Nodes (5): get_player(), _Player, One persistent 24 kHz output stream driven by a callback that pulls from a…, Loudest output RMS in the last `window` s — the voice agent's echo reference., Play a clip as it arrives. Returns False if interrupted.

### Community 120 - "browser_mail"
Cohesion: 0.24
Nodes (7): check_emails(), _get_api_key(), list_unread(), browser_mail.py — Standard Browser Mail Automation…, A generic tool to perform any mail task (like sending or reading) by pre-…, smart_mail_action(), webbrowser

### Community 122 - "resume_builder"
Cohesion: 0.29
Nodes (6): _crop_photo(), _face_ratio(), _faces(), _grow_photo_box(), Grow from the face outwards until each edge hits a flat (uniform) line = the…, Cut the portrait out of the reference resume: face-anchored edge growth → VLM…

### Community 124 - "voice_agent"
Cohesion: 0.33
Nodes (3): MicListener, Initial ambient noise floor (kept up to date on every non-speech frame)., One 32 ms frame → clap check + VAD state machine → events.

### Community 125 - "resume_builder"
Cohesion: 0.24
Nodes (11): _data_uri(), _guess_name(), _guess_title(), _launch(), _placement(), Design's column lists + every other section (content or not) appended where it…, HTML → PDF (auto-shrinks to avoid a nearly-empty last page) → PNG previews., Smaller fallback models sometimes drop the name; recover it from the user's own… (+3 more)

### Community 126 - "media_state + youtube_control"
Cohesion: 0.18
Nodes (12): _media_target(), Which player an ambiguous media command ("pause it", "next song") is for: named…, get_last(), media_state.py — which media app the user used last (Spotify or YouTube)…, Last media app used within max_age seconds, else None., True if the Spotify desktop app has a window (cheap: EnumWindows, no UIA)., spotify_running(), _get_process_name() (+4 more)

### Community 127 - "client"
Cohesion: 0.24
Nodes (4): CacheClient, Explicitly close the socket connection., Close self._sock, suppressing errors. Called within the lock., Thread-safe client for the Neural Cache server. One instance can be safely…

### Community 128 - "acoustic_tripwire"
Cohesion: 0.18
Nodes (9): calibrate_tripwire(), get_wake_event(), _play_chime(), acoustic_tripwire.py — Jarvis Acoustic Wake Engine…, Return the threading.Event that the engine sets on a double-clap., Play the wake chime via sounddevice (non-blocking from caller's perspective)., Sample ambient noise for `sample_seconds`, calculate the mean RMS, then set…, Event (+1 more)

### Community 129 - "resume-creator"
Cohesion: 0.22
Nodes (8): _image_b64(), Downscaled JPEG (a 1080x2400 phone screenshot costs far fewer vision tokens at…, Data/config, Files & symbols (auto-generated, line numbers are current), Graphify, Purpose, Resume creator, UI

### Community 130 - "server + protocol"
Cohesion: 0.07
Nodes (31): argparse, neural_cache, benchmark.py — Neural Cache vs JSON-file Baseline (Milestone 8)…, client.py — Python Client Library for Neural Cache (Milestone 5)…, protocol.py — Wire Protocol for Neural Cache (Milestone 2)…, Loop until exactly n bytes have been read from sock. This is necessary because…, _recv_exact(), CacheServer (+23 more)

### Community 131 - "neural-cache"
Cohesion: 0.25
Nodes (7): Design, Files & symbols (auto-generated, line numbers are current), Graphify, Neural cache (Redis-like LRU server), Purpose, Runtime, Tests

### Community 132 - "dag_executor + dynamic_skill"
Cohesion: 0.07
Nodes (46): Settings, _call_dag_planner(), DAGNode, _execute_node(), dag_executor.py — Jarvis DAG-Based Multi-Step Agent Planner…, Ask the LLM to produce a DAG plan. Returns parsed dict., Returns execution waves — each wave is a list of node IDs that can run in…, Replace $variable references in args with actual stored results. (+38 more)

### Community 133 - "resume_builder"
Cohesion: 0.17
Nodes (16): _build_content(), _content_brief(), _drop_invented(), clean_text(), ok(), _edit_content(), _gemini(), _groq() (+8 more)

### Community 134 - "ppt_content + ppt_designer"
Cohesion: 0.11
Nodes (28): detect_profile(), interpret_image_instructions(), _is_instruction(), needs_architect(), parse_user_slides(), Separate the user's command, any pasted/attached content and attachment paths., Return strict slides if the text is written slide-by-slide, else []., Restore structure that copy-paste destroyed ("Title and OverviewEvent: …",… (+20 more)

### Community 135 - "acoustic_tripwire"
Cohesion: 0.25
Nodes (7): _generate_chime(), ndarray, Root Mean Square amplitude. Cast to float64 to prevent int16 overflow., FFT-based dominant frequency. Only inspect the positive half-spectrum (0 ……, Return True if this chunk looks like a clap/snap (loud + right frequency)., Main loop — opened inside the thread so PyAudio errors stay contained. State…, Generate a pleasant two-tone wake chime as a float32 numpy array.

### Community 138 - "ppt_designer"
Cohesion: 0.33
Nodes (3): Largest body size so all items fit in (w,h). style: 'stack'|'inline'., Row-aligned multi-column list: item i sits in row i//cols, so rows line up., _runs_for()

### Community 139 - "smart_navigator"
Cohesion: 0.24
Nodes (10): _get_api_key(), _llm_extract(), smart_navigator.py — Isolated Smart Web Navigator for Jarvis…, Attempt to find the GROQ API key safely., Pass scraped text through LLM for structured extraction., Resolve a verbal site name like 'unstop' to a URL like 'https://unstop.com'., Resolves site name, opens a VISIBLE browser, and performs a search or action…, _resolve_url() (+2 more)

### Community 140 - "benchmark"
Cohesion: 0.14
Nodes (7): JSONFileBaseline, main(), measure_latency(), measure_throughput(), Spin up n_threads threads each doing ops_per_thread SET+GET pairs. Returns…, Mimics memory_tool.py's approach: every read/write touches disk. Uses a…, Run op_fn warmup times (discard), then timed times (measure). Returns (mean_µs,…

### Community 141 - "email-calendar + tools"
Cohesion: 0.18
Nodes (10): _mail_tool(), Email tools: try the real Gmail API (gmail_tool) first, fall back to opening…, Calendar, Email, Email, calendar & morning brief, Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify (+2 more)

### Community 142 - "youtube_control + youtube_player"
Cohesion: 0.20
Nodes (11): _fetch_results(), _parse_videos(), add(), walk(), Collect videos from ytInitialData: classic videoRenderer (search) and the newer…, Scrape YouTube's results page → [{id,title,channel,duration,seconds,views}]; []…, 1,234,567 views' / '82 million views' / '1.2M' → int., _views() (+3 more)

### Community 143 - "ARCHITECTURE"
Cohesion: 0.22
Nodes (7): Inline (shared-stream) mode — called by voice_agent.py on every audio frame it…, Architecture, HTTP endpoints, LLM usage, Memory layers (five separate stores), Processes, Voice path (`scripts/voice_agent.py`)

### Community 144 - "ppt + KNOWN_ISSUES"
Cohesion: 0.14
Nodes (12): ppt_edit(), Follow-up edit of the last deck (generator). See ppt_studio.edit., _ppt_edit(), Generator wrapper — follow-up edits of the last deck ("on slide 3 …", "make it…, Entry points, Files & symbols (auto-generated, line numbers are current), Flow — edit (`ppt_edit` → `ppt_studio.edit` → `ppt_content.apply_edit`), Graphify (+4 more)

### Community 145 - "rag_memory"
Cohesion: 0.11
Nodes (29): get_mysql_pool(), Return the shared MySQL connection pool, initializing it if needed., get_embedding(), Runs the local fastembed ONNX model in a thread pool so it doesn't block the…, _extract_topics(), forget_turns(), _get_faiss_lock(), get_history() (+21 more)

### Community 146 - "tools"
Cohesion: 0.33
Nodes (6): execute_tool(), BaseModel, post, ToolExecuteRequest, fastapi, pydantic

### Community 148 - "dark_enhancement"
Cohesion: 0.39
Nodes (7): _apply_gamma(), _fusion_and_polish(), _normalize_to_8bit(), _path_1_retinex(), _path_2_wavelet(), run_pipeline_b(), pywt

### Community 149 - "test_lru"
Cohesion: 0.50
Nodes (3): Return average time per (set + get) operation in microseconds., Per-op time for N=1000 vs N=100000 should be within 3x of each other. If the…, TestO1Timing

### Community 150 - "assignment_assembler"
Cohesion: 0.36
Nodes (7): assemble_assignment(), _create_powerpoint(), _create_word_doc(), _parse_qa_json(), Jarvis Assignment Tool — Phase 4: Document Assembly…, Assemble the extracted/humanized questions and answers into a formatted…, Extract and parse the JSON array from the input string.

### Community 151 - "tool-registry"
Cohesion: 0.29
Nodes (6): Adding a tool (checklist), Calling tools from code, Files & symbols (auto-generated, line numbers are current), Graphify, Purpose, Tool registry & adding tools

### Community 152 - "test_lru"
Cohesion: 0.50
Nodes (4): large_cache(), fixture, LRU cache with capacity 3 — easy to reason about eviction., small_cache()

### Community 153 - "CLAUDE"
Cohesion: 0.33
Nodes (5): Gotchas, graphify, Jarvis — Claude Code guide, Run, Where things are

### Community 154 - "agents"
Cohesion: 0.33
Nodes (5): Agents: DAG executor, linear planner, dynamic skills, Data, Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify

### Community 155 - "voice + tools"
Cohesion: 0.12
Nodes (14): Sets a reminder that Jarvis will speak after a given number of seconds., set_reminder(), preload_local_stt(), _load(), Load the local Whisper models in the background (voice agent startup)., Feed streamed tokens; get back speakable sentences as early as possible., Speak a complete text. All sentences synthesise in parallel, play in order., Speak an async generator of text chunks, sentence by sentence, pipelined. (+6 more)

### Community 156 - "whatsapp"
Cohesion: 0.33
Nodes (5): Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Purpose, WhatsApp: send, call, read, reply-style cloning

### Community 157 - "memory"
Cohesion: 0.40
Nodes (5): get_history(), memory_stats(), get, Return statistics about Jarvis's long-term memory store. Includes total turns,…, Retrieve paginated conversation history from MySQL. Query params: limit (int):…

### Community 158 - "media-enhancement"
Cohesion: 0.40
Nodes (4): Dark image/video enhancement, Files & symbols (auto-generated, line numbers are current), Graphify, Purpose

### Community 159 - "download_kokoro"
Cohesion: 0.40
Nodes (3): download(), Download Kokoro TTS model files from GitHub releases. Run this ONCE to get the…, urllib_request

### Community 160 - "tool_runner"
Cohesion: 0.50
Nodes (3): _call_sync(), tool_runner.py — Async execution of TOOL_REGISTRY entries for orchestrators…, inspect

## Knowledge Gaps
- **156 isolated node(s):** `Settings`, `Architecture`, `Benchmark`, `LRU Cache Design`, `Persistence` (+151 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1347 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **25 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Tool registry` connect `tools` to `dag_executor + dynamic_skill`, `dark_video_enhancement + media_enhancement`, `window_layout + tools`, `youtube_control`, `syllabus_auditor`, `smart_navigator`, `browser_tool`, `file_ops`, `ppt + KNOWN_ISSUES`, `prompt_enhancement_library + skill_prompt_enhancer`, `chat + youtube_control`, `assignment_assembler`, `ppt_router + ppt_tool`, `voice + tools`, `task_ledger + test_task_resumption`, `agentic_web`, `air-drawing + air_drawing_tool`, `assignment_humanizer`, `whatsapp`, `web_search + tools`, `memory_tool + calendar_tool`, `whatsapp_smart + tools`, `spotify_service`, `tools + ui_inspector`, `assignment + assignment_answers`, `whatsapp_call`, `social_content_manager + ui_inspector`, `assignment_tool`, `memory`, `resume_builder`, `browser_mail`, `media_state + youtube_control`?**
  _High betweenness centrality (0.165) - this node is a cross-community bridge._
- **Why does `open_air_drawing()` connect `air-drawing + air_drawing_tool` to `tools`?**
  _High betweenness centrality (0.107) - this node is a cross-community bridge._
- **Are the 122 inferred relationships involving `Tool registry` (e.g. with `keyword_detect_tool()` and `_media_compound()`) actually correct?**
  _`Tool registry` has 122 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `chat_endpoint()` (e.g. with `describe_screen_for_llm()` and `get_screen_text_summary()`) actually correct?**
  _`chat_endpoint()` has 8 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Settings`, `Architecture`, `Benchmark` to the rest of the system?**
  _156 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `tools` be split into smaller, more focused modules?**
  _Cohesion score 0.036075949367088606 - nodes in this community are weakly interconnected._
- **Should `style_profiler + refresh_docs` be split into smaller, more focused modules?**
  _Cohesion score 0.07682926829268293 - nodes in this community are weakly interconnected._