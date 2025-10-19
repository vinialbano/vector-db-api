from vector_db_api.api.documents.update_document import (
    UpdateDocumentRequest,
    update_document,
)
from vector_db_api.infrastructure.repositories import InMemoryDocumentRepository
from vector_db_api.application.documents import UpdateDocumentHandler


def test_update_document_endpoint(document_factory):
    repo = InMemoryDocumentRepository()
    handler = UpdateDocumentHandler(repo)

    doc = document_factory()
    repo.save(doc)

    req = UpdateDocumentRequest(title="New title")
    res = update_document(document_id=str(doc.id), request=req, handler=handler)

    assert res.document_id == str(doc.id)
    updated = repo.find_by_id(doc.id)
    assert updated is not None
    assert updated.metadata.title == "New title"
