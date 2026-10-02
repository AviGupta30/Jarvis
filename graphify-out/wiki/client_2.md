# client

> 10 nodes · cohesion 0.24

## Key Concepts

- **CacheClient** (27 connections) — `neural_cache/client.py`
- **.close()** (4 connections) — `neural_cache/client.py`
- **._close_socket()** (4 connections) — `neural_cache/client.py`
- **.__exit__()** (2 connections) — `neural_cache/client.py`
- **.__enter__()** (1 connections) — `neural_cache/client.py`
- **.__init__()** (1 connections) — `neural_cache/client.py`
- **.__repr__()** (1 connections) — `neural_cache/client.py`
- **Explicitly close the socket connection.** (1 connections) — `neural_cache/client.py`
- **Close self._sock, suppressing errors. Called within the lock.** (1 connections) — `neural_cache/client.py`
- **Thread-safe client for the Neural Cache server. One instance can be safely…** (1 connections) — `neural_cache/client.py`

## Relationships

- [client](client.md) (8 shared connections)
- [test_concurrency](test_concurrency.md) (5 shared connections)
- [server + test_concurrency](server_+_test_concurrency.md) (3 shared connections)
- [benchmark](benchmark.md) (1 shared connections)
- [dsa_enforcer + dsa-mode](dsa_enforcer_+_dsa-mode.md) (1 shared connections)
- [tools](tools.md) (1 shared connections)
- [smart_navigator + rag_memory](smart_navigator_+_rag_memory.md) (1 shared connections)
- [neural-cache](neural-cache.md) (1 shared connections)

## Source Files

- `neural_cache/client.py`

## Audit Trail

- EXTRACTED: 29 (91%)
- INFERRED: 3 (9%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*