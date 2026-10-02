# test_protocol

> 31 nodes · cohesion 0.11

## Key Concepts

- **encode_message()** (17 connections) — `neural_cache/protocol.py`
- **decode_message()** (13 connections) — `neural_cache/protocol.py`
- **make_fake_socket()** (9 connections) — `neural_cache/tests/test_protocol.py`
- **TestDecode** (8 connections) — `neural_cache/tests/test_protocol.py`
- **.test_connection_close_mid_body_raises()** (6 connections) — `neural_cache/tests/test_protocol.py`
- **TestEncode** (6 connections) — `neural_cache/tests/test_protocol.py`
- **make_socket_from_messages()** (5 connections) — `neural_cache/tests/test_protocol.py`
- **.test_large_payload_roundtrip()** (5 connections) — `neural_cache/tests/test_protocol.py`
- **.test_partial_read_handling()** (5 connections) — `neural_cache/tests/test_protocol.py`
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
- **Serialise a dict to the wire format: [4-byte length][UTF-8 JSON body] Args:…** (1 connections) — `neural_cache/protocol.py`
- **Read exactly one message from a socket, handling partial TCP reads correctly.…** (1 connections) — `neural_cache/protocol.py`
- **1 MB value — tests that the length prefix handles large messages.** (1 connections) — `neural_cache/tests/test_protocol.py`
- **The fake socket returns 1 byte at a time. _recv_exact must loop until it has…** (1 connections) — `neural_cache/tests/test_protocol.py`
- *... and 6 more nodes in this community*

## Relationships

- [persistence + engine](persistence_+_engine.md) (13 shared connections)

## Source Files

- `neural_cache/protocol.py`
- `neural_cache/tests/test_protocol.py`

## Audit Trail

- EXTRACTED: 63 (97%)
- INFERRED: 2 (3%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*