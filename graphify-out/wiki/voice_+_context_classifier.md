# voice + context_classifier

> 7 nodes · cohesion 0.33

## Key Concepts

- **Flow (`scripts/voice_agent.py`)** (20 connections) — `docs/features/voice.md`
- **detect_language()** (10 connections) — `app/services/context_classifier.py`
- **language_mismatch()** (4 connections) — `app/services/voice.py`
- **.output_level()** (3 connections) — `app/services/voice.py`
- **Detect whether the user spoke English, Hinglish, or Hindi. Returns: 'english' —…** (1 connections) — `app/services/context_classifier.py`
- **True if a reply sentence is in the other language than the one the user spoke.** (1 connections) — `app/services/voice.py`
- **Loudest output RMS in the last `window` s — the voice agent's echo reference.** (1 connections) — `app/services/voice.py`

## Relationships

- [voice](voice.md) (11 shared connections)
- [voice_agent](voice_agent.md) (10 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (4 shared connections)
- [voice + tools](voice_+_tools.md) (1 shared connections)

## Source Files

- `app/services/context_classifier.py`
- `app/services/voice.py`
- `docs/features/voice.md`

## Audit Trail

- EXTRACTED: 14 (42%)
- INFERRED: 19 (58%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*