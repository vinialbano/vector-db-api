from vector_db_api.application.documents import (
    GetDocumentQuery,
    GetDocumentHandler,
)
from vector_db_api.infrastructure import InMemoryDocumentRepository


def test_get_document_happy_path(document_factory):
    repo = InMemoryDocumentRepository()
    doc = document_factory()
    repo.save(doc)

    handler = GetDocumentHandler(repo)
    res = handler.handle(GetDocumentQuery(document_id=str(doc.id)))
    assert res.document is not None
    assert res.document.id == doc.id


def test_get_document_not_found():
    repo = InMemoryDocumentRepository()
    handler = GetDocumentHandler(repo)
    try:
        handler.handle(GetDocumentQuery(document_id="non-existent"))
        assert False, "expected ValueError"
    except ValueError:
        pass
