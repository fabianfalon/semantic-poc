from dataclasses import dataclass
from datetime import datetime


@dataclass
class Document:
    id: int | None = None
    title: str | None = None
    content: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class DocumentChunk:
    id: int | None = None
    document_id: int | None = None
    content: str | None = None
    embedding: list[float] | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
