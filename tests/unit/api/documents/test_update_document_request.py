from app.api.documents.update_document import (
    UpdateDocumentRequest,
    update_document,
)
from app.application.documents import UpdateDocumentHandler
from app.infrastructure import InMemoryDocumentRepository


def test_update_document_endpoint(document_factory):
    repo = InMemoryDocumentRepository()
    handler = UpdateDocumentHandler(repo)

    doc = document_factory()
    repo.save(doc)

    req = UpdateDocumentRequest(title="New title")
    res = update_document(document_id=str(doc.id), request=req, handler=handler)

    assert res is None
    updated = repo.find_by_id(doc.id)
    assert updated is not None
    assert updated.metadata.title == "New title"
