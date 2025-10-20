from dataclasses import dataclass
from typing import Any, Dict, Optional

from app.domain.libraries import LibraryId, LibraryRepository
from app.errors import NotFoundError


@dataclass
class UpdateLibraryCommand:
    library_id: str
    name: Optional[str] = None
    description: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = None


@dataclass
class UpdateLibraryHandler:
    _repository: LibraryRepository

    def handle(self, command: UpdateLibraryCommand) -> None:
        lib_id = LibraryId.from_string(command.library_id)
        library = self._repository.find_by_id(lib_id)
        if library is None:
            raise NotFoundError(f"Library {command.library_id} not found")

        library.update_metadata(
            name=command.name,
            description=command.description,
            custom_fields=command.custom_fields,
        )
        self._repository.save(library)
