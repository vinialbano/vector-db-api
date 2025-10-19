from app.api.documents.v1.get_document import get_document
from app.application.documents import GetDocumentHandler
from app.infrastructure import InMemoryDocumentRepository


def test_get_document_presentation(document_factory):
    repo = InMemoryDocumentRepository()
    doc = document_factory()
    repo.save(doc)

    handler = GetDocumentHandler(repo)
    res = get_document(document_id=str(doc.id), handler=handler)
    assert res.document_id == str(doc.id)
