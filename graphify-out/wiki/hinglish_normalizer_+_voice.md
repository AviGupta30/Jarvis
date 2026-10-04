# hinglish_normalizer + voice

> 15 nodes · cohesion 0.16

## Key Concepts

- **hinglish_normalizer.py** (9 connections) — `app/services/hinglish_normalizer.py`
- **devanagari_to_hinglish()** (7 connections) — `app/services/hinglish_normalizer.py`
- **_finish()** (7 connections) — `app/services/voice.py`
- **loanword_ratio()** (5 connections) — `app/services/hinglish_normalizer.py`
- **Transcript** (5 connections) — `app/services/voice.py`
- **STT (`voice.transcribe_pcm` → `Transcript`)** (4 connections) — `docs/features/voice.md`
- **_translit_dev_word()** (3 connections) — `app/services/hinglish_normalizer.py`
- **.confident()** (3 connections) — `app/services/voice.py`
- **_sub()** (2 connections) — `app/services/hinglish_normalizer.py`
- **_clean_transcript()** (2 connections) — `app/services/voice.py`
- **hinglish_normalizer.py — Devanagari Crash Prevention + Text Normalizer…** (1 connections) — `app/services/hinglish_normalizer.py`
- **One Devanagari word → casual Hinglish roman ("चलाओ" → "chalao", "करना" →…** (1 connections) — `app/services/hinglish_normalizer.py`
- **Share of Devanagari words that are English loanwords ("ओपन क्रोम" → 1.0). High…** (1 connections) — `app/services/hinglish_normalizer.py`
- **Romanize a Devanagari (Hindi) transcript for the backend, keeping any Latin…** (1 connections) — `app/services/hinglish_normalizer.py`
- **Strict check used when there is no wake word to vouch for the audio.** (1 connections) — `app/services/voice.py`

## Relationships

- [voice](voice.md) (13 shared connections)
- [voice + hinglish_normalizer](voice_+_hinglish_normalizer.md) (2 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (2 shared connections)
- [assignment_assembler + smart_navigator](assignment_assembler_+_smart_navigator.md) (1 shared connections)

## Source Files

- `app/services/hinglish_normalizer.py`
- `app/services/voice.py`
- `docs/features/voice.md`

## Audit Trail

- EXTRACTED: 29 (83%)
- INFERRED: 6 (17%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*