import pytest

from app.application.documents import (
    UpdateChunkCommand,
    UpdateChunkHandler,
)
from app.infrastructure import InMemoryDocumentRepository


def test_update_chunk_happy_path(document_factory, chunk_factory):
    repo = InMemoryDocumentRepository()
    ch = chunk_factory(text="old")
    doc = document_factory(chunks=[ch])
    repo.save(doc)

    handler = UpdateChunkHandler(repo)
    cmd = UpdateChunkCommand(
        document_id=str(doc.id),
        chunk_id=str(ch.id),
        text="new",
        embedding=[0.0, 1.0],
        metadata={"source": "updated"},
    )

    dto = handler.handle(cmd)
    assert dto.document_id == str(doc.id)
    assert dto.chunk_id == str(ch.id)

    updated = repo.find_by_id(doc.id)
    assert updated is not None
    assert updated.chunks[0].text == "new"
    assert updated.chunks[0].metadata.source == "updated"


def test_update_chunk_not_found_raises(document_factory, chunk_factory):
    repo = InMemoryDocumentRepository()
    ch = chunk_factory(text="x")
    doc = document_factory(chunks=[ch])
    repo.save(doc)

    handler = UpdateChunkHandler(repo)
    fake_chunk_id = "00000000-0000-0000-0000-000000000000"

    with pytest.raises(ValueError):
        handler.handle(
            UpdateChunkCommand(
                document_id=str(doc.id), chunk_id=fake_chunk_id, text="no"
            )
        )
