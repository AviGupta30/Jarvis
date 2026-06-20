"""
test_protocol.py — Unit tests for neural_cache.protocol (Milestone 7)
=======================================================================
Tests:
  - Basic encode/decode round-trip
  - Partial TCP reads (the whole point of _recv_exact)
  - Large payload (1 MB)
  - Empty payload {}
  - Multi-message stream (two messages glued together)
  - ok_response / err_response helpers

Run with:
    python -m pytest neural_cache/tests/test_protocol.py -v
"""

import io
import struct
import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pytest
from neural_cache.protocol import (
    encode_message,
    decode_message,
    _recv_exact,
    ok_response,
    err_response,
    LENGTH_PREFIX_BYTES,
    LENGTH_PREFIX_FMT,
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def make_fake_socket(data: bytes):
    """
    Return a mock socket that reads from `data` in small chunks,
    simulating partial TCP reads (the real-world problem _recv_exact solves).
    """
    buf = bytearray(data)
    pos = [0]

    def fake_recv(n):
        # Deliberately return only 1 byte at a time to torture _recv_exact
        if pos[0] >= len(buf):
            return b""
        chunk = bytes(buf[pos[0]: pos[0] + 1])
        pos[0] += 1
        return chunk

    sock = MagicMock()
    sock.recv.side_effect = fake_recv
    return sock


def make_socket_from_messages(*payloads):
    """Encode multiple messages and concatenate them into a single stream."""
    raw = b"".join(encode_message(p) for p in payloads)
    return make_fake_socket(raw)


# ── encode_message ────────────────────────────────────────────────────────────

class TestEncode:
    def test_returns_bytes(self):
        result = encode_message({"cmd": "PING"})
        assert isinstance(result, bytes)

    def test_header_is_4_bytes(self):
        result = encode_message({"cmd": "PING"})
        assert len(result) >= 4

    def test_header_encodes_body_length(self):
        payload = {"cmd": "SET", "key": "k", "value": "v"}
        result = encode_message(payload)
        body_len = struct.unpack(LENGTH_PREFIX_FMT, result[:LENGTH_PREFIX_BYTES])[0]
        assert body_len == len(result) - LENGTH_PREFIX_BYTES

    def test_body_is_valid_json(self):
        payload = {"cmd": "GET", "key": "hello"}
        result = encode_message(payload)
        body = result[LENGTH_PREFIX_BYTES:]
        parsed = json.loads(body.decode("utf-8"))
        assert parsed == payload

    def test_non_ascii_value(self):
        payload = {"key": "मनीषा", "value": "नमस्ते 🙏"}
        result = encode_message(payload)
        body = result[LENGTH_PREFIX_BYTES:]
        parsed = json.loads(body.decode("utf-8"))
        assert parsed["value"] == "नमस्ते 🙏"


# ── decode_message ────────────────────────────────────────────────────────────

class TestDecode:
    def test_basic_roundtrip(self):
        payload = {"cmd": "SET", "key": "foo", "value": "bar", "ttl": 60}
        sock = make_fake_socket(encode_message(payload))
        result = decode_message(sock)
        assert result == payload

    def test_ping_roundtrip(self):
        sock = make_fake_socket(encode_message({"cmd": "PING"}))
        result = decode_message(sock)
        assert result == {"cmd": "PING"}

    def test_empty_dict_roundtrip(self):
        sock = make_fake_socket(encode_message({}))
        result = decode_message(sock)
        assert result == {}

    def test_large_payload_roundtrip(self):
        """1 MB value — tests that the length prefix handles large messages."""
        big_value = "x" * (1024 * 1024)
        payload = {"cmd": "SET", "key": "big", "value": big_value}
        sock = make_fake_socket(encode_message(payload))
        result = decode_message(sock)
        assert result["value"] == big_value

    def test_partial_read_handling(self):
        """
        The fake socket returns 1 byte at a time.
        _recv_exact must loop until it has the full message.
        This is the core correctness property of the protocol.
        """
        payload = {"status": "OK", "value": "hello world from JARVIS"}
        sock = make_fake_socket(encode_message(payload))
        result = decode_message(sock)
        assert result == payload

    def test_connection_close_mid_header_raises(self):
        """Socket closes after 2 bytes — ConnectionError expected."""
        sock = MagicMock()
        sock.recv.side_effect = [b"\x00\x00", b""]  # 2 bytes then EOF
        with pytest.raises(ConnectionError):
            decode_message(sock)

    def test_connection_close_mid_body_raises(self):
        """Socket delivers the header but then closes before the body."""
        payload = {"cmd": "GET", "key": "x"}
        raw = encode_message(payload)
        header = raw[:LENGTH_PREFIX_BYTES]
        # Give only first byte of body then EOF
        call_count = [0]

        def fake_recv(n):
            call_count[0] += 1
            if call_count[0] == 1:
                return header      # full header in one call
            return b""             # then EOF

        sock = MagicMock()
        sock.recv.side_effect = fake_recv
        with pytest.raises(ConnectionError):
            decode_message(sock)


# ── Multi-message stream ──────────────────────────────────────────────────────

class TestMultiMessage:
    def test_two_messages_decoded_independently(self):
        """
        Encode two separate messages and feed them through the same socket.
        decode_message must return them one at a time, correctly framed.
        """
        msg1 = {"cmd": "PING"}
        msg2 = {"cmd": "GET", "key": "dsa_mode"}
        sock = make_socket_from_messages(msg1, msg2)

        r1 = decode_message(sock)
        r2 = decode_message(sock)

        assert r1 == msg1
        assert r2 == msg2


# ── Response helpers ──────────────────────────────────────────────────────────

class TestHelpers:
    def test_ok_response_no_value(self):
        r = ok_response()
        assert r["status"] == "OK"
        assert r["value"] is None

    def test_ok_response_with_value(self):
        r = ok_response("active")
        assert r["value"] == "active"

    def test_err_response(self):
        r = err_response("key not found")
        assert r["status"] == "ERR"
        assert r["error"] == "key not found"

    def test_helpers_are_json_serialisable(self):
        for r in [ok_response(42), ok_response(None), err_response("boom")]:
            encoded = encode_message(r)
            assert isinstance(encoded, bytes)
