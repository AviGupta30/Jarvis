# voice

> 51 nodes · cohesion 0.07

## Key Concepts

- **voice.py** (57 connections) — `app/services/voice.py`
- **transcribe_pcm()** (12 connections) — `app/services/voice.py`
- **Clip** (11 connections) — `app/services/voice.py`
- **start_clip()** (10 connections) — `app/services/voice.py`
- **transcribe_audio()** (8 connections) — `app/services/voice.py`
- **devanagari_to_hinglish()** (7 connections) — `app/services/hinglish_normalizer.py`
- **_finish()** (7 connections) — `app/services/voice.py`
- **ndarray** (6 connections)
- **_synth_edge()** (6 connections) — `app/services/voice.py`
- **loanword_ratio()** (5 connections) — `app/services/hinglish_normalizer.py`
- **_synthesize()** (5 connections) — `app/services/voice.py`
- **_transcribe_groq()** (5 connections) — `app/services/voice.py`
- **_transcribe_local_sync()** (5 connections) — `app/services/voice.py`
- **Transcript** (5 connections) — `app/services/voice.py`
- **_groq_once()** (4 connections) — `app/services/voice.py`
- **route_language()** (4 connections) — `app/services/voice.py`
- **_transcribe_local()** (4 connections) — `app/services/voice.py`
- **translate_for_speech()** (4 connections) — `app/services/voice.py`
- **STT (`voice.transcribe_pcm` → `Transcript`)** (4 connections) — `docs/features/voice.md`
- **_get_groq()** (3 connections) — `app/services/voice.py`
- **groq_stt_available()** (3 connections) — `app/services/voice.py`
- **_load_whisper_model()** (3 connections) — `app/services/voice.py`
- **pcm_to_wav_bytes()** (3 connections) — `app/services/voice.py`
- **prewarm()** (3 connections) — `app/services/voice.py`
- **_sapi_sync()** (3 connections) — `app/services/voice.py`
- *... and 26 more nodes in this community*

## Relationships

- [voice](voice.md) (15 shared connections)
- [hinglish_normalizer](hinglish_normalizer.md) (7 shared connections)
- [voice_agent + voice](voice_agent_+_voice.md) (7 shared connections)
- [voice_agent + download_kokoro](voice_agent_+_download_kokoro.md) (6 shared connections)
- [voice + voice](voice_+_voice.md) (5 shared connections)
- [message_reader + thread_extractor](message_reader_+_thread_extractor.md) (3 shared connections)
- [rag_memory + tool_runner](rag_memory_+_tool_runner.md) (1 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (1 shared connections)
- [ppt_image_engine](ppt_image_engine.md) (1 shared connections)
- [dynamic_skill + planner](dynamic_skill_+_planner.md) (1 shared connections)
- [acoustic_tripwire](acoustic_tripwire.md) (1 shared connections)

## Source Files

- `app/services/hinglish_normalizer.py`
- `app/services/voice.py`
- `docs/features/voice.md`

## Audit Trail

- EXTRACTED: 121 (90%)
- INFERRED: 13 (10%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*