# voice + voice_agent

> 8 nodes · cohesion 0.25

## Key Concepts

- **Flow (`scripts/voice_agent.py`)** (20 connections) — `docs/features/voice.md`
- **language_mismatch()** (4 connections) — `app/services/voice.py`
- **.output_level()** (3 connections) — `app/services/voice.py`
- **.confident()** (3 connections) — `app/services/voice.py`
- **_is_stop()** (3 connections) — `scripts/voice_agent.py`
- **True if a reply sentence is in the other language than the one the user spoke.** (1 connections) — `app/services/voice.py`
- **Loudest output RMS in the last `window` s — the voice agent's echo reference.** (1 connections) — `app/services/voice.py`
- **Strict check used when there is no wake word to vouch for the audio.** (1 connections) — `app/services/voice.py`

## Relationships

- [voice_agent](voice_agent.md) (9 shared connections)
- [voice](voice.md) (8 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (3 shared connections)
- [voice + voice](voice_+_voice.md) (1 shared connections)
- [hinglish_normalizer](hinglish_normalizer.md) (1 shared connections)

## Source Files

- `app/services/voice.py`
- `docs/features/voice.md`
- `scripts/voice_agent.py`

## Audit Trail

- EXTRACTED: 10 (34%)
- INFERRED: 19 (66%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*