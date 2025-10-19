from dataclasses import dataclass
from typing import Any, Dict, Optional

from vector_db_api.domain.libraries import LibraryId, LibraryRepository


@dataclass
class UpdateLibraryCommand:
    library_id: str
    name: Optional[str] = None
    description: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = None


@dataclass
class UpdateLibraryResult:
    library_id: str


@dataclass
class UpdateLibraryHandler:
    _repository: LibraryRepository

    def handle(self, command: UpdateLibraryCommand) -> UpdateLibraryResult:
        lib_id = LibraryId.from_string(command.library_id)
        library = self._repository.find_by_id(lib_id)
        if library is None:
            raise ValueError(f"Library {command.library_id} not found")

        library.update_metadata(
            name=command.name,
            description=command.description,
            custom_fields=command.custom_fields,
        )
        self._repository.save(library)

        return UpdateLibraryResult(library_id=str(lib_id))
