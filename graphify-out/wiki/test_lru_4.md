# test_lru

> 7 nodes · cohesion 0.29

## Key Concepts

- **TestSnapshot** (7 connections) — `neural_cache/tests/test_lru.py`
- **.test_snapshot_load_respects_capacity()** (2 connections) — `neural_cache/tests/test_lru.py`
- **Snapshot with more keys than capacity should trigger LRU eviction on load.** (1 connections) — `neural_cache/tests/test_lru.py`
- **.test_load_snapshot_restores_values()** (1 connections) — `neural_cache/tests/test_lru.py`
- **.test_load_snapshot_skips_expired()** (1 connections) — `neural_cache/tests/test_lru.py`
- **.test_snapshot_contains_all_live_keys()** (1 connections) — `neural_cache/tests/test_lru.py`
- **.test_snapshot_excludes_expired_keys()** (1 connections) — `neural_cache/tests/test_lru.py`

## Relationships

- [test_lru](test_lru.md) (1 shared connections)
- [lru](lru.md) (1 shared connections)

## Source Files

- `neural_cache/tests/test_lru.py`

## Audit Trail

- EXTRACTED: 7 (88%)
- INFERRED: 1 (12%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*