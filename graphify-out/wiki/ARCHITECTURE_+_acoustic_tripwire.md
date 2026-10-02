# ARCHITECTURE + acoustic_tripwire

> 11 nodes · cohesion 0.18

## Key Concepts

- **Architecture** (8 connections) — `docs/ARCHITECTURE.md`
- **.process_chunk()** (5 connections) — `app/services/acoustic_tripwire.py`
- **_play_chime()** (4 connections) — `app/services/acoustic_tripwire.py`
- **Voice path (`scripts/voice_agent.py`)** (3 connections) — `docs/ARCHITECTURE.md`
- **HTTP endpoints** (2 connections) — `docs/ARCHITECTURE.md`
- **Inline (shared-stream) mode — called by voice_agent.py on every audio frame it…** (1 connections) — `app/services/acoustic_tripwire.py`
- **Play the wake chime via sounddevice (non-blocking from caller's perspective).** (1 connections) — `app/services/acoustic_tripwire.py`
- **ARCHITECTURE.md** (1 connections) — `docs/ARCHITECTURE.md`
- **LLM usage** (1 connections) — `docs/ARCHITECTURE.md`
- **Memory layers (five separate stores)** (1 connections) — `docs/ARCHITECTURE.md`
- **Processes** (1 connections) — `docs/ARCHITECTURE.md`

## Relationships

- [acoustic_tripwire](acoustic_tripwire.md) (3 shared connections)
- [voice_agent + acoustic_tripwire](voice_agent_+_acoustic_tripwire.md) (1 shared connections)
- [dag_executor + planner](dag_executor_+_planner.md) (1 shared connections)
- [frontend](frontend.md) (1 shared connections)
- [mysql_db + rag_memory](mysql_db_+_rag_memory.md) (1 shared connections)
- [voice](voice.md) (1 shared connections)

## Source Files

- `app/services/acoustic_tripwire.py`
- `docs/ARCHITECTURE.md`

## Audit Trail

- EXTRACTED: 13 (72%)
- INFERRED: 5 (28%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*