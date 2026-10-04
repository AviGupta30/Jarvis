# acoustic_tripwire

> 44 nodes · cohesion 0.05

## Key Concepts

- **AcousticWakeEngine** (16 connections) — `app/services/acoustic_tripwire.py`
- **Architecture** (8 connections) — `docs/ARCHITECTURE.md`
- **._run()** (7 connections) — `app/services/acoustic_tripwire.py`
- **._is_clap()** (6 connections) — `app/services/acoustic_tripwire.py`
- **._rms()** (6 connections) — `app/services/acoustic_tripwire.py`
- **._dominant_freq()** (5 connections) — `app/services/acoustic_tripwire.py`
- **.process_chunk()** (5 connections) — `app/services/acoustic_tripwire.py`
- **_play_chime()** (4 connections) — `app/services/acoustic_tripwire.py`
- **ndarray** (4 connections)
- **calibrate_tripwire()** (3 connections) — `app/services/acoustic_tripwire.py`
- **_generate_chime()** (3 connections) — `app/services/acoustic_tripwire.py`
- **get_wake_event()** (3 connections) — `app/services/acoustic_tripwire.py`
- **Voice path (`scripts/voice_agent.py`)** (3 connections) — `docs/ARCHITECTURE.md`
- **.disable()** (2 connections) — `app/services/acoustic_tripwire.py`
- **.enable()** (2 connections) — `app/services/acoustic_tripwire.py`
- **.get_status()** (2 connections) — `app/services/acoustic_tripwire.py`
- **.__init__()** (2 connections) — `app/services/acoustic_tripwire.py`
- **.recalibrate()** (2 connections) — `app/services/acoustic_tripwire.py`
- **.set_volume_threshold()** (2 connections) — `app/services/acoustic_tripwire.py`
- **.start()** (2 connections) — `app/services/acoustic_tripwire.py`
- **.stop()** (2 connections) — `app/services/acoustic_tripwire.py`
- **HTTP endpoints** (2 connections) — `docs/ARCHITECTURE.md`
- **Event** (2 connections)
- **Background thread that watches the microphone for a double-clap pattern. Usage…** (1 connections) — `app/services/acoustic_tripwire.py`
- **Start the background listening thread.** (1 connections) — `app/services/acoustic_tripwire.py`
- *... and 19 more nodes in this community*

## Relationships

- [benchmark + server](benchmark_+_server.md) (5 shared connections)
- [main](main.md) (1 shared connections)
- [chat + chat-routing](chat_+_chat-routing.md) (1 shared connections)
- [frontend](frontend.md) (1 shared connections)
- [rag_memory + mysql_db](rag_memory_+_mysql_db.md) (1 shared connections)
- [voice](voice.md) (1 shared connections)

## Source Files

- `app/services/acoustic_tripwire.py`
- `docs/ARCHITECTURE.md`

## Audit Trail

- EXTRACTED: 57 (92%)
- INFERRED: 5 (8%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*