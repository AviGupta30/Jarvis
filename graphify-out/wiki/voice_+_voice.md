# voice + voice

> 18 nodes · cohesion 0.11

## Key Concepts

- **Voice: STT, TTS, wake word, clap wake, overlay** (12 connections) — `docs/features/voice.md`
- **SentenceSplitter** (9 connections) — `app/services/voice.py`
- **speak_stream()** (5 connections) — `app/services/voice.py`
- **Gotchas** (5 connections) — `docs/features/voice.md`
- **preload_local_stt()** (4 connections) — `app/services/voice.py`
- **Load the local Whisper models in the background (voice agent startup).** (1 connections) — `app/services/voice.py`
- **Feed streamed tokens; get back speakable sentences as early as possible.** (1 connections) — `app/services/voice.py`
- **Speak an async generator of text chunks, sentence by sentence, pipelined.** (1 connections) — `app/services/voice.py`
- **.feed()** (1 connections) — `app/services/voice.py`
- **.flush()** (1 connections) — `app/services/voice.py`
- **.__init__()** (1 connections) — `app/services/voice.py`
- **voice.md** (1 connections) — `docs/features/voice.md`
- **Config (`app/core/config.py` + env)** (1 connections) — `docs/features/voice.md`
- **Files & symbols (auto-generated, line numbers are current)** (1 connections) — `docs/features/voice.md`
- **Graphify** (1 connections) — `docs/features/voice.md`
- **Measured (2026-09-30/10-01, i9-13900H, no GPU)** (1 connections) — `docs/features/voice.md`
- **Purpose** (1 connections) — `docs/features/voice.md`
- **Server-side tripwire** (1 connections) — `docs/features/voice.md`

## Relationships

- [voice](voice.md) (9 shared connections)
- [voice_agent + voice](voice_agent_+_voice.md) (2 shared connections)
- [voice_agent + main](voice_agent_+_main.md) (1 shared connections)
- [tools](tools.md) (1 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (1 shared connections)

## Source Files

- `app/services/voice.py`
- `docs/features/voice.md`

## Audit Trail

- EXTRACTED: 25 (81%)
- INFERRED: 6 (19%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*