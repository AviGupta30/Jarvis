# voice + hinglish_normalizer

> 11 nodes · cohesion 0.18

## Key Concepts

- **Channel** (8 connections) — `app/services/voice.py`
- **strip_markdown()** (6 connections) — `app/services/hinglish_normalizer.py`
- **normalize_for_tts()** (4 connections) — `app/services/hinglish_normalizer.py`
- **.say()** (2 connections) — `app/services/voice.py`
- **.channel()** (2 connections) — `app/services/voice.py`
- **Transform text so it's safe and natural-sounding for TTS: 1. Replace known…** (1 connections) — `app/services/hinglish_normalizer.py`
- **Markdown → plain speakable text (keeps Devanagari). Also drops URLs and emoji.** (1 connections) — `app/services/hinglish_normalizer.py`
- **.close()** (1 connections) — `app/services/voice.py`
- **.__init__()** (1 connections) — `app/services/voice.py`
- **.mute()** (1 connections) — `app/services/voice.py`
- **The speech stream of one command's reply.** (1 connections) — `app/services/voice.py`

## Relationships

- [voice](voice.md) (6 shared connections)
- [hinglish_normalizer + voice](hinglish_normalizer_+_voice.md) (2 shared connections)

## Source Files

- `app/services/hinglish_normalizer.py`
- `app/services/voice.py`

## Audit Trail

- EXTRACTED: 18 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*