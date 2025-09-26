import math
from dataclasses import dataclass

from .exceptions import (
    DocumentTitleEmptyException,
    EmbeddingEmptyException,
    SearchQueryEmptyException,
    SearchQueryInvalidException,
)


@dataclass(frozen=True)
class Embedding:
    """Value Object for embeddings"""

    values: list[float]

    def __post_init__(self):
        if not self.values:
            raise EmbeddingEmptyException
        if any(not isinstance(v, (int, float)) for v in self.values):
            raise ValueError("All values must be numbers")

    def cosine_similarity(self, other: "Embedding") -> float:
        """Calculate cosine similarity with another embedding"""
        if len(self.values) != len(other.values):
            raise ValueError("Embeddings must have the same dimension")

        dot_product = sum(a * b for a, b in zip(self.values, other.values))
        magnitude_a = math.sqrt(sum(a * a for a in self.values))
        magnitude_b = math.sqrt(sum(b * b for b in other.values))

        if magnitude_a == 0 or magnitude_b == 0:
            return 0.0

        return dot_product / (magnitude_a * magnitude_b)

    def to_list(self) -> list[float]:
        """Convert to list for database compatibility"""
        return self.values.copy()


@dataclass(frozen=True)
class DocumentTitle:
    """Value Object for document titles"""

    value: str

    def __post_init__(self):
        if not self.value.strip():
            raise DocumentTitleEmptyException
        if len(self.value) > 255:
            raise ValueError("Title cannot exceed 255 characters")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class SearchQuery:
    """Value Object for search queries"""

    text: str
    limit: int = 5
    min_similarity: float = 0.0

    def __post_init__(self):
        if not self.text.strip():
            raise SearchQueryEmptyException
        if self.limit <= 0:
            raise SearchQueryInvalidException("Limit must be greater than 0")
        if not 0 <= self.min_similarity <= 1:
            raise SearchQueryInvalidException("Minimum similarity must be between 0 and 1")

    def __str__(self) -> str:
        return self.text
