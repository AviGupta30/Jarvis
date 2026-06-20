"""
scripts/init_rag_memory.py
---------------------------
One-time initialization script for Jarvis Long-Term RAG Memory.
Creates the MySQL database and tables, initializes an empty FAISS index.

Usage:
    python scripts/init_rag_memory.py

Safe to run multiple times -- fully idempotent.
"""

import asyncio
import sys
import os

# Force UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


async def main():
    print("=" * 60)
    print("  Jarvis Long-Term RAG Memory -- Initialization")
    print("=" * 60)

    # Step 1: Check dependencies
    print("\n[1/4] Checking dependencies...")
    missing = []
    try:
        import aiomysql
        print("  [OK] aiomysql")
    except ImportError:
        missing.append("aiomysql")
        print("  [MISSING] aiomysql")

    try:
        import faiss
        print("  [OK] faiss-cpu")
    except ImportError:
        missing.append("faiss-cpu")
        print("  [MISSING] faiss-cpu")

    try:
        from fastembed import TextEmbedding
        print("  [OK] fastembed (BAAI/bge-small-en-v1.5)")
    except ImportError:
        missing.append("fastembed")
        print("  [MISSING] fastembed")

    if missing:
        print(f"\n[FAIL] Missing packages: {', '.join(missing)}")
        print(f"   Fix: pip install {' '.join(missing)}")
        sys.exit(1)

    # Step 2: Load config
    print("\n[2/4] Loading configuration...")
    from app.core.config import settings
    print(f"  MYSQL_URL: {settings.MYSQL_URL}")

    # Step 3: Initialize MySQL
    print("\n[3/4] Initializing MySQL database and tables...")
    try:
        from app.core.mysql_db import init_mysql
        await init_mysql()
        print("  [OK] MySQL initialized. Database 'jarvis_memory' ready.")
        print("  [OK] Table 'conversation_turns' created/verified.")
        print("  [OK] Table 'faiss_meta' created/verified.")
    except Exception as e:
        print(f"  [FAIL] MySQL init failed: {e}")
        print("\n  Troubleshooting:")
        print("  - Is MySQL running? Try: net start MySQL80 (Windows)")
        print("  - Check credentials in .env: MYSQL_URL=mysql+aiomysql://root:@localhost/jarvis_memory")
        sys.exit(1)

    # Step 4: Initialize FAISS index
    print("\n[4/4] Initializing FAISS vector index...")
    try:
        from app.services.rag_memory import init_rag_memory, _DATA_DIR
        await init_rag_memory()
        from app.services.rag_memory import _faiss_index
        print(f"  [OK] FAISS index initialized (0 vectors).")
        print(f"  [OK] Index file: {_DATA_DIR / 'jarvis_faiss.index'}")
    except Exception as e:
        print(f"  [FAIL] FAISS init failed: {e}")
        sys.exit(1)

    # Done
    print("\n" + "=" * 60)
    print("  [DONE] Initialization complete!")
    print("  Jarvis long-term memory is ready.")
    print("")
    print("  What's next:")
    print("  - Start Jarvis: python -m uvicorn app.main:app --reload")
    print("  - Test recall:  curl -X POST http://localhost:8000/memory/recall")
    print("                       -H 'Content-Type: application/json'")
    print("                       -d '{\"query\": \"exam schedule\"}'")
    print("  - View stats:   curl http://localhost:8000/memory/stats")
    print("=" * 60)

    # Close pool
    try:
        from app.core.mysql_db import close_mysql
        await close_mysql()
    except Exception:
        pass


if __name__ == "__main__":
    asyncio.run(main())
