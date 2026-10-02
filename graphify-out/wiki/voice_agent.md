# voice_agent

> 20 nodes · cohesion 0.13

## Key Concepts

- **_ClapDetector** (8 connections) — `scripts/voice_agent.py`
- **.__init__()** (7 connections) — `scripts/voice_agent.py`
- **_SileroStream** (7 connections) — `scripts/voice_agent.py`
- **_EnergyVAD** (6 connections) — `scripts/voice_agent.py`
- **ndarray** (5 connections)
- **.feed()** (3 connections) — `scripts/voice_agent.py`
- **._hf_ratio()** (3 connections) — `scripts/voice_agent.py`
- **.__call__()** (2 connections) — `scripts/voice_agent.py`
- **.reset()** (2 connections) — `scripts/voice_agent.py`
- **.__call__()** (2 connections) — `scripts/voice_agent.py`
- **.__init__()** (2 connections) — `scripts/voice_agent.py`
- **.__init__()** (2 connections) — `scripts/voice_agent.py`
- **AbstractEventLoop** (1 connections)
- **.__init__()** (1 connections) — `scripts/voice_agent.py`
- **.__init__()** (1 connections) — `scripts/voice_agent.py`
- **Queue** (1 connections)
- **Stateful frame-by-frame Silero VAD using the ONNX model bundled with faster-…** (1 connections) — `scripts/voice_agent.py`
- **Fallback if Silero can't load: adaptive noise floor.** (1 connections) — `scripts/voice_agent.py`
- **Strict double clap. The old tripwire fired on ANY two loud 2–8 kHz frames…** (1 connections) — `scripts/voice_agent.py`
- **.reset()** (1 connections) — `scripts/voice_agent.py`

## Relationships

- [voice_agent + acoustic_tripwire](voice_agent_+_acoustic_tripwire.md) (3 shared connections)
- [voice_agent](voice_agent.md) (3 shared connections)
- [voice + context_classifier](voice_+_context_classifier.md) (2 shared connections)
- [ppt_content + KNOWN_ISSUES](ppt_content_+_KNOWN_ISSUES.md) (1 shared connections)

## Source Files

- `scripts/voice_agent.py`

## Audit Trail

- EXTRACTED: 30 (91%)
- INFERRED: 3 (9%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*