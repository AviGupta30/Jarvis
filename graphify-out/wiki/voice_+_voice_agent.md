# voice + voice_agent

> 13 nodes · cohesion 0.17

## Key Concepts

- **SentenceSplitter** (9 connections) — `app/services/voice.py`
- **stream_chat()** (9 connections) — `scripts/voice_agent.py`
- **speak_stream()** (5 connections) — `app/services/voice.py`
- **on_event()** (4 connections) — `scripts/voice_agent.py`
- **say_text()** (4 connections) — `scripts/voice_agent.py`
- **Feed streamed tokens; get back speakable sentences as early as possible.** (1 connections) — `app/services/voice.py`
- **Speak an async generator of text chunks, sentence by sentence, pipelined.** (1 connections) — `app/services/voice.py`
- **.feed()** (1 connections) — `app/services/voice.py`
- **.flush()** (1 connections) — `app/services/voice.py`
- **.__init__()** (1 connections) — `app/services/voice.py`
- **AsyncClient** (1 connections)
- **POST /chat with the spoken language, speak the reply into `ch` as it streams.…** (1 connections) — `scripts/voice_agent.py`
- **pusher()** (1 connections) — `scripts/voice_agent.py`

## Relationships

- [voice](voice.md) (4 shared connections)
- [voice + context_classifier](voice_+_context_classifier.md) (2 shared connections)
- [voice_agent](voice_agent.md) (2 shared connections)
- [voice_agent + acoustic_tripwire](voice_agent_+_acoustic_tripwire.md) (2 shared connections)
- [main + screen_vision](main_+_screen_vision.md) (2 shared connections)
- [voice + test_hindi_tts](voice_+_test_hindi_tts.md) (1 shared connections)

## Source Files

- `app/services/voice.py`
- `scripts/voice_agent.py`

## Audit Trail

- EXTRACTED: 23 (88%)
- INFERRED: 3 (12%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*