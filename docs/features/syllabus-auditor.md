# Syllabus auditor (YouTube playlist vs syllabus)

## Purpose
"Does this YouTube playlist cover my syllabus?" → per-topic coverage report (markdown) + spoken summary.

## Pipeline (`audit_playlist_syllabus(playlist_url, image_path)`)
Syllabus image → topics (vision model) → playlist video IDs → transcripts (youtube-transcript-api, skip missing) → 300-token chunks with 50 overlap → MiniLM embeddings → in-memory ChromaDB → cosine depth score per topic (`_coverage_level`) → top chunks verified by Groq 120b (`_llm_verify_topic`) → `_assemble_response` with timestamps.

## Triggers
"audit my playlist", "check playlist coverage", "gap analysis", … plus a playlist URL and an attached image (`[ATTACHED_FILE: …png]`), or an image filename searched in Desktop/Pictures/Downloads/Documents (chat.py).

## Gotchas
- Nothing is written to disk. The first run downloads the MiniLM model.
- Long playlists = many transcript fetches (slow, and may get rate-limited by YouTube).

## Graphify
`graphify explain "audit_playlist_syllabus"`

<!-- AUTO:BEGIN (scripts/refresh_docs.py) -->
## Files & symbols (auto-generated, line numbers are current)

- `app/services/syllabus_auditor.py` (1048 lines): syllabus_auditor.py — YouTube Playlist Syllabus Auditor (Jarvis Skill)
  L38 _EMBED_MODEL · L41 _get_groq_client() · L51 _get_embed_model() · L69 _load_image_as_b64() · L88 _extract_syllabus_from_image() · L166 _extract_playlist_id() · L172 _fetch_playlist_video_ids() · L303 _fetch_transcript() · L361 _approx_token_count() · L366 _chunk_transcript() · L469 _embed_texts() · L484 _build_vector_store() · L541 _DEPTH_THRESHOLDS · L549 _coverage_level() · L559 _score_topic_coverage() · L627 _format_timestamp() · L638 _llm_verify_topic() · L733 _DEPTH_EMOJI · L740 _DEPTH_LABEL · L748 _assemble_response() · L908 audit_playlist_syllabus()
<!-- AUTO:END -->
