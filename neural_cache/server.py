"""
server.py — TCP Accept Loop for Neural Cache (Milestone 4)
==========================================================
Accepts incoming socket connections, spawns one thread per client, and wires
each connection to the CacheEngine via its command queue.

Architecture:
  MainThread:         binds socket → starts engine → accept loop
  Per-connection:     _handle_client() thread (one per active client)
  CacheEngineThread:  single writer, owns the hash map

Connection threads are I/O-bound. They never touch the LRUCache directly —
they only enqueue (cmd, response_queue) pairs and block waiting for the reply.

Startup sequence:
  1. Load snapshot from disk
  2. Replay WAL on top of snapshot
  3. Start engine writer thread
  4. Start snapshot background thread
  5. Bind and accept connections

Run with:
  python -m neural_cache.server [--host HOST] [--port PORT] [--capacity N]
  python neural_cache/server.py
"""

import argparse
import logging
import queue
import signal
import socket
import sys
import threading
from pathlib import Path
from typing import Optional

# Add project root to sys.path so this works when run directly
_HERE = Path(__file__).resolve().parent
_PROJECT_ROOT = _HERE.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from neural_cache.engine import CacheEngine
from neural_cache.persistence import WALWriter, SnapshotManager
from neural_cache import protocol

# ── Logging setup ─────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s  %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("neural_cache.server")

# ── Default paths ─────────────────────────────────────────────────────────────

_DATA_DIR       = _HERE / "data"
_WAL_PATH       = _DATA_DIR / "wal.log"
_SNAPSHOT_PATH  = _DATA_DIR / "snapshot.rdb"


# ── CacheServer ───────────────────────────────────────────────────────────────

