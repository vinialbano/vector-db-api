from dataclasses import dataclass

from app.domain.libraries import LibraryId, LibraryRepository


@dataclass
class DeleteLibraryCommand:
    library_id: str


@dataclass
class DeleteLibraryResult:
    library_id: str
    deleted: bool


@dataclass
class DeleteLibraryHandler:
    _repository: LibraryRepository

    def handle(self, command: DeleteLibraryCommand) -> DeleteLibraryResult:
        library_id = LibraryId.from_string(command.library_id)
        deleted = self._repository.delete(library_id)
        return DeleteLibraryResult(library_id=str(library_id), deleted=deleted)
