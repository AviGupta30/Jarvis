# hinglish_normalizer + voice

> 28 nodes · cohesion 0.08

## Key Concepts

- **Voice: STT, TTS, wake word, clap wake, overlay** (12 connections) — `docs/features/voice.md`
- **hinglish_normalizer.py** (9 connections) — `app/services/hinglish_normalizer.py`
- **devanagari_to_hinglish()** (7 connections) — `app/services/hinglish_normalizer.py`
- **_finish()** (7 connections) — `app/services/voice.py`
- **strip_markdown()** (6 connections) — `app/services/hinglish_normalizer.py`
- **loanword_ratio()** (5 connections) — `app/services/hinglish_normalizer.py`
- **Transcript** (5 connections) — `app/services/voice.py`
- **normalize_for_tts()** (4 connections) — `app/services/hinglish_normalizer.py`
- **STT (`voice.transcribe_pcm` → `Transcript`)** (4 connections) — `docs/features/voice.md`
- **_translit_dev_word()** (3 connections) — `app/services/hinglish_normalizer.py`
- **.confident()** (3 connections) — `app/services/voice.py`
- **_sub()** (2 connections) — `app/services/hinglish_normalizer.py`
- **.say()** (2 connections) — `app/services/voice.py`
- **_clean_transcript()** (2 connections) — `app/services/voice.py`
- **hinglish_normalizer.py — Devanagari Crash Prevention + Text Normalizer…** (1 connections) — `app/services/hinglish_normalizer.py`
- **One Devanagari word → casual Hinglish roman ("चलाओ" → "chalao", "करना" →…** (1 connections) — `app/services/hinglish_normalizer.py`
- **Share of Devanagari words that are English loanwords ("ओपन क्रोम" → 1.0). High…** (1 connections) — `app/services/hinglish_normalizer.py`
- **Romanize a Devanagari (Hindi) transcript for the backend, keeping any Latin…** (1 connections) — `app/services/hinglish_normalizer.py`
- **Transform text so it's safe and natural-sounding for TTS: 1. Replace known…** (1 connections) — `app/services/hinglish_normalizer.py`
- **Markdown → plain speakable text (keeps Devanagari). Also drops URLs and emoji.** (1 connections) — `app/services/hinglish_normalizer.py`
- **Strict check used when there is no wake word to vouch for the audio.** (1 connections) — `app/services/voice.py`
- **voice.md** (1 connections) — `docs/features/voice.md`
- **Config (`app/core/config.py` + env)** (1 connections) — `docs/features/voice.md`
- **Files & symbols (auto-generated, line numbers are current)** (1 connections) — `docs/features/voice.md`
- **Graphify** (1 connections) — `docs/features/voice.md`
- *... and 3 more nodes in this community*

## Relationships

- [voice](voice.md) (17 shared connections)
- [voice_agent](voice_agent.md) (3 shared connections)
- [assignment_tool + assignment_humanizer](assignment_tool_+_assignment_humanizer.md) (1 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (1 shared connections)
- [voice + tools](voice_+_tools.md) (1 shared connections)

## Source Files

- `app/services/hinglish_normalizer.py`
- `app/services/voice.py`
- `docs/features/voice.md`

## Audit Trail

- EXTRACTED: 48 (89%)
- INFERRED: 6 (11%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*