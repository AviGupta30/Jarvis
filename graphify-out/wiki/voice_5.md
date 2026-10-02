# voice

> 10 nodes · cohesion 0.27

## Key Concepts

- **_Player** (12 connections) — `app/services/voice.py`
- **.play()** (6 connections) — `app/services/voice.py`
- **._push()** (3 connections) — `app/services/voice.py`
- **.clear()** (2 connections) — `app/services/voice.py`
- **._ensure()** (2 connections) — `app/services/voice.py`
- **._callback()** (1 connections) — `app/services/voice.py`
- **.__init__()** (1 connections) — `app/services/voice.py`
- **.pending()** (1 connections) — `app/services/voice.py`
- **One persistent 24 kHz output stream driven by a callback that pulls from a…** (1 connections) — `app/services/voice.py`
- **Play a clip as it arrives. Returns False if interrupted.** (1 connections) — `app/services/voice.py`

## Relationships

- [voice](voice.md) (4 shared connections)
- [voice + test_hindi_tts](voice_+_test_hindi_tts.md) (1 shared connections)
- [voice + context_classifier](voice_+_context_classifier.md) (1 shared connections)

## Source Files

- `app/services/voice.py`

## Audit Trail

- EXTRACTED: 17 (94%)
- INFERRED: 1 (6%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*