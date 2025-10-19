from app.application.libraries import (
    GetLibraryQuery,
    GetLibraryHandler,
)
from app.infrastructure import InMemoryLibraryRepository


def test_get_library_happy_path(library_factory):
    repo = InMemoryLibraryRepository()
    lib = library_factory()
    repo.save(lib)

    handler = GetLibraryHandler(repo)
    res = handler.handle(GetLibraryQuery(library_id=str(lib.id)))
    assert res.library is not None
    assert res.library.id == lib.id


def test_get_library_not_found():
    repo = InMemoryLibraryRepository()
    handler = GetLibraryHandler(repo)
    try:
        handler.handle(GetLibraryQuery(library_id="non-existent"))
        assert False, "expected ValueError"
    except ValueError:
        pass
