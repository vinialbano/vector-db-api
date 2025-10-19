from dataclasses import dataclass

from vector_db_api.domain.libraries import LibraryId, LibraryRepository


@dataclass
class GetLibraryQuery:
    library_id: str


@dataclass
class GetLibraryResult:
    library: object


@dataclass
class GetLibraryHandler:
    _repository: LibraryRepository

    def handle(self, query: GetLibraryQuery) -> GetLibraryResult:
        lib_id = LibraryId.from_string(query.library_id)
        library = self._repository.find_by_id(lib_id)
        if library is None:
            raise ValueError(f"Library {query.library_id} not found")
        return GetLibraryResult(library=library)
