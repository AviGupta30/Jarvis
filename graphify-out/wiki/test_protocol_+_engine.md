# test_protocol + engine

> 66 nodes · cohesion 0.06

## Key Concepts

- **CacheEngine** (20 connections) — `neural_cache/engine.py`
- **test_protocol.py** (20 connections) — `neural_cache/tests/test_protocol.py`
- **encode_message()** (17 connections) — `neural_cache/protocol.py`
- **ok_response()** (14 connections) — `neural_cache/protocol.py`
- **protocol.py** (13 connections) — `neural_cache/protocol.py`
- **decode_message()** (13 connections) — `neural_cache/protocol.py`
- **err_response()** (13 connections) — `neural_cache/protocol.py`
- **._dispatch()** (11 connections) — `neural_cache/engine.py`
- **make_fake_socket()** (9 connections) — `neural_cache/tests/test_protocol.py`
- **TestDecode** (8 connections) — `neural_cache/tests/test_protocol.py`
- **Any** (7 connections)
- **.test_connection_close_mid_body_raises()** (6 connections) — `neural_cache/tests/test_protocol.py`
- **TestEncode** (6 connections) — `neural_cache/tests/test_protocol.py`
- **._handle_del()** (5 connections) — `neural_cache/engine.py`
- **._handle_get()** (5 connections) — `neural_cache/engine.py`
- **._handle_set()** (5 connections) — `neural_cache/engine.py`
- **._handle_snapshot()** (5 connections) — `neural_cache/engine.py`
- **make_socket_from_messages()** (5 connections) — `neural_cache/tests/test_protocol.py`
- **.test_large_payload_roundtrip()** (5 connections) — `neural_cache/tests/test_protocol.py`
- **.test_partial_read_handling()** (5 connections) — `neural_cache/tests/test_protocol.py`
- **TestHelpers** (5 connections) — `neural_cache/tests/test_protocol.py`
- **._handle_ping()** (4 connections) — `neural_cache/engine.py`
- **._handle_stats()** (4 connections) — `neural_cache/engine.py`
- **._worker()** (4 connections) — `neural_cache/engine.py`
- **Any** (4 connections)
- *... and 41 more nodes in this community*

## Relationships

- [message_reader + thread_extractor](message_reader_+_thread_extractor.md) (10 shared connections)
- [persistence + server](persistence_+_server.md) (5 shared connections)
- [voice_agent + download_kokoro](voice_agent_+_download_kokoro.md) (4 shared connections)
- [neural-cache](neural-cache.md) (1 shared connections)
- [lru](lru.md) (1 shared connections)

## Source Files

- `neural_cache/engine.py`
- `neural_cache/protocol.py`
- `neural_cache/tests/test_protocol.py`

## Audit Trail

- EXTRACTED: 147 (95%)
- INFERRED: 7 (5%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*