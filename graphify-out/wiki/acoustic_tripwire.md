# acoustic_tripwire

> 13 nodes · cohesion 0.21

## Key Concepts

- **._run()** (7 connections) — `app/services/acoustic_tripwire.py`
- **._is_clap()** (6 connections) — `app/services/acoustic_tripwire.py`
- **._rms()** (6 connections) — `app/services/acoustic_tripwire.py`
- **._dominant_freq()** (5 connections) — `app/services/acoustic_tripwire.py`
- **ndarray** (4 connections)
- **calibrate_tripwire()** (3 connections) — `app/services/acoustic_tripwire.py`
- **_generate_chime()** (3 connections) — `app/services/acoustic_tripwire.py`
- **Root Mean Square amplitude. Cast to float64 to prevent int16 overflow.** (1 connections) — `app/services/acoustic_tripwire.py`
- **FFT-based dominant frequency. Only inspect the positive half-spectrum (0 ……** (1 connections) — `app/services/acoustic_tripwire.py`
- **Return True if this chunk looks like a clap/snap (loud + right frequency).** (1 connections) — `app/services/acoustic_tripwire.py`
- **Main loop — opened inside the thread so PyAudio errors stay contained. State…** (1 connections) — `app/services/acoustic_tripwire.py`
- **Generate a pleasant two-tone wake chime as a float32 numpy array.** (1 connections) — `app/services/acoustic_tripwire.py`
- **Sample ambient noise for `sample_seconds`, calculate the mean RMS, then set…** (1 connections) — `app/services/acoustic_tripwire.py`

## Relationships

- [acoustic_tripwire](acoustic_tripwire.md) (4 shared connections)
- [ARCHITECTURE + acoustic_tripwire](ARCHITECTURE_+_acoustic_tripwire.md) (2 shared connections)
- [voice_agent + acoustic_tripwire](voice_agent_+_acoustic_tripwire.md) (2 shared connections)

## Source Files

- `app/services/acoustic_tripwire.py`

## Audit Trail

- EXTRACTED: 23 (96%)
- INFERRED: 1 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*