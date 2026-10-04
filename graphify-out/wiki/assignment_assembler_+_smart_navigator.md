# assignment_assembler + smart_navigator

> 20 nodes · cohesion 0.13

## Key Concepts

- **re** (60 connections)
- **assignment_assembler.py** (9 connections) — `app/services/assignment_assembler.py`
- **smart_navigator.py** (9 connections) — `app/services/smart_navigator.py`
- **assemble_assignment()** (8 connections) — `app/services/assignment_assembler.py`
- **_llm_extract()** (4 connections) — `app/services/smart_navigator.py`
- **_parse_qa_json()** (3 connections) — `app/services/assignment_assembler.py`
- **_get_api_key()** (3 connections) — `app/services/smart_navigator.py`
- **debug_wa.py** (3 connections) — `debug_wa.py`
- **_create_powerpoint()** (2 connections) — `app/services/assignment_assembler.py`
- **_create_word_doc()** (2 connections) — `app/services/assignment_assembler.py`
- **detect_whatsapp_call()** (2 connections) — `debug_wa.py`
- **detect_whatsapp_send()** (2 connections) — `debug_wa.py`
- **Jarvis Assignment Tool — Phase 4: Document Assembly…** (1 connections) — `app/services/assignment_assembler.py`
- **Assemble the extracted/humanized questions and answers into a formatted…** (1 connections) — `app/services/assignment_assembler.py`
- **Extract and parse the JSON array from the input string.** (1 connections) — `app/services/assignment_assembler.py`
- **smart_navigator.py — Isolated Smart Web Navigator for Jarvis…** (1 connections) — `app/services/smart_navigator.py`
- **Attempt to find the GROQ API key safely.** (1 connections) — `app/services/smart_navigator.py`
- **Pass scraped text through LLM for structured extraction.** (1 connections) — `app/services/smart_navigator.py`
- **patch.py** (1 connections) — `patch.py`
- **patch_chart_engine.py** (1 connections) — `patch_chart_engine.py`

## Relationships

- [benchmark + download_kokoro](benchmark_+_download_kokoro.md) (4 shared connections)
- [assignment_tool + assignment_pipeline](assignment_tool_+_assignment_pipeline.md) (4 shared connections)
- [whatsapp_smart + tools](whatsapp_smart_+_tools.md) (4 shared connections)
- [style_profiler + reply_generator](style_profiler_+_reply_generator.md) (4 shared connections)
- [tools](tools.md) (2 shared connections)
- [browser_tool](browser_tool.md) (2 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (2 shared connections)
- [spotify_service + media_sessions](spotify_service_+_media_sessions.md) (2 shared connections)
- [test_lru](test_lru.md) (1 shared connections)
- [dump_wa_ui + test_wa](dump_wa_ui_+_test_wa.md) (1 shared connections)
- [planner + dynamic_skill](planner_+_dynamic_skill.md) (1 shared connections)
- [agentic_web](agentic_web.md) (1 shared connections)

## Source Files

- `app/services/assignment_assembler.py`
- `app/services/smart_navigator.py`
- `debug_wa.py`
- `patch.py`
- `patch_chart_engine.py`

## Audit Trail

- EXTRACTED: 90 (99%)
- INFERRED: 1 (1%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*