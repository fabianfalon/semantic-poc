import logging

from src.domain.document_repository import DocumentRepository
from src.domain.services import generate_embeddings_mock as generate_embeddings

logger = logging.getLogger(__name__)


class SearchDocumentsUseCase:
    def __init__(self, repository: DocumentRepository):
        self.repo = repository

    def execute(self, query: str, limit: int = 5) -> list[dict]:
        query_emb = generate_embeddings([query])[0]
        logger.info(f"Query embedding: {query_emb}")
        rows = self.repo.search_similar(query_emb, limit)
        logger.info(f"Search results: {rows}")
        # Transform results
        results = []
        for row in rows:
            distance = (
                float(row["distance"]) if isinstance(row, dict) or hasattr(row, "__getitem__") else float(row.distance)
            )
            similarity = round((1 - min(distance, 1.0)) * 100, 2)
            title = row["title"] if isinstance(row, dict) or hasattr(row, "__getitem__") else row.title
            chunk_id = row["id"] if isinstance(row, dict) or hasattr(row, "__getitem__") else row.id
            content = row["content"] if isinstance(row, dict) or hasattr(row, "__getitem__") else row.content
            results.append(
                {
                    "chunk_id": chunk_id,
                    "document_title": title,
                    "content": content,
                    "similarity": f"{similarity} %",
                }
            )
        return results
