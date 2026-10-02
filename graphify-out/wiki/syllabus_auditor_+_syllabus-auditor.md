# syllabus_auditor + syllabus-auditor

> 51 nodes · cohesion 0.06

## Key Concepts

- **rag_memory.py** (27 connections) — `app/services/rag_memory.py`
- **syllabus_auditor.py** (25 connections) — `app/services/syllabus_auditor.py`
- **logging** (14 connections)
- **audit_playlist_syllabus()** (11 connections) — `app/services/syllabus_auditor.py`
- **Syllabus auditor (YouTube playlist vs syllabus)** (7 connections) — `docs/features/syllabus-auditor.md`
- **_llm_verify_topic()** (6 connections) — `app/services/syllabus_auditor.py`
- **_assemble_response()** (5 connections) — `app/services/syllabus_auditor.py`
- **_embed_texts()** (5 connections) — `app/services/syllabus_auditor.py`
- **_extract_syllabus_from_image()** (5 connections) — `app/services/syllabus_auditor.py`
- **_score_topic_coverage()** (5 connections) — `app/services/syllabus_auditor.py`
- **_save_faiss_index_async()** (4 connections) — `app/services/rag_memory.py`
- **_build_vector_store()** (4 connections) — `app/services/syllabus_auditor.py`
- **_chunk_transcript()** (4 connections) — `app/services/syllabus_auditor.py`
- **_fetch_playlist_video_ids()** (4 connections) — `app/services/syllabus_auditor.py`
- **_format_timestamp()** (4 connections) — `app/services/syllabus_auditor.py`
- **_get_groq_client()** (4 connections) — `app/services/syllabus_auditor.py`
- **Pipeline (`audit_playlist_syllabus(playlist_url, image_path)`)** (4 connections) — `docs/features/syllabus-auditor.md`
- **_save_faiss_index()** (3 connections) — `app/services/rag_memory.py`
- **_approx_token_count()** (3 connections) — `app/services/syllabus_auditor.py`
- **_coverage_level()** (3 connections) — `app/services/syllabus_auditor.py`
- **_extract_playlist_id()** (3 connections) — `app/services/syllabus_auditor.py`
- **_fetch_transcript()** (3 connections) — `app/services/syllabus_auditor.py`
- **_get_embed_model()** (3 connections) — `app/services/syllabus_auditor.py`
- **_load_image_as_b64()** (3 connections) — `app/services/syllabus_auditor.py`
- **uuid** (3 connections)
- *... and 26 more nodes in this community*

## Relationships

- [rag_memory + memory](rag_memory_+_memory.md) (11 shared connections)
- [assignment_tool + safe_executor](assignment_tool_+_safe_executor.md) (8 shared connections)
- [mysql_db + rag_memory](mysql_db_+_rag_memory.md) (5 shared connections)
- [persistence + server](persistence_+_server.md) (3 shared connections)
- [ui_inspector + lru](ui_inspector_+_lru.md) (2 shared connections)
- [voice_agent + acoustic_tripwire](voice_agent_+_acoustic_tripwire.md) (2 shared connections)
- [chat](chat.md) (1 shared connections)
- [memory](memory.md) (1 shared connections)
- [calendar_tool](calendar_tool.md) (1 shared connections)
- [agents + tool_runner](agents_+_tool_runner.md) (1 shared connections)
- [tools](tools.md) (1 shared connections)
- [main + screen_vision](main_+_screen_vision.md) (1 shared connections)

## Source Files

- `app/services/rag_memory.py`
- `app/services/syllabus_auditor.py`
- `docs/features/syllabus-auditor.md`

## Audit Trail

- EXTRACTED: 110 (96%)
- INFERRED: 5 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*