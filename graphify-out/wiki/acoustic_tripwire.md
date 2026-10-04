# acoustic_tripwire

> 16 nodes · cohesion 0.12

## Key Concepts

- **AcousticWakeEngine** (16 connections) — `app/services/acoustic_tripwire.py`
- **.disable()** (2 connections) — `app/services/acoustic_tripwire.py`
- **.enable()** (2 connections) — `app/services/acoustic_tripwire.py`
- **.get_status()** (2 connections) — `app/services/acoustic_tripwire.py`
- **.recalibrate()** (2 connections) — `app/services/acoustic_tripwire.py`
- **.set_volume_threshold()** (2 connections) — `app/services/acoustic_tripwire.py`
- **.start()** (2 connections) — `app/services/acoustic_tripwire.py`
- **.stop()** (2 connections) — `app/services/acoustic_tripwire.py`
- **Background thread that watches the microphone for a double-clap pattern. Usage…** (1 connections) — `app/services/acoustic_tripwire.py`
- **Start the background listening thread.** (1 connections) — `app/services/acoustic_tripwire.py`
- **Signal the background thread to exit and wait for it.** (1 connections) — `app/services/acoustic_tripwire.py`
- **Resume detection after a disable().** (1 connections) — `app/services/acoustic_tripwire.py`
- **Pause detection without stopping the thread (fast resume).** (1 connections) — `app/services/acoustic_tripwire.py`
- **Signal the background thread to re-run calibration on the next cycle. Returns…** (1 connections) — `app/services/acoustic_tripwire.py`
- **Override the volume threshold (used by voice_agent inline mode).** (1 connections) — `app/services/acoustic_tripwire.py`
- **Return a JSON-serialisable status dict for the /tripwire/status endpoint.** (1 connections) — `app/services/acoustic_tripwire.py`

## Relationships

- [acoustic_tripwire](acoustic_tripwire.md) (6 shared connections)
- [main](main.md) (1 shared connections)
- [ARCHITECTURE](ARCHITECTURE.md) (1 shared connections)

## Source Files

- `app/services/acoustic_tripwire.py`

## Audit Trail

- EXTRACTED: 23 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*