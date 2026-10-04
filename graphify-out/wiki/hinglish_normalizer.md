# hinglish_normalizer

> 10 nodes · cohesion 0.22

## Key Concepts

- **hinglish_normalizer.py** (9 connections) — `app/services/hinglish_normalizer.py`
- **strip_markdown()** (6 connections) — `app/services/hinglish_normalizer.py`
- **normalize_for_tts()** (4 connections) — `app/services/hinglish_normalizer.py`
- **_translit_dev_word()** (3 connections) — `app/services/hinglish_normalizer.py`
- **_sub()** (2 connections) — `app/services/hinglish_normalizer.py`
- **.say()** (2 connections) — `app/services/voice.py`
- **hinglish_normalizer.py — Devanagari Crash Prevention + Text Normalizer…** (1 connections) — `app/services/hinglish_normalizer.py`
- **One Devanagari word → casual Hinglish roman ("चलाओ" → "chalao", "करना" →…** (1 connections) — `app/services/hinglish_normalizer.py`
- **Transform text so it's safe and natural-sounding for TTS: 1. Replace known…** (1 connections) — `app/services/hinglish_normalizer.py`
- **Markdown → plain speakable text (keeps Devanagari). Also drops URLs and emoji.** (1 connections) — `app/services/hinglish_normalizer.py`

## Relationships

- [voice](voice.md) (9 shared connections)
- [voice_agent + download_kokoro](voice_agent_+_download_kokoro.md) (1 shared connections)

## Source Files

- `app/services/hinglish_normalizer.py`
- `app/services/voice.py`

## Audit Trail

- EXTRACTED: 19 (95%)
- INFERRED: 1 (5%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*