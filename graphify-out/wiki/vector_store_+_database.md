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

- [chat + youtube_control](chat_+_youtube_control.md) (4 shared connections)
- [memory](memory.md) (2 shared connections)
- [dynamic_skill + planner](dynamic_skill_+_planner.md) (1 shared connections)

## Source Files

- `app/core/database.py`
- `app/services/vector_store.py`

## Audit Trail

- EXTRACTED: 18 (95%)
- INFERRED: 1 (5%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*