# ARCHITECTURE

> 10 nodes · cohesion 0.20

## Key Concepts

- **Architecture** (8 connections) — `docs/ARCHITECTURE.md`
- **.process_chunk()** (5 connections) — `app/services/acoustic_tripwire.py`
- **Voice path (`scripts/voice_agent.py`)** (3 connections) — `docs/ARCHITECTURE.md`
- **Frontend (`frontend/src`)** (2 connections) — `docs/ARCHITECTURE.md`
- **HTTP endpoints** (2 connections) — `docs/ARCHITECTURE.md`
- **Inline (shared-stream) mode — called by voice_agent.py on every audio frame it…** (1 connections) — `app/services/acoustic_tripwire.py`
- **ARCHITECTURE.md** (1 connections) — `docs/ARCHITECTURE.md`
- **LLM usage** (1 connections) — `docs/ARCHITECTURE.md`
- **Memory layers (five separate stores)** (1 connections) — `docs/ARCHITECTURE.md`
- **Processes** (1 connections) — `docs/ARCHITECTURE.md`

## Relationships

- [acoustic_tripwire](acoustic_tripwire.md) (3 shared connections)
- [dag_executor](dag_executor.md) (1 shared connections)
- [frontend + DagPlanPanel](frontend_+_DagPlanPanel.md) (1 shared connections)
- [rag_memory + memory](rag_memory_+_memory.md) (1 shared connections)
- [voice](voice.md) (1 shared connections)

## Source Files

- `app/services/acoustic_tripwire.py`
- `docs/ARCHITECTURE.md`

## Audit Trail

- EXTRACTED: 11 (69%)
- INFERRED: 5 (31%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*