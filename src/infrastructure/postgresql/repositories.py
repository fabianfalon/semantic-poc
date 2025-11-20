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
    def save_document(self, doc: Document) -> Document:
        db_doc = DocumentORM(title=doc.title, content=doc.content)
        self.db.add(db_doc)
        self.db.commit()
        self.db.refresh(db_doc)

        # Convertir ORM a entidad de dominio
        return Document(
            id=db_doc.id,
            title=db_doc.title,
            content=db_doc.content,
            created_at=db_doc.created_at,
            updated_at=db_doc.updated_at,
        )

    def get_document(self, doc_id: int) -> Document | None:
        db_doc = self.db.query(DocumentORM).filter(DocumentORM.id == doc_id).first()
        if not db_doc:
            return None

        return Document(
            id=db_doc.id,
            title=db_doc.title,
            content=db_doc.content,
            created_at=db_doc.created_at,
            updated_at=db_doc.updated_at,
        )

    def get_all_documents(self, limit: int = 100, offset: int = 0) -> list[Document]:
        db_docs = self.db.query(DocumentORM).offset(offset).limit(limit).all()
        return [
            Document(
                id=doc.id, title=doc.title, content=doc.content, created_at=doc.created_at, updated_at=doc.updated_at
            )
            for doc in db_docs
        ]

    def delete_document(self, doc_id: int) -> bool:
        try:
            db_doc = self.db.query(DocumentORM).filter(DocumentORM.id == doc_id).first()
            if db_doc:
                self.db.delete(db_doc)
                self.db.commit()
                return True
            return False
        except Exception:
            self.db.rollback()
            return False

    def document_exists(self, doc_id: int) -> bool:
        return self.db.query(DocumentORM).filter(DocumentORM.id == doc_id).first() is not None

    # -------- Chunks ----------
    def save_chunk(self, chunk: DocumentChunk) -> DocumentChunk:
        db_chunk = DocumentChunkORM(
            document_id=chunk.document_id,
            content=chunk.content,
            embedding=chunk.embedding,
        )
        self.db.add(db_chunk)
        self.db.commit()
        self.db.refresh(db_chunk)

        return DocumentChunk(
            id=db_chunk.id,
            document_id=db_chunk.document_id,
            content=db_chunk.content,
            embedding=db_chunk.embedding,
            created_at=db_chunk.created_at,
            updated_at=db_chunk.updated_at,
        )

    def get_chunks_by_document(self, document_id: int) -> list[DocumentChunk]:
        db_chunks = self.db.query(DocumentChunkORM).filter(DocumentChunkORM.document_id == document_id).all()

        return [
            DocumentChunk(
                id=chunk.id,
                document_id=chunk.document_id,
                content=chunk.content,
                embedding=chunk.embedding,
                created_at=chunk.created_at,
                updated_at=chunk.updated_at,
            )
            for chunk in db_chunks
        ]

    def get_chunk(self, chunk_id: int) -> DocumentChunk | None:
        db_chunk = self.db.query(DocumentChunkORM).filter(DocumentChunkORM.id == chunk_id).first()
        if not db_chunk:
            return None

        return DocumentChunk(
            id=db_chunk.id,
            document_id=db_chunk.document_id,
            content=db_chunk.content,
            embedding=db_chunk.embedding,
            created_at=db_chunk.created_at,
            updated_at=db_chunk.updated_at,
        )

    def delete_chunk(self, chunk_id: int) -> bool:
        try:
            db_chunk = self.db.query(DocumentChunkORM).filter(DocumentChunkORM.id == chunk_id).first()
            if db_chunk:
                self.db.delete(db_chunk)
                self.db.commit()
                return True
            return False
        except Exception:
            self.db.rollback()
            return False

    def get_chunks_without_embeddings(self, limit: int = 100) -> list[DocumentChunk]:
        db_chunks = self.db.query(DocumentChunkORM).filter(DocumentChunkORM.embedding.is_(None)).limit(limit).all()

        return [
            DocumentChunk(
                id=chunk.id,
                document_id=chunk.document_id,
                content=chunk.content,
                embedding=chunk.embedding,
                created_at=chunk.created_at,
                updated_at=chunk.updated_at,
            )
            for chunk in db_chunks
        ]

    def update_chunk_embedding(self, chunk_id: int, embedding: list[float]) -> bool:
        try:
            db_chunk = self.db.query(DocumentChunkORM).filter(DocumentChunkORM.id == chunk_id).first()
            if db_chunk:
                db_chunk.embedding = embedding
                self.db.commit()
                return True
            return False
        except Exception:
            self.db.rollback()
            return False

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
