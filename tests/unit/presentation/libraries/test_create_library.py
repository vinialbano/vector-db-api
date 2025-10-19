from vector_db_api.presentation.api.commands.libraries.create_library import (
    CreateLibraryRequest,
    create_library,
)
from vector_db_api.infrastructure.repositories import InMemoryLibraryRepository
from vector_db_api.application.commands.libraries import CreateLibraryHandler


def test_create_library_endpoint():
    repo = InMemoryLibraryRepository()
    handler = CreateLibraryHandler(repo, vector_index_factory=lambda: None)

    req = CreateLibraryRequest(name="Lib", description="desc")
    res = create_library(req, handler=handler)

    assert res.library_id is not None
    assert repo.exists(res.library_id)
