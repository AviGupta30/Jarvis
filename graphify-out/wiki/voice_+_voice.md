# voice + voice

> 12 nodes · cohesion 0.17

## Key Concepts

- **Flow (`scripts/voice_agent.py`)** (20 connections) — `docs/features/voice.md`
- **Voice: STT, TTS, wake word, clap wake, overlay** (12 connections) — `docs/features/voice.md`
- **language_mismatch()** (4 connections) — `app/services/voice.py`
- **_is_stop()** (3 connections) — `scripts/voice_agent.py`
- **True if a reply sentence is in the other language than the one the user spoke.** (1 connections) — `app/services/voice.py`
- **voice.md** (1 connections) — `docs/features/voice.md`
- **Config (`app/core/config.py` + env)** (1 connections) — `docs/features/voice.md`
- **Files & symbols (auto-generated, line numbers are current)** (1 connections) — `docs/features/voice.md`
- **Graphify** (1 connections) — `docs/features/voice.md`
- **Measured (2026-09-30/10-01, i9-13900H, no GPU)** (1 connections) — `docs/features/voice.md`
- **Purpose** (1 connections) — `docs/features/voice.md`
- **Server-side tripwire** (1 connections) — `docs/features/voice.md`

## Relationships

- [voice](voice.md) (9 shared connections)
- [voice_agent](voice_agent.md) (9 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (4 shared connections)
- [voice + tools](voice_+_tools.md) (2 shared connections)
- [hinglish_normalizer](hinglish_normalizer.md) (1 shared connections)

## Source Files

- `app/services/voice.py`
- `docs/features/voice.md`
- `scripts/voice_agent.py`

## Audit Trail

- EXTRACTED: 17 (47%)
- INFERRED: 19 (53%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*