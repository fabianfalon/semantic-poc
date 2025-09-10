from typing import List

from src.application.create_document import CreateDocumentUseCase
from src.domain.content_text_spliter import ContentTextSplitter
from src.domain.document import Document, DocumentChunk
from src.domain.document_repository import DocumentRepository
from src.domain.embeddings import EmbeddingGenerator


class FakeEmbeddings(EmbeddingGenerator):
    def embed(self, texts: list[str]) -> list[list[float]]:
        return [[0.0] * 3072 for _ in texts]


class FakeSplitter(ContentTextSplitter):
    def split(self, text: str) -> List[str]:
        return [text[:5], text[5:]] if text else []


class FakeRepo(DocumentRepository):
    def __init__(self):
        self.documents: list[Document] = []
        self.chunks: list[DocumentChunk] = []
        self._doc_id = 0
        self._chunk_id = 0

    def save_document(self, doc: Document) -> Document:
        self._doc_id += 1
        persisted = Document(id=self._doc_id, title=doc.title, content=doc.content)
        self.documents.append(persisted)
        return persisted

    def get_document(self, doc_id: int) -> Document | None:
        for d in self.documents:
            if d.id == doc_id:
                return d
        return None

    def save_chunk(self, chunk: DocumentChunk) -> DocumentChunk:
        self._chunk_id += 1
        persisted = DocumentChunk(
            id=self._chunk_id, document_id=chunk.document_id, content=chunk.content, embedding=chunk.embedding
        )
        self.chunks.append(persisted)
        return persisted

    def search_similar(self, query_embedding: list[float], limit: int = 5) -> list[dict]:
        return []


def test_create_document_use_case():
    repo = FakeRepo()
    splitter = FakeSplitter()
    embeddings = FakeEmbeddings()
    use_case = CreateDocumentUseCase(repo, splitter, embeddings)

    result = use_case.execute("Title", "abcdefghij")

    assert "document" in result
    assert "chunks" in result
    assert result["document"]["title"] == "Title"
    assert len(result["chunks"]) == 2
