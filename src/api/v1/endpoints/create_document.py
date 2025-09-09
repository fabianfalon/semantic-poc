import logging

from fastapi import APIRouter, Depends

from src.api.v1.dependencies import get_create_document_use_case
from src.api.v1.schemas import DocumentCreateRequest, DocumentCreateResponse
from src.application.create_document import CreateDocumentUseCase

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/documents/",
    response_model=DocumentCreateResponse,
    summary="Create and index a document",
    description=(
        "Ingest a document by title and long text. The text is split into chunks with LangChain, "
        "each chunk is embedded, and both the document and its chunk embeddings are persisted in PostgreSQL (pgvector)."
    ),
    response_description="Created document with stored chunk identifiers",
)
def add_document(
    payload: DocumentCreateRequest, use_case: CreateDocumentUseCase = Depends(get_create_document_use_case)
) -> DocumentCreateResponse:
    """Create a document, split content, embed chunks, and persist everything."""
    result = use_case.execute(payload.title, payload.text)
    logger.info(f"Document created: {result}")
    return DocumentCreateResponse.model_validate(result)
