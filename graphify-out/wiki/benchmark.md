# benchmark

> 14 nodes · cohesion 0.14

## Key Concepts

- **JSONFileBaseline** (7 connections) — `neural_cache/benchmark.py`
- **main()** (7 connections) — `neural_cache/benchmark.py`
- **measure_throughput()** (4 connections) — `neural_cache/benchmark.py`
- **measure_latency()** (3 connections) — `neural_cache/benchmark.py`
- **.delete()** (1 connections) — `neural_cache/benchmark.py`
- **.get()** (1 connections) — `neural_cache/benchmark.py`
- **.__init__()** (1 connections) — `neural_cache/benchmark.py`
- **.set()** (1 connections) — `neural_cache/benchmark.py`
- **_cache_set()** (1 connections) — `neural_cache/benchmark.py`
- **_json_set()** (1 connections) — `neural_cache/benchmark.py`
- **_worker()** (1 connections) — `neural_cache/benchmark.py`
- **Spin up n_threads threads each doing ops_per_thread SET+GET pairs. Returns…** (1 connections) — `neural_cache/benchmark.py`
- **Mimics memory_tool.py's approach: every read/write touches disk. Uses a…** (1 connections) — `neural_cache/benchmark.py`
- **Run op_fn warmup times (discard), then timed times (measure). Returns (mean_µs,…** (1 connections) — `neural_cache/benchmark.py`

## Relationships

- [message_reader + thread_extractor](message_reader_+_thread_extractor.md) (4 shared connections)
- [client](client.md) (1 shared connections)

## Source Files

- `neural_cache/benchmark.py`

## Audit Trail

- EXTRACTED: 15 (83%)
- INFERRED: 3 (17%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*