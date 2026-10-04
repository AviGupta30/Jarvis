# voice

> 15 nodes · cohesion 0.14

## Key Concepts

- **speak_text()** (10 connections) — `app/services/voice.py`
- **SentenceSplitter** (9 connections) — `app/services/voice.py`
- **test_hindi_tts.py** (6 connections) — `scripts/test_hindi_tts.py`
- **speak_stream()** (5 connections) — `app/services/voice.py`
- **get_player()** (4 connections) — `app/services/voice.py`
- **split_sentences()** (3 connections) — `app/services/voice.py`
- **.__init__()** (2 connections) — `app/services/voice.py`
- **main()** (2 connections) — `scripts/test_hindi_tts.py`
- **Feed streamed tokens; get back speakable sentences as early as possible.** (1 connections) — `app/services/voice.py`
- **Speak a complete text. All sentences synthesise in parallel, play in order.** (1 connections) — `app/services/voice.py`
- **Speak an async generator of text chunks, sentence by sentence, pipelined.** (1 connections) — `app/services/voice.py`
- **.feed()** (1 connections) — `app/services/voice.py`
- **.flush()** (1 connections) — `app/services/voice.py`
- **.__init__()** (1 connections) — `app/services/voice.py`
- **Test language-adaptive TTS - plays English then Hindi to verify both engines…** (1 connections) — `scripts/test_hindi_tts.py`

## Relationships

- [voice](voice.md) (9 shared connections)
- [voice + voice](voice_+_voice.md) (2 shared connections)
- [tools](tools.md) (2 shared connections)
- [voice_agent](voice_agent.md) (1 shared connections)
- [voice + voice_agent](voice_+_voice_agent.md) (1 shared connections)
- [rag_memory + mysql_db](rag_memory_+_mysql_db.md) (1 shared connections)
- [benchmark + server](benchmark_+_server.md) (1 shared connections)
- [chat + llm](chat_+_llm.md) (1 shared connections)

## Source Files

- `app/services/voice.py`
- `scripts/test_hindi_tts.py`

## Audit Trail

- EXTRACTED: 30 (91%)
- INFERRED: 3 (9%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*