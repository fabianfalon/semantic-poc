import logging

from fastapi import APIRouter, Depends, HTTPException, Query

from src.api.v1.dependencies import get_search_documents_use_case
from src.api.v1.exceptions import handle_domain_exception
from src.api.v1.schemas import SearchDocumentsResponse
from src.application.search_document import SearchDocumentsUseCase
from src.domain.exceptions import DomainException

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get(
    "/search/",
    response_model=SearchDocumentsResponse,
    summary="Semantic search over document chunks",
    description=(
        "Compute the embedding of the query and return the most similar chunks stored in PostgreSQL (pgvector) "
        "using the `<->` distance operator."
    ),
    response_description="Search results with metadata",
)
def search_documents(
    query: str,
    limit: int = 5,
    min_similarity: float = Query(0.0, ge=0.0, le=1.0, description="Filter out results below this similarity [0..1]"),
    use_case: SearchDocumentsUseCase = Depends(get_search_documents_use_case),
) -> SearchDocumentsResponse:
    """Search for top-N similar chunks to the given query (limit default = 5)."""
    try:
        result = use_case.execute(query, limit, min_similarity)
        logger.info(f"Search completed: {result.get('total_results', 0)} results found")
        return SearchDocumentsResponse.model_validate(result)
    except DomainException as exc:
        logger.warning(f"Domain exception: {exc!s}")
        raise handle_domain_exception(exc) from exc
    except Exception as exc:
        logger.error(f"Unexpected error: {exc!s}")
        raise HTTPException(status_code=500, detail="Internal server error") from exc
