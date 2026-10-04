# voice

> 13 nodes · cohesion 0.15

## Key Concepts

- **Clip** (11 connections) — `app/services/voice.py`
- **start_clip()** (10 connections) — `app/services/voice.py`
- **route_language()** (4 connections) — `app/services/voice.py`
- **prewarm()** (3 connections) — `app/services/voice.py`
- **.push()** (2 connections) — `app/services/voice.py`
- **.cancel()** (1 connections) — `app/services/voice.py`
- **.finish()** (1 connections) — `app/services/voice.py`
- **.__init__()** (1 connections) — `app/services/voice.py`
- **.iter_chunks()** (1 connections) — `app/services/voice.py`
- **PCM (int16, 24 kHz) that fills while synthesis streams; playable immediately.** (1 connections) — `app/services/voice.py`
- **hi' → Hindi voice, 'en' → English voice, for one sentence.** (1 connections) — `app/services/voice.py`
- **Begin synthesising `text` now; returns a Clip that can be played while it fills.** (1 connections) — `app/services/voice.py`
- **Synthesise short stock phrases (greetings, acks) into the cache for instant…** (1 connections) — `app/services/voice.py`

## Relationships

- [voice](voice.md) (11 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (1 shared connections)
- [voice + tools](voice_+_tools.md) (1 shared connections)
- [hinglish_normalizer](hinglish_normalizer.md) (1 shared connections)

## Source Files

- `app/services/voice.py`

## Audit Trail

- EXTRACTED: 25 (96%)
- INFERRED: 1 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*