# test_concurrency

> 11 nodes · cohesion 0.20

## Key Concepts

- **_worker()** (6 connections) — `neural_cache/tests/test_concurrency.py`
- **TestConcurrency** (5 connections) — `neural_cache/tests/test_concurrency.py`
- **.test_50_threads_no_corruption()** (4 connections) — `neural_cache/tests/test_concurrency.py`
- **.test_ping_under_load()** (4 connections) — `neural_cache/tests/test_concurrency.py`
- **.test_server_stats_after_load()** (3 connections) — `neural_cache/tests/test_concurrency.py`
- **_ping_loop()** (2 connections) — `neural_cache/tests/test_concurrency.py`
- **Lock** (1 connections)
- **50 concurrent clients, each doing 1000 ops. After completion: - Server still…** (1 connections) — `neural_cache/tests/test_concurrency.py`
- **The engine should report meaningful stats after the load test.** (1 connections) — `neural_cache/tests/test_concurrency.py`
- **While 10 threads hammer the cache, a separate thread pings repeatedly. All…** (1 connections) — `neural_cache/tests/test_concurrency.py`
- **One client thread. Performs `ops` random GET/SET/DEL operations. Records any…** (1 connections) — `neural_cache/tests/test_concurrency.py`

## Relationships

- [client](client.md) (5 shared connections)
- [server + test_concurrency](server_+_test_concurrency.md) (2 shared connections)

## Source Files

- `neural_cache/tests/test_concurrency.py`

## Audit Trail

- EXTRACTED: 14 (78%)
- INFERRED: 4 (22%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*