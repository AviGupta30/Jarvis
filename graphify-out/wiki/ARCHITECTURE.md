# ARCHITECTURE

> 9 nodes · cohesion 0.22

## Key Concepts

- **Architecture** (8 connections) — `docs/ARCHITECTURE.md`
- **.process_chunk()** (5 connections) — `app/services/acoustic_tripwire.py`
- **Voice path (`scripts/voice_agent.py`)** (3 connections) — `docs/ARCHITECTURE.md`
- **HTTP endpoints** (2 connections) — `docs/ARCHITECTURE.md`
- **Inline (shared-stream) mode — called by voice_agent.py on every audio frame it…** (1 connections) — `app/services/acoustic_tripwire.py`
- **ARCHITECTURE.md** (1 connections) — `docs/ARCHITECTURE.md`
- **LLM usage** (1 connections) — `docs/ARCHITECTURE.md`
- **Memory layers (five separate stores)** (1 connections) — `docs/ARCHITECTURE.md`
- **Processes** (1 connections) — `docs/ARCHITECTURE.md`

## Relationships

- [acoustic_tripwire](acoustic_tripwire.md) (3 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (1 shared connections)
- [frontend](frontend.md) (1 shared connections)
- [mysql_db + rag_memory](mysql_db_+_rag_memory.md) (1 shared connections)
- [voice](voice.md) (1 shared connections)

## Source Files

- `app/services/acoustic_tripwire.py`
- `docs/ARCHITECTURE.md`

## Audit Trail

- EXTRACTED: 11 (73%)
- INFERRED: 4 (27%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*