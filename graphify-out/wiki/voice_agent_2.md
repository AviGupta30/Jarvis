# voice_agent

> 34 nodes · cohesion 0.10

## Key Concepts

- **Flow (`scripts/voice_agent.py`)** (20 connections) — `docs/features/voice.md`
- **VoiceAgent** (14 connections) — `scripts/voice_agent.py`
- **detect_language()** (10 connections) — `app/services/context_classifier.py`
- **stream_chat()** (9 connections) — `scripts/voice_agent.py`
- **.handle_utterance()** (9 connections) — `scripts/voice_agent.py`
- **_pick()** (7 connections) — `scripts/voice_agent.py`
- **.dispatch()** (6 connections) — `scripts/voice_agent.py`
- **._run_command()** (6 connections) — `scripts/voice_agent.py`
- **extract_wake_word_command()** (5 connections) — `scripts/voice_agent.py`
- **.run()** (5 connections) — `scripts/voice_agent.py`
- **language_mismatch()** (4 connections) — `app/services/voice.py`
- **on_event()** (4 connections) — `scripts/voice_agent.py`
- **say_text()** (4 connections) — `scripts/voice_agent.py`
- **._ui_loop()** (4 connections) — `scripts/voice_agent.py`
- **_reply_language_note()** (3 connections) — `app/services/llm.py`
- **_is_stop()** (3 connections) — `scripts/voice_agent.py`
- **set_ui_state()** (3 connections) — `scripts/voice_agent.py`
- **._greet_after_pause()** (3 connections) — `scripts/voice_agent.py`
- **.on_clap()** (3 connections) — `scripts/voice_agent.py`
- **._overlaps_speech()** (3 connections) — `scripts/voice_agent.py`
- **._safe_utterance()** (3 connections) — `scripts/voice_agent.py`
- **_is_wake_token()** (2 connections) — `scripts/voice_agent.py`
- **._open_followup()** (2 connections) — `scripts/voice_agent.py`
- **filler()** (2 connections) — `scripts/voice_agent.py`
- **Detect whether the user spoke English, Hinglish, or Hindi. Returns: 'english' —…** (1 connections) — `app/services/context_classifier.py`
- *... and 9 more nodes in this community*

## Relationships

- [voice_agent + ui_inspector](voice_agent_+_ui_inspector.md) (11 shared connections)
- [voice](voice.md) (8 shared connections)
- [voice_agent](voice_agent.md) (6 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (4 shared connections)
- [hinglish_normalizer + voice](hinglish_normalizer_+_voice.md) (3 shared connections)
- [voice + tools](voice_+_tools.md) (2 shared connections)
- [main + screen_vision](main_+_screen_vision.md) (2 shared connections)

## Source Files

- `app/services/context_classifier.py`
- `app/services/llm.py`
- `app/services/voice.py`
- `docs/features/voice.md`
- `scripts/voice_agent.py`

## Audit Trail

- EXTRACTED: 70 (78%)
- INFERRED: 20 (22%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*