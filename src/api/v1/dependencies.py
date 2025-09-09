from fastapi import Depends

from src.application.create_document import CreateDocumentUseCase
from src.application.search_document import SearchDocumentsUseCase
from src.infrastructure.postgresql.repositories import PostgresDocumentRepository
from src.infrastructure.text_splitter import LangchainTextSplitter


def get_postgresql_document_repository() -> PostgresDocumentRepository:
    return PostgresDocumentRepository()


def get_text_splitter() -> LangchainTextSplitter:
    return LangchainTextSplitter()


def get_create_document_use_case(
    repository: PostgresDocumentRepository = Depends(get_postgresql_document_repository),
    splitter: LangchainTextSplitter = Depends(get_text_splitter),
) -> CreateDocumentUseCase:
    return CreateDocumentUseCase(repository, splitter)


def get_search_documents_use_case(
    repository: PostgresDocumentRepository = Depends(get_postgresql_document_repository),
) -> SearchDocumentsUseCase:
    return SearchDocumentsUseCase(repository)
