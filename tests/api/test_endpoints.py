from fastapi.testclient import TestClient

from src.main import app
from src.api.v1.dependencies import get_create_document_use_case, get_search_documents_use_case
from src.application.create_document import CreateDocumentUseCase
from src.application.search_document import SearchDocumentsUseCase
from src.domain.content_text_spliter import ContentTextSplitter
from src.domain.document import Document, DocumentChunk
from src.domain.document_repository import DocumentRepository


class FakeSplitter(ContentTextSplitter):
    def split(self, text: str) -> list[str]:
        return [text]


class FakeRepo(DocumentRepository):
    def __init__(self):
        self._doc_id = 0
        self._chunk_id = 0
        self.docs: list[Document] = []
        self.chunks: list[DocumentChunk] = []

    def save_document(self, doc: Document) -> Document:
        self._doc_id += 1
        persisted = Document(id=self._doc_id, title=doc.title, content=doc.content)
        self.docs.append(persisted)
        return persisted

    def get_document(self, doc_id: int) -> Document | None:
        for d in self.docs:
            if d.id == doc_id:
                return d
        return None

    def save_chunk(self, chunk: DocumentChunk) -> DocumentChunk:
        self._chunk_id += 1
        persisted = DocumentChunk(
            id=self._chunk_id, document_id=chunk.document_id, content=chunk.content, embedding=[0.0] * 3072
        )
        self.chunks.append(persisted)
        return persisted

    def search_similar(self, query_embedding: list[float], limit: int = 5) -> list[dict]:
        # Return the last chunk as the top match
        if not self.chunks:
            return []
        last = self.chunks[-1]
        return [
            {
                "id": last.id,
                "document_id": last.document_id,
                "content": last.content,
                "title": self.docs[-1].title if self.docs else "",
                "distance": 0.01,
            }
        ]


def get_fake_create_uc() -> CreateDocumentUseCase:
    return CreateDocumentUseCase(FakeRepo(), FakeSplitter())


def get_fake_search_uc() -> SearchDocumentsUseCase:
    return SearchDocumentsUseCase(FakeRepo())


app.dependency_overrides[get_create_document_use_case] = get_fake_create_uc
app.dependency_overrides[get_search_documents_use_case] = get_fake_search_uc

client = TestClient(app)


def test_create_document_endpoint():
    resp = client.post(
        "/v1/documents/",
        json={"title": "T", "text": "content"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["document"]["title"] == "T"
    assert isinstance(data["chunks"], list)


def test_search_endpoint():
    # Seed create to have something to search
    client.post("/v1/documents/", json={"title": "Doc", "text": "hello world"})
    resp = client.get("/v1/search/?query=hello&limit=5")
    assert resp.status_code == 200
    results = resp.json()
    assert isinstance(results, list)
    if results:
        assert "chunk_id" in results[0]
        assert "document_title" in results[0] 