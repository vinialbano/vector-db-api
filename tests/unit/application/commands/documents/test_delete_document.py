from vector_db_api.application.commands.documents import (
    DeleteDocumentCommand,
    DeleteDocumentHandler,
)
from vector_db_api.domain.documents import Document, DocumentId, DocumentMetadata
from vector_db_api.infrastructure.repositories import InMemoryDocumentRepository


def test_delete_existing_document():
    repo = InMemoryDocumentRepository()
    # create and save a document
    doc = Document(
        id=DocumentId.generate(), chunks=[], metadata=DocumentMetadata(title="t")
    )
    repo.save(doc)

    handler = DeleteDocumentHandler(repo)
    cmd = DeleteDocumentCommand(document_id=str(doc.id))

    dto = handler.handle(cmd)
    assert dto.deleted is True
    assert not repo.exists(doc.id)


def test_delete_nonexistent_document():
    repo = InMemoryDocumentRepository()
    handler = DeleteDocumentHandler(repo)
    fake_id = str(DocumentId.generate())

    dto = handler.handle(DeleteDocumentCommand(document_id=fake_id))
    assert dto.deleted is False
