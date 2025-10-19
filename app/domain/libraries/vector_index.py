from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from app.domain.documents import Chunk, Embedding


@dataclass
class VectorIndex(ABC):
    """Interface for indexing strategies"""

    @abstractmethod
    def build(self, chunks: List[Chunk]) -> None:
        """Build the vector index from the provided chunks"""
        ...

    @abstractmethod
    def search(self, query: Embedding, k: int) -> List[Chunk]:
        """Search the index for the k most similar chunks to the query embedding"""
        ...

    @abstractmethod
    def clear(self) -> None:
        """Clear the index"""
        ...

    @abstractmethod
    def get_chunks(self) -> List[Chunk]:
        """Return the chunks currently stored in the index."""
        ...
