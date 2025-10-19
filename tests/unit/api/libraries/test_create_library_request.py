from app.api.libraries.v1.create_library import (
    CreateLibraryRequest,
    create_library,
)
from app.application.libraries import CreateLibraryHandler
from app.infrastructure import InMemoryLibraryRepository


def test_create_library_endpoint():
    repo = InMemoryLibraryRepository()
    handler = CreateLibraryHandler(repo, vector_index_factory=lambda: None)

    req = CreateLibraryRequest(
        metadata={
            "name": "Lib",
            "description": "desc",
        }
    )
    res = create_library(req, handler=handler)

    assert res.library_id is not None
    assert repo.exists(res.library_id)
