# lru

> 14 nodes · cohesion 0.18

## Key Concepts

- **._evict()** (7 connections) — `neural_cache/lru.py`
- **._evict_tail()** (6 connections) — `neural_cache/lru.py`
- **.set()** (6 connections) — `neural_cache/lru.py`
- **._unlink()** (6 connections) — `neural_cache/lru.py`
- **.get()** (5 connections) — `neural_cache/lru.py`
- **._insert_after_head()** (5 connections) — `neural_cache/lru.py`
- **.delete()** (3 connections) — `neural_cache/lru.py`
- **Insert or update a key-value pair. - If key already exists: update value + TTL,…** (1 connections) — `neural_cache/lru.py`
- **Remove a key from the cache. Returns True if the key existed, False if it was…** (1 connections) — `neural_cache/lru.py`
- **Place node at the MRU (most-recently-used) end of the list.** (1 connections) — `neural_cache/lru.py`
- **Remove node from its current position in the list (O(1) because doubly-linked).** (1 connections) — `neural_cache/lru.py`
- **Evict a specific node (unlink + remove from map).** (1 connections) — `neural_cache/lru.py`
- **Evict the LRU entry (the node just before the tail sentinel). Returns the…** (1 connections) — `neural_cache/lru.py`
- **Return the value for key, or None on miss / expiry. On hit: moves node to the…** (1 connections) — `neural_cache/lru.py`

## Relationships

- [lru](lru.md) (13 shared connections)

## Source Files

- `neural_cache/lru.py`

## Audit Trail

- EXTRACTED: 29 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*