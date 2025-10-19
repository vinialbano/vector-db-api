from vector_db_api.application.documents import (
    UpdateDocumentCommand,
    UpdateDocumentHandler,
)
from vector_db_api.domain.documents import Document, DocumentId, DocumentMetadata
from vector_db_api.infrastructure.repositories import InMemoryDocumentRepository


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

    dto = handler.handle(cmd)
    assert dto.document_id == str(doc.id)

    updated = repo.find_by_id(doc.id)
    assert updated is not None
    assert updated.metadata.title == "New Title"
    assert updated.metadata.author == "Author"


def test_update_document_not_found_raises():
    repo = InMemoryDocumentRepository()
    handler = UpdateDocumentHandler(repo)

    fake = str(DocumentId.generate())
    try:
        handler.handle(UpdateDocumentCommand(document_id=fake, title="x"))
        raised = False
    except ValueError:
        raised = True

    assert raised
