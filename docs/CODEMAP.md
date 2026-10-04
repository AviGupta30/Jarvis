# Code map

One line per source file: what it does and its public entry points. Use this to pick a file **before** searching. Line counts are as of commit `cb8a3aa` (2026-09-28). For call relationships use `graphify explain "<symbol>"` or `graphify affected "<symbol>"`.

## Jump table for the big files
| File | Section | Line |
|---|---|---|
| `app/api/chat.py` | WhatsApp/note detectors | 43–103 |
| | `keyword_detect_tool()` regex cascade | 106–1057 |
| | `_semantic_window_adjust` (window layout parser) | 402 |
| | PPT keyword → `ppt_create` args (style, purpose, images) | 891–938 |
| | `chat_endpoint()` pipeline | 1066–1495 |
| `app/services/tools.py` | tool functions | 31–1080 |
| | `_mail_tool` (Gmail API → browser fallback), `_recall_memory_placeholder` | ~1082–1105 |
| | `TOOL_REGISTRY` | ~1107–end |
| `app/services/ppt_tool.py` | `PERSONALITIES` palettes | 48 |
| | `STYLE_PROFILES` | 158 |
| | Groq helpers / theme extraction | 603, 736 |
| | `PresentationBuilder` (+ `build_with_progress` 1175) | 834 |
| | layouts `_lay_aesthetic_{title,showcase,split,grid,poster,flow,timeline,comparison,metrics,pitch,gallery}` | 1195–2130 |
| | `_normalize_and_recover` (fix LLM slide JSON) | 2200 |
| | `ppt_create()` generator: outline → chunked content → chart data → images → save to Desktop | 2260–2620 |
| `app/services/personality.py` | `JARVIS_SYSTEM_PROMPT` / `TOOL_ROUTER_PROMPT` | 13 / 71 |
| `app/services/planner.py` | `PLANNER_PROMPT` / `run_agentic_plan` / `is_complex_task` | 36 / 259 / 353 |
| `app/services/dag_executor.py` | `DAGNode` / `is_dag_task` / `run_dag_plan` | 56 / 374 / 443 |

## Backend core & API

