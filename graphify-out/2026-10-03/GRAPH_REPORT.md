# Graph Report - Jarvis  (2026-10-03)

## Corpus Check
- 199 files · ~280,952 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 3, .css 3, .bat 1)

## Summary
- 3515 nodes · 7507 edges · 175 communities (143 shown, 32 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 752 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d81c4976`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Tool registry
- style_profiler.py
- analyzer.py
- Chat pipeline & routing (/chat)
- ppt_chart_engine.py
- dark_video_enhancement.py
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
- assignment_answers.py
- resume_detector
- prompt_enhancement_library + skill_prompt_enhancer
- prompt_enhancer_button.py
- generate_deck
- chat.py
- ppt_research.py
- ppt_template.py
- main.py
- ppt_router.py
- package
- gestureController + gestureInterpreter
- orchestrator.py
- ppt_image_engine
- test_task_resumption.py
- ppt_composer.py
- dsa_enforcer.py
- ppt_content.py
- gmail_tool.py
- PromptOverlay
- ui_inspector
- agentic_web.py
- media_sessions.py
- ._run
- voice_agent
- transformEngine
- CacheServer
- air-drawing + air_drawing_tool
- ppt_designer.py
- voice.py
- package + App
- AcousticWakeEngine
- assignment_humanizer.py
- message_reader.py
- CacheClient
- interactionEngine + DrawingCanvas
- Clip
- package
- strokeManager
- repair.py
- llm.py
- time
- create_resume
- web_search.py
- content_humanizer + content-tools
- os
- Voice: STT, TTS, wake word, clap wake, overlay
- PowerPoint generator
- 2. Tool Registry (`tools.py`)
- Architecture
- shapeManager
- Flow — create (`ppt_tool.ppt_create` → `ppt_studio.create`, a generator)
- spotify_service.py
- prompt_enhancer_button
- Speaker
- drawingEngine
- Gotchas
- test_lru
- assignment_tool.py
- refresh_docs.py
- reply_generator.py
- Element
- WALWriter
- memory/memory.py
- package
- handTracking
- .process_chunk
- screen_vision.py
- safe_executor.py
- .load_snapshot
- ControlPanel + HandSkeleton
- strokeRefiner
- ppt_chart_engine
- compiler.py
- smart_navigator.py
- prompt_enhancer_button
- typing
- re
- calendar_tool.py
- CODEMAP
- youtube_player.py
- _compile_section
- _compile_node
- rag_memory.py
- render_sections
- package
- schema.py
- test_lru
- prompt-enhancer + prompt_enhancer_button
- ppt_tool.py
- assignment_pipeline.py
- _measure_frame
- 2. The new approach: measure, label, calibrate, transfer, verify
- bindings.py
- _ef
- README
- test_lru
- __init__
- README
- _Player
- Neural Cache
- PROMPT_TEMPLATE
- Flow
- FEATURES
- voice_agent
- Content fidelity & page limits (2026-10-02)
- _e
- CacheEngine
- search_site
- Open
- voice_agent.py
- thread_extractor.py
- dag_executor.py
- resume_builder.py
- database.py
- acoustic_tripwire.py
- edge_tts
- pygame
- pathlib
- ui_inspector.py
- benchmark.py
- dark_enhancement.py
- whatsapp
- ._list_grid
- parse_youtube_followup
- ppt_tool
- api/memory.py
- test_lru
- test_lru
- _llm_json
- test_lru.py
- make_frame_node
- _fetch_page_text
- ResearchScraper
- _find_spotify_window
- parse_player_command
- DSA / LeetCode enforcer mode
- test_builder
- Syllabus auditor (YouTube playlist vs syllabus)
- _extract_theme_pil_local
- ppt_create
- _render_competency_item
- Dark image/video enhancement
- Web search, research & browser automation
- make_image_node
- _collect_google_fonts
- collect_bindings
- make_chart_node
- make_commands_geometry
- make_radial_fill
- make_repeat_node
- make_ring_spec
- make_rule_node
- make_text_style
- resolve_binding

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
- `Gotchas` --references--> `recall_memory()`  [INFERRED]
  docs/features/memory.md → app/api/memory.py
- `Entry points` --references--> `PresentationBuilder`  [INFERRED]
  docs/features/ppt.md → app/services/ppt_tool.py
- `Gotchas` --references--> `classify_app()`  [INFERRED]
  docs/features/prompt-enhancer.md → app/services/prompt_enhancer_button.py

## Import Cycles
- None detected.

## Communities (175 total, 32 thin omitted)

### Community 0 - "Tool registry"
Cohesion: 0.03
Nodes (96): list_skills(), List all saved skill descriptions., Store a user preference (e.g. key='browser', value='Chrome')., save_preference(), ppt_styles(), append_to_file(), cache_get(), cache_set() (+88 more)

### Community 1 - "style_profiler.py"
Cohesion: 0.12
Nodes (27): build_style_profile(), One-time training: parse a WhatsApp .txt chat export to build your personal…, add_deflection_phrase(), build_style_profile(), _compute_profile_stats(), _empty_profile(), get_profile(), get_profile_summary() (+19 more)

### Community 2 - "analyzer.py"
Cohesion: 0.12
Nodes (43): _file_hash(), _hex(), analyze_reference(), _build_decor_nodes(), _build_experience_component(), _build_from_legacy(), _make_section_nodes(), _build_header_nodes() (+35 more)

### Community 3 - "Chat pipeline & routing (/chat)"
Cohesion: 0.25
Nodes (7): Change recipes, Chat pipeline & routing (/chat), Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Purpose, Response formats

### Community 4 - "ppt_chart_engine.py"
Cohesion: 0.13
Nodes (33): _bg_color(), _extract_strict_metric(), _fig_to_bytes(), _hex(), _metrics_to_bar(), _palette_colors(), ppt_chart_engine.py — Dynamic Data-Visualization Engine for JARVIS PPT…, Horizontal or vertical bar chart. (+25 more)

### Community 5 - "dark_video_enhancement.py"
Cohesion: 0.26
Nodes (12): get_all_enhancements(), ndarray, run_pipeline_a(), _enhance_frame(), _get_ffmpeg_binary(), process_video_smartly(), Re-encode a video to H.264 MP4 so browsers can play it., _reencode_to_h264() (+4 more)

### Community 6 - "window_layout.py"
Cohesion: 0.08
Nodes (39): media_state.py — which media app the user used last (Spotify or YouTube)…, True if the Spotify desktop app has a window (cheap: EnumWindows, no UIA)., spotify_running(), close_tab(), focus_window(), Closes the current browser tab using Ctrl+W, targeting the real foreground app., Bring a window to the foreground by partial name match (Win32 API, no…, adjust_active_window() (+31 more)

### Community 7 - "test_protocol.py"
Cohesion: 0.10
Nodes (23): decode_message(), encode_message(), protocol.py — Wire Protocol for Neural Cache (Milestone 2)…, Serialise a dict to the wire format: [4-byte length][UTF-8 JSON body] Args:…, Read exactly one message from a socket, handling partial TCP reads correctly.…, Loop until exactly n bytes have been read from sock. This is necessary because…, _recv_exact(), make_fake_socket() (+15 more)

### Community 8 - "youtube_control.py"
Cohesion: 0.11
Nodes (36): _dur_to_sec(), _end_session(), _find_channel(), _find_channel_at(), walk(), _format_results(), _initial_data(), _load() (+28 more)

### Community 9 - "syllabus_auditor.py"
Cohesion: 0.09
Nodes (35): _approx_token_count(), _assemble_response(), audit_playlist_syllabus(), _build_vector_store(), _chunk_transcript(), _coverage_level(), _embed_texts(), _extract_playlist_id() (+27 more)

### Community 10 - "ppt_studio.py"
Cohesion: 0.09
Nodes (39): Separate the user's command, any pasted/attached content and attachment paths., [(n, heading, raw content)] split on 'Slide N:' markers of repaired text., raw_slide_blocks(), split_request(), choice may be a THEMES key, a legacy palette key, a palette dict, or None…, resolve_theme(), _assign_images(), _caption() (+31 more)

### Community 11 - "DeckRenderer"
Cohesion: 0.14
Nodes (24): _compact_header(), box(), DeckRenderer, fit_size(), _items(), para_h(), place_image(), Header + lead + list inside a column. Returns nothing. (+16 more)

### Community 12 - "browser_tool.py"
Cohesion: 0.20
Nodes (22): browse_and_paginate(), browse_and_read(), _clean_text(), click_element(), _ensure_url(), fill_form(), _llm_extract(), _new_browser_page() (+14 more)

### Community 13 - "LRUCache"
Cohesion: 0.13
Nodes (12): LRUCache, Node, Insert or update a key-value pair. - If key already exists: update value + TTL,…, Remove a key from the cache. Returns True if the key existed, False if it was…, Place node at the MRU (most-recently-used) end of the list., Remove node from its current position in the list (O(1) because doubly-linked)., Evict a specific node (unlink + remove from map)., A doubly-linked list node holding one cache entry. Attributes: key (str): Cache… (+4 more)

### Community 14 - "file_ops.py"
Cohesion: 0.10
Nodes (29): append_file(), bulk_rename(), create_folder(), delete_file(), diff_files(), _fmt_size(), list_directory(), _maybe_summarize() (+21 more)

### Community 15 - "PresentationBuilder"
Cohesion: 0.18
Nodes (18): _clean_image_path(), _get_image_aspect_ratio(), _oval(), _parse_bullet(), _parse_card(), PresentationBuilder, _frame(), Render a single image with CONTAIN-FIT (object-fit: contain). The image is… (+10 more)

### Community 16 - "assignment_answers.py"
Cohesion: 0.12
Nodes (25): _ask_question_on_page(), _find_input(), generate_answer(), generate_answers(), _get_persistent_page(), _groq_answer(), Jarvis Assignment Tool — Phase 2: Answer Generation…, Launch a visible (non-headless) Chromium with a persistent profile. Login… (+17 more)

### Community 17 - "resume_detector"
Cohesion: 0.18
Nodes (14): detect_resume_intent(), _extract_task_resource(), _find_best_task_match(), _has_continuation_verb(), _has_fresh_task_indicator(), _has_reference_phrase(), resume_detector.py — Jarvis Resume Intent Classifier…, Return True if the text contains a strong resume-intent reference phrase. (+6 more)

### Community 18 - "prompt_enhancement_library + skill_prompt_enhancer"
Cohesion: 0.16
Nodes (21): check_for_hallucination(), clean_output(), detect_domain(), is_bloated(), protect_blocks(), prompt_enhancement_library.py…, Replace ``` fenced blocks with [[BLOCK_n]] placeholders., Put protected blocks back; append any the model dropped. (+13 more)

### Community 19 - "prompt_enhancer_button.py"
Cohesion: 0.08
Nodes (33): _acquire_single_instance(), _app_title_match(), _browser_url(), classify_app(), _exe_name(), _has_pattern(), install_autostart(), _is_editable() (+25 more)

### Community 20 - "generate_deck"
Cohesion: 0.11
Nodes (24): _budget_left(), _content_prompt(), _flatten(), _gemini_json(), generate_deck(), _is_note(), run(), take() (+16 more)

### Community 21 - "chat.py"
Cohesion: 0.06
Nodes (41): chat_endpoint(), _dag_stream_with_history(), planner_stream(), response_stream_with_history(), resume_stream(), tool_stream(), ChatRequest, _clean_yt_query() (+33 more)

### Community 22 - "ppt_research.py"
Cohesion: 0.11
Nodes (36): ground_slides(), plan_queries(), 4-6 web queries covering the angles a deck on `topic` needs. Templates, not an…, Web + Wikipedia → verified facts. [] when offline (the deck is then written…, Audit every generated slide; LLM-repair flagged ones with their facts; scrub…, research_facts(), allowed_numbers(), _anchors() (+28 more)

### Community 23 - "ppt_template.py"
Cohesion: 0.06
Nodes (56): prepare_image(), Return a PPTX-safe copy (EXIF-rotated, RGB, ≤2400px, png/jpg) and its aspect., analyze_format(), _analyze_slide(), classify_box(), _clear(), clone_slide(), delete_slide() (+48 more)

### Community 24 - "main.py"
Cohesion: 0.08
Nodes (34): resume_router.py — FastAPI router for the visual resume editor…, get_alerts(), _on_screen_alert(), get, post, Stop watcher, acoustic tripwire, and close DB pool cleanly on server shutdown., Frontend polls this endpoint to receive proactive JARVIS screen alerts. e.g.…, Return current acoustic tripwire state for the frontend toggle. (+26 more)

### Community 25 - "ppt_router.py"
Cohesion: 0.14
Nodes (20): build_ppt(), generate(), create_ppt_backend(), generate(), extract_theme(), get_styles(), PPTBuildRequest, PPTCreateRequest (+12 more)

### Community 26 - "package"
Cohesion: 0.11
Nodes (20): name, private, type, version, autoprefixer, eslint, ref_eslint_config, @eslint/js (+12 more)

### Community 28 - "orchestrator.py"
Cohesion: 0.09
Nodes (35): compile_replica_html(), Main entry point. Returns a complete HTML document string. content : normalised…, resume_replica — Scene-graph-based resume replication engine. Import the public…, build_replica(), compile_replica_html(), _compute_fit_scale(), create_replica_resume(), _data_uri() (+27 more)

### Community 29 - "ppt_image_engine"
Cohesion: 0.16
Nodes (18): build_image_descriptors(), _extract_keywords(), get_aspect_ratio(), ImageDescriptor, match_images_to_slides(), _parse_slide_ref(), _parse_slide_ref_by_title(), ppt_image_engine.py — Semantic Image-Slide Matcher for JARVIS PPT Engine… (+10 more)

### Community 30 - "test_task_resumption.py"
Cohesion: 0.12
Nodes (20): _ensure_ledger_file(), find_resumable_task(), get_recent_tasks(), get_recent_tasks_raw(), _load_ledger(), log_task(), task_ledger.py — Jarvis Task Context Ledger…, Return a formatted string of the last N tasks, suitable for display or speech.… (+12 more)

### Community 31 - "ppt_composer.py"
Cohesion: 0.15
Nodes (38): _balanced_rows(), _body_cards(), _body_fields(), _body_list(), _body_paragraph(), _body_stats(), _body_steps(), _body_table() (+30 more)

### Community 32 - "dsa_enforcer.py"
Cohesion: 0.16
Nodes (11): _cache_del(), _cache_set(), DSAEnforcer, get_dsa_enforcer(), Write to Neural Cache, silently skipping if unavailable., Delete from Neural Cache, silently skipping if unavailable., Flow, selenium (+3 more)

### Community 33 - "ppt_content.py"
Cohesion: 0.10
Nodes (37): apply_edit(), apply_structure(), _as_dated(), _as_stat(), _clauses(), _compact(), _edit_facts(), finalize_slides() (+29 more)

### Community 34 - "gmail_tool.py"
Cohesion: 0.06
Nodes (46): check_emails(), _decode_body(), _format_date(), get_email_body(), _get_gmail_service(), _get_header(), list_unread(), gmail_tool.py — Jarvis Gmail Integration (Step 5)… (+38 more)

### Community 35 - "PromptOverlay"
Cohesion: 0.07
Nodes (13): main(), PromptOverlay, prompt_overlay.py ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Jarvis…, Strip the **ENHANCED PROMPT (CODING):** header if present., Image, keyboard, math, generate_arc_reactor() (+5 more)

### Community 36 - "ui_inspector"
Cohesion: 0.10
Nodes (11): Walk all descendants looking for any control whose window_text contains `text`…, Fire an element's primary action via UIA Invoke pattern. No mouse movement —…, Inject text into an input element via UIA Value pattern. No simulated…, Read text from an element via UIA TextPattern or window_text. Returns empty…, Walk the accessibility tree and return all elements up to `depth` levels. Use…, Core wrapper around pywinauto's UIA backend. All interactions go through the OS…, Get a window wrapper by partial title match (regex-safe). Returns None if not…, Get the currently focused window via Win32 HWND matching. (+3 more)

### Community 37 - "agentic_web.py"
Cohesion: 0.18
Nodes (14): agentic_web_action(), _worker(), _build_search_queries(), _get_api_key(), agentic_web.py — Smart Web Research Engine for Jarvis…, Use the LLM to extract specific listings from the fetched content., Generator that streams progress and final answer., Return known direct listing URLs for a site+task combo. (+6 more)

### Community 38 - "media_sessions.py"
Cohesion: 0.13
Nodes (23): app_kind(), control(), run(), _do(), _filter(), kind_playing(), _label(), media_command() (+15 more)

### Community 39 - "._run"
Cohesion: 0.25
Nodes (7): _generate_chime(), ndarray, Root Mean Square amplitude. Cast to float64 to prevent int16 overflow., FFT-based dominant frequency. Only inspect the positive half-spectrum (0 ……, Return True if this chunk looks like a clap/snap (loud + right frequency)., Main loop — opened inside the thread so PyAudio errors stay contained. State…, Generate a pleasant two-tone wake chime as a float32 numpy array.

### Community 40 - "voice_agent"
Cohesion: 0.13
Nodes (9): AbstractEventLoop, _ClapDetector, _EnergyVAD, ndarray, Queue, Stateful frame-by-frame Silero VAD using the ONNX model bundled with faster-…, Fallback if Silero can't load: adaptive noise floor., Strict double clap. The old tripwire fired on ANY two loud 2–8 kHz frames… (+1 more)

### Community 42 - "CacheServer"
Cohesion: 0.16
Nodes (10): CacheServer, main(), Full startup: recover state, start engine, begin accepting connections., Restore cache state from disk before the engine thread starts. Called on the…, Main thread: bind socket and accept connections indefinitely., Graceful shutdown: take a final snapshot, stop engine, close socket., TCP server that wires incoming connections to the CacheEngine. Each accepted…, live_server() (+2 more)

### Community 43 - "air-drawing + air_drawing_tool"
Cohesion: 0.18
Nodes (9): open_air_drawing(), Opens the Air Drawing Canvas on the screen. This feature allows the user to…, Air drawing (webcam hand drawing), Files & symbols (auto-generated, line numbers are current), Flow, Gotchas, Graphify, Purpose (+1 more)

### Community 44 - "ppt_designer.py"
Cohesion: 0.08
Nodes (31): _lead_h(), Leads are drawn entirely in the semibold heading font — measure them that way., _as_plain_content(), _contrast(), count_lines(), _deep_plain(), E(), _finish_theme() (+23 more)

### Community 45 - "voice.py"
Cohesion: 0.09
Nodes (35): devanagari_to_hinglish(), _sub(), loanword_ratio(), normalize_for_tts(), hinglish_normalizer.py — Devanagari Crash Prevention + Text Normalizer…, One Devanagari word → casual Hinglish roman ("चलाओ" → "chalao", "करना" →…, Share of Devanagari words that are English loanwords ("ओपन क्रोम" → 1.0). High…, Romanize a Devanagari (Hindi) transcript for the backend, keeping any Latin… (+27 more)

### Community 46 - "package + App"
Cohesion: 0.16
Nodes (11): App(), ChatMessage(), API_BASE, frontend_src_index, lucide-react, react, ref_react_dom_client, react-markdown (+3 more)

### Community 47 - "AcousticWakeEngine"
Cohesion: 0.12
Nodes (9): AcousticWakeEngine, Background thread that watches the microphone for a double-clap pattern. Usage…, Start the background listening thread., Signal the background thread to exit and wait for it., Resume detection after a disable()., Pause detection without stopping the thread (fast resume)., Signal the background thread to re-run calibration on the next cycle. Returns…, Override the volume threshold (used by voice_agent inline mode). (+1 more)

### Community 48 - "assignment_humanizer.py"
Cohesion: 0.12
Nodes (25): _extract_output_text(), _fill_input(), _find_element(), _get_browser_page(), humanize_all_answers(), _humanize_chunk_via_browser(), humanize_text(), _humanize_via_browser() (+17 more)

### Community 49 - "message_reader.py"
Cohesion: 0.15
Nodes (18): _bring_whatsapp_to_front(), _get_whatsapp_window(), _heuristic_parse_ocr_lines(), _parse_uia_message_string(), message_reader.py — Jarvis WhatsApp Intelligence: Message Reader…, Restores and focuses WhatsApp window. Returns True on success., Walks the WhatsApp UIA accessibility tree to extract messages. WhatsApp Desktop…, Parses a raw UIA ListItem Name string into a structured message dict.… (+10 more)

### Community 50 - "CacheClient"
Cohesion: 0.06
Nodes (27): Design, Files & symbols (auto-generated, line numbers are current), Graphify, Neural cache (Redis-like LRU server), Purpose, Runtime, Tests, CacheClient (+19 more)

### Community 52 - "Clip"
Cohesion: 0.13
Nodes (12): Clip, prewarm(), PCM (int16, 24 kHz) that fills while synthesis streams; playable immediately., hi' → Hindi voice, 'en' → English voice, for one sentence., Begin synthesising `text` now; returns a Clip that can be played while it fills., Synthesise short stock phrases (greetings, acks) into the cache for instant…, route_language(), _sapi_sync() (+4 more)

### Community 53 - "package"
Cohesion: 0.14
Nodes (14): devDependencies, autoprefixer, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, postcss (+6 more)

### Community 55 - "repair.py"
Cohesion: 0.09
Nodes (23): apply_diff_patches(), compute_visual_diff(), _images_to_base64_pair(), _parse_diff_json(), _patch_fill(), repair.py — Visual diff and bounded repair loop. Runs after an initial render…, Sends both images to the VLM and asks it to describe differences. Returns a…, Converts VLM diffs into structured patches and applies them to the replica_doc.… (+15 more)

### Community 56 - "llm.py"
Cohesion: 0.06
Nodes (49): classify_context(), detect_language(), context_classifier.py — Jarvis Situational Awareness…, Detect whether the user spoke English, Hinglish, or Hindi. Returns: 'english' —…, Classify the situation from user input. Returns a dict with keys: urgency :…, check_for_tool_intent(), generate_chat_response(), _groq_generate() (+41 more)

### Community 57 - "time"
Cohesion: 0.16
Nodes (11): find_controls(), Dump WhatsApp Desktop UI tree to find the Voice Call button name. Run this…, search_tree(), Find the Voice Call button position in WhatsApp Desktop window. Run this while…, Step 1: Open WhatsApp, go to any chat (e.g. Archit Shukla) Step 2: Hover your…, pyautogui, pygetwindow, pywinauto (+3 more)

### Community 58 - "create_resume"
Cohesion: 0.09
Nodes (35): get, post, resume_editor(), resume_save(), _apply_op(), _attachments(), _clean_free(), create_resume() (+27 more)

### Community 59 - "web_search.py"
Cohesion: 0.18
Nodes (15): research_scraper.py — Autonomous Web Research Scraper…, _duckduckgo_search(), _format_ddg_results(), web_search.py — Jarvis Reliable Web Search (Step 3)…, PRIMARY PUBLIC FUNCTION — used by get_info() in tools.py. Enhanced with: -…, Use a fast LLM call to synthesize multiple search sources into a single…, Search DuckDuckGo using direct HTML scraping (faster, no brittle dependencies).…, Convert DDG result list into a clean readable string for the LLM. (+7 more)

### Community 60 - "content_humanizer + content-tools"
Cohesion: 0.09
Nodes (34): build_structure_prompt(), build_vocab_prompt(), call_groq(), check_similarity(), detect_tone(), fact_check(), get_groq_client(), get_sentence_scores() (+26 more)

### Community 61 - "os"
Cohesion: 0.10
Nodes (21): NLPExtractor, nlp_extractor.py — LLM-Powered Fact & Entity Extractor…, Runs extraction on each scraped source and aggregates the results. Returns a…, research_pipeline.py — End-to-End Autonomous Research Orchestrator…, Scrapes the web for a topic and extracts verified facts and statistics. Yields…, research_topic(), _count_pages_and_fill(), _launch_browser() (+13 more)

### Community 62 - "Voice: STT, TTS, wake word, clap wake, overlay"
Cohesion: 0.08
Nodes (22): Sets a reminder that Jarvis will speak after a given number of seconds., set_reminder(), preload_local_stt(), _load(), Load the local Whisper models in the background (voice agent startup)., Feed streamed tokens; get back speakable sentences as early as possible., Speak a complete text. All sentences synthesise in parallel, play in order., Speak an async generator of text chunks, sentence by sentence, pipelined. (+14 more)

### Community 63 - "PowerPoint generator"
Cohesion: 0.13
Nodes (13): ppt_edit(), Follow-up edit of the last deck (generator). See ppt_studio.edit., _ppt_edit(), Generator wrapper — follow-up edits of the last deck ("on slide 3 …", "make it…, Entry points, Files & symbols (auto-generated, line numbers are current), Flow — edit (`ppt_edit` → `ppt_studio.edit` → `ppt_content.apply_edit`), Graphify (+5 more)

### Community 64 - "2. Tool Registry (`tools.py`)"
Cohesion: 0.07
Nodes (39): close_window(), create_word_doc(), get_system_time(), lock_screen(), open_app(), open_windows_copilot(), Returns current date and time naturally., Closes the current active real app window (skips the Jarvis overlay). (+31 more)

### Community 65 - "Architecture"
Cohesion: 0.13
Nodes (13): Architecture, Frontend (`frontend/src`), HTTP endpoints, LLM usage, Memory layers (five separate stores), Processes, Files & symbols (auto-generated, line numbers are current), Gotchas (+5 more)

### Community 67 - "Flow — create (`ppt_tool.ppt_create` → `ppt_studio.create`, a generator)"
Cohesion: 0.11
Nodes (28): architect_slides(), ask(), _retry(), run(), _complete_from_source(), deck_facts(), detect_profile(), extractive_ok() (+20 more)

### Community 68 - "spotify_service.py"
Cohesion: 0.12
Nodes (29): _buttons(), _clean_query(), _com_init(), _content_play_buttons(), _is_playing(), _mark_last(), _now_playing_title(), _page_matches() (+21 more)

### Community 69 - "prompt_enhancer_button"
Cohesion: 0.14
Nodes (4): EnhanceButton, Move (and optionally show) without ever activating the window; Tk's deiconify()…, Default spot: just above the prompt box's top-right corner; below it or inside…, _save_state()

### Community 70 - "Speaker"
Cohesion: 0.11
Nodes (11): hinglish_to_devanagari(), Rewrite the Hindi words of a romanized Hinglish sentence in Devanagari, leaving…, Channel, The speech stream of one command's reply., Plays sentences from many Channels without overlap: - urgent phrases (acks,…, Barge-in "stop": silence now and drop everything queued., Did the mic just hear Jarvis himself (speaker → mic bleed)? Echo comes back…, Next (channel, text, lang) or None. Non-blocking. (+3 more)

### Community 72 - "Gotchas"
Cohesion: 0.18
Nodes (10): _mail_tool(), Email tools: try the real Gmail API (gmail_tool) first, fall back to opening…, Email, Adding a tool (checklist), Calling tools from code, Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify (+2 more)

### Community 73 - "test_lru"
Cohesion: 0.20
Nodes (5): Accessing 'a' should move it to MRU and save it from eviction., Re-setting an existing key should move it to MRU., len(cache.map) must never exceed capacity., Fill to capacity+1. The first key inserted (LRU) should be evicted., TestEviction

### Community 74 - "assignment_tool.py"
Cohesion: 0.12
Nodes (23): _classify_question_type(), _clean_text(), _extract_marks(), _extract_via_llm_text(), _extract_via_vision(), _has_figure_reference(), _parse_llm_json_response(), _pdf_pages_to_images() (+15 more)

### Community 75 - "refresh_docs.py"
Cohesion: 0.27
Nodes (10): fnmatch, auto_block(), _js_symbols(), label_communities(), Path, _py_symbols(), refresh_docs.py — keep docs/features/*.md and the graphify graph in sync with…, Name each graph community after its dominant source file(s) (no LLM). (+2 more)

### Community 76 - "reply_generator.py"
Cohesion: 0.08
Nodes (31): generate_reply_draft(), Open a WhatsApp chat, read the last N messages, and return a structured thread…, Read the latest WhatsApp thread with a contact and generate 3 reply drafts that…, Send one of the reply drafts generated by generate_reply_draft. draft_index is…, read_whatsapp_thread(), send_style_reply(), _build_system_prompt(), _build_user_prompt() (+23 more)

### Community 77 - "Element"
Cohesion: 0.10
Nodes (13): Element, element_from_handle(), focused_element(), uia_local.py — thread-safe UI Automation access (helper, not a tool)…, This thread's IUIAutomation (COM initialised for the thread on first use)., Minimal pywinauto-style wrapper around an IUIAutomationElement., Rect, uia() (+5 more)

### Community 78 - "WALWriter"
Cohesion: 0.09
Nodes (15): Any, Path, Queue, Flush and close the file handle cleanly on server shutdown., Manages periodic full-state snapshots. The snapshot itself is triggered through…, Serialise cache state to disk and truncate the WAL. Called by CacheEngine on…, Load the snapshot from disk. Returns None if no snapshot exists yet. Called…, Start a daemon thread that enqueues a SNAPSHOT command every interval_seconds.… (+7 more)

### Community 79 - "memory/memory.py"
Cohesion: 0.17
Nodes (14): find_skill(), format_preferences_for_prompt(), get_all_preferences(), Jarvis Vector Memory — ChromaDB-based long-term memory engine. Stores and…, Returns a string suitable for injecting into LLM prompts., Stable short ID based on content hash., Persist a successful dynamic skill for future reuse., Returns up to n most relevant saved skills for a given task description. Each… (+6 more)

### Community 80 - "package"
Cohesion: 0.22
Nodes (9): dependencies, framer-motion, lucide-react, react, react-dom, react-markdown, react-syntax-highlighter, remark-gfm (+1 more)

### Community 81 - "handTracking"
Cohesion: 0.31
Nodes (3): CameraView(), getHandsConstructor(), HandTracker

### Community 82 - ".process_chunk"
Cohesion: 0.40
Nodes (4): _play_chime(), Inline (shared-stream) mode — called by voice_agent.py on every audio frame it…, Play the wake chime via sounddevice (non-blocking from caller's perspective)., Voice path (`scripts/voice_agent.py`)

### Community 83 - "screen_vision.py"
Cohesion: 0.05
Nodes (60): _accessibility_tree(), describe_screen_for_llm(), get_screen_screenshot_b64(), _groq_vision_screen(), _init_tesseract(), _ocr_screen(), screen_reader.py — Jarvis Screen Vision (VLM-first architecture)…, Legacy OCR layer. Works on any app but extracts raw text only — no layout,… (+52 more)

### Community 84 - "safe_executor.py"
Cohesion: 0.14
Nodes (16): execute_safe(), Exception, Safe Code Executor for Jarvis ------------------------------- Runs LLM-…, Restricted open(): blocks writes to system paths., Restricted __import__: blocks dangerous modules., Raised when generated code violates safety constraints., AST visitor that inspects generated code before execution., Parse and walk the AST, raising SecurityError on violations. (+8 more)

### Community 85 - ".load_snapshot"
Cohesion: 0.29
Nodes (4): Any, Serialise the entire live cache to a plain dict. Expired entries are excluded —…, Restore cache state from a snapshot dict (produced by snapshot()). Called once…, Place node at the LRU (least-recently-used) end of the list.

### Community 86 - "ControlPanel + HandSkeleton"
Cohesion: 0.13
Nodes (13): frontend_src_airdrawing_airdrawing, COLORS, ControlPanel(), FONTS, SHAPES, FINGERTIP_INDICES, HAND_CONNECTIONS, HandSkeleton() (+5 more)

### Community 88 - "ppt_chart_engine"
Cohesion: 0.33
Nodes (3): ChartEngine, Stateless chart renderer. All colors are derived from the active PPT palette —…, Render a chart from structured data. Args: chart_data: {"type": "bar",…

### Community 89 - "compiler.py"
Cohesion: 0.11
Nodes (21): _commands_to_d(), _compile_document_css(), _compile_frame(), _compile_path(), _fill_to_css_background(), _fill_to_svg_fill(), _mm_to_pt(), _parametric_to_commands() (+13 more)

### Community 90 - "smart_navigator.py"
Cohesion: 0.24
Nodes (10): _get_api_key(), _llm_extract(), smart_navigator.py — Isolated Smart Web Navigator for Jarvis…, Attempt to find the GROQ API key safely., Pass scraped text through LLM for structured extraction., Resolve a verbal site name like 'unstop' to a URL like 'https://unstop.com'., Resolves site name, opens a VISIBLE browser, and performs a search or action…, _resolve_url() (+2 more)

### Community 91 - "prompt_enhancer_button"
Cohesion: 0.21
Nodes (11): _box_contains(), _box_set_value(), _clip_get(), _clip_set(), _ctrl(), _focus(), _focused_text(), _norm() (+3 more)

### Community 92 - "typing"
Cohesion: 0.14
Nodes (15): argparse, neural_cache, client.py — Python Client Library for Neural Cache (Milestone 5)…, engine.py — Single-Writer Command Queue (Milestone 3)…, lru.py — Hand-rolled LRU Cache (Milestone 1)…, persistence.py — WAL + Snapshot for Neural Cache (Milestone 6)…, server.py — TCP Accept Loop for Neural Cache (Milestone 4)…, One thread per connected client. Reads commands, enqueues them to the engine,… (+7 more)

### Community 94 - "re"
Cohesion: 0.12
Nodes (15): assemble_assignment(), _create_powerpoint(), _create_word_doc(), _parse_qa_json(), Jarvis Assignment Tool — Phase 4: Document Assembly…, Assemble the extracted/humanized questions and answers into a formatted…, Extract and parse the JSON array from the input string., add_human_prosody() (+7 more)

### Community 95 - "calendar_tool.py"
Cohesion: 0.12
Nodes (18): add_event(), check_today_schedule(), _get_calendar_service(), get_upcoming_events(), calendar_tool.py — Jarvis Google Calendar Integration (Step 8)…, Create a new event in Google Calendar. - title: "Project Meeting" - date:…, Authenticate and return a Google Calendar API service object., List events in the next N days. (+10 more)

### Community 96 - "CODEMAP"
Cohesion: 0.22
Nodes (8): Backend core & API, Code map, Frontend (`frontend/src`, React 19 + Vite + Tailwind 4), Ignore these (no runtime role), Neural cache (neural_cache/, see its README.md), Scripts, Services (app/services), WhatsApp intelligence (app/services/whatsapp_intelligence)

### Community 97 - "youtube_player.py"
Cohesion: 0.09
Nodes (54): _address_bar_value(), _clip_get(), _clip_restore(), _clip_set(), com_init(), current_video_info(), _fallback(), fmt_span() (+46 more)

### Community 98 - "_compile_section"
Cohesion: 0.18
Nodes (18): _compile_chart(), _compile_section(), _it(), Simple <ul><li> list of skill names., High-level section renderer. Returns complete HTML for the section (heading +…, Returns data-item attribute string in edit mode, else empty string., Compiles a CHART node to the appropriate skill/language visualisation., Progress bar skills. Supports 2-column CSS grid. (+10 more)

### Community 99 - "_compile_node"
Cohesion: 0.15
Nodes (14): _compile_image(), _compile_node(), _compile_rule(), _compile_text(), _initials_block(), Returns the initials text for the photo placeholder., Converts a TEXT_STYLE dict to a CSS properties string., Dispatches to the appropriate node compiler based on node['type']. (+6 more)

### Community 100 - "rag_memory.py"
Cohesion: 0.07
Nodes (45): aiomysql, close_mysql(), get_mysql_pool(), init_mysql(), mysql_db.py — Jarvis Async MySQL Connection Pool…, Gracefully close the MySQL connection pool on server shutdown., Return the shared MySQL connection pool, initializing it if needed., Initialize the MySQL connection pool and ensure all required tables exist. Safe… (+37 more)

### Community 101 - "render_sections"
Cohesion: 0.13
Nodes (21): _fill(), image_block(), _image_panel(), _masonry(), How much extra height a section can absorb before it looks inflated., Framed images (no crop) + numbered captions under each. Returns used height., Boxes for the images at full column width in exactly `rows` rows (scaled down…, Balanced split of sections into columns (reading order kept inside each… (+13 more)

### Community 102 - "package"
Cohesion: 0.40
Nodes (5): scripts, build, dev, lint, preview

### Community 103 - "schema.py"
Cohesion: 0.15
Nodes (13): make_default_replica_document(), make_group_node(), make_page_node(), make_parametric_geometry(), make_text_node(), schema.py — Scene-graph node types, constants, and factory helpers. A Replica…, Returns a complete PAGE node., Returns a complete GROUP node. (+5 more)

### Community 105 - "prompt-enhancer + prompt_enhancer_button"
Cohesion: 0.22
Nodes (10): _hint_text(), _ide_allows(), is_prompt_box(), In IDEs only chat / agent inputs qualify, never the code editor, the terminal,…, Entry points, Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify (+2 more)

### Community 106 - "ppt_tool.py"
Cohesion: 0.13
Nodes (23): _auto_select_image_layout(), _bg_fill(), _c(), _corner_L(), _detect_purpose(), extract_theme_from_image(), _groq_call(), _normalize_and_recover() (+15 more)

### Community 107 - "assignment_pipeline.py"
Cohesion: 0.08
Nodes (34): _browser_thread(), do_assignment(), _find_el(), _get_answer(), _get_browser_ctx(), _groq_answer(), _groq_humanize(), _humanize_browser() (+26 more)

### Community 108 - "_measure_frame"
Cohesion: 0.11
Nodes (27): _apply_color(), _contrast(), _css(), _css_extra(), _design_set(), _faces(), _lum(), _measure_band() (+19 more)

### Community 109 - "2. The new approach: measure, label, calibrate, transfer, verify"
Cohesion: 0.15
Nodes (12): _balance_columns(), Greedy: move the section that most reduces the taller column, until no move…, 2. The new approach: measure, label, calibrate, transfer, verify, 3. Fidelity contract (acceptance numbers), 6. Test harness (makes "exact" measurable and keeps it from regressing), 7. Milestones (each ends with a measurable exit check), Plan: exact design replication for the resume creator, Step 0: Ingest and harden the input (+4 more)

### Community 110 - "bindings.py"
Cohesion: 0.15
Nodes (11): build_editor_path_map(), format_binding_value(), iter_content_items(), bindings.py — Content binding resolution and editor path mapping. Binding paths…, Walks the scene graph and builds a map from binding path -> list of node IDs…, Iterator for repeat bindings. Yields (index, item) for each item in the list at…, Returns the display title for a section, checking content['section_titles']…, Resolves a binding path against content dict. Returns the value at that path,… (+3 more)

### Community 111 - "_ef"
Cohesion: 0.23
Nodes (12): _compile_repeat(), _ef(), Renders a single experience entry (same format as legacy builder's…, Renders a single education entry., Renders a single project entry (same format as legacy builder's _projects_html)., Renders the contact section with icons., Returns escaped text in normal mode, or a contenteditable span in edit mode.…, Compiles a REPEAT node by iterating content[binding] and rendering items. (+4 more)

### Community 112 - "README"
Cohesion: 0.50
Nodes (3): Expanding the ESLint configuration, React Compiler, React + Vite

### Community 119 - "_Player"
Cohesion: 0.15
Nodes (6): get_player(), _Player, ndarray, One persistent 24 kHz output stream driven by a callback that pulls from a…, Loudest output RMS in the last `window` s — the voice agent's echo reference., Play a clip as it arrives. Returns False if interrupted.

### Community 120 - "Neural Cache"
Cohesion: 0.20
Nodes (9): Architecture, Benchmark, Files, LRU Cache Design, Neural Cache, Persistence, Running, Tests (+1 more)

### Community 122 - "Flow"
Cohesion: 0.11
Nodes (24): _analyse_design(), _apply_layout_answer(), _closest_preset(), _crop_photo(), _grow_photo_box(), _image_b64(), _merge_design(), _palette() (+16 more)

### Community 124 - "voice_agent"
Cohesion: 0.33
Nodes (3): MicListener, Initial ambient noise floor (kept up to date on every non-speech frame)., One 32 ms frame → clap check + VAD state machine → events.

### Community 125 - "Content fidelity & page limits (2026-10-02)"
Cohesion: 0.12
Nodes (26): _apply_layout_hint(), _build_content(), _condense_content(), _content_brief(), _drop_invented(), clean_text(), ok(), _finalize_content() (+18 more)

### Community 126 - "_e"
Cohesion: 0.18
Nodes (9): _compile_group(), _e(), Radar/spider chart as inline SVG. 100x100 viewBox, center (50,50), max radius…, Tags where size/opacity indicates level (higher → larger/more saturated)., Renders a single ring/donut chart SVG for a skill., Compiles a GROUP node to a <div>. Used for section headings and composites., _render_radar(), _render_tag_level() (+1 more)

### Community 127 - "CacheEngine"
Cohesion: 0.15
Nodes (13): CacheEngine, Any, Route a command dict to the appropriate handler. All handlers return a response…, Owns the LRUCache. Runs a single consumer loop on a dedicated thread. External…, Spawn the single writer thread. Call once at server boot., Gracefully stop the engine writer thread., The single consumer loop. Runs on CacheEngineThread. Processes one command at a…, err_response() (+5 more)

### Community 128 - "search_site"
Cohesion: 0.20
Nodes (11): Search for a query within a specific website using DuckDuckGo site: operator., Read and extract readable text content from a specific URL., scrape_url_tool(), search_site_tool(), _clean_html_text(), Parse HTML and extract readable text. Removes scripts, styles, navbars,…, PUBLIC TOOL: Read and extract readable text from any URL. Called when user says…, PUBLIC TOOL: Search for a query within a specific website. Uses DuckDuckGo with… (+3 more)

### Community 129 - "Open"
Cohesion: 0.20
Nodes (11): _fetch_results(), _parse_videos(), add(), walk(), Collect videos from ytInitialData: classic videoRenderer (search) and the newer…, Scrape YouTube's results page → [{id,title,channel,duration,seconds,views}]; []…, 1,234,567 views' / '82 million views' / '1.2M' → int., _views() (+3 more)

### Community 130 - "voice_agent.py"
Cohesion: 0.08
Nodes (27): app_services, language_mismatch(), True if a reply sentence is in the other language than the one the user spoke., Strict check used when there is no wake word to vouch for the audio., AsyncClient, difflib, Flow (`scripts/voice_agent.py`), httpx (+19 more)

### Community 131 - "thread_extractor.py"
Cohesion: 0.20
Nodes (9): _find_latest_incoming(), _get_current_chat_title(), _group_into_turns(), _open_contact_chat(), thread_extractor.py — Jarvis WhatsApp Intelligence: Thread Extractor…, Merges consecutive messages from the same sender into a single turn. This makes…, Scans the thread from the end to find the most recent message from 'them' —…, Opens a specific contact's chat using Ctrl+N → paste → Enter. Mirrors the exact… (+1 more)

### Community 132 - "dag_executor.py"
Cohesion: 0.07
Nodes (51): _semantic_window_adjust(), Settings, app_memory, _call_dag_planner(), DAGNode, _execute_node(), is_dag_task(), dag_executor.py — Jarvis DAG-Based Multi-Step Agent Planner… (+43 more)

### Community 133 - "resume_builder.py"
Cohesion: 0.09
Nodes (54): _competencies_html(), _contact_html(), _custom_section_html(), _data_uri(), _decor_html(), _e(), _editor_meta(), shown() (+46 more)

### Community 134 - "database.py"
Cohesion: 0.33
Nodes (7): get_db_pool(), init_db(), Queries the table and uses the pgvector cosine distance operator (<=>) to fetch…, Inserts text chunks and vectors into the knowledge_store table., save_document_chunk(), search_similar_chunks(), asyncpg

### Community 135 - "acoustic_tripwire.py"
Cohesion: 0.22
Nodes (7): calibrate_tripwire(), get_wake_event(), acoustic_tripwire.py — Jarvis Acoustic Wake Engine…, Return the threading.Event that the engine sets on a double-clap., Sample ambient noise for `sample_seconds`, calculate the mean RMS, then set…, Event, numpy

### Community 138 - "pathlib"
Cohesion: 0.22
Nodes (8): check_emails(), _get_api_key(), list_unread(), browser_mail.py — Standard Browser Mail Automation…, A generic tool to perform any mail task (like sending or reading) by pre-…, smart_mail_action(), pathlib, webbrowser

### Community 139 - "ui_inspector.py"
Cohesion: 0.06
Nodes (41): flow_stream(), click_ui_element_uia(), dump_app_ui_tree(), Get all readable text from the currently active window., Click a UI element inside an app by AutomationId, name, or control type. Does…, Inject text into a specific input field in an app via UIA Value pattern. No…, Read the current text content of a UI element — e.g. a terminal output pane, a…, Dump the full Windows UI Automation accessibility tree of an app window. Use… (+33 more)

### Community 140 - "benchmark.py"
Cohesion: 0.13
Nodes (10): JSONFileBaseline, main(), measure_latency(), measure_throughput(), benchmark.py — Neural Cache vs JSON-file Baseline (Milestone 8)…, Spin up n_threads threads each doing ops_per_thread SET+GET pairs. Returns…, Mimics memory_tool.py's approach: every read/write touches disk. Uses a…, Run op_fn warmup times (discard), then timed times (measure). Returns (mean_µs,… (+2 more)

### Community 141 - "dark_enhancement.py"
Cohesion: 0.39
Nodes (7): _apply_gamma(), _fusion_and_polish(), _normalize_to_8bit(), _path_1_retinex(), _path_2_wavelet(), run_pipeline_b(), pywt

### Community 142 - "whatsapp"
Cohesion: 0.33
Nodes (5): Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Purpose, WhatsApp: send, call, read, reply-style cloning

### Community 143 - "._list_grid"
Cohesion: 0.22
Nodes (6): _best_window(), Start fraction of the window (length=keep fraction) with most detail, biased to…, Largest body size so all items fit in (w,h). style: 'stack'|'inline'., Row-aligned multi-column list: item i sits in row i//cols, so rows line up., _runs_for(), Layout engine (`ppt_designer.py`)

### Community 144 - "parse_youtube_followup"
Cohesion: 0.11
Nodes (17): _media_intent_for(), Media tool intent for one clause (YouTube-mode parser first, then keyword…, _channel_name(), _is_positional(), _latest_of(), parse_youtube_followup(), True if some browser window's active tab is YouTube., A pick by position, not by title: 'the first result', 'number 3', 'the latest… (+9 more)

### Community 145 - "ppt_tool"
Cohesion: 0.50
Nodes (4): compute_split_geometry(), Computed image + text zone dimensions (in EMU — python-pptx native)., Dynamically compute left-text / right-image split geometry. The split ratio…, SlotGeometry

### Community 146 - "api/memory.py"
Cohesion: 0.07
Nodes (36): forget_memory(), ForgetRequest, get_history(), ingest_memory(), IngestRequest, memory_stats(), BaseModel, delete (+28 more)

### Community 148 - "test_lru"
Cohesion: 0.50
Nodes (3): Return average time per (set + get) operation in microseconds., Per-op time for N=1000 vs N=100000 should be within 3x of each other. If the…, TestO1Timing

### Community 149 - "_llm_json"
Cohesion: 0.33
Nodes (9): _edit_content(), _gemini(), _groq(), _llm_json(), _parse_json(), Fallback when Groq is rate-limited (its vision model has a 200k tokens/DAY cap)., _vision(), Single vision call: tries Groq first, falls back to Gemini. (+1 more)

### Community 150 - "test_lru.py"
Cohesion: 0.18
Nodes (7): large_cache(), fixture, test_lru.py — Unit tests for neural_cache.lru (Milestone 7)…, LRU cache with capacity 3 — easy to reason about eviction., small_cache(), TestSentinels, pytest

### Community 151 - "make_frame_node"
Cohesion: 0.25
Nodes (8): make_frame_node(), make_no_fill(), make_padding(), make_path_node(), Returns {"type": "none"}, Returns a complete FRAME node., Returns a complete PATH node., Returns {"top_mm": ..., "right_mm": ..., "bottom_mm": ..., "left_mm": ...}

### Community 152 - "_fetch_page_text"
Cohesion: 0.29
Nodes (4): _fetch_page_text(), __init__(), Download a page and return clean readable text (no HTML tags)., fetch_one()

### Community 154 - "_find_spotify_window"
Cohesion: 0.33
Nodes (6): _close_spotify(), _find_spotify_window(), _cb(), Quit the Spotify app: WM_CLOSE its windows, then end the process if it only hid…, UIA element of the Spotify main window (visible, titled), or None. Uses…, _spotify_pids()

### Community 155 - "parse_player_command"
Cohesion: 0.33
Nodes (7): _num(), parse_clock(), parse_duration(), parse_player_command(), Map a spoken player command to (action, amount, value), or None. `t` should…, 10 minutes' → 600, '1 hour 5 min' → 3900, 'half a minute' → 30, '90 s' → 90.…, 5:30' → 330, '1:02:03' → 3723, 'to 5 30' → 330. None if absent.

### Community 156 - "DSA / LeetCode enforcer mode"
Cohesion: 0.29
Nodes (6): Data, DSA / LeetCode enforcer mode, Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Purpose

### Community 158 - "Syllabus auditor (YouTube playlist vs syllabus)"
Cohesion: 0.29
Nodes (6): Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Purpose, Syllabus auditor (YouTube playlist vs syllabus), Triggers

### Community 160 - "ppt_create"
Cohesion: 0.33
Nodes (6): ppt_create(), PPT v6 entry point → ppt_studio.create (adaptive layouts, strict user content,…, _ppt_create(), Generator wrapper — streams live progress to the frontend via chat.py's…, Phase 3: Autonomous Research Aggregator. Scrapes live facts from the web,…, _research_and_create_ppt()

### Community 161 - "_render_competency_item"
Cohesion: 0.33
Nodes (6): _guess_icon(), _icon_svg(), Renders a single competency as an icon+title+description card., Returns an inline SVG icon using the _ICONS dict., Guesses an icon name from a competency title string., _render_competency_item()

### Community 162 - "Dark image/video enhancement"
Cohesion: 0.40
Nodes (4): Dark image/video enhancement, Files & symbols (auto-generated, line numbers are current), Graphify, Purpose

### Community 163 - "Web search, research & browser automation"
Cohesion: 0.40
Nodes (4): Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Web search, research & browser automation

### Community 164 - "make_image_node"
Cohesion: 0.50
Nodes (4): make_image_node(), make_size(), Returns a complete IMAGE node., Returns size dict, only including non-None values.

### Community 165 - "_collect_google_fonts"
Cohesion: 0.67
Nodes (3): _collect_google_fonts(), _walk(), Scans the scene graph and style registry for font families. Returns a Google…

## Knowledge Gaps
- **162 isolated node(s):** `Settings`, `name`, `private`, `version`, `type` (+157 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1513 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **32 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Tool registry` connect `Tool registry` to `search_site`, `dark_video_enhancement.py`, `window_layout.py`, `youtube_control.py`, `syllabus_auditor.py`, `pathlib`, `ui_inspector.py`, `browser_tool.py`, `file_ops.py`, `assignment_answers.py`, `api/memory.py`, `prompt_enhancement_library + skill_prompt_enhancer`, `chat.py`, `test_task_resumption.py`, `ppt_create`, `gmail_tool.py`, `agentic_web.py`, `air-drawing + air_drawing_tool`, `assignment_humanizer.py`, `create_resume`, `content_humanizer + content-tools`, `Voice: STT, TTS, wake word, clap wake, overlay`, `PowerPoint generator`, `2. Tool Registry (`tools.py`)`, `spotify_service.py`, `reply_generator.py`, `smart_navigator.py`, `re`, `calendar_tool.py`, `assignment_pipeline.py`?**
  _High betweenness centrality (0.144) - this node is a cross-community bridge._
- **Why does `open_air_drawing()` connect `air-drawing + air_drawing_tool` to `Tool registry`?**
  _High betweenness centrality (0.109) - this node is a cross-community bridge._
- **Are the 122 inferred relationships involving `Tool registry` (e.g. with `keyword_detect_tool()` and `_media_compound()`) actually correct?**
  _`Tool registry` has 122 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `chat_endpoint()` (e.g. with `describe_screen_for_llm()` and `get_screen_text_summary()`) actually correct?**
  _`chat_endpoint()` has 8 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Settings`, `name`, `private` to the rest of the system?**
  _162 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Tool registry` be split into smaller, more focused modules?**
  _Cohesion score 0.02966547443719756 - nodes in this community are weakly interconnected._
- **Should `style_profiler.py` be split into smaller, more focused modules?**
  _Cohesion score 0.11904761904761904 - nodes in this community are weakly interconnected._