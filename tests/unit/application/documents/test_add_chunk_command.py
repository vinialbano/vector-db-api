import pytest

from vector_db_api.application.documents import (
    AddChunkCommand,
    AddChunkHandler,
)
from vector_db_api.infrastructure.repositories import InMemoryDocumentRepository


def test_add_chunk_happy_path(document_factory):
    repo = InMemoryDocumentRepository()
    handler = AddChunkHandler(repo)

    # create and persist a document
    doc = document_factory()
    repo.save(doc)

    cmd = AddChunkCommand(
        document_id=str(doc.id),
        text="New chunk",
        embedding=[1.0, 0.0],
        metadata={},
    )

    result = handler.handle(cmd)

    # ensure persisted and chunk added
    saved = repo.find_by_id(doc.id)
    assert saved is not None
    assert saved.chunk_count == 2  # document_factory creates 1 chunk by default
    # returned dto references should match
    assert result.document_id == str(doc.id)
    assert isinstance(result.chunk_id, str)

    # verify chunk content and metadata defaults
    added = saved.chunks[-1]
    assert added.text == "New chunk"
    assert added.metadata.source == "unknown"


def test_add_chunk_document_not_found():
    repo = InMemoryDocumentRepository()
    handler = AddChunkHandler(repo)

    cmd = AddChunkCommand(
        document_id="00000000-0000-0000-0000-000000000000",
        text="New chunk",
        embedding=[1.0, 0.0],
        metadata={},
    )

    with pytest.raises(ValueError):
        handler.handle(cmd)


def test_add_chunk_empty_text_raises(document_factory):
    repo = InMemoryDocumentRepository()
    handler = AddChunkHandler(repo)

    doc = document_factory()
    repo.save(doc)

    cmd = AddChunkCommand(
        document_id=str(doc.id),
        text="   ",
        embedding=[1.0, 0.0],
        metadata={},
    )

    with pytest.raises(ValueError):
        handler.handle(cmd)
