# memory_tool + email-calendar

> 28 nodes · cohesion 0.11

## Key Concepts

- **memory_tool.py** (16 connections) — `app/services/memory_tool.py`
- **Email, calendar & morning brief** (8 connections) — `docs/features/email-calendar.md`
- **forget_fact()** (7 connections) — `app/services/memory_tool.py`
- **_load_memory()** (7 connections) — `app/services/memory_tool.py`
- **Purpose** (7 connections) — `docs/features/memory.md`
- **get_morning_brief()** (6 connections) — `app/services/memory_tool.py`
- **recall_facts()** (6 connections) — `app/services/memory_tool.py`
- **save_fact()** (6 connections) — `app/services/memory_tool.py`
- **update_fact()** (6 connections) — `app/services/memory_tool.py`
- **get_all_facts_as_context()** (5 connections) — `app/services/memory_tool.py`
- **_save_memory()** (5 connections) — `app/services/memory_tool.py`
- **_fuzzy_match_topics()** (4 connections) — `app/services/memory_tool.py`
- **_ensure_memory_file()** (3 connections) — `app/services/memory_tool.py`
- **Calendar** (2 connections) — `docs/features/email-calendar.md`
- **Morning brief** (2 connections) — `docs/features/email-calendar.md`
- **memory_tool.py — Jarvis Persistent Memory (Step 10 — ENHANCED)…** (1 connections) — `app/services/memory_tool.py`
- **Replace an existing fact with an updated version.** (1 connections) — `app/services/memory_tool.py`
- **Remove all facts under a topic.** (1 connections) — `app/services/memory_tool.py`
- **Returns a compact string of all saved facts for injecting into LLM system…** (1 connections) — `app/services/memory_tool.py`
- **Generates a smart, narrative morning briefing via LLM. Pulls calendar and email…** (1 connections) — `app/services/memory_tool.py`
- **Return topics that fuzzy-match the query. Falls back to substring if rapidfuzz…** (1 connections) — `app/services/memory_tool.py`
- **Save a fact about the user or system to persistent memory with timestamp.** (1 connections) — `app/services/memory_tool.py`
- **Recall facts using fuzzy matching. Returns all if no topic given.** (1 connections) — `app/services/memory_tool.py`
- **email-calendar.md** (1 connections) — `docs/features/email-calendar.md`
- **Files & symbols (auto-generated, line numbers are current)** (1 connections) — `docs/features/email-calendar.md`
- *... and 3 more nodes in this community*

## Relationships

- [tools](tools.md) (6 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (3 shared connections)
- [calendar_tool](calendar_tool.md) (3 shared connections)
- [gmail_tool](gmail_tool.md) (2 shared connections)
- [memory + CLAUDE](memory_+_CLAUDE.md) (2 shared connections)
- [nlp_extractor + download_kokoro](nlp_extractor_+_download_kokoro.md) (1 shared connections)
- [benchmark + server](benchmark_+_server.md) (1 shared connections)
- [chat + tools](chat_+_tools.md) (1 shared connections)

## Source Files

- `app/services/memory_tool.py`
- `docs/features/email-calendar.md`
- `docs/features/memory.md`

## Audit Trail

- EXTRACTED: 48 (79%)
- INFERRED: 13 (21%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*