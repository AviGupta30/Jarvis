# voice

> 12 nodes · cohesion 0.24

## Key Concepts

- **transcribe_pcm()** (12 connections) — `app/services/voice.py`
- **transcribe_audio()** (8 connections) — `app/services/voice.py`
- **ndarray** (6 connections)
- **_transcribe_groq()** (5 connections) — `app/services/voice.py`
- **_transcribe_local_sync()** (5 connections) — `app/services/voice.py`
- **_transcribe_local()** (4 connections) — `app/services/voice.py`
- **groq_stt_available()** (3 connections) — `app/services/voice.py`
- **pcm_to_wav_bytes()** (3 connections) — `app/services/voice.py`
- **Returns (text, 'en'|'hi', logprob, no_speech). Raises on network/API failure.** (1 connections) — `app/services/voice.py`
- **Transcribe one VAD-segmented utterance (int16 mono 16 kHz). prefer_local=True…** (1 connections) — `app/services/voice.py`
- **Back-compat: transcribe a WAV file path → romanized text ('' on failure).** (1 connections) — `app/services/voice.py`
- **_run()** (1 connections) — `app/services/voice.py`

## Relationships

- [voice](voice.md) (12 shared connections)
- [hinglish_normalizer + voice](hinglish_normalizer_+_voice.md) (4 shared connections)
- [ARCHITECTURE](ARCHITECTURE.md) (1 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (1 shared connections)

## Source Files

- `app/services/voice.py`

## Audit Trail

- EXTRACTED: 30 (88%)
- INFERRED: 4 (12%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*