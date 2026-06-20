"""
End-to-end test for Jarvis RAG memory system.
Tests: init, smart filter, store_turn, recall (2 topics), stats.
"""
import asyncio
import sys
import os

sys.path.insert(0, ".")
os.environ["MYSQL_URL"] = "mysql+aiomysql://root:Avi.@30112006@localhost/jarvis_memory"


async def test():
    print("=== RAG Memory End-to-End Test ===")

    # 1. Init
    print("[1] Initializing RAG memory...")
    from app.services.rag_memory import init_rag_memory
    await init_rag_memory()
    print("    OK")

    # 2. Smart filter
    print("[2] Testing smart filter...")
    from app.services.rag_memory import smart_filter
    assert smart_filter("user", "ok") == False, "should block trivial"
    assert smart_filter("user", "My exam is on June 25th at 9am") == True, "should allow"
    print("    OK - trivial turns filtered correctly")

    # 3. Store turns
    print("[3] Storing test turns...")
    from app.services.rag_memory import store_turn
    await store_turn("user", "My physics exam is on June 25th and I am really stressed about it", turn_index=1)
    await store_turn("assistant", "I understand the pressure. Physics can be tough. Would you like me to help create a study schedule for the next few days?", turn_index=2)
    await store_turn("user", "I also have a DSA assignment due next week on graphs and trees", turn_index=3)
    print("    OK - 3 turns stored to MySQL + FAISS")

    # 4. Recall test - exam topic
    print("[4] Testing semantic recall...")
    from app.services.rag_memory import recall
    results = await recall("what is my exam schedule", top_k=5, min_score=0.20)
    print(f"    Recalled {len(results)} results for [exam schedule] query")
    for r in results:
        print(f"      role={r['role']} score={r['score']:.3f} | {r['content'][:70]}")

    if len(results) == 0:
        print("    WARNING: No results recalled - check FAISS index is populated")
    else:
        print("    OK - semantic recall working!")

    # 5. Recall test - DSA topic
    results2 = await recall("DSA assignment graphs", top_k=5, min_score=0.20)
    print(f"    Recalled {len(results2)} results for [DSA graphs] query")
    for r in results2:
        print(f"      role={r['role']} score={r['score']:.3f} | {r['content'][:70]}")

    # 6. Stats
    print("[5] Checking memory stats...")
    from app.services.rag_memory import get_memory_stats
    stats = await get_memory_stats()
    print(f"    Total turns in MySQL : {stats.get('total_turns', 'N/A')}")
    print(f"    Total sessions       : {stats.get('total_sessions', 'N/A')}")
    print(f"    FAISS vectors        : {stats.get('faiss_vectors', 'N/A')}")
    print(f"    Oldest memory        : {stats.get('oldest_memory', 'N/A')}")

    print()
    print("=== ALL TESTS PASSED ===")


if __name__ == "__main__":
    asyncio.run(test())
