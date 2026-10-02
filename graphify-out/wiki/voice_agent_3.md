# voice_agent

> 10 nodes · cohesion 0.33

## Key Concepts

- **MicListener** (11 connections) — `scripts/voice_agent.py`
- **._process()** (5 connections) — `scripts/voice_agent.py`
- **.run()** (5 connections) — `scripts/voice_agent.py`
- **._calibrate()** (3 connections) — `scripts/voice_agent.py`
- **._is_user_frame()** (3 connections) — `scripts/voice_agent.py`
- **._emit()** (2 connections) — `scripts/voice_agent.py`
- **._open()** (2 connections) — `scripts/voice_agent.py`
- **._reset_segmenter()** (2 connections) — `scripts/voice_agent.py`
- **Initial ambient noise floor (kept up to date on every non-speech frame).** (1 connections) — `scripts/voice_agent.py`
- **One 32 ms frame → clap check + VAD state machine → events.** (1 connections) — `scripts/voice_agent.py`

## Relationships

- [voice_agent](voice_agent.md) (3 shared connections)
- [voice](voice.md) (1 shared connections)
- [context_classifier + personality](context_classifier_+_personality.md) (1 shared connections)

## Source Files

- `scripts/voice_agent.py`

## Audit Trail

- EXTRACTED: 18 (90%)
- INFERRED: 2 (10%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*