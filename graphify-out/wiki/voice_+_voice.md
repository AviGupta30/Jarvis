# voice + voice

> 13 nodes · cohesion 0.15

## Key Concepts

- **Voice: STT, TTS, wake word, clap wake, overlay** (12 connections) — `docs/features/voice.md`
- **Gotchas** (5 connections) — `docs/features/voice.md`
- **preload_local_stt()** (4 connections) — `app/services/voice.py`
- **_load_whisper_model()** (3 connections) — `app/services/voice.py`
- **_load()** (2 connections) — `app/services/voice.py`
- **Load the local Whisper models in the background (voice agent startup).** (1 connections) — `app/services/voice.py`
- **voice.md** (1 connections) — `docs/features/voice.md`
- **Config (`app/core/config.py` + env)** (1 connections) — `docs/features/voice.md`
- **Files & symbols (auto-generated, line numbers are current)** (1 connections) — `docs/features/voice.md`
- **Graphify** (1 connections) — `docs/features/voice.md`
- **Measured (2026-09-30/10-01, i9-13900H, no GPU)** (1 connections) — `docs/features/voice.md`
- **Purpose** (1 connections) — `docs/features/voice.md`
- **Server-side tripwire** (1 connections) — `docs/features/voice.md`

## Relationships

- [voice](voice.md) (7 shared connections)
- [tools](tools.md) (1 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (1 shared connections)
- [voice + voice_agent](voice_+_voice_agent.md) (1 shared connections)

## Source Files

- `app/services/voice.py`
- `docs/features/voice.md`

## Audit Trail

- EXTRACTED: 17 (77%)
- INFERRED: 5 (23%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*