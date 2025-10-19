from dataclasses import dataclass

from app.domain.libraries import LibraryId, LibraryRepository, LibraryIndexerService


@dataclass
class IndexLibraryCommand:
    library_id: str


@dataclass
class IndexLibraryResult:
    library_id: str


@dataclass
class IndexLibraryHandler:
    _repository: LibraryRepository
    _indexer: LibraryIndexerService

    def handle(self, command: IndexLibraryCommand) -> IndexLibraryResult:
        lib_id = LibraryId.from_string(command.library_id)
        library = self._repository.find_by_id(lib_id)
        if library is None:
            raise ValueError(f"Library {command.library_id} not found")

        self._indexer.index(library)
        self._repository.save(library)

        return IndexLibraryResult(library_id=str(lib_id))
