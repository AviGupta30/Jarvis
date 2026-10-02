# Content humanizer & social content

## Purpose
Text generation helpers.

## Content humanizer (`content_humanizer.humanize_text_sync(text)`, tool `humanize_ai_content`)
Detect tone → structure rewrite prompt (Groq 120b) → reshape paragraphs → loop up to 3×: local per-sentence AI-probability scoring (`get_sentence_scores`, sentence-transformers) → rewrite flagged sentences (>0.70) → then `inject_micro_errors` + `inject_human_fingerprints` → `check_similarity` / `fact_check` against the original.

## Social content (`social_content_manager`)
`generate_social_content(idea, platform, tone, creativity, formality, smart_emojis, auto_hashtag, contextual_suggestions, target_audience)` and `refine_social_content(original_content, refinement_instruction, platform)`, Groq 120b via `build_prompt`.
Chat flow: "linkedin post / caption for / tweet about…" without preferences → asks "Would you like auto hashtags? Emojis? …". The next message is treated as the answer (chat.py checks the last bot message) → platform/tone/emoji/hashtag parsed from both messages.

## Related
The assignment humanizer (browser paraphrasers) is separate: see assignment.md.

## Graphify
`graphify explain "humanize_text_sync"` · `graphify explain "generate_social_content"`

<!-- AUTO:BEGIN (scripts/refresh_docs.py) -->
## Files & symbols (auto-generated, line numbers are current)

- `app/services/content_humanizer.py` (288 lines)
  L13 get_groq_client() · L21 get_similarity_model() · L27 BANNED_WORDS · L42 SIMILARITY_THRESHOLD · L44 PERPLEXITY_FORCING_PROMPT · L59 get_sentence_scores() · L89 detect_tone() · L94 build_structure_prompt() · L112 build_vocab_prompt() · L128 call_groq() · L142 rewrite_sentences() · L150 reshape_paragraphs() · L164 inject_micro_errors() · L192 inject_human_fingerprints() · L216 fact_check() · L222 check_similarity() · L228 humanize_text_sync()
- `app/services/social_content_manager.py` (190 lines)
  L7 build_prompt() · L68 call_llm() · L82 generate_social_content() · L157 refine_social_content()
<!-- AUTO:END -->
