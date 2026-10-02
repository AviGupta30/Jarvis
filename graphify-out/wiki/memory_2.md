# memory

> 17 nodes · cohesion 0.17

## Key Concepts

- **api/memory.py** (21 connections) — `app/api/memory.py`
- **recall_memory()** (14 connections) — `app/api/memory.py`
- **format_recall_for_prompt()** (10 connections) — `app/services/rag_memory.py`
- **ingest_memory()** (7 connections) — `app/api/memory.py`
- **forget_memory()** (5 connections) — `app/api/memory.py`
- **ForgetRequest** (3 connections) — `app/api/memory.py`
- **IngestRequest** (3 connections) — `app/api/memory.py`
- **BaseModel** (3 connections)
- **RecallRequest** (3 connections) — `app/api/memory.py`
- **Adding / changing a tool (project rules, from JARVIS_ARCHITECTURE.md)** (3 connections) — `CLAUDE.md`
- **post** (2 connections)
- **delete** (1 connections)
- **app/api/memory.py — Jarvis Long-Term Memory API Router…** (1 connections) — `app/api/memory.py`
- **Soft-delete conversation turns that are semantically related to the query.…** (1 connections) — `app/api/memory.py`
- **Ingest a knowledge chunk. Primary store: Postgres/pgvector (DATABASE_URL). If…** (1 connections) — `app/api/memory.py`
- **Semantic search over all stored conversation turns. Returns the most relevant…** (1 connections) — `app/api/memory.py`
- **Format recalled memory turns into an injectable LLM context block with clear…** (1 connections) — `app/services/rag_memory.py`

## Relationships

- [rag_memory](rag_memory.md) (11 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (5 shared connections)
- [tools](tools.md) (3 shared connections)
- [vector_store + database](vector_store_+_database.md) (2 shared connections)
- [memory](memory.md) (2 shared connections)
- [message_reader + reply_generator](message_reader_+_reply_generator.md) (1 shared connections)
- [main](main.md) (1 shared connections)
- [memory + main](memory_+_main.md) (1 shared connections)
- [memory_tool + calendar_tool](memory_tool_+_calendar_tool.md) (1 shared connections)
- [tool-registry](tool-registry.md) (1 shared connections)
- [email-calendar + tools](email-calendar_+_tools.md) (1 shared connections)
- [agentic_web](agentic_web.md) (1 shared connections)

## Source Files

- `CLAUDE.md`
- `app/api/memory.py`
- `app/services/rag_memory.py`

## Audit Trail

- EXTRACTED: 48 (84%)
- INFERRED: 9 (16%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*