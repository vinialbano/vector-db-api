from __future__ import annotations

from typing import Dict, List, Optional

from app.domain.libraries import Library, LibraryId
from app.domain.libraries.library_repository import LibraryRepository


class InMemoryLibraryRepository(LibraryRepository):
    def __init__(self):
        self._store: Dict[str, Library] = {}

    def save(self, library: Library) -> None:
        self._store[str(library.id)] = library

    def find_by_id(self, library_id: LibraryId) -> Optional[Library]:
        return self._store.get(str(library_id))

    def find_all(self) -> List[Library]:
        return list(self._store.values())

    def delete(self, library_id: LibraryId) -> None:
        removed = self._store.pop(str(library_id), None)
        if removed is None:
            raise ValueError(f"Library {library_id} not found")

    def exists(self, library_id: LibraryId) -> bool:
        return str(library_id) in self._store
