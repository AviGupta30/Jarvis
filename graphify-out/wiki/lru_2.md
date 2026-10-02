# lru

> 18 nodes · cohesion 0.17

## Key Concepts

- **LRUCache** (26 connections) — `neural_cache/lru.py`
- **._evict()** (7 connections) — `neural_cache/lru.py`
- **._evict_tail()** (6 connections) — `neural_cache/lru.py`
- **.set()** (6 connections) — `neural_cache/lru.py`
- **._unlink()** (6 connections) — `neural_cache/lru.py`
- **.get()** (5 connections) — `neural_cache/lru.py`
- **._insert_after_head()** (5 connections) — `neural_cache/lru.py`
- **.delete()** (3 connections) — `neural_cache/lru.py`
- **.__contains__()** (1 connections) — `neural_cache/lru.py`
- **.__len__()** (1 connections) — `neural_cache/lru.py`
- **Insert or update a key-value pair. - If key already exists: update value + TTL,…** (1 connections) — `neural_cache/lru.py`
- **Remove a key from the cache. Returns True if the key existed, False if it was…** (1 connections) — `neural_cache/lru.py`
- **Place node at the MRU (most-recently-used) end of the list.** (1 connections) — `neural_cache/lru.py`
- **Remove node from its current position in the list (O(1) because doubly-linked).** (1 connections) — `neural_cache/lru.py`
- **Evict a specific node (unlink + remove from map).** (1 connections) — `neural_cache/lru.py`
- **Evict the LRU entry (the node just before the tail sentinel). Returns the…** (1 connections) — `neural_cache/lru.py`
- **O(1) Least-Recently-Used cache backed by: - dict[str, Node] — hash map for O(1)…** (1 connections) — `neural_cache/lru.py`
- **Return the value for key, or None on miss / expiry. On hit: moves node to the…** (1 connections) — `neural_cache/lru.py`

## Relationships

- [lru](lru.md) (10 shared connections)
- [test_lru](test_lru.md) (6 shared connections)
- [message_reader + reply_generator](message_reader_+_reply_generator.md) (2 shared connections)
- [persistence](persistence.md) (1 shared connections)
- [server + protocol](server_+_protocol.md) (1 shared connections)
- [neural-cache](neural-cache.md) (1 shared connections)
- [test_protocol + engine](test_protocol_+_engine.md) (1 shared connections)

## Source Files

- `neural_cache/lru.py`

## Audit Trail

- EXTRACTED: 41 (85%)
- INFERRED: 7 (15%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*