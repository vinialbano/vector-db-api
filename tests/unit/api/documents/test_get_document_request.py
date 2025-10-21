from app.api.documents.get_document import get_document
from app.application.documents import GetDocumentHandler
from app.infrastructure import InMemoryDocumentRepository


def test_get_document_presentation(document_factory):
    repo = InMemoryDocumentRepository()
    doc = document_factory()
    repo.save(doc)

    handler = GetDocumentHandler(repo)
    res = get_document(document_id=str(doc.id), handler=handler)
    assert res.document_id == str(doc.id)
    assert res.chunk_count == doc.chunk_count
    assert res.metadata.title == doc.metadata.title
    assert len(res.chunks) == len(doc.chunks)
    assert res.chunks[0].chunk_id == str(doc.chunks[0].id)
    assert res.chunks[0].text == doc.chunks[0].text
