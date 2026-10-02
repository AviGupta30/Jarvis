# Graph Report - Jarvis  (2026-10-02)

## Corpus Check
- 188 files · ~244,658 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 3, .css 3, .bat 1)

## Summary
- 3205 nodes · 6851 edges · 153 communities (130 shown, 23 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 714 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `7fd21515`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Tool registry
- style_profiler
- assignment_assembler.py
- create
- ppt_chart_engine.py
- dark_enhancement.py
- window_layout.py
- test_protocol.py
- youtube_control.py
- syllabus_auditor.py
- ppt_studio.py
- DeckRenderer
- browser_tool.py
- LRUCache
- file_ops.py
- PresentationBuilder
- assignment_answers
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
- resume_builder.py
- ppt_image_engine
- json
- ppt_composer.py
- dsa_enforcer.py
- ppt_content.py
- gmail_tool.py
- prompt_overlay
- ui_inspector
- os
- keyword_detect_tool
- typing
- voice_agent
- transformEngine
- CacheEngine
- air-drawing + air_drawing_tool
- ppt_designer.py
- voice.py
- package + App
- acoustic_tripwire
- assignment_humanizer.py
- time
- CacheClient
- interactionEngine + DrawingCanvas
- Clip
- package
- strokeManager
- render_sections
- llm.py
- safe_executor.py
- _render_html_inner
- web_search.py
- content_humanizer.py
- ResearchScraper
- Voice: STT, TTS, wake word, clap wake, overlay
- PowerPoint generator
- 2. Tool Registry (`tools.py`)
- frontend
- shapeManager
- ppt_content
- spotify_service.py
- prompt_enhancer_button
- Speaker
- drawingEngine
- message_reader
- test_lru
- test_lru
- refresh_docs.py
- screen_vision.py
- Element
- voice_agent.py
- memory/memory.py
- package
- handTracking
- .load_snapshot
- screen_reader.py
- ui_inspector.py
- datetime
- ControlPanel + HandSkeleton
- strokeRefiner
- ppt_chart_engine
- media_sessions.py
- pathlib
- prompt_enhancer_button
- thread_extractor.py
- re
- whatsapp_call
- CODEMAP
- youtube_player.py
- memory_tool.py
- .render
- rag_memory.py
- editor_save
- package
- create_resume
- test_lru
- Entry points
- ppt_tool.py
- assignment_pipeline.py
- Flow
- social_content_manager.py
- hinglish_normalizer.py
- Gotchas
- README
- ppt_tool
- __init__
- README
- _Player
- README
- PROMPT_TEMPLATE
- _crop_photo
- FEATURES
- voice_agent
- _build_content
- vector_store + database
- persistence.py
- extract_questions
- Resume creator
- server.py
- neural-cache
- dag_executor.py
- _llm_json
- get_active_window_info
- chat-routing
- edge_tts
- pygame
- browser_mail.py
- whatsapp
- benchmark.py
- Screen understanding & UI automation
- test_lru
- test_lru.py
- parse_player_command
- Syllabus auditor (YouTube playlist vs syllabus)
- run_tool
- test_lru
- _fetch_page_text
- Assignment solver (5 phases)
- Dark image/video enhancement
- download_kokoro.py
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
- `Entry points` --references--> `PresentationBuilder`  [INFERRED]
  docs/features/ppt.md → app/services/ppt_tool.py
- `Gotchas` --references--> `classify_app()`  [INFERRED]
  docs/features/prompt-enhancer.md → app/services/prompt_enhancer_button.py
- `HTTP endpoints` --references--> `init_rag_memory()`  [INFERRED]
  docs/ARCHITECTURE.md → app/services/rag_memory.py

## Import Cycles
- None detected.

## Communities (153 total, 23 thin omitted)

### Community 0 - "Tool registry"
Cohesion: 0.03
Nodes (86): ppt_styles(), append_to_file(), cache_get(), cache_set(), calculate(), close_specific_window(), close_sticky_notes(), close_tab() (+78 more)

### Community 1 - "style_profiler"
Cohesion: 0.12
Nodes (27): build_style_profile(), One-time training: parse a WhatsApp .txt chat export to build your personal…, add_deflection_phrase(), build_style_profile(), _compute_profile_stats(), _empty_profile(), get_profile(), get_profile_summary() (+19 more)

### Community 2 - "assignment_assembler.py"
Cohesion: 0.36
Nodes (7): assemble_assignment(), _create_powerpoint(), _create_word_doc(), _parse_qa_json(), Jarvis Assignment Tool — Phase 4: Document Assembly…, Assemble the extracted/humanized questions and answers into a formatted…, Extract and parse the JSON array from the input string.

### Community 3 - "create"
Cohesion: 0.11
Nodes (28): detect_profile(), interpret_image_instructions(), _is_instruction(), needs_architect(), parse_user_slides(), Separate the user's command, any pasted/attached content and attachment paths., Return strict slides if the text is written slide-by-slide, else []., Restore structure that copy-paste destroyed ("Title and OverviewEvent: …",… (+20 more)

### Community 4 - "ppt_chart_engine.py"
Cohesion: 0.08
Nodes (40): _bg_color(), _extract_strict_metric(), _fig_to_bytes(), _hex(), _metrics_to_bar(), _palette_colors(), ppt_chart_engine.py — Dynamic Data-Visualization Engine for JARVIS PPT…, Horizontal or vertical bar chart. (+32 more)

### Community 5 - "dark_enhancement.py"
Cohesion: 0.17
Nodes (20): _apply_gamma(), _fusion_and_polish(), get_all_enhancements(), _normalize_to_8bit(), _path_1_retinex(), _path_2_wavelet(), ndarray, run_pipeline_a() (+12 more)

### Community 6 - "window_layout.py"
Cohesion: 0.10
Nodes (35): media_state.py — which media app the user used last (Spotify or YouTube)…, True if the Spotify desktop app has a window (cheap: EnumWindows, no UIA)., spotify_running(), adjust_active_window(), _enumerate_app_windows(), _cb(), _get_process_name(), _get_title() (+27 more)

### Community 7 - "test_protocol.py"
Cohesion: 0.10
Nodes (23): decode_message(), encode_message(), protocol.py — Wire Protocol for Neural Cache (Milestone 2)…, Serialise a dict to the wire format: [4-byte length][UTF-8 JSON body] Args:…, Read exactly one message from a socket, handling partial TCP reads correctly.…, Loop until exactly n bytes have been read from sock. This is necessary because…, _recv_exact(), make_fake_socket() (+15 more)

### Community 8 - "youtube_control.py"
Cohesion: 0.08
Nodes (45): _dur_to_sec(), _end_session(), _fetch_results(), _find_channel(), _find_channel_at(), walk(), _format_results(), _initial_data() (+37 more)

### Community 9 - "syllabus_auditor.py"
Cohesion: 0.09
Nodes (35): _approx_token_count(), _assemble_response(), audit_playlist_syllabus(), _build_vector_store(), _chunk_transcript(), _coverage_level(), _embed_texts(), _extract_playlist_id() (+27 more)

### Community 10 - "ppt_studio.py"
Cohesion: 0.09
Nodes (30): _assign_images(), _caption(), _collect_attachments(), _create_format(), current_deck(), _desktop(), edit(), has_active_deck() (+22 more)

### Community 11 - "DeckRenderer"
Cohesion: 0.15
Nodes (21): _compact_header(), box(), DeckRenderer, fit_size(), _items(), para_h(), Header + lead + list inside a column. Returns nothing., Portrait/square image as a full-height panel flush to one edge. (+13 more)

### Community 12 - "browser_tool.py"
Cohesion: 0.09
Nodes (36): browse_and_paginate(), browse_and_read(), _clean_text(), click_element(), _ensure_url(), fill_form(), _llm_extract(), _new_browser_page() (+28 more)

### Community 13 - "LRUCache"
Cohesion: 0.13
Nodes (12): LRUCache, Node, Insert or update a key-value pair. - If key already exists: update value + TTL,…, Remove a key from the cache. Returns True if the key existed, False if it was…, Place node at the MRU (most-recently-used) end of the list., Remove node from its current position in the list (O(1) because doubly-linked)., Evict a specific node (unlink + remove from map)., A doubly-linked list node holding one cache entry. Attributes: key (str): Cache… (+4 more)

### Community 14 - "file_ops.py"
Cohesion: 0.10
Nodes (28): append_file(), bulk_rename(), create_folder(), delete_file(), diff_files(), _fmt_size(), list_directory(), _maybe_summarize() (+20 more)

### Community 15 - "PresentationBuilder"
Cohesion: 0.18
Nodes (19): _clean_image_path(), _get_image_aspect_ratio(), _oval(), _parse_bullet(), _parse_card(), PresentationBuilder, _frame(), Render a single image with CONTAIN-FIT (object-fit: contain). The image is… (+11 more)

### Community 16 - "assignment_answers"
Cohesion: 0.12
Nodes (25): _ask_question_on_page(), _find_input(), generate_answer(), generate_answers(), _get_persistent_page(), _groq_answer(), Jarvis Assignment Tool — Phase 2: Answer Generation…, Launch a visible (non-headless) Chromium with a persistent profile. Login… (+17 more)

### Community 17 - "resume_detector.py"
Cohesion: 0.18
Nodes (14): detect_resume_intent(), _extract_task_resource(), _find_best_task_match(), _has_continuation_verb(), _has_fresh_task_indicator(), _has_reference_phrase(), resume_detector.py — Jarvis Resume Intent Classifier…, Return True if the text contains a strong resume-intent reference phrase. (+6 more)

### Community 18 - "skill_prompt_enhancer.py"
Cohesion: 0.16
Nodes (21): check_for_hallucination(), clean_output(), detect_domain(), is_bloated(), protect_blocks(), prompt_enhancement_library.py…, Replace ``` fenced blocks with [[BLOCK_n]] placeholders., Put protected blocks back; append any the model dropped. (+13 more)

### Community 19 - "prompt_enhancer_button.py"
Cohesion: 0.08
Nodes (32): _acquire_single_instance(), _app_title_match(), _browser_url(), classify_app(), _exe_name(), _has_pattern(), install_autostart(), _is_editable() (+24 more)

### Community 20 - "generate_deck"
Cohesion: 0.10
Nodes (31): _budget_left(), _compact(), _content_prompt(), _flatten(), _gemini_json(), generate_deck(), _is_note(), run() (+23 more)

### Community 21 - "chat.py"
Cohesion: 0.07
Nodes (36): chat_endpoint(), _dag_stream_with_history(), planner_stream(), response_stream_with_history(), resume_stream(), tool_stream(), ChatRequest, _clean_yt_query() (+28 more)

### Community 22 - "ppt_research.py"
Cohesion: 0.10
Nodes (34): _edit_facts(), plan_queries(), 4-6 web queries covering the angles a deck on `topic` needs. Templates, not an…, Web + Wikipedia → verified facts. [] when offline (the deck is then written…, Facts relevant to an edit + the fact discipline (edits must not hallucinate…, research_facts(), allowed_numbers(), _anchors() (+26 more)

### Community 23 - "ppt_template.py"
Cohesion: 0.06
Nodes (55): analyze_format(), _analyze_slide(), classify_box(), _clear(), clone_slide(), delete_slide(), describe_template(), _field_label() (+47 more)

### Community 24 - "main.py"
Cohesion: 0.11
Nodes (24): get_alerts(), get, post, Stop watcher, acoustic tripwire, and close DB pool cleanly on server shutdown., Frontend polls this endpoint to receive proactive JARVIS screen alerts. e.g.…, Return current acoustic tripwire state for the frontend toggle., Arm the acoustic tripwire so double-claps wake Jarvis., Disarm the acoustic tripwire (engine keeps running, just paused). (+16 more)

### Community 25 - "ppt_router.py"
Cohesion: 0.11
Nodes (25): build_ppt(), generate(), create_ppt_backend(), generate(), extract_theme(), get_styles(), PPTBuildRequest, PPTCreateRequest (+17 more)

### Community 26 - "package"
Cohesion: 0.11
Nodes (20): name, private, type, version, autoprefixer, eslint, ref_eslint_config, @eslint/js (+12 more)

### Community 28 - "resume_builder.py"
Cohesion: 0.17
Nodes (23): _competencies_html(), _contact_html(), _education_html(), _experience_html(), _f(), _guess_icon(), _icon(), _it() (+15 more)

### Community 29 - "ppt_image_engine"
Cohesion: 0.16
Nodes (18): build_image_descriptors(), _extract_keywords(), get_aspect_ratio(), ImageDescriptor, match_images_to_slides(), _parse_slide_ref(), _parse_slide_ref_by_title(), ppt_image_engine.py — Semantic Image-Slide Matcher for JARVIS PPT Engine… (+10 more)

### Community 30 - "json"
Cohesion: 0.09
Nodes (27): nlp_extractor.py — LLM-Powered Fact & Entity Extractor…, _ensure_ledger_file(), find_resumable_task(), get_recent_tasks(), get_recent_tasks_raw(), get_task_ledger_for_prompt(), _load_ledger(), log_task() (+19 more)

### Community 31 - "ppt_composer.py"
Cohesion: 0.16
Nodes (38): _body_cards(), _body_fields(), _body_list(), _body_paragraph(), _body_stats(), _body_steps(), _body_table(), _cols_for() (+30 more)

### Community 32 - "dsa_enforcer.py"
Cohesion: 0.11
Nodes (17): _cache_del(), _cache_set(), DSAEnforcer, get_dsa_enforcer(), Write to Neural Cache, silently skipping if unavailable., Delete from Neural Cache, silently skipping if unavailable., Data, DSA / LeetCode enforcer mode (+9 more)

### Community 33 - "ppt_content.py"
Cohesion: 0.13
Nodes (27): apply_edit(), apply_structure(), _as_dated(), _as_stat(), _clauses(), finalize_slides(), find_targets(), _guess_targets() (+19 more)

### Community 34 - "gmail_tool.py"
Cohesion: 0.17
Nodes (19): check_emails(), _decode_body(), _format_date(), get_email_body(), _get_gmail_service(), _get_header(), list_unread(), gmail_tool.py — Jarvis Gmail Integration (Step 5)… (+11 more)

### Community 36 - "ui_inspector"
Cohesion: 0.10
Nodes (11): Walk all descendants looking for any control whose window_text contains `text`…, Fire an element's primary action via UIA Invoke pattern. No mouse movement —…, Inject text into an input element via UIA Value pattern. No simulated…, Read text from an element via UIA TextPattern or window_text. Returns empty…, Walk the accessibility tree and return all elements up to `depth` levels. Use…, Core wrapper around pywinauto's UIA backend. All interactions go through the OS…, Get a window wrapper by partial title match (regex-safe). Returns None if not…, Get the currently focused window via Win32 HWND matching. (+3 more)

### Community 37 - "os"
Cohesion: 0.16
Nodes (16): agentic_web_action(), _worker(), _build_search_queries(), _get_api_key(), agentic_web.py — Smart Web Research Engine for Jarvis…, Use the LLM to extract specific listings from the fetched content., Generator that streams progress and final answer., Return known direct listing URLs for a site+task combo. (+8 more)

### Community 38 - "keyword_detect_tool"
Cohesion: 0.07
Nodes (29): keyword_detect_tool(), _media_compound(), _media_intent_for(), _media_target(), Which player an ambiguous media command ("pause it", "next song") is for: named…, Media tool intent for one clause (YouTube-mode parser first, then keyword…, Re-target an unspecific media intent (pause/next/play X) to the given platform., "close this song and play shape of you", "pause the video then open mrbeast's… (+21 more)

### Community 39 - "typing"
Cohesion: 0.10
Nodes (25): generate_reply_draft(), Read the latest WhatsApp thread with a contact and generate 3 reply drafts that…, _build_system_prompt(), _build_user_prompt(), _call_groq(), generate_reply_draft(), get_cached_contact(), get_cached_drafts() (+17 more)

### Community 40 - "voice_agent"
Cohesion: 0.12
Nodes (10): AbstractEventLoop, Fixed on 2026-10-01 (voice, round 2), _ClapDetector, _EnergyVAD, ndarray, Queue, Stateful frame-by-frame Silero VAD using the ONNX model bundled with faster-…, Fallback if Silero can't load: adaptive noise floor. (+2 more)

### Community 42 - "CacheEngine"
Cohesion: 0.14
Nodes (14): CacheEngine, Any, engine.py — Single-Writer Command Queue (Milestone 3)…, Route a command dict to the appropriate handler. All handlers return a response…, Owns the LRUCache. Runs a single consumer loop on a dedicated thread. External…, Spawn the single writer thread. Call once at server boot., Gracefully stop the engine writer thread., The single consumer loop. Runs on CacheEngineThread. Processes one command at a… (+6 more)

### Community 43 - "air-drawing + air_drawing_tool"
Cohesion: 0.18
Nodes (9): open_air_drawing(), Opens the Air Drawing Canvas on the screen. This feature allows the user to…, Air drawing (webcam hand drawing), Files & symbols (auto-generated, line numbers are current), Flow, Gotchas, Graphify, Purpose (+1 more)

### Community 44 - "ppt_designer.py"
Cohesion: 0.08
Nodes (30): _best_window(), count_lines(), E(), gradient_box(), _line_factor(), line_shape(), _pil_font(), place_image() (+22 more)

### Community 45 - "voice.py"
Cohesion: 0.08
Nodes (33): loanword_ratio(), Share of Devanagari words that are English loanwords ("ओपन क्रोम" → 1.0). High…, _clean_transcript(), _finish(), _get_groq(), _groq_once(), groq_stt_available(), _load_whisper_model() (+25 more)

### Community 46 - "package + App"
Cohesion: 0.16
Nodes (11): App(), ChatMessage(), API_BASE, frontend_src_index, lucide-react, react, ref_react_dom_client, react-markdown (+3 more)

### Community 47 - "acoustic_tripwire"
Cohesion: 0.05
Nodes (30): AcousticWakeEngine, calibrate_tripwire(), _generate_chime(), get_wake_event(), _play_chime(), ndarray, Background thread that watches the microphone for a double-clap pattern. Usage…, Start the background listening thread. (+22 more)

### Community 48 - "assignment_humanizer.py"
Cohesion: 0.12
Nodes (25): _extract_output_text(), _fill_input(), _find_element(), _get_browser_page(), humanize_all_answers(), _humanize_chunk_via_browser(), humanize_text(), _humanize_via_browser() (+17 more)

### Community 49 - "time"
Cohesion: 0.10
Nodes (22): main(), prompt_overlay.py ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Jarvis…, _focus_or_open_whatsapp(), open_whatsapp(), WhatsApp Windows Desktop App Automation Uses the native Windows app via…, Focus the WhatsApp window or open it if not running. Returns True on success., Opens the WhatsApp desktop app., find_controls() (+14 more)

### Community 50 - "CacheClient"
Cohesion: 0.07
Nodes (22): Send one of the reply drafts generated by generate_reply_draft. draft_index is…, send_style_reply(), CacheClient, Any, Store a key-value pair, optionally with a TTL. Args: key: Cache key. value:…, Delete a key from the cache. Returns: True if the key existed and was deleted,…, Retrieve server statistics (hit rate, evictions, cache size, etc.). Returns…, Explicitly close the socket connection. (+14 more)

### Community 52 - "Clip"
Cohesion: 0.12
Nodes (12): Clip, prewarm(), PCM (int16, 24 kHz) that fills while synthesis streams; playable immediately., hi' → Hindi voice, 'en' → English voice, for one sentence., Begin synthesising `text` now; returns a Clip that can be played while it fills., Synthesise short stock phrases (greetings, acks) into the cache for instant…, route_language(), _sapi_sync() (+4 more)

### Community 53 - "package"
Cohesion: 0.14
Nodes (14): devDependencies, autoprefixer, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, postcss (+6 more)

### Community 55 - "render_sections"
Cohesion: 0.11
Nodes (25): _balanced_rows(), _fill(), image_block(), _image_panel(), _masonry(), Split items into rows with at most one item difference (5 in 3 cols → 3+2, 7 →…, How much extra height a section can absorb before it looks inflated., Framed images (no crop) + numbered captions under each. Returns used height. (+17 more)

### Community 56 - "llm.py"
Cohesion: 0.06
Nodes (46): classify_context(), context_classifier.py — Jarvis Situational Awareness…, Classify the situation from user input. Returns a dict with keys: urgency :…, check_for_tool_intent(), generate_chat_response(), _groq_generate(), _is_complex_response(), _is_rate_limit() (+38 more)

### Community 57 - "safe_executor.py"
Cohesion: 0.14
Nodes (16): execute_safe(), Exception, Safe Code Executor for Jarvis ------------------------------- Runs LLM-…, Restricted open(): blocks writes to system paths., Restricted __import__: blocks dangerous modules., Raised when generated code violates safety constraints., AST visitor that inspects generated code before execution., Parse and walk the AST, raising SecurityError on violations. (+8 more)

### Community 58 - "_render_html_inner"
Cohesion: 0.16
Nodes (20): _apply_layout_answer(), _balance_columns(), _css_extra(), _decor_html(), _e(), _footer_html(), _header_html(), _initials() (+12 more)

### Community 59 - "web_search.py"
Cohesion: 0.09
Nodes (32): research_scraper.py — Autonomous Web Research Scraper…, _extract_location(), get_info(), get_weather(), Pulls a clean location name out of a weather query., Get current weather using wttr.in — returns a clean spoken string., Search for a query within a specific website using DuckDuckGo site: operator., Read and extract readable text content from a specific URL. (+24 more)

### Community 60 - "content_humanizer.py"
Cohesion: 0.17
Nodes (21): build_structure_prompt(), build_vocab_prompt(), call_groq(), check_similarity(), detect_tone(), fact_check(), get_groq_client(), get_sentence_scores() (+13 more)

### Community 61 - "ResearchScraper"
Cohesion: 0.14
Nodes (9): NLPExtractor, Runs extraction on each scraped source and aggregates the results. Returns a…, research_pipeline.py — End-to-End Autonomous Research Orchestrator…, Scrapes the web for a topic and extracts verified facts and statistics. Yields…, research_topic(), Searches DDG for the topic, fetches the top N links concurrently, and returns…, ResearchScraper, Phase 3: Autonomous Research Aggregator. Scrapes live facts from the web,… (+1 more)

### Community 62 - "Voice: STT, TTS, wake word, clap wake, overlay"
Cohesion: 0.13
Nodes (14): Sets a reminder that Jarvis will speak after a given number of seconds., set_reminder(), Speak a complete text. All sentences synthesise in parallel, play in order., speak_text(), Config (`app/core/config.py` + env), Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify (+6 more)

### Community 63 - "PowerPoint generator"
Cohesion: 0.14
Nodes (12): ppt_edit(), Follow-up edit of the last deck (generator). See ppt_studio.edit., _ppt_edit(), Generator wrapper — follow-up edits of the last deck ("on slide 3 …", "make it…, Entry points, Files & symbols (auto-generated, line numbers are current), Flow — edit (`ppt_edit` → `ppt_studio.edit` → `ppt_content.apply_edit`), Graphify (+4 more)

### Community 64 - "2. Tool Registry (`tools.py`)"
Cohesion: 0.06
Nodes (43): close_window(), get_system_info(), get_system_time(), lock_screen(), open_app(), open_windows_copilot(), Returns current date and time naturally., Returns CPU usage, RAM usage, and battery status. (+35 more)

### Community 65 - "frontend"
Cohesion: 0.22
Nodes (8): Frontend (`frontend/src`), Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Key behaviour (App.jsx), Purpose, Web UI (React/Vite), DagPlanPanel()

### Community 67 - "ppt_content"
Cohesion: 0.16
Nodes (18): architect_slides(), ask(), _retry(), run(), _complete_from_source(), deck_facts(), extractive_ok(), _missing_parts() (+10 more)

### Community 68 - "spotify_service.py"
Cohesion: 0.10
Nodes (35): _buttons(), _clean_query(), _close_spotify(), _com_init(), _content_play_buttons(), _find_spotify_window(), _cb(), _is_playing() (+27 more)

### Community 69 - "prompt_enhancer_button"
Cohesion: 0.14
Nodes (4): EnhanceButton, Move (and optionally show) without ever activating the window; Tk's deiconify()…, Default spot: just above the prompt box's top-right corner; below it or inside…, _save_state()

### Community 70 - "Speaker"
Cohesion: 0.11
Nodes (12): hinglish_to_devanagari(), Rewrite the Hindi words of a romanized Hinglish sentence in Devanagari, leaving…, Channel, _norm_words(), The speech stream of one command's reply., Plays sentences from many Channels without overlap: - urgent phrases (acks,…, Barge-in "stop": silence now and drop everything queued., Did the mic just hear Jarvis himself (speaker → mic bleed)? Echo comes back… (+4 more)

### Community 72 - "message_reader"
Cohesion: 0.15
Nodes (18): _bring_whatsapp_to_front(), _get_whatsapp_window(), _heuristic_parse_ocr_lines(), _parse_uia_message_string(), message_reader.py — Jarvis WhatsApp Intelligence: Message Reader…, Restores and focuses WhatsApp window. Returns True on success., Walks the WhatsApp UIA accessibility tree to extract messages. WhatsApp Desktop…, Parses a raw UIA ListItem Name string into a structured message dict.… (+10 more)

### Community 73 - "test_lru"
Cohesion: 0.20
Nodes (5): Accessing 'a' should move it to MRU and save it from eviction., Re-setting an existing key should move it to MRU., len(cache.map) must never exceed capacity., Fill to capacity+1. The first key inserted (LRU) should be evicted., TestEviction

### Community 75 - "refresh_docs.py"
Cohesion: 0.24
Nodes (11): collections, fnmatch, auto_block(), _js_symbols(), label_communities(), Path, _py_symbols(), refresh_docs.py — keep docs/features/*.md and the graphify graph in sync with… (+3 more)

### Community 76 - "screen_vision.py"
Cohesion: 0.12
Nodes (25): _build_history_context(), _build_system_prompt(), _call_gemma_reasoning(), capture_screen_b64(), _get_active_process_name(), _get_active_window_title(), _pixel_diff_percent(), ndarray (+17 more)

### Community 77 - "Element"
Cohesion: 0.10
Nodes (10): Element, element_from_handle(), focused_element(), uia_local.py — thread-safe UI Automation access (helper, not a tool)…, This thread's IUIAutomation (COM initialised for the thread on first use)., Minimal pywinauto-style wrapper around an IUIAutomationElement., Rect, uia() (+2 more)

### Community 78 - "voice_agent.py"
Cohesion: 0.08
Nodes (24): app_services, AsyncClient, difflib, httpx, pyaudio, _clean_agentic_line(), extract_wake_word_command(), _is_stop() (+16 more)

### Community 79 - "memory/memory.py"
Cohesion: 0.15
Nodes (18): find_skill(), format_preferences_for_prompt(), get_all_preferences(), list_skills(), Jarvis Vector Memory — ChromaDB-based long-term memory engine. Stores and…, Returns a string suitable for injecting into LLM prompts., Stable short ID based on content hash., Persist a successful dynamic skill for future reuse. (+10 more)

### Community 80 - "package"
Cohesion: 0.22
Nodes (9): dependencies, framer-motion, lucide-react, react, react-dom, react-markdown, react-syntax-highlighter, remark-gfm (+1 more)

### Community 81 - "handTracking"
Cohesion: 0.31
Nodes (3): CameraView(), getHandsConstructor(), HandTracker

### Community 82 - ".load_snapshot"
Cohesion: 0.29
Nodes (4): Any, Serialise the entire live cache to a plain dict. Expired entries are excluded —…, Restore cache state from a snapshot dict (produced by snapshot()). Called once…, Place node at the LRU (least-recently-used) end of the list.

### Community 83 - "screen_reader.py"
Cohesion: 0.11
Nodes (24): _accessibility_tree(), get_screen_screenshot_b64(), _groq_vision_screen(), _init_tesseract(), _ocr_screen(), screen_reader.py — Jarvis Screen Vision (VLM-first architecture)…, Legacy OCR layer. Works on any app but extracts raw text only — no layout,…, Reads the active window's accessibility tree. Works best for native Win32 apps.… (+16 more)

### Community 84 - "ui_inspector.py"
Cohesion: 0.09
Nodes (21): click_ui_element_uia(), dump_app_ui_tree(), Click a UI element inside an app by AutomationId, name, or control type. Does…, Inject text into a specific input field in an app via UIA Value pattern. No…, Read the current text content of a UI element — e.g. a terminal output pane, a…, Dump the full Windows UI Automation accessibility tree of an app window. Use…, Type a question into the Windows Copilot sidebar and retrieve the response.…, read_ui_element_text() (+13 more)

### Community 85 - "datetime"
Cohesion: 0.11
Nodes (20): add_event(), check_today_schedule(), _get_calendar_service(), get_upcoming_events(), calendar_tool.py — Jarvis Google Calendar Integration (Step 8)…, Create a new event in Google Calendar. - title: "Project Meeting" - date:…, Authenticate and return a Google Calendar API service object., List events in the next N days. (+12 more)

### Community 86 - "ControlPanel + HandSkeleton"
Cohesion: 0.13
Nodes (13): frontend_src_airdrawing_airdrawing, COLORS, ControlPanel(), FONTS, SHAPES, FINGERTIP_INDICES, HAND_CONNECTIONS, HandSkeleton() (+5 more)

### Community 88 - "ppt_chart_engine"
Cohesion: 0.33
Nodes (3): ChartEngine, Stateless chart renderer. All colors are derived from the active PPT palette —…, Render a chart from structured data. Args: chart_data: {"type": "bar",…

### Community 89 - "media_sessions.py"
Cohesion: 0.16
Nodes (20): app_kind(), control(), run(), _do(), _filter(), kind_playing(), _label(), media_command() (+12 more)

### Community 90 - "pathlib"
Cohesion: 0.12
Nodes (24): _classify_question_type(), _clean_text(), _extract_marks(), _extract_via_llm_text(), _extract_via_vision(), _has_figure_reference(), _parse_llm_json_response(), _pdf_pages_to_images() (+16 more)

### Community 91 - "prompt_enhancer_button"
Cohesion: 0.21
Nodes (11): _box_contains(), _box_set_value(), _clip_get(), _clip_set(), _ctrl(), _focus(), _focused_text(), _norm() (+3 more)

### Community 92 - "thread_extractor.py"
Cohesion: 0.19
Nodes (13): extract_thread(), extract_thread_as_string(), _find_latest_incoming(), _get_current_chat_title(), _group_into_turns(), _open_contact_chat(), thread_extractor.py — Jarvis WhatsApp Intelligence: Thread Extractor…, Merges consecutive messages from the same sender into a single turn. This makes… (+5 more)

### Community 94 - "re"
Cohesion: 0.18
Nodes (8): add_human_prosody(), ssml_processor.py — Human Prosody Pre-processor…, Add natural speech prosody to plain text. Args: text: Plain text (already…, Remove all SSML tags from text — used when falling back to edge-tts which does…, strip_ssml(), detect_whatsapp_call(), detect_whatsapp_send(), re

### Community 95 - "whatsapp_call"
Cohesion: 0.27
Nodes (10): flow_stream(), _click_voice_call_button(), confirm_whatsapp_call(), _focus_or_open_whatsapp(), _get_whatsapp_window(), initiate_whatsapp_call(), whatsapp_call.py — Jarvis Smart WhatsApp Calling Integration (Fully Isolated)…, Focus the WhatsApp window or open it if not running. Returns True on success. (+2 more)

### Community 96 - "CODEMAP"
Cohesion: 0.22
Nodes (8): Backend core & API, Code map, Frontend (`frontend/src`, React 19 + Vite + Tailwind 4), Ignore these (no runtime role), Neural cache (neural_cache/, see its README.md), Scripts, Services (app/services), WhatsApp intelligence (app/services/whatsapp_intelligence)

### Community 97 - "youtube_player.py"
Cohesion: 0.08
Nodes (59): _address_bar_focused(), _address_bar_value(), _clip_get(), _clip_restore(), _clip_set(), com_init(), current_video_info(), _fallback() (+51 more)

### Community 98 - "memory_tool.py"
Cohesion: 0.18
Nodes (19): _ensure_memory_file(), forget_fact(), _fuzzy_match_topics(), get_all_facts_as_context(), _load_memory(), memory_tool.py — Jarvis Persistent Memory (Step 10 — ENHANCED)…, Replace an existing fact with an updated version., Remove all facts under a topic. (+11 more)

### Community 99 - ".render"
Cohesion: 0.40
Nodes (3): _as_plain_content(), _deep_plain(), Last-resort fallback: every word of a composite slide as plain bullets (never…

### Community 100 - "rag_memory.py"
Cohesion: 0.05
Nodes (68): aiomysql, forget_memory(), ForgetRequest, get_history(), ingest_memory(), IngestRequest, memory_stats(), BaseModel (+60 more)

### Community 101 - "editor_save"
Cohesion: 0.11
Nodes (24): get, post, resume_router.py — FastAPI router for the visual resume editor…, resume_editor(), resume_save(), _apply_op(), _data_uri(), _edit_content() (+16 more)

### Community 102 - "package"
Cohesion: 0.40
Nodes (5): scripts, build, dev, lint, preview

### Community 103 - "create_resume"
Cohesion: 0.14
Nodes (20): _analyse_design(), _apply_layout_hint(), _attachments(), create_resume(), detect_resume_request(), _file_hash(), _has_details(), _load_state() (+12 more)

### Community 105 - "Entry points"
Cohesion: 0.22
Nodes (10): _hint_text(), _ide_allows(), is_prompt_box(), In IDEs only chat / agent inputs qualify, never the code editor, the terminal,…, Entry points, Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify (+2 more)

### Community 106 - "ppt_tool.py"
Cohesion: 0.10
Nodes (27): _auto_select_image_layout(), _bg_fill(), _c(), compute_split_geometry(), _corner_L(), _detect_purpose(), extract_theme_from_image(), _groq_call() (+19 more)

### Community 107 - "assignment_pipeline.py"
Cohesion: 0.20
Nodes (17): _browser_thread(), _find_el(), _get_answer(), _get_browser_ctx(), _groq_answer(), _groq_humanize(), _humanize_browser(), Queue (+9 more)

### Community 108 - "Flow"
Cohesion: 0.20
Nodes (17): _apply_color(), _closest_preset(), _contrast(), _css(), _hex(), _lum(), _merge_design(), _mix() (+9 more)

### Community 109 - "social_content_manager.py"
Cohesion: 0.16
Nodes (14): build_prompt(), call_llm(), generate_social_content(), Refine an existing piece of social media content based on user instructions.…, Calls Groq Llama 3.3 70B directly for maximum speed. No slow fallbacks., Generate professional, multi-version social media content., refine_social_content(), Content humanizer & social content (+6 more)

### Community 110 - "hinglish_normalizer.py"
Cohesion: 0.18
Nodes (11): devanagari_to_hinglish(), _sub(), normalize_for_tts(), hinglish_normalizer.py — Devanagari Crash Prevention + Text Normalizer…, One Devanagari word → casual Hinglish roman ("चलाओ" → "chalao", "करना" →…, Romanize a Devanagari (Hindi) transcript for the backend, keeping any Latin…, Transform text so it's safe and natural-sounding for TTS: 1. Replace known…, Markdown → plain speakable text (keeps Devanagari). Also drops URLs and emoji. (+3 more)

### Community 111 - "Gotchas"
Cohesion: 0.20
Nodes (9): _mail_tool(), Email tools: try the real Gmail API (gmail_tool) first, fall back to opening…, Adding a tool (checklist), Calling tools from code, Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Purpose (+1 more)

### Community 112 - "README"
Cohesion: 0.50
Nodes (3): Expanding the ESLint configuration, React Compiler, React + Vite

### Community 119 - "_Player"
Cohesion: 0.21
Nodes (4): get_player(), _Player, One persistent 24 kHz output stream driven by a callback that pulls from a…, Play a clip as it arrives. Returns False if interrupted.

### Community 120 - "README"
Cohesion: 0.20
Nodes (9): Architecture, Benchmark, Files, LRU Cache Design, Neural Cache, Persistence, Running, Tests (+1 more)

### Community 122 - "_crop_photo"
Cohesion: 0.29
Nodes (6): _crop_photo(), _face_ratio(), _faces(), _grow_photo_box(), Grow from the face outwards until each edge hits a flat (uniform) line = the…, Cut the portrait out of the reference resume: face-anchored edge growth → VLM…

### Community 124 - "voice_agent"
Cohesion: 0.33
Nodes (3): MicListener, Initial ambient noise floor (kept up to date on every non-speech frame)., One 32 ms frame → clap check + VAD state machine → events.

### Community 125 - "_build_content"
Cohesion: 0.13
Nodes (25): _build_content(), _condense_content(), _content_brief(), _drop_invented(), clean_text(), ok(), _finalize_content(), _fit_render() (+17 more)

### Community 126 - "vector_store + database"
Cohesion: 0.33
Nodes (7): get_db_pool(), init_db(), Queries the table and uses the pgvector cosine distance operator (<=>) to fetch…, Inserts text chunks and vectors into the knowledge_store table., save_document_chunk(), search_similar_chunks(), asyncpg

### Community 127 - "persistence.py"
Cohesion: 0.09
Nodes (17): Any, Path, Queue, persistence.py — WAL + Snapshot for Neural Cache (Milestone 6)…, Flush and close the file handle cleanly on server shutdown., Manages periodic full-state snapshots. The snapshot itself is triggered through…, Serialise cache state to disk and truncate the WAL. Called by CacheEngine on…, Load the snapshot from disk. Returns None if no snapshot exists yet. Called… (+9 more)

### Community 128 - "extract_questions"
Cohesion: 0.19
Nodes (12): do_assignment(), Master orchestrator. Uses a background thread for all Playwright code. Yields…, extract_questions(), list_assignments(), _merge_and_deduplicate(), Merge questions from all three tracks. Priority: regex > vision > llm text. A…, Extract ALL questions from an assignment PDF using a 3-track hybrid system.…, Resolve PDF path: handles full paths, filenames, partial names. (+4 more)

### Community 129 - "Resume creator"
Cohesion: 0.22
Nodes (8): _image_b64(), Downscaled JPEG (a 1080x2400 phone screenshot costs far fewer vision tokens at…, Data/config, Files & symbols (auto-generated, line numbers are current), Graphify, Purpose, Resume creator, UI

### Community 130 - "server.py"
Cohesion: 0.09
Nodes (21): acoustic_tripwire.py — Jarvis Acoustic Wake Engine…, argparse, neural_cache, client.py — Python Client Library for Neural Cache (Milestone 5)…, CacheServer, main(), server.py — TCP Accept Loop for Neural Cache (Milestone 4)…, Full startup: recover state, start engine, begin accepting connections. (+13 more)

### Community 131 - "neural-cache"
Cohesion: 0.25
Nodes (7): Design, Files & symbols (auto-generated, line numbers are current), Graphify, Neural cache (Redis-like LRU server), Purpose, Runtime, Tests

### Community 132 - "dag_executor.py"
Cohesion: 0.07
Nodes (52): _semantic_window_adjust(), Settings, app_memory, _call_dag_planner(), DAGNode, _execute_node(), is_dag_task(), dag_executor.py — Jarvis DAG-Based Multi-Step Agent Planner… (+44 more)

### Community 133 - "_llm_json"
Cohesion: 0.47
Nodes (6): _gemini(), _groq(), _llm_json(), _parse_json(), Fallback when Groq is rate-limited (its vision model has a 200k tokens/DAY cap)., _vision()

### Community 134 - "get_active_window_info"
Cohesion: 0.17
Nodes (13): _on_screen_alert(), Callback fired by the background watcher when something notable is detected.…, Start background screen watcher and RAG memory system when the server boots., startup_event(), describe_screen_for_llm(), Returns a clean, LLM-optimized description of the current screen. Used as…, describe_screen_vlm(), Lightweight passive description — used as context injection in chat.py. Always… (+5 more)

### Community 135 - "chat-routing"
Cohesion: 0.25
Nodes (7): Change recipes, Chat pipeline & routing (/chat), Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Purpose, Response formats

### Community 138 - "browser_mail.py"
Cohesion: 0.24
Nodes (7): check_emails(), _get_api_key(), list_unread(), browser_mail.py — Standard Browser Mail Automation…, A generic tool to perform any mail task (like sending or reading) by pre-…, smart_mail_action(), webbrowser

### Community 139 - "whatsapp"
Cohesion: 0.33
Nodes (5): Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Purpose, WhatsApp: send, call, read, reply-style cloning

### Community 140 - "benchmark.py"
Cohesion: 0.13
Nodes (10): JSONFileBaseline, main(), measure_latency(), measure_throughput(), benchmark.py — Neural Cache vs JSON-file Baseline (Milestone 8)…, Spin up n_threads threads each doing ops_per_thread SET+GET pairs. Returns…, Mimics memory_tool.py's approach: every read/write touches disk. Uses a…, Run op_fn warmup times (discard), then timed times (measure). Returns (mean_µs,… (+2 more)

### Community 141 - "Screen understanding & UI automation"
Cohesion: 0.25
Nodes (7): _call_gemini_vision(), Send screenshot + context to the Groq vision model (settings.GROQ_VISION_MODEL)., Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Purpose, Screen understanding & UI automation

### Community 142 - "test_lru"
Cohesion: 0.50
Nodes (3): Return average time per (set + get) operation in microseconds., Per-op time for N=1000 vs N=100000 should be within 3x of each other. If the…, TestO1Timing

### Community 143 - "test_lru.py"
Cohesion: 0.18
Nodes (7): large_cache(), fixture, test_lru.py — Unit tests for neural_cache.lru (Milestone 7)…, LRU cache with capacity 3 — easy to reason about eviction., small_cache(), TestSentinels, pytest

### Community 144 - "parse_player_command"
Cohesion: 0.33
Nodes (7): _num(), parse_clock(), parse_duration(), parse_player_command(), Map a spoken player command to (action, amount, value), or None. `t` should…, 10 minutes' → 600, '1 hour 5 min' → 3900, 'half a minute' → 30, '90 s' → 90.…, 5:30' → 330, '1:02:03' → 3723, 'to 5 30' → 330. None if absent.

### Community 145 - "Syllabus auditor (YouTube playlist vs syllabus)"
Cohesion: 0.29
Nodes (6): Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Purpose, Syllabus auditor (YouTube playlist vs syllabus), Triggers

### Community 146 - "run_tool"
Cohesion: 0.15
Nodes (14): execute_tool(), BaseModel, post, ToolExecuteRequest, _call_sync(), tool_runner.py — Async execution of TOOL_REGISTRY entries for orchestrators…, Run a registry tool and return its output as a string. Raises on unknown tool…, run_tool() (+6 more)

### Community 148 - "_fetch_page_text"
Cohesion: 0.33
Nodes (3): _fetch_page_text(), __init__(), Download a page and return clean readable text (no HTML tags).

### Community 149 - "Assignment solver (5 phases)"
Cohesion: 0.33
Nodes (5): Assignment solver (5 phases), Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Purpose

### Community 150 - "Dark image/video enhancement"
Cohesion: 0.40
Nodes (4): Dark image/video enhancement, Files & symbols (auto-generated, line numbers are current), Graphify, Purpose

### Community 155 - "Flow (`scripts/voice_agent.py`)"
Cohesion: 0.33
Nodes (6): detect_language(), Detect whether the user spoke English, Hinglish, or Hindi. Returns: 'english' —…, language_mismatch(), True if a reply sentence is in the other language than the one the user spoke., Loudest output RMS in the last `window` s — the voice agent's echo reference., Flow (`scripts/voice_agent.py`)

## Knowledge Gaps
- **156 isolated node(s):** `Settings`, `name`, `private`, `version`, `type` (+151 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1367 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **23 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Tool registry` connect `Tool registry` to `extract_questions`, `assignment_assembler.py`, `dag_executor.py`, `dark_enhancement.py`, `window_layout.py`, `youtube_control.py`, `syllabus_auditor.py`, `browser_mail.py`, `browser_tool.py`, `file_ops.py`, `assignment_answers`, `skill_prompt_enhancer.py`, `run_tool`, `chat.py`, `ppt_router.py`, `json`, `os`, `keyword_detect_tool`, `air-drawing + air_drawing_tool`, `assignment_humanizer.py`, `web_search.py`, `Voice: STT, TTS, wake word, clap wake, overlay`, `PowerPoint generator`, `2. Tool Registry (`tools.py`)`, `spotify_service.py`, `ui_inspector.py`, `datetime`, `whatsapp_call`, `memory_tool.py`, `rag_memory.py`, `create_resume`, `social_content_manager.py`?**
  _High betweenness centrality (0.132) - this node is a cross-community bridge._
- **Why does `open_air_drawing()` connect `air-drawing + air_drawing_tool` to `Tool registry`?**
  _High betweenness centrality (0.082) - this node is a cross-community bridge._
- **Are the 122 inferred relationships involving `Tool registry` (e.g. with `keyword_detect_tool()` and `_media_compound()`) actually correct?**
  _`Tool registry` has 122 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `chat_endpoint()` (e.g. with `describe_screen_for_llm()` and `get_screen_text_summary()`) actually correct?**
  _`chat_endpoint()` has 8 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Settings`, `name`, `private` to the rest of the system?**
  _156 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Tool registry` be split into smaller, more focused modules?**
  _Cohesion score 0.032915360501567396 - nodes in this community are weakly interconnected._
- **Should `style_profiler` be split into smaller, more focused modules?**
  _Cohesion score 0.11904761904761904 - nodes in this community are weakly interconnected._