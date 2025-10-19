from vector_db_api.api.libraries.v1.update_library import (
    UpdateLibraryRequest,
    update_library,
)
from vector_db_api.infrastructure import InMemoryLibraryRepository
from vector_db_api.application.libraries import UpdateLibraryHandler


def test_update_library_endpoint(library_factory):
    repo = InMemoryLibraryRepository()
    handler = UpdateLibraryHandler(repo)

    lib = library_factory(name="L")
    repo.save(lib)

    req = UpdateLibraryRequest(name="New name")
    res = update_library(library_id=str(lib.id), request=req, handler=handler)

    assert res.library_id == str(lib.id)
    updated = repo.find_by_id(lib.id)
    assert updated is not None
    assert updated.metadata.name == "New name"
