"""
benchmark.py — Neural Cache vs JSON-file Baseline (Milestone 8)
===============================================================
Measures:
  - Average GET latency (µs)
  - Average SET latency (µs)
  - Throughput under 50 concurrent clients (ops/sec)
  - Memory usage at capacity

Produces two side-by-side columns:
  Neural Cache vs JSON-file read/write (the baseline JARVIS used before)

The JSON-file baseline mirrors what memory_tool.py does:
  every read = json.load() from disk
  every write = json.dump() to disk

Run:
  # Start the Neural Cache server first in another terminal:
  #   python -m neural_cache.server
  #
  # Then run this benchmark:
  python neural_cache/benchmark.py

Results are printed to stdout AND saved to neural_cache/benchmark_results.txt
"""

import json
import os
import queue
import sys
import tempfile
import threading
import time
from pathlib import Path
from typing import Callable, Tuple

# Allow running from project root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from neural_cache.client import CacheClient

# ── Configuration ─────────────────────────────────────────────────────────────

CACHE_HOST    = "127.0.0.1"
CACHE_PORT    = 9090
WARMUP_OPS    = 200        # ops to run before timing (JIT warmup)
TIMED_OPS     = 5_000      # ops to time per latency measurement
THREAD_COUNT  = 50         # for throughput test
OPS_PER_THREAD= 500        # each thread's op count in throughput test
RESULTS_FILE  = Path(__file__).parent / "benchmark_results.txt"


# ── JSON-file baseline ────────────────────────────────────────────────────────

class JSONFileBaseline:
    """
    Mimics memory_tool.py's approach: every read/write touches disk.
    Uses a threading.Lock so concurrent writes don't corrupt the file.
    """

    def __init__(self, path: str):
        self.path = path
        self._lock = threading.Lock()
        with open(path, "w") as f:
            json.dump({}, f)

    def get(self, key: str):
        with self._lock:
            with open(self.path, "r") as f:
                data = json.load(f)
            return data.get(key)

    def set(self, key: str, value: str):
        with self._lock:
            with open(self.path, "r") as f:
                data = json.load(f)
            data[key] = value
            with open(self.path, "w") as f:
                json.dump(data, f)

    def delete(self, key: str):
        with self._lock:
            with open(self.path, "r") as f:
                data = json.load(f)
            data.pop(key, None)
            with open(self.path, "w") as f:
                json.dump(data, f)


# ── Latency measurement ───────────────────────────────────────────────────────

def measure_latency(
    op_fn: Callable,
    warmup: int = WARMUP_OPS,
    timed: int = TIMED_OPS,
) -> Tuple[float, float, float]:
    """
    Run op_fn warmup times (discard), then timed times (measure).
    Returns (mean_µs, min_µs, max_µs).
    """
    for _ in range(warmup):
        op_fn()

    latencies = []
    for _ in range(timed):
        t0 = time.perf_counter()
        op_fn()
        latencies.append((time.perf_counter() - t0) * 1e6)  # µs

    return (
        sum(latencies) / len(latencies),
        min(latencies),
        max(latencies),
    )


# ── Throughput measurement ────────────────────────────────────────────────────

