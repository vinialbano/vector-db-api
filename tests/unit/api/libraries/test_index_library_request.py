from app.api.libraries.index_library import index_library

from app.application.libraries import IndexLibraryHandler
from app.infrastructure import InMemoryLibraryRepository


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
    assert res is None
