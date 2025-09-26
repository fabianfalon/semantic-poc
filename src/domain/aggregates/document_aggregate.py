from typing import Optional

from src.domain.document import Document, DocumentChunk
from src.domain.value_objects import Embedding


class DocumentAggregate:
    """Aggregate Root for documents"""

    def __init__(self, document: Document):
        self._document = document
        self._chunks: list[DocumentChunk] = []

    @property
    def document(self) -> Document:
        return self._document

    @property
    def chunks(self) -> list[DocumentChunk]:
        return self._chunks.copy()

    @property
    def document_id(self) -> Optional[int]:
        return self._document.id

    def add_chunk(self, chunk: DocumentChunk) -> None:
        """Add chunk to aggregate"""
        if chunk.document_id != self._document.id:
            raise ValueError("Chunk must belong to this document")

        self._chunks.append(chunk)
        self._document.add_chunk(chunk)

    def add_chunks(self, chunks: list[DocumentChunk]) -> None:
        """Add multiple chunks to aggregate"""
        for chunk in chunks:
            self.add_chunk(chunk)

    def search_similar_chunks(self, query_embedding: Embedding, min_similarity: float = 0.0) -> list[DocumentChunk]:
        """Search similar chunks within the document"""
        similar_chunks = []
        for chunk in self._chunks:
            if chunk.has_embedding():
                similarity = chunk.similarity_to(query_embedding.to_list())
                if similarity >= min_similarity:
                    similar_chunks.append(chunk)

        # Sort by similarity descending
        return sorted(similar_chunks, key=lambda c: c.similarity_to(query_embedding.to_list()), reverse=True)

    def get_chunks_with_embeddings(self) -> list[DocumentChunk]:
        """Get only chunks that have embeddings"""
        return [chunk for chunk in self._chunks if chunk.has_embedding()]

    def get_chunks_without_embeddings(self) -> list[DocumentChunk]:
        """Get only chunks that don't have embeddings"""
        return [chunk for chunk in self._chunks if not chunk.has_embedding()]

    def total_word_count(self) -> int:
        """Count total words in all chunks"""
        return sum(chunk.word_count() for chunk in self._chunks)

    def is_processed(self) -> bool:
        """Check if document has been processed (has chunks with embeddings)"""
        return len(self.get_chunks_with_embeddings()) > 0

    def get_processing_status(self) -> dict:
        """Get document processing status"""
        total_chunks = len(self._chunks)
        chunks_with_embeddings = len(self.get_chunks_with_embeddings())

        return {
            "total_chunks": total_chunks,
            "chunks_with_embeddings": chunks_with_embeddings,
            "chunks_without_embeddings": total_chunks - chunks_with_embeddings,
            "is_fully_processed": total_chunks > 0 and chunks_with_embeddings == total_chunks,
            "total_words": self.total_word_count(),
        }

    def validate_integrity(self) -> bool:
        """Validate aggregate integrity"""
        # Check that all chunks belong to the document
        for chunk in self._chunks:
            if chunk.document_id != self._document.id:
                return False

        # Check that document is not empty
        return not self._document.is_empty()
