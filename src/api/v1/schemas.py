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


class DocumentChunkResponse(BaseModel):
    id: int
    content: str


class DocumentCreateResponse(BaseModel):
    document: DocumentResponse
    chunks: list[DocumentChunkResponse]


class SearchResultItem(BaseModel):
    chunk_id: int
    document_title: str
    content: str
    similarity: str
