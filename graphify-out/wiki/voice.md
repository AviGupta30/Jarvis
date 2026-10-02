# voice

> 21 nodes · cohesion 0.14

## Key Concepts

- **transcribe_pcm()** (12 connections) — `app/services/voice.py`
- **transcribe_audio()** (8 connections) — `app/services/voice.py`
- **devanagari_to_hinglish()** (7 connections) — `app/services/hinglish_normalizer.py`
- **_finish()** (7 connections) — `app/services/voice.py`
- **ndarray** (6 connections)
- **_transcribe_groq()** (5 connections) — `app/services/voice.py`
- **_transcribe_local_sync()** (5 connections) — `app/services/voice.py`
- **Transcript** (5 connections) — `app/services/voice.py`
- **_transcribe_local()** (4 connections) — `app/services/voice.py`
- **STT (`voice.transcribe_pcm` → `Transcript`)** (4 connections) — `docs/features/voice.md`
- **groq_stt_available()** (3 connections) — `app/services/voice.py`
- **pcm_to_wav_bytes()** (3 connections) — `app/services/voice.py`
- **.confident()** (3 connections) — `app/services/voice.py`
- **_clean_transcript()** (2 connections) — `app/services/voice.py`
- **.push()** (2 connections) — `app/services/voice.py`
- **Romanize a Devanagari (Hindi) transcript for the backend, keeping any Latin…** (1 connections) — `app/services/hinglish_normalizer.py`
- **Returns (text, 'en'|'hi', logprob, no_speech). Raises on network/API failure.** (1 connections) — `app/services/voice.py`
- **Transcribe one VAD-segmented utterance (int16 mono 16 kHz). prefer_local=True…** (1 connections) — `app/services/voice.py`
- **Back-compat: transcribe a WAV file path → romanized text ('' on failure).** (1 connections) — `app/services/voice.py`
- **Strict check used when there is no wake word to vouch for the audio.** (1 connections) — `app/services/voice.py`
- **_run()** (1 connections) — `app/services/voice.py`

## Relationships

- [voice](voice.md) (16 shared connections)
- [hinglish_normalizer](hinglish_normalizer.md) (3 shared connections)
- [voice + voice](voice_+_voice.md) (2 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (2 shared connections)
- [ARCHITECTURE + acoustic_tripwire](ARCHITECTURE_+_acoustic_tripwire.md) (1 shared connections)

## Source Files

- `app/services/hinglish_normalizer.py`
- `app/services/voice.py`
- `docs/features/voice.md`

## Audit Trail

- EXTRACTED: 45 (85%)
- INFERRED: 8 (15%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*