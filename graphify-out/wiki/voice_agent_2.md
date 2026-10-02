# voice_agent

> 19 nodes · cohesion 0.18

## Key Concepts

- **VoiceAgent** (14 connections) — `scripts/voice_agent.py`
- **.handle_utterance()** (9 connections) — `scripts/voice_agent.py`
- **_pick()** (7 connections) — `scripts/voice_agent.py`
- **.dispatch()** (6 connections) — `scripts/voice_agent.py`
- **._run_command()** (6 connections) — `scripts/voice_agent.py`
- **.run()** (5 connections) — `scripts/voice_agent.py`
- **._ui_loop()** (4 connections) — `scripts/voice_agent.py`
- **_is_stop()** (3 connections) — `scripts/voice_agent.py`
- **set_ui_state()** (3 connections) — `scripts/voice_agent.py`
- **._greet_after_pause()** (3 connections) — `scripts/voice_agent.py`
- **.on_clap()** (3 connections) — `scripts/voice_agent.py`
- **._overlaps_speech()** (3 connections) — `scripts/voice_agent.py`
- **._safe_utterance()** (3 connections) — `scripts/voice_agent.py`
- **._open_followup()** (2 connections) — `scripts/voice_agent.py`
- **filler()** (2 connections) — `scripts/voice_agent.py`
- **Write Jarvis UI state so the overlay can animate accordingly.** (1 connections) — `scripts/voice_agent.py`
- **Was Jarvis talking (or just finished) during [t0, t1]?** (1 connections) — `scripts/voice_agent.py`
- **_done()** (1 connections) — `scripts/voice_agent.py`
- **._on_speaker_state()** (1 connections) — `scripts/voice_agent.py`

## Relationships

- [voice_agent + acoustic_tripwire](voice_agent_+_acoustic_tripwire.md) (6 shared connections)
- [voice + context_classifier](voice_+_context_classifier.md) (4 shared connections)
- [voice_agent](voice_agent.md) (3 shared connections)
- [voice + voice_agent](voice_+_voice_agent.md) (2 shared connections)

## Source Files

- `scripts/voice_agent.py`

## Audit Trail

- EXTRACTED: 42 (91%)
- INFERRED: 4 (9%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*