from app.api.libraries.delete_library import delete_library
from app.application.libraries import DeleteLibraryHandler
from app.infrastructure import InMemoryLibraryRepository


def test_delete_library_endpoint(library_factory):
    repo = InMemoryLibraryRepository()
    handler = DeleteLibraryHandler(repo)

    lib = library_factory(name="L")
    repo.save(lib)

    res = delete_library(library_id=str(lib.id), handler=handler)
    assert res is None
    assert not repo.exists(lib.id)
