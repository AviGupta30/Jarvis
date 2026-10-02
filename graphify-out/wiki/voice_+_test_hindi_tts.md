# voice + test_hindi_tts

> 8 nodes · cohesion 0.29

## Key Concepts

- **speak_text()** (10 connections) — `app/services/voice.py`
- **test_hindi_tts.py** (6 connections) — `scripts/test_hindi_tts.py`
- **get_player()** (4 connections) — `app/services/voice.py`
- **split_sentences()** (3 connections) — `app/services/voice.py`
- **.__init__()** (2 connections) — `app/services/voice.py`
- **main()** (2 connections) — `scripts/test_hindi_tts.py`
- **Speak a complete text. All sentences synthesise in parallel, play in order.** (1 connections) — `app/services/voice.py`
- **Test language-adaptive TTS - plays English then Hindi to verify both engines…** (1 connections) — `scripts/test_hindi_tts.py`

## Relationships

- [voice](voice.md) (7 shared connections)
- [tools](tools.md) (2 shared connections)
- [assignment_tool + safe_executor](assignment_tool_+_safe_executor.md) (2 shared connections)
- [voice + voice_agent](voice_+_voice_agent.md) (1 shared connections)
- [chat](chat.md) (1 shared connections)

## Source Files

- `app/services/voice.py`
- `scripts/test_hindi_tts.py`

## Audit Trail

- EXTRACTED: 20 (95%)
- INFERRED: 1 (5%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*