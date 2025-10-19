from dataclasses import dataclass
from typing import Callable

from vector_db_api.domain.libraries import (
    Library,
    LibraryId,
    LibraryMetadata,
    LibraryRepository,
    VectorIndex,
)


@dataclass
class CreateLibraryCommand:
    name: str
    description: str


@dataclass
class CreateLibraryResult:
    library_id: str


@dataclass
class CreateLibraryHandler:
    _repository: LibraryRepository
    vector_index_factory: Callable[[], VectorIndex]

    def handle(self, command: CreateLibraryCommand) -> CreateLibraryResult:
        vector_index = self.vector_index_factory()
        library = Library(
            id=LibraryId.generate(),
            documents=[],
            metadata=LibraryMetadata(
                name=command.name, description=command.description
            ),
            vector_index=vector_index,
        )

        self._repository.save(library)

        return CreateLibraryResult(
            library_id=str(library.id),
        )
