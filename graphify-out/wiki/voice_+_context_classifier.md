# voice + context_classifier

> 11 nodes · cohesion 0.20

## Key Concepts

- **Flow (`scripts/voice_agent.py`)** (20 connections) — `docs/features/voice.md`
- **detect_language()** (10 connections) — `app/services/context_classifier.py`
- **language_mismatch()** (4 connections) — `app/services/voice.py`
- **route_language()** (4 connections) — `app/services/voice.py`
- **.output_level()** (3 connections) — `app/services/voice.py`
- **.confident()** (3 connections) — `app/services/voice.py`
- **Detect whether the user spoke English, Hinglish, or Hindi. Returns: 'english' —…** (1 connections) — `app/services/context_classifier.py`
- **True if a reply sentence is in the other language than the one the user spoke.** (1 connections) — `app/services/voice.py`
- **hi' → Hindi voice, 'en' → English voice, for one sentence.** (1 connections) — `app/services/voice.py`
- **Loudest output RMS in the last `window` s — the voice agent's echo reference.** (1 connections) — `app/services/voice.py`
- **Strict check used when there is no wake word to vouch for the audio.** (1 connections) — `app/services/voice.py`

## Relationships

- [voice](voice.md) (11 shared connections)
- [voice_agent](voice_agent.md) (7 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (4 shared connections)
- [voice_agent + acoustic_tripwire](voice_agent_+_acoustic_tripwire.md) (2 shared connections)
- [voice + voice_agent](voice_+_voice_agent.md) (2 shared connections)
- [hinglish_normalizer](hinglish_normalizer.md) (1 shared connections)

## Source Files

- `app/services/context_classifier.py`
- `app/services/voice.py`
- `docs/features/voice.md`

## Audit Trail

- EXTRACTED: 19 (50%)
- INFERRED: 19 (50%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*