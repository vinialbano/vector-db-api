from app.application.documents import (
    GetChunkHandler,
    GetChunkQuery,
)
from app.infrastructure import InMemoryDocumentRepository


def test_get_chunk_happy_path(document_factory):
    repo = InMemoryDocumentRepository()
    doc = document_factory()
    repo.save(doc)

    handler = GetChunkHandler(repo)
    res = handler.handle(
        GetChunkQuery(document_id=str(doc.id), chunk_id=str(doc.chunks[0].id))
    )
    assert res is not None
    assert res.chunk_id == str(doc.chunks[0].id)
    assert res.text == doc.chunks[0].text
    assert res.embedding == list(doc.chunks[0].embedding.values)
    assert res.metadata["source"] == doc.chunks[0].metadata.source
    assert res.metadata["page_number"] == doc.chunks[0].metadata.page_number
    assert res.metadata["created_at"] == doc.chunks[0].metadata.created_at.isoformat()
    assert res.metadata["updated_at"] == doc.chunks[0].metadata.updated_at.isoformat()
    assert res.metadata["custom_fields"] == dict(doc.chunks[0].metadata.custom_fields)


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
