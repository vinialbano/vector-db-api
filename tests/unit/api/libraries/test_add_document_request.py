from app.api.libraries.add_document import (
    add_document,
)

from app.application.libraries import AddDocumentHandler
from app.infrastructure import (
    InMemoryDocumentRepository,
    InMemoryLibraryRepository,
)


def test_add_document_endpoint(library_factory, document_factory):
    lib_repo = InMemoryLibraryRepository()
    doc_repo = InMemoryDocumentRepository()

    lib = library_factory(name="L")
    lib_repo.save(lib)

    doc = document_factory()
    doc_repo.save(doc)

    handler = AddDocumentHandler(lib_repo, doc_repo)
    res = add_document(library_id=str(lib.id), document_id=str(doc.id), handler=handler)

    assert res is None
