from vector_db_api.presentation.api.commands.libraries.delete_library import (
    delete_library,
)
from vector_db_api.infrastructure.repositories import InMemoryLibraryRepository
from vector_db_api.application.commands.libraries import DeleteLibraryHandler
# using library_factory fixture


def test_delete_library_endpoint(library_factory):
    repo = InMemoryLibraryRepository()
    handler = DeleteLibraryHandler(repo)

    lib = library_factory(name="L")
    repo.save(lib)

    res = delete_library(library_id=str(lib.id), handler=handler)
    assert res.library_id == str(lib.id)
    assert res.deleted is True
    assert not repo.exists(lib.id)
