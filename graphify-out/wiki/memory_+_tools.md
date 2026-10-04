# memory + tools

> 22 nodes · cohesion 0.13

## Key Concepts

- **memory/memory.py** (14 connections) — `app/memory/memory.py`
- **memory/__init__.py** (7 connections) — `app/memory/__init__.py`
- **format_preferences_for_prompt()** (6 connections) — `app/memory/memory.py`
- **save_preference()** (6 connections) — `app/memory/memory.py`
- **save_skill()** (6 connections) — `app/memory/memory.py`
- **list_skills()** (5 connections) — `app/memory/memory.py`
- **remember_preference()** (5 connections) — `app/services/tools.py`
- **get_all_preferences()** (4 connections) — `app/memory/memory.py`
- **_uid()** (4 connections) — `app/memory/memory.py`
- **list_learned_skills()** (4 connections) — `app/services/tools.py`
- **hashlib** (4 connections)
- **Jarvis Vector Memory — ChromaDB-based long-term memory engine. Stores and…** (1 connections) — `app/memory/memory.py`
- **Returns a string suitable for injecting into LLM prompts.** (1 connections) — `app/memory/memory.py`
- **Stable short ID based on content hash.** (1 connections) — `app/memory/memory.py`
- **Persist a successful dynamic skill for future reuse.** (1 connections) — `app/memory/memory.py`
- **List all saved skill descriptions.** (1 connections) — `app/memory/memory.py`
- **Store a user preference (e.g. key='browser', value='Chrome').** (1 connections) — `app/memory/memory.py`
- **Return all stored preferences as a plain dict.** (1 connections) — `app/memory/memory.py`
- **Save a user preference to long-term memory.** (1 connections) — `app/services/tools.py`
- **Return all dynamic skills Jarvis has learned.** (1 connections) — `app/services/tools.py`
- **chromadb** (1 connections)
- **chromadb_config** (1 connections)

## Relationships

- [tools + window_layout](tools_+_window_layout.md) (6 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (4 shared connections)
- [jarvis_overlay + prompt_overlay](jarvis_overlay_+_prompt_overlay.md) (2 shared connections)
- [chat](chat.md) (1 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (1 shared connections)
- [memory_tool + memory](memory_tool_+_memory.md) (1 shared connections)
- [ppt_designer](ppt_designer.md) (1 shared connections)
- [rag_memory + mysql_db](rag_memory_+_mysql_db.md) (1 shared connections)
- [resume_builder](resume_builder.md) (1 shared connections)

## Source Files

- `app/memory/__init__.py`
- `app/memory/memory.py`
- `app/services/tools.py`

## Audit Trail

- EXTRACTED: 42 (89%)
- INFERRED: 5 (11%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*