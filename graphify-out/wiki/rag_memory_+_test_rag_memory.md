# rag_memory + test_rag_memory

> 11 nodes · cohesion 0.24

## Key Concepts

- **init_rag_memory()** (12 connections) — `app/services/rag_memory.py`
- **test_rag_memory.py** (10 connections) — `scripts/test_rag_memory.py`
- **get_memory_stats()** (7 connections) — `app/services/rag_memory.py`
- **test()** (6 connections) — `scripts/test_rag_memory.py`
- **smart_filter()** (5 connections) — `app/services/rag_memory.py`
- **_load_faiss_index()** (3 connections) — `app/services/rag_memory.py`
- **Boot the RAG memory system: 1. Initialize MySQL pool + ensure tables exist 2.…** (1 connections) — `app/services/rag_memory.py`
- **Returns True if the turn is meaningful enough to store. Skips trivial single-…** (1 connections) — `app/services/rag_memory.py`
- **Return statistics about stored long-term memory.** (1 connections) — `app/services/rag_memory.py`
- **Load FAISS index from disk, or create a fresh one.** (1 connections) — `app/services/rag_memory.py`
- **End-to-end test for Jarvis RAG memory system. Tests: init, smart filter,…** (1 connections) — `scripts/test_rag_memory.py`

## Relationships

- [assignment_tool + assignment_humanizer](assignment_tool_+_assignment_humanizer.md) (6 shared connections)
- [chat + rag_memory](chat_+_rag_memory.md) (5 shared connections)
- [mysql_db + init_rag_memory](mysql_db_+_init_rag_memory.md) (4 shared connections)
- [memory + memory](memory_+_memory.md) (3 shared connections)
- [main + screen_vision](main_+_screen_vision.md) (2 shared connections)
- [acoustic_tripwire](acoustic_tripwire.md) (1 shared connections)
- [dump_wa_ui + test_wa](dump_wa_ui_+_test_wa.md) (1 shared connections)

## Source Files

- `app/services/rag_memory.py`
- `scripts/test_rag_memory.py`

## Audit Trail

- EXTRACTED: 33 (94%)
- INFERRED: 2 (6%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*