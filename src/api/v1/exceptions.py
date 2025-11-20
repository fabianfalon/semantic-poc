"""Exception handler for API"""

from fastapi import HTTPException, status

from src.domain.exceptions import (
    ChunkContentEmptyException,
    ChunkNotBelongsToDocumentException,
    ChunkSaveException,
    DocumentContentEmptyException,
    DocumentNotFoundError,
    DocumentProcessingException,
    DocumentSaveException,
    DocumentTitleEmptyException,
    DocumentTooShortException,
    DomainException,
    EmbeddingEmptyException,
    EmbeddingGenerationException,
    SearchQueryEmptyException,
    SearchQueryInvalidException,
)


def handle_domain_exception(exception: DomainException) -> HTTPException:
    """Convert domain exceptions to HTTP exceptions"""

    # Validation errors (400 Bad Request)
    if isinstance(
        exception,
        (
            DocumentTitleEmptyException,
            DocumentContentEmptyException,
            DocumentTooShortException,
            SearchQueryEmptyException,
            SearchQueryInvalidException,
            ChunkContentEmptyException,
            EmbeddingEmptyException,
        ),
    ):
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exception))

    # Processing errors (422 Unprocessable Entity)
    if isinstance(exception, (DocumentProcessingException, EmbeddingGenerationException)):
        return HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exception))

    # Persistence errors (500 Internal Server Error)
    if isinstance(exception, (DocumentSaveException, ChunkSaveException)):
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exception))

    # Resource not found (404 Not Found)
    if isinstance(exception, DocumentNotFoundError):
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exception))

    # Business logic errors (409 Conflict)
    if isinstance(exception, ChunkNotBelongsToDocumentException):
        return HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exception))

    # Generic domain error (400 Bad Request)
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exception))
