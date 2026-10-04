# Architecture

## Processes
| Process | Entry | Talks to |
|---|---|---|
| Backend API | `uvicorn app.main:app --port 8000` | Groq, Gemini (key gate only), MySQL, Postgres/pgvector, local OS |
| Neural Cache | spawned by `app/main.py` startup → `neural_cache/server.py` on 127.0.0.1:9090 | used by `tools.cache_*`, `dsa_enforcer` |
| Web UI | `frontend/` (Vite + React 19 + Tailwind 4) | `API_BASE` from `frontend/src/config.js` (`VITE_API_URL`, default `http://127.0.0.1:8000`) |
| Voice agent | `scripts/voice_agent.py` | mic → faster-whisper STT → `POST /chat` (streamed) → Kokoro/edge-tts |
| Arc-reactor overlay | `scripts/jarvis_overlay.py` | reads UI state file written by voice_agent |
| Prompt enhancer popup | `python -m app.services.prompt_overlay` (Ctrl+Space) | `POST /chat` with "enhance …" |

## HTTP endpoints
- `app/main.py`: `GET /`, `POST /upload` (→ `data/uploads/`, served at `/media`), `GET /alerts` (screen-watcher queue), `GET /tripwire/status`, `POST /tripwire/{enable,disable,calibrate}`, static `/airdrawing` (→ `3D/dist`).
- `app/api/chat.py`: `POST /chat {prompt}` → streamed text or SSE; `DELETE /chat/history`.
- `app/api/memory.py` (prefix `/memory`): `POST /ingest`, `POST /recall`, `GET /history`, `GET /stats`, `DELETE /forget`.
- `app/api/ppt_router.py` (prefix `/ppt`): `POST /build` (from JSON plan), `POST /create` (end-to-end), `POST /extract-theme`, `GET /styles`.
- `app/api/tools.py`: `POST /execute {tool_name, arguments}` → direct `TOOL_REGISTRY` call.

Startup (`app/main.py:startup_event`), each step non-fatal: spawn neural cache → `init_rag_memory()` (MySQL + FAISS) → acoustic tripwire thread (double-clap wake) → screen watcher thread (only if `GEMINI_API_KEY` set).

## `/chat` pipeline (`app/api/chat.py:chat_endpoint`, L1066)
Order matters; the first stage that returns wins.
1. **Attachments.** `[ATTACHED_FILE: path | DESCRIPTION: …]` tags in the prompt: text-like files are read via `file_ops.read_file` and appended as "Attached Context". Tags stay in the prompt so media/PPT tools can use the paths.
2. **Pending flows** (module-global dicts): `api_note_flow` (next message becomes a sticky note), `api_whatsapp_call_flow` (yes/no confirm), `api_whatsapp_flow` (ask_contact → ask_message → confirm). Yes/no uses English and Hindi keyword lists.
3. **New note / WhatsApp intents.** `detect_note_intent`, `detect_whatsapp_call`, `detect_whatsapp_send` start the flows above.
4. **Task resumption.** `task_ledger.get_recent_tasks_raw` + `resume_detector.detect_resume_intent`. If the user is continuing a prior task, the original context is prepended to the prompt.
5. **DAG path.** `dag_executor.is_dag_task` (≥5 words, a conjunction, ≥2 domains or a multi-branch regex; excludes assignment/PPT/search). `run_dag_plan` gets an LLM DAG, runs a Kahn topo-sort into waves (`MAX_PARALLEL=2`, retries + fallback_tool), then an aggregate node. It streams `data: {"type": thinking|plan|node_start|node_done|node_failed|narration|aggregate|error|fallback|done}`. On a planning failure or cycle it falls back to the linear `planner.run_agentic_plan`. History and RAG are saved after the stream.
6. **Keyword router.** `keyword_detect_tool` (L106–1057) is a big ordered regex/keyword cascade that returns `{tool_name, arguments}`, or a `StreamingResponse` for "enhance/refine …". It returns None early when `planner.is_complex_task`. Categories in order: weather → Spotify/YouTube/browser-video/media → news/sports/finance → time → screenshot → volume → enhance media → prompt enhancer → WhatsApp → agentic web → window layout (`_semantic_window_adjust`) → close/min/max → screen read (describe/suggest/execute) → search-on-site → scrape URL → file ops → calendar → morning brief → memory recall → Gmail → generic "open X" → assignment phases → PPT create/edit/styles → syllabus audit → social content.
7. **LLM router.** `llm.check_for_tool_intent` (Groq JSON mode, temp 0, `max_tokens=600`, `reasoning_effort="low"`, last 6 history msgs, `TOOL_ROUTER_PROMPT`).
7b. **Linear planner.** If no tool was chosen and `planner.is_complex_task(prompt)`, `run_agentic_plan` is streamed as plain text lines, then history/RAG are saved.
8. **Execute.**
   - `ask_for_clarification`: stream the question.
   - `recall_memory`: async FAISS recall.
   - Otherwise `TOOL_REGISTRY[name](**args)`. If it returns a **generator** (PPT, agentic web, assignment pipeline…), each chunk is streamed straight to the client and the LLM step is skipped.
   - Successful calls get logged to the task ledger.
   - Special direct returns: WhatsApp send/call/search, `enhance_media`, `generate_social_content`.
