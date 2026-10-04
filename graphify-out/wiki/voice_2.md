# voice

> 20 nodes · cohesion 0.11

## Key Concepts

- **speak_text()** (10 connections) — `app/services/voice.py`
- **SentenceSplitter** (9 connections) — `app/services/voice.py`
- **test_hindi_tts.py** (6 connections) — `scripts/test_hindi_tts.py`
- **speak_stream()** (5 connections) — `app/services/voice.py`
- **Gotchas** (5 connections) — `docs/features/voice.md`
- **get_player()** (4 connections) — `app/services/voice.py`
- **preload_local_stt()** (4 connections) — `app/services/voice.py`
- **_load_whisper_model()** (3 connections) — `app/services/voice.py`
- **split_sentences()** (3 connections) — `app/services/voice.py`
- **_load()** (2 connections) — `app/services/voice.py`
- **.__init__()** (2 connections) — `app/services/voice.py`
- **main()** (2 connections) — `scripts/test_hindi_tts.py`
- **Load the local Whisper models in the background (voice agent startup).** (1 connections) — `app/services/voice.py`
- **Feed streamed tokens; get back speakable sentences as early as possible.** (1 connections) — `app/services/voice.py`
- **Speak a complete text. All sentences synthesise in parallel, play in order.** (1 connections) — `app/services/voice.py`
- **Speak an async generator of text chunks, sentence by sentence, pipelined.** (1 connections) — `app/services/voice.py`
- **.feed()** (1 connections) — `app/services/voice.py`
- **.flush()** (1 connections) — `app/services/voice.py`
- **.__init__()** (1 connections) — `app/services/voice.py`
- **Test language-adaptive TTS - plays English then Hindi to verify both engines…** (1 connections) — `scripts/test_hindi_tts.py`

## Relationships

- [voice](voice.md) (13 shared connections)
- [tools](tools.md) (3 shared connections)
- [benchmark + download_kokoro](benchmark_+_download_kokoro.md) (2 shared connections)
- [voice_agent](voice_agent.md) (1 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (1 shared connections)
- [planner + dynamic_skill](planner_+_dynamic_skill.md) (1 shared connections)

## Source Files

- `app/services/voice.py`
- `docs/features/voice.md`
- `scripts/test_hindi_tts.py`

## Audit Trail

- EXTRACTED: 36 (86%)
- INFERRED: 6 (14%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*