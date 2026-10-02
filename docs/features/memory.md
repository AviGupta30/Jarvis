# Memory: RAG, facts, task ledger, resume, skills

## Purpose
Everything Jarvis remembers, across 6 separate stores.

| Store | Where | Module | Used by |
|---|---|---|---|
| Short-term history | `app/memory/session.json` (deque 20) | llm.py | every reply |
| User facts | `app/memory/facts.json` | memory_tool (`save_fact`, `recall_facts`, `update_fact`, `forget_fact`, fuzzy via rapidfuzz) | injected into every system prompt; morning brief |
| Long-term turns | MySQL `jarvis_memory.conversation_turns` + `data/jarvis_faiss.index` (+ids json) | rag_memory, core/mysql_db | auto-recall every reply; `recall_memory` tool; `/memory/*` |
| Knowledge chunks | Postgres pgvector `knowledge_store` (`DATABASE_URL`, **currently unreachable**) | core/database, vector_store | "what/how" RAG in chat.py; `/memory/ingest` falls back to MySQL memory |
| Skills + prefs | ChromaDB `data/jarvis_memory/` | app/memory/memory.py | dynamic skills, `remember_preference` |
| Task ledger | `app/data/task_ledger.json` (20 entries FIFO) | task_ledger + resume_detector | "continue that", ledger summary in prompts |

## RAG details
fastembed `BAAI/bge-small-en-v1.5` (384-d) → FAISS `IndexFlatIP`. `store_turn` skips trivial/short (<12 chars) turns and MD5 duplicates, and tags topics by keywords. `recall(query, top_k, min_score)`. `forget_turns` soft-deletes. The server boots it in `main.startup_event` via `init_rag_memory`. One-time setup: `scripts/init_rag_memory.py`, `scripts/setup_mysql.bat`.

## API
`/memory/ingest`, `/memory/recall`, `/memory/history`, `/memory/stats`, `/memory/forget`.

## Gotchas
- MySQL must be running locally (`MYSQL_URL`); otherwise storing is skipped silently.
- The aiomysql pool is bound to the server's event loop. Call rag_memory only from async code on that loop (`tool_runner` handles `recall_memory`).
- Test: `scripts/test_rag_memory.py`.

## Graphify
`graphify explain "store_turn"` · `graphify explain "recall"` · `graphify explain "log_task"`

<!-- AUTO:BEGIN (scripts/refresh_docs.py) -->
## Files & symbols (auto-generated, line numbers are current)

- `app/services/rag_memory.py` (487 lines): rag_memory.py — Jarvis Long-Term RAG Memory Engine
  L45 _get_faiss_lock() · L76 _load_faiss_index() · L100 _save_faiss_index() · L112 _save_faiss_index_async() · L118 init_rag_memory() · L136 smart_filter() · L151 _extract_topics() · L168 store_turn() · L255 recall() · L346 format_recall_for_prompt() · L372 get_memory_stats() · L401 get_history() · L454 forget_turns()
- `app/core/mysql_db.py` (127 lines): mysql_db.py — Jarvis Async MySQL Connection Pool
  L18 get_mysql_pool() · L26 init_mysql() · L119 close_mysql()
- `app/api/memory.py` (146 lines): app/api/memory.py — Jarvis Long-Term Memory API Router
  L23 class IngestRequest · L26 class RecallRequest · L31 class ForgetRequest · L38 ingest_memory() · L63 recall_memory() · L92 get_history() · L117 memory_stats() · L131 forget_memory()
- `app/services/memory_tool.py` (204 lines): memory_tool.py — Jarvis Persistent Memory (Step 10 — ENHANCED)
  L22 _ensure_memory_file() · L27 _load_memory() · L34 _save_memory() · L40 _fuzzy_match_topics() · L52 save_fact() · L74 recall_facts() · L105 update_fact() · L130 forget_fact() · L143 get_all_facts_as_context() · L159 get_morning_brief()
- `app/services/task_ledger.py` (288 lines): task_ledger.py — Jarvis Task Context Ledger
  L36 _MAX_ENTRIES · L50 _ensure_ledger_file() · L57 _load_ledger() · L66 _save_ledger() · L79 log_task() · L118 get_recent_tasks() · L143 get_recent_tasks_raw() · L158 find_resumable_task() · L218 update_task() · L243 get_task_ledger_for_prompt()
- `app/services/resume_detector.py` (321 lines): resume_detector.py — Jarvis Resume Intent Classifier
  L25 _REFERENCE_PATTERNS · L75 _FRESH_TASK_INDICATORS · L84 _TASK_RESUME_ACTIONS · L105 _CONTEXT_PATH_KEYS · L110 _has_reference_phrase() · L119 _has_fresh_task_indicator() · L128 _has_continuation_verb() · L134 _extract_task_resource() · L149 _find_best_task_match() · L197 detect_resume_intent() · L272 get_resume_context_string()
- `app/memory/memory.py` (110 lines): Jarvis Vector Memory — ChromaDB-based long-term memory engine.
  L32 _uid() · L39 save_skill() · L50 find_skill() · L74 list_skills() · L84 save_preference() · L94 get_all_preferences() · L103 format_preferences_for_prompt()
- `app/services/embeddings.py` (21 lines)
  L9 get_embedding()
- `app/services/vector_store.py` (33 lines)
  L3 save_document_chunk() · L18 search_similar_chunks()
- `app/core/database.py` (30 lines)
  L6 init_db() · L25 get_db_pool()
<!-- AUTO:END -->
