from app.application.documents import (
    GetDocumentHandler,
    GetDocumentQuery,
)
from app.errors import InvalidEntityError
from app.infrastructure import InMemoryDocumentRepository


def test_get_document_happy_path(document_factory):
    repo = InMemoryDocumentRepository()
    doc = document_factory()
    repo.save(doc)

    handler = GetDocumentHandler(repo)
    res = handler.handle(GetDocumentQuery(document_id=str(doc.id)))
    assert res is not None
    assert res.document_id == str(doc.id)
    assert res.chunk_count == doc.chunk_count
    assert res.metadata["title"] == doc.metadata.title
    # check chunks serialization
    assert len(res.chunks) == len(doc.chunks)
    assert res.chunks[0]["chunk_id"] == str(doc.chunks[0].id)
    assert res.chunks[0]["text"] == doc.chunks[0].text


def test_get_document_not_found():
    repo = InMemoryDocumentRepository()
    handler = GetDocumentHandler(repo)

    try:
        handler.handle(GetDocumentQuery(document_id="non-existent"))
        assert False, "expected InvalidEntityError"
    except InvalidEntityError:
        pass
