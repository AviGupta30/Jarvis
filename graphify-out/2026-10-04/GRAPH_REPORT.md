# Graph Report - Jarvis  (2026-10-04)

## Corpus Check
- 226 files · ~358,337 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 3, .css 3, .bat 1)

## Summary
- 3859 nodes · 8359 edges · 177 communities (150 shown, 27 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 831 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f582a868`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Tool registry
- reply_generator.py
- analyzer.py
- plate.py
- ppt_chart_engine
- content_humanizer + content-tools
- window_layout.py
- Resume creator
- youtube_control.py
- syllabus_auditor
- ppt_studio.py
- DeckRenderer
- browser_tool.py
- LRUCache
- file_ops.py
- PresentationBuilder
- assignment_answers.py
- resume_builder.py
- fontmatch.py
- prompt_enhancer_button
- _sanitize_design
- Jarvis — Claude Code guide
- ppt_research
- ppt_template.py
- create_resume
- ppt_router.py
- package
- gestureController + gestureInterpreter
- orchestrator.py
- ppt_image_engine
- rag_memory.py
- ppt_composer.py
- DSAEnforcer
- ppt_content.py
- WALWriter
- PromptOverlay
- ui_inspector
- agentic_web.py
- exact_render.py
- pipeline.py
- memory/memory.py
- transformEngine
- editor_save
- air-drawing + air_drawing_tool
- ppt_designer.py
- voice.py
- package + App
- acoustic_tripwire
- render_sections
- _verbatim
- CacheClient
- interactionEngine + DrawingCanvas
- calendar_tool.py
- package
- strokeManager
- stream_chat
- llm.py
- skill_prompt_enhancer.py
- dark_enhancement.py
- web_search.py
- execute_safe
- Node
- dag_executor.py
- edit
- whatsapp_smart.py
- frontend
- shapeManager
- Flow — create (`ppt_tool.ppt_create` → `ppt_studio.create`, a generator)
- spotify_service.py
- prompt_enhancer_button
- voice
- drawingEngine
- jarvis_overlay.py
- test_lru
- Gotchas
- _humanize_via_browser
- recall
- Element
- _worker
- gmail_tool.py
- package
- handTracking
- chat.py
- screen_reader.py
- apply_diff_patches
- Flow (`scripts/voice_agent.py`)
- ControlPanel + HandSkeleton
- strokeRefiner
- ppt_chart_engine
- compiler
- ingest
- measure.py
- assignment_humanizer.py
- database.py
- Assignment solver (5 phases)
- walk_nodes
- youtube_player.py
- compiler
- compiler
- init_rag_memory
- detect_resume_intent
- package
- schema.py
- hinglish_normalizer.py
- time
- ppt_tool.py
- assignment_pipeline.py
- api/memory.py
- CacheEngine
- bindings.py
- compiler
- README
- README
- __init__
- README
- config.py
- resume_router.py
- PROMPT_TEMPLATE
- extract_questions
- FEATURES
- _Player
- Content fidelity & page limits (2026-10-02)
- compiler
- Gotchas
- dsa_enforcer.py
- main.py
- Known issues
- refresh_docs.py
- os
- ppt_studio
- make_frame_node
- ppt_tool
- edge_tts
- pygame
- browser_mail.py
- .render
- Screen understanding & UI automation
- prompt_enhancer_button
- Chat pipeline & routing (/chat)
- DSA / LeetCode enforcer mode
- neural-cache
- voice_agent
- startup_event
- _photo_edges
- assemble_assignment
- make_solid_fill
- TestBasicOps
- ssml_processor.py
- Agents: DAG executor, linear planner, dynamic skills
- smart_navigator.py
- prompt-enhancer + prompt_enhancer_button
- Memory: RAG, facts, task ledger, resume, skills
- test_lru
- assignment_tool.py
- _straight_edges
- ResearchScraper
- Voice: STT, TTS, wake word, clap wake, overlay
- compiler
- CODEMAP
- _watcher_loop
- TestTTL
- compiler
- TestO1Timing
- TestSentinels
- make_image_node
- small_cache
- .snapshot
- make_commands_geometry
- make_text_style
- benchmark
- _build_history_context
- _build_system_prompt
- _call_gemma_reasoning

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
10. `create_resume()` - 31 edges

## Surprising Connections (you probably didn't know these)
- `Change recipes` --references--> `keyword_detect_tool()`  [INFERRED]
  docs/features/chat-routing.md → app/api/chat.py
- `Adding a tool (checklist)` --references--> `keyword_detect_tool()`  [INFERRED]
  docs/features/tool-registry.md → app/api/chat.py
- `Gotchas` --references--> `recall_memory()`  [INFERRED]
  docs/features/memory.md → app/api/memory.py
- `Calendar` --references--> `check_today_schedule()`  [INFERRED]
  docs/features/email-calendar.md → app/services/calendar_tool.py
- `Flow` --references--> `get_dsa_enforcer()`  [INFERRED]
  docs/features/dsa-mode.md → app/services/dsa_enforcer.py

## Import Cycles
- None detected.

## Communities (177 total, 27 thin omitted)

### Community 0 - "Tool registry"
Cohesion: 0.02
Nodes (141): list_skills(), List all saved skill descriptions., Store a user preference (e.g. key='browser', value='Chrome')., save_preference(), ppt_styles(), Resolves site name, opens a VISIBLE browser, and performs a search or action…, smart_web_action(), append_to_file() (+133 more)

### Community 1 - "reply_generator.py"
Cohesion: 0.06
Nodes (50): build_style_profile(), generate_reply_draft(), One-time training: parse a WhatsApp .txt chat export to build your personal…, Read the latest WhatsApp thread with a contact and generate 3 reply drafts that…, _build_system_prompt(), _build_user_prompt(), _call_groq(), generate_reply_draft() (+42 more)

### Community 2 - "analyzer.py"
Cohesion: 0.10
Nodes (51): _file_hash(), _gemini(), _groq(), _hex(), _llm_json(), _parse_json(), Fallback when Groq is rate-limited (its vision model has a 200k tokens/DAY cap)., _vision() (+43 more)

### Community 3 - "plate.py"
Cohesion: 0.08
Nodes (43): contact_type(), _hex(), background_mask(), _bg_model(), _bgr(), build(), comps_in(), _chip_gap() (+35 more)

### Community 4 - "ppt_chart_engine"
Cohesion: 0.12
Nodes (34): _bg_color(), _extract_strict_metric(), _fig_to_bytes(), _hex(), _metrics_to_bar(), _palette_colors(), ppt_chart_engine.py — Dynamic Data-Visualization Engine for JARVIS PPT…, Horizontal or vertical bar chart. (+26 more)

### Community 5 - "content_humanizer + content-tools"
Cohesion: 0.09
Nodes (34): build_structure_prompt(), build_vocab_prompt(), call_groq(), check_similarity(), detect_tone(), fact_check(), get_groq_client(), get_sentence_scores() (+26 more)

### Community 6 - "window_layout.py"
Cohesion: 0.09
Nodes (37): media_state.py — which media app the user used last (Spotify or YouTube)…, True if the Spotify desktop app has a window (cheap: EnumWindows, no UIA)., spotify_running(), _find_window_fuzzy(), Find a window HWND by fuzzy name matching using Win32 API (no pygetwindow)., adjust_active_window(), _enumerate_app_windows(), _cb() (+29 more)

### Community 7 - "Resume creator"
Cohesion: 0.06
Nodes (42): _analyse_design(), _apply_layout_answer(), _balance_columns(), _closest_preset(), _crop_photo(), _face_ratio(), _faces(), _grow_photo_box() (+34 more)

### Community 8 - "youtube_control.py"
Cohesion: 0.09
Nodes (42): _dur_to_sec(), _end_session(), _fetch_results(), _find_channel(), _find_channel_at(), walk(), _format_results(), _initial_data() (+34 more)

### Community 9 - "syllabus_auditor"
Cohesion: 0.07
Nodes (41): _approx_token_count(), _assemble_response(), audit_playlist_syllabus(), _build_vector_store(), _chunk_transcript(), _coverage_level(), _embed_texts(), _extract_playlist_id() (+33 more)

### Community 10 - "ppt_studio.py"
Cohesion: 0.09
Nodes (39): detect_profile(), parse_instructions(), slide 2' / 'second slide' / 'slide two' / 'the solution slide' → slide number., Deterministic reading of the user's instructions. image_rules: [{"images":…, [(n, heading, raw content)] split on 'Slide N:' markers of repaired text., raw_slide_blocks(), slide_count(), _slide_ref() (+31 more)

### Community 11 - "DeckRenderer"
Cohesion: 0.15
Nodes (21): _compact_header(), box(), DeckRenderer, fit_size(), _items(), para_h(), Header + lead + list inside a column. Returns nothing., Portrait/square image as a full-height panel flush to one edge. (+13 more)

### Community 12 - "browser_tool.py"
Cohesion: 0.15
Nodes (26): browse_and_paginate(), browse_and_read(), _clean_text(), click_element(), _ensure_url(), fill_form(), _llm_extract(), _new_browser_page() (+18 more)

### Community 13 - "LRUCache"
Cohesion: 0.18
Nodes (8): LRUCache, Insert or update a key-value pair. - If key already exists: update value + TTL,…, Remove a key from the cache. Returns True if the key existed, False if it was…, Place node at the MRU (most-recently-used) end of the list., Remove node from its current position in the list (O(1) because doubly-linked)., Evict a specific node (unlink + remove from map)., O(1) Least-Recently-Used cache backed by: - dict[str, Node] — hash map for O(1)…, Return the value for key, or None on miss / expiry. On hit: moves node to the…

### Community 14 - "file_ops.py"
Cohesion: 0.10
Nodes (28): append_file(), bulk_rename(), create_folder(), delete_file(), diff_files(), _fmt_size(), list_directory(), _maybe_summarize() (+20 more)

### Community 15 - "PresentationBuilder"
Cohesion: 0.18
Nodes (19): _clean_image_path(), _get_image_aspect_ratio(), _oval(), _parse_bullet(), _parse_card(), PresentationBuilder, _frame(), Render a single image with CONTAIN-FIT (object-fit: contain). The image is… (+11 more)

### Community 16 - "assignment_answers.py"
Cohesion: 0.12
Nodes (25): _ask_question_on_page(), _find_input(), generate_answer(), generate_answers(), _get_persistent_page(), _groq_answer(), Jarvis Assignment Tool — Phase 2: Answer Generation…, Launch a visible (non-headless) Chromium with a persistent profile. Login… (+17 more)

### Community 17 - "resume_builder.py"
Cohesion: 0.07
Nodes (60): _clean_free(), _competencies_html(), _contact_html(), _css_val(), _custom_section_html(), _data_uri(), _decor_html(), _design_set() (+52 more)

### Community 18 - "fontmatch.py"
Cohesion: 0.08
Nodes (26): all_faces(), _core_norm(), FontMatcher, identify(), ndarray, fontmatch.py — Font identification against the local library (fonts.py), all in…, Scale so the stroke cores read 1.0 (same rule as the JS side: mean of values…, Reference intensity map (0 = background, 1 = text colour) of a line's ink box… (+18 more)

### Community 19 - "prompt_enhancer_button"
Cohesion: 0.08
Nodes (33): _acquire_single_instance(), _app_title_match(), _browser_url(), classify_app(), _exe_name(), _has_pattern(), install_autostart(), _is_editable() (+25 more)

### Community 20 - "_sanitize_design"
Cohesion: 0.15
Nodes (21): _apply_color(), _contrast(), _css(), _css_extra(), _lum(), _measure_band(), near(), _measure_frame() (+13 more)

### Community 21 - "Jarvis — Claude Code guide"
Cohesion: 0.25
Nodes (7): Adding / changing a tool (project rules, from JARVIS_ARCHITECTURE.md), /chat request flow (short), Gotchas, graphify, Jarvis — Claude Code guide, Run, Where things are

### Community 22 - "ppt_research"
Cohesion: 0.11
Nodes (36): ground_slides(), plan_queries(), 4-6 web queries covering the angles a deck on `topic` needs. Templates, not an…, Web + Wikipedia → verified facts. [] when offline (the deck is then written…, Audit every generated slide; LLM-repair flagged ones with their facts; scrub…, research_facts(), allowed_numbers(), _anchors() (+28 more)

### Community 23 - "ppt_template.py"
Cohesion: 0.06
Nodes (56): analyze_format(), _analyze_slide(), classify_box(), _clear(), clone_slide(), delete_slide(), describe_template(), _field_label() (+48 more)

### Community 24 - "create_resume"
Cohesion: 0.09
Nodes (31): _apply_layout_hint(), _attachments(), create_resume(), detect_resume_request(), _has_details(), _is_logo_label(), list_resume_templates(), _load_state() (+23 more)

### Community 25 - "ppt_router.py"
Cohesion: 0.11
Nodes (25): build_ppt(), generate(), create_ppt_backend(), generate(), extract_theme(), get_styles(), PPTBuildRequest, PPTCreateRequest (+17 more)

### Community 26 - "package"
Cohesion: 0.11
Nodes (20): name, private, type, version, autoprefixer, eslint, ref_eslint_config, @eslint/js (+12 more)

### Community 28 - "orchestrator.py"
Cohesion: 0.07
Nodes (44): resume_replica — Scene-graph-based resume replication engine. Import the public…, build_replica(), compile_replica_html(), _compute_fit_scale(), create_replica_resume(), _data_uri(), _design_with_replica(), orchestrator.py — Main pipeline for replica resume creation. The public API:… (+36 more)

### Community 29 - "ppt_image_engine"
Cohesion: 0.16
Nodes (18): build_image_descriptors(), _extract_keywords(), get_aspect_ratio(), ImageDescriptor, match_images_to_slides(), _parse_slide_ref(), _parse_slide_ref_by_title(), ppt_image_engine.py — Semantic Image-Slide Matcher for JARVIS PPT Engine… (+10 more)

### Community 30 - "rag_memory.py"
Cohesion: 0.08
Nodes (31): _extract_topics(), _get_faiss_lock(), Lock, rag_memory.py — Jarvis Long-Term RAG Memory Engine…, Persist FAISS index and ID map to disk (sync, runs in thread executor)., Run the sync FAISS save in a thread pool to avoid blocking the event loop., Lightweight keyword-based topic extraction (no LLM call). Returns a CSV of the…, Lazily create the FAISS lock inside a running event loop. (+23 more)

### Community 31 - "ppt_composer.py"
Cohesion: 0.16
Nodes (38): _body_cards(), _body_fields(), _body_list(), _body_paragraph(), _body_stats(), _body_steps(), _body_table(), _cols_for() (+30 more)

### Community 32 - "DSAEnforcer"
Cohesion: 0.28
Nodes (4): _cache_set(), DSAEnforcer, Write to Neural Cache, silently skipping if unavailable., Flow

### Community 33 - "ppt_content.py"
Cohesion: 0.07
Nodes (55): apply_edit(), apply_structure(), _as_dated(), _as_stat(), _budget_left(), _clauses(), _compact(), _content_prompt() (+47 more)

### Community 34 - "WALWriter"
Cohesion: 0.06
Nodes (26): Any, Path, Queue, Flush and close the file handle cleanly on server shutdown., Manages periodic full-state snapshots. The snapshot itself is triggered through…, Serialise cache state to disk and truncate the WAL. Called by CacheEngine on…, Load the snapshot from disk. Returns None if no snapshot exists yet. Called…, Start a daemon thread that enqueues a SNAPSHOT command every interval_seconds.… (+18 more)

### Community 35 - "PromptOverlay"
Cohesion: 0.14
Nodes (3): main(), PromptOverlay, Strip the **ENHANCED PROMPT (CODING):** header if present.

### Community 36 - "ui_inspector"
Cohesion: 0.10
Nodes (11): Walk all descendants looking for any control whose window_text contains `text`…, Fire an element's primary action via UIA Invoke pattern. No mouse movement —…, Inject text into an input element via UIA Value pattern. No simulated…, Read text from an element via UIA TextPattern or window_text. Returns empty…, Walk the accessibility tree and return all elements up to `depth` levels. Use…, Core wrapper around pywinauto's UIA backend. All interactions go through the OS…, Get a window wrapper by partial title match (regex-safe). Returns None if not…, Get the currently focused window via Win32 HWND matching. (+3 more)

### Community 37 - "agentic_web.py"
Cohesion: 0.13
Nodes (16): _worker(), _build_search_queries(), _fetch_page_text(), __init__(), _get_api_key(), agentic_web.py — Smart Web Research Engine for Jarvis…, Download a page and return clean readable text (no HTML tags)., Use the LLM to extract specific listings from the fetched content. (+8 more)

### Community 38 - "exact_render.py"
Cohesion: 0.05
Nodes (75): _f(), Escaped text; in editor mode an editable span carrying the content JSON path it…, _abs_text(), _bar_grid_html(), _bg_grid(), canon_title(), _chips_html(), _contact_html() (+67 more)

### Community 39 - "pipeline.py"
Cohesion: 0.12
Nodes (23): run(), _align(), analyse_reference(), line_box(), _choose_families(), best_in(), total(), _font_styles() (+15 more)

### Community 40 - "memory/memory.py"
Cohesion: 0.17
Nodes (14): find_skill(), format_preferences_for_prompt(), get_all_preferences(), Jarvis Vector Memory — ChromaDB-based long-term memory engine. Stores and…, Returns a string suitable for injecting into LLM prompts., Stable short ID based on content hash., Persist a successful dynamic skill for future reuse., Returns up to n most relevant saved skills for a given task description. Each… (+6 more)

### Community 42 - "editor_save"
Cohesion: 0.09
Nodes (34): _apply_op(), _custom_sections(), editor_page(), editor_save(), undo_id(), _normalise_content(), _raster_palette(), User-made sections from the editor: {id: custom_N, title, style, items}. Kept… (+26 more)

### Community 43 - "air-drawing + air_drawing_tool"
Cohesion: 0.18
Nodes (9): open_air_drawing(), Opens the Air Drawing Canvas on the screen. This feature allows the user to…, Air drawing (webcam hand drawing), Files & symbols (auto-generated, line numbers are current), Flow, Gotchas, Graphify, Purpose (+1 more)

### Community 44 - "ppt_designer.py"
Cohesion: 0.08
Nodes (30): _best_window(), count_lines(), E(), gradient_box(), _line_factor(), line_shape(), _pil_font(), place_image() (+22 more)

### Community 45 - "voice.py"
Cohesion: 0.07
Nodes (41): devanagari_to_hinglish(), loanword_ratio(), Share of Devanagari words that are English loanwords ("ओपन क्रोम" → 1.0). High…, Romanize a Devanagari (Hindi) transcript for the backend, keeping any Latin…, _clean_transcript(), Clip, _finish(), _get_groq() (+33 more)

### Community 46 - "package + App"
Cohesion: 0.16
Nodes (11): App(), ChatMessage(), API_BASE, frontend_src_index, lucide-react, react, ref_react_dom_client, react-markdown (+3 more)

### Community 47 - "acoustic_tripwire"
Cohesion: 0.05
Nodes (30): AcousticWakeEngine, calibrate_tripwire(), _generate_chime(), get_wake_event(), _play_chime(), ndarray, Background thread that watches the microphone for a double-clap pattern. Usage…, Start the background listening thread. (+22 more)

### Community 48 - "render_sections"
Cohesion: 0.11
Nodes (25): _balanced_rows(), _fill(), image_block(), _image_panel(), _masonry(), Split items into rows with at most one item difference (5 in 3 cols → 3+2, 7 →…, How much extra height a section can absorb before it looks inflated., Framed images (no crop) + numbered captions under each. Returns used height. (+17 more)

### Community 49 - "_verbatim"
Cohesion: 0.17
Nodes (16): Pasted resumes often lose their line breaks, gluing a heading to the next word…, (position, section key) of every heading line marked in the person's text., The exact source text of v (case, dashes, quotes and spacing may differ), or…, The person's own pieces of text: lines/bullets/cells (coarse) and their…, The resume shows the person's own words only. Every sentence-like field is…, _region_keys(), _segments(), _src_span() (+8 more)

### Community 50 - "CacheClient"
Cohesion: 0.10
Nodes (14): Send one of the reply drafts generated by generate_reply_draft. draft_index is…, send_style_reply(), CacheClient, Any, Store a key-value pair, optionally with a TTL. Args: key: Cache key. value:…, Delete a key from the cache. Returns: True if the key existed and was deleted,…, Retrieve server statistics (hit rate, evictions, cache size, etc.). Returns…, Explicitly close the socket connection. (+6 more)

### Community 52 - "calendar_tool.py"
Cohesion: 0.27
Nodes (9): add_event(), check_today_schedule(), _get_calendar_service(), get_upcoming_events(), calendar_tool.py — Jarvis Google Calendar Integration (Step 8)…, Create a new event in Google Calendar. - title: "Project Meeting" - date:…, Authenticate and return a Google Calendar API service object., List events in the next N days. (+1 more)

### Community 53 - "package"
Cohesion: 0.14
Nodes (14): devDependencies, autoprefixer, eslint, @eslint/js, eslint-plugin-react-hooks, eslint-plugin-react-refresh, globals, postcss (+6 more)

### Community 55 - "stream_chat"
Cohesion: 0.17
Nodes (12): Stop watcher, acoustic tripwire, and close DB pool cleanly on server shutdown., shutdown_event(), Stop the background screen watcher thread cleanly., stop_background_watcher(), AsyncClient, _clean_agentic_line(), Convert a linear-planner tag line into natural spoken text., POST /chat with the spoken language, speak the reply into `ch` as it streams.… (+4 more)

### Community 56 - "llm.py"
Cohesion: 0.08
Nodes (38): classify_context(), context_classifier.py — Jarvis Situational Awareness…, Classify the situation from user input. Returns a dict with keys: urgency :…, check_for_tool_intent(), generate_chat_response(), _groq_generate(), _is_complex_response(), _is_rate_limit() (+30 more)

### Community 57 - "skill_prompt_enhancer.py"
Cohesion: 0.16
Nodes (21): check_for_hallucination(), clean_output(), detect_domain(), is_bloated(), protect_blocks(), prompt_enhancement_library.py…, Replace ``` fenced blocks with [[BLOCK_n]] placeholders., Put protected blocks back; append any the model dropped. (+13 more)

### Community 58 - "dark_enhancement.py"
Cohesion: 0.13
Nodes (23): _apply_gamma(), _fusion_and_polish(), get_all_enhancements(), _normalize_to_8bit(), _path_1_retinex(), _path_2_wavelet(), ndarray, run_pipeline_a() (+15 more)

### Community 59 - "web_search.py"
Cohesion: 0.09
Nodes (31): research_scraper.py — Autonomous Web Research Scraper…, _extract_location(), get_info(), get_weather(), Pulls a clean location name out of a weather query., Get current weather using wttr.in — returns a clean spoken string., Search for a query within a specific website using DuckDuckGo site: operator., Read and extract readable text content from a specific URL. (+23 more)

### Community 60 - "execute_safe"
Cohesion: 0.15
Nodes (13): execute_safe(), Exception, Restricted open(): blocks writes to system paths., Restricted __import__: blocks dangerous modules., Raised when generated code violates safety constraints., AST visitor that inspects generated code before execution., Parse and walk the AST, raising SecurityError on violations., Validates and runs 'code' in a restricted namespace. Returns: (success: bool,… (+5 more)

### Community 61 - "Node"
Cohesion: 0.18
Nodes (6): Node, Restore cache state from a snapshot dict (produced by snapshot()). Called once…, Place node at the LRU (least-recently-used) end of the list., A doubly-linked list node holding one cache entry. Attributes: key (str): Cache…, Evict the LRU entry (the node just before the tail sentinel). Returns the…, Return True if this entry has a TTL and it has elapsed.

### Community 62 - "dag_executor.py"
Cohesion: 0.10
Nodes (34): _semantic_window_adjust(), _call_dag_planner(), DAGNode, _execute_node(), is_dag_task(), dag_executor.py — Jarvis DAG-Based Multi-Step Agent Planner…, Ask the LLM to produce a DAG plan. Returns parsed dict., Returns execution waves — each wave is a list of node IDs that can run in… (+26 more)

### Community 63 - "edit"
Cohesion: 0.12
Nodes (17): Separate the user's command, any pasted/attached content and attachment paths., split_request(), _collect_attachments(), edit(), Run fn(progress=cb) in a thread, yield progress strings live; result in…, _with_progress(), ppt_edit(), Follow-up edit of the last deck (generator). See ppt_studio.edit. (+9 more)

### Community 64 - "whatsapp_smart.py"
Cohesion: 0.08
Nodes (36): flow_stream(), _click_voice_call_button(), confirm_whatsapp_call(), _focus_or_open_whatsapp(), _get_whatsapp_window(), initiate_whatsapp_call(), whatsapp_call.py — Jarvis Smart WhatsApp Calling Integration (Fully Isolated)…, Focus the WhatsApp window or open it if not running. Returns True on success. (+28 more)

### Community 65 - "frontend"
Cohesion: 0.22
Nodes (8): Frontend (`frontend/src`), Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Key behaviour (App.jsx), Purpose, Web UI (React/Vite), DagPlanPanel()

### Community 67 - "Flow — create (`ppt_tool.ppt_create` → `ppt_studio.create`, a generator)"
Cohesion: 0.11
Nodes (28): architect_slides(), ask(), _retry(), run(), _complete_from_source(), deck_facts(), extractive_ok(), _is_instruction() (+20 more)

### Community 68 - "spotify_service.py"
Cohesion: 0.06
Nodes (55): app_kind(), control(), run(), _do(), _filter(), kind_playing(), _label(), media_command() (+47 more)

### Community 69 - "prompt_enhancer_button"
Cohesion: 0.14
Nodes (4): EnhanceButton, Move (and optionally show) without ever activating the window; Tk's deiconify()…, Default spot: just above the prompt box's top-right corner; below it or inside…, _save_state()

### Community 70 - "voice"
Cohesion: 0.11
Nodes (12): hinglish_to_devanagari(), Rewrite the Hindi words of a romanized Hinglish sentence in Devanagari, leaving…, Channel, _norm_words(), The speech stream of one command's reply., Plays sentences from many Channels without overlap: - urgent phrases (acks,…, Barge-in "stop": silence now and drop everything queued., Did the mic just hear Jarvis himself (speaker → mic bleed)? Echo comes back… (+4 more)

### Community 72 - "jarvis_overlay.py"
Cohesion: 0.18
Nodes (7): Image, pil, generate_arc_reactor(), JarvisOverlay, Jarvis Arc Reactor Overlay -------------------------- A floating, always-on-…, Draws a beautiful arc reactor using PIL when no icon file is found., read_state()

### Community 73 - "test_lru"
Cohesion: 0.20
Nodes (5): Accessing 'a' should move it to MRU and save it from eviction., Re-setting an existing key should move it to MRU., len(cache.map) must never exceed capacity., Fill to capacity+1. The first key inserted (LRU) should be evicted., TestEviction

### Community 74 - "Gotchas"
Cohesion: 0.18
Nodes (10): _mail_tool(), Email tools: try the real Gmail API (gmail_tool) first, fall back to opening…, Email, Adding a tool (checklist), Calling tools from code, Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify (+2 more)

### Community 75 - "_humanize_via_browser"
Cohesion: 0.11
Nodes (19): _get_browser_page(), humanize_all_answers(), humanize_text(), _humanize_via_browser(), _humanize_via_llm(), _protect_technical(), Replace technical content with numbered placeholders. Returns (modified_text,…, Restore original technical content from placeholders. (+11 more)

### Community 76 - "recall"
Cohesion: 0.14
Nodes (18): execute_tool(), BaseModel, post, ToolExecuteRequest, get_memory_stats(), Returns True if the turn is meaningful enough to store. Skips trivial single-…, Semantically recall the most relevant past conversation turns. Args: query: The…, Return statistics about stored long-term memory. (+10 more)

### Community 77 - "Element"
Cohesion: 0.12
Nodes (3): Element, Minimal pywinauto-style wrapper around an IUIAutomationElement., Rect

### Community 78 - "_worker"
Cohesion: 0.20
Nodes (8): Lock, 50 concurrent clients, each doing 1000 ops. After completion: - Server still…, The engine should report meaningful stats after the load test., While 10 threads hammer the cache, a separate thread pings repeatedly. All…, One client thread. Performs `ops` random GET/SET/DEL operations. Records any…, TestConcurrency, _ping_loop(), _worker()

### Community 79 - "gmail_tool.py"
Cohesion: 0.07
Nodes (45): check_emails(), _decode_body(), _format_date(), get_email_body(), _get_gmail_service(), _get_header(), list_unread(), gmail_tool.py — Jarvis Gmail Integration (Step 5)… (+37 more)

### Community 80 - "package"
Cohesion: 0.22
Nodes (9): dependencies, framer-motion, lucide-react, react, react-dom, react-markdown, react-syntax-highlighter, remark-gfm (+1 more)

### Community 81 - "handTracking"
Cohesion: 0.31
Nodes (3): CameraView(), getHandsConstructor(), HandTracker

### Community 82 - "chat.py"
Cohesion: 0.05
Nodes (63): chat_endpoint(), _dag_stream_with_history(), planner_stream(), response_stream_with_history(), resume_stream(), tool_stream(), ChatRequest, _clean_yt_query() (+55 more)

### Community 83 - "screen_reader.py"
Cohesion: 0.11
Nodes (28): _accessibility_tree(), describe_screen_for_llm(), get_screen_screenshot_b64(), _groq_vision_screen(), _init_tesseract(), _ocr_screen(), screen_reader.py — Jarvis Screen Vision (VLM-first architecture)…, Legacy OCR layer. Works on any app but extracts raw text only — no layout,… (+20 more)

### Community 84 - "apply_diff_patches"
Cohesion: 0.20
Nodes (6): apply_diff_patches(), _patch_fill(), Converts VLM diffs into structured patches and applies them to the replica_doc.…, Finds the frame with the given ID in the scene graph and updates its fill.…, make_linear_fill(), stops = [{"offset_pct": 0, "color": "#hex"}, {"offset_pct": 100, "color":…

### Community 85 - "Flow (`scripts/voice_agent.py`)"
Cohesion: 0.12
Nodes (15): detect_language(), Detect whether the user spoke English, Hinglish, or Hindi. Returns: 'english' —…, _reply_language_note(), language_mismatch(), True if a reply sentence is in the other language than the one the user spoke., Loudest output RMS in the last `window` s — the voice agent's echo reference., Flow (`scripts/voice_agent.py`), _is_stop() (+7 more)

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
Cohesion: 0.10
Nodes (32): detect(), Design overrides if the image is a campus-format resume (education table header…, analyse(), _cdist(), _get_ocr(), _h_overlap(), is_ornament_text(), _is_upper() (+24 more)

### Community 92 - "assignment_humanizer.py"
Cohesion: 0.10
Nodes (23): _extract_output_text(), _fill_input(), _find_element(), _humanize_chunk_via_browser(), Jarvis Assignment Tool — Phase 3: Answer Humanizer…, Try multiple CSS selectors to find a visible element., Fill an input area with text using the most reliable method available., Extract text from the output area of the humanizer. (+15 more)

### Community 94 - "database.py"
Cohesion: 0.33
Nodes (7): get_db_pool(), init_db(), Queries the table and uses the pgvector cosine distance operator (<=>) to fetch…, Inserts text chunks and vectors into the knowledge_store table., save_document_chunk(), search_similar_chunks(), asyncpg

### Community 95 - "Assignment solver (5 phases)"
Cohesion: 0.22
Nodes (8): list_assignments(), Scan Desktop, Documents, and Downloads for PDF files., Assignment solver (5 phases), Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Purpose, Triggers

### Community 96 - "walk_nodes"
Cohesion: 0.22
Nodes (7): build_editor_path_map(), Walks the scene graph and builds a map from binding path -> list of node IDs…, collect_bindings(), Depth-first traversal of the scene graph. visitor(node, parent, depth) is…, Returns all unique binding paths referenced in the scene graph. E.g. ["name",…, walk_nodes(), _walk()

### Community 97 - "youtube_player.py"
Cohesion: 0.06
Nodes (76): element_from_handle(), focused_element(), uia_local.py — thread-safe UI Automation access (helper, not a tool)…, This thread's IUIAutomation (COM initialised for the thread on first use)., uia(), _address_bar_focused(), _address_bar_value(), _clip_get() (+68 more)

### Community 98 - "compiler"
Cohesion: 0.18
Nodes (18): _compile_chart(), _compile_section(), _it(), Simple <ul><li> list of skill names., High-level section renderer. Returns complete HTML for the section (heading +…, Returns data-item attribute string in edit mode, else empty string., Compiles a CHART node to the appropriate skill/language visualisation., Progress bar skills. Supports 2-column CSS grid. (+10 more)

### Community 99 - "compiler"
Cohesion: 0.15
Nodes (14): _compile_image(), _compile_node(), _compile_rule(), _compile_text(), _initials_block(), Returns the initials text for the photo placeholder., Converts a TEXT_STYLE dict to a CSS properties string., Dispatches to the appropriate node compiler based on node['type']. (+6 more)

### Community 100 - "init_rag_memory"
Cohesion: 0.14
Nodes (18): aiomysql, close_mysql(), get_mysql_pool(), init_mysql(), mysql_db.py — Jarvis Async MySQL Connection Pool…, Gracefully close the MySQL connection pool on server shutdown., Return the shared MySQL connection pool, initializing it if needed., Initialize the MySQL connection pool and ensure all required tables exist. Safe… (+10 more)

### Community 101 - "detect_resume_intent"
Cohesion: 0.18
Nodes (14): detect_resume_intent(), _extract_task_resource(), _find_best_task_match(), _has_continuation_verb(), _has_fresh_task_indicator(), _has_reference_phrase(), resume_detector.py — Jarvis Resume Intent Classifier…, Return True if the text contains a strong resume-intent reference phrase. (+6 more)

### Community 102 - "package"
Cohesion: 0.40
Nodes (5): scripts, build, dev, lint, preview

### Community 103 - "schema.py"
Cohesion: 0.09
Nodes (21): make_chart_node(), make_group_node(), make_parametric_geometry(), make_radial_fill(), make_repeat_node(), make_ring_spec(), make_rule_node(), make_text_node() (+13 more)

### Community 104 - "hinglish_normalizer.py"
Cohesion: 0.22
Nodes (8): _sub(), normalize_for_tts(), hinglish_normalizer.py — Devanagari Crash Prevention + Text Normalizer…, One Devanagari word → casual Hinglish roman ("चलाओ" → "chalao", "करना" →…, Transform text so it's safe and natural-sounding for TTS: 1. Replace known…, Markdown → plain speakable text (keeps Devanagari). Also drops URLs and emoji., strip_markdown(), _translit_dev_word()

### Community 105 - "time"
Cohesion: 0.05
Nodes (55): acoustic_tripwire.py — Jarvis Acoustic Wake Engine…, _bring_whatsapp_to_front(), _get_whatsapp_window(), _heuristic_parse_ocr_lines(), _parse_uia_message_string(), message_reader.py — Jarvis WhatsApp Intelligence: Message Reader…, Restores and focuses WhatsApp window. Returns True on success., Walks the WhatsApp UIA accessibility tree to extract messages. WhatsApp Desktop… (+47 more)

### Community 106 - "ppt_tool.py"
Cohesion: 0.09
Nodes (26): _auto_select_image_layout(), _bg_fill(), _c(), _corner_L(), _detect_purpose(), extract_theme_from_image(), _extract_theme_pil_local(), _groq_call() (+18 more)

### Community 107 - "assignment_pipeline.py"
Cohesion: 0.18
Nodes (19): _browser_thread(), do_assignment(), _find_el(), _get_answer(), _get_browser_ctx(), _groq_answer(), _groq_humanize(), _humanize_browser() (+11 more)

### Community 108 - "api/memory.py"
Cohesion: 0.12
Nodes (22): forget_memory(), ForgetRequest, get_history(), ingest_memory(), IngestRequest, memory_stats(), BaseModel, delete (+14 more)

### Community 109 - "CacheEngine"
Cohesion: 0.06
Nodes (36): CacheEngine, Any, Route a command dict to the appropriate handler. All handlers return a response…, Owns the LRUCache. Runs a single consumer loop on a dedicated thread. External…, Spawn the single writer thread. Call once at server boot., Gracefully stop the engine writer thread., The single consumer loop. Runs on CacheEngineThread. Processes one command at a…, decode_message() (+28 more)

### Community 110 - "bindings.py"
Cohesion: 0.20
Nodes (9): format_binding_value(), iter_content_items(), bindings.py — Content binding resolution and editor path mapping. Binding paths…, Iterator for repeat bindings. Yields (index, item) for each item in the list at…, Returns the display title for a section, checking content['section_titles']…, Resolves a binding path against content dict. Returns the value at that path,…, Converts a resolved binding value to a display string. - None / empty string /…, resolve_binding() (+1 more)

### Community 111 - "compiler"
Cohesion: 0.23
Nodes (12): _compile_repeat(), _ef(), Renders a single experience entry (same format as legacy builder's…, Renders a single education entry., Renders a single project entry (same format as legacy builder's _projects_html)., Renders the contact section with icons., Returns escaped text in normal mode, or a contenteditable span in edit mode.…, Compiles a REPEAT node by iterating content[binding] and rendering items. (+4 more)

### Community 112 - "README"
Cohesion: 0.50
Nodes (3): Expanding the ESLint configuration, React Compiler, React + Vite

### Community 113 - "README"
Cohesion: 0.20
Nodes (9): Architecture, Benchmark, Files, LRU Cache Design, Neural Cache, Persistence, Running, Tests (+1 more)

### Community 119 - "config.py"
Cohesion: 0.12
Nodes (17): Settings, app_memory, _llm_fix_code(), _llm_write_code(), Dynamic Skill Engine for Jarvis 2.0 ------------------------------------- When…, Ask the LLM to fix a broken script., Remove accidental markdown code fences if LLM adds them., Ask the LLM to write Python code for a given task. (+9 more)

### Community 120 - "resume_router.py"
Cohesion: 0.25
Nodes (7): get, post, resume_router.py — FastAPI router for the visual resume editor…, resume_editor(), resume_save(), fastapi, fastapi_responses

### Community 122 - "extract_questions"
Cohesion: 0.29
Nodes (8): extract_questions(), _extract_via_llm_text(), _pdf_pages_to_text(), Extract text from each PDF page separately. Returns list of page strings., LLM-based text extraction as fallback for when regex fails., Extract ALL questions from an assignment PDF using a 3-track hybrid system.…, Resolve PDF path: handles full paths, filenames, partial names., _resolve_pdf_path()

### Community 124 - "_Player"
Cohesion: 0.14
Nodes (9): get_player(), _Player, One persistent 24 kHz output stream driven by a callback that pulls from a…, Play a clip as it arrives. Returns False if interrupted., Speak a complete text. All sentences synthesise in parallel, play in order., speak_text(), split_sentences(), main() (+1 more)

### Community 125 - "Content fidelity & page limits (2026-10-02)"
Cohesion: 0.09
Nodes (35): _build_content(), _condense_content(), _content_brief(), _design_slots(), _drop_invented(), clean_text(), ok(), _edit_content() (+27 more)

### Community 126 - "compiler"
Cohesion: 0.18
Nodes (9): _compile_group(), _e(), Radar/spider chart as inline SVG. 100x100 viewBox, center (50,50), max radius…, Tags where size/opacity indicates level (higher → larger/more saturated)., Renders a single ring/donut chart SVG for a skill., Compiles a GROUP node to a <div>. Used for section headings and composites., _render_radar(), _render_tag_level() (+1 more)

### Community 127 - "Gotchas"
Cohesion: 0.25
Nodes (7): _is_positional(), A pick by position, not by title: 'the first result', 'number 3', 'the latest…, Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Purpose, Windows/OS control: windows, media, apps, files

### Community 128 - "dsa_enforcer.py"
Cohesion: 0.25
Nodes (7): _cache_del(), get_dsa_enforcer(), Delete from Neural Cache, silently skipping if unavailable., selenium, selenium_webdriver_edge_options, selenium_webdriver_edge_service, webdriver_manager_microsoft

### Community 129 - "main.py"
Cohesion: 0.14
Nodes (20): get_alerts(), get, post, Frontend polls this endpoint to receive proactive JARVIS screen alerts. e.g.…, Return current acoustic tripwire state for the frontend toggle., Arm the acoustic tripwire so double-claps wake Jarvis., Disarm the acoustic tripwire (engine keeps running, just paused)., Schedule an ambient-noise recalibration pass. The engine samples the mic for ~2… (+12 more)

### Community 130 - "Known issues"
Cohesion: 0.08
Nodes (16): AbstractEventLoop, Fixed on 2026-10-01 (voice, round 2), Fixed on 2026-10-03 (resume creator), Fixed on 2026-10-03 (resume editor), Fixed on 2026-10-04 (resume creator, exact replica), Fixed on 2026-10-04, round 3 (resume creator), Fixed on 2026-10-04, round 6 (resume creator), Known issues (+8 more)

### Community 131 - "refresh_docs.py"
Cohesion: 0.10
Nodes (21): _focus_or_open_whatsapp(), open_whatsapp(), WhatsApp Windows Desktop App Automation Uses the native Windows app via…, Focus the WhatsApp window or open it if not running. Returns True on success., Opens the WhatsApp desktop app., find_controls(), Dump WhatsApp Desktop UI tree to find the Voice Call button name. Run this…, search_tree() (+13 more)

### Community 132 - "os"
Cohesion: 0.05
Nodes (41): app_services, Jarvis Assignment Tool — Phase 4: Document Assembly…, nlp_extractor.py — LLM-Powered Fact & Entity Extractor…, prompt_overlay.py ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Jarvis…, research_pipeline.py — End-to-End Autonomous Research Orchestrator…, fonts.py — Local font library + font identification for exact resume…, Safe Code Executor for Jarvis ------------------------------- Runs LLM-…, screen_vision.py — Jarvis VLM Screen Understanding (Layer 1 Upgrade)… (+33 more)

### Community 133 - "ppt_studio"
Cohesion: 0.33
Nodes (4): _assign_images(), Put each image on its best slide. Explicit instructions win. Mutates deck;…, Move images off slides whose layout can't show them (or has too many) onto…, _rebalance()

### Community 134 - "make_frame_node"
Cohesion: 0.25
Nodes (8): make_frame_node(), make_no_fill(), make_padding(), make_path_node(), Returns {"type": "none"}, Returns a complete FRAME node., Returns a complete PATH node., Returns {"top_mm": ..., "right_mm": ..., "bottom_mm": ..., "left_mm": ...}

### Community 135 - "ppt_tool"
Cohesion: 0.50
Nodes (4): compute_split_geometry(), Computed image + text zone dimensions (in EMU — python-pptx native)., Dynamically compute left-text / right-image split geometry. The split ratio…, SlotGeometry

### Community 138 - "browser_mail.py"
Cohesion: 0.28
Nodes (6): check_emails(), _get_api_key(), list_unread(), browser_mail.py — Standard Browser Mail Automation…, A generic tool to perform any mail task (like sending or reading) by pre-…, smart_mail_action()

### Community 139 - ".render"
Cohesion: 0.40
Nodes (3): _as_plain_content(), _deep_plain(), Last-resort fallback: every word of a composite slide as plain bullets (never…

### Community 140 - "Screen understanding & UI automation"
Cohesion: 0.25
Nodes (7): _call_gemini_vision(), Send screenshot + context to the Groq vision model (settings.GROQ_VISION_MODEL)., Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Purpose, Screen understanding & UI automation

### Community 141 - "prompt_enhancer_button"
Cohesion: 0.21
Nodes (11): _box_contains(), _box_set_value(), _clip_get(), _clip_set(), _ctrl(), _focus(), _focused_text(), _norm() (+3 more)

### Community 142 - "Chat pipeline & routing (/chat)"
Cohesion: 0.25
Nodes (7): Change recipes, Chat pipeline & routing (/chat), Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Purpose, Response formats

### Community 143 - "DSA / LeetCode enforcer mode"
Cohesion: 0.29
Nodes (6): Data, DSA / LeetCode enforcer mode, Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Purpose

### Community 144 - "neural-cache"
Cohesion: 0.25
Nodes (7): Design, Files & symbols (auto-generated, line numbers are current), Graphify, Neural cache (Redis-like LRU server), Purpose, Runtime, Tests

### Community 145 - "voice_agent"
Cohesion: 0.33
Nodes (3): MicListener, Initial ambient noise floor (kept up to date on every non-speech frame)., One 32 ms frame → clap check + VAD state machine → events.

### Community 146 - "startup_event"
Cohesion: 0.33
Nodes (6): _on_screen_alert(), Callback fired by the background watcher when something notable is detected.…, Start background screen watcher and RAG memory system when the server boots., startup_event(), Start the passive background screen watcher. Args: callback: Function called…, start_background_watcher()

### Community 147 - "_photo_edges"
Cohesion: 0.22
Nodes (6): _flat_outside(), _photo_edges(), Just outside the circle the colour is flat (a ring, frame or background), not…, Colour difference just inside vs just outside a circle (high = a real frame…, Frame of the photo: every strong colour edge along 96 rays from the face is a…, _ring_contrast()

### Community 148 - "assemble_assignment"
Cohesion: 0.33
Nodes (6): assemble_assignment(), _create_powerpoint(), _create_word_doc(), _parse_qa_json(), Assemble the extracted/humanized questions and answers into a formatted…, Extract and parse the JSON array from the input string.

### Community 149 - "make_solid_fill"
Cohesion: 0.33
Nodes (6): make_default_replica_document(), make_page_node(), make_solid_fill(), Returns {"type": "solid", "color": color}, Returns a complete PAGE node., Returns a skeleton replica document with an empty scene graph. The caller is…

### Community 151 - "ssml_processor.py"
Cohesion: 0.33
Nodes (5): add_human_prosody(), ssml_processor.py — Human Prosody Pre-processor…, Add natural speech prosody to plain text. Args: text: Plain text (already…, Remove all SSML tags from text — used when falling back to edge-tts which does…, strip_ssml()

### Community 152 - "Agents: DAG executor, linear planner, dynamic skills"
Cohesion: 0.33
Nodes (5): Agents: DAG executor, linear planner, dynamic skills, Data, Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify

### Community 153 - "smart_navigator.py"
Cohesion: 0.25
Nodes (8): _get_api_key(), _llm_extract(), smart_navigator.py — Isolated Smart Web Navigator for Jarvis…, Attempt to find the GROQ API key safely., Pass scraped text through LLM for structured extraction., Resolve a verbal site name like 'unstop' to a URL like 'https://unstop.com'., _resolve_url(), playwright_sync_api

### Community 154 - "prompt-enhancer + prompt_enhancer_button"
Cohesion: 0.22
Nodes (10): _hint_text(), _ide_allows(), is_prompt_box(), In IDEs only chat / agent inputs qualify, never the code editor, the terminal,…, Entry points, Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify (+2 more)

### Community 155 - "Memory: RAG, facts, task ledger, resume, skills"
Cohesion: 0.33
Nodes (5): API, Files & symbols (auto-generated, line numbers are current), Gotchas, Graphify, Memory: RAG, facts, task ledger, resume, skills

### Community 157 - "assignment_tool.py"
Cohesion: 0.15
Nodes (19): _classify_question_type(), _clean_text(), _extract_marks(), _extract_via_vision(), _has_figure_reference(), _parse_llm_json_response(), _pdf_pages_to_images(), Jarvis Assignment Tool — Phase 1: Smart Question Extractor… (+11 more)

### Community 158 - "_straight_edges"
Cohesion: 0.29
Nodes (7): _band_extent(), The photo's width from the flat bands that border it above and below (their run…, Rectangular photo whose frame the ray fit can't see (a translucent band across…, _straight_edges(), flat(), horizontal(), Generic analysis rules added 2026-10-04 (round 5, `SPEC_VERSION` 6)

### Community 159 - "ResearchScraper"
Cohesion: 0.15
Nodes (8): NLPExtractor, Runs extraction on each scraped source and aggregates the results. Returns a…, Scrapes the web for a topic and extracts verified facts and statistics. Yields…, research_topic(), Searches DDG for the topic, fetches the top N links concurrently, and returns…, ResearchScraper, Phase 3: Autonomous Research Aggregator. Scrapes live facts from the web,…, _research_and_create_ppt()

### Community 160 - "Voice: STT, TTS, wake word, clap wake, overlay"
Cohesion: 0.11
Nodes (14): preload_local_stt(), Load the local Whisper models in the background (voice agent startup)., Feed streamed tokens; get back speakable sentences as early as possible., Speak an async generator of text chunks, sentence by sentence, pipelined., SentenceSplitter, speak_stream(), Config (`app/core/config.py` + env), Files & symbols (auto-generated, line numbers are current) (+6 more)

### Community 161 - "compiler"
Cohesion: 0.33
Nodes (6): _guess_icon(), _icon_svg(), Renders a single competency as an icon+title+description card., Returns an inline SVG icon using the _ICONS dict., Guesses an icon name from a competency title string., _render_competency_item()

### Community 162 - "CODEMAP"
Cohesion: 0.22
Nodes (8): Backend core & API, Code map, Frontend (`frontend/src`, React 19 + Vite + Tailwind 4), Ignore these (no runtime role), Neural cache (neural_cache/, see its README.md), Scripts, Services (app/services), WhatsApp intelligence (app/services/whatsapp_intelligence)

### Community 163 - "_watcher_loop"
Cohesion: 0.15
Nodes (14): capture_screen_b64(), _get_active_process_name(), _get_active_window_title(), _pixel_diff_percent(), ndarray, Returns the foreground window title using WinAPI., Returns the executable name of the foreground window's process., Match window title / process name to a per-app prompt. (+6 more)

### Community 165 - "compiler"
Cohesion: 0.67
Nodes (3): _collect_google_fonts(), _walk(), Scans the scene graph and style registry for font families. Returns a Google…

### Community 166 - "TestO1Timing"
Cohesion: 0.50
Nodes (3): Return average time per (set + get) operation in microseconds., Per-op time for N=1000 vs N=100000 should be within 3x of each other. If the…, TestO1Timing

### Community 168 - "make_image_node"
Cohesion: 0.50
Nodes (4): make_image_node(), make_size(), Returns a complete IMAGE node., Returns size dict, only including non-None values.

### Community 169 - "small_cache"
Cohesion: 0.50
Nodes (4): large_cache(), fixture, LRU cache with capacity 3 — easy to reason about eviction., small_cache()

### Community 173 - "benchmark"
Cohesion: 0.14
Nodes (7): JSONFileBaseline, main(), measure_latency(), measure_throughput(), Spin up n_threads threads each doing ops_per_thread SET+GET pairs. Returns…, Mimics memory_tool.py's approach: every read/write touches disk. Uses a…, Run op_fn warmup times (discard), then timed times (measure). Returns (mean_µs,…

## Knowledge Gaps
- **166 isolated node(s):** `Settings`, `name`, `private`, `version`, `type` (+161 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1644 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **27 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Tool registry` connect `Tool registry` to `content_humanizer + content-tools`, `window_layout.py`, `youtube_control.py`, `syllabus_auditor`, `browser_mail.py`, `browser_tool.py`, `file_ops.py`, `assignment_answers.py`, `assemble_assignment`, `create_resume`, `ppt_router.py`, `rag_memory.py`, `air-drawing + air_drawing_tool`, `calendar_tool.py`, `skill_prompt_enhancer.py`, `dark_enhancement.py`, `web_search.py`, `edit`, `whatsapp_smart.py`, `spotify_service.py`, `_humanize_via_browser`, `recall`, `gmail_tool.py`, `chat.py`, `Assignment solver (5 phases)`, `assignment_pipeline.py`, `api/memory.py`, `extract_questions`?**
  _High betweenness centrality (0.136) - this node is a cross-community bridge._
- **Why does `open_air_drawing()` connect `air-drawing + air_drawing_tool` to `Tool registry`?**
  _High betweenness centrality (0.095) - this node is a cross-community bridge._
- **Are the 122 inferred relationships involving `Tool registry` (e.g. with `keyword_detect_tool()` and `_media_compound()`) actually correct?**
  _`Tool registry` has 122 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `chat_endpoint()` (e.g. with `describe_screen_for_llm()` and `get_screen_text_summary()`) actually correct?**
  _`chat_endpoint()` has 8 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Settings`, `name`, `private` to the rest of the system?**
  _166 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Tool registry` be split into smaller, more focused modules?**
  _Cohesion score 0.021917808219178082 - nodes in this community are weakly interconnected._
- **Should `reply_generator.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06108597285067873 - nodes in this community are weakly interconnected._