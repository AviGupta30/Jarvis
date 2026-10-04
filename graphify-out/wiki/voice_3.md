# voice

> 18 nodes · cohesion 0.14

## Key Concepts

- **_Player** (12 connections) — `app/services/voice.py`
- **speak_text()** (10 connections) — `app/services/voice.py`
- **.play()** (6 connections) — `app/services/voice.py`
- **test_hindi_tts.py** (6 connections) — `scripts/test_hindi_tts.py`
- **get_player()** (4 connections) — `app/services/voice.py`
- **._push()** (3 connections) — `app/services/voice.py`
- **split_sentences()** (3 connections) — `app/services/voice.py`
- **.clear()** (2 connections) — `app/services/voice.py`
- **._ensure()** (2 connections) — `app/services/voice.py`
- **.__init__()** (2 connections) — `app/services/voice.py`
- **main()** (2 connections) — `scripts/test_hindi_tts.py`
- **._callback()** (1 connections) — `app/services/voice.py`
- **.__init__()** (1 connections) — `app/services/voice.py`
- **.pending()** (1 connections) — `app/services/voice.py`
- **One persistent 24 kHz output stream driven by a callback that pulls from a…** (1 connections) — `app/services/voice.py`
- **Play a clip as it arrives. Returns False if interrupted.** (1 connections) — `app/services/voice.py`
- **Speak a complete text. All sentences synthesise in parallel, play in order.** (1 connections) — `app/services/voice.py`
- **Test language-adaptive TTS - plays English then Hindi to verify both engines…** (1 connections) — `scripts/test_hindi_tts.py`

## Relationships

- [voice](voice.md) (9 shared connections)
- [tools](tools.md) (2 shared connections)
- [voice + voice](voice_+_voice.md) (2 shared connections)
- [voice_agent + download_kokoro](voice_agent_+_download_kokoro.md) (2 shared connections)
- [voice_agent + voice](voice_agent_+_voice.md) (1 shared connections)
- [rag_memory + tool_runner](rag_memory_+_tool_runner.md) (1 shared connections)

## Source Files

- `app/services/voice.py`
- `scripts/test_hindi_tts.py`

## Audit Trail

- EXTRACTED: 36 (95%)
- INFERRED: 2 (5%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*