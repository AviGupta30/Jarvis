# voice

> 59 nodes · cohesion 0.06

## Key Concepts

- **voice.py** (57 connections) — `app/services/voice.py`
- **transcribe_pcm()** (12 connections) — `app/services/voice.py`
- **Clip** (11 connections) — `app/services/voice.py`
- **start_clip()** (10 connections) — `app/services/voice.py`
- **hinglish_normalizer.py** (9 connections) — `app/services/hinglish_normalizer.py`
- **transcribe_audio()** (8 connections) — `app/services/voice.py`
- **devanagari_to_hinglish()** (7 connections) — `app/services/hinglish_normalizer.py`
- **_finish()** (7 connections) — `app/services/voice.py`
- **strip_markdown()** (6 connections) — `app/services/hinglish_normalizer.py`
- **ndarray** (6 connections)
- **_synth_edge()** (6 connections) — `app/services/voice.py`
- **loanword_ratio()** (5 connections) — `app/services/hinglish_normalizer.py`
- **_synthesize()** (5 connections) — `app/services/voice.py`
- **_transcribe_groq()** (5 connections) — `app/services/voice.py`
- **_transcribe_local_sync()** (5 connections) — `app/services/voice.py`
- **Transcript** (5 connections) — `app/services/voice.py`
- **normalize_for_tts()** (4 connections) — `app/services/hinglish_normalizer.py`
- **_groq_once()** (4 connections) — `app/services/voice.py`
- **_norm_words()** (4 connections) — `app/services/voice.py`
- **route_language()** (4 connections) — `app/services/voice.py`
- **_transcribe_local()** (4 connections) — `app/services/voice.py`
- **translate_for_speech()** (4 connections) — `app/services/voice.py`
- **STT (`voice.transcribe_pcm` → `Transcript`)** (4 connections) — `docs/features/voice.md`
- **_translit_dev_word()** (3 connections) — `app/services/hinglish_normalizer.py`
- **_get_groq()** (3 connections) — `app/services/voice.py`
- *... and 34 more nodes in this community*

## Relationships

- [voice](voice.md) (15 shared connections)
- [context_classifier + personality](context_classifier_+_personality.md) (7 shared connections)
- [voice + tools](voice_+_tools.md) (7 shared connections)
- [social_content_manager + ui_inspector](social_content_manager_+_ui_inspector.md) (5 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (2 shared connections)
- [server + protocol](server_+_protocol.md) (1 shared connections)
- [message_reader + reply_generator](message_reader_+_reply_generator.md) (1 shared connections)
- [acoustic_tripwire](acoustic_tripwire.md) (1 shared connections)
- [style_profiler + refresh_docs](style_profiler_+_refresh_docs.md) (1 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (1 shared connections)
- [ppt_image_engine](ppt_image_engine.md) (1 shared connections)
- [voice_agent](voice_agent.md) (1 shared connections)

## Source Files

- `app/services/hinglish_normalizer.py`
- `app/services/voice.py`
- `docs/features/voice.md`

## Audit Trail

- EXTRACTED: 135 (92%)
- INFERRED: 11 (8%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*