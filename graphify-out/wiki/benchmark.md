# benchmark

> 18 nodes · cohesion 0.13

## Key Concepts

- **benchmark.py** (16 connections) — `neural_cache/benchmark.py`
- **JSONFileBaseline** (7 connections) — `neural_cache/benchmark.py`
- **main()** (7 connections) — `neural_cache/benchmark.py`
- **queue** (6 connections)
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

- [server + test_concurrency](server_+_test_concurrency.md) (3 shared connections)
- [agentic_web](agentic_web.md) (2 shared connections)
- [client + test_concurrency](client_+_test_concurrency.md) (2 shared connections)
- [task_ledger + test_task_resumption](task_ledger_+_test_task_resumption.md) (1 shared connections)
- [chat + llm](chat_+_llm.md) (1 shared connections)
- [whatsapp + dump_wa_ui](whatsapp_+_dump_wa_ui.md) (1 shared connections)
- [assignment_tool](assignment_tool.md) (1 shared connections)
- [reply_generator](reply_generator.md) (1 shared connections)
- [ppt_studio](ppt_studio.md) (1 shared connections)
- [prompt_enhancer_button](prompt_enhancer_button.md) (1 shared connections)
- [engine + test_protocol](engine_+_test_protocol.md) (1 shared connections)
- [ppt_template](ppt_template.md) (1 shared connections)

## Source Files

- `neural_cache/benchmark.py`

## Audit Trail

- EXTRACTED: 33 (92%)
- INFERRED: 3 (8%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*