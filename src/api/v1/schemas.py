from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str


class DocumentCreateRequest(BaseModel):
    title: str
    text: str


class DocumentResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    word_count: int


class DocumentChunkResponse(BaseModel):
    id: int
    content: str
    has_embedding: bool
    word_count: int


class ProcessingStatusResponse(BaseModel):
    total_chunks: int
    chunks_with_embeddings: int
    chunks_without_embeddings: int
    is_fully_processed: bool
    total_words: int


class DocumentCreateResponse(BaseModel):
    document: DocumentResponse
    chunks: list[DocumentChunkResponse]
    processing_status: ProcessingStatusResponse


class SearchResultItem(BaseModel):
    chunk_id: int
    document_title: str
    content: str
    similarity: str
    similarity_value: float


class SearchParametersResponse(BaseModel):
    limit: int
    min_similarity: float


class SearchDocumentsResponse(BaseModel):
    query: str
    results: list[SearchResultItem]
    total_results: int
    search_parameters: SearchParametersResponse
