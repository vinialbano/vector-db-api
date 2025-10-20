import pytest

from app.application.documents import DeleteChunkCommand, DeleteChunkHandler
from app.infrastructure import InMemoryDocumentRepository


def test_delete_chunk_happy_path(document_factory, chunk_factory):
    repo = InMemoryDocumentRepository()
    c1 = chunk_factory(text="a")
    c2 = chunk_factory(text="b")
    doc = document_factory(chunks=[c1, c2])
    repo.save(doc)

    handler = DeleteChunkHandler(repo)
    result = handler.handle(
        DeleteChunkCommand(document_id=str(doc.id), chunk_id=str(c2.id))
    )

    assert result is None
    updated = repo.find_by_id(doc.id)
    assert updated is not None
    assert updated.chunk_count == 1
    assert updated.contains_chunk(c1.id)


def test_delete_last_chunk_allowed(document_factory, chunk_factory):
    repo = InMemoryDocumentRepository()
    c1 = chunk_factory(text="only")
    doc = document_factory(chunks=[c1])
    repo.save(doc)

    handler = DeleteChunkHandler(repo)
    result = handler.handle(
        DeleteChunkCommand(document_id=str(doc.id), chunk_id=str(c1.id))
    )

    assert result is None
    updated = repo.find_by_id(doc.id)
    assert updated is not None
    assert updated.chunk_count == 0


def test_delete_chunk_not_found_raises(document_factory, chunk_factory):
    repo = InMemoryDocumentRepository()
    c1 = chunk_factory()
    doc = document_factory(chunks=[c1])
    repo.save(doc)

    handler = DeleteChunkHandler(repo)

    with pytest.raises(ValueError):
        handler.handle(
            DeleteChunkCommand(
                document_id=str(doc.id), chunk_id="00000000-0000-0000-0000-000000000000"
            )
        )
