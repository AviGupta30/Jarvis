# acoustic_tripwire

> 38 nodes · cohesion 0.07

## Key Concepts

- **AcousticWakeEngine** (16 connections) — `app/services/acoustic_tripwire.py`
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
- **Event** (2 connections)
- **Background thread that watches the microphone for a double-clap pattern. Usage…** (1 connections) — `app/services/acoustic_tripwire.py`
- **Start the background listening thread.** (1 connections) — `app/services/acoustic_tripwire.py`
- **Signal the background thread to exit and wait for it.** (1 connections) — `app/services/acoustic_tripwire.py`
- **Resume detection after a disable().** (1 connections) — `app/services/acoustic_tripwire.py`
- *... and 13 more nodes in this community*

## Relationships

- [server + persistence](server_+_persistence.md) (5 shared connections)
- [main](main.md) (1 shared connections)
- [llm-personality + ARCHITECTURE](llm-personality_+_ARCHITECTURE.md) (1 shared connections)
- [voice](voice.md) (1 shared connections)

## Source Files

- `app/services/acoustic_tripwire.py`
- `docs/ARCHITECTURE.md`

## Audit Trail

- EXTRACTED: 50 (93%)
- INFERRED: 4 (7%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*