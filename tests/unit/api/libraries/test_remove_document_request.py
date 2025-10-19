from vector_db_api.api.libraries import (
    remove_document,
)
from vector_db_api.infrastructure.repositories import (
    InMemoryLibraryRepository,
    InMemoryDocumentRepository,
)
from vector_db_api.application.libraries import RemoveDocumentHandler


def test_remove_document_endpoint(library_factory, document_factory):
    lib_repo = InMemoryLibraryRepository()
    doc_repo = InMemoryDocumentRepository()

    lib = library_factory(name="L")
    doc = document_factory()
    doc_repo.save(doc)

    # attach doc to library
    lib.add_document(doc.id)
    lib_repo.save(lib)

    handler = RemoveDocumentHandler(lib_repo, doc_repo)
    res = remove_document(
        library_id=str(lib.id), document_id=str(doc.id), handler=handler
    )

    assert res.library_id == str(lib.id)
    assert res.document_id == str(doc.id)
    assert res.removed is True
