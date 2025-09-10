import logging

from fastapi import APIRouter, Depends, Query

from src.api.v1.dependencies import get_search_documents_use_case
from src.api.v1.schemas import SearchResultItem
from src.application.search_document import SearchDocumentsUseCase

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get(
    "/search/",
    response_model=list[SearchResultItem],
    summary="Semantic search over document chunks",
    description=(
        "Compute the embedding of the query and return the most similar chunks stored in PostgreSQL (pgvector) "
        "using the `<->` distance operator."
    ),
    response_description="List of matched chunks ranked by similarity",
)
def search_documents(
    query: str,
    limit: int = 5,
    min_similarity: float = Query(0.0, ge=0.0, le=1.0, description="Filter out results below this similarity [0..1]"),
    use_case: SearchDocumentsUseCase = Depends(get_search_documents_use_case),
) -> list[SearchResultItem]:
    """Search for top-N similar chunks to the given query (limit default = 5)."""
    results = use_case.execute(query, limit, min_similarity)
    logger.info(f"Search results: {results}")
    return [SearchResultItem.model_validate(item) for item in results]
