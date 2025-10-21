from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from app.domain.common import Embedding
from app.domain.documents.chunk_metadata import ChunkMetadataFilterDict
from app.domain.libraries.indexed_chunk import IndexedChunk


@dataclass
class VectorIndex(ABC):
    """Interface for indexing strategies"""

    @abstractmethod
    def build(self, chunks: List[IndexedChunk]) -> None:
        """Build the vector index from the provided chunks"""
        ...

    @abstractmethod
    def search(
        self, query: Embedding, k: int, filters: ChunkMetadataFilterDict | None = None
    ) -> List[IndexedChunk]:
        """Search the index for the k most similar chunks to the query embedding"""
        ...

    @abstractmethod
    def clear(self) -> None:
        """Clear the index"""
        ...

    @abstractmethod
    def get_chunks(self) -> List[IndexedChunk]:
        """Return the chunks currently stored in the index."""
        ...
