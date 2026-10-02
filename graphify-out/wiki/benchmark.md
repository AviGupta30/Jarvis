# benchmark

> 8 nodes · cohesion 0.25

## Key Concepts

- **main()** (7 connections) — `neural_cache/benchmark.py`
- **measure_throughput()** (4 connections) — `neural_cache/benchmark.py`
- **measure_latency()** (3 connections) — `neural_cache/benchmark.py`
- **_cache_set()** (1 connections) — `neural_cache/benchmark.py`
- **_json_set()** (1 connections) — `neural_cache/benchmark.py`
- **_worker()** (1 connections) — `neural_cache/benchmark.py`
- **Spin up n_threads threads each doing ops_per_thread SET+GET pairs. Returns…** (1 connections) — `neural_cache/benchmark.py`
- **Run op_fn warmup times (discard), then timed times (measure). Returns (mean_µs,…** (1 connections) — `neural_cache/benchmark.py`

## Relationships

- [smart_navigator + rag_memory](smart_navigator_+_rag_memory.md) (3 shared connections)
- [client](client.md) (1 shared connections)
- [benchmark](benchmark.md) (1 shared connections)

## Source Files

- `neural_cache/benchmark.py`

## Audit Trail

- EXTRACTED: 9 (75%)
- INFERRED: 3 (25%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*