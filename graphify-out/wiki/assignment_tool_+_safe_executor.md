# assignment_tool + safe_executor

> 76 nodes · cohesion 0.05

## Key Concepts

- **re** (52 connections)
- **os** (50 connections)
- **time** (46 connections)
- **json** (41 connections)
- **sys** (29 connections)
- **pathlib** (28 connections)
- **assignment_tool.py** (25 connections) — `app/services/assignment_tool.py`
- **assignment_answers.py** (22 connections) — `app/services/assignment_answers.py`
- **safe_executor.py** (22 connections) — `app/services/safe_executor.py`
- **assignment_humanizer.py** (20 connections) — `app/services/assignment_humanizer.py`
- **config.py** (19 connections) — `app/core/config.py`
- **dynamic_skill.py** (18 connections) — `app/services/dynamic_skill.py`
- **benchmark.py** (16 connections) — `neural_cache/benchmark.py`
- **prompt_overlay.py** (12 connections) — `app/services/prompt_overlay.py`
- **execute_safe()** (11 connections) — `app/services/safe_executor.py`
- **groq** (11 connections)
- **jarvis_overlay.py** (11 connections) — `scripts/jarvis_overlay.py`
- **io** (10 connections)
- **media_state.py** (9 connections) — `app/services/media_state.py`
- **base64** (9 connections)
- **nlp_extractor.py** (8 connections) — `app/services/nlp_extractor.py`
- **SecurityError** (8 connections) — `app/services/safe_executor.py`
- **_split_with_subquestions()** (7 connections) — `app/services/assignment_tool.py`
- **research_pipeline.py** (7 connections) — `app/services/research_pipeline.py`
- **SafetyVisitor** (6 connections) — `app/services/safe_executor.py`
- *... and 51 more nodes in this community*

## Relationships

- [assignment_pipeline + assignment_tool](assignment_pipeline_+_assignment_tool.md) (22 shared connections)
- [message_reader + whatsapp](message_reader_+_whatsapp.md) (17 shared connections)
- [dag_executor + planner](dag_executor_+_planner.md) (15 shared connections)
- [voice_agent + acoustic_tripwire](voice_agent_+_acoustic_tripwire.md) (14 shared connections)
- [assignment_humanizer](assignment_humanizer.md) (12 shared connections)
- [ppt_tool + ppt_image_engine](ppt_tool_+_ppt_image_engine.md) (10 shared connections)
- [persistence + server](persistence_+_server.md) (10 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (9 shared connections)
- [assignment_answers](assignment_answers.md) (9 shared connections)
- [screen_reader](screen_reader.md) (8 shared connections)
- [gmail_tool + memory_tool](gmail_tool_+_memory_tool.md) (8 shared connections)
- [syllabus_auditor + syllabus-auditor](syllabus_auditor_+_syllabus-auditor.md) (8 shared connections)

## Source Files

- `app/core/config.py`
- `app/services/assignment_answers.py`
- `app/services/assignment_humanizer.py`
- `app/services/assignment_tool.py`
- `app/services/dynamic_skill.py`
- `app/services/media_state.py`
- `app/services/nlp_extractor.py`
- `app/services/prompt_overlay.py`
- `app/services/research_pipeline.py`
- `app/services/safe_executor.py`
- `neural_cache/benchmark.py`
- `patch.py`
- `patch_chart_engine.py`
- `patch_window.py`
- `scripts/jarvis_overlay.py`
- `test_exec.py`

## Audit Trail

- EXTRACTED: 452 (99%)
- INFERRED: 6 (1%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*