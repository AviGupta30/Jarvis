"""
lru.py — Hand-rolled LRU Cache (Milestone 1)
=============================================
Pure data structure: doubly-linked list + hash map.
- O(1) get / set / delete
- TTL support (expires_at stored as float unix timestamp)
- Sentinel head/tail nodes — no None-checks in hot path
- snapshot() / load_snapshot() for persistence integration
- NO use of collections.OrderedDict — the entire point is to build this ourselves

Thread-safety: this class is NOT thread-safe on its own.
All callers go through CacheEngine, which runs on a single writer thread.
"""

import time
from typing import Optional, Dict, Any


# ── Node ─────────────────────────────────────────────────────────────────────

class Node:
    """
    A doubly-linked list node holding one cache entry.

    Attributes:
        key        (str):   Cache key
        value      (str):   Stored value (always a string at the wire level)
        expires_at (float): Unix timestamp after which this entry is stale.
                            None means the entry never expires.
        prev       (Node):  Previous node in the list (towards head = MRU side)
        next       (Node):  Next node in the list (towards tail = LRU side)
    """
    __slots__ = ("key", "value", "expires_at", "prev", "next")

    def __init__(self, key: str = "", value: str = "", expires_at: Optional[float] = None):
        self.key = key
        self.value = value
        self.expires_at = expires_at
        self.prev: Optional["Node"] = None
        self.next: Optional["Node"] = None

    def is_expired(self) -> bool:
        """Return True if this entry has a TTL and it has elapsed."""
        if self.expires_at is None:
            return False
        return time.time() >= self.expires_at

    def __repr__(self) -> str:
        ttl_info = f", ttl={self.expires_at:.2f}" if self.expires_at else ""
        return f"Node(key={self.key!r}, value={self.value!r}{ttl_info})"


# ── LRUCache ─────────────────────────────────────────────────────────────────

class LRUCache:
    """
    O(1) Least-Recently-Used cache backed by:
      - dict[str, Node]  — hash map for O(1) key lookup
      - doubly linked list — ordered by recency (head=MRU, tail=LRU)

    The linked list uses two sentinel nodes (self.head, self.tail) so that
    _unlink() and _insert_after_head() never have to handle None neighbours.

    Layout after a few inserts:

        head(sentinel) <-> [most recent] <-> ... <-> [least recent] <-> tail(sentinel)

    Eviction always removes the node just before the tail sentinel.
    """

    def __init__(self, capacity: int = 1024):
        if capacity < 1:
            raise ValueError(f"Capacity must be >= 1, got {capacity}")

        self.capacity = capacity
        self.map: Dict[str, Node] = {}      # key → Node
        self.eviction_count: int = 0        # total evictions since start

        # Sentinel nodes — never stored in self.map
        self.head = Node("__HEAD__", "__HEAD__")  # MRU end
        self.tail = Node("__TAIL__", "__TAIL__")  # LRU end
        self.head.next = self.tail
        self.tail.prev = self.head

    # ── Public API ────────────────────────────────────────────────────────────

    def get(self, key: str) -> Optional[str]:
        """
        Return the value for key, or None on miss / expiry.
        On hit: moves node to the MRU position (front of list).
        On TTL expiry: evicts the node, returns None.
        O(1).
        """
        node = self.map.get(key)
        if node is None:
            return None

        if node.is_expired():
            self._evict(node)
            return None

        # Promote to MRU
        self._unlink(node)
        self._insert_after_head(node)
        return node.value

    def set(self, key: str, value: str, ttl: Optional[int] = None) -> None:
        """
        Insert or update a key-value pair.
        - If key already exists: update value + TTL, move to MRU.
        - If new key: create node, insert at MRU position.
        - If at capacity after insert: evict the LRU node.
        O(1).

        Args:
            key:   Cache key (string)
            value: Cache value (string)
            ttl:   Time-to-live in seconds. None = never expires.
        """
        expires_at = (time.time() + ttl) if ttl is not None else None

        if key in self.map:
            node = self.map[key]
            node.value = value
            node.expires_at = expires_at
            self._unlink(node)
            self._insert_after_head(node)
        else:
            node = Node(key, value, expires_at)
            self.map[key] = node
            self._insert_after_head(node)

            if len(self.map) > self.capacity:
                self._evict_tail()

    def delete(self, key: str) -> bool:
        """
        Remove a key from the cache.
        Returns True if the key existed, False if it was already absent.
        O(1).
        """
        node = self.map.get(key)
        if node is None:
            return False
        self._evict(node)
        return True

    def __len__(self) -> int:
        return len(self.map)

    def __contains__(self, key: str) -> bool:
        return key in self.map

    # ── Persistence helpers ───────────────────────────────────────────────────

    def snapshot(self) -> Dict[str, Any]:
        """
        Serialise the entire live cache to a plain dict.
        Expired entries are excluded — no point snapshotting stale data.
        Order is MRU → LRU for human readability; load_snapshot restores
        in insertion order which preserves a sensible eviction priority.
        """
        result = {}
        now = time.time()
        node = self.head.next
        while node is not self.tail:
            if node.expires_at is None or node.expires_at > now:
                result[node.key] = {
                    "value": node.value,
                    "expires_at": node.expires_at,
                }
            node = node.next
        return result

    def load_snapshot(self, data: Dict[str, Any]) -> None:
        """
        Restore cache state from a snapshot dict (produced by snapshot()).
        Called once at server startup before the engine thread begins.
        Skips already-expired entries gracefully.
        """
        now = time.time()
        for key, entry in data.items():
            expires_at = entry.get("expires_at")
            # Skip entries that expired while the server was offline
            if expires_at is not None and expires_at <= now:
                continue
            value = entry.get("value", "")
            node = Node(key, value, expires_at)
            self.map[key] = node
            # Insert at LRU end — we don't know original access order from disk
            self._insert_before_tail(node)
            if len(self.map) > self.capacity:
                self._evict_tail()

    # ── Internal linked-list operations ──────────────────────────────────────

    def _insert_after_head(self, node: Node) -> None:
        """Place node at the MRU (most-recently-used) end of the list."""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _insert_before_tail(self, node: Node) -> None:
        """Place node at the LRU (least-recently-used) end of the list."""
        node.next = self.tail
        node.prev = self.tail.prev
        self.tail.prev.next = node
        self.tail.prev = node

    def _unlink(self, node: Node) -> None:
        """Remove node from its current position in the list (O(1) because doubly-linked)."""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _evict(self, node: Node) -> None:
        """Evict a specific node (unlink + remove from map)."""
        self._unlink(node)
        del self.map[node.key]
        self.eviction_count += 1

    def _evict_tail(self) -> Optional[Node]:
        """
        Evict the LRU entry (the node just before the tail sentinel).
        Returns the evicted node, or None if the list was already empty.
        """
        lru_node = self.tail.prev
        if lru_node is self.head:
            return None  # list is empty
        self._evict(lru_node)
        return lru_node
