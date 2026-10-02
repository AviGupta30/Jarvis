# voice

> 7 nodes · cohesion 0.29

## Key Concepts

- **SentenceSplitter** (9 connections) — `app/services/voice.py`
- **speak_stream()** (5 connections) — `app/services/voice.py`
- **Feed streamed tokens; get back speakable sentences as early as possible.** (1 connections) — `app/services/voice.py`
- **Speak an async generator of text chunks, sentence by sentence, pipelined.** (1 connections) — `app/services/voice.py`
- **.feed()** (1 connections) — `app/services/voice.py`
- **.flush()** (1 connections) — `app/services/voice.py`
- **.__init__()** (1 connections) — `app/services/voice.py`

## Relationships

- [voice](voice.md) (3 shared connections)
- [voice + tools](voice_+_tools.md) (1 shared connections)
- [voice_agent](voice_agent.md) (1 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (1 shared connections)
- [voice + voice](voice_+_voice.md) (1 shared connections)

## Source Files

- `app/services/voice.py`

## Audit Trail

- EXTRACTED: 11 (85%)
- INFERRED: 2 (15%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*