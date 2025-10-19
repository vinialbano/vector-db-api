from dataclasses import dataclass
from typing import Any, Callable, Dict, TypedDict

from app.domain.libraries import (
    Library,
    LibraryId,
    LibraryMetadata,
    LibraryRepository,
    VectorIndex,
)


@dataclass
class CreateLibraryCommand:
    class LibraryMetadataInput(TypedDict):
        name: str
        description: str
        custom_fields: Dict[str, Any]

    metadata: LibraryMetadataInput


@dataclass
class CreateLibraryResult:
    library_id: str


@dataclass
class CreateLibraryHandler:
    _repository: LibraryRepository
    vector_index_factory: Callable[[], VectorIndex]

    def handle(self, command: CreateLibraryCommand) -> CreateLibraryResult:
        meta = command.metadata or {}
        name = meta.get("name")
        description = meta.get("description")
        custom_fields = meta.get("custom_fields", {}) or {}

        vector_index = self.vector_index_factory()
        library = Library(
            id=LibraryId.generate(),
            documents=[],
            metadata=LibraryMetadata(
                name=name,
                description=description,
                custom_fields=custom_fields,
            ),
            vector_index=vector_index,
        )

        self._repository.save(library)

        return CreateLibraryResult(library_id=str(library.id))
