from app.errors import NotFoundError
from app.infrastructure import InMemoryLibraryRepository


def test_inmemory_repository_crud(library_factory):
    repo = InMemoryLibraryRepository()

    lib = library_factory(documents=[])
    assert not repo.exists(lib.id)

    repo.save(lib)
    assert repo.exists(lib.id)

    found = repo.find_by_id(lib.id)
    assert found is lib

    all_libs = repo.find_all()
    assert lib in all_libs

    repo.delete(lib.id)
    assert not repo.exists(lib.id)

    # deleting again should raise NotFoundError

    try:
        repo.delete(lib.id)
        assert False, "expected NotFoundError"
    except NotFoundError:
        pass
