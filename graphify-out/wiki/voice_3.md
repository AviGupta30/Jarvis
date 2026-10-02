# voice

> 14 nodes · cohesion 0.18

## Key Concepts

- **_Player** (12 connections) — `app/services/voice.py`
- **.play()** (6 connections) — `app/services/voice.py`
- **get_player()** (4 connections) — `app/services/voice.py`
- **.output_level()** (3 connections) — `app/services/voice.py`
- **._push()** (3 connections) — `app/services/voice.py`
- **.clear()** (2 connections) — `app/services/voice.py`
- **._ensure()** (2 connections) — `app/services/voice.py`
- **.__init__()** (2 connections) — `app/services/voice.py`
- **._callback()** (1 connections) — `app/services/voice.py`
- **.__init__()** (1 connections) — `app/services/voice.py`
- **.pending()** (1 connections) — `app/services/voice.py`
- **One persistent 24 kHz output stream driven by a callback that pulls from a…** (1 connections) — `app/services/voice.py`
- **Loudest output RMS in the last `window` s — the voice agent's echo reference.** (1 connections) — `app/services/voice.py`
- **Play a clip as it arrives. Returns False if interrupted.** (1 connections) — `app/services/voice.py`

## Relationships

- [voice](voice.md) (6 shared connections)
- [voice + tools](voice_+_tools.md) (1 shared connections)
- [voice_agent](voice_agent.md) (1 shared connections)

## Source Files

- `app/services/voice.py`

## Audit Trail

- EXTRACTED: 22 (92%)
- INFERRED: 2 (8%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*