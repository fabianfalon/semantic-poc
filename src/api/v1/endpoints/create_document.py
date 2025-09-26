import logging

from fastapi import APIRouter, Depends, HTTPException

from src.api.v1.dependencies import get_create_document_use_case
from src.api.v1.exceptions import handle_domain_exception
from src.api.v1.schemas import DocumentCreateRequest, DocumentCreateResponse
from src.application.create_document import CreateDocumentUseCase
from src.domain.exceptions import DomainException

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
    try:
        result = use_case.execute(payload.title, payload.text)
        logger.info(f"Document created successfully: {result['document']['id']}")
        return DocumentCreateResponse.model_validate(result)
    except DomainException as exc:
        logger.warning(f"Domain exception: {exc!s}")
        raise handle_domain_exception(exc) from exc
    except Exception as exc:
        logger.error(f"Unexpected error: {exc!s}")
        raise HTTPException(status_code=500, detail="Internal server error") from exc
