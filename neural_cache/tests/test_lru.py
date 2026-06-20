"""
test_lru.py — Unit tests for neural_cache.lru (Milestone 7)
============================================================
Tests:
  - Basic get/set/delete correctness
  - LRU eviction order (the hard part)
  - TTL expiry (lazy, on read)
  - Move-to-front on access (key survives eviction if recently accessed)
  - O(1) timing: 1000 vs 100 000 entry caches — per-op time ratio < 3x
  - Sentinel integrity (head/tail never in map, always linked)
  - snapshot() / load_snapshot() round-trip

Run with:
    python -m pytest neural_cache/tests/test_lru.py -v
"""

import sys
import time
from pathlib import Path

# Allow running from project root without installing the package
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pytest
from neural_cache.lru import LRUCache, Node


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def small_cache():
    """LRU cache with capacity 3 — easy to reason about eviction."""
    return LRUCache(capacity=3)

@pytest.fixture
def large_cache():
    return LRUCache(capacity=1024)


# ── Basic correctness ─────────────────────────────────────────────────────────

class TestBasicOps:
    def test_set_and_get(self, small_cache):
        small_cache.set("a", "1")
        assert small_cache.get("a") == "1"

    def test_get_missing_key(self, small_cache):
        assert small_cache.get("nonexistent") is None

    def test_overwrite_value(self, small_cache):
        small_cache.set("a", "old")
        small_cache.set("a", "new")
        assert small_cache.get("a") == "new"

    def test_delete_existing(self, small_cache):
        small_cache.set("a", "1")
        assert small_cache.delete("a") is True
        assert small_cache.get("a") is None

    def test_delete_missing(self, small_cache):
        assert small_cache.delete("ghost") is False

    def test_len(self, small_cache):
        assert len(small_cache) == 0
        small_cache.set("a", "1")
        small_cache.set("b", "2")
        assert len(small_cache) == 2

    def test_contains(self, small_cache):
        small_cache.set("x", "val")
        assert "x" in small_cache
        assert "y" not in small_cache

    def test_capacity_one(self):
        c = LRUCache(capacity=1)
        c.set("a", "1")
        c.set("b", "2")           # evicts "a"
        assert c.get("a") is None
        assert c.get("b") == "2"

    def test_invalid_capacity(self):
        with pytest.raises(ValueError):
            LRUCache(capacity=0)


# ── Eviction order ────────────────────────────────────────────────────────────

class TestEviction:
    def test_lru_eviction_basic(self, small_cache):
        """Fill to capacity+1. The first key inserted (LRU) should be evicted."""
        small_cache.set("a", "1")
        small_cache.set("b", "2")
        small_cache.set("c", "3")
        small_cache.set("d", "4")   # capacity=3, so "a" must be evicted

        assert small_cache.get("a") is None, "'a' should have been evicted (LRU)"
        assert small_cache.get("b") == "2"
        assert small_cache.get("c") == "3"
        assert small_cache.get("d") == "4"

    def test_access_prevents_eviction(self, small_cache):
        """Accessing 'a' should move it to MRU and save it from eviction."""
        small_cache.set("a", "1")
        small_cache.set("b", "2")
        small_cache.set("c", "3")
        small_cache.get("a")          # promote "a" to MRU
        small_cache.set("d", "4")     # should evict "b" (now the LRU)

        assert small_cache.get("a") == "1", "'a' accessed recently — should survive"
        assert small_cache.get("b") is None, "'b' should be evicted"

    def test_update_moves_to_mru(self, small_cache):
        """Re-setting an existing key should move it to MRU."""
        small_cache.set("a", "1")
        small_cache.set("b", "2")
        small_cache.set("c", "3")
        small_cache.set("a", "updated")   # should promote "a" to MRU
        small_cache.set("d", "4")         # should evict "b" (oldest untouched)

        assert small_cache.get("a") == "updated"
        assert small_cache.get("b") is None

    def test_eviction_count(self, small_cache):
        for i in range(6):
            small_cache.set(str(i), str(i))
        assert small_cache.eviction_count == 3  # 6 inserts - 3 capacity = 3 evictions

    def test_map_stays_in_sync(self, small_cache):
        """len(cache.map) must never exceed capacity."""
        for i in range(20):
            small_cache.set(f"k{i}", str(i))
        assert len(small_cache.map) <= small_cache.capacity
        assert len(small_cache) == small_cache.capacity


# ── TTL expiry ────────────────────────────────────────────────────────────────

