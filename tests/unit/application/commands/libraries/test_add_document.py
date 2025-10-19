import pytest

from vector_db_api.application.commands.libraries import (
    AddDocumentCommand,
    AddDocumentHandler,
)
from vector_db_api.infrastructure.repositories import (
    InMemoryDocumentRepository,
    InMemoryLibraryRepository,
)


def test_add_document_happy_path(library_factory, document_factory):
    lib_repo = InMemoryLibraryRepository()
    doc_repo = InMemoryDocumentRepository()

    # create a library and a document using fixtures
    lib = library_factory(name="L")
    lib_repo.save(lib)

    doc = document_factory(title="T")
    doc_repo.save(doc)

    handler = AddDocumentHandler(lib_repo, doc_repo)
    cmd = AddDocumentCommand(library_id=str(lib.id), document_id=str(doc.id))
    res = handler.handle(cmd)

    assert res.library_id == str(lib.id)
    assert res.document_id == str(doc.id)

    stored = lib_repo.find_by_id(lib.id)
    assert stored is not None
    assert stored.contains_document(doc.id)


def test_add_document_missing_library_raises(document_factory):
    lib_repo = InMemoryLibraryRepository()
    doc_repo = InMemoryDocumentRepository()

    doc = document_factory(title="T")
    doc_repo.save(doc)

    handler = AddDocumentHandler(lib_repo, doc_repo)
    cmd = AddDocumentCommand(library_id="non-existent", document_id=str(doc.id))
    with pytest.raises(ValueError):
        handler.handle(cmd)


def test_add_document_missing_document_raises(library_factory):
    lib_repo = InMemoryLibraryRepository()
    doc_repo = InMemoryDocumentRepository()

    lib = library_factory(name="L")
    lib_repo.save(lib)

    handler = AddDocumentHandler(lib_repo, doc_repo)
    cmd = AddDocumentCommand(library_id=str(lib.id), document_id="non-existent")
    with pytest.raises(ValueError):
        handler.handle(cmd)


def test_add_document_duplicate_raises(library_factory, document_factory):
    """Adding the same document twice should raise a ValueError from the domain."""
    lib_repo = InMemoryLibraryRepository()
    doc_repo = InMemoryDocumentRepository()

    lib = library_factory(name="L")
    lib_repo.save(lib)

    doc = document_factory(title="T")
    doc_repo.save(doc)

    handler = AddDocumentHandler(lib_repo, doc_repo)
    cmd = AddDocumentCommand(library_id=str(lib.id), document_id=str(doc.id))
    # first add succeeds
    handler.handle(cmd)

    # second add should raise (Library.add_document enforces uniqueness)
    with pytest.raises(ValueError):
        handler.handle(cmd)
