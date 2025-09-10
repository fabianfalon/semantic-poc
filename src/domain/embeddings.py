from abc import ABC, abstractmethod


class EmbeddingGenerator(ABC):
    @abstractmethod
    def embed(self, texts: list[str]) -> list[list[float]]:
        """Return one embedding per input text"""
        pass
