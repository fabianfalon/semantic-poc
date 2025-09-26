import logging
from typing import Any

from src.domain.document_repository import DocumentRepository
from src.domain.services.document_processing_service import DocumentProcessingService
from src.domain.value_objects import SearchQuery

logger = logging.getLogger(__name__)


class SearchDocumentsUseCase:
    """Use case for searching documents"""

    def __init__(self, repository: DocumentRepository, processing_service: DocumentProcessingService):
        self.repository = repository
        self.processing_service = processing_service

    def execute(self, query: str, limit: int = 5, min_similarity: float = 0.0) -> dict[str, Any]:
        """Execute document search use case"""
        search_query = SearchQuery(text=query, limit=limit, min_similarity=min_similarity)

        # Generate query embedding (may throw EmbeddingGenerationException)
        query_embedding = self.processing_service.process_query(search_query.text)
        logger.info(f"Query embedding generated for: {search_query.text}")

        # Search in repository
        rows = self.repository.search_similar(
            query_embedding.to_list(), search_query.limit, search_query.min_similarity
        )

        logger.info(f"Found {len(rows)} search results")

        results = []
        for row in rows:
            try:
                # Extract data from result
                similarity_val = self._extract_similarity(row)
                title = self._extract_title(row)
                chunk_id = self._extract_chunk_id(row)
                content = self._extract_content(row)

                # Check minimum similarity
                if similarity_val < search_query.min_similarity:
                    continue

                # Format result
                similarity_pct = round(similarity_val * 100, 2)
                results.append(
                    {
                        "chunk_id": chunk_id,
                        "document_title": title,
                        "content": content,
                        "similarity": f"{similarity_pct}%",
                        "similarity_value": similarity_val,
                    }
                )

            except Exception as e:
                logger.warning(f"Error processing search result: {e!s}")
                continue

        # Sort by similarity descending
        results.sort(key=lambda x: x["similarity_value"], reverse=True)

        return {
            "query": search_query.text,
            "results": results,
            "total_results": len(results),
            "search_parameters": {"limit": search_query.limit, "min_similarity": search_query.min_similarity},
        }

    @staticmethod
    def _extract_similarity(row: dict) -> float:
        """Extract similarity value from result"""
        if isinstance(row, dict):
            return float(row.get("similarity", 0.0))
        if hasattr(row, "similarity"):
            return float(row.similarity)
        return 0.0

    @staticmethod
    def _extract_title(row: dict) -> str:
        """Extract title from result"""
        if isinstance(row, dict):
            return row.get("title", "")
        if hasattr(row, "title"):
            return str(row.title)
        return ""

    @staticmethod
    def _extract_chunk_id(row: dict) -> int:
        """Extract chunk ID from result"""
        if isinstance(row, dict):
            return int(row.get("id", 0))
        if hasattr(row, "id"):
            return int(row.id)
        return 0

    @staticmethod
    def _extract_content(row: dict) -> str:
        """Extract content from result"""
        if isinstance(row, dict):
            return row.get("content", "")
        if hasattr(row, "content"):
            return str(row.content)
        return ""
