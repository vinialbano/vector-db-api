from app.application.libraries import (
    DeleteLibraryCommand,
    DeleteLibraryHandler,
)
from app.domain.libraries import LibraryId
from app.infrastructure import InMemoryLibraryRepository


def test_delete_library_returns_deleted_true_when_exists(library_factory):
    repo = InMemoryLibraryRepository()
    library = library_factory()
    repo.save(library)

    handler = DeleteLibraryHandler(repo)
    cmd = DeleteLibraryCommand(library_id=str(library.id))
    result = handler.handle(cmd)

    assert result.deleted is True
    assert repo.find_by_id(library.id) is None


def test_delete_library_returns_false_when_missing():
    repo = InMemoryLibraryRepository()
    handler = DeleteLibraryHandler(repo)
    fake_id = str(LibraryId.generate())
    cmd = DeleteLibraryCommand(library_id=fake_id)
    result = handler.handle(cmd)

    assert result.deleted is False
