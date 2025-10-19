from vector_db_api.api.libraries.index_library import (
    index_library,
)
from vector_db_api.infrastructure.repositories import InMemoryLibraryRepository
from vector_db_api.application.libraries import IndexLibraryHandler


def test_index_library_endpoint(library_factory):
    repo = InMemoryLibraryRepository()

    class DummyIndexer:
        def index(self, library):
            # no-op index: mark library as indexed via domain method
            try:
                library.index([])
            except Exception:
                # ignore domain errors for this unit test
                pass

    handler = IndexLibraryHandler(repo, DummyIndexer())

    lib = library_factory(name="L")
    repo.save(lib)

    res = index_library(library_id=str(lib.id), handler=handler)
    assert res.library_id == str(lib.id)