| File | Lines | Purpose | Public entry points |
|---|---|---|---|
| `app/main.py` | 251 | FastAPI app; mounts routers, /upload, /alerts, /tripwire/*, startup/shutdown hooks | read_root(), upload_file(), startup_event(), shutdown_event(), get_alerts(), tripwire_status(), tripwire_enable(), tripwire_disable(), tripwire_calibrate() |
| `app/core/config.py` | 21 | Settings from .env (API keys, MYSQL_URL, DATABASE_URL, GROQ_VISION_MODEL, JARVIS_API_URL) | Settings |
| `app/core/database.py` | 27 | asyncpg pool for Postgres/pgvector knowledge_store | init_db(), get_db_pool() |
| `app/core/mysql_db.py` | 126 | aiomysql pool; creates jarvis_memory DB + conversation_turns/faiss_meta tables | get_mysql_pool(), init_mysql(), close_mysql() |
| `app/api/chat.py` | 1502 | POST /chat: keyword router + whole request pipeline + WhatsApp/note state machines | ChatRequest, detect_whatsapp_call(), detect_whatsapp_send(), detect_note_intent(), keyword_detect_tool(), chat_endpoint(), clear_history() |
| `app/api/memory.py` | 135 | /memory/{ingest,recall,history,stats,forget} over rag_memory + pgvector | IngestRequest, RecallRequest, ForgetRequest, ingest_memory(), recall_memory(), get_history(), memory_stats(), forget_memory() |
| `app/api/ppt_router.py` | 163 | /ppt/{build,create,extract-theme,styles} | PPTBuildRequest, build_ppt(), PPTCreateRequest, create_ppt_backend(), PPTExtractThemeRequest, extract_theme(), PPTStylesResponse, get_styles() |
| `app/api/tools.py` | 31 | POST /execute: call any TOOL_REGISTRY entry directly | ToolExecuteRequest, execute_tool() |
| `app/memory/__init__.py` | 9 | re-exports memory.py helpers |  |
| `app/memory/memory.py` | 109 | ChromaDB (data/jarvis_memory): learned skills + user preferences | save_skill(), find_skill(), list_skills(), save_preference(), get_all_preferences(), format_preferences_for_prompt() |

## Services (app/services)

| File | Lines | Purpose | Public entry points |
|---|---|---|---|
| `app/services/acoustic_tripwire.py` | 442 | Double-clap wake detector (RMS + freq) with calibration; singleton engine | calibrate_tripwire(), AcousticWakeEngine, get_engine(), get_wake_event() |
| `app/services/agentic_web.py` | 323 | Search → fetch pages → LLM-extract listings; generator streaming progress | agentic_web_action() |
| `app/services/air_drawing_tool.py` | 7 | Returns [OPEN_AIR_DRAWING] marker that makes the frontend open AirDrawing | open_air_drawing() |
| `app/services/assignment_answers.py` | 596 | Phase 2: answers via Playwright AI sites (Gemini/ChatGPT/DeepSeek) → Groq fallback | generate_answers(), generate_answer() |
| `app/services/assignment_assembler.py` | 194 | Phase 4: build Word/PPTX from QA JSON | assemble_assignment() |
| `app/services/assignment_humanizer.py` | 642 | Phase 3: humanize via paraphraser sites → Groq fallback; protects code/math | humanize_text(), humanize_all_answers() |
| `app/services/assignment_pipeline.py` | 622 | Phase 5: do_assignment() end-to-end orchestrator (browser thread) | do_assignment() |
| `app/services/assignment_tool.py` | 780 | Phase 1: extract questions from PDF (regex + vision + LLM tracks, merged) | extract_questions(), list_assignments() |
| `app/services/browser_mail.py` | 97 | Gmail via opening pre-filled browser URLs (the registered email tools) | check_emails(), list_unread(), get_email_body(), summarize_inbox(), smart_mail_action() |
| `app/services/browser_tool.py` | 263 | Playwright anti-bot browser: browse/search/click/scroll/fill_form/paginate + LLM extract | browse_and_read(), search_on_site(), click_element(), scroll_and_read(), fill_form(), browse_and_paginate() |
| `app/services/calendar_tool.py` | 219 | Google Calendar API (calendar_token.json): today, upcoming, add_event | get_upcoming_events(), check_today_schedule(), add_event() |
| `app/services/content_humanizer.py` | 287 | 5-stage AI-text humanizer (sentence scoring, rewrite, micro-errors, similarity check) | get_groq_client(), get_similarity_model(), get_sentence_scores(), detect_tone(), build_structure_prompt(), build_vocab_prompt(), call_groq(), rewrite_sentences(), reshape_paragraphs(), inject_micro_errors() … |
| `app/services/context_classifier.py` | 160 | Classify input: language (en/hinglish/hindi), mood, urgency, topic, hour | detect_language(), classify_context() |
| `app/services/dag_executor.py` | 629 | Parallel DAG planner: is_dag_task(), run_dag_plan() SSE events, waves, retries, aggregate | DAGNode, is_dag_task(), run_dag_plan() |
| `app/services/dark_enhancement.py` | 159 | Low-light image pipelines (HSV/gamma, Retinex + wavelet fusion) | run_pipeline_a(), run_pipeline_b(), get_all_enhancements() |
| `app/services/dark_video_enhancement.py` | 115 | Frame-sampled video enhancement + ffmpeg H.264 re-encode | process_video_smartly() |
| `app/services/dsa_enforcer.py` | 317 | LeetCode DSA mode: browser enforcement loop, hides tags/hints, tracks solved (neural cache) | DSAEnforcer, get_dsa_enforcer() |
| `app/services/dynamic_skill.py` | 166 | LLM writes Python for unknown tasks, runs via safe_executor, caches in ChromaDB | run_dynamic_skill() |
| `app/services/embeddings.py` | 20 | fastembed BAAI/bge-small-en-v1.5 → 384-d vectors (async wrapper) | get_embedding() |
| `app/services/file_ops.py` | 461 | Path shortcuts + read (txt/pdf/docx)/write/append/list/move/trash/search/rename/diff | read_file(), write_file(), append_file(), list_directory(), move_file(), delete_file(), search_files(), create_folder(), bulk_rename(), diff_files() |
| `app/services/gmail_tool.py` | 341 | Gmail API OAuth (token.json): search/unread triage/body/summary (not in registry) | check_emails(), list_unread(), get_email_body(), summarize_inbox() |
| `app/services/hinglish_normalizer.py` | 108 | Strip Devanagari / normalise text before TTS | normalize_for_tts() |
| `app/services/tool_runner.py` | 43 | Async runner for registry tools used by planner/DAG//execute: thread pool, consumes generator tools, awaits recall_memory | run_tool() |
| `app/services/llm.py` | 245 | Groq client, tool-intent router, streaming chat reply (FAST_MODEL 20b / DEEP_MODEL 120b), history deque + compression | check_for_tool_intent(), generate_chat_response() |
| `app/services/media_enhancement.py` | 60 | enhance_media(): dispatch image/video to dark enhancement | enhance_media() |
| `app/services/memory_tool.py` | 203 | facts.json save/recall/update/forget; facts-as-context; LLM morning brief (calendar+gmail) | save_fact(), recall_facts(), update_fact(), forget_fact(), get_all_facts_as_context(), get_morning_brief() |
| `app/services/nlp_extractor.py` | 108 | Groq fact/statistic extraction from scraped text | NLPExtractor |
| `app/services/personality.py` | 238 | JARVIS_SYSTEM_PROMPT, TOOL_ROUTER_PROMPT, time/mood/language-aware prompt builder | get_context_aware_prompt() |
| `app/services/planner.py` | 466 | Linear agentic planner (plan → execute → replan) + is_complex_task() heuristic | run_agentic_plan(), is_complex_task() |
| `app/services/ppt_chart_engine.py` | 602 | matplotlib charts (bar/pie/line/comparison/metrics/timeline) themed to palette → PNG bytes | ChartEngine |
| `app/services/ppt_image_engine.py` | 314 | Match user images to slides (keywords, explicit refs, aspect ratio) | ImageDescriptor, get_aspect_ratio(), build_image_descriptors(), match_images_to_slides() |
| `app/services/ppt_tool.py` | 2667 | PPT entry points (ppt_create → ppt_studio, ppt_edit) + legacy v5 engine (fallback, /ppt/build), PERSONALITIES, theme-from-image | SlotGeometry, compute_split_geometry(), extract_theme_from_image(), PresentationBuilder, ppt_create(), ppt_styles() |
| `app/services/ppt_studio.py` | 609 | PPT v6 orchestrator: create/edit/undo, image assignment, fixed-format templates, deck state in data/ppt_decks | create(), edit(), has_active_deck(), _assign_images(), _create_format() |
| `app/services/ppt_content.py` | 1164 | PPT content brain: profile/density, strict "Slide N:" parser, kind inference, LLM outline+content, follow-up edit ops | parse_user_slides(), infer_kind(), generate_deck(), apply_edit() |
| `app/services/ppt_designer.py` | 1769 | PPT adaptive renderer: themes, real-font text fitting, content/aspect-driven layouts, native charts/tables | THEMES, resolve_theme(), DeckRenderer, place_image(), justified_rows() |
| `app/services/ppt_composer.py` | ~780 | PPT composite "infographic" slides: section pills, icon cards, framed screenshots with captions, highlight band; layout search (image width × 1/2/3-col masonry × band × compact) for the largest font that fits | render_sections(), render_title_sections(), _norm_sections() |
| `app/services/ppt_research.py` | ~420 | PPT anti-hallucination: Wikipedia + web (ddgs) sources, verbatim fact extraction (no LLM), fact retrieval, slide audit (numbers/years/quotes/URLs) and deterministic scrub | gather_sources(), extract_facts(), relevant_facts(), audit_slide(), scrub_slide() |
| `app/services/ppt_template.py` | 1014 | Fill a user .pptx/.potx keeping its design: format / clone / layout modes | TemplateFiller, analyze_format(), fill_form_slide(), clone_slide() |
| `app/services/prompt_enhancement_library.py` | 415 | Enhancer templates, domain detection, output validation/cleanup | classify_prompt(), check_for_hallucination(), strip_chatbot_filler(), strip_leaked_reasoning(), validate_enhancement(), detect_domain() |
| `app/services/prompt_overlay.py` | 360 | Tkinter Ctrl+Space popup; sends enhance request to /chat and pastes the result | PromptOverlay, main() |
| `app/services/rag_memory.py` | 486 | Long-term memory: store_turn/recall/forget over MySQL + FAISS (bge-small embeddings) | init_rag_memory(), smart_filter(), store_turn(), recall(), format_recall_for_prompt(), get_memory_stats(), get_history(), forget_turns() |
| `app/services/research_pipeline.py` | 37 | research_topic(): scraper + NLP extractor → facts for PPT | research_topic() |
| `app/services/research_scraper.py` | 96 | DDG search + BeautifulSoup scraping for research | ResearchScraper |
| `app/services/resume_detector.py` | 320 | Detect "continue/extend that" intent and build resume context from the ledger | detect_resume_intent(), get_resume_context_string() |
| `app/services/safe_executor.py` | 184 | AST-validated restricted exec sandbox for generated code | SecurityError, SafetyVisitor, execute_safe() |
| `app/services/screen_reader.py` | 328 | Layered screen reading: VLM → Groq vision → OCR → UIA tree → window title | read_screen(), describe_screen_for_llm(), read_screen_as_tool(), get_screen_screenshot_b64() |
| `app/services/screen_vision.py` | 511 | Screen capture (mss) → vision LLM; intent modes; background pixel-diff watcher | capture_screen_b64(), understand_screen(), describe_screen_vlm(), start_background_watcher(), stop_background_watcher() |
| `app/services/skill_prompt_enhancer.py` | 124 | Prompt enhancer: faithful rewrite via Groq 120b (code blocks protected, chatbot/bloat guards + retry) | enhance_prompt(), enhance_prompt_text() |
| `app/services/prompt_enhancer_button.py` | 931 | Floating click-only "✦ Enhance" pill that follows focus to prompt boxes in AI sites/apps/IDE chat panels (UIA), Ctrl+A/C → enhance → Ctrl+A/V (+SetValue fallback); spawned by main.py, optional login autostart | EnhanceButton, classify_app(), is_prompt_box(), main() |
| `app/services/smart_navigator.py` | 194 | Visible-browser site navigation (resolve site name → URL → search) | smart_web_action() |
| `app/services/social_content_manager.py` | 189 | Social post generation/refinement per platform/tone | build_prompt(), call_llm(), generate_social_content(), refine_social_content() |
| `app/services/spotify_service.py` | 107 | Spotify desktop GUI automation: search + play song | play_song_dynamic() |
| `app/services/ssml_processor.py` | 100 | Add prosody pauses/SSML for TTS; strip_ssml | add_human_prosody(), strip_ssml() |
| `app/services/syllabus_auditor.py` | 1046 | YouTube playlist transcripts vs syllabus image → coverage report (Chroma + MiniLM + LLM verify) | audit_playlist_syllabus() |
| `app/services/task_ledger.py` | 287 | app/data/task_ledger.json log of completed tool runs; prompt summary; resumable lookup | log_task(), get_recent_tasks(), get_recent_tasks_raw(), find_resumable_task(), update_task(), get_task_ledger_for_prompt() |
| `app/services/tools.py` | 1275 | TOOL_REGISTRY + ~70 small OS/web/media tool functions (win32, pyautogui, clipboard, sticky notes, copilot, cache) | read_my_screen(), play_video_in_browser(), get_weather(), get_info(), open_safe_website(), open_google_search_in_browser(), youtube_search(), get_system_time(), get_system_info(), take_screenshot() … |
| `app/services/ui_inspector.py` | 429 | pywinauto UIA engine: find/click/type/read elements, dump tree, active-window info | UIAEngine, click_ui_element(), smart_click(), type_into_element(), read_element_text(), debug_ui_tree(), get_active_window_info(), get_screen_text_summary() |
| `app/services/vector_store.py` | 32 | pgvector save/search for knowledge_store | save_document_chunk(), search_similar_chunks() |
| `app/services/voice.py` | 875 | STT (Groq whisper-large-v3-turbo → local faster-whisper), TTS (edge-tts streamed, en-GB Ryan / hi-IN Madhur, SAPI fallback), multi-channel Speaker | transcribe_pcm(), transcribe_audio(), Speaker, start_clip(), speak_text(), speak_stream() |
| `app/services/web_search.py` | 346 | DuckDuckGo HTML + Wikipedia + scrape_url/search_site + LLM synthesis (smart_search) | scrape_url(), search_site(), smart_search() |
| `app/services/whatsapp.py` | 94 | Legacy WhatsApp Desktop keyboard automation (open/send) | open_whatsapp(), send_whatsapp_message() |
| `app/services/whatsapp_call.py` | 143 | WhatsApp Desktop voice call (2-phase confirm, clicks call button) | initiate_whatsapp_call(), confirm_whatsapp_call() |
| `app/services/whatsapp_smart.py` | 389 | WhatsApp Desktop: fuzzy contact search (OCR), 2-phase confirm send, read via OCR | open_whatsapp(), search_whatsapp_contact(), initiate_whatsapp_send(), confirm_whatsapp_send(), read_whatsapp_messages() |
| `app/services/window_layout.py` | 494 | Win32 window finding/snap/resize/min/max/close (fuzzy app-name match) | win32_find_window(), adjust_active_window(), win32_focus_window(), win32_minimize_window(), win32_maximize_window(), win32_close_window(), win32_close_active_window(), win32_close_active_tab(), win32_snap_two_windows() |

## WhatsApp intelligence (app/services/whatsapp_intelligence)

| File | Lines | Purpose | Public entry points |
|---|---|---|---|
| `app/services/whatsapp_intelligence/message_reader.py` | 359 | Read visible messages via UIA, OCR fallback | read_messages(), read_messages_as_string() |
| `app/services/whatsapp_intelligence/reply_generator.py` | 403 | 3 style-matched reply drafts (Groq), cached; send_style_reply | generate_reply_draft(), get_cached_drafts(), get_cached_contact(), get_cached_incoming(), send_style_reply() |
| `app/services/whatsapp_intelligence/style_profiler.py` | 400 | Learn your reply style from a .txt export; per-contact profiles | record_sent_reply(), mark_contact_formal(), add_deflection_phrase(), build_style_profile(), get_profile(), get_profile_summary() |
| `app/services/whatsapp_intelligence/thread_extractor.py` | 252 | Open a contact chat and build a structured thread | extract_thread(), extract_thread_as_string() |

## Neural cache (neural_cache/, see its README.md)

| File | Lines | Purpose | Public entry points |
|---|---|---|---|
| `neural_cache/__init__.py` | 2 | package marker |  |
| `neural_cache/benchmark.py` | 269 | Latency/throughput vs JSON-file baseline | JSONFileBaseline, measure_latency(), measure_throughput(), main() |
| `neural_cache/client.py` | 224 | Thread-safe CacheClient with auto-reconnect | CacheClient |
| `neural_cache/engine.py` | 224 | Single-writer command queue owning the LRU | CacheEngine |
| `neural_cache/lru.py` | 231 | Hand-rolled O(1) LRU (dict + doubly linked list), TTL, snapshot | Node, LRUCache |
| `neural_cache/persistence.py` | 205 | WAL writer + periodic snapshot manager | WALWriter, SnapshotManager |
| `neural_cache/protocol.py` | 121 | 4-byte length-prefixed JSON wire format | encode_message(), decode_message(), ok_response(), err_response() |
| `neural_cache/server.py` | 270 | TCP server :9090, thread per client, WAL/snapshot recovery (python -m neural_cache.server) | CacheServer, main() |

## Scripts

| File | Lines | Purpose | Public entry points |
|---|---|---|---|
| `scripts/download_kokoro.py` | 38 | Download Kokoro TTS model into models/ | download() |
| `scripts/init_rag_memory.py` | 113 | One-time MySQL/FAISS init | main() |
| `scripts/jarvis_overlay.py` | 190 | Floating arc-reactor Tk window animated by voice state | read_state(), generate_arc_reactor(), JarvisOverlay |
| `scripts/refresh_docs.py` | ~290 | Regenerates docs/features/*.md line tables (FEATURES map) + rebuilds/labels graphify graph + wiki. Run after every code change | write_docs(), refresh_graph(), label_communities() |
| `scripts/test_hindi_tts.py` | 26 | Manual TTS test | main() |
| `scripts/test_humanizer.py` | 27 | Manual humanizer test | test() |
| `scripts/test_language.py` | 41 | Manual language classifier test |  |
| `scripts/test_rag_memory.py` | 70 | Manual RAG memory smoke test | test() |
| `scripts/test_routing.py` | 36 | Manual keyword-router checks |  |
| `scripts/voice_agent.py` | 669 | Voice loop: always-on mic thread + Silero VAD, wake word/clap/follow-up, echo + stop handling, concurrent /chat commands | MicListener, VoiceAgent, extract_wake_word_command(), stream_chat(), run_voice_agent() |

## Frontend (`frontend/src`, React 19 + Vite + Tailwind 4)
| File | Lines | Purpose |
|---|---|---|
| `config.js` | 2 | `API_BASE` backend URL (`VITE_API_URL` override) |
| `App.jsx` | 571 | App shell: messages (persisted in localStorage), mode state, `/upload` (+ drag/drop/paste), `runRequest` stream reader for `/chat` and `/ppt/create` (plain text vs DAG SSE, DAG state per message), stop/regenerate, tripwire + `/alerts` polling, dictation, AirDrawing overlay |
| `ChatMessage.jsx` | 193 | Markdown message (code copy, file chips, media cards), inline DagPlanPanel, copy/regenerate |
| `DagPlanPanel.jsx` | 145 | Live DAG plan/node status panel (collapsible, progress bar) |
| `modes.js` | 312 | Mode definitions (Chat, Resume Creator, PPT Generator, Deep Research, Assignment, Humanizer) + `buildRequest` |
| `components/*.jsx` | ~750 | Sidebar, Composer, EmptyState, MemoryPanel (`/memory/*`), Toasts, Orb |
| `AirDrawing/AirDrawingApp.jsx` | 275 | Webcam air-drawing overlay root |
| `AirDrawing/components/*` | ~1000 | CameraView, DrawingCanvas, HandSkeleton, ControlPanel, HelpPanel |
| `AirDrawing/modules/handTracking.js` | 50 | MediaPipe hands setup |
| `AirDrawing/modules/gesture{Interpreter,Controller}.js` | 282 | Landmarks → gestures → actions |
| `AirDrawing/modules/{drawingEngine,strokeManager,strokeRefiner,shapeManager,transformEngine,interactionEngine}.js` | ~1050 | Stroke capture/smoothing, shape detection, move/scale/rotate |

## Ignore these (no runtime role)
- `3D/`, `AirDrawer_ref/`, `AirDrawer_ref_new/`: older standalone copies of AirDrawing (`3D/dist` is still mounted at `/airdrawing`, but the UI uses `frontend/src/AirDrawing`).
- Root scratch files: `chat_old.py`, `patch*.py`, `debug_wa.py`, `dump_*.py`, `find_call_btn.py`, `get_btn_pos.py`, `test_*.py` (manual one-offs, not a test suite), `*_diff.txt`, `diff_utf8.txt`, `spotify_*.txt`, `test_*.pptx`, `wa_*.png`, `verify.txt`, `H tab requires write-off space.~.txt`.
- `data/`, `models/`, `graphify-out/`, `__pycache__/`, `node_modules/`.
- `JARVIS_ARCHITECTURE.md`: the original design rules. Its module list is partly stale (it mentions `dynamic_tool.py`, `vector_score.py`, `safe_executer.py`); `CLAUDE.md` + `docs/` are current.
