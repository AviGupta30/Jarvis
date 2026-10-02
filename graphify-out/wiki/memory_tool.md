# memory_tool

> 20 nodes · cohesion 0.18

## Key Concepts

- **memory_tool.py** (16 connections) — `app/services/memory_tool.py`
- **forget_fact()** (7 connections) — `app/services/memory_tool.py`
- **_load_memory()** (7 connections) — `app/services/memory_tool.py`
- **Purpose** (7 connections) — `docs/features/memory.md`
- **recall_facts()** (6 connections) — `app/services/memory_tool.py`
- **save_fact()** (6 connections) — `app/services/memory_tool.py`
- **update_fact()** (6 connections) — `app/services/memory_tool.py`
- **get_all_facts_as_context()** (5 connections) — `app/services/memory_tool.py`
- **_save_memory()** (5 connections) — `app/services/memory_tool.py`
- **remember_preference()** (5 connections) — `app/services/tools.py`
- **_fuzzy_match_topics()** (4 connections) — `app/services/memory_tool.py`
- **_ensure_memory_file()** (3 connections) — `app/services/memory_tool.py`
- **memory_tool.py — Jarvis Persistent Memory (Step 10 — ENHANCED)…** (1 connections) — `app/services/memory_tool.py`
- **Replace an existing fact with an updated version.** (1 connections) — `app/services/memory_tool.py`
- **Remove all facts under a topic.** (1 connections) — `app/services/memory_tool.py`
- **Returns a compact string of all saved facts for injecting into LLM system…** (1 connections) — `app/services/memory_tool.py`
- **Return topics that fuzzy-match the query. Falls back to substring if rapidfuzz…** (1 connections) — `app/services/memory_tool.py`
- **Save a fact about the user or system to persistent memory with timestamp.** (1 connections) — `app/services/memory_tool.py`
- **Recall facts using fuzzy matching. Returns all if no topic given.** (1 connections) — `app/services/memory_tool.py`
- **Save a user preference to long-term memory.** (1 connections) — `app/services/tools.py`

## Relationships

- [tools](tools.md) (6 shared connections)
- [calendar_tool + email-calendar](calendar_tool_+_email-calendar.md) (3 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (2 shared connections)
- [rag_memory + memory](rag_memory_+_memory.md) (2 shared connections)
- [task_ledger + test_task_resumption](task_ledger_+_test_task_resumption.md) (1 shared connections)
- [gmail_tool](gmail_tool.md) (1 shared connections)
- [assignment_tool](assignment_tool.md) (1 shared connections)
- [memory](memory.md) (1 shared connections)

## Source Files

- `app/services/memory_tool.py`
- `app/services/tools.py`
- `docs/features/memory.md`

## Audit Trail

- EXTRACTED: 39 (76%)
- INFERRED: 12 (24%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*