# Neural cache (Redis-like LRU server)

## Purpose
A small Redis-like in-memory KV store (hand-rolled LRU + TTL) over TCP, used for cross-process state (DSA mode, `cache_get/set` tools). Full design: `neural_cache/README.md`.

## Runtime
`app/main.py` startup spawns `python neural_cache/server.py --host 127.0.0.1 --port 9090 --capacity 1024` (detached; if already running, the new one exits). Manual: `python -m neural_cache.server`.

## Design
Client threads → `server.py` (thread per connection) → queue → `engine.CacheEngine` single-writer thread owning `lru.LRUCache` (dict + doubly linked list, O(1)) → `persistence` WAL append on write + snapshot every 5 min (recovery on boot). Wire format: 4-byte big-endian length + UTF-8 JSON (`protocol.py`). `client.CacheClient` is thread-safe, auto-reconnects, and degrades gracefully.

## Tests
`python -m pytest neural_cache/tests -v` (LRU, protocol, 50-thread concurrency). Benchmark: `python neural_cache/benchmark.py`.

## Graphify
`graphify explain "CacheEngine"` · `graphify explain "LRUCache"`

<!-- AUTO:BEGIN (scripts/refresh_docs.py) -->
## Files & symbols (auto-generated, line numbers are current)

- `neural_cache/lru.py` (232 lines): lru.py — Hand-rolled LRU Cache (Milestone 1)
  L21 class Node · (L42 .is_expired) · L55 class LRUCache · (L87 .get, L107 .set, L136 .delete, L156 .snapshot, L175 .load_snapshot, L197 ._insert_after_head, L204 ._insert_before_tail, L211 ._unlink, L216 ._evict, L222 ._evict_tail)
- `neural_cache/protocol.py` (122 lines): protocol.py — Wire Protocol for Neural Cache (Milestone 2)
  L28 LENGTH_PREFIX_FMT · L34 encode_message() · L55 decode_message() · L82 _recv_exact() · L114 ok_response() · L119 err_response()
- `neural_cache/engine.py` (225 lines): engine.py — Single-Writer Command Queue (Milestone 3)
  L37 class CacheEngine · (L69 .start, L83 .stop, L94 ._worker, L125 ._dispatch, L149 ._handle_ping, L152 ._handle_get, L167 ._handle_set, L189 ._handle_del, L206 ._handle_stats, L219 ._handle_snapshot)
- `neural_cache/server.py` (271 lines): server.py — TCP Accept Loop for Neural Cache (Milestone 4)
  L65 class CacheServer · (L104 .start, L113 ._recover_state, L144 ._accept_loop, L181 ._handle_client, L219 ._shutdown) · L241 main()
- `neural_cache/client.py` (225 lines): client.py — Python Client Library for Neural Cache (Milestone 5)
  L41 DEFAULT_HOST · L42 DEFAULT_PORT · L43 DEFAULT_TIMEOUT · L46 class CacheClient · (L68 .ping, L79 .get, L98 .set, L125 .delete, L139 .stats, L153 .close, L160 ._send, L184 ._ensure_connected, L207 ._close_socket)
- `neural_cache/persistence.py` (206 lines): persistence.py — WAL + Snapshot for Neural Cache (Milestone 6)
  L40 class WALWriter · (L58 .append, L75 .read_all, L98 .truncate, L114 .close) · L125 class SnapshotManager · (L146 .write, L162 .read, L179 .start_background_thread)
<!-- AUTO:END -->