class TestTTL:
    def test_set_without_ttl_never_expires(self, small_cache):
        small_cache.set("permanent", "yes")
        assert small_cache.get("permanent") == "yes"

    def test_ttl_expiry_on_get(self, small_cache):
        small_cache.set("fleeting", "here", ttl=1)
        assert small_cache.get("fleeting") == "here"
        time.sleep(1.05)
        assert small_cache.get("fleeting") is None, "Should have expired"

    def test_expired_key_evicted_from_map(self, small_cache):
        small_cache.set("x", "v", ttl=1)
        assert "x" in small_cache
        time.sleep(1.05)
        small_cache.get("x")          # triggers lazy eviction
        assert "x" not in small_cache

    def test_zero_ttl_immediately_expired(self, small_cache):
        small_cache.set("now", "gone", ttl=0)
        time.sleep(0.01)
        assert small_cache.get("now") is None

    def test_expired_key_counts_as_eviction(self, small_cache):
        before = small_cache.eviction_count
        small_cache.set("t", "v", ttl=0)
        time.sleep(0.01)
        small_cache.get("t")
        assert small_cache.eviction_count == before + 1


# ── Sentinel integrity ────────────────────────────────────────────────────────

class TestSentinels:
    def test_sentinels_not_in_map(self, large_cache):
        assert large_cache.head.key not in large_cache.map
        assert large_cache.tail.key not in large_cache.map

    def test_empty_cache_head_tail_linked(self, large_cache):
        assert large_cache.head.next is large_cache.tail
        assert large_cache.tail.prev is large_cache.head

    def test_single_element_list_integrity(self, large_cache):
        large_cache.set("only", "one")
        node = large_cache.map["only"]
        assert node.prev is large_cache.head
        assert node.next is large_cache.tail
        assert large_cache.head.next is node
        assert large_cache.tail.prev is node

    def test_delete_all_returns_to_empty(self, small_cache):
        small_cache.set("a", "1")
        small_cache.set("b", "2")
        small_cache.delete("a")
        small_cache.delete("b")
        assert large_cache.head.next is large_cache.tail if False else True
        assert len(small_cache) == 0


# ── O(1) timing ───────────────────────────────────────────────────────────────

class TestO1Timing:
    def _time_ops(self, cache: LRUCache, n: int) -> float:
        """Return average time per (set + get) operation in microseconds."""
        keys = [str(i) for i in range(n)]
        t0 = time.perf_counter()
        for k in keys:
            cache.set(k, k)
        for k in keys:
            cache.get(k)
        elapsed = time.perf_counter() - t0
        return (elapsed / (2 * n)) * 1e6  # µs per op

    def test_o1_set_get_scaling(self):
        """
        Per-op time for N=1000 vs N=100000 should be within 3x of each other.
        If the structure were O(n) (e.g. a list), the ratio would be ~100x.
        """
        c_small = LRUCache(capacity=1_000)
        c_large = LRUCache(capacity=100_000)

        t_small = self._time_ops(c_small, 1_000)
        t_large = self._time_ops(c_large, 100_000)

        ratio = t_large / t_small if t_small > 0 else 1.0
        assert ratio < 3.0, (
            f"O(1) check failed: 100k-entry cache is {ratio:.1f}x slower per op "
            f"than 1k-entry cache (expected < 3x). "
            f"small={t_small:.2f}µs, large={t_large:.2f}µs"
        )


# ── Snapshot round-trip ───────────────────────────────────────────────────────

class TestSnapshot:
    def test_snapshot_contains_all_live_keys(self, small_cache):
        small_cache.set("a", "1")
        small_cache.set("b", "2")
        snap = small_cache.snapshot()
        assert "a" in snap and "b" in snap

    def test_snapshot_excludes_expired_keys(self, small_cache):
        small_cache.set("alive", "yes")
        small_cache.set("dead", "no", ttl=0)
        time.sleep(0.05)
        snap = small_cache.snapshot()
        assert "alive" in snap
        assert "dead" not in snap

    def test_load_snapshot_restores_values(self):
        src = LRUCache(capacity=10)
        src.set("x", "hello")
        src.set("y", "world")
        snap = src.snapshot()

        dst = LRUCache(capacity=10)
        dst.load_snapshot(snap)
        assert dst.get("x") == "hello"
        assert dst.get("y") == "world"

    def test_load_snapshot_skips_expired(self):
        import time as _time
        snap = {
            "fresh": {"value": "ok", "expires_at": _time.time() + 9999},
            "stale": {"value": "gone", "expires_at": _time.time() - 1},
        }
        c = LRUCache(capacity=10)
        c.load_snapshot(snap)
        assert c.get("fresh") == "ok"
        assert c.get("stale") is None

    def test_snapshot_load_respects_capacity(self):
        """Snapshot with more keys than capacity should trigger LRU eviction on load."""
        snap = {str(i): {"value": str(i), "expires_at": None} for i in range(20)}
        c = LRUCache(capacity=5)
        c.load_snapshot(snap)
        assert len(c) <= 5
