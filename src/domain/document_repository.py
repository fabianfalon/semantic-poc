from abc import ABC, abstractmethod
from typing import Optional

from src.domain.document import Document, DocumentChunk


class DocumentRepository(ABC):
    """Interfaz del repositorio de documentos"""

    @abstractmethod
    def save_document(self, doc: Document) -> Document:
        """Persistir un documento y retornar la entidad almacenada"""
        pass

    @abstractmethod
    def get_document(self, doc_id: int) -> Optional[Document]:
        """Obtener un documento por su ID"""
        pass

    @abstractmethod
    def get_all_documents(self, limit: int = 100, offset: int = 0) -> list[Document]:
        """Obtener todos los documentos con paginación"""
        pass

    @abstractmethod
    def delete_document(self, doc_id: int) -> bool:
        """Eliminar un documento por su ID"""
        pass

    @abstractmethod
    def document_exists(self, doc_id: int) -> bool:
        """Verificar si un documento existe"""
        pass

    @abstractmethod
    def save_chunk(self, chunk: DocumentChunk) -> DocumentChunk:
        """Persistir un chunk asociado a un documento"""
        pass

    @abstractmethod
    def get_chunks_by_document(self, document_id: int) -> list[DocumentChunk]:
        """Obtener todos los chunks de un documento"""
        pass

    @abstractmethod
    def get_chunk(self, chunk_id: int) -> Optional[DocumentChunk]:
        """Obtener un chunk por su ID"""
        pass

    @abstractmethod
    def delete_chunk(self, chunk_id: int) -> bool:
        """Eliminar un chunk por su ID"""
        pass

    @abstractmethod
    def search_similar(self, query_embedding: list[float], limit: int = 5, min_similarity: float = 0.0) -> list[dict]:
        """Buscar chunks similares a un embedding dado; retorna filas con 'similarity' en [0..1]"""
        pass

    @abstractmethod
    def get_chunks_without_embeddings(self, limit: int = 100) -> list[DocumentChunk]:
        """Obtener chunks que no tienen embeddings"""
        pass

    @abstractmethod
    def update_chunk_embedding(self, chunk_id: int, embedding: list[float]) -> bool:
        """Actualizar el embedding de un chunk"""
        pass
