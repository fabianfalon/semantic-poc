from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    bindparam,
    func,
    text,
)
from sqlalchemy.orm import relationship

from src.domain.document import Document, DocumentChunk
from src.domain.document_repository import (
    DocumentRepository as DocumentRepositoryInterface,
)

from ..database import Base, SessionLocal


# ORM: Document
class DocumentORM(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    chunks = relationship("DocumentChunkORM", back_populates="document")


# ORM: DocumentChunk
class DocumentChunkORM(Base):
    __tablename__ = "document_chunks"
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(768))
    # embedding = Column(Vector(3072), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    document = relationship("DocumentORM", back_populates="chunks")


class PostgresDocumentRepository(DocumentRepositoryInterface):
    def __init__(self):
        self.db = SessionLocal()

    # -------- Documents ----------
    def save_document(self, doc: Document) -> DocumentORM:
        db_doc = DocumentORM(title=doc.title, content=doc.content)
        self.db.add(db_doc)
        self.db.commit()
        self.db.refresh(db_doc)
        return db_doc

    def get_document(self, doc_id: int) -> DocumentORM | None:
        return self.db.query(DocumentORM).filter(DocumentORM.id == doc_id).first()

    # -------- Chunks ----------
    def save_chunk(self, chunk: DocumentChunk) -> DocumentChunkORM:
        db_chunk = DocumentChunkORM(
            document_id=chunk.document_id,
            content=chunk.content,
            embedding=chunk.embedding,
        )
        self.db.add(db_chunk)
        self.db.commit()
        self.db.refresh(db_chunk)
        return db_chunk

    def search_similar(self, query_embedding: list[float], limit: int = 5, min_similarity: float = 0.3) -> list[dict]:
        sql = text(
            """
            SELECT c.id AS id,
                   c.document_id AS document_id,
                   c.content AS content,
                   d.title AS title,
                   (1 - (c.embedding <=> :query)) AS similarity
            FROM document_chunks c
            JOIN documents d ON d.id = c.document_id
            WHERE (1 - (c.embedding <=> :query)) >= :min_similarity
            ORDER BY (c.embedding <=> :query) ASC
            LIMIT :limit
            """
        ).bindparams(
            bindparam("query", value=query_embedding, type_=Vector(768)),
            bindparam("min_similarity", value=min_similarity, type_=Float),
            bindparam("limit", value=limit, type_=Integer),
        )
        return self.db.execute(sql).mappings().all()
