import pytest

from app.application.documents import (
    UpdateDocumentCommand,
    UpdateDocumentHandler,
)
from app.domain.documents import Document, DocumentId, DocumentMetadata
from app.errors import NotFoundError
from app.infrastructure import InMemoryDocumentRepository


def test_update_document_metadata_happy_path():
    repo = InMemoryDocumentRepository()
    doc = Document(
        id=DocumentId.generate(),
        chunks=[],
        metadata=DocumentMetadata(title="T", author=None),
    )
    repo.save(doc)

    handler = UpdateDocumentHandler(repo)
    cmd = UpdateDocumentCommand(
        document_id=str(doc.id), title="New Title", author="Author"
    )

    result = handler.handle(cmd)
    assert result is None

    updated = repo.find_by_id(doc.id)
    assert updated is not None
    assert updated.metadata.title == "New Title"
    assert updated.metadata.author == "Author"


def test_update_document_not_found_raises():
    repo = InMemoryDocumentRepository()
    handler = UpdateDocumentHandler(repo)

    fake = str(DocumentId.generate())

    with pytest.raises(NotFoundError):
        handler.handle(UpdateDocumentCommand(document_id=fake, title="x"))
