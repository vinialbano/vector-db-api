from dataclasses import dataclass

from app.domain.libraries import LibraryId, LibraryIndexerService, LibraryRepository
from app.errors import NotFoundError


@dataclass
class IndexLibraryCommand:
    library_id: str


@dataclass
class IndexLibraryHandler:
    _repository: LibraryRepository
    _indexer: LibraryIndexerService

    def handle(self, command: IndexLibraryCommand) -> None:
        lib_id = LibraryId.from_string(command.library_id)
        library = self._repository.find_by_id(lib_id)
        if library is None:
            raise NotFoundError(f"Library {command.library_id} not found")

        self._indexer.index(library)
        self._repository.save(library)
