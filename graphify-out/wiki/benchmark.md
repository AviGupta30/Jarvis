# benchmark

> 18 nodes · cohesion 0.13

## Key Concepts

- **benchmark.py** (16 connections) — `neural_cache/benchmark.py`
- **JSONFileBaseline** (7 connections) — `neural_cache/benchmark.py`
- **main()** (7 connections) — `neural_cache/benchmark.py`
- **queue** (7 connections)
- **measure_throughput()** (4 connections) — `neural_cache/benchmark.py`
- **measure_latency()** (3 connections) — `neural_cache/benchmark.py`
- **tempfile** (2 connections)
- **.delete()** (1 connections) — `neural_cache/benchmark.py`
- **.get()** (1 connections) — `neural_cache/benchmark.py`
- **.__init__()** (1 connections) — `neural_cache/benchmark.py`
- **.set()** (1 connections) — `neural_cache/benchmark.py`
- **_cache_set()** (1 connections) — `neural_cache/benchmark.py`
- **_json_set()** (1 connections) — `neural_cache/benchmark.py`
- **_worker()** (1 connections) — `neural_cache/benchmark.py`
- **benchmark.py — Neural Cache vs JSON-file Baseline (Milestone 8)…** (1 connections) — `neural_cache/benchmark.py`
- **Spin up n_threads threads each doing ops_per_thread SET+GET pairs. Returns…** (1 connections) — `neural_cache/benchmark.py`
- **Mimics memory_tool.py's approach: every read/write touches disk. Uses a…** (1 connections) — `neural_cache/benchmark.py`
- **Run op_fn warmup times (discard), then timed times (measure). Returns (mean_µs,…** (1 connections) — `neural_cache/benchmark.py`

## Relationships

- [server](server.md) (3 shared connections)
- [assignment_humanizer + task_ledger](assignment_humanizer_+_task_ledger.md) (2 shared connections)
- [client + test_concurrency](client_+_test_concurrency.md) (2 shared connections)
- [social_content_manager + content-tools](social_content_manager_+_content-tools.md) (1 shared connections)
- [safe_executor + refresh_docs](safe_executor_+_refresh_docs.md) (1 shared connections)
- [message_reader + thread_extractor](message_reader_+_thread_extractor.md) (1 shared connections)
- [style_profiler + reply_generator](style_profiler_+_reply_generator.md) (1 shared connections)
- [agentic_web + email-calendar](agentic_web_+_email-calendar.md) (1 shared connections)
- [ppt_studio](ppt_studio.md) (1 shared connections)
- [prompt_enhancer_button](prompt_enhancer_button.md) (1 shared connections)
- [resume_builder + integrate](resume_builder_+_integrate.md) (1 shared connections)
- [engine + test_protocol](engine_+_test_protocol.md) (1 shared connections)

## Source Files

- `neural_cache/benchmark.py`

## Audit Trail

- EXTRACTED: 34 (92%)
- INFERRED: 3 (8%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*