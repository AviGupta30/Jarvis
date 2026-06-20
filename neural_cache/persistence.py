"""
persistence.py — WAL + Snapshot for Neural Cache (Milestone 6)
===============================================================
Two-layer crash-safety:

1. WAL (Write-Ahead Log) — wal.log
   Every SET/DEL is appended as a JSON line BEFORE the response is sent to the
   client. If the server crashes, no acknowledged write is lost — they all live
   in the WAL. Cheap sequential disk writes only.

2. Snapshot — snapshot.rdb
   Every SNAPSHOT_INTERVAL_SECONDS (default 300), the engine serialises the
   entire live hash map to a pickle file, then truncates wal.log to empty
   (since the snapshot captures everything up to that point).

Startup recovery sequence (performed in server.py before the engine starts):
   a. Load snapshot.rdb → restore base state into LRUCache
   b. Replay wal.log on top → apply any writes since the last snapshot
   c. Start engine, server, snapshot background thread

WAL format: one JSON object per line.
  {"cmd": "SET", "key": "x", "value": "1", "ttl": null}
  {"cmd": "DEL", "key": "x"}
"""

import json
import pickle
import queue
import threading
import time
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional

logger = logging.getLogger("neural_cache.persistence")


# ── WALWriter ─────────────────────────────────────────────────────────────────

class WALWriter:
    """
    Append-only write-ahead log.

    Each SET/DEL command is written as a JSON line before the engine replies
    to the client — guaranteeing durability of every acknowledged write.

    The WAL is truncated (NOT deleted) after a successful snapshot so that
    the file handle stays valid for subsequent appends.
    """

    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        # Open in append mode. 'a' creates the file if it doesn't exist.
        self._fh = open(self.path, "a", encoding="utf-8")
        logger.info(f"[WAL] Opened log at {self.path}")

    def append(self, cmd: Dict[str, Any]) -> None:
        """
        Append one command to the WAL and flush immediately.

        Flushing on every write is intentional — it ensures the OS kernel
        has the data before we tell the client "OK". Without flush(), a
        crash could lose the last few writes that were still in the userspace
        buffer. The performance cost is a single system call per write, which
        is acceptable for a localhost server.
        """
        try:
            line = json.dumps(cmd, ensure_ascii=False) + "\n"
            self._fh.write(line)
            self._fh.flush()
        except Exception as e:
            logger.error(f"[WAL] append failed: {e}")

    def read_all(self) -> List[Dict[str, Any]]:
        """
        Read and parse all commands from the WAL file.
        Called once at startup for recovery. Skips malformed lines with a warning.
        """
        commands = []
        if not self.path.exists():
            return commands
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                for lineno, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        commands.append(json.loads(line))
                    except json.JSONDecodeError as e:
                        logger.warning(f"[WAL] Skipping malformed line {lineno}: {e}")
        except Exception as e:
            logger.error(f"[WAL] Could not read log: {e}")
        logger.info(f"[WAL] Replayed {len(commands)} commands from {self.path}")
        return commands

    def truncate(self) -> None:
        """
        Empty the WAL file after a successful snapshot.

        We truncate (overwrite with empty content) rather than delete so that
        the file descriptor remains open and subsequent appends work without
        needing to reopen the file.
        """
        try:
            self._fh.close()
            self.path.write_text("", encoding="utf-8")
            self._fh = open(self.path, "a", encoding="utf-8")
            logger.info("[WAL] Truncated after snapshot.")
        except Exception as e:
            logger.error(f"[WAL] Truncate failed: {e}")

    def close(self) -> None:
        """Flush and close the file handle cleanly on server shutdown."""
        try:
            self._fh.flush()
            self._fh.close()
        except Exception:
            pass


# ── SnapshotManager ───────────────────────────────────────────────────────────

class SnapshotManager:
    """
    Manages periodic full-state snapshots.

    The snapshot itself is triggered through the engine's command_queue so it
    executes on the single writer thread — never racing with a concurrent write.

    File format: pickle (safe here because both writer and reader are our own
    server code — we control both ends. JSON would work too but pickle is
    faster for large dicts and handles float precision correctly for expires_at).
    """

    SNAPSHOT_CMD = "__SNAPSHOT__"

    def __init__(self, path: Path, wal_writer: WALWriter):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.wal = wal_writer
        self._thread: Optional[threading.Thread] = None
        logger.info(f"[Snapshot] Snapshot path: {self.path}")

    def write(self, data: Dict[str, Any]) -> None:
        """
        Serialise cache state to disk and truncate the WAL.
        Called by CacheEngine on its own thread — no locking needed.
        """
        try:
            # Write to a temp file first, then rename — atomic on most OSes
            tmp = self.path.with_suffix(".tmp")
            with open(tmp, "wb") as f:
                pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
            tmp.replace(self.path)
            self.wal.truncate()
            logger.info(f"[Snapshot] Written {len(data)} keys to {self.path}")
        except Exception as e:
            logger.error(f"[Snapshot] Write failed: {e}")

    def read(self) -> Optional[Dict[str, Any]]:
        """
        Load the snapshot from disk. Returns None if no snapshot exists yet.
        Called once at startup before the engine starts.
        """
        if not self.path.exists():
            logger.info("[Snapshot] No snapshot found — starting fresh.")
            return None
        try:
            with open(self.path, "rb") as f:
                data = pickle.load(f)
            logger.info(f"[Snapshot] Loaded {len(data)} keys from {self.path}")
            return data
        except Exception as e:
            logger.error(f"[Snapshot] Could not load snapshot: {e}. Starting fresh.")
            return None

    def start_background_thread(
        self,
        command_queue: queue.Queue,
        interval_seconds: int = 300,
    ) -> None:
        """
        Start a daemon thread that enqueues a SNAPSHOT command every
        interval_seconds. The engine processes it on its own thread, so
        there is never a race with live writes.

        Args:
            command_queue:    The engine's command queue (shared reference).
            interval_seconds: How often to snapshot (default 5 minutes).
        """
        def _loop():
            while True:
                time.sleep(interval_seconds)
                response_q: queue.Queue = queue.Queue(maxsize=1)
                command_queue.put(({"cmd": self.SNAPSHOT_CMD}, response_q))
                try:
                    response_q.get(timeout=30)  # wait for engine to confirm
                except queue.Empty:
                    logger.warning("[Snapshot] Engine did not confirm snapshot within 30s.")

        self._thread = threading.Thread(target=_loop, daemon=True, name="SnapshotThread")
        self._thread.start()
        logger.info(f"[Snapshot] Background thread started (interval={interval_seconds}s).")
