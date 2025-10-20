from dataclasses import dataclass

from app.domain.libraries import LibraryId, LibraryRepository


@dataclass
class DeleteLibraryCommand:
    library_id: str


@dataclass
class DeleteLibraryHandler:
    _repository: LibraryRepository

    def handle(self, command: DeleteLibraryCommand) -> None:
        library_id = LibraryId.from_string(command.library_id)
        self._repository.delete(library_id)