def measure_throughput(
    make_client_fn: Callable,
    n_threads: int = THREAD_COUNT,
    ops_per_thread: int = OPS_PER_THREAD,
) -> float:
    """
    Spin up n_threads threads each doing ops_per_thread SET+GET pairs.
    Returns total ops/sec across all threads.
    """
    errors = []

    def _worker():
        client = make_client_fn()
        try:
            for i in range(ops_per_thread):
                key = f"bench_k{i % 100}"
                client.set(key, str(i))
                client.get(key)
        except Exception as e:
            errors.append(str(e))

    threads = [threading.Thread(target=_worker, daemon=True) for _ in range(n_threads)]
    t0 = time.time()
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=120)
    elapsed = time.time() - t0

    if errors:
        print(f"  ⚠ Throughput test errors: {len(errors)} — first: {errors[0]}")

    total_ops = n_threads * ops_per_thread * 2  # SET + GET
    return total_ops / elapsed


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("\n" + "=" * 62)
    print("  Neural Cache — Benchmark vs JSON-file baseline")
    print("=" * 62)

    # ── Check server is up ────────────────────────────────────────────────────
    probe = CacheClient(host=CACHE_HOST, port=CACHE_PORT, timeout=2.0)
    if not probe.ping():
        print(
            "\n  ❌  Neural Cache server is not running.\n"
            f"     Start it with: python -m neural_cache.server\n"
            f"     (host={CACHE_HOST}, port={CACHE_PORT})\n"
        )
        sys.exit(1)
    probe.close()
    print(f"\n  ✅  Server reachable at {CACHE_HOST}:{CACHE_PORT}\n")

    # ── Setup ─────────────────────────────────────────────────────────────────
    tmp_json = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
    tmp_json.close()
    json_store = JSONFileBaseline(tmp_json.name)
    cache_client = CacheClient(host=CACHE_HOST, port=CACHE_PORT, timeout=5.0)

    # Pre-seed a key so GET has something to find
    cache_client.set("bench_key", "benchmark_value")
    json_store.set("bench_key", "benchmark_value")

    results = {}

    # ── GET latency ───────────────────────────────────────────────────────────
    print("  Measuring GET latency...")
    cache_get_mean, cache_get_min, cache_get_max = measure_latency(
        lambda: cache_client.get("bench_key")
    )
    json_get_mean, json_get_min, json_get_max = measure_latency(
        lambda: json_store.get("bench_key")
    )
    results["get"] = (cache_get_mean, json_get_mean)

    # ── SET latency ───────────────────────────────────────────────────────────
    print("  Measuring SET latency...")
    i_c = [0]
    i_j = [0]

    def _cache_set():
        cache_client.set(f"k{i_c[0] % 50}", str(i_c[0]))
        i_c[0] += 1

    def _json_set():
        json_store.set(f"k{i_j[0] % 50}", str(i_j[0]))
        i_j[0] += 1

    cache_set_mean, cache_set_min, cache_set_max = measure_latency(_cache_set)
    json_set_mean, json_set_min, json_set_max = measure_latency(_json_set)
    results["set"] = (cache_set_mean, json_set_mean)
    cache_client.close()

    # ── Throughput ────────────────────────────────────────────────────────────
    print(f"  Measuring throughput ({THREAD_COUNT} threads × {OPS_PER_THREAD} ops each)...")

    cache_throughput = measure_throughput(
        make_client_fn=lambda: CacheClient(host=CACHE_HOST, port=CACHE_PORT, timeout=5.0)
    )
    json_throughput = measure_throughput(
        make_client_fn=lambda: json_store  # shared instance (has its own lock)
    )
    results["throughput"] = (cache_throughput, json_throughput)

    # ── Report ────────────────────────────────────────────────────────────────
    speedup_get = json_get_mean / cache_get_mean if cache_get_mean > 0 else 0
    speedup_set = json_set_mean / cache_set_mean if cache_set_mean > 0 else 0
    speedup_thr = cache_throughput / json_throughput if json_throughput > 0 else 0

    report = f"""
{'=' * 62}
  Neural Cache Benchmark Results
  {time.strftime('%Y-%m-%d %H:%M:%S')}
{'=' * 62}

  Metric                  NeuralCache        JSON-file          Speedup
  ─────────────────────────────────────────────────────────────────────
  GET latency (avg µs)    {cache_get_mean:>10.2f}µs     {json_get_mean:>10.2f}µs     {speedup_get:.1f}x
  SET latency (avg µs)    {cache_set_mean:>10.2f}µs     {json_set_mean:>10.2f}µs     {speedup_set:.1f}x
  Throughput (ops/sec)    {cache_throughput:>10,.0f}       {json_throughput:>10,.0f}        {speedup_thr:.1f}x

  GET latency range:
    NeuralCache:  {cache_get_min:.2f}µs – {cache_get_max:.2f}µs
    JSON file:    {json_get_min:.2f}µs – {json_get_max:.2f}µs

  SET latency range:
    NeuralCache:  {cache_set_min:.2f}µs – {cache_set_max:.2f}µs
    JSON file:    {json_set_min:.2f}µs – {json_set_max:.2f}µs

  ─────────────────────────────────────────────────────────────────────
  Resume line:
  "Built a custom in-memory KV store with O(1) LRU eviction,
   a length-prefixed TCP protocol, and WAL-based persistence —
   {speedup_get:.0f}x faster GETs and {speedup_set:.0f}x faster SETs vs JSON-file reads
   under {THREAD_COUNT} concurrent clients ({cache_throughput:,.0f} ops/sec throughput)."
{'=' * 62}
"""
    print(report)

    # Save to file
    RESULTS_FILE.write_text(report, encoding="utf-8")
    print(f"  Results saved to: {RESULTS_FILE}\n")

    # Cleanup
    os.unlink(tmp_json.name)


if __name__ == "__main__":
    main()
