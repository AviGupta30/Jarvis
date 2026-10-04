# content_humanizer + content-tools

> 37 nodes · cohesion 0.09

## Key Concepts

- **content_humanizer.py** (23 connections) — `app/services/content_humanizer.py`
- **humanize_text_sync()** (13 connections) — `app/services/content_humanizer.py`
- **Content humanizer & social content** (7 connections) — `docs/features/content-tools.md`
- **generate_social_content()** (6 connections) — `app/services/social_content_manager.py`
- **Content humanizer (`content_humanizer.humanize_text_sync(text)`, tool `humanize_ai_content`)** (6 connections) — `docs/features/content-tools.md`
- **rewrite_sentences()** (5 connections) — `app/services/content_humanizer.py`
- **refine_social_content()** (5 connections) — `app/services/social_content_manager.py`
- **test_humanizer.py** (5 connections) — `scripts/test_humanizer.py`
- **call_groq()** (4 connections) — `app/services/content_humanizer.py`
- **check_similarity()** (4 connections) — `app/services/content_humanizer.py`
- **get_sentence_scores()** (4 connections) — `app/services/content_humanizer.py`
- **inject_micro_errors()** (4 connections) — `app/services/content_humanizer.py`
- **build_prompt()** (4 connections) — `app/services/social_content_manager.py`
- **call_llm()** (4 connections) — `app/services/social_content_manager.py`
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
- *... and 12 more nodes in this community*

## Relationships

- [voice_agent + download_kokoro](voice_agent_+_download_kokoro.md) (10 shared connections)
- [dynamic_skill + planner](dynamic_skill_+_planner.md) (2 shared connections)
- [tools](tools.md) (2 shared connections)
- [dag_executor + planner](dag_executor_+_planner.md) (1 shared connections)

## Source Files

- `app/services/content_humanizer.py`
- `app/services/social_content_manager.py`
- `docs/features/content-tools.md`
- `scripts/test_humanizer.py`

## Audit Trail

- EXTRACTED: 62 (86%)
- INFERRED: 10 (14%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*