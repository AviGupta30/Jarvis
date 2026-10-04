# voice

> 27 nodes · cohesion 0.11

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
- **.push()** (2 connections) — `app/services/voice.py`
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
- *... and 2 more nodes in this community*

## Relationships

- [voice](voice.md) (26 shared connections)
- [hinglish_normalizer + voice](hinglish_normalizer_+_voice.md) (6 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (4 shared connections)
- [voice + hinglish_normalizer](voice_+_hinglish_normalizer.md) (4 shared connections)
- [planner + dynamic_skill](planner_+_dynamic_skill.md) (2 shared connections)
- [server + persistence](server_+_persistence.md) (2 shared connections)
- [benchmark + download_kokoro](benchmark_+_download_kokoro.md) (2 shared connections)
- [safe_executor](safe_executor.md) (1 shared connections)
- [assignment_assembler + smart_navigator](assignment_assembler_+_smart_navigator.md) (1 shared connections)
- [dump_wa_ui + test_wa](dump_wa_ui_+_test_wa.md) (1 shared connections)
- [acoustic_tripwire](acoustic_tripwire.md) (1 shared connections)
- [refresh_docs](refresh_docs.md) (1 shared connections)

## Source Files

- `app/services/voice.py`

## Audit Trail

- EXTRACTED: 88 (97%)
- INFERRED: 3 (3%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*