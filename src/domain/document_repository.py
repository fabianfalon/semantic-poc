from abc import ABC, abstractmethod

from src.domain.document import Document, DocumentChunk


class DocumentRepository(ABC):
    @abstractmethod
    def save_document(self, doc: Document) -> Document:
        """Persist a document and return the stored entity"""
        pass

    @abstractmethod
    def get_document(self, doc_id: int) -> Document | None:
        """Get a document by its ID"""
        pass

    @abstractmethod
    def save_chunk(self, chunk: DocumentChunk) -> DocumentChunk:
        """Persist a chunk associated with a document"""
        pass

    @abstractmethod
    def search_similar(self, query_embedding: list[float], limit: int = 5, min_similarity: float = 0.0) -> list[dict]:
        """Search for chunks similar to a given embedding; return rows with 'similarity' in [0..1]"""
        pass
