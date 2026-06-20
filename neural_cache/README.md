# Neural Cache

A custom in-memory key-value store for JARVIS — Redis-style, single-writer architecture.

## Architecture

```
┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│ Jarvis script│   │ Jarvis script│   │ Jarvis script│
│      A       │   │      B       │   │      C       │
└──────┬───────┘   └──────┬───────┘   └──────┬───────┘
       │  TCP socket connections (port 9090)  │
       └───────────────────┼───────────────────┘
                            ▼
                 ┌─────────────────────┐
                 │   CacheServer        │
                 │  (accepts conns,     │
                 │   1 thread per conn) │
                 └──────────┬───────────┘
                             │  puts (request, conn) onto
                             ▼
                 ┌─────────────────────┐
                 │   command_queue      │  (queue.Queue)
                 └──────────┬───────────┘
                             │  single consumer
                             ▼
                 ┌─────────────────────┐
                 │   CacheEngine        │
                 │  - hash map          │
                 │  - doubly linked list│
                 │  - WAL writer        │
                 │  (runs on ONE thread)│
                 └──────────┬───────────┘
                             │  every 5 minutes
                             ▼
                 ┌─────────────────────┐
                 │  SnapshotThread      │
                 │  dumps full state,  │
                 │  truncates WAL      │
                 └─────────────────────┘
```

## Files

| File | Purpose |
|------|---------|
| `lru.py` | Hand-rolled LRU: `Node` + doubly-linked list + hash map. No `OrderedDict`. |
| `protocol.py` | 4-byte length-prefixed TCP framing. Handles partial reads correctly. |
| `engine.py` | Single-writer queue consumer. Dispatches GET/SET/DEL/PING/SNAPSHOT. |
| `server.py` | TCP accept loop. One thread per client. Startup recovery from disk. |
| `client.py` | Thin Python client. Auto-reconnect. Graceful degradation when server is down. |
| `persistence.py` | WAL (append-on-write) + Snapshot (periodic pickle). |
| `tests/test_lru.py` | Unit tests: eviction order, TTL expiry, O(1) timing, snapshot round-trip. |
| `tests/test_protocol.py` | Wire framing: partial reads, multi-message, large payloads. |
| `tests/test_concurrency.py` | 50 threads × 1000 ops each. Proves no corruption or deadlocks. |
| `benchmark.py` | Latency + throughput vs JSON-file baseline. Generates resume numbers. |

## Wire Protocol

Every message: `<4-byte big-endian length><UTF-8 JSON body>`

**Requests:**
```json
{"cmd": "SET", "key": "dsa_mode", "value": "active", "ttl": 1800}
{"cmd": "GET", "key": "dsa_mode"}
{"cmd": "DEL", "key": "dsa_mode"}
{"cmd": "PING"}
{"cmd": "STATS"}
```

**Responses:**
```json
{"status": "OK", "value": null}
{"status": "OK", "value": "active"}
{"status": "ERR", "error": "key not found"}
```

## Running

```powershell
# Start the server (from project root)
python -m neural_cache.server

# Or with custom settings
python -m neural_cache.server --host 127.0.0.1 --port 9090 --capacity 1024

# Quick test from Python REPL
python -c "
from neural_cache.client import CacheClient
c = CacheClient()
print(c.ping())               # True
c.set('foo', 'bar', ttl=60)
print(c.get('foo'))           # 'bar'
c.delete('foo')
print(c.get('foo'))           # None
"
```

## Tests

```powershell
# From project root
python -m pytest neural_cache/tests/ -v

# Individual suites
python -m pytest neural_cache/tests/test_lru.py -v
python -m pytest neural_cache/tests/test_protocol.py -v
python -m pytest neural_cache/tests/test_concurrency.py -v -s
```

## Benchmark

```powershell
# Start server first, then:
python neural_cache/benchmark.py
# Results saved to neural_cache/benchmark_results.txt
```

## LRU Cache Design

```
head(sentinel) <─> [MRU node] <─> ... <─> [LRU node] <─> tail(sentinel)
     ↑                                                           ↑
  new entries                                           eviction target
  go here                                              (tail.prev)
```

- **O(1) GET**: dict lookup → TTL check → unlink → insert after head
- **O(1) SET**: insert at head → evict tail if over capacity
- **O(1) DEL**: unlink from list → remove from dict
- **Sentinel nodes**: head + tail never in dict → no null checks in hot path

## Persistence

- **WAL (`data/wal.log`)**: every SET/DEL appended before client reply
- **Snapshot (`data/snapshot.rdb`)**: full pickle every 5 min, then WAL truncated
- **Recovery on startup**: load snapshot → replay WAL → start engine

## JARVIS Integration

JARVIS tools use the client as a module-level singleton:

```python
from neural_cache.client import CacheClient
_cache = CacheClient()

_cache.set("dsa_mode:active", "true", ttl=86400)
val = _cache.get("dsa_mode:active")   # "true" or None
```

The LLM can also call `cache_set` and `cache_get` as registered tools, making
state available to voice, frontend, and planner simultaneously — **Rule #4 compliant**.
