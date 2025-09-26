from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from .exceptions import (
    ChunkContentEmptyException,
    DocumentContentEmptyException,
    DocumentTitleEmptyException,
)
from .value_objects import DocumentTitle, Embedding


@dataclass
class Document:
    id: Optional[int] = None
    title: str = ""
    content: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    chunks: list["DocumentChunk"] = field(default_factory=list)

    def __post_init__(self):
        if not self.title.strip():
            raise DocumentTitleEmptyException
        if not self.content.strip():
            raise DocumentContentEmptyException

    def add_chunk(self, chunk: "DocumentChunk") -> None:
        """Add a chunk to the document"""
        if chunk.document_id != self.id:
            raise ValueError("Chunk must belong to this document")
        self.chunks.append(chunk)

    def is_empty(self) -> bool:
        """Check if document is empty"""
        return not self.content.strip()

    def word_count(self) -> int:
        """Count words in the document"""
        return len(self.content.split())

    def get_title(self) -> DocumentTitle:
        """Get title as value object"""
        return DocumentTitle(self.title)

    def has_chunks(self) -> bool:
        """Check if document has chunks"""
        return len(self.chunks) > 0


@dataclass
class DocumentChunk:
    id: Optional[int] = None
    document_id: Optional[int] = None
    content: str = ""
    embedding: Optional[list[float]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if not self.content.strip():
            raise ChunkContentEmptyException

    def has_embedding(self) -> bool:
        """Check if chunk has embedding"""
        return self.embedding is not None and len(self.embedding) > 0

    def get_embedding(self) -> Optional[Embedding]:
        """Get embedding as value object"""
        if self.has_embedding():
            return Embedding(self.embedding)
        return None

    def set_embedding(self, embedding: Embedding) -> None:
        """Set embedding from value object"""
        self.embedding = embedding.to_list()

    def similarity_to(self, other_embedding: list[float]) -> float:
        """Calculate similarity with another embedding"""
        if not self.has_embedding():
            raise ValueError("This chunk has no embedding")

        current_embedding = self.get_embedding()
        other_embedding_obj = Embedding(other_embedding)
        return current_embedding.cosine_similarity(other_embedding_obj)

    def word_count(self) -> int:
        """Count words in the chunk"""
        return len(self.content.split())
