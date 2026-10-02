# memory_tool

> 18 nodes · cohesion 0.21

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
- **_fuzzy_match_topics()** (4 connections) — `app/services/memory_tool.py`
- **_ensure_memory_file()** (3 connections) — `app/services/memory_tool.py`
- **memory_tool.py — Jarvis Persistent Memory (Step 10 — ENHANCED)…** (1 connections) — `app/services/memory_tool.py`
- **Replace an existing fact with an updated version.** (1 connections) — `app/services/memory_tool.py`
- **Remove all facts under a topic.** (1 connections) — `app/services/memory_tool.py`
- **Returns a compact string of all saved facts for injecting into LLM system…** (1 connections) — `app/services/memory_tool.py`
- **Return topics that fuzzy-match the query. Falls back to substring if rapidfuzz…** (1 connections) — `app/services/memory_tool.py`
- **Save a fact about the user or system to persistent memory with timestamp.** (1 connections) — `app/services/memory_tool.py`
- **Recall facts using fuzzy matching. Returns all if no topic given.** (1 connections) — `app/services/memory_tool.py`

## Relationships

- [tools](tools.md) (5 shared connections)
- [calendar_tool](calendar_tool.md) (3 shared connections)
- [assignment_tool + assignment_humanizer](assignment_tool_+_assignment_humanizer.md) (2 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (2 shared connections)
- [memory + memory](memory_+_memory.md) (2 shared connections)
- [gmail_tool + download_kokoro](gmail_tool_+_download_kokoro.md) (1 shared connections)

## Source Files

- `app/services/memory_tool.py`
- `docs/features/memory.md`

## Audit Trail

- EXTRACTED: 37 (79%)
- INFERRED: 10 (21%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*