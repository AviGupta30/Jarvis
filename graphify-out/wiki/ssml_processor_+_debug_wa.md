# ssml_processor + debug_wa

> 12 nodes · cohesion 0.18

## Key Concepts

- **re** (52 connections)
- **ssml_processor.py** (4 connections) — `app/services/ssml_processor.py`
- **debug_wa.py** (3 connections) — `debug_wa.py`
- **add_human_prosody()** (2 connections) — `app/services/ssml_processor.py`
- **strip_ssml()** (2 connections) — `app/services/ssml_processor.py`
- **detect_whatsapp_call()** (2 connections) — `debug_wa.py`
- **detect_whatsapp_send()** (2 connections) — `debug_wa.py`
- **ssml_processor.py — Human Prosody Pre-processor…** (1 connections) — `app/services/ssml_processor.py`
- **Add natural speech prosody to plain text. Args: text: Plain text (already…** (1 connections) — `app/services/ssml_processor.py`
- **Remove all SSML tags from text — used when falling back to edge-tts which does…** (1 connections) — `app/services/ssml_processor.py`
- **patch.py** (1 connections) — `patch.py`
- **patch_chart_engine.py** (1 connections) — `patch_chart_engine.py`

## Relationships

- [browser_tool + smart_navigator](browser_tool_+_smart_navigator.md) (2 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (2 shared connections)
- [chat + llm](chat_+_llm.md) (1 shared connections)
- [agentic_web](agentic_web.md) (1 shared connections)
- [assignment_answers](assignment_answers.md) (1 shared connections)
- [assignment_assembler](assignment_assembler.md) (1 shared connections)
- [assignment_humanizer](assignment_humanizer.md) (1 shared connections)
- [assignment_pipeline](assignment_pipeline.md) (1 shared connections)
- [assignment_tool](assignment_tool.md) (1 shared connections)
- [content_humanizer](content_humanizer.md) (1 shared connections)
- [dsa_enforcer + dsa-mode](dsa_enforcer_+_dsa-mode.md) (1 shared connections)
- [file_ops](file_ops.md) (1 shared connections)

## Source Files

- `app/services/ssml_processor.py`
- `debug_wa.py`
- `patch.py`
- `patch_chart_engine.py`

## Audit Trail

- EXTRACTED: 60 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*