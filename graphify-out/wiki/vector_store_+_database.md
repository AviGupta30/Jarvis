# vector_store + database

> 9 nodes · cohesion 0.33

## Key Concepts

- **database.py** (5 connections) — `app/core/database.py`
- **get_db_pool()** (5 connections) — `app/core/database.py`
- **vector_store.py** (5 connections) — `app/services/vector_store.py`
- **save_document_chunk()** (5 connections) — `app/services/vector_store.py`
- **search_similar_chunks()** (5 connections) — `app/services/vector_store.py`
- **init_db()** (3 connections) — `app/core/database.py`
- **Queries the table and uses the pgvector cosine distance operator (<=>) to fetch…** (1 connections) — `app/services/vector_store.py`
- **Inserts text chunks and vectors into the knowledge_store table.** (1 connections) — `app/services/vector_store.py`
- **asyncpg** (1 connections)

## Relationships

- [chat](chat.md) (3 shared connections)
- [rag_memory + memory](rag_memory_+_memory.md) (2 shared connections)
- [assignment_tool + safe_executor](assignment_tool_+_safe_executor.md) (1 shared connections)
- [youtube_control](youtube_control.md) (1 shared connections)

## Source Files

- `app/core/database.py`
- `app/services/vector_store.py`

## Audit Trail

- EXTRACTED: 18 (95%)
- INFERRED: 1 (5%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*