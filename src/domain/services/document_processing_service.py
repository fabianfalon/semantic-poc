from src.domain.content_text_spliter import ContentTextSplitter
from src.domain.document import Document, DocumentChunk
from src.domain.embeddings import EmbeddingGenerator
from src.domain.exceptions import (
    DocumentProcessingException,
    DocumentTooShortException,
    EmbeddingGenerationException,
)
from src.domain.value_objects import Embedding


class DocumentProcessingService:
    """Domain service for document processing"""

    def __init__(self, splitter: ContentTextSplitter, embedding_generator: EmbeddingGenerator):
        self.splitter = splitter
        self.embedding_generator = embedding_generator

    def process_document(self, document: Document) -> list[DocumentChunk]:
        """Process document: split into chunks and generate embeddings"""
        if document.is_empty():
            raise DocumentProcessingException("Cannot process empty document")

        if not self.validate_document_for_processing(document):
            raise DocumentTooShortException

        try:
            # Split content
            text_chunks = self.splitter.split(document.content)

            if not text_chunks:
                raise DocumentProcessingException("Could not generate chunks from document")

            # Generate embeddings
            embeddings = self.embedding_generator.embed(text_chunks)

            if len(embeddings) != len(text_chunks):
                raise DocumentProcessingException("Number of embeddings does not match number of chunks")

            # Create domain chunks
            document_chunks = []
            for i, (text_chunk, embedding) in enumerate(zip(text_chunks, embeddings)):
                # Convert embedding to value object for validation
                embedding_obj = Embedding(embedding)

                chunk = DocumentChunk(document_id=document.id, content=text_chunk, embedding=embedding_obj.to_list())
                document_chunks.append(chunk)

            return document_chunks

        except Exception as exc:
            if isinstance(exc, DocumentProcessingException):
                raise
            raise DocumentProcessingException(f"Error during processing: {exc!s}") from exc

    def process_query(self, query: str) -> Embedding:
        """Process query and generate its embedding"""
        try:
            # embed_query now returns list[float] directly
            query_embedding = self.embedding_generator.embed_query(query)

            if not query_embedding:
                raise EmbeddingGenerationException("Could not generate embedding for query")

            return Embedding(query_embedding)

        except Exception as exc:
            if isinstance(exc, EmbeddingGenerationException):
                raise
            raise EmbeddingGenerationException(f"Error generating embedding for query: {exc!s}") from exc

    def validate_document_for_processing(self, document: Document) -> bool:
        """Validate if document can be processed"""
        return (
            not document.is_empty()
            and document.word_count() > 0
            and len(document.content.strip()) > 10  # Minimum 10 characters
        )
