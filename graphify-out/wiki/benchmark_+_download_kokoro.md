# benchmark + download_kokoro

> 42 nodes · cohesion 0.06

## Key Concepts

- **os** (63 connections)
- **json** (50 connections)
- **sys** (30 connections)
- **config.py** (20 connections) — `app/core/config.py`
- **benchmark.py** (16 connections) — `neural_cache/benchmark.py`
- **replica_eval.py** (12 connections) — `scripts/replica_eval.py`
- **groq** (11 connections)
- **social_content_manager.py** (9 connections) — `app/services/social_content_manager.py`
- **nlp_extractor.py** (8 connections) — `app/services/nlp_extractor.py`
- **research_pipeline.py** (7 connections) — `app/services/research_pipeline.py`
- **JSONFileBaseline** (7 connections) — `neural_cache/benchmark.py`
- **main()** (7 connections) — `neural_cache/benchmark.py`
- **measure_throughput()** (4 connections) — `neural_cache/benchmark.py`
- **download_kokoro.py** (4 connections) — `scripts/download_kokoro.py`
- **test_agentic_web.py** (4 connections) — `test_agentic_web.py`
- **dotenv** (3 connections)
- **html** (3 connections)
- **measure_latency()** (3 connections) — `neural_cache/benchmark.py`
- **test_api.py** (3 connections) — `test_api.py`
- **urllib_request** (3 connections)
- **argparse** (2 connections)
- **glob** (2 connections)
- **download()** (2 connections) — `scripts/download_kokoro.py`
- **Settings** (1 connections) — `app/core/config.py`
- **nlp_extractor.py — LLM-Powered Fact & Entity Extractor…** (1 connections) — `app/services/nlp_extractor.py`
- *... and 17 more nodes in this community*

## Relationships

- [content_humanizer + content-tools](content_humanizer_+_content-tools.md) (8 shared connections)
- [planner + dynamic_skill](planner_+_dynamic_skill.md) (8 shared connections)
- [resume_builder](resume_builder.md) (8 shared connections)
- [server + persistence](server_+_persistence.md) (8 shared connections)
- [dump_wa_ui + test_wa](dump_wa_ui_+_test_wa.md) (8 shared connections)
- [rag_memory + memory](rag_memory_+_memory.md) (7 shared connections)
- [style_profiler + reply_generator](style_profiler_+_reply_generator.md) (7 shared connections)
- [assignment_tool + assignment_pipeline](assignment_tool_+_assignment_pipeline.md) (6 shared connections)
- [ppt_tool](ppt_tool.md) (6 shared connections)
- [storage + orchestrator](storage_+_orchestrator.md) (6 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (5 shared connections)
- [task_ledger + test_task_resumption](task_ledger_+_test_task_resumption.md) (5 shared connections)

## Source Files

- `app/core/config.py`
- `app/services/nlp_extractor.py`
- `app/services/research_pipeline.py`
- `app/services/social_content_manager.py`
- `neural_cache/benchmark.py`
- `patch_window.py`
- `scripts/download_kokoro.py`
- `scripts/replica_eval.py`
- `test_agentic_web.py`
- `test_api.py`

## Audit Trail

- EXTRACTED: 236 (98%)
- INFERRED: 4 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*