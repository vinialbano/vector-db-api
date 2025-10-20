import pytest

from app.application.libraries import (
    CreateLibraryCommand,
    CreateLibraryHandler,
)
from app.domain.documents import Document, DocumentMetadata
from app.domain.documents.document_id import DocumentId
from app.domain.libraries import BruteForceIndex
from app.errors import InvalidEntityError
from app.infrastructure import InMemoryDocumentRepository, InMemoryLibraryRepository


def test_create_library_happy_path():
    library_repo = InMemoryLibraryRepository()
    document_repo = InMemoryDocumentRepository()
    handler = CreateLibraryHandler(
        library_repo,
        document_repo,
        vector_index_factory=lambda: BruteForceIndex(),
    )

    cmd = CreateLibraryCommand(metadata={"name": "L", "description": "desc"})
    result = handler.handle(cmd)

    assert library_repo.exists(result.library_id)
    lib = library_repo.find_by_id(result.library_id)
    assert lib is not None
    assert lib.metadata.name == "L"
    assert lib.document_count == 0


def test_create_library_with_documents():
    library_repo = InMemoryLibraryRepository()
    document_repo = InMemoryDocumentRepository()
    handler = CreateLibraryHandler(
        library_repo,
        document_repo,
        vector_index_factory=lambda: BruteForceIndex(),
    )

    did = str(DocumentId.generate())
    # persist a document with this id so the handler's validation passes
    doc_id_obj = DocumentId.from_string(did)
    doc = Document(id=doc_id_obj, chunks=[], metadata=DocumentMetadata(title="T"))
    # save into the in-memory document repository used by the handler
    handler._document_repository.save(doc)
    cmd = CreateLibraryCommand(
        metadata={"name": "L2", "description": "desc"}, documents=[did]
    )
    result = handler.handle(cmd)

    lib = library_repo.find_by_id(result.library_id)
    assert lib is not None
    assert lib.document_count == 1


def test_create_library_empty_name_raises():
    library_repo = InMemoryLibraryRepository()
    document_repo = InMemoryDocumentRepository()
    handler = CreateLibraryHandler(
        library_repo,
        document_repo,
        vector_index_factory=lambda: BruteForceIndex(),
    )

    cmd = CreateLibraryCommand(metadata={"name": "", "description": "desc"})

    with pytest.raises(InvalidEntityError):
        handler.handle(cmd)
