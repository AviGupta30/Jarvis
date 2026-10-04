# memory_tool + memory

> 24 nodes · cohesion 0.14

## Key Concepts

- **memory_tool.py** (16 connections) — `app/services/memory_tool.py`
- **forget_fact()** (7 connections) — `app/services/memory_tool.py`
- **_load_memory()** (7 connections) — `app/services/memory_tool.py`
- **Memory: RAG, facts, task ledger, resume, skills** (7 connections) — `docs/features/memory.md`
- **Purpose** (7 connections) — `docs/features/memory.md`
- **recall_facts()** (6 connections) — `app/services/memory_tool.py`
- **save_fact()** (6 connections) — `app/services/memory_tool.py`
- **update_fact()** (6 connections) — `app/services/memory_tool.py`
- **get_all_facts_as_context()** (5 connections) — `app/services/memory_tool.py`
- **_save_memory()** (5 connections) — `app/services/memory_tool.py`
- **_fuzzy_match_topics()** (4 connections) — `app/services/memory_tool.py`
- **_ensure_memory_file()** (3 connections) — `app/services/memory_tool.py`
- **Gotchas** (2 connections) — `docs/features/memory.md`
- **memory_tool.py — Jarvis Persistent Memory (Step 10 — ENHANCED)…** (1 connections) — `app/services/memory_tool.py`
- **Replace an existing fact with an updated version.** (1 connections) — `app/services/memory_tool.py`
- **Remove all facts under a topic.** (1 connections) — `app/services/memory_tool.py`
- **Returns a compact string of all saved facts for injecting into LLM system…** (1 connections) — `app/services/memory_tool.py`
- **Return topics that fuzzy-match the query. Falls back to substring if rapidfuzz…** (1 connections) — `app/services/memory_tool.py`
- **Save a fact about the user or system to persistent memory with timestamp.** (1 connections) — `app/services/memory_tool.py`
- **Recall facts using fuzzy matching. Returns all if no topic given.** (1 connections) — `app/services/memory_tool.py`
- **memory.md** (1 connections) — `docs/features/memory.md`
- **API** (1 connections) — `docs/features/memory.md`
- **Files & symbols (auto-generated, line numbers are current)** (1 connections) — `docs/features/memory.md`
- **Graphify** (1 connections) — `docs/features/memory.md`

## Relationships

- [tools + window_layout](tools_+_window_layout.md) (4 shared connections)
- [calendar_tool + email-calendar](calendar_tool_+_email-calendar.md) (3 shared connections)
- [llm + context_classifier](llm_+_context_classifier.md) (2 shared connections)
- [memory + tool_runner](memory_+_tool_runner.md) (2 shared connections)
- [jarvis_overlay + prompt_overlay](jarvis_overlay_+_prompt_overlay.md) (1 shared connections)
- [gmail_tool](gmail_tool.md) (1 shared connections)
- [server + persistence](server_+_persistence.md) (1 shared connections)
- [rag_memory + mysql_db](rag_memory_+_mysql_db.md) (1 shared connections)
- [memory + tools](memory_+_tools.md) (1 shared connections)

## Source Files

- `app/services/memory_tool.py`
- `docs/features/memory.md`

## Audit Trail

- EXTRACTED: 43 (80%)
- INFERRED: 11 (20%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*