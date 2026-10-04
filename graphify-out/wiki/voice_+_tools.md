# voice + tools

> 17 nodes · cohesion 0.13

## Key Concepts

- **Voice: STT, TTS, wake word, clap wake, overlay** (12 connections) — `docs/features/voice.md`
- **speak_text()** (10 connections) — `app/services/voice.py`
- **set_reminder()** (7 connections) — `app/services/tools.py`
- **test_hindi_tts.py** (6 connections) — `scripts/test_hindi_tts.py`
- **Gotchas** (5 connections) — `docs/features/voice.md`
- **main()** (2 connections) — `scripts/test_hindi_tts.py`
- **Sets a reminder that Jarvis will speak after a given number of seconds.** (1 connections) — `app/services/tools.py`
- **_remind()** (1 connections) — `app/services/tools.py`
- **Speak a complete text. All sentences synthesise in parallel, play in order.** (1 connections) — `app/services/voice.py`
- **voice.md** (1 connections) — `docs/features/voice.md`
- **Config (`app/core/config.py` + env)** (1 connections) — `docs/features/voice.md`
- **Files & symbols (auto-generated, line numbers are current)** (1 connections) — `docs/features/voice.md`
- **Graphify** (1 connections) — `docs/features/voice.md`
- **Measured (2026-09-30/10-01, i9-13900H, no GPU)** (1 connections) — `docs/features/voice.md`
- **Purpose** (1 connections) — `docs/features/voice.md`
- **Server-side tripwire** (1 connections) — `docs/features/voice.md`
- **Test language-adaptive TTS - plays English then Hindi to verify both engines…** (1 connections) — `scripts/test_hindi_tts.py`

## Relationships

- [voice](voice.md) (7 shared connections)
- [tools + window_layout](tools_+_window_layout.md) (3 shared connections)
- [jarvis_overlay + prompt_overlay](jarvis_overlay_+_prompt_overlay.md) (2 shared connections)
- [youtube_player](youtube_player.md) (1 shared connections)
- [hinglish_normalizer](hinglish_normalizer.md) (1 shared connections)
- [llm + context_classifier](llm_+_context_classifier.md) (1 shared connections)
- [voice + context_classifier](voice_+_context_classifier.md) (1 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (1 shared connections)

## Source Files

- `app/services/tools.py`
- `app/services/voice.py`
- `docs/features/voice.md`
- `scripts/test_hindi_tts.py`

## Audit Trail

- EXTRACTED: 27 (77%)
- INFERRED: 8 (23%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*