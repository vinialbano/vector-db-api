from vector_db_api.api.libraries.v1.create_library import (
    CreateLibraryRequest,
    create_library,
)
from vector_db_api.application.libraries import CreateLibraryHandler
from vector_db_api.infrastructure import InMemoryLibraryRepository


def test_create_library_endpoint():
    repo = InMemoryLibraryRepository()
    handler = CreateLibraryHandler(repo, vector_index_factory=lambda: None)

    req = CreateLibraryRequest(name="Lib", description="desc")
    res = create_library(req, handler=handler)

    assert res.library_id is not None
    assert repo.exists(res.library_id)
