import logging

from src.domain.document_repository import DocumentRepository
from src.domain.embeddings import EmbeddingGenerator

logger = logging.getLogger(__name__)


class SearchDocumentsUseCase:
    def __init__(self, repository: DocumentRepository, embeddings: EmbeddingGenerator):
        self.repo = repository
        self.embeddings = embeddings

    def execute(self, query: str, limit: int = 5, min_similarity: float = 0.0) -> list[dict]:
        query_emb = self.embeddings.embed([query])[0]
        logger.info(f"Query embedding: {query_emb}")
        rows = self.repo.search_similar(query_emb, limit, min_similarity)
        logger.info(f"Search results: {rows}")
        # Transform results
        results = []
        for row in rows:
            sim_val = (
                float(row["similarity"])
                if isinstance(row, dict) or hasattr(row, "__getitem__")
                else float(row.similarity)
            )
            if sim_val < min_similarity:
                continue
            similarity_pct = round(sim_val * 100, 2)
            title = row["title"] if isinstance(row, dict) or hasattr(row, "__getitem__") else row.title
            chunk_id = row["id"] if isinstance(row, dict) or hasattr(row, "__getitem__") else row.id
            content = row["content"] if isinstance(row, dict) or hasattr(row, "__getitem__") else row.content
            results.append(
                {
                    "chunk_id": chunk_id,
                    "document_title": title,
                    "content": content,
                    "similarity": f"{similarity_pct} %",
                }
            )
        return results
