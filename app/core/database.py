import asyncpg
from app.core.config import settings

pool = None

async def init_db():
    global pool
    pool = await asyncpg.create_pool(settings.DATABASE_URL)
    
    async with pool.acquire() as conn:
        # Ensure the pgvector extension is active
        await conn.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        
        # Create the knowledge_store table automatically if it doesn't exist
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_store (
                id SERIAL PRIMARY KEY,
                content TEXT,
                embedding VECTOR(384)
            );
        """)

async def get_db_pool():
    global pool
    if pool is None:
        await init_db()
    return pool
