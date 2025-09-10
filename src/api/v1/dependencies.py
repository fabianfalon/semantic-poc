import os

from fastapi import Depends

from src.application.create_document import CreateDocumentUseCase
from src.application.search_document import SearchDocumentsUseCase
from src.config import settings
from src.domain.embeddings import EmbeddingGenerator
from src.infrastructure.embeddings.mock_generator import MockEmbeddingGenerator
from src.infrastructure.embeddings.openai_generator import OpenAIEmbeddingGenerator
from src.infrastructure.postgresql.repositories import PostgresDocumentRepository
from src.infrastructure.splitter.langchain_text_splitter import LangchainTextSplitter


def get_postgresql_document_repository() -> PostgresDocumentRepository:
    return PostgresDocumentRepository()


def get_text_splitter() -> LangchainTextSplitter:
    return LangchainTextSplitter()


def get_embedding_generator() -> EmbeddingGenerator:
    use_mock = (
        getattr(settings, "use_embedding_mock", False) or os.getenv("USE_EMBEDDINGS_MOCK", "false").lower() == "true"
    )
    if use_mock:
        return MockEmbeddingGenerator(dims=3072)
    api_key = getattr(settings, "open_api_key", None) or os.getenv("OPENAI_API_KEY")
    return OpenAIEmbeddingGenerator(api_key=api_key)


def get_create_document_use_case(
    repository: PostgresDocumentRepository = Depends(get_postgresql_document_repository),
    splitter: LangchainTextSplitter = Depends(get_text_splitter),
    embeddings: EmbeddingGenerator = Depends(get_embedding_generator),
) -> CreateDocumentUseCase:
    return CreateDocumentUseCase(repository, splitter, embeddings)


def get_search_documents_use_case(
    repository: PostgresDocumentRepository = Depends(get_postgresql_document_repository),
    embeddings: EmbeddingGenerator = Depends(get_embedding_generator),
) -> SearchDocumentsUseCase:
    return SearchDocumentsUseCase(repository, embeddings)
