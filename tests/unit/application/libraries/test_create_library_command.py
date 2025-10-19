import pytest

from vector_db_api.application.libraries import (
    CreateLibraryCommand,
    CreateLibraryHandler,
)
from vector_db_api.infrastructure import InMemoryLibraryRepository
from vector_db_api.domain.libraries import BruteForceIndex


def test_create_library_happy_path():
    repo = InMemoryLibraryRepository()
    handler = CreateLibraryHandler(repo, vector_index_factory=lambda: BruteForceIndex())

    cmd = CreateLibraryCommand(name="L", description="desc")
    result = handler.handle(cmd)

    assert repo.exists(result.library_id)
    lib = repo.find_by_id(result.library_id)
    assert lib is not None
    assert lib.metadata.name == "L"
    assert lib.document_count == 0


def test_create_library_empty_name_raises():
    repo = InMemoryLibraryRepository()
    handler = CreateLibraryHandler(repo, vector_index_factory=lambda: BruteForceIndex())

    cmd = CreateLibraryCommand(name="", description="desc")
    with pytest.raises(ValueError):
        handler.handle(cmd)
