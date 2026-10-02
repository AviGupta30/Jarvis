# test_lru

> 10 nodes · cohesion 0.20

## Key Concepts

- **TestEviction** (6 connections) — `neural_cache/tests/test_lru.py`
- **.test_access_prevents_eviction()** (2 connections) — `neural_cache/tests/test_lru.py`
- **.test_lru_eviction_basic()** (2 connections) — `neural_cache/tests/test_lru.py`
- **.test_map_stays_in_sync()** (2 connections) — `neural_cache/tests/test_lru.py`
- **.test_update_moves_to_mru()** (2 connections) — `neural_cache/tests/test_lru.py`
- **Accessing 'a' should move it to MRU and save it from eviction.** (1 connections) — `neural_cache/tests/test_lru.py`
- **Re-setting an existing key should move it to MRU.** (1 connections) — `neural_cache/tests/test_lru.py`
- **len(cache.map) must never exceed capacity.** (1 connections) — `neural_cache/tests/test_lru.py`
- **Fill to capacity+1. The first key inserted (LRU) should be evicted.** (1 connections) — `neural_cache/tests/test_lru.py`
- **.test_eviction_count()** (1 connections) — `neural_cache/tests/test_lru.py`

## Relationships

- [server + protocol](server_+_protocol.md) (1 shared connections)

## Source Files

- `neural_cache/tests/test_lru.py`

## Audit Trail

- EXTRACTED: 10 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*