from vector_db_api.api.libraries.v1.delete_library import delete_library
from vector_db_api.application.libraries import DeleteLibraryHandler
from vector_db_api.infrastructure import InMemoryLibraryRepository


def test_delete_library_endpoint(library_factory):
    repo = InMemoryLibraryRepository()
    handler = DeleteLibraryHandler(repo)

    lib = library_factory(name="L")
    repo.save(lib)

    res = delete_library(library_id=str(lib.id), handler=handler)
    assert res.library_id == str(lib.id)
    assert res.deleted is True
    assert not repo.exists(lib.id)
