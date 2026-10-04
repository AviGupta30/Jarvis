# test_protocol

> 39 nodes · cohesion 0.10

## Key Concepts

- **test_protocol.py** (20 connections) — `neural_cache/tests/test_protocol.py`
- **encode_message()** (17 connections) — `neural_cache/protocol.py`
- **protocol.py** (13 connections) — `neural_cache/protocol.py`
- **decode_message()** (13 connections) — `neural_cache/protocol.py`
- **make_fake_socket()** (9 connections) — `neural_cache/tests/test_protocol.py`
- **TestDecode** (8 connections) — `neural_cache/tests/test_protocol.py`
- **.test_connection_close_mid_body_raises()** (6 connections) — `neural_cache/tests/test_protocol.py`
- **TestEncode** (6 connections) — `neural_cache/tests/test_protocol.py`
- **make_socket_from_messages()** (5 connections) — `neural_cache/tests/test_protocol.py`
- **.test_large_payload_roundtrip()** (5 connections) — `neural_cache/tests/test_protocol.py`
- **.test_partial_read_handling()** (5 connections) — `neural_cache/tests/test_protocol.py`
- **_recv_exact()** (4 connections) — `neural_cache/protocol.py`
- **.test_basic_roundtrip()** (4 connections) — `neural_cache/tests/test_protocol.py`
- **.test_empty_dict_roundtrip()** (4 connections) — `neural_cache/tests/test_protocol.py`
- **.test_ping_roundtrip()** (4 connections) — `neural_cache/tests/test_protocol.py`
- **.test_two_messages_decoded_independently()** (4 connections) — `neural_cache/tests/test_protocol.py`
- **.test_connection_close_mid_header_raises()** (3 connections) — `neural_cache/tests/test_protocol.py`
- **fake_recv()** (2 connections) — `neural_cache/tests/test_protocol.py`
- **.test_body_is_valid_json()** (2 connections) — `neural_cache/tests/test_protocol.py`
- **.test_header_encodes_body_length()** (2 connections) — `neural_cache/tests/test_protocol.py`
- **.test_header_is_4_bytes()** (2 connections) — `neural_cache/tests/test_protocol.py`
- **.test_non_ascii_value()** (2 connections) — `neural_cache/tests/test_protocol.py`
- **.test_returns_bytes()** (2 connections) — `neural_cache/tests/test_protocol.py`
- **TestMultiMessage** (2 connections) — `neural_cache/tests/test_protocol.py`
- **struct** (2 connections)
- *... and 14 more nodes in this community*

## Relationships

- [engine + test_protocol](engine_+_test_protocol.md) (9 shared connections)
- [assignment_humanizer + task_ledger](assignment_humanizer_+_task_ledger.md) (3 shared connections)
- [server](server.md) (2 shared connections)
- [style_profiler + reply_generator](style_profiler_+_reply_generator.md) (1 shared connections)
- [assignment_answers](assignment_answers.md) (1 shared connections)
- [safe_executor + refresh_docs](safe_executor_+_refresh_docs.md) (1 shared connections)
- [test_lru](test_lru.md) (1 shared connections)

## Source Files

- `neural_cache/protocol.py`
- `neural_cache/tests/test_protocol.py`

## Audit Trail

- EXTRACTED: 87 (98%)
- INFERRED: 2 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*