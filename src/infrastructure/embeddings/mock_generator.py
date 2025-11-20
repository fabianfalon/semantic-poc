import hashlib

import numpy as np

from src.domain.embeddings import EmbeddingGenerator


class MockEmbeddingGenerator(EmbeddingGenerator):
    def __init__(self, dims: int = 3072):
        self.dims = dims

    def embed(self, texts: list[str]) -> list[list[float]]:
        embeddings: list[list[float]] = []
        for t in texts:
            h = hashlib.sha256(t.encode("utf-8")).digest()
            seed = int.from_bytes(h[:8], byteorder="little", signed=False)
            rng = np.random.default_rng(seed)
            vec = rng.standard_normal(self.dims)
            norm = np.linalg.norm(vec) or 1.0
            embeddings.append((vec / norm).astype(float).tolist())
        return embeddings

    def embed_query(self, text: str) -> list[float]:
        h = hashlib.sha256(text.encode("utf-8")).digest()
        seed = int.from_bytes(h[:8], byteorder="little", signed=False)
        rng = np.random.default_rng(seed)
        vec = rng.standard_normal(self.dims)
        norm = np.linalg.norm(vec) or 1.0
        return (vec / norm).astype(float).tolist()
