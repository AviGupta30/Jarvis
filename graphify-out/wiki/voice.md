# voice

> 45 nodes · cohesion 0.08

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
- **pcm_to_wav_bytes()** (3 connections) — `app/services/voice.py`
- **prewarm()** (3 connections) — `app/services/voice.py`
- **_sapi_sync()** (3 connections) — `app/services/voice.py`
- **_clean_transcript()** (2 connections) — `app/services/voice.py`
- **.push()** (2 connections) — `app/services/voice.py`
- *... and 20 more nodes in this community*

## Relationships

- [voice](voice.md) (17 shared connections)
- [hinglish_normalizer](hinglish_normalizer.md) (8 shared connections)
- [benchmark + server](benchmark_+_server.md) (4 shared connections)
- [voice + voice](voice_+_voice.md) (4 shared connections)
- [voice + voice_agent](voice_+_voice_agent.md) (4 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (3 shared connections)
- [rag_memory + mysql_db](rag_memory_+_mysql_db.md) (1 shared connections)
- [safe_executor](safe_executor.md) (1 shared connections)
- [assignment_assembler + smart_navigator](assignment_assembler_+_smart_navigator.md) (1 shared connections)
- [dark_enhancement + dark_video_enhancement](dark_enhancement_+_dark_video_enhancement.md) (1 shared connections)
- [chat + llm](chat_+_llm.md) (1 shared connections)
- [ppt_image_engine](ppt_image_engine.md) (1 shared connections)

## Source Files

- `app/services/hinglish_normalizer.py`
- `app/services/voice.py`
- `docs/features/voice.md`

## Audit Trail

- EXTRACTED: 117 (92%)
- INFERRED: 10 (8%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*