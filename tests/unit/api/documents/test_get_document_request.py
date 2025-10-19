from vector_db_api.api.documents import get_document
from vector_db_api.application.documents import GetDocumentHandler
from vector_db_api.infrastructure import InMemoryDocumentRepository


def test_get_document_presentation(document_factory):
    repo = InMemoryDocumentRepository()
    doc = document_factory()
    repo.save(doc)

    handler = GetDocumentHandler(repo)
    res = get_document(document_id=str(doc.id), handler=handler)
    assert res.document_id == str(doc.id)
