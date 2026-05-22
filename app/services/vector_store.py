from app.core.database import get_db_pool

async def save_document_chunk(content: str, embedding: list[float]):
    """
    Inserts text chunks and vectors into the knowledge_store table.
    """
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        # Convert list of floats to PostgreSQL vector string representation: '[1.0, 2.0, ...]'
        embedding_str = f"[{','.join(map(str, embedding))}]"
        
        await conn.execute(
            "INSERT INTO knowledge_store (content, embedding) VALUES ($1, $2::vector)",
            content,
            embedding_str
        )

async def search_similar_chunks(query_embedding: list[float], limit: int = 3) -> list[str]:
    """
    Queries the table and uses the pgvector cosine distance operator (<=>) to fetch the closest matches.
    """
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        embedding_str = f"[{','.join(map(str, query_embedding))}]"
        
        rows = await conn.fetch(
            "SELECT content FROM knowledge_store ORDER BY embedding <=> $1::vector LIMIT $2",
            embedding_str,
            limit
        )
        
        return [row["content"] for row in rows]
