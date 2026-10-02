# voice

> 40 nodes · cohesion 0.08

## Key Concepts

- **voice.py** (57 connections) — `app/services/voice.py`
- **transcribe_pcm()** (12 connections) — `app/services/voice.py`
- **SentenceSplitter** (9 connections) — `app/services/voice.py`
- **transcribe_audio()** (8 connections) — `app/services/voice.py`
- **_finish()** (7 connections) — `app/services/voice.py`
- **ndarray** (6 connections)
- **loanword_ratio()** (5 connections) — `app/services/hinglish_normalizer.py`
- **speak_stream()** (5 connections) — `app/services/voice.py`
- **_transcribe_groq()** (5 connections) — `app/services/voice.py`
- **_transcribe_local_sync()** (5 connections) — `app/services/voice.py`
- **Transcript** (5 connections) — `app/services/voice.py`
- **_groq_once()** (4 connections) — `app/services/voice.py`
- **preload_local_stt()** (4 connections) — `app/services/voice.py`
- **_transcribe_local()** (4 connections) — `app/services/voice.py`
- **translate_for_speech()** (4 connections) — `app/services/voice.py`
- **_get_groq()** (3 connections) — `app/services/voice.py`
- **groq_stt_available()** (3 connections) — `app/services/voice.py`
- **_load_whisper_model()** (3 connections) — `app/services/voice.py`
- **pcm_to_wav_bytes()** (3 connections) — `app/services/voice.py`
- **split_sentences()** (3 connections) — `app/services/voice.py`
- **.confident()** (3 connections) — `app/services/voice.py`
- **_clean_transcript()** (2 connections) — `app/services/voice.py`
- **_load()** (2 connections) — `app/services/voice.py`
- **_seg_get()** (2 connections) — `app/services/voice.py`
- **Share of Devanagari words that are English loanwords ("ओपन क्रोम" → 1.0). High…** (1 connections) — `app/services/hinglish_normalizer.py`
- *... and 15 more nodes in this community*

## Relationships

- [voice](voice.md) (18 shared connections)
- [hinglish_normalizer](hinglish_normalizer.md) (8 shared connections)
- [voice + context_classifier](voice_+_context_classifier.md) (7 shared connections)
- [voice + tools](voice_+_tools.md) (4 shared connections)
- [chat + llm](chat_+_llm.md) (2 shared connections)
- [voice_agent](voice_agent.md) (2 shared connections)
- [screen_reader](screen_reader.md) (1 shared connections)
- [rag_memory + memory](rag_memory_+_memory.md) (1 shared connections)
- [agentic_web](agentic_web.md) (1 shared connections)
- [ssml_processor + debug_wa](ssml_processor_+_debug_wa.md) (1 shared connections)
- [server + test_concurrency](server_+_test_concurrency.md) (1 shared connections)
- [whatsapp + dump_wa_ui](whatsapp_+_dump_wa_ui.md) (1 shared connections)

## Source Files

- `app/services/hinglish_normalizer.py`
- `app/services/voice.py`

## Audit Trail

- EXTRACTED: 104 (90%)
- INFERRED: 12 (10%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*