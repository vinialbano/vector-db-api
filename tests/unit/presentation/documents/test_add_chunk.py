from vector_db_api.presentation.api.commands.documents.add_chunk import (
    AddChunkRequest,
    add_chunk,
)
from vector_db_api.infrastructure.repositories import InMemoryDocumentRepository
from vector_db_api.application.commands.documents import AddChunkHandler


def test_add_chunk_endpoint(document_factory):
    repo = InMemoryDocumentRepository()
    handler = AddChunkHandler(repo)

    doc = document_factory()
    repo.save(doc)

    req = AddChunkRequest(text="chunk text", embedding=[1.0, 0.0], metadata={})
    res = add_chunk(document_id=str(doc.id), request=req, handler=handler)

    assert res.document_id == str(doc.id)
    assert res.chunk_id is not None
