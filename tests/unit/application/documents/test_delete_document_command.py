from app.application.documents import (
    DeleteDocumentCommand,
    DeleteDocumentHandler,
)
from app.domain.documents import Document, DocumentId, DocumentMetadata
from app.errors import NotFoundError
from app.infrastructure import InMemoryDocumentRepository


def test_delete_existing_document():
    repo = InMemoryDocumentRepository()
    # create and save a document
    doc = Document(
        id=DocumentId.generate(), chunks=[], metadata=DocumentMetadata(title="t")
    )
    repo.save(doc)

    handler = DeleteDocumentHandler(repo)
    cmd = DeleteDocumentCommand(document_id=str(doc.id))

    result = handler.handle(cmd)
    assert result is None
    assert not repo.exists(doc.id)


def test_delete_nonexistent_document():
    repo = InMemoryDocumentRepository()
    handler = DeleteDocumentHandler(repo)
    fake_id = str(DocumentId.generate())

    try:
        handler.handle(DeleteDocumentCommand(document_id=fake_id))
        assert False, "expected NotFoundError"
    except NotFoundError:
        pass
