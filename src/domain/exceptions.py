"""Domain-specific exceptions"""


class DomainException(Exception):
    """Base domain exception"""

    pass


class DocumentException(DomainException):
    """Document-related exception"""

    pass


class DocumentTitleEmptyException(DocumentException):
    """Exception when document title is empty"""

    def __init__(self):
        super().__init__("Document title cannot be empty")


class DocumentContentEmptyException(DocumentException):
    """Exception when document content is empty"""

    def __init__(self):
        super().__init__("Document content cannot be empty")


class DocumentTooShortException(DocumentException):
    """Exception when document is too short to process"""

    def __init__(self, min_length: int = 10):
        super().__init__(f"Document must have at least {min_length} characters to be processed")


class DocumentProcessingException(DocumentException):
    """Exception during document processing"""

    pass


class DocumentNotFoundError(DocumentException):
    """Exception when document is not found"""

    def __init__(self, document_id: int):
        super().__init__(f"Document with ID {document_id} not found")


class ChunkException(DomainException):
    """Chunk-related exception"""

    pass


class ChunkContentEmptyException(ChunkException):
    """Exception when chunk content is empty"""

    def __init__(self):
        super().__init__("Chunk content cannot be empty")


class ChunkNotBelongsToDocumentException(ChunkException):
    """Exception when chunk does not belong to specified document"""

    def __init__(self, chunk_id: int, document_id: int):
        super().__init__(f"Chunk {chunk_id} does not belong to document {document_id}")


class SearchException(DomainException):
    """Search-related exception"""

    pass


class SearchQueryEmptyException(SearchException):
    """Exception when search query is empty"""

    def __init__(self):
        super().__init__("Search query cannot be empty")


class SearchQueryInvalidException(SearchException):
    """Exception when search parameters are invalid"""

    def __init__(self, message: str):
        super().__init__(f"Invalid search parameters: {message}")


class EmbeddingException(DomainException):
    """Embedding-related exception"""

    pass


class EmbeddingGenerationException(EmbeddingException):
    """Exception during embedding generation"""

    def __init__(self, message: str = "Error generating embedding"):
        super().__init__(message)


class EmbeddingEmptyException(EmbeddingException):
    """Exception when embedding is empty"""

    def __init__(self):
        super().__init__("Embedding cannot be empty")


class RepositoryException(DomainException):
    """Repository-related exception"""

    pass


class DocumentSaveException(RepositoryException):
    """Exception when saving document"""

    def __init__(self, message: str = "Error saving document"):
        super().__init__(message)


class ChunkSaveException(RepositoryException):
    """Exception when saving chunk"""

    def __init__(self, message: str = "Error saving chunk"):
        super().__init__(message)
