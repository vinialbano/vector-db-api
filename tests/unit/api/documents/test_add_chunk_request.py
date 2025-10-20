from app.api.documents.v1.add_chunk import (
    AddChunkRequest,
    add_chunk,
)
from app.application.documents import AddChunkHandler
from app.infrastructure import InMemoryDocumentRepository


def test_add_chunk_endpoint(document_factory):
    repo = InMemoryDocumentRepository()
    handler = AddChunkHandler(repo)

    doc = document_factory()
    repo.save(doc)

    req = AddChunkRequest(text="chunk text", embedding=[1.0, 0.0], metadata={})
    res = add_chunk(document_id=str(doc.id), request=req, handler=handler)

    assert res.chunk_id is not None
