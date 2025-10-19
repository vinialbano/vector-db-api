from vector_db_api.api.libraries.get_library import get_library
from vector_db_api.application.libraries import GetLibraryHandler
from vector_db_api.infrastructure import InMemoryLibraryRepository


def test_get_library_presentation(library_factory):
    repo = InMemoryLibraryRepository()
    lib = library_factory()
    repo.save(lib)

    handler = GetLibraryHandler(repo)
    res = get_library(library_id=str(lib.id), handler=handler)
    assert res.library_id == str(lib.id)
