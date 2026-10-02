# syllabus_auditor

> 36 nodes · cohesion 0.09

## Key Concepts

- **syllabus_auditor.py** (25 connections) — `app/services/syllabus_auditor.py`
- **audit_playlist_syllabus()** (11 connections) — `app/services/syllabus_auditor.py`
- **_llm_verify_topic()** (6 connections) — `app/services/syllabus_auditor.py`
- **_assemble_response()** (5 connections) — `app/services/syllabus_auditor.py`
- **_embed_texts()** (5 connections) — `app/services/syllabus_auditor.py`
- **_extract_syllabus_from_image()** (5 connections) — `app/services/syllabus_auditor.py`
- **_score_topic_coverage()** (5 connections) — `app/services/syllabus_auditor.py`
- **_build_vector_store()** (4 connections) — `app/services/syllabus_auditor.py`
- **_chunk_transcript()** (4 connections) — `app/services/syllabus_auditor.py`
- **_fetch_playlist_video_ids()** (4 connections) — `app/services/syllabus_auditor.py`
- **_format_timestamp()** (4 connections) — `app/services/syllabus_auditor.py`
- **_get_groq_client()** (4 connections) — `app/services/syllabus_auditor.py`
- **Pipeline (`audit_playlist_syllabus(playlist_url, image_path)`)** (4 connections) — `docs/features/syllabus-auditor.md`
- **_approx_token_count()** (3 connections) — `app/services/syllabus_auditor.py`
- **_coverage_level()** (3 connections) — `app/services/syllabus_auditor.py`
- **_extract_playlist_id()** (3 connections) — `app/services/syllabus_auditor.py`
- **_fetch_transcript()** (3 connections) — `app/services/syllabus_auditor.py`
- **_get_embed_model()** (3 connections) — `app/services/syllabus_auditor.py`
- **_load_image_as_b64()** (3 connections) — `app/services/syllabus_auditor.py`
- **syllabus_auditor.py — YouTube Playlist Syllabus Auditor (Jarvis Skill)…** (1 connections) — `app/services/syllabus_auditor.py`
- **Extract the playlist ID from any standard YouTube playlist URL.** (1 connections) — `app/services/syllabus_auditor.py`
- **Retrieve all video IDs (and titles where available) from a YouTube playlist.…** (1 connections) — `app/services/syllabus_auditor.py`
- **Fetch auto-generated or manual captions for a single YouTube video. Tries…** (1 connections) — `app/services/syllabus_auditor.py`
- **Approximate token count: ~0.75 tokens per word (safe undercount for chunking).** (1 connections) — `app/services/syllabus_auditor.py`
- **Split a transcript into overlapping chunks for semantic search. Strategy: -…** (1 connections) — `app/services/syllabus_auditor.py`
- *... and 11 more nodes in this community*

## Relationships

- [agentic_web](agentic_web.md) (1 shared connections)
- [ssml_processor + debug_wa](ssml_processor_+_debug_wa.md) (1 shared connections)
- [screen_reader](screen_reader.md) (1 shared connections)
- [rag_memory + memory](rag_memory_+_memory.md) (1 shared connections)
- [whatsapp + dump_wa_ui](whatsapp_+_dump_wa_ui.md) (1 shared connections)
- [task_ledger + test_task_resumption](task_ledger_+_test_task_resumption.md) (1 shared connections)
- [reply_generator](reply_generator.md) (1 shared connections)
- [tools](tools.md) (1 shared connections)
- [syllabus-auditor](syllabus-auditor.md) (1 shared connections)

## Source Files

- `app/services/syllabus_auditor.py`
- `docs/features/syllabus-auditor.md`

## Audit Trail

- EXTRACTED: 61 (94%)
- INFERRED: 4 (6%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*