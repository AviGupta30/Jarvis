# hinglish_normalizer

> 13 nodes · cohesion 0.18

## Key Concepts

- **hinglish_normalizer.py** (9 connections) — `app/services/hinglish_normalizer.py`
- **devanagari_to_hinglish()** (7 connections) — `app/services/hinglish_normalizer.py`
- **strip_markdown()** (6 connections) — `app/services/hinglish_normalizer.py`
- **normalize_for_tts()** (4 connections) — `app/services/hinglish_normalizer.py`
- **STT (`voice.transcribe_pcm` → `Transcript`)** (4 connections) — `docs/features/voice.md`
- **_translit_dev_word()** (3 connections) — `app/services/hinglish_normalizer.py`
- **_sub()** (2 connections) — `app/services/hinglish_normalizer.py`
- **.say()** (2 connections) — `app/services/voice.py`
- **hinglish_normalizer.py — Devanagari Crash Prevention + Text Normalizer…** (1 connections) — `app/services/hinglish_normalizer.py`
- **One Devanagari word → casual Hinglish roman ("चलाओ" → "chalao", "करना" →…** (1 connections) — `app/services/hinglish_normalizer.py`
- **Romanize a Devanagari (Hindi) transcript for the backend, keeping any Latin…** (1 connections) — `app/services/hinglish_normalizer.py`
- **Transform text so it's safe and natural-sounding for TTS: 1. Replace known…** (1 connections) — `app/services/hinglish_normalizer.py`
- **Markdown → plain speakable text (keeps Devanagari). Also drops URLs and emoji.** (1 connections) — `app/services/hinglish_normalizer.py`

## Relationships

- [voice](voice.md) (12 shared connections)
- [assignment_assembler + smart_navigator](assignment_assembler_+_smart_navigator.md) (1 shared connections)
- [voice + tools](voice_+_tools.md) (1 shared connections)

## Source Files

- `app/services/hinglish_normalizer.py`
- `app/services/voice.py`
- `docs/features/voice.md`

## Audit Trail

- EXTRACTED: 24 (86%)
- INFERRED: 4 (14%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*