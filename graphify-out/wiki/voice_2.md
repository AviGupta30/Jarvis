# voice

> 26 nodes · cohesion 0.11

## Key Concepts

- **voice.py** (57 connections) — `app/services/voice.py`
- **Clip** (11 connections) — `app/services/voice.py`
- **start_clip()** (10 connections) — `app/services/voice.py`
- **_synth_edge()** (6 connections) — `app/services/voice.py`
- **_synthesize()** (5 connections) — `app/services/voice.py`
- **_groq_once()** (4 connections) — `app/services/voice.py`
- **route_language()** (4 connections) — `app/services/voice.py`
- **translate_for_speech()** (4 connections) — `app/services/voice.py`
- **_get_groq()** (3 connections) — `app/services/voice.py`
- **prewarm()** (3 connections) — `app/services/voice.py`
- **_sapi_sync()** (3 connections) — `app/services/voice.py`
- **_seg_get()** (2 connections) — `app/services/voice.py`
- **_voice_for()** (2 connections) — `app/services/voice.py`
- **.cancel()** (1 connections) — `app/services/voice.py`
- **.finish()** (1 connections) — `app/services/voice.py`
- **.__init__()** (1 connections) — `app/services/voice.py`
- **.iter_chunks()** (1 connections) — `app/services/voice.py`
- **groq_quota_low()** (1 connections) — `app/services/voice.py`
- **voice.py — Jarvis Voice Engine ------------------------------ STT Groq whisper-…** (1 connections) — `app/services/voice.py`
- **Translate one reply sentence into the user's language (canned tool/flow replies…** (1 connections) — `app/services/voice.py`
- **PCM (int16, 24 kHz) that fills while synthesis streams; playable immediately.** (1 connections) — `app/services/voice.py`
- **hi' → Hindi voice, 'en' → English voice, for one sentence.** (1 connections) — `app/services/voice.py`
- **Begin synthesising `text` now; returns a Clip that can be played while it fills.** (1 connections) — `app/services/voice.py`
- **Synthesise short stock phrases (greetings, acks) into the cache for instant…** (1 connections) — `app/services/voice.py`
- **_decode()** (1 connections) — `app/services/voice.py`
- *... and 1 more nodes in this community*

## Relationships

- [voice](voice.md) (25 shared connections)
- [hinglish_normalizer](hinglish_normalizer.md) (5 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (4 shared connections)
- [smart_navigator + rag_memory](smart_navigator_+_rag_memory.md) (4 shared connections)
- [voice + tools](voice_+_tools.md) (4 shared connections)
- [memory + rag_memory](memory_+_rag_memory.md) (2 shared connections)
- [screen_vision + screen_reader](screen_vision_+_screen_reader.md) (2 shared connections)
- [voice + voice](voice_+_voice.md) (2 shared connections)
- [persistence + engine](persistence_+_engine.md) (1 shared connections)
- [server + test_concurrency](server_+_test_concurrency.md) (1 shared connections)
- [refresh_docs](refresh_docs.md) (1 shared connections)
- [ppt_image_engine](ppt_image_engine.md) (1 shared connections)

## Source Files

- `app/services/voice.py`

## Audit Trail

- EXTRACTED: 87 (97%)
- INFERRED: 3 (3%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*