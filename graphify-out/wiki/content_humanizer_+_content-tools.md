# content_humanizer + content-tools

> 31 nodes · cohesion 0.11

## Key Concepts

- **content_humanizer.py** (23 connections) — `app/services/content_humanizer.py`
- **humanize_text_sync()** (13 connections) — `app/services/content_humanizer.py`
- **Content humanizer & social content** (7 connections) — `docs/features/content-tools.md`
- **Content humanizer (`content_humanizer.humanize_text_sync(text)`, tool `humanize_ai_content`)** (6 connections) — `docs/features/content-tools.md`
- **rewrite_sentences()** (5 connections) — `app/services/content_humanizer.py`
- **test_humanizer.py** (5 connections) — `scripts/test_humanizer.py`
- **call_groq()** (4 connections) — `app/services/content_humanizer.py`
- **check_similarity()** (4 connections) — `app/services/content_humanizer.py`
- **get_sentence_scores()** (4 connections) — `app/services/content_humanizer.py`
- **inject_micro_errors()** (4 connections) — `app/services/content_humanizer.py`
- **random** (4 connections)
- **fact_check()** (3 connections) — `app/services/content_humanizer.py`
- **inject_human_fingerprints()** (3 connections) — `app/services/content_humanizer.py`
- **build_structure_prompt()** (2 connections) — `app/services/content_humanizer.py`
- **build_vocab_prompt()** (2 connections) — `app/services/content_humanizer.py`
- **detect_tone()** (2 connections) — `app/services/content_humanizer.py`
- **get_groq_client()** (2 connections) — `app/services/content_humanizer.py`
- **get_similarity_model()** (2 connections) — `app/services/content_humanizer.py`
- **reshape_paragraphs()** (2 connections) — `app/services/content_humanizer.py`
- **Social content (`social_content_manager`)** (2 connections) — `docs/features/content-tools.md`
- **test()** (2 connections) — `scripts/test_humanizer.py`
- **Helper to rewrite a batch of sentences via Groq.** (1 connections) — `app/services/content_humanizer.py`
- **Inject subtle, natural human imperfections post-rewrite.** (1 connections) — `app/services/content_humanizer.py`
- **Local, keyless per-sentence AI probability detector.** (1 connections) — `app/services/content_humanizer.py`
- **content-tools.md** (1 connections) — `docs/features/content-tools.md`
- *... and 6 more nodes in this community*

## Relationships

- [social_content_manager + ui_inspector](social_content_manager_+_ui_inspector.md) (3 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (2 shared connections)
- [server + protocol](server_+_protocol.md) (2 shared connections)
- [web_search + tools](web_search_+_tools.md) (1 shared connections)
- [acoustic_tripwire](acoustic_tripwire.md) (1 shared connections)
- [youtube_player](youtube_player.md) (1 shared connections)
- [voice_agent](voice_agent.md) (1 shared connections)

## Source Files

- `app/services/content_humanizer.py`
- `docs/features/content-tools.md`
- `scripts/test_humanizer.py`

## Audit Trail

- EXTRACTED: 55 (90%)
- INFERRED: 6 (10%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*