9. **Dynamic skill.** Runs if nothing matched and the prompt has automation words (rename/compress/batch…). `dynamic_skill.run_dynamic_skill` has the LLM write Python, runs it in `safe_executor`'s AST sandbox, and caches successes in ChromaDB.
10. **Context build.** Tool result + pgvector RAG (`embeddings` + `vector_store`, knowledge questions only) + screen description (`screen_reader.describe_screen_for_llm`, only when no tool ran) + task-ledger summary.
11. **Respond.** `llm.generate_chat_response` builds its system prompt from `personality.get_context_aware_prompt(hour, mood, language)` (+urgency/topic hints from `context_classifier`), `memory_tool` facts, FAISS recall (top 5, ≥0.30), and history (compressed when >15 msgs). It streams plain tokens: `llm.DEEP_MODEL` (gpt-oss-120b) when `_is_complex_response` (long tool result or explain/why/debug… wording), otherwise `llm.FAST_MODEL` (gpt-oss-20b).

**Non-streaming tool calls** (planner steps, DAG nodes, `POST /execute`) go through `app/services/tool_runner.run_tool(name, args)`. It runs the tool in a thread pool, joins generator output into one string, and awaits `recall_memory` itself.

## LLM usage
- Groq `openai/gpt-oss-20b`: router, simple chat, planner, DAG, most tools.
- Groq `openai/gpt-oss-120b`: complex chat replies, PPT content, social content, prompt enhancer, content humanizer, syllabus verify.
- Groq `settings.GROQ_VISION_MODEL` (default `qwen/qwen3.8-27b`): every call that sends an image (screen vision/reader, assignment page vision, syllabus image, PPT theme). gpt-oss models reject image input.
- Groq `whisper-large-v3`: STT fallback.
- Local models: fastembed `BAAI/bge-small-en-v1.5` (384-d) for RAG, sentence-transformers MiniLM (syllabus auditor, humanizer), faster-whisper base (STT), Kokoro ONNX (TTS), edge-tts fallback.
- Browser automation (Playwright): assignment answers via Gemini/ChatGPT/DeepSeek web UIs, humanizer sites, `browser_tool`.

## Memory layers (five separate stores)
| Store | File/DB | Module | Used for |
|---|---|---|---|
| Short-term history | `app/memory/session.json` (deque 20) | `llm.py` | chat context |
| User facts | `app/memory/facts.json` | `memory_tool.py` | injected in every system prompt, morning brief |
| Long-term turns | MySQL `jarvis_memory.conversation_turns` + `data/jarvis_faiss.index` | `rag_memory.py`, `core/mysql_db.py` | auto-recall, `/memory/*` |
| Knowledge chunks | Postgres pgvector `knowledge_store` (`DATABASE_URL`, currently unreachable) | `core/database.py`, `vector_store.py` | RAG for "what/how…" questions; `/memory/ingest` falls back to MySQL memory |
| Skills + prefs | ChromaDB `data/jarvis_memory/` | `app/memory/memory.py` | dynamic-skill reuse, preferences |
| Task ledger | `app/data/task_ledger.json` | `task_ledger.py` | resume / "what did you just do" |
| WhatsApp style | `app/services/whatsapp_intelligence/style_profiles/` | `style_profiler.py` | reply cloning |
| KV cache | neural_cache WAL+snapshot | `neural_cache/` | DSA mode state, `cache_get/set` |

## Frontend (`frontend/src`)
- `App.jsx` (859 L): chat UI, file upload menu (→ `/upload`, then inserts `[ATTACHED_FILE: …]`), PPT theme image, tripwire toggle, SSE reader. The first chunk decides the mode: `data: {` = DAG events → `DagPlanPanel`; anything else is appended to the message as raw text. The `[OPEN_AIR_DRAWING]` marker in a reply opens `AirDrawing/AirDrawingApp`.
- `ChatMessage.jsx`: markdown + syntax highlighting. `DagPlanPanel.jsx`: live node graph. `modes.js`: per-mode uploads/options/prompt building (`buildRequest`). `components/MemoryPanel.jsx`: memory drawer (stats, recall, forget, ingest).
- `AirDrawing/`: MediaPipe hand tracking → gesture interpreter → stroke/shape/transform engines on a canvas (`modules/*.js`).

## Voice path (`scripts/voice_agent.py`)
PyAudio 16 kHz. Noise calibration, then wake word (fuzzy "jarvis") or double clap (tripwire `process_chunk` inline, sharing the mic stream). Recording runs until silence, then `voice.transcribe_audio` (faster-whisper → Groq fallback), then `POST /chat` streamed. Replies are spoken sentence by sentence (`hinglish_normalizer` + `ssml_processor` → Kokoro/edge-tts). The mic is flushed after TTS to avoid echo.
