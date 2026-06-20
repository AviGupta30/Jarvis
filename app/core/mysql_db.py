"""
mysql_db.py — Jarvis Async MySQL Connection Pool
-------------------------------------------------
Manages the persistent MySQL database for long-term RAG memory.
Creates the jarvis_memory database and required tables on first boot.
Isolated from all other tool modules per JARVIS_ARCHITECTURE Rule #1.
"""

import logging
import aiomysql
from app.core.config import settings

logger = logging.getLogger(__name__)

_pool: aiomysql.Pool | None = None


async def get_mysql_pool() -> aiomysql.Pool:
    """Return the shared MySQL connection pool, initializing it if needed."""
    global _pool
    if _pool is None:
        await init_mysql()
    return _pool


async def init_mysql() -> None:
    """
    Initialize the MySQL connection pool and ensure all required tables exist.
    Safe to call multiple times — fully idempotent.
    """
    global _pool
    try:
        # Parse connection params from MYSQL_URL
        # Expected format: mysql+aiomysql://user:password@host/dbname
        url = settings.MYSQL_URL
        url_body = url.replace("mysql+aiomysql://", "").replace("mysql://", "")

        # Split user:pass@host/db
        user_pass, host_db = url_body.rsplit("@", 1)
        if ":" in user_pass:
            user, password = user_pass.split(":", 1)
        else:
            user, password = user_pass, ""

        if "/" in host_db:
            host_port, db_name = host_db.split("/", 1)
        else:
            host_port, db_name = host_db, "jarvis_memory"

        host = host_port.split(":")[0]
        port = int(host_port.split(":")[1]) if ":" in host_port else 3306

        # Step 1: Connect without DB to create it if it doesn't exist
        conn = await aiomysql.connect(
            host=host, port=port, user=user, password=password, autocommit=True
        )
        async with conn.cursor() as cur:
            await cur.execute(
                f"CREATE DATABASE IF NOT EXISTS `{db_name}` "
                f"CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
        conn.close()

        # Step 2: Create pool connected to the jarvis_memory database
        _pool = await aiomysql.create_pool(
            host=host,
            port=port,
            user=user,
            password=password,
            db=db_name,
            charset="utf8mb4",
            autocommit=True,
            minsize=2,
            maxsize=10,
        )

        # Step 3: Create tables
        async with _pool.acquire() as conn:
            async with conn.cursor() as cur:
                # Main conversation turns table
                await cur.execute("""
                    CREATE TABLE IF NOT EXISTS conversation_turns (
                        id           BIGINT AUTO_INCREMENT PRIMARY KEY,
                        session_id   VARCHAR(64)  NOT NULL,
                        turn_index   INT          NOT NULL DEFAULT 0,
                        role         ENUM('user','assistant') NOT NULL,
                        content      TEXT         NOT NULL,
                        content_hash VARCHAR(32)  NOT NULL,
                        timestamp    DATETIME     DEFAULT CURRENT_TIMESTAMP,
                        faiss_id     BIGINT       DEFAULT NULL,
                        topic_tags   VARCHAR(512) DEFAULT NULL,
                        INDEX idx_session   (session_id),
                        INDEX idx_timestamp (timestamp),
                        INDEX idx_hash      (content_hash),
                        INDEX idx_faiss     (faiss_id)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """)

                # FAISS ID counter table — keeps FAISS position in sync with MySQL
                await cur.execute("""
                    CREATE TABLE IF NOT EXISTS faiss_meta (
                        id       INT PRIMARY KEY DEFAULT 1,
                        next_id  BIGINT NOT NULL DEFAULT 0
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """)
                # Ensure the single meta row exists
                await cur.execute(
                    "INSERT IGNORE INTO faiss_meta (id, next_id) VALUES (1, 0)"
                )

        logger.info("✅ [mysql_db] MySQL pool initialized. Tables ready.")

    except Exception as e:
        logger.error(f"❌ [mysql_db] Failed to initialize MySQL: {e}")
        _pool = None
        raise


async def close_mysql() -> None:
    """Gracefully close the MySQL connection pool on server shutdown."""
    global _pool
    if _pool:
        _pool.close()
        await _pool.wait_closed()
        _pool = None
        logger.info("[mysql_db] MySQL pool closed.")
