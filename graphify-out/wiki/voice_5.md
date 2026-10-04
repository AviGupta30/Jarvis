# voice

> 12 nodes · cohesion 0.21

## Key Concepts

- **_Player** (12 connections) — `app/services/voice.py`
- **.play()** (6 connections) — `app/services/voice.py`
- **.output_level()** (3 connections) — `app/services/voice.py`
- **._push()** (3 connections) — `app/services/voice.py`
- **.clear()** (2 connections) — `app/services/voice.py`
- **._ensure()** (2 connections) — `app/services/voice.py`
- **._callback()** (1 connections) — `app/services/voice.py`
- **.__init__()** (1 connections) — `app/services/voice.py`
- **.pending()** (1 connections) — `app/services/voice.py`
- **One persistent 24 kHz output stream driven by a callback that pulls from a…** (1 connections) — `app/services/voice.py`
- **Loudest output RMS in the last `window` s — the voice agent's echo reference.** (1 connections) — `app/services/voice.py`
- **Play a clip as it arrives. Returns False if interrupted.** (1 connections) — `app/services/voice.py`

## Relationships

- [voice](voice.md) (5 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (1 shared connections)

## Source Files

- `app/services/voice.py`

## Audit Trail

- EXTRACTED: 18 (90%)
- INFERRED: 2 (10%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*