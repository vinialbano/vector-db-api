import pytest

from app.application.documents import (
    CreateDocumentCommand,
    CreateDocumentHandler,
)
from app.errors import InvalidEntityError
from app.infrastructure import InMemoryDocumentRepository


def test_create_document_happy_path():
    repo = InMemoryDocumentRepository()
    handler = CreateDocumentHandler(repo)

    cmd = CreateDocumentCommand(
        metadata={"title": "T"},
        chunks=[{"text": "hello", "embedding": [1.0, 0.0], "metadata": {}}],
    )

    dto = handler.handle(cmd)
    # ensure persisted
    assert repo.exists(dto.document_id)
    doc = repo.find_by_id(dto.document_id)
    assert doc is not None
    assert doc.metadata.title == "T"
    assert doc.chunk_count == 1


def test_create_document_with_empty_chunk_text_raises():
    repo = InMemoryDocumentRepository()
    handler = CreateDocumentHandler(repo)

    cmd = CreateDocumentCommand(
        metadata={"title": "T"},
        chunks=[{"text": "   ", "embedding": [1.0, 0.0], "metadata": {}}],
    )

    with pytest.raises(InvalidEntityError):
        handler.handle(cmd)