class CacheServer:
    """
    TCP server that wires incoming connections to the CacheEngine.

    Each accepted connection gets its own _handle_client() thread.
    That thread owns the socket I/O — read a message, enqueue it to the engine,
    wait for the response, write the response back.
    """

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 9090,
        capacity: int = 1024,
        wal_path: Path = _WAL_PATH,
        snapshot_path: Path = _SNAPSHOT_PATH,
        snapshot_interval: int = 300,
    ):
        self.host = host
        self.port = port
        self.capacity = capacity
        self._server_sock: Optional[socket.socket] = None
        self._running = False

        # ── Persistence ──────────────────────────────────────────────────────
        wal_path.parent.mkdir(parents=True, exist_ok=True)
        self._wal = WALWriter(wal_path)
        self._snapshot_mgr = SnapshotManager(snapshot_path, self._wal)
        self._snapshot_interval = snapshot_interval

        # ── Engine ───────────────────────────────────────────────────────────
        self._engine = CacheEngine(
            capacity=capacity,
            wal_writer=self._wal,
            snapshot_manager=self._snapshot_mgr,
        )

    # ── Startup ───────────────────────────────────────────────────────────────

    def start(self) -> None:
        """Full startup: recover state, start engine, begin accepting connections."""
        self._recover_state()
        self._engine.start()
        self._snapshot_mgr.start_background_thread(
            self._engine.queue, self._snapshot_interval
        )
        self._accept_loop()

    def _recover_state(self) -> None:
        """
        Restore cache state from disk before the engine thread starts.
        Called on the main thread — no concurrency, no locking needed.

        Steps:
            a) Load snapshot.rdb → restore base state
            b) Replay wal.log on top → recover writes since last snapshot
        """
        snapshot_data = self._snapshot_mgr.read()
        if snapshot_data:
            self._engine.cache.load_snapshot(snapshot_data)
            logger.info(f"[Server] Restored {len(snapshot_data)} keys from snapshot.")

        wal_commands = self._wal.read_all()
        replayed = 0
        for cmd in wal_commands:
            op = cmd.get("cmd", "").upper()
            if op == "SET":
                self._engine.cache.set(
                    cmd["key"], cmd["value"], ttl=cmd.get("ttl")
                )
                replayed += 1
            elif op == "DEL":
                self._engine.cache.delete(cmd["key"])
                replayed += 1
        if replayed:
            logger.info(f"[Server] Replayed {replayed} WAL commands.")

    # ── Accept loop ───────────────────────────────────────────────────────────

    def _accept_loop(self) -> None:
        """Main thread: bind socket and accept connections indefinitely."""
        self._server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_sock.bind((self.host, self.port))
        self._server_sock.listen(128)
        self._running = True

        logger.info(
            f"[Server] Neural Cache listening on {self.host}:{self.port} "
            f"(capacity={self.capacity})"
        )
        print(
            f"\n  [Neural Cache] Listening on {self.host}:{self.port}"
            f"  |  capacity={self.capacity} entries\n"
        )

        try:
            while self._running:
                try:
                    conn, addr = self._server_sock.accept()
                    conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                    t = threading.Thread(
                        target=self._handle_client,
                        args=(conn, addr),
                        daemon=True,
                        name=f"client-{addr[1]}",
                    )
                    t.start()
                except OSError:
                    if self._running:
                        raise
        finally:
            self._shutdown()

    # ── Per-client handler ────────────────────────────────────────────────────

    def _handle_client(self, conn: socket.socket, addr) -> None:
        """
        One thread per connected client.
        Reads commands, enqueues them to the engine, sends responses back.

        This thread is purely I/O-bound — it never touches self._engine.cache.
        """
        logger.debug(f"[Server] Client connected: {addr}")
        try:
            while True:
                try:
                    cmd = protocol.decode_message(conn)
                except ConnectionError:
                    # Client closed the connection — normal exit
                    break
                except Exception as e:
                    logger.warning(f"[Server] Protocol error from {addr}: {e}")
                    break

                # Hand off to the engine and wait for the response
                response_q: queue.Queue = queue.Queue(maxsize=1)
                self._engine.queue.put((cmd, response_q))
                try:
                    result = response_q.get(timeout=10)
                except queue.Empty:
                    result = protocol.err_response("Engine timeout — server may be overloaded")

                try:
                    conn.sendall(protocol.encode_message(result))
                except Exception as e:
                    logger.warning(f"[Server] Send failed to {addr}: {e}")
                    break
        finally:
            conn.close()
            logger.debug(f"[Server] Client disconnected: {addr}")

    # ── Shutdown ──────────────────────────────────────────────────────────────

    def _shutdown(self) -> None:
        """Graceful shutdown: take a final snapshot, stop engine, close socket."""
        logger.info("[Server] Shutting down...")
        # Final snapshot
        try:
            response_q: queue.Queue = queue.Queue(maxsize=1)
            self._engine.queue.put(({"cmd": SnapshotManager.SNAPSHOT_CMD}, response_q))
            response_q.get(timeout=15)
        except Exception as e:
            logger.warning(f"[Server] Final snapshot failed: {e}")
        self._engine.stop()
        self._wal.close()
        if self._server_sock:
            try:
                self._server_sock.close()
            except Exception:
                pass
        logger.info("[Server] Shutdown complete.")


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Neural Cache — Redis-style in-memory KV store")
    parser.add_argument("--host",     default="127.0.0.1", help="Bind address (default: 127.0.0.1)")
    parser.add_argument("--port",     default=9090, type=int, help="TCP port (default: 9090)")
    parser.add_argument("--capacity", default=1024, type=int, help="LRU capacity in entries (default: 1024)")
    parser.add_argument("--snapshot-interval", default=300, type=int,
                        help="Snapshot interval in seconds (default: 300)")
    args = parser.parse_args()

    server = CacheServer(
        host=args.host,
        port=args.port,
        capacity=args.capacity,
        snapshot_interval=args.snapshot_interval,
    )

    # Graceful Ctrl+C
    def _sigint(sig, frame):
        logger.info("[Server] SIGINT received. Stopping...")
        server._running = False
        if server._server_sock:
            server._server_sock.close()

    signal.signal(signal.SIGINT, _sigint)

    server.start()


if __name__ == "__main__":
    main()
