from vector_db_api.api.libraries.add_document import (
    add_document,
)
from vector_db_api.infrastructure.repositories import (
    InMemoryLibraryRepository,
    InMemoryDocumentRepository,
)
from vector_db_api.application.libraries import AddDocumentHandler


def test_add_document_endpoint(library_factory, document_factory):
    lib_repo = InMemoryLibraryRepository()
    doc_repo = InMemoryDocumentRepository()

    lib = library_factory(name="L")
    lib_repo.save(lib)

    doc = document_factory()
    doc_repo.save(doc)

    handler = AddDocumentHandler(lib_repo, doc_repo)
    res = add_document(library_id=str(lib.id), document_id=str(doc.id), handler=handler)

    assert res.library_id == str(lib.id)
    assert res.document_id == str(doc.id)
