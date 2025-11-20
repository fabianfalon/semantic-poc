import logging
from typing import Any

from src.domain.aggregates.document_aggregate import DocumentAggregate
from src.domain.document import Document
from src.domain.document_repository import DocumentRepository
from src.domain.exceptions import (
    ChunkSaveException,
    DocumentSaveException,
)
from src.domain.services.document_processing_service import DocumentProcessingService

logger = logging.getLogger(__name__)


class CreateDocumentUseCase:
    """Use case for creating documents"""

    def __init__(self, repository: DocumentRepository, processing_service: DocumentProcessingService):
        self.repository = repository
        self.processing_service = processing_service

    def execute(self, title: str, content: str) -> dict[str, Any]:
        """Execute document creation use case"""

        # Create domain entity
        document = Document(title=title, content=content)

        try:
            saved_document = self.repository.save_document(document)
            logger.info(f"Document created: {saved_document.id}")
        except Exception as exc:
            logger.error(f"Error saving document: {exc!s}")
            raise DocumentSaveException(f"Error saving document: {exc!s}") from exc

        document_aggregate = DocumentAggregate(saved_document)

        # Process document (split and generate embeddings)
        chunks = self.processing_service.process_document(saved_document)

        # Add chunks to aggregate
        document_aggregate.add_chunks(chunks)

        # Persist chunks
        saved_chunks = []
        for chunk in chunks:
            try:
                chunk.document_id = saved_document.id
                saved_chunk = self.repository.save_chunk(chunk)
                saved_chunks.append(saved_chunk)
            except Exception as exc:
                logger.error(f"Error saving chunk: {exc!s}")
                raise ChunkSaveException(f"Error saving chunk: {exc!s}") from exc

        logger.info(f"Document processed with {len(saved_chunks)} chunks")

        # Get processing status
        processing_status = document_aggregate.get_processing_status()

        return {
            "document": {
                "id": saved_document.id,
                "title": saved_document.title,
                "content": saved_document.content,
                "created_at": saved_document.created_at,
                "updated_at": saved_document.updated_at,
                "word_count": saved_document.word_count(),
            },
            "chunks": [
                {
                    "id": chunk.id,
                    "content": chunk.content,
                    "has_embedding": chunk.has_embedding(),
                    "word_count": chunk.word_count(),
                }
                for chunk in saved_chunks
            ],
            "processing_status": processing_status,
        }
