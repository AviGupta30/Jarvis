# voice + tools

> 19 nodes · cohesion 0.12

## Key Concepts

- **speak_text()** (10 connections) — `app/services/voice.py`
- **SentenceSplitter** (9 connections) — `app/services/voice.py`
- **set_reminder()** (7 connections) — `app/services/tools.py`
- **test_hindi_tts.py** (6 connections) — `scripts/test_hindi_tts.py`
- **speak_stream()** (5 connections) — `app/services/voice.py`
- **Gotchas** (5 connections) — `docs/features/voice.md`
- **preload_local_stt()** (4 connections) — `app/services/voice.py`
- **split_sentences()** (3 connections) — `app/services/voice.py`
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
- **Test language-adaptive TTS - plays English then Hindi to verify both engines…** (1 connections) — `scripts/test_hindi_tts.py`

## Relationships

- [voice](voice.md) (9 shared connections)
- [tools](tools.md) (3 shared connections)
- [voice + voice](voice_+_voice.md) (2 shared connections)
- [youtube_control + youtube_player](youtube_control_+_youtube_player.md) (1 shared connections)
- [voice_agent](voice_agent.md) (1 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (1 shared connections)
- [social_content_manager + content-tools](social_content_manager_+_content-tools.md) (1 shared connections)
- [safe_executor + refresh_docs](safe_executor_+_refresh_docs.md) (1 shared connections)

## Source Files

- `app/services/tools.py`
- `app/services/voice.py`
- `docs/features/voice.md`
- `scripts/test_hindi_tts.py`

## Audit Trail

- EXTRACTED: 30 (75%)
- INFERRED: 10 (25%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*