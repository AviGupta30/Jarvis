# main

> 12 nodes · cohesion 0.20

## Key Concepts

- **get_engine()** (8 connections) — `app/services/acoustic_tripwire.py`
- **post** (4 connections)
- **tripwire_calibrate()** (4 connections) — `app/main.py`
- **tripwire_disable()** (4 connections) — `app/main.py`
- **tripwire_enable()** (4 connections) — `app/main.py`
- **upload_file()** (4 connections) — `app/main.py`
- **Arm the acoustic tripwire so double-claps wake Jarvis.** (1 connections) — `app/main.py`
- **Disarm the acoustic tripwire (engine keeps running, just paused).** (1 connections) — `app/main.py`
- **Schedule an ambient-noise recalibration pass. The engine samples the mic for ~2…** (1 connections) — `app/main.py`
- **Upload a file to the data/uploads folder for Jarvis to process.** (1 connections) — `app/main.py`
- **Return the module-level singleton engine, creating it if necessary. Thread-…** (1 connections) — `app/services/acoustic_tripwire.py`
- **UploadFile** (1 connections)

## Relationships

- [main + screen_vision](main_+_screen_vision.md) (5 shared connections)
- [main](main.md) (1 shared connections)
- [acoustic_tripwire](acoustic_tripwire.md) (1 shared connections)
- [benchmark + server](benchmark_+_server.md) (1 shared connections)

## Source Files

- `app/main.py`
- `app/services/acoustic_tripwire.py`

## Audit Trail

- EXTRACTED: 21 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*