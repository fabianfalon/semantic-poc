import logging
from typing import ClassVar

from langchain.text_splitter import RecursiveCharacterTextSplitter

from src.domain.content_text_spliter import ContentTextSplitter

logger = logging.getLogger(__name__)


class LangchainTextSplitter(ContentTextSplitter):
    CHUNK_SIZE: ClassVar[int] = 100  # chunk length
    OVERLAP: ClassVar[int] = 10  # chunk overlap length
    SEPARATORS: ClassVar[list[str]] = ["\n", "\n\n", "", " "]

    def split(self, text: str) -> list[str]:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.CHUNK_SIZE, chunk_overlap=self.OVERLAP, separators=self.SEPARATORS
        )
        raw_chunks = text_splitter.split_text(text)
        logger.info(f"Split text into {len(raw_chunks)} chunks")
        return raw_chunks
