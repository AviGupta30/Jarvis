# tool-registry + vector_store

> 28 nodes · cohesion 0.09

## Key Concepts

- **Fixed on 2026-09-28** (16 connections) — `docs/KNOWN_ISSUES.md`
- **recall_memory()** (14 connections) — `app/api/memory.py`
- **_media_target()** (9 connections) — `app/api/chat.py`
- **Gotchas** (7 connections) — `docs/features/tool-registry.md`
- **Tool registry & adding tools** (7 connections) — `docs/features/tool-registry.md`
- **spotify_running()** (6 connections) — `app/services/media_state.py`
- **_mail_tool()** (6 connections) — `app/services/tools.py`
- **database.py** (5 connections) — `app/core/database.py`
- **get_db_pool()** (5 connections) — `app/core/database.py`
- **vector_store.py** (5 connections) — `app/services/vector_store.py`
- **save_document_chunk()** (5 connections) — `app/services/vector_store.py`
- **search_similar_chunks()** (5 connections) — `app/services/vector_store.py`
- **init_db()** (3 connections) — `app/core/database.py`
- **Calling tools from code** (3 connections) — `docs/features/tool-registry.md`
- **post** (2 connections)
- **Email** (2 connections) — `docs/features/email-calendar.md`
- **Adding a tool (checklist)** (2 connections) — `docs/features/tool-registry.md`
- **Which player an ambiguous media command ("pause it", "next song") is for: named…** (1 connections) — `app/api/chat.py`
- **Semantic search over all stored conversation turns. Returns the most relevant…** (1 connections) — `app/api/memory.py`
- **True if the Spotify desktop app has a window (cheap: EnumWindows, no UIA).** (1 connections) — `app/services/media_state.py`
- **Email tools: try the real Gmail API (gmail_tool) first, fall back to opening…** (1 connections) — `app/services/tools.py`
- **Queries the table and uses the pgvector cosine distance operator (<=>) to fetch…** (1 connections) — `app/services/vector_store.py`
- **Inserts text chunks and vectors into the knowledge_store table.** (1 connections) — `app/services/vector_store.py`
- **asyncpg** (1 connections)
- **tool-registry.md** (1 connections) — `docs/features/tool-registry.md`
- *... and 3 more nodes in this community*

## Relationships

- [planner + dynamic_skill](planner_+_dynamic_skill.md) (6 shared connections)
- [rag_memory + memory](rag_memory_+_memory.md) (6 shared connections)
- [chat-routing + chat](chat-routing_+_chat.md) (4 shared connections)
- [tools](tools.md) (4 shared connections)
- [gmail_tool + memory_tool](gmail_tool_+_memory_tool.md) (3 shared connections)
- [chat + llm](chat_+_llm.md) (3 shared connections)
- [youtube_control](youtube_control.md) (2 shared connections)
- [dag_executor](dag_executor.md) (2 shared connections)
- [youtube_player](youtube_player.md) (2 shared connections)
- [agentic_web](agentic_web.md) (2 shared connections)
- [assignment_tool + assignment_pipeline](assignment_tool_+_assignment_pipeline.md) (2 shared connections)
- [ppt_router + ppt_tool](ppt_router_+_ppt_tool.md) (2 shared connections)

## Source Files

- `app/api/chat.py`
- `app/api/memory.py`
- `app/core/database.py`
- `app/services/media_state.py`
- `app/services/tools.py`
- `app/services/vector_store.py`
- `docs/KNOWN_ISSUES.md`
- `docs/features/email-calendar.md`
- `docs/features/tool-registry.md`

## Audit Trail

- EXTRACTED: 47 (59%)
- INFERRED: 33 (41%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*