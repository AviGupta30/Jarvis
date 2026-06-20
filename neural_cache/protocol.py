"""
protocol.py — Wire Protocol for Neural Cache (Milestone 2)
===========================================================
Format: <4-byte big-endian unsigned int length><UTF-8 JSON payload>

Why length-prefixing?
  TCP is a stream protocol, not a message protocol. A single recv() call can
  return partial data or multiple messages glued together. Length-prefixing is
  the standard, correct fix — it tells the receiver exactly how many bytes to
  wait for before attempting JSON decoding.

Why not JSON-lines (\n delimited)?
  If a value itself contains a newline (e.g. stored text, code), the framing
  breaks silently. Length-prefixing is unambiguous regardless of payload content.

Why not pickle over the wire?
  pickle allows arbitrary code execution on deserialise — never safe across
  a socket boundary, even on localhost. JSON is safe; pickle is used ONLY for
  the on-disk snapshot where both ends are controlled by us.
"""

import json
import struct
from typing import Any, Dict

# ── Constants ─────────────────────────────────────────────────────────────────

LENGTH_PREFIX_FMT   = ">I"          # big-endian unsigned 32-bit int
LENGTH_PREFIX_BYTES = struct.calcsize(LENGTH_PREFIX_FMT)  # = 4


# ── Encode ────────────────────────────────────────────────────────────────────

def encode_message(payload: Dict[str, Any]) -> bytes:
    """
    Serialise a dict to the wire format:
        [4-byte length][UTF-8 JSON body]

    Args:
        payload: A JSON-serialisable dict (command or response).

    Returns:
        Bytes ready to be sent over a socket with sendall().

    Raises:
        TypeError: If payload is not JSON-serialisable.
    """
    body: bytes = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    header: bytes = struct.pack(LENGTH_PREFIX_FMT, len(body))
    return header + body


# ── Decode ────────────────────────────────────────────────────────────────────

def decode_message(sock) -> Dict[str, Any]:
    """
    Read exactly one message from a socket, handling partial TCP reads correctly.

    Protocol:
        1. Read exactly 4 bytes → parse as big-endian uint32 → msg_len
        2. Read exactly msg_len bytes → UTF-8 decode → JSON parse

    Args:
        sock: A connected socket.socket instance (blocking mode).

    Returns:
        The decoded message as a Python dict.

    Raises:
        ConnectionError: If the socket closes mid-message.
        json.JSONDecodeError: If the payload is not valid JSON.
        struct.error: If the length header is malformed.
    """
    raw_len = _recv_exact(sock, LENGTH_PREFIX_BYTES)
    msg_len: int = struct.unpack(LENGTH_PREFIX_FMT, raw_len)[0]
    raw_body = _recv_exact(sock, msg_len)
    return json.loads(raw_body.decode("utf-8"))


# ── Internal ──────────────────────────────────────────────────────────────────

def _recv_exact(sock, n: int) -> bytes:
    """
    Loop until exactly n bytes have been read from sock.

    This is necessary because TCP does NOT guarantee that a single recv() call
    returns all the bytes you asked for — it can return anywhere from 1 to n
    bytes. This function accumulates chunks until the buffer is full.

    Args:
        sock: Connected blocking socket.
        n:    Exact number of bytes to read.

    Returns:
        Exactly n bytes.

    Raises:
        ConnectionError: If the connection closes before n bytes are received.
    """
    buf = bytearray()
    while len(buf) < n:
        remaining = n - len(buf)
        chunk = sock.recv(remaining)
        if not chunk:
            raise ConnectionError(
                f"Socket closed after {len(buf)} bytes; expected {n} bytes total."
            )
        buf.extend(chunk)
    return bytes(buf)


# ── Convenience constructors for command/response dicts ──────────────────────

def ok_response(value=None) -> Dict[str, Any]:
    """Build a success response dict."""
    return {"status": "OK", "value": value}


def err_response(message: str) -> Dict[str, Any]:
    """Build an error response dict."""
    return {"status": "ERR", "error": message}
