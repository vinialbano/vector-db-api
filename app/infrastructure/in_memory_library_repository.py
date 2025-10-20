from __future__ import annotations

from typing import Dict, List, Optional
from threading import RLock

from app.domain.libraries import Library, LibraryId
from app.domain.libraries.library_repository import LibraryRepository
from app.errors import NotFoundError


class InMemoryLibraryRepository(LibraryRepository):
    def __init__(self):
        self._store: Dict[str, Library] = {}
        self._lock = RLock()

    def save(self, library: Library) -> None:
        with self._lock:
            self._store[str(library.id)] = library

    def find_by_id(self, library_id: LibraryId) -> Optional[Library]:
        with self._lock:
            return self._store.get(str(library_id))

    def find_all(self) -> List[Library]:
        with self._lock:
            return list(self._store.values())

    def delete(self, library_id: LibraryId) -> None:
        with self._lock:
            removed = self._store.pop(str(library_id), None)
        if removed is None:
            raise NotFoundError(f"Library {library_id} not found")

    def exists(self, library_id: LibraryId) -> bool:
        with self._lock:
            return str(library_id) in self._store

    def clear(self) -> None:
        """Clear all stored libraries (thread-safe)."""
        with self._lock:
            self._store.clear()
