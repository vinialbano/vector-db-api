import pytest

from vector_db_api.application.commands.libraries import (
    RemoveDocumentCommand,
    RemoveDocumentHandler,
)
from vector_db_api.infrastructure.repositories import (
    InMemoryDocumentRepository,
    InMemoryLibraryRepository,
)


def test_remove_document_happy_path_removed_true(library_factory, document_factory):
    lib_repo = InMemoryLibraryRepository()
    doc_repo = InMemoryDocumentRepository()

    lib = library_factory(name="L")
    lib_repo.save(lib)

    doc = document_factory(title="T")
    doc_repo.save(doc)

    # add document to library first (manipulate library aggregate directly)
    lib.add_document(doc.id)
    lib_repo.save(lib)

    handler = RemoveDocumentHandler(lib_repo, doc_repo)
    cmd = RemoveDocumentCommand(library_id=str(lib.id), document_id=str(doc.id))
    res = handler.handle(cmd)

    assert res.removed is True

    stored = lib_repo.find_by_id(lib.id)
    assert stored is not None
    assert not stored.contains_document(doc.id)


def test_remove_document_happy_path_removed_false_when_not_present(
    library_factory, document_factory
):
    lib_repo = InMemoryLibraryRepository()
    doc_repo = InMemoryDocumentRepository()

    lib = library_factory(name="L")
    lib_repo.save(lib)

    doc = document_factory(title="T")
    doc_repo.save(doc)

    handler = RemoveDocumentHandler(lib_repo, doc_repo)
    cmd = RemoveDocumentCommand(library_id=str(lib.id), document_id=str(doc.id))
    res = handler.handle(cmd)

    assert res.removed is False


def test_remove_document_missing_library_raises(document_factory):
    lib_repo = InMemoryLibraryRepository()
    doc_repo = InMemoryDocumentRepository()

    doc = document_factory(title="T")
    doc_repo.save(doc)

    handler = RemoveDocumentHandler(lib_repo, doc_repo)
    cmd = RemoveDocumentCommand(library_id="non-existent", document_id=str(doc.id))
    with pytest.raises(ValueError):
        handler.handle(cmd)


def test_remove_document_missing_document_raises(library_factory):
    lib_repo = InMemoryLibraryRepository()
    doc_repo = InMemoryDocumentRepository()

    lib = library_factory(name="L")
    lib_repo.save(lib)

    handler = RemoveDocumentHandler(lib_repo, doc_repo)
    cmd = RemoveDocumentCommand(library_id=str(lib.id), document_id="non-existent")
    with pytest.raises(ValueError):
        handler.handle(cmd)
