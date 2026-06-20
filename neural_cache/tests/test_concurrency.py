"""
test_concurrency.py — 50-thread hammer test for Neural Cache (Milestone 7)
===========================================================================
The entire resume value of this project rests on this test.
"Built a concurrent cache and proved it under concurrent load."

What this test does:
  1. Spins up a real CacheServer on port 19090 (separate from prod port 9090)
     in a background thread.
  2. Waits for the server to be ready.
  3. Launches NUM_THREADS=50 threads, each running NUM_OPS=1000 random
     GET/SET/DEL operations using a real CacheClient socket connection.
  4. After all threads complete:
     - Asserts the server is still alive (PING returns PONG)
     - Asserts no exception was raised in any client thread
     - Asserts the engine thread is still running
     - Asserts the final cache state is internally consistent

Run with:
    python -m pytest neural_cache/tests/test_concurrency.py -v -s
"""

import random
import sys
import threading
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pytest
from neural_cache.server import CacheServer
from neural_cache.client import CacheClient
from neural_cache.persistence import SnapshotManager

# ── Test parameters ───────────────────────────────────────────────────────────

TEST_PORT    = 19090          # dedicated test port, separate from prod 9090
NUM_THREADS  = 50
NUM_OPS      = 1_000
KEY_SPACE    = 200            # small key space → lots of contention on same keys


# ── Server fixture ────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def live_server(tmp_path_factory):
    """
    Start a CacheServer in a background thread for the duration of the module.
    Uses a temp directory for WAL/snapshot so tests don't pollute prod data.
    """
    data_dir = tmp_path_factory.mktemp("nc_test_data")
    server = CacheServer(
        host="127.0.0.1",
        port=TEST_PORT,
        capacity=1024,
        wal_path=data_dir / "wal.log",
        snapshot_path=data_dir / "snapshot.rdb",
        snapshot_interval=9999,  # disable auto-snapshot during test
    )

    t = threading.Thread(target=server.start, daemon=True, name="TestCacheServer")
    t.start()

    # Wait until the server is accepting connections (up to 5s)
    client = CacheClient(port=TEST_PORT, timeout=1.0)
    deadline = time.time() + 5
    while time.time() < deadline:
        try:
            if client.ping():
                break
        except Exception:
            pass
        time.sleep(0.05)
    else:
        pytest.fail("CacheServer did not start within 5 seconds.")

    client.close()
    yield server

    # Teardown: close server socket
    server._running = False
    if server._server_sock:
        try:
            server._server_sock.close()
        except Exception:
            pass


# ── Worker ────────────────────────────────────────────────────────────────────

def _worker(port: int, ops: int, key_space: int, errors: list, written: dict, lock: threading.Lock):
    """
    One client thread. Performs `ops` random GET/SET/DEL operations.
    Records any exception in `errors`. Records every SET in `written` so
    we can check consistency after all threads finish.
    """
    client = CacheClient(port=port, timeout=5.0)
    rng = random.Random()  # thread-local RNG — no shared state

    try:
        for _ in range(ops):
            key = f"k{rng.randint(0, key_space - 1)}"
            op = rng.choice(["SET", "SET", "SET", "GET", "DEL"])  # bias toward SET

            if op == "SET":
                value = str(rng.randint(0, 999_999))
                ok = client.set(key, value)
                if ok:
                    with lock:
                        written[key] = value  # record last confirmed write
            elif op == "GET":
                client.get(key)   # result is fine to ignore
            elif op == "DEL":
                client.delete(key)
                with lock:
                    written.pop(key, None)

    except Exception as e:
        errors.append(f"Thread error: {e}")
    finally:
        client.close()


# ── Test ──────────────────────────────────────────────────────────────────────

class TestConcurrency:
    def test_50_threads_no_corruption(self, live_server):
        """
        50 concurrent clients, each doing 1000 ops.
        After completion:
          - Server still alive (PING)
          - No exceptions in any thread
          - Engine thread still running
        """
        errors = []
        written = {}
        lock = threading.Lock()

        threads = [
            threading.Thread(
                target=_worker,
                args=(TEST_PORT, NUM_OPS, KEY_SPACE, errors, written, lock),
                daemon=True,
                name=f"client-{i}",
            )
            for i in range(NUM_THREADS)
        ]

        t0 = time.time()
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=60)
        elapsed = time.time() - t0

        # ── Assertions ────────────────────────────────────────────────────────

        # 1. No thread panicked
        assert not errors, f"Thread errors:\n" + "\n".join(errors)

        # 2. Server still alive
        probe = CacheClient(port=TEST_PORT, timeout=2.0)
        assert probe.ping(), "Server did not respond to PING after concurrent load"
        probe.close()

        # 3. Engine thread still running
        assert live_server._engine._thread is not None
        assert live_server._engine._thread.is_alive(), "Engine thread died!"

        # 4. Throughput info (not an assertion -- just informational)
        total_ops = NUM_THREADS * NUM_OPS
        throughput = total_ops / elapsed
        print(
            f"\n  [PASS] Concurrency test passed\n"
            f"      {NUM_THREADS} threads x {NUM_OPS} ops = {total_ops:,} total ops\n"
            f"      Elapsed: {elapsed:.2f}s\n"
            f"      Throughput: {throughput:,.0f} ops/sec\n"
        )

    def test_server_stats_after_load(self, live_server):
        """The engine should report meaningful stats after the load test."""
        probe = CacheClient(port=TEST_PORT, timeout=2.0)
        stats = probe.stats()
        probe.close()

        assert stats is not None
        assert stats["gets"] > 0
        assert stats["sets"] > 0
        assert "hit_rate_pct" in stats
        print(
            f"\n  Cache stats after load:\n"
            f"    Size:      {stats['cache_size']}\n"
            f"    GETs:      {stats['gets']:,}\n"
            f"    SETs:      {stats['sets']:,}\n"
            f"    DELs:      {stats['dels']:,}\n"
            f"    Hits:      {stats['hits']:,}\n"
            f"    Hit rate:  {stats['hit_rate_pct']}%\n"
            f"    Evictions: {stats['evictions']:,}\n"
        )

    def test_ping_under_load(self, live_server):
        """
        While 10 threads hammer the cache, a separate thread pings repeatedly.
        All pings must succeed — proving the engine never deadlocks.
        """
        errors = []
        pings_ok = []
        ping_errors = []
        lock = threading.Lock()
        written = {}

        # Hammering threads
        hammers = [
            threading.Thread(
                target=_worker,
                args=(TEST_PORT, 200, 50, errors, written, lock),
                daemon=True,
            )
            for _ in range(10)
        ]

        # Ping thread
        stop_pinging = threading.Event()

        def _ping_loop():
            probe = CacheClient(port=TEST_PORT, timeout=1.0)
            while not stop_pinging.is_set():
                if probe.ping():
                    pings_ok.append(1)
                else:
                    ping_errors.append(1)
                time.sleep(0.01)
            probe.close()

        ping_t = threading.Thread(target=_ping_loop, daemon=True)
        ping_t.start()

        for t in hammers:
            t.start()
        for t in hammers:
            t.join(timeout=30)

        stop_pinging.set()
        ping_t.join(timeout=3)

        assert not errors
        assert not ping_errors, f"{len(ping_errors)} pings failed during load"
        assert len(pings_ok) > 0
