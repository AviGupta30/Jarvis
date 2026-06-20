"""
engine.py — Single-Writer Command Queue (Milestone 3)
=====================================================
The CacheEngine owns the LRUCache exclusively. It runs on exactly ONE thread
(the "writer thread"). All other threads (connection handlers) talk to it only
by putting requests onto a queue.Queue and blocking on a per-request response
queue.

Why single-writer instead of a global lock?
  - No lock contention: connection threads never fight over the hash map.
  - No deadlocks: there is nothing to deadlock — only one thread writes.
  - This is how Redis works internally (single-threaded event loop).
  - The queue.Queue is the synchronisation boundary; its internal lock is
    managed by Python's stdlib, not by us.

The engine also handles the SNAPSHOT pseudo-command, which is enqueued by the
SnapshotThread so that snapshot serialisation runs on the writer thread and
is never concurrent with a live write.
"""

import queue
import logging
import threading
import time
from typing import Any, Dict, Optional, Tuple

from neural_cache.lru import LRUCache
from neural_cache.protocol import ok_response, err_response
from neural_cache.persistence import WALWriter, SnapshotManager

logger = logging.getLogger("neural_cache.engine")

# Sentinel object used to signal the engine thread to stop cleanly.
_STOP_SENTINEL = object()


class CacheEngine:
    """
    Owns the LRUCache. Runs a single consumer loop on a dedicated thread.

    External interface:
        engine.queue.put((cmd_dict, response_queue))
        result = response_queue.get()   # blocks until engine replies
    """

    def __init__(
        self,
        capacity: int = 1024,
        wal_writer: Optional[WALWriter] = None,
        snapshot_manager: Optional[SnapshotManager] = None,
    ):
        self.cache = LRUCache(capacity=capacity)
        self.queue: queue.Queue[Tuple[Dict, queue.Queue]] = queue.Queue()
        self._wal = wal_writer
        self._snapshot = snapshot_manager
        self._thread: Optional[threading.Thread] = None
        self._running = False
        self._stats = {
            "gets": 0,
            "sets": 0,
            "dels": 0,
            "hits": 0,
            "misses": 0,
            "errors": 0,
        }

    # ── Lifecycle ─────────────────────────────────────────────────────────────

    def start(self) -> None:
        """Spawn the single writer thread. Call once at server boot."""
        if self._running:
            logger.warning("[Engine] Already running.")
            return
        self._running = True
        self._thread = threading.Thread(
            target=self._worker,
            daemon=True,
            name="CacheEngineThread",
        )
        self._thread.start()
        logger.info("[Engine] Writer thread started.")

    def stop(self) -> None:
        """Gracefully stop the engine writer thread."""
        self._running = False
        # Unblock the worker if it's waiting on an empty queue
        self.queue.put((_STOP_SENTINEL, None))
        if self._thread:
            self._thread.join(timeout=5)
        logger.info("[Engine] Writer thread stopped.")

    # ── Worker loop ───────────────────────────────────────────────────────────

    def _worker(self) -> None:
        """
        The single consumer loop. Runs on CacheEngineThread.
        Processes one command at a time — no locking required.
        """
        logger.info("[Engine] Worker loop running.")
        while True:
            try:
                item = self.queue.get(timeout=1.0)
            except queue.Empty:
                continue

            cmd, response_q = item

            # Stop signal
            if cmd is _STOP_SENTINEL:
                logger.info("[Engine] Stop sentinel received.")
                break

            try:
                result = self._dispatch(cmd)
            except Exception as e:
                logger.exception(f"[Engine] Unhandled error dispatching {cmd}: {e}")
                result = err_response(f"Internal engine error: {e}")
                self._stats["errors"] += 1

            if response_q is not None:
                response_q.put(result)

    # ── Dispatcher ────────────────────────────────────────────────────────────

    def _dispatch(self, cmd: Dict[str, Any]) -> Dict[str, Any]:
        """
        Route a command dict to the appropriate handler.
        All handlers return a response dict.
        """
        op = cmd.get("cmd", "").upper()

        if op == "PING":
            return self._handle_ping()
        elif op == "GET":
            return self._handle_get(cmd)
        elif op == "SET":
            return self._handle_set(cmd)
        elif op == "DEL":
            return self._handle_del(cmd)
        elif op == "STATS":
            return self._handle_stats()
        elif op == SnapshotManager.SNAPSHOT_CMD:
            return self._handle_snapshot()
        else:
            return err_response(f"Unknown command: {op!r}")

    # ── Command handlers ──────────────────────────────────────────────────────

    def _handle_ping(self) -> Dict[str, Any]:
        return ok_response("PONG")

    def _handle_get(self, cmd: Dict[str, Any]) -> Dict[str, Any]:
        key = cmd.get("key")
        if not key:
            return err_response("GET requires 'key'")

        self._stats["gets"] += 1
        value = self.cache.get(key)

        if value is None:
            self._stats["misses"] += 1
            return err_response("key not found")

        self._stats["hits"] += 1
        return ok_response(value)

    def _handle_set(self, cmd: Dict[str, Any]) -> Dict[str, Any]:
        key = cmd.get("key")
        value = cmd.get("value")
        if not key:
            return err_response("SET requires 'key'")
        if value is None:
            return err_response("SET requires 'value'")

        ttl = cmd.get("ttl")  # seconds, or None for no expiry

        # Coerce value to string — the LRU only stores strings
        value = str(value)

        self.cache.set(key, value, ttl=ttl)
        self._stats["sets"] += 1

        # WAL: append BEFORE replying to client (durability guarantee)
        if self._wal:
            self._wal.append({"cmd": "SET", "key": key, "value": value, "ttl": ttl})

        return ok_response(None)

    def _handle_del(self, cmd: Dict[str, Any]) -> Dict[str, Any]:
        key = cmd.get("key")
        if not key:
            return err_response("DEL requires 'key'")

        existed = self.cache.delete(key)
        self._stats["dels"] += 1

        if not existed:
            return err_response("key not found")

        # WAL: record the deletion
        if self._wal:
            self._wal.append({"cmd": "DEL", "key": key})

        return ok_response(None)

    def _handle_stats(self) -> Dict[str, Any]:
        stats = dict(self._stats)
        stats["cache_size"] = len(self.cache)
        stats["capacity"] = self.cache.capacity
        stats["evictions"] = self.cache.eviction_count
        hit_rate = (
            stats["hits"] / stats["gets"] * 100
            if stats["gets"] > 0
            else 0.0
        )
        stats["hit_rate_pct"] = round(hit_rate, 2)
        return ok_response(stats)

    def _handle_snapshot(self) -> Dict[str, Any]:
        if self._snapshot:
            data = self.cache.snapshot()
            self._snapshot.write(data)
            return ok_response(f"Snapshot written ({len(data)} keys)")
        return err_response("No snapshot manager configured")
