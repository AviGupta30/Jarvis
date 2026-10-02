# lru + test_lru

> 57 nodes · cohesion 0.05

## Key Concepts

- **LRUCache** (26 connections) — `neural_cache/lru.py`
- **test_lru.py** (16 connections) — `neural_cache/tests/test_lru.py`
- **Node** (15 connections) — `neural_cache/lru.py`
- **._evict()** (7 connections) — `neural_cache/lru.py`
- **TestSnapshot** (7 connections) — `neural_cache/tests/test_lru.py`
- **._evict_tail()** (6 connections) — `neural_cache/lru.py`
- **.load_snapshot()** (6 connections) — `neural_cache/lru.py`
- **.set()** (6 connections) — `neural_cache/lru.py`
- **._unlink()** (6 connections) — `neural_cache/lru.py`
- **.get()** (5 connections) — `neural_cache/lru.py`
- **._insert_after_head()** (5 connections) — `neural_cache/lru.py`
- **TestSentinels** (5 connections) — `neural_cache/tests/test_lru.py`
- **Design** (4 connections) — `docs/features/neural-cache.md`
- **._insert_before_tail()** (4 connections) — `neural_cache/lru.py`
- **small_cache()** (4 connections) — `neural_cache/tests/test_lru.py`
- **TestO1Timing** (4 connections) — `neural_cache/tests/test_lru.py`
- **._time_ops()** (4 connections) — `neural_cache/tests/test_lru.py`
- **.delete()** (3 connections) — `neural_cache/lru.py`
- **.snapshot()** (3 connections) — `neural_cache/lru.py`
- **large_cache()** (3 connections) — `neural_cache/tests/test_lru.py`
- **.test_o1_set_get_scaling()** (3 connections) — `neural_cache/tests/test_lru.py`
- **pytest** (3 connections)
- **.__init__()** (2 connections) — `neural_cache/lru.py`
- **.is_expired()** (2 connections) — `neural_cache/lru.py`
- **Any** (2 connections)
- *... and 32 more nodes in this community*

## Relationships

- [test_lru](test_lru.md) (4 shared connections)
- [engine + test_protocol](engine_+_test_protocol.md) (3 shared connections)
- [ui_inspector + lru](ui_inspector_+_lru.md) (3 shared connections)
- [assignment_tool + safe_executor](assignment_tool_+_safe_executor.md) (3 shared connections)
- [persistence + server](persistence_+_server.md) (2 shared connections)
- [neural-cache](neural-cache.md) (1 shared connections)
- [client](client.md) (1 shared connections)
- [README](README.md) (1 shared connections)
- [test_protocol](test_protocol.md) (1 shared connections)

## Source Files

- `docs/features/neural-cache.md`
- `neural_cache/lru.py`
- `neural_cache/tests/test_lru.py`

## Audit Trail

- EXTRACTED: 92 (90%)
- INFERRED: 10 (10%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*