from vector_db_api.application.queries.documents import (
    GetChunkQuery,
    GetChunkHandler,
)
from vector_db_api.infrastructure.repositories import InMemoryDocumentRepository


def test_get_chunk_happy_path(document_factory):
    repo = InMemoryDocumentRepository()
    doc = document_factory()
    repo.save(doc)

    handler = GetChunkHandler(repo)
    res = handler.handle(
        GetChunkQuery(document_id=str(doc.id), chunk_id=str(doc.chunks[0].id))
    )
    assert res.chunk is not None
    assert res.chunk.id == doc.chunks[0].id


def test_get_chunk_not_found(document_factory):
    repo = InMemoryDocumentRepository()
    doc = document_factory()
    repo.save(doc)

    handler = GetChunkHandler(repo)
    try:
        handler.handle(GetChunkQuery(document_id=str(doc.id), chunk_id="non-existent"))
        assert False, "expected ValueError"
    except ValueError:
        pass
