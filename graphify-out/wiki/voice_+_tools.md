# voice + tools

> 11 nodes · cohesion 0.20

## Key Concepts

- **speak_text()** (10 connections) — `app/services/voice.py`
- **set_reminder()** (7 connections) — `app/services/tools.py`
- **test_hindi_tts.py** (6 connections) — `scripts/test_hindi_tts.py`
- **get_player()** (4 connections) — `app/services/voice.py`
- **split_sentences()** (3 connections) — `app/services/voice.py`
- **.__init__()** (2 connections) — `app/services/voice.py`
- **main()** (2 connections) — `scripts/test_hindi_tts.py`
- **Sets a reminder that Jarvis will speak after a given number of seconds.** (1 connections) — `app/services/tools.py`
- **_remind()** (1 connections) — `app/services/tools.py`
- **Speak a complete text. All sentences synthesise in parallel, play in order.** (1 connections) — `app/services/voice.py`
- **Test language-adaptive TTS - plays English then Hindi to verify both engines…** (1 connections) — `scripts/test_hindi_tts.py`

## Relationships

- [voice](voice.md) (7 shared connections)
- [tools](tools.md) (2 shared connections)
- [voice + voice](voice_+_voice.md) (2 shared connections)
- [youtube_control](youtube_control.md) (1 shared connections)
- [tools + whatsapp_smart](tools_+_whatsapp_smart.md) (1 shared connections)
- [memory + rag_memory](memory_+_rag_memory.md) (1 shared connections)
- [smart_navigator + rag_memory](smart_navigator_+_rag_memory.md) (1 shared connections)
- [server + test_concurrency](server_+_test_concurrency.md) (1 shared connections)

## Source Files

- `app/services/tools.py`
- `app/services/voice.py`
- `scripts/test_hindi_tts.py`

## Audit Trail

- EXTRACTED: 21 (78%)
- INFERRED: 6 (22%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*