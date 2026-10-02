# client

> 15 nodes · cohesion 0.13

## Key Concepts

- **._send()** (10 connections) — `neural_cache/client.py`
- **.set()** (4 connections) — `neural_cache/client.py`
- **.delete()** (3 connections) — `neural_cache/client.py`
- **._ensure_connected()** (3 connections) — `neural_cache/client.py`
- **.get()** (3 connections) — `neural_cache/client.py`
- **.ping()** (3 connections) — `neural_cache/client.py`
- **.stats()** (3 connections) — `neural_cache/client.py`
- **Any** (1 connections)
- **Store a key-value pair, optionally with a TTL. Args: key: Cache key. value:…** (1 connections) — `neural_cache/client.py`
- **Delete a key from the cache. Returns: True if the key existed and was deleted,…** (1 connections) — `neural_cache/client.py`
- **Retrieve server statistics (hit rate, evictions, cache size, etc.). Returns…** (1 connections) — `neural_cache/client.py`
- **Send a command and return the response. Thread-safe. Handles lazy connect and…** (1 connections) — `neural_cache/client.py`
- **Open a socket to the server if not already connected. Called within the lock —…** (1 connections) — `neural_cache/client.py`
- **Send a PING and return True if the server replies PONG. Useful for health…** (1 connections) — `neural_cache/client.py`
- **Retrieve the value for a key, or None on miss / expiry / error. Args: key:…** (1 connections) — `neural_cache/client.py`

## Relationships

- [client](client.md) (8 shared connections)
- [style_profiler + reply_generator](style_profiler_+_reply_generator.md) (1 shared connections)

## Source Files

- `neural_cache/client.py`

## Audit Trail

- EXTRACTED: 23 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*