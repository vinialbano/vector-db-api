from vector_db_api.api.documents.v1.delete_document import (
    delete_document,
)
from vector_db_api.application.documents import DeleteDocumentHandler
from vector_db_api.infrastructure import InMemoryDocumentRepository


def test_delete_document_endpoint(document_factory):
    repo = InMemoryDocumentRepository()
    handler = DeleteDocumentHandler(repo)

    doc = document_factory()
    repo.save(doc)

    res = delete_document(document_id=str(doc.id), handler=handler)
    assert res.document_id == str(doc.id)
    assert not repo.exists(doc.id)
