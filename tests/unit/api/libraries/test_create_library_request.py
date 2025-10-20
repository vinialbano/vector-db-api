from app.api.libraries.v1.create_library import (
    CreateLibraryRequest,
    create_library,
)
from app.application.libraries import CreateLibraryHandler
from app.domain.documents import Document, DocumentMetadata
from app.domain.documents.document_id import DocumentId
from app.infrastructure import InMemoryDocumentRepository, InMemoryLibraryRepository


def test_create_library_endpoint():
    library_repo = InMemoryLibraryRepository()
    handler = CreateLibraryHandler(
        library_repo, InMemoryDocumentRepository(), vector_index_factory=lambda: None
    )

    req = CreateLibraryRequest(
        metadata={
            "name": "Lib",
            "description": "desc",
        }
    )
    res = create_library(req, handler=handler)

    assert res.library_id is not None
    assert library_repo.exists(res.library_id)


def test_create_library_with_documents():
    library_repo = InMemoryLibraryRepository()
    handler = CreateLibraryHandler(
        library_repo, InMemoryDocumentRepository(), vector_index_factory=lambda: None
    )

    did = str(DocumentId.generate())
    # save a document with this id so handler validation succeeds
    doc_obj = Document(
        id=DocumentId.from_string(did), chunks=[], metadata=DocumentMetadata(title="T")
    )
    handler._document_repository.save(doc_obj)

    req = CreateLibraryRequest(
        metadata={"name": "LibDocs", "description": "desc"},
        documents=[did],
    )
    res = create_library(req, handler=handler)
    assert res.library_id is not None
    assert library_repo.exists(res.library_id)
