# voice

> 15 nodes · cohesion 0.15

## Key Concepts

- **Clip** (11 connections) — `app/services/voice.py`
- **start_clip()** (10 connections) — `app/services/voice.py`
- **_synth_edge()** (6 connections) — `app/services/voice.py`
- **_synthesize()** (5 connections) — `app/services/voice.py`
- **prewarm()** (3 connections) — `app/services/voice.py`
- **_sapi_sync()** (3 connections) — `app/services/voice.py`
- **_voice_for()** (2 connections) — `app/services/voice.py`
- **.cancel()** (1 connections) — `app/services/voice.py`
- **.finish()** (1 connections) — `app/services/voice.py`
- **.__init__()** (1 connections) — `app/services/voice.py`
- **.iter_chunks()** (1 connections) — `app/services/voice.py`
- **PCM (int16, 24 kHz) that fills while synthesis streams; playable immediately.** (1 connections) — `app/services/voice.py`
- **Begin synthesising `text` now; returns a Clip that can be played while it fills.** (1 connections) — `app/services/voice.py`
- **Synthesise short stock phrases (greetings, acks) into the cache for instant…** (1 connections) — `app/services/voice.py`
- **_decode()** (1 connections) — `app/services/voice.py`

## Relationships

- [voice](voice.md) (13 shared connections)
- [voice + test_hindi_tts](voice_+_test_hindi_tts.md) (1 shared connections)
- [hinglish_normalizer](hinglish_normalizer.md) (1 shared connections)
- [voice + context_classifier](voice_+_context_classifier.md) (1 shared connections)

## Source Files

- `app/services/voice.py`

## Audit Trail

- EXTRACTED: 30 (94%)
- INFERRED: 2 (6%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*