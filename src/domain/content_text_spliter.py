from abc import ABC, abstractmethod


class ContentTextSplitter(ABC):
    @abstractmethod
    def split(self, text: str) -> list[str]:
        """Split raw text into chunks"""
        pass
