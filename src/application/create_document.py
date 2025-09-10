import logging

from src.domain.content_text_spliter import ContentTextSplitter
from src.domain.document import Document, DocumentChunk
from src.domain.document_repository import DocumentRepository
from src.domain.embeddings import EmbeddingGenerator

logger = logging.getLogger(__name__)


class CreateDocumentUseCase:
    def __init__(self, repository: DocumentRepository, splitter: ContentTextSplitter, embeddings: EmbeddingGenerator):
        self.repo = repository
        self.splitter = splitter
        self.embeddings = embeddings

    def execute(self, title: str, content: str) -> dict:
        # Persist document
        doc = Document(title=title, content=content)
        saved_doc = self.repo.save_document(doc)
        logger.info(f"Document created: {saved_doc}")

        # Split content and generate embeddings
        chunks = self.splitter.split(content)
        logger.info(f"Content split into {len(chunks)} chunks")
        vectors = self.embeddings.embed(chunks)
        saved_chunks = []

        for chunk, emb in zip(chunks, vectors):
            chunk_obj = DocumentChunk(document_id=saved_doc.id, content=chunk, embedding=emb)
            saved_chunk = self.repo.save_chunk(chunk_obj)
            saved_chunks.append(saved_chunk)
        logger.info(f"Chunks saved: {saved_chunks}")
        return {
            "document": {
                "id": saved_doc.id,
                "title": saved_doc.title,
                "content": saved_doc.content,
                "created_at": saved_doc.created_at,
                "updated_at": saved_doc.updated_at,
            },
            "chunks": [{"id": c.id, "content": c.content} for c in saved_chunks],
        }
