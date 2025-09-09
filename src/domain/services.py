import hashlib
import os

from openai import OpenAI

try:
    from src.config import settings  # type: ignore
except Exception:  # pragma: no cover
    settings = None  # type: ignore

api_key = None
if settings is not None:
    api_key = getattr(settings, "openai_api_key", None)

if not api_key:
    api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key) if api_key else None


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """
    Convierte lista de textos en embeddings con 3072 dimensiones.
    - Si USE_EMBEDDINGS_MOCK=true o no hay API key: usa el mock (3072 dims)
    - Si hay API key: usa OpenAI text-embedding-3-large (3072 dims)
    """
    use_mock = os.getenv("USE_EMBEDDINGS_MOCK", "false").lower() == "true" or client is None
    if use_mock:
        return generate_embeddings_mock(texts)

    response = client.embeddings.create(model="text-embedding-3-large", input=texts)
    return [data.embedding for data in response.data]


def generate_embeddings_mock(texts: list[str]) -> list[list[float]]:
    # Retorna vectores determinísticos de 3072 dimensiones por texto (semilla hash)
    import numpy as np

    embeddings: list[list[float]] = []
    for t in texts:
        h = hashlib.sha256(t.encode("utf-8")).digest()
        # Usamos los primeros 8 bytes para una semilla estable
        seed = int.from_bytes(h[:8], byteorder="little", signed=False)
        rng = np.random.default_rng(seed)
        vec = rng.standard_normal(3072)
        # Normalizamos a norma 1 para estabilidad numérica
        norm = np.linalg.norm(vec) or 1.0
        embeddings.append((vec / norm).astype(float).tolist())
    return embeddings
