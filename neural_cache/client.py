"""
client.py — Python Client Library for Neural Cache (Milestone 5)
================================================================
A thin, reusable Python wrapper that any JARVIS tool can import to
talk to the Neural Cache server without knowing anything about sockets
or the wire protocol.

Design goals:
  1. Lazy connect — opens the socket on first use, not on import.
  2. Auto-reconnect — if the connection drops, transparently reconnects
     on the next call. The caller sees a slight delay, not an exception.
  3. Graceful degradation — if the server is not running at all,
     every method returns None/False and logs a warning. No JARVIS tool
     should ever crash because the cache server is down.
  4. Thread-safe — a single CacheClient instance can be shared between
     threads (e.g., a module-level singleton). A threading.Lock guards
     the socket send/recv cycle to prevent interleaving.

Usage (anywhere in JARVIS):
    from neural_cache.client import CacheClient

    _cache = CacheClient()   # module-level singleton, reconnects automatically

    _cache.set("dsa_mode", "active", ttl=1800)   # → True on success
    val = _cache.get("dsa_mode")                  # → "active" or None
    _cache.delete("dsa_mode")                      # → True if existed
    _cache.ping()                                  # → True if server alive
"""

import logging
import socket
import threading
from typing import Any, Optional

from neural_cache import protocol

logger = logging.getLogger("neural_cache.client")

# ── Default connection settings ────────────────────────────────────────────────

DEFAULT_HOST    = "127.0.0.1"
DEFAULT_PORT    = 9090
DEFAULT_TIMEOUT = 2.0          # seconds — fast fail so JARVIS isn't sluggish


class CacheClient:
    """
    Thread-safe client for the Neural Cache server.

    One instance can be safely shared between multiple threads. Internally,
    a lock serialises the send→recv cycle so responses are never mixed up.
    """

    def __init__(
        self,
        host: str = DEFAULT_HOST,
        port: int = DEFAULT_PORT,
        timeout: float = DEFAULT_TIMEOUT,
    ):
        self._host = host
        self._port = port
        self._timeout = timeout
        self._sock: Optional[socket.socket] = None
        self._lock = threading.Lock()

    # ── Public API ────────────────────────────────────────────────────────────

    def ping(self) -> bool:
        """
        Send a PING and return True if the server replies PONG.
        Useful for health checks and startup assertions.
        """
        try:
            resp = self._send({"cmd": "PING"})
            return resp.get("value") == "PONG"
        except Exception:
            return False

    def get(self, key: str) -> Optional[str]:
        """
        Retrieve the value for a key, or None on miss / expiry / error.

        Args:
            key: Cache key (non-empty string).

        Returns:
            The stored string value, or None.
        """
        try:
            resp = self._send({"cmd": "GET", "key": key})
            if resp.get("status") == "OK":
                return resp.get("value")
            return None
        except Exception as e:
            logger.warning(f"[CacheClient] get({key!r}) failed: {e}")
            return None

    def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None,
    ) -> bool:
        """
        Store a key-value pair, optionally with a TTL.

        Args:
            key:   Cache key.
            value: Value to store (will be coerced to str by the engine).
            ttl:   Time-to-live in seconds. None = never expires.

        Returns:
            True on success, False on error.
        """
        try:
            cmd: dict = {"cmd": "SET", "key": key, "value": value}
            if ttl is not None:
                cmd["ttl"] = ttl
            resp = self._send(cmd)
            return resp.get("status") == "OK"
        except Exception as e:
            logger.warning(f"[CacheClient] set({key!r}) failed: {e}")
            return False

    def delete(self, key: str) -> bool:
        """
        Delete a key from the cache.

        Returns:
            True if the key existed and was deleted, False otherwise.
        """
        try:
            resp = self._send({"cmd": "DEL", "key": key})
            return resp.get("status") == "OK"
        except Exception as e:
            logger.warning(f"[CacheClient] delete({key!r}) failed: {e}")
            return False

    def stats(self) -> Optional[dict]:
        """
        Retrieve server statistics (hit rate, evictions, cache size, etc.).
        Returns None on error.
        """
        try:
            resp = self._send({"cmd": "STATS"})
            if resp.get("status") == "OK":
                return resp.get("value")
            return None
        except Exception as e:
            logger.warning(f"[CacheClient] stats() failed: {e}")
            return None

    def close(self) -> None:
        """Explicitly close the socket connection."""
        with self._lock:
            self._close_socket()

    # ── Internal ──────────────────────────────────────────────────────────────

    def _send(self, cmd: dict) -> dict:
        """
        Send a command and return the response. Thread-safe.

        Handles lazy connect and auto-reconnect transparently.

        Raises:
            ConnectionRefusedError: If the server is not reachable and
                                    reconnect also fails.
            Exception:              Any other socket / protocol error.
        """
        with self._lock:
            self._ensure_connected()
            try:
                self._sock.sendall(protocol.encode_message(cmd))
                return protocol.decode_message(self._sock)
            except (BrokenPipeError, ConnectionResetError, OSError):
                # Connection was dropped — reconnect and retry once
                logger.debug("[CacheClient] Connection lost. Reconnecting...")
                self._close_socket()
                self._ensure_connected()
                self._sock.sendall(protocol.encode_message(cmd))
                return protocol.decode_message(self._sock)

    def _ensure_connected(self) -> None:
        """
        Open a socket to the server if not already connected.
        Called within the lock — safe to mutate self._sock.
        """
        if self._sock is not None:
            return
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self._timeout)
            sock.connect((self._host, self._port))
            # After connect, switch to blocking mode with a timeout
            sock.settimeout(self._timeout)
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            self._sock = sock
            logger.debug(f"[CacheClient] Connected to {self._host}:{self._port}")
        except ConnectionRefusedError:
            logger.warning(
                f"[CacheClient] Cannot connect to Neural Cache at "
                f"{self._host}:{self._port}. Is the server running?"
            )
            raise

    def _close_socket(self) -> None:
        """Close self._sock, suppressing errors. Called within the lock."""
        if self._sock:
            try:
                self._sock.close()
            except Exception:
                pass
            self._sock = None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def __repr__(self) -> str:
        connected = "connected" if self._sock else "disconnected"
        return f"CacheClient({self._host}:{self._port}, {connected})"
