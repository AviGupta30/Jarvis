# voice

> 30 nodes · cohesion 0.12

## Key Concepts

- **voice.py** (57 connections) — `app/services/voice.py`
- **transcribe_pcm()** (12 connections) — `app/services/voice.py`
- **transcribe_audio()** (8 connections) — `app/services/voice.py`
- **devanagari_to_hinglish()** (7 connections) — `app/services/hinglish_normalizer.py`
- **_finish()** (7 connections) — `app/services/voice.py`
- **ndarray** (6 connections)
- **_transcribe_groq()** (5 connections) — `app/services/voice.py`
- **_transcribe_local_sync()** (5 connections) — `app/services/voice.py`
- **Transcript** (5 connections) — `app/services/voice.py`
- **_groq_once()** (4 connections) — `app/services/voice.py`
- **_transcribe_local()** (4 connections) — `app/services/voice.py`
- **translate_for_speech()** (4 connections) — `app/services/voice.py`
- **STT (`voice.transcribe_pcm` → `Transcript`)** (4 connections) — `docs/features/voice.md`
- **_get_groq()** (3 connections) — `app/services/voice.py`
- **groq_stt_available()** (3 connections) — `app/services/voice.py`
- **_load_whisper_model()** (3 connections) — `app/services/voice.py`
- **pcm_to_wav_bytes()** (3 connections) — `app/services/voice.py`
- **_clean_transcript()** (2 connections) — `app/services/voice.py`
- **.push()** (2 connections) — `app/services/voice.py`
- **_load()** (2 connections) — `app/services/voice.py`
- **_seg_get()** (2 connections) — `app/services/voice.py`
- **Romanize a Devanagari (Hindi) transcript for the backend, keeping any Latin…** (1 connections) — `app/services/hinglish_normalizer.py`
- **groq_quota_low()** (1 connections) — `app/services/voice.py`
- **voice.py — Jarvis Voice Engine ------------------------------ STT Groq whisper-…** (1 connections) — `app/services/voice.py`
- **Returns (text, 'en'|'hi', logprob, no_speech). Raises on network/API failure.** (1 connections) — `app/services/voice.py`
- *... and 5 more nodes in this community*

## Relationships

- [voice](voice.md) (19 shared connections)
- [hinglish_normalizer](hinglish_normalizer.md) (7 shared connections)
- [voice + context_classifier](voice_+_context_classifier.md) (6 shared connections)
- [assignment_tool + safe_executor](assignment_tool_+_safe_executor.md) (5 shared connections)
- [voice_agent + acoustic_tripwire](voice_agent_+_acoustic_tripwire.md) (4 shared connections)
- [voice + test_hindi_tts](voice_+_test_hindi_tts.md) (3 shared connections)
- [chat](chat.md) (2 shared connections)
- [voice + voice_agent](voice_+_voice_agent.md) (2 shared connections)
- [syllabus_auditor + syllabus-auditor](syllabus_auditor_+_syllabus-auditor.md) (1 shared connections)
- [ppt_image_engine](ppt_image_engine.md) (1 shared connections)
- [ARCHITECTURE + acoustic_tripwire](ARCHITECTURE_+_acoustic_tripwire.md) (1 shared connections)

## Source Files

- `app/services/hinglish_normalizer.py`
- `app/services/voice.py`
- `docs/features/voice.md`

## Audit Trail

- EXTRACTED: 95 (91%)
- INFERRED: 9 (9%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*