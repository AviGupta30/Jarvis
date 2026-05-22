import asyncio
from concurrent.futures import ThreadPoolExecutor
from fastembed import TextEmbedding

# Load ONNX-based model once at startup — no PyTorch, no API, no 404s
_model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
_executor = ThreadPoolExecutor(max_workers=2)

async def get_embedding(text: str) -> list[float]:
    """
    Runs the local fastembed ONNX model in a thread pool
    so it doesn't block the async event loop.
    Returns a 384-dimensional float vector.
    """
    loop = asyncio.get_event_loop()
    embedding = await loop.run_in_executor(
        _executor,
        lambda: list(next(iter(_model.embed([text]))))
    )
    return embedding
