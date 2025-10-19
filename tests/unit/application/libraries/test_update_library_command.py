from vector_db_api.application.libraries import (
    UpdateLibraryCommand,
    UpdateLibraryHandler,
)
from vector_db_api.infrastructure import InMemoryLibraryRepository


def test_update_library_updates_metadata(library_factory):
    repo = InMemoryLibraryRepository()
    library = library_factory(name="Initial")
    repo.save(library)

    handler = UpdateLibraryHandler(repo)
    cmd = UpdateLibraryCommand(
        library_id=str(library.id), name="Updated", description="New desc"
    )
    result = handler.handle(cmd)

    assert result.library_id == str(library.id)
    saved = repo.find_by_id(library.id)
    assert saved is not None
    assert saved.metadata.name == "Updated"
    assert saved.metadata.description == "New desc"
