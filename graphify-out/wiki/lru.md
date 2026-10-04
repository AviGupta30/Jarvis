# lru

> 37 nodes · cohesion 0.09

## Key Concepts

- **LRUCache** (26 connections) — `neural_cache/lru.py`
- **Node** (15 connections) — `neural_cache/lru.py`
- **._evict()** (7 connections) — `neural_cache/lru.py`
- **._evict_tail()** (6 connections) — `neural_cache/lru.py`
- **.load_snapshot()** (6 connections) — `neural_cache/lru.py`
- **.set()** (6 connections) — `neural_cache/lru.py`
- **._unlink()** (6 connections) — `neural_cache/lru.py`
- **.get()** (5 connections) — `neural_cache/lru.py`
- **._insert_after_head()** (5 connections) — `neural_cache/lru.py`
- **._insert_before_tail()** (4 connections) — `neural_cache/lru.py`
- **.snapshot()** (4 connections) — `neural_cache/lru.py`
- **TestO1Timing** (4 connections) — `neural_cache/tests/test_lru.py`
- **._time_ops()** (4 connections) — `neural_cache/tests/test_lru.py`
- **.delete()** (3 connections) — `neural_cache/lru.py`
- **.test_o1_set_get_scaling()** (3 connections) — `neural_cache/tests/test_lru.py`
- **.__init__()** (2 connections) — `neural_cache/lru.py`
- **.is_expired()** (2 connections) — `neural_cache/lru.py`
- **Any** (2 connections)
- **.__contains__()** (1 connections) — `neural_cache/lru.py`
- **.__len__()** (1 connections) — `neural_cache/lru.py`
- **.__init__()** (1 connections) — `neural_cache/lru.py`
- **.__repr__()** (1 connections) — `neural_cache/lru.py`
- **Insert or update a key-value pair. - If key already exists: update value + TTL,…** (1 connections) — `neural_cache/lru.py`
- **Remove a key from the cache. Returns True if the key existed, False if it was…** (1 connections) — `neural_cache/lru.py`
- **Serialise the entire live cache to a plain dict. Expired entries are excluded —…** (1 connections) — `neural_cache/lru.py`
- *... and 12 more nodes in this community*

## Relationships

- [test_lru](test_lru.md) (7 shared connections)
- [server + persistence](server_+_persistence.md) (4 shared connections)
- [neural-cache](neural-cache.md) (1 shared connections)
- [test_protocol + engine](test_protocol_+_engine.md) (1 shared connections)
- [resume_builder](resume_builder.md) (1 shared connections)
- [README + tools](README_+_tools.md) (1 shared connections)

## Source Files

- `neural_cache/lru.py`
- `neural_cache/tests/test_lru.py`

## Audit Trail

- EXTRACTED: 63 (88%)
- INFERRED: 9 (12%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*