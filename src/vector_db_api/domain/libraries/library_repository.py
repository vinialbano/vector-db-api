from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from vector_db_api.domain.libraries.library import Library
from vector_db_api.domain.libraries.library_id import LibraryId


class LibraryRepository(ABC):
    """Repository contract for Library aggregate"""

    @abstractmethod
    def save(self, library: Library) -> None:
        """Save or update library"""
        raise NotImplementedError()

    @abstractmethod
    def find_by_id(self, library_id: LibraryId) -> Optional[Library]:
        """Find library by ID"""
        raise NotImplementedError()

    @abstractmethod
    def find_all(self) -> List[Library]:
        """Get all libraries"""
        raise NotImplementedError()

    @abstractmethod
    def delete(self, library_id: LibraryId) -> bool:
        """Delete library, return True if existed"""
        raise NotImplementedError()

    @abstractmethod
    def exists(self, library_id: LibraryId) -> bool:
        """Check if library exists"""
        raise NotImplementedError()
