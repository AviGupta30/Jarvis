# Jarvis — Claude Code guide

Personal Windows-11 AI assistant (Iron-Man JARVIS persona). FastAPI backend + React/Vite UI + a separate voice-agent process, all funnelling into one `POST /chat` endpoint. LLM = Groq (`openai/gpt-oss-20b`, some `gpt-oss-120b`). ~31k lines, mostly `app/services/`.

**Read-first rule for saving tokens:** for a task on one feature, read **only** `docs/features/<slug>.md` (index: `docs/FEATURES.md`). It has the flow, gotchas and a current file/line table. Then use `graphify explain "<symbol>"` / `graphify affected "<symbol>"` / `graphify query "<q>" --budget 800` (ambiguous name → `path::symbol`), and read source **by line range** only. Wider references, only if needed: `docs/CODEMAP.md` (all files), `docs/TOOLS.md` (all tools), `docs/ARCHITECTURE.md`, `docs/KNOWN_ISSUES.md`. Big files, never read whole: `ppt_tool.py` (2.7k), `chat.py` (1.5k), `tools.py` (1.3k), `syllabus_auditor.py` (1k).
**After changing code:** run `python scripts/refresh_docs.py` (updates the line tables + rebuilds and labels the graph). Then edit the hand-written part of the touched feature doc(s), and `docs/KNOWN_ISSUES.md` / `docs/TOOLS.md` if relevant. The reusable task prompt is in `docs/PROMPT_TEMPLATE.md`.

## Run
```
uvicorn app.main:app --port 8000          # backend (auto-spawns neural_cache server on :9090 + floating prompt-Enhance button)
cd frontend && npm run dev                 # UI → talks to http://127.0.0.1:8000 (hardcoded)
python scripts/voice_agent.py              # mic/wake-word loop → POST /chat, speaks reply
python -m app.services.prompt_enhancer_button --install-autostart   # floating Enhance pill at Windows login (also spawned by backend)
python -m app.services.prompt_overlay      # optional Ctrl+Space prompt-enhancer popup
python -m pytest neural_cache/tests -v     # the only real test suite
```
Secrets in `.env` (see `app/core/config.py`): GROQ_API_KEY, GEMINI_API_KEY, MYSQL_URL, DATABASE_URL (pgvector), HF_API_KEY, ELEVENLABS_*, GPTZERO_API_KEY. Optional: GROQ_VISION_MODEL (image calls; gpt-oss can't take images), JARVIS_API_URL (voice agent/overlay), VITE_API_URL in `frontend/.env`. Google OAuth: `credentials.json`, `token.json`, `calendar_token.json` at repo root. Never print or commit these.

## Where things are
```
app/main.py              FastAPI app, startup hooks (cache server, RAG, tripwire, screen watcher), /upload /alerts /tripwire/*
app/api/chat.py          THE router: keyword_detect_tool() + chat_endpoint() pipeline (see docs/ARCHITECTURE.md)
app/api/{memory,ppt_router,tools}.py   /memory/*, /ppt/*, /execute
app/services/tools.py    TOOL_REGISTRY dict (bottom of file), the only tool surface the routers see
app/services/llm.py      Groq client, check_for_tool_intent(), generate_chat_response(), conversation_history
app/services/personality.py  JARVIS_SYSTEM_PROMPT + TOOL_ROUTER_PROMPT (tool list the LLM router sees)
app/services/*           one feature per file (see docs/CODEMAP.md)
app/memory/              ChromaDB skills/prefs (memory.py), facts.json, session.json
neural_cache/            standalone Redis-like LRU TCP server (own README)
frontend/src/            App.jsx (chat + SSE/DAG parsing), DagPlanPanel, MemorySidebar, AirDrawing/
scripts/                 voice_agent.py, jarvis_overlay.py, init/test scripts
3D/, AirDrawer_ref*/     older copies of AirDrawing, ignore (live copy: frontend/src/AirDrawing)
root *.py / *.txt        scratch/debug scripts & old diffs (chat_old.py etc.), ignore
```

## /chat request flow (short)
attached-file expansion → pending note/WhatsApp state machines → YouTube-mode follow-ups → resume detection (task_ledger) → **DAG path** if `is_dag_task()` (multi-intent, parallel, SSE JSON events) → else `keyword_detect_tool()` regex router → else LLM router `check_for_tool_intent()` → run `TOOL_REGISTRY[name](**args)` (generators are streamed raw; media tools run in a thread and reply verbatim) → optional dynamic-skill codegen → build context (tool result, pgvector RAG, screen) → `generate_chat_response()` streams plain text. Full detail: `docs/ARCHITECTURE.md`.

## Adding / changing a tool (project rules, from JARVIS_ARCHITECTURE.md)
1. Put the feature in its **own** `app/services/<name>.py`. Tool modules must not import other tool modules; orchestration goes through planner/DAG + TOOL_REGISTRY.
2. Wrap everything in try/except and **return a human-readable string** (or a generator of strings for progress). Never raise into FastAPI.
3. Stateless: persist via memory_tool / task_ledger / rag_memory, not module globals.
4. Must work for both UI and voice, i.e. only via `/chat`.
5. Outside chat.py, never call `TOOL_REGISTRY[x](...)` directly from async code. Use `await tool_runner.run_tool(name, args)`: it handles threads, generator tools and async `recall_memory`.
6. Wiring checklist: register in `TOOL_REGISTRY` (usually lazy `__import__` lambda) → describe it in `TOOL_ROUTER_PROMPT` (personality.py) → optionally add a regex in `keyword_detect_tool()` (chat.py; order matters, first match wins) → optionally list it in `PLANNER_PROMPT` (planner.py) / DAG prompt.

## Gotchas
- Windows-only (pywinauto, win32, pyautogui, WhatsApp Desktop UIA/OCR). Tests hitting the UI can't run headless.
- `conversation_history` is a global deque(20) persisted to `app/memory/session.json`; chat.py flow state (`api_whatsapp_flow`, etc.) is also module-global.
- Streaming responses: plain text for normal replies; `data: {json}\n\n` SSE for DAG. Frontend decides by the first chunk.
- Known bugs are listed in `docs/KNOWN_ISSUES.md`. Check there before "fixing" odd behaviour.
- After code changes run `graphify update .` (AST only, no API cost) to refresh the graph.

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
