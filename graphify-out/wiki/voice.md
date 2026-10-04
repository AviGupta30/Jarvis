# voice

> 35 nodes · cohesion 0.10

## Key Concepts

- **voice.py** (57 connections) — `app/services/voice.py`
- **transcribe_pcm()** (12 connections) — `app/services/voice.py`
- **transcribe_audio()** (8 connections) — `app/services/voice.py`
- **_finish()** (7 connections) — `app/services/voice.py`
- **ndarray** (6 connections)
- **_synth_edge()** (6 connections) — `app/services/voice.py`
- **loanword_ratio()** (5 connections) — `app/services/hinglish_normalizer.py`
- **_synthesize()** (5 connections) — `app/services/voice.py`
- **_transcribe_groq()** (5 connections) — `app/services/voice.py`
- **_transcribe_local_sync()** (5 connections) — `app/services/voice.py`
- **Transcript** (5 connections) — `app/services/voice.py`
- **_groq_once()** (4 connections) — `app/services/voice.py`
- **_transcribe_local()** (4 connections) — `app/services/voice.py`
- **translate_for_speech()** (4 connections) — `app/services/voice.py`
- **_get_groq()** (3 connections) — `app/services/voice.py`
- **groq_stt_available()** (3 connections) — `app/services/voice.py`
- **_load_whisper_model()** (3 connections) — `app/services/voice.py`
- **pcm_to_wav_bytes()** (3 connections) — `app/services/voice.py`
- **_sapi_sync()** (3 connections) — `app/services/voice.py`
- **.confident()** (3 connections) — `app/services/voice.py`
- **_clean_transcript()** (2 connections) — `app/services/voice.py`
- **_load()** (2 connections) — `app/services/voice.py`
- **_seg_get()** (2 connections) — `app/services/voice.py`
- **_voice_for()** (2 connections) — `app/services/voice.py`
- **Share of Devanagari words that are English loanwords ("ओपन क्रोम" → 1.0). High…** (1 connections) — `app/services/hinglish_normalizer.py`
- *... and 10 more nodes in this community*

## Relationships

- [voice](voice.md) (16 shared connections)
- [hinglish_normalizer](hinglish_normalizer.md) (8 shared connections)
- [voice + tools](voice_+_tools.md) (6 shared connections)
- [voice + voice](voice_+_voice.md) (5 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (3 shared connections)
- [assignment_answers](assignment_answers.md) (1 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (1 shared connections)
- [social_content_manager + content-tools](social_content_manager_+_content-tools.md) (1 shared connections)
- [smart_navigator + ssml_processor](smart_navigator_+_ssml_processor.md) (1 shared connections)
- [server](server.md) (1 shared connections)
- [message_reader + thread_extractor](message_reader_+_thread_extractor.md) (1 shared connections)
- [fontmatch + fonts](fontmatch_+_fonts.md) (1 shared connections)

## Source Files

- `app/services/hinglish_normalizer.py`
- `app/services/voice.py`

## Audit Trail

- EXTRACTED: 100 (91%)
- INFERRED: 10 (9%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*