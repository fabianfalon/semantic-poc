from datetime import datetime

from src.domain.document import Document, DocumentChunk


def test_document_defaults():
    doc = Document(title="T", content="C")
    assert doc.id is None
    assert doc.title == "T"
    assert doc.content == "C"
    assert isinstance(doc.created_at, (type(None), datetime))
    assert isinstance(doc.updated_at, (type(None), datetime))


def test_document_chunk_defaults():
    chunk = DocumentChunk(document_id=1, content="chunk", embedding=[0.1, 0.2])
    assert chunk.id is None
    assert chunk.document_id == 1
    assert chunk.content == "chunk"
    assert isinstance(chunk.created_at, (type(None), datetime))
    assert isinstance(chunk.updated_at, (type(None), datetime)) 