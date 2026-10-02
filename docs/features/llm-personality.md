# LLM layer & Jarvis personality

## Purpose
All chat LLM calls and the JARVIS persona.

## Models (Groq)
- `llm.FAST_MODEL` = `openai/gpt-oss-20b`: router, simple replies, history compression.
- `llm.DEEP_MODEL` = `openai/gpt-oss-120b`: when `_is_complex_response` (tool result > 500 chars, or explain/why/debug/plan… wording).
- `settings.GROQ_VISION_MODEL` (default `qwen/qwen3.8-27b`): any image input. gpt-oss rejects images.
- Other modules create their own Groq clients with hardcoded model strings (grep `model=`).

## Flow of `generate_chat_response`
`context_classifier.classify_context` (hour, mood, language en/hinglish/hindi, urgency, topic) → `personality.get_context_aware_prompt` → + `memory_tool` facts → + FAISS recall (top 5, ≥0.30) → `_maybe_compress_history` (>15 msgs → summary) → + tool result block (≤2000 chars) → history → stream.

## Router
`check_for_tool_intent`: JSON mode, temp 0, `max_tokens=600` + `reasoning_effort="low"` (gpt-oss hidden reasoning eats tokens; 150 caused empty output). Returns None on error/rate limit.

## Gotchas
- Groq free tier: 8,000 TPM on gpt-oss-20b. The router prompt is ~2.4k tokens, so bursts give 429s.
- The persona forbids Devanagari output (TTS crashes). Hindi input gets Romanised Hinglish.
- History is a global deque(20) persisted to `app/memory/session.json` (git-ignored).

## Graphify
`graphify explain "generate_chat_response"` · `graphify explain "get_context_aware_prompt"`

<!-- AUTO:BEGIN (scripts/refresh_docs.py) -->
## Files & symbols (auto-generated, line numbers are current)

- `app/services/llm.py` (366 lines): llm.py — Jarvis LLM Brain
  L29 FAST_MODEL · L30 DEEP_MODEL · L34 _TPM_DEFAULT · L37 _parse_reset() · L47 _track_limits() · L62 _room() · L69 _other() · L73 pick_model() · L82 _is_rate_limit() · L87 _mark_exhausted() · L102 _groq_generate() · L139 _is_complex_response() · L159 _load_session() · L170 _save_session() · L182 check_for_tool_intent() · L213 _reply_language_note() · L232 generate_chat_response() · L336 _maybe_compress_history()
- `app/services/personality.py` (264 lines): personality.py — Jarvis Character & Personality Engine
  L13 JARVIS_SYSTEM_PROMPT · L72 TOOL_ROUTER_PROMPT · L212 get_context_aware_prompt()
- `app/services/context_classifier.py` (163 lines): context_classifier.py — Jarvis Situational Awareness
  L43 detect_language() · L73 classify_context()
- `app/core/config.py` (30 lines)
  L6 class Settings
<!-- AUTO:END -->
