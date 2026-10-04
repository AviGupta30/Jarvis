# smart_navigator + ssml_processor

> 21 nodes · cohesion 0.10

## Key Concepts

- **re** (59 connections)
- **smart_navigator.py** (9 connections) — `app/services/smart_navigator.py`
- **_llm_extract()** (4 connections) — `app/services/smart_navigator.py`
- **ssml_processor.py** (4 connections) — `app/services/ssml_processor.py`
- **_get_api_key()** (3 connections) — `app/services/smart_navigator.py`
- **_resolve_url()** (3 connections) — `app/services/smart_navigator.py`
- **debug_wa.py** (3 connections) — `debug_wa.py`
- **add_human_prosody()** (2 connections) — `app/services/ssml_processor.py`
- **strip_ssml()** (2 connections) — `app/services/ssml_processor.py`
- **detect_whatsapp_call()** (2 connections) — `debug_wa.py`
- **detect_whatsapp_send()** (2 connections) — `debug_wa.py`
- **playwright_sync_api** (2 connections)
- **smart_navigator.py — Isolated Smart Web Navigator for Jarvis…** (1 connections) — `app/services/smart_navigator.py`
- **Attempt to find the GROQ API key safely.** (1 connections) — `app/services/smart_navigator.py`
- **Pass scraped text through LLM for structured extraction.** (1 connections) — `app/services/smart_navigator.py`
- **Resolve a verbal site name like 'unstop' to a URL like 'https://unstop.com'.** (1 connections) — `app/services/smart_navigator.py`
- **ssml_processor.py — Human Prosody Pre-processor…** (1 connections) — `app/services/ssml_processor.py`
- **Add natural speech prosody to plain text. Args: text: Plain text (already…** (1 connections) — `app/services/ssml_processor.py`
- **Remove all SSML tags from text — used when falling back to edge-tts which does…** (1 connections) — `app/services/ssml_processor.py`
- **patch.py** (1 connections) — `patch.py`
- **patch_chart_engine.py** (1 connections) — `patch_chart_engine.py`

## Relationships

- [whatsapp_smart + tools](whatsapp_smart_+_tools.md) (4 shared connections)
- [message_reader + thread_extractor](message_reader_+_thread_extractor.md) (3 shared connections)
- [browser_tool](browser_tool.md) (2 shared connections)
- [assignment_humanizer + task_ledger](assignment_humanizer_+_task_ledger.md) (2 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (2 shared connections)
- [style_profiler + reply_generator](style_profiler_+_reply_generator.md) (2 shared connections)
- [social_content_manager + content-tools](social_content_manager_+_content-tools.md) (1 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (1 shared connections)
- [agentic_web + email-calendar](agentic_web_+_email-calendar.md) (1 shared connections)
- [assignment_answers](assignment_answers.md) (1 shared connections)
- [assignment_assembler](assignment_assembler.md) (1 shared connections)
- [assignment_pipeline](assignment_pipeline.md) (1 shared connections)

## Source Files

- `app/services/smart_navigator.py`
- `app/services/ssml_processor.py`
- `debug_wa.py`
- `patch.py`
- `patch_chart_engine.py`

## Audit Trail

- EXTRACTED: 82 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*