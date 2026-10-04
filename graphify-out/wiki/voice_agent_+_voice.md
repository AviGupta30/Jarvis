# voice_agent + voice

> 28 nodes · cohesion 0.12

## Key Concepts

- **Flow (`scripts/voice_agent.py`)** (20 connections) — `docs/features/voice.md`
- **VoiceAgent** (14 connections) — `scripts/voice_agent.py`
- **detect_language()** (10 connections) — `app/services/context_classifier.py`
- **.handle_utterance()** (9 connections) — `scripts/voice_agent.py`
- **_pick()** (7 connections) — `scripts/voice_agent.py`
- **.dispatch()** (6 connections) — `scripts/voice_agent.py`
- **._run_command()** (6 connections) — `scripts/voice_agent.py`
- **.run()** (5 connections) — `scripts/voice_agent.py`
- **language_mismatch()** (4 connections) — `app/services/voice.py`
- **._ui_loop()** (4 connections) — `scripts/voice_agent.py`
- **_reply_language_note()** (3 connections) — `app/services/llm.py`
- **.output_level()** (3 connections) — `app/services/voice.py`
- **_is_stop()** (3 connections) — `scripts/voice_agent.py`
- **set_ui_state()** (3 connections) — `scripts/voice_agent.py`
- **._greet_after_pause()** (3 connections) — `scripts/voice_agent.py`
- **.on_clap()** (3 connections) — `scripts/voice_agent.py`
- **._overlaps_speech()** (3 connections) — `scripts/voice_agent.py`
- **._safe_utterance()** (3 connections) — `scripts/voice_agent.py`
- **run_voice_agent()** (2 connections) — `scripts/voice_agent.py`
- **._open_followup()** (2 connections) — `scripts/voice_agent.py`
- **filler()** (2 connections) — `scripts/voice_agent.py`
- **Detect whether the user spoke English, Hinglish, or Hindi. Returns: 'english' —…** (1 connections) — `app/services/context_classifier.py`
- **True if a reply sentence is in the other language than the one the user spoke.** (1 connections) — `app/services/voice.py`
- **Loudest output RMS in the last `window` s — the voice agent's echo reference.** (1 connections) — `app/services/voice.py`
- **Write Jarvis UI state so the overlay can animate accordingly.** (1 connections) — `scripts/voice_agent.py`
- *... and 3 more nodes in this community*

## Relationships

- [voice](voice.md) (10 shared connections)
- [voice_agent + download_kokoro](voice_agent_+_download_kokoro.md) (8 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (5 shared connections)
- [voice_agent + KNOWN_ISSUES](voice_agent_+_KNOWN_ISSUES.md) (4 shared connections)
- [voice_agent + main](voice_agent_+_main.md) (3 shared connections)
- [voice + voice](voice_+_voice.md) (2 shared connections)
- [voice_agent](voice_agent.md) (2 shared connections)

## Source Files

- `app/services/context_classifier.py`
- `app/services/llm.py`
- `app/services/voice.py`
- `docs/features/voice.md`
- `scripts/voice_agent.py`

## Audit Trail

- EXTRACTED: 58 (74%)
- INFERRED: 20 (26%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*