# voice + tools

> 18 nodes · cohesion 0.12

## Key Concepts

- **speak_text()** (10 connections) — `app/services/voice.py`
- **SentenceSplitter** (9 connections) — `app/services/voice.py`
- **set_reminder()** (7 connections) — `app/services/tools.py`
- **speak_stream()** (5 connections) — `app/services/voice.py`
- **Gotchas** (5 connections) — `docs/features/voice.md`
- **preload_local_stt()** (4 connections) — `app/services/voice.py`
- **split_sentences()** (3 connections) — `app/services/voice.py`
- **_load()** (2 connections) — `app/services/voice.py`
- **main()** (2 connections) — `scripts/test_hindi_tts.py`
- **Sets a reminder that Jarvis will speak after a given number of seconds.** (1 connections) — `app/services/tools.py`
- **_remind()** (1 connections) — `app/services/tools.py`
- **Load the local Whisper models in the background (voice agent startup).** (1 connections) — `app/services/voice.py`
- **Feed streamed tokens; get back speakable sentences as early as possible.** (1 connections) — `app/services/voice.py`
- **Speak a complete text. All sentences synthesise in parallel, play in order.** (1 connections) — `app/services/voice.py`
- **Speak an async generator of text chunks, sentence by sentence, pipelined.** (1 connections) — `app/services/voice.py`
- **.feed()** (1 connections) — `app/services/voice.py`
- **.flush()** (1 connections) — `app/services/voice.py`
- **.__init__()** (1 connections) — `app/services/voice.py`

## Relationships

- [voice](voice.md) (10 shared connections)
- [tools](tools.md) (3 shared connections)
- [social_content_manager + ui_inspector](social_content_manager_+_ui_inspector.md) (2 shared connections)
- [youtube_player](youtube_player.md) (1 shared connections)
- [voice_agent](voice_agent.md) (1 shared connections)
- [context_classifier + personality](context_classifier_+_personality.md) (1 shared connections)

## Source Files

- `app/services/tools.py`
- `app/services/voice.py`
- `docs/features/voice.md`
- `scripts/test_hindi_tts.py`

## Audit Trail

- EXTRACTED: 27 (73%)
- INFERRED: 10 (27%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*