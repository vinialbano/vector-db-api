from app.application.libraries import (
    GetLibraryHandler,
    GetLibraryQuery,
)
from app.infrastructure import InMemoryLibraryRepository


def test_get_library_happy_path(library_factory):
    repo = InMemoryLibraryRepository()
    lib = library_factory()
    repo.save(lib)

    handler = GetLibraryHandler(repo)
    res = handler.handle(GetLibraryQuery(library_id=str(lib.id)))
    assert res is not None
    assert res.library_id == str(lib.id)
    assert res.document_ids == [str(d) for d in lib.documents]
    assert res.metadata["name"] == lib.metadata.name
    # indexed_chunks may be empty by default
    assert isinstance(res.indexed_chunks, list)


def test_get_library_not_found():
    repo = InMemoryLibraryRepository()
    handler = GetLibraryHandler(repo)
    try:
        handler.handle(GetLibraryQuery(library_id="non-existent"))
        assert False, "expected ValueError"
    except ValueError:
        pass
