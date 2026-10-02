# syllabus_auditor

> 41 nodes · cohesion 0.05

## Key Concepts

- **audit_playlist_syllabus()** (11 connections) — `app/services/syllabus_auditor.py`
- **Syllabus auditor (YouTube playlist vs syllabus)** (7 connections) — `docs/features/syllabus-auditor.md`
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
- **Extract the playlist ID from any standard YouTube playlist URL.** (1 connections) — `app/services/syllabus_auditor.py`
- **Retrieve all video IDs (and titles where available) from a YouTube playlist.…** (1 connections) — `app/services/syllabus_auditor.py`
- **Fetch auto-generated or manual captions for a single YouTube video. Tries…** (1 connections) — `app/services/syllabus_auditor.py`
- **Approximate token count: ~0.75 tokens per word (safe undercount for chunking).** (1 connections) — `app/services/syllabus_auditor.py`
- **Split a transcript into overlapping chunks for semantic search. Strategy: -…** (1 connections) — `app/services/syllabus_auditor.py`
- **Return a Groq client using the shared GROQ_API_KEY from Jarvis settings.** (1 connections) — `app/services/syllabus_auditor.py`
- *... and 16 more nodes in this community*

## Relationships

- [social_content_manager + ui_inspector](social_content_manager_+_ui_inspector.md) (17 shared connections)
- [tools](tools.md) (1 shared connections)

## Source Files

- `app/services/syllabus_auditor.py`
- `docs/features/syllabus-auditor.md`

## Audit Trail

- EXTRACTED: 59 (94%)
- INFERRED: 4 (6%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